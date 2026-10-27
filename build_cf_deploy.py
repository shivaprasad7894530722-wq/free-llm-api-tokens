#!/usr/bin/env python3
"""Build the Cloudflare MCP `execute` payload that deploys this site to
Cloudflare Pages (project: free-llm-api-tokens).

Why: the Cloudflare MCP connector cannot use the Pages asset-upload endpoint
(it returns 'Authorization failed'), so the site is shipped as a Pages
`_worker.js` that embeds index.html and data.json and serves them directly.

Usage:  python3 build_cf_deploy.py [out_path]   (default /workspace/cf_deploy_payload.js)
Then call the Cloudflare MCP tool `execute` with code = "$file:<out_path>".
"""
import json, subprocess, sys, os

here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else "/workspace/cf_deploy_payload.js"
files = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/data.json": ("data.json", "application/json; charset=utf-8"),
}
blobs = {}
for route, (fn, ct) in files.items():
    blobs[route] = {"body": open(os.path.join(here, fn), encoding="utf-8").read(), "ct": ct}

worker = """const FILES = %s;
export default {
  async fetch(request) {
    const url = new URL(request.url);
    let p = url.pathname;
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    const f = FILES[p];
    if (!f) return new Response('Not found', { status: 404, headers: { 'content-type': 'text/plain' } });
    return new Response(f.body, { headers: { 'content-type': f.ct, 'cache-control': 'public, max-age=300', 'access-control-allow-origin': '*' } });
  }
};
""" % json.dumps(blobs)

try:
    sha = subprocess.check_output(["git", "-C", here, "rev-parse", "HEAD"], text=True).strip()
    msg = subprocess.check_output(["git", "-C", here, "log", "-1", "--pretty=%s"], text=True).strip()
except Exception:
    sha, msg = "", "manual deploy"

code = """async () => {
  const P = 'free-llm-api-tokens';
  const worker = %s;
  const fields = { manifest: '{}', branch: 'main', commit_hash: %s, commit_message: %s, commit_dirty: 'false' };
  const b = '----cfpages' + Date.now();
  const parts = [];
  for (const [k, v] of Object.entries(fields)) parts.push('--' + b, `Content-Disposition: form-data; name="${k}"`, '', v);
  parts.push('--' + b, 'Content-Disposition: form-data; name="_worker.js"; filename="_worker.js"', 'Content-Type: application/javascript+module', '', worker, '--' + b + '--', '');
  const d = await cloudflare.request({ method: 'POST', path: `/accounts/${accountId}/pages/projects/${P}/deployments`, body: parts.join('\\r\\n'), contentType: 'multipart/form-data; boundary=' + b, rawBody: true });
  return { success: d.success, url: d.result && d.result.url, id: d.result && d.result.id, errors: d.errors };
}""" % (json.dumps(worker), json.dumps(sha), json.dumps(msg))
open(out, "w").write(code)
print(out, len(code), "bytes")
