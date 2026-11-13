# Free LLM API Tokens Tracker

Live sites:
- Canonical: https://freellmapi.link/ (and https://www.freellmapi.link/)
- Cloudflare Pages: https://free-llm-api-tokens.pages.dev/
- GitHub Pages (mirror, root-relative URLs may not resolve on this subpath): https://shivaprasad7894530722-wq.github.io/free-llm-api-tokens/

A static site listing sites and providers that give **free LLM API tokens**, with OpenAI compatibility, base URL, tokens per day, limits and risk flags. Updated daily. Original guides, a What’s new page with an RSS feed, per-model pages, a sitemap and machine-readable files (`data.json`, `changes.json`, `llms.txt`, `llms-full.txt`) support search and answer engines.

Figures come from each provider's own pages on the date shown. They change often, so check before you rely on them, and never share API keys. "Not published" means the provider does not publish that figure. Nothing here is invented.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Home page (generated). The provider list is pre-rendered in HTML for crawlers, then enhanced at runtime from `data.json`. |
| `data.json` | The single source of truth for provider figures. Edit only this file (or use `update.py`). |
| `content/guides/*.md` | Guide source (front matter + Markdown). `{{placeholders}}` are filled from `data.json`. |
| `content/pages/*.md` | About, Contact, Privacy and Terms source. |
| `templates/home.html` | Home page `<main>` and list script, wrapped by the generator. |
| `assets/styles.css`, `assets/site.js` | Shared theme, layout, theme toggle and copy buttons. |
| `build_site.py` | Generates HTML pages, `sitemap.xml`, `robots.txt`, `ads.txt`, `llms.txt`, `llms-full.txt`, `/new`, `/feed.xml` and `/models`. |
| `site_features.py` | Git-derived changelog and model-family mapping used by the generator. Dates and model availability are never invented. |
| `changes.json` | Machine-readable changelog written by the build from git history of `data.json`. |
| `update.py` | Daily helper: add or update a site, then runs `build_site.py`. |
| `deploy.sh` | Validate, regenerate, commit, push to GitHub, and build the Cloudflare deploy payload. |
| `build_cf_deploy.py` | Builds `/workspace/cf_deploy_payload.js` for the Cloudflare MCP `execute` tool. |
| `.nojekyll` | Tells GitHub Pages to serve files as they are. |

Generated routes (do not edit by hand; rerun `python3 build_site.py`): `/`, `/new`, `/feed.xml`, `/models`, each model family under `/models/<slug>`, `/about`, `/contact`, `/privacy`, `/terms`, `/guides/`, each guide under `/guides/<slug>`, `/sitemap.xml`, `/robots.txt`, `/ads.txt`, `/llms.txt`, `/llms-full.txt`, `/changes.json`, `/404`.

## Analytics and AdSense

1. **Google Analytics 4** is live on every generated page. The Measurement ID is `GA4_ID` in `build_site.py` (currently `G-60M3MTCPVQ`). The standard `gtag.js` snippet is printed in the HTML `<head>`.
2. **Google AdSense** is still a commented placeholder in that same head block. When approved, uncomment the AdSense `<script>` and replace `ca-pub-XXXXXXXXXXXXXXXX` (`ADSENSE_PLACEHOLDER`).
3. **ads.txt** — when AdSense is approved, uncomment the `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0` line and replace the publisher id (`ADS_TXT_PUB_PLACEHOLDER`).

After changing these values, run `python3 build_site.py` and deploy so every page picks them up.

The contact address on the site is `hello@lumiono.com`. There is no form that collects secrets.

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
./deploy.sh        # regenerates pages, validates, commits, pushes, builds /workspace/cf_deploy_payload.js
```

`update.py` and `deploy.sh` both run `build_site.py`, so sitemap `lastmod`, the “Best free LLM APIs” tables, provider fact boxes and `llms.txt` stay aligned with `data.json`.

GitHub Pages redeploys automatically within a minute or two of the push.

### Cloudflare Pages sync

Project `free-llm-api-tokens` on Cloudflare Pages (direct upload, no Git link: the
Cloudflare Pages GitHub app is not installed on the account). After `./deploy.sh`:

1. Call the Cloudflare MCP tool `execute` with `code` = `"$file:/workspace/cf_deploy_payload.js"`.
   It must return `success: true`.
2. Check: `curl -s https://free-llm-api-tokens.pages.dev/data.json | python3 -c "import json,sys;print(json.load(sys.stdin)['last_updated'])"`
   should match the local `data.json`.
3. Spot-check a new route, for example `https://free-llm-api-tokens.pages.dev/guides/` and `/privacy`.

The payload ships the site as a Pages `_worker.js` that embeds the HTML, CSS, JS, `data.json` and text files
(the MCP connector can't use the Pages asset-upload endpoint). If a `CLOUDFLARE_API_TOKEN`
with Pages:Edit is ever set, `deploy.sh` deploys with `wrangler pages deploy` instead.
To get fully automatic deploys on every push, install the Cloudflare Pages GitHub app in the
Cloudflare dashboard and connect this repo.
