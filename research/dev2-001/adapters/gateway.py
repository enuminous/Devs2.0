"""Transport for a separately audited exact-token-counting model gateway.

No model is chosen by this file. API credentials are environment variables,
never command-line arguments or browser storage. No automatic retries.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

def call(request, endpoint=None, token=None):
    endpoint=endpoint or os.environ.get('DEV2_GATEWAY_URL','')
    parsed=urllib.parse.urlparse(endpoint)
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError('credentials/fragments forbidden in gateway URL')
    if not (parsed.scheme=='https' or (parsed.scheme=='http' and parsed.hostname in ('localhost','127.0.0.1','::1'))):
        raise ValueError('use HTTPS or an explicit loopback development gateway')
    headers={'Content-Type':'application/json'}
    token=token if token is not None else os.environ.get('DEV2_GATEWAY_TOKEN')
    if token: headers['Authorization']='Bearer '+token
    req=urllib.request.Request(endpoint,data=json.dumps(request).encode(),headers=headers,method='POST')
    # Disable redirects so credentials and research prompts cannot be redirected
    # to an unintended host. Backend records are preserved by the main runner.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs): return None
    with urllib.request.build_opener(NoRedirect).open(req,timeout=120) as response:
        raw=response.read(4_000_001)
        if len(raw)>4_000_000: raise ValueError('oversized gateway response')
        return json.loads(raw)

if __name__=='__main__':
    try: print(json.dumps(call(json.load(sys.stdin))))
    except Exception:
        print('Gateway failed; inspect private server logs. No retry performed.',file=sys.stderr)
        sys.exit(1)
