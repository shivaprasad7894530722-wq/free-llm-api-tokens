#!/usr/bin/env bash
# Sync the site after a daily update: push to GitHub (GitHub Pages auto-deploys)
# and build the Cloudflare Pages deploy payload.
#
# Cloudflare step (one of):
#  A) Agent / routine with the Cloudflare MCP connector (current setup):
#       after this script, call Cloudflare MCP tool `execute` with
#       code = "$file:/workspace/cf_deploy_payload.js"
#     It returns {success, url}. Then check https://free-llm-api-tokens.pages.dev/data.json
#  B) If CLOUDFLARE_API_TOKEN (Pages:Edit) + CLOUDFLARE_ACCOUNT_ID are set in the env,
#     this script deploys directly with wrangler instead.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m json.tool data.json > /dev/null
git add -A
git diff --cached --quiet || git commit -q -m "Daily update $(TZ=Asia/Kolkata date +%F)"
git push -q origin main
python3 build_cf_deploy.py /workspace/cf_deploy_payload.js
if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  d=$(mktemp -d); cp index.html data.json "$d"/
  npx -y wrangler pages deploy "$d" --project-name free-llm-api-tokens --branch main --commit-dirty=true
  echo "Deployed with wrangler."
else
  echo "Now run Cloudflare MCP execute with code=\"\$file:/workspace/cf_deploy_payload.js\""
fi
