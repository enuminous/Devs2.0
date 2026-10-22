"""Loopback transport and accounting checks; no external model or credentials."""
import importlib.util
import json
import sys
import threading
import unittest
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('gateway',ROOT/'adapters/gateway.py')
gateway=importlib.util.module_from_spec(spec);spec.loader.exec_module(gateway)
from analyze import analyze
from core import read
from test_dev2 import synthetic_scores

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_POST(self):
        raw=self.rfile.read(int(self.headers['Content-Length']))
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','/target');self.end_headers();return
        body=json.dumps({'received':json.loads(raw),'auth':self.headers.get('Authorization')}).encode()
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)

class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_actual_loopback_json_and_header(self):
        result=gateway.call({'op':'count','input':{'question':'Software fixture'}},self.url,'TEST_FIXTURE_NOT_A_SECRET')
        self.assertEqual(result['received']['op'],'count')
        self.assertEqual(result['auth'],'Bearer TEST_FIXTURE_NOT_A_SECRET')
    def test_redirect_rejected(self):
        with self.assertRaises(urllib.error.HTTPError): gateway.call({'op':'count'},self.url+'/redirect','TEST_FIXTURE')
    def test_insecure_remote_or_url_credentials_rejected_before_request(self):
        with patch('urllib.request.build_opener') as network:
            for url in ('http://example.com','https://name:secret@example.com','https://example.com/#secret','file:///tmp/x'):
                with self.assertRaises(ValueError): gateway.call({},url)
            network.assert_not_called()
    def test_usage_distribution_and_cached_input_are_reported(self):
        scored=synthetic_scores();cfg=read(ROOT/'CONFIG.json');th=read(ROOT/'THRESHOLDS.json');th['bootstrap_draws']=100
        for r in scored['rows']: r['cached_input_tokens']=25
        result=analyze(scored,cfg,th)
        self.assertEqual(result['arms']['C']['median_tokens'],150)
        self.assertEqual(result['arms']['C']['p95_tokens'],150)
        self.assertEqual(result['arms']['C']['total_cached_input_tokens'],300)
        self.assertEqual(result['token_ratio_C_over_A'],1)
        self.assertEqual(result['verdict'],'UNVERIFIED')
