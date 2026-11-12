#!/usr/bin/env bash
# Sync the site after a daily update: regenerate derived pages, push to GitHub
# (GitHub Pages auto-deploys) and build the Cloudflare Pages deploy payload.
#
# Cloudflare step (one of):
#  A) Agent / routine with the Cloudflare MCP connector (current setup):
#       after this script, call Cloudflare MCP tool `execute` with
#       code = "$file:/workspace/cf_deploy_payload.js"
#     It returns {success, url, id}. Then check https://free-llm-api-tokens.pages.dev/
#  B) If CLOUDFLARE_API_TOKEN (Pages:Edit) + CLOUDFLARE_ACCOUNT_ID are set in the env,
#     this script deploys directly with wrangler instead.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m json.tool data.json > /dev/null
python3 build_site.py
git add -A
git diff --cached --quiet || git commit -q -m "Daily update $(TZ=Asia/Kolkata date +%F)"
git push -q origin main
python3 build_cf_deploy.py /workspace/cf_deploy_payload.js
if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  d=$(mktemp -d)
  python3 - << PY
import os, shutil
from pathlib import Path
root = Path(".").resolve()
dest = Path("$d")
skip = {".git", "content", "templates", "__pycache__"}
for p in root.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(root)
    if any(part in skip or part.startswith(".") for part in rel.parts if part != ".nojekyll"):
        continue
    if p.suffix in {".py", ".sh", ".md"} and rel.parts[0] not in {"about","contact","privacy","terms","guides","assets"}:
        # keep root markdown/scripts off the Pages upload; HTML/JSON/txt/xml/css/js only
        if p.suffix in {".py", ".sh"}:
            continue
        if p.name == "README.md":
            continue
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, target)
print("staged", sum(1 for _ in dest.rglob("*") if _.is_file()), "files in", dest)
PY
  npx -y wrangler pages deploy "$d" --project-name free-llm-api-tokens --branch main --commit-dirty=true
  echo "Deployed with wrangler."
else
  echo "Now run Cloudflare MCP execute with code=\"\$file:/workspace/cf_deploy_payload.js\""
fi
