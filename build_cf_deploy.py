#!/usr/bin/env python3
"""Build the Cloudflare MCP `execute` payload that deploys this site to
Cloudflare Pages (project: free-llm-api-tokens).

Why: the Cloudflare MCP connector cannot use the Pages asset-upload endpoint
(it returns 'Authorization failed'), so the site is shipped as a Pages
`_worker.js` that embeds the static files and serves them directly.

Usage:  python3 build_cf_deploy.py [out_path]   (default /workspace/cf_deploy_payload.js)
Then call the Cloudflare MCP tool `execute` with code = "$file:<out_path>".
"""
import json, subprocess, sys, os
from pathlib import Path

here = Path(__file__).resolve().parent
out = sys.argv[1] if len(sys.argv) > 1 else "/workspace/cf_deploy_payload.js"

CT = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
}

SKIP_DIRS = {".git", "content", "templates", "__pycache__"}
SKIP_FILES = {"build_site.py", "build_cf_deploy.py", "update.py", "deploy.sh", "README.md"}


def should_skip(rel: Path) -> bool:
    if any(part in SKIP_DIRS or (part.startswith(".") and part != ".nojekyll") for part in rel.parts):
        return True
    if rel.name in SKIP_FILES:
        return True
    if rel.suffix not in CT:
        return True
    return False


def routes_for(rel: Path):
    """Map a repo-relative file to the URL pathnames the worker should serve."""
    parts = rel.as_posix()
    if parts == "index.html":
        return ["/", "/index.html"]
    if parts == "404.html":
        return ["/404", "/404.html"]
    if rel.name == "index.html":
        folder = "/" + rel.parent.as_posix()
        return [folder, folder + "/", folder + "/index.html"]
    return ["/" + parts]


blobs = {}
for p in sorted(here.rglob("*")):
    if not p.is_file():
        continue
    rel = p.relative_to(here)
    if should_skip(rel):
        continue
    body = p.read_text(encoding="utf-8")
    ct = CT[rel.suffix]
    for route in routes_for(rel):
        if route in blobs and blobs[route]["body"] != body:
            raise SystemExit(f"route collision at {route} ({rel})")
        blobs[route] = {"body": body, "ct": ct}

worker = """const FILES = %s;
export default {
  async fetch(request) {
    const url = new URL(request.url);
    let p = url.pathname;
    if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    let f = FILES[p] || FILES[p + '/'] || FILES[url.pathname];
    if (!f) {
      const nf = FILES['/404'] || FILES['/404.html'];
      return new Response(nf ? nf.body : 'Not found', {
        status: 404,
        headers: { 'content-type': nf ? nf.ct : 'text/plain; charset=utf-8', 'cache-control': 'no-store' }
      });
    }
    return new Response(f.body, { headers: { 'content-type': f.ct, 'cache-control': 'public, max-age=300', 'access-control-allow-origin': '*' } });
  }
};
""" % json.dumps(blobs)

try:
    sha = subprocess.check_output(["git", "-C", str(here), "rev-parse", "HEAD"], text=True).strip()
    msg = subprocess.check_output(["git", "-C", str(here), "log", "-1", "--pretty=%s"], text=True).strip()
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
Path(out).write_text(code)
print(out, len(code), "bytes,", len(blobs), "routes,", len({id(b["body"]) for b in blobs.values()}), "unique bodies")
