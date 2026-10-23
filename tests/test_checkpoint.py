"""Exercise checkpoint publication without network access or credentials."""
import contextlib
import importlib.util
import io
import json
import os
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("checkpoint", Path(__file__).resolve().parents[1]/"scripts/tag_checkpoint.py")
checkpoint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checkpoint)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 40
        env = {"GITHUB_REPOSITORY": checkpoint.REPOSITORY, "GITHUB_REF": "refs/heads/main",
               "GITHUB_EVENT_NAME": "push", "GITHUB_SHA": self.sha, "GITHUB_TOKEN": "fixture-only"}
        self.enterContext(patch.dict(os.environ, env))
        self.enterContext(patch.object(checkpoint, "check"))
        self.enterContext(patch.object(checkpoint.subprocess, "check_output",
                                      side_effect=[self.sha, f"[tag-{checkpoint.TAG}]"]))
        self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def test_wrong_event_refuses_before_any_network(self):
        os.environ["GITHUB_EVENT_NAME"] = "pull_request"
        with patch.object(checkpoint.urllib.request, "urlopen") as network:
            with self.assertRaisesRegex(ValueError, "main-branch push"):
                checkpoint.publish()
        network.assert_not_called()

    def test_existing_tag_at_other_commit_never_moves(self):
        body = {"object": {"type": "commit", "sha": "b" * 40}}
        with patch.object(checkpoint.urllib.request, "urlopen", return_value=io.StringIO(json.dumps(body))) as network:
            with self.assertRaisesRegex(ValueError, "never be moved"):
                checkpoint.publish()
        self.assertEqual(network.call_count, 1)
        self.assertEqual(network.call_args.args[0].get_method(), "GET")

    def test_same_existing_tag_is_idempotent(self):
        body = {"object": {"type": "commit", "sha": self.sha}}
        with patch.object(checkpoint.urllib.request, "urlopen", return_value=io.StringIO(json.dumps(body))) as network:
            checkpoint.publish()
        self.assertEqual(network.call_count, 1)

    def test_missing_tag_creates_only_the_checked_commit(self):
        missing = urllib.error.HTTPError("fixture", 404, "missing", {}, None)
        with patch.object(checkpoint.urllib.request, "urlopen", side_effect=[missing, io.StringIO("{}")]) as network:
            checkpoint.publish()
        self.assertEqual(network.call_count, 2)
        request = network.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(json.loads(request.data), {"ref": f"refs/tags/{checkpoint.TAG}", "sha": self.sha})
