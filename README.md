# Free LLM API Tokens Tracker

Live sites:
- Cloudflare Pages (main): https://free-llm-api-tokens.pages.dev/
- GitHub Pages (mirror): https://shivaprasad7894530722-wq.github.io/free-llm-api-tokens/

A single-page static site (no build step) listing sites and providers that give **free LLM API tokens**, with OpenAI compatibility, base URL, tokens per day, limits and risk flags. Updated on weekdays.

Figures come from each provider's own pages on the date shown. They change often, so check before you rely on them, and never share API keys. "Unspecified" means the provider does not publish that figure. Nothing here is invented.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole site (vanilla HTML/CSS/JS). It loads `data.json` at runtime. |
| `data.json` | The single source of truth. Edit only this file (or use `update.py`). |
| `update.py` | Optional helper for the daily job: add or update a site and write a changelog line. |
| `deploy.sh` | Validate, commit, push to GitHub, and build the Cloudflare deploy payload. |
| `build_cf_deploy.py` | Builds `/workspace/cf_deploy_payload.js` for the Cloudflare MCP `execute` tool. |
| `.nojekyll` | Tells GitHub Pages to serve files as they are. |

## data.json schema (schema_version 1)

```jsonc
{
  "schema_version": 1,
  "last_updated": "2026-10-26T09:45:00+05:30",   // ISO 8601 with the +05:30 offset; shown on the site as IST
  "changelog": [                                  // newest first
    { "date": "2026-10-26", "items": ["Added Flexlora.", "NaraRouter free models cut from 5 to 3."] }
  ],
  "sites": [
    {
      "id": "flexlora",                 // unique slug, lowercase
      "name": "Flexlora",
      "url": "https://flexlora.com/",   // official site or pricing/docs page
      "openai_compatible": "yes",       // "yes" | "no" | "partial" | null (unknown)
      "base_url": "https://api.flexlora.com/v1",   // or "Unspecified"
      "free_allowance": "7M tokens/day (Free plan)",  // human-readable
      "tokens_per_day": 7000000,        // integer if a daily token figure is published, else null
      "limits": "15 RPM",               // RPM/RPD etc., or "Unspecified"
      "card_required": "No",            // "Yes" | "No" | "Top-up" | "Unspecified"
      "notes": "Looks like a NaraRouter rebrand.",
      "relay_risk": true,               // true = unofficial reseller/relay or unknown operator
      "category": "gateway",            // "official" (model maker/cloud) | "gateway"
      "first_reported": "2026-10-26",   // YYYY-MM-DD (IST)
      "last_updated": "2026-10-26"      // YYYY-MM-DD (IST) of the last change to this entry
    }
  ]
}
```

## Daily update

```bash
cd /workspace/free-llm-api-tokens
git pull --rebase -q
# new site
python3 update.py add --id example --name "Example" --url https://example.com/ --oai yes \
  --base https://api.example.com/v1 --allowance "1M tokens/day" --tpd 1000000 --limits "10 RPM" --card No --relay
# change to an existing site
python3 update.py set --id apinex --tpd 3000000 --allowance "3M tokens/day on free models" \
  --note-change "APInex free allowance cut from 10M to 3M tokens/day."
python3 -m json.tool data.json > /dev/null   # validate
./deploy.sh        # validates, commits, pushes to GitHub, builds /workspace/cf_deploy_payload.js
```

GitHub Pages redeploys automatically within a minute or two of the push.

### Cloudflare Pages sync

Project `free-llm-api-tokens` on Cloudflare Pages (direct upload, no Git link: the
Cloudflare Pages GitHub app is not installed on the account). After `./deploy.sh`:

1. Call the Cloudflare MCP tool `execute` with `code` = `"$file:/workspace/cf_deploy_payload.js"`.
   It must return `success: true`.
2. Check: `curl -s https://free-llm-api-tokens.pages.dev/data.json | python3 -c "import json,sys;print(json.load(sys.stdin)['last_updated'])"`
   should match the local `data.json`.

The payload ships the site as a Pages `_worker.js` that embeds `index.html` and `data.json`
(the MCP connector can't use the Pages asset-upload endpoint). If a `CLOUDFLARE_API_TOKEN`
with Pages:Edit is ever set, `deploy.sh` deploys with `wrangler pages deploy` instead.
To get fully automatic deploys on every push, install the Cloudflare Pages GitHub app in the
Cloudflare dashboard and connect this repo.
