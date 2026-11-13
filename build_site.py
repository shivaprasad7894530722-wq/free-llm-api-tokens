#!/usr/bin/env python3
"""Generate static pages, sitemap, robots.txt, _headers, ads.txt, llms.txt, og.png and the IndexNow key file.

Run from the repo root (or any cwd; paths are relative to this file):

    python3 build_site.py

Called automatically by update.py after a data.json change, and by deploy.sh
before a commit, so sitemap lastmod, the "best free LLM APIs" tables,
provider fact boxes and llms.txt stay in sync with data.json.

Do not invent quotas, prices or endpoints: generated figures come only from
data.json. Guide prose may use {{placeholders}} that are filled from the same
file.
"""
from __future__ import annotations

import datetime as dt
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
SITE = "https://freellmapi.link"
NAME = "Free LLM API Tokens Tracker"
SHORT = "Free LLM API Tokens"
CONTACT_EMAIL = "hello@lumiono.com"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))

# Google Analytics 4 is live on every generated page.
GA4_ID = "G-60M3MTCPVQ"
# AdSense remains a commented placeholder until the account is approved.
ADSENSE_PLACEHOLDER = "ca-pub-XXXXXXXXXXXXXXXX"
ADS_TXT_PUB_PLACEHOLDER = "pub-XXXXXXXXXXXXXXXX"

# Stable IndexNow key. Served at /<key>.txt (the file body is the key itself).
INDEXNOW_KEY = "8ba0054ef7ffc7621e5321a380b67bb8"
OG_IMAGE_PATH = "/og.png"
OG_IMAGE_URL = SITE + OG_IMAGE_PATH
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630

# Applied via Cloudflare Pages `_headers` and also by the `_worker.js` deploy
# path in build_cf_deploy.py (that worker is what currently serves the site).
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com https://*.google-analytics.com; "
    "connect-src 'self' https://www.google-analytics.com https://region1.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com https://*.googletagmanager.com; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "object-src 'none'; "
    "upgrade-insecure-requests"
)
DATA_USE_HEADER = (
    "Personal and research use only; no bulk commercial reuse without permission. "
    "See https://freellmapi.link/terms"
)
HEADERS_FILE = f"""/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Content-Security-Policy: {CSP}

/data.json
  X-Content-Usage: {DATA_USE_HEADER}
"""


NAV = [
    ("/", "Tracker"),
    ("/guides/", "Guides"),
    ("/about", "About"),
    ("/contact", "Contact"),
]
FOOTER = [
    ("/", "Tracker"),
    ("/guides/", "Guides"),
    ("/about", "About"),
    ("/contact", "Contact"),
    ("/privacy", "Privacy"),
    ("/terms", "Terms"),
    ("/data.json", "data.json"),
]


def load_data():
    return json.loads((HERE / "data.json").read_text(encoding="utf-8"))


def is_dropped(s: dict) -> bool:
    a = (s.get("free_allowance") or "").strip()
    return bool(re.match(r"^(DROPPED|None|No free( cloud)? tier)\b", a, re.I))


def published(v) -> str:
    if v is None or v == "" or str(v).strip().lower() == "unspecified":
        return "Not published"
    return str(v)


def fmt_date(d: str) -> str:
    if not d:
        return "—"
    y, m, dd = d.split("-")
    return dt.date(int(y), int(m), int(dd)).strftime("%-d %b %Y")


def fmt_ist(iso: str) -> str:
    try:
        d = dt.datetime.fromisoformat(iso)
    except Exception:
        return iso
    if d.tzinfo is None:
        d = d.replace(tzinfo=IST)
    return d.astimezone(IST).strftime("%-d %b %Y, %H:%M") + " IST"


def fmt_num(n) -> str:
    if n is None:
        return "Not published"
    return f"{int(n):,}"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def attr_esc(s) -> str:
    return html.escape(str(s), quote=True)


# --- markdown -------------------------------------------------------------

_INLINE = [
    (re.compile(r"`([^`]+)`"), lambda m: f"<code>{esc(m.group(1))}</code>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), lambda m: f'<a href="{attr_esc(m.group(2))}">{esc(m.group(1))}</a>'),
    (re.compile(r"\*\*([^*]+)\*\*"), lambda m: f"<strong>{esc(m.group(1))}</strong>"),
    (re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)"), lambda m: f"<em>{esc(m.group(1))}</em>"),
]


def inline(text: str) -> str:
    # Protect already-escaped or raw HTML placeholders first? Placeholders should
    # already be substituted to HTML or plain text before md_to_html.
    # Handle inline in a single pass with a placeholder for code already done.
    parts = []
    pos = 0
    token_re = re.compile(
        r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|(?<!\*)\*([^*]+)\*(?!\*)"
    )
    for m in token_re.finditer(text):
        parts.append(esc(text[pos:m.start()]))
        if m.group(1) is not None:
            parts.append(f"<code>{esc(m.group(1))}</code>")
        elif m.group(2) is not None:
            parts.append(f'<a href="{attr_esc(m.group(3))}">{esc(m.group(2))}</a>')
        elif m.group(4) is not None:
            parts.append(f"<strong>{esc(m.group(4))}</strong>")
        else:
            parts.append(f"<em>{esc(m.group(5))}</em>")
        pos = m.end()
    parts.append(esc(text[pos:]))
    return "".join(parts)


def md_to_html(src: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            code = "\n".join(buf)
            out.append(
                '<div class="snippet"><button type="button" class="copy copy-snip" data-c="'
                + attr_esc(code)
                + '">Copy</button><pre>'
                + esc(code)
                + "</pre></div>"
            )
            i += 1
            continue
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.startswith("> "):
            buf = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            out.append("<blockquote><p>" + "<br>".join(inline(x) for x in buf) + "</p></blockquote>")
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*-+", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_table(rows))
            continue
        if re.match(r"^#{1,3} ", line):
            level = len(line) - len(line.lstrip("#"))
            text = line[level + 1 :].strip()
            hid = slugify(re.sub(r"[*_`]", "", text))
            out.append(f'<h{level} id="{attr_esc(hid)}">{inline(text)}</h{level}>')
            i += 1
            continue
        if re.match(r"^[-*] ", line) or re.match(r"^\d+\. ", line):
            ordered = bool(re.match(r"^\d+\. ", line))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and (
                (ordered and re.match(r"^\d+\. ", lines[i]))
                or (not ordered and re.match(r"^[-*] ", lines[i]))
            ):
                item = re.sub(r"^([-*] |\d+\. )", "", lines[i])
                items.append("<li>" + inline(item) + "</li>")
                i += 1
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        if line.strip() == "":
            i += 1
            continue
        if re.match(r"^\{\{[A-Za-z0-9_]+\}\}$", line.strip()):
            out.append(line.strip())
            i += 1
            continue
        if line.startswith('<') and not line.startswith("<http"):
            # raw HTML block (injected tables, fact boxes)
            buf = [line]
            i += 1
            # keep raw until a blank line if it looks like an open tag block
            while i < len(lines) and lines[i].strip() != "" and (
                lines[i].startswith("<") or lines[i].startswith("  ") or buf[-1].strip() and not buf[-1].rstrip().endswith(">")
            ):
                buf.append(lines[i])
                i += 1
            # simpler: if line is raw HTML, consume until blank
            while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith("#") and not lines[i].startswith("```"):
                if lines[i].startswith("|") or re.match(r"^[-*] ", lines[i]) or re.match(r"^\d+\. ", lines[i]):
                    break
                if lines[i].startswith("<") or "<" in "".join(buf):
                    buf.append(lines[i])
                    i += 1
                    continue
                break
            out.append("\n".join(buf))
            continue
        # paragraph: join wrapped text
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^#{1,3} ", lines[i]) and not lines[i].startswith("```") and not lines[i].startswith("|") and not re.match(r"^[-*] ", lines[i]) and not re.match(r"^\d+\. ", lines[i]) and not lines[i].startswith("> ") and not re.match(r"^---+\s*$", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>" + inline(" ".join(x.strip() for x in buf)) + "</p>")
    return "\n".join(out)


def _table(rows):
    def cells(row):
        parts = [c.strip() for c in row.strip().strip("|").split("|")]
        return parts
    body = rows[:]
    # drop separator
    if len(body) > 1 and re.match(r"^\|?\s*-+", body[1]):
        header = cells(body[0])
        body = body[2:]
        thead = "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>"
    else:
        thead = ""
    trs = []
    for r in body:
        if re.match(r"^\|?\s*-+", r):
            continue
        trs.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>")
    return "<table>" + thead + "<tbody>" + "".join(trs) + "</tbody></table>"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---\n", 4)
    if end < 0:
        return {}, raw
    meta = {}
    for line in raw[4:end].split("\n"):
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, raw[end + 5 :]


# --- data helpers ---------------------------------------------------------

def oai_label(s):
    v = s.get("openai_compatible")
    return {"yes": "Yes", "no": "No", "partial": "Partial"}.get(v, "Not published")


def sites_by_id(data):
    return {s["id"]: s for s in data["sites"]}


def factbox(s: dict) -> str:
    rows = [
        ("Official site", f'<a href="{attr_esc(s["url"])}" rel="noopener">Visit {esc(s["name"])}</a>'),
        ("Category", "Official provider" if s.get("category") == "official" else "Gateway"),
        ("OpenAI compatible", esc(oai_label(s))),
        ("Free allowance", esc(published(s.get("free_allowance")))),
        ("Tokens per day", esc(fmt_num(s.get("tokens_per_day")))),
        ("Rate limits", esc(published(s.get("limits")))),
        ("Card required", esc(published(s.get("card_required")))),
        ("Base URL", esc(published(s.get("base_url"))) if not has_base(s) else f"<code>{esc(s['base_url'])}</code>"),
        ("Relay warning", "Yes — treat as a relay or reseller" if s.get("relay_risk") else "No"),
        ("First listed", esc(fmt_date(s.get("first_reported")))),
        ("Entry updated", esc(fmt_date(s.get("last_updated")))),
    ]
    if s.get("notes"):
        rows.append(("Notes", esc(s["notes"])))
    html_rows = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    return (
        f'<div class="callout"><strong>Snapshot from this tracker</strong>'
        f"Figures below are copied from our <a href=\"/\">provider list</a> "
        f"(entry last updated {esc(fmt_date(s.get('last_updated')))}). "
        f"They change often — confirm on the official site before you rely on them.</div>"
        f"<table>{html_rows}</table>"
    )


def has_base(s) -> bool:
    return bool(s.get("base_url")) and str(s.get("base_url")).strip().lower() != "unspecified"


def snippets_for(s: dict) -> str:
    if not has_base(s):
        return (
            '<p>This provider has not published a base URL in our list, so we do not invent one. '
            "Copy the endpoint from their official docs after you sign up.</p>"
        )
    base = s["base_url"]
    py = (
        "import os\n"
        "from openai import OpenAI\n\n"
        "client = OpenAI(\n"
        "    api_key=os.environ[\"API_KEY\"],\n"
        f"    base_url=\"{base}\",\n"
        ")\n\n"
        "resp = client.chat.completions.create(\n"
        "    model=\"MODEL_ID\",  # copy the model id from the provider's docs\n"
        "    messages=[{\"role\": \"user\", \"content\": \"Hello\"}],\n"
        ")\n"
        "print(resp.choices[0].message.content)\n"
    )
    js = (
        "import OpenAI from \"openai\";\n\n"
        "const client = new OpenAI({\n"
        "  apiKey: process.env.API_KEY,\n"
        f"  baseURL: \"{base}\",\n"
        "});\n\n"
        "const resp = await client.chat.completions.create({\n"
        "  model: \"MODEL_ID\", // copy the model id from the provider's docs\n"
        "  messages: [{ role: \"user\", content: \"Hello\" }],\n"
        "});\n"
        "console.log(resp.choices[0].message.content);\n"
    )
    curl = (
        f'curl https://HOST/chat/completions \\\n'
        f"  -H \"Authorization: Bearer $API_KEY\" \\\n"
        f"  -H \"Content-Type: application/json\" \\\n"
        f"  -d '{{\"model\":\"MODEL_ID\",\"messages\":[{{\"role\":\"user\",\"content\":\"Hello\"}}]}}'\n"
    )
    # Use the published base for curl when it looks like a full URL without placeholders
    if base.startswith("http") and "{" not in base:
        curl_url = base.rstrip("/") + "/chat/completions"
        curl = (
            f"curl {curl_url} \\\n"
            "  -H \"Authorization: Bearer $API_KEY\" \\\n"
            "  -H \"Content-Type: application/json\" \\\n"
            "  -d '{\"model\":\"MODEL_ID\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'\n"
        )
    else:
        curl = (
            "# Replace the URL with the provider's published base URL, then append /chat/completions\n"
            f"# Base URL in our list: {base}\n"
            "curl \"$BASE_URL/chat/completions\" \\\n"
            "  -H \"Authorization: Bearer $API_KEY\" \\\n"
            "  -H \"Content-Type: application/json\" \\\n"
            "  -d '{\"model\":\"MODEL_ID\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'\n"
        )
    def block(code):
        return (
            '<div class="snippet"><button type="button" class="copy copy-snip" data-c="'
            + attr_esc(code)
            + '">Copy</button><pre>'
            + esc(code)
            + "</pre></div>"
        )
    return (
        "<h3>Python</h3>"
        + block(py)
        + "<h3>JavaScript</h3>"
        + block(js)
        + "<h3>curl</h3>"
        + block(curl)
        + "<p>The <code>MODEL_ID</code> string is not guessed here. Copy it from the provider’s "
        "dashboard or official model list, because catalogues change.</p>"
    )


def provider_placeholders(s: dict, data: dict) -> dict:
    return {
        "name": s["name"],
        "url": s["url"],
        "id": s["id"],
        "free_allowance": published(s.get("free_allowance")),
        "tokens_per_day": fmt_num(s.get("tokens_per_day")),
        "limits": published(s.get("limits")),
        "card_required": published(s.get("card_required")),
        "base_url": published(s.get("base_url")),
        "notes": s.get("notes") or "None recorded in our list.",
        "openai_compatible": oai_label(s),
        "category": "official provider" if s.get("category") == "official" else "gateway",
        "relay": "yes" if s.get("relay_risk") else "no",
        "first_reported": fmt_date(s.get("first_reported")),
        "entry_updated": fmt_date(s.get("last_updated")),
        "list_updated": fmt_ist(data["last_updated"]),
        "FACTBOX": factbox(s),
        "SNIPPETS": snippets_for(s),
    }


HTML_PLACEHOLDERS = {
    "FACTBOX", "SNIPPETS", "STATS", "TABLE_TPD", "TABLE_OFFICIAL",
    "TABLE_NO_CARD_OAI", "TABLE_ENDED",
}

def fill(text: str, mapping: dict, *, html_keys=None) -> str:
    """Replace {{KEY}} tokens. If html_keys is a set, only those keys (or its
    complement when using defer=True) are applied. Values that are HTML must be
    filled *after* Markdown conversion so newlines inside <pre> do not split tags.
    """
    def repl(m):
        key = m.group(1)
        if key not in mapping:
            raise SystemExit(f"unknown placeholder {{{{{key}}}}}")
        if html_keys is not None and key not in html_keys:
            return m.group(0)
        return str(mapping[key])
    return re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", repl, text)


def table_rows(sites, cols):
    # cols: list of (header, fn)
    thead = "<thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h, _ in cols) + "</tr></thead>"
    body = []
    for s in sites:
        tds = "".join(f"<td>{fn(s)}</td>" for _, fn in cols)
        body.append(f"<tr>{tds}</tr>")
    return f"<table>{thead}<tbody>{''.join(body)}</tbody></table>"


def name_link(s):
    return f'<a href="{attr_esc(s["url"])}" rel="noopener">{esc(s["name"])}</a>'


def generated_tables(data: dict) -> dict:
    active = [s for s in data["sites"] if not is_dropped(s)]
    dropped = [s for s in data["sites"] if is_dropped(s)]
    official = [s for s in active if s.get("category") == "official"]
    gateways = [s for s in active if s.get("category") != "official"]
    with_tpd = sorted(
        [s for s in active if s.get("tokens_per_day")],
        key=lambda s: (-s["tokens_per_day"], s["name"]),
    )
    oai_yes = [s for s in active if s.get("openai_compatible") == "yes"]

    def no_card(s):
        c = (s.get("card_required") or "").strip().lower()
        if not c or c == "unspecified" or c == "yes" or c == "top-up" or c.startswith("yes "):
            return False
        return bool(re.match(r"^(no\b|no card)", s["card_required"].strip(), re.I))

    nocard_oai = [s for s in oai_yes if no_card(s) and not s.get("relay_risk")]

    cols_full = [
        ("Provider", name_link),
        ("OpenAI compatible", lambda s: esc(oai_label(s))),
        ("Free allowance", lambda s: esc(published(s.get("free_allowance")))),
        ("Tokens/day", lambda s: esc(fmt_num(s.get("tokens_per_day")))),
        ("Card", lambda s: esc(published(s.get("card_required")))),
        ("Relay warning", lambda s: "Yes" if s.get("relay_risk") else "No"),
    ]
    cols_official = [
        ("Provider", name_link),
        ("Free allowance", lambda s: esc(published(s.get("free_allowance")))),
        ("Tokens/day", lambda s: esc(fmt_num(s.get("tokens_per_day")))),
        ("Limits", lambda s: esc(published(s.get("limits")))),
        ("Card", lambda s: esc(published(s.get("card_required")))),
        ("Base URL", lambda s: f"<code>{esc(s['base_url'])}</code>" if has_base(s) else "Not published"),
    ]

    stats = (
        f"<p>As of {esc(fmt_ist(data['last_updated']))} this tracker lists "
        f"<strong>{len(data['sites'])}</strong> providers: <strong>{len(active)}</strong> with an "
        f"active free offer in our data, and <strong>{len(dropped)}</strong> ended offers. "
        f"Of the active list, <strong>{len(official)}</strong> are marked official, "
        f"<strong>{len(oai_yes)}</strong> are OpenAI compatible, and "
        f"<strong>{len(with_tpd)}</strong> publish a daily token figure. "
        f"These counts will change the next time the list is updated.</p>"
    )

    return {
        "STATS": stats,
        "TABLE_TPD": table_rows(with_tpd, cols_full) if with_tpd else "<p>No active provider currently publishes a tokens-per-day figure in our list.</p>",
        "TABLE_OFFICIAL": table_rows(sorted(official, key=lambda s: s["name"].lower()), cols_official),
        "TABLE_NO_CARD_OAI": table_rows(sorted(nocard_oai, key=lambda s: s["name"].lower()), cols_full),
        "TABLE_ENDED": table_rows(dropped, cols_full) if dropped else "<p>No ended offers are currently recorded.</p>",
        "list_updated": fmt_ist(data["last_updated"]),
        "site_count": str(len(data["sites"])),
        "active_count": str(len(active)),
        "official_count": str(len(official)),
        "oai_count": str(len(oai_yes)),
    }


# --- HTML shell -----------------------------------------------------------

ANALYTICS_HEAD = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>
<!--
  Google AdSense is not active yet. When approved, uncomment the script below
  and replace {ADSENSE_PLACEHOLDER} with the real publisher client id.
  Also edit /ads.txt and uncomment the google.com line with your publisher ID
  ({ADS_TXT_PUB_PLACEHOLDER}).
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PLACEHOLDER}" crossorigin="anonymous"></script>
-->"""


def jsonld_script(objs) -> str:
    if not objs:
        return ""
    if not isinstance(objs, list):
        objs = [objs]
    chunks = []
    for obj in objs:
        chunks.append(
            '<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>"
        )
    return "\n".join(chunks)


def crumbs_html(items):
    # items: list of (href, label)
    parts = []
    for i, (href, label) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f"<span>{esc(label)}</span>")
        else:
            parts.append(f'<a href="{attr_esc(href)}">{esc(label)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def breadcrumb_ld(items):
    els = []
    for i, (href, label) in enumerate(items, 1):
        els.append({
            "@type": "ListItem",
            "position": i,
            "name": label,
            "item": SITE + href if href.startswith("/") else href,
        })
    # last item should still have item
    if els:
        els[-1]["item"] = SITE + items[-1][0] if items[-1][0].startswith("/") else items[-1][0]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": els}


def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SHORT,
        "url": SITE + "/",
        "email": CONTACT_EMAIL,
    }


def website_ld():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": NAME,
        "url": SITE + "/",
        "description": "Daily-updated list of sites giving free LLM API tokens, with OpenAI compatibility, base URLs and tokens per day.",
        "publisher": {"@type": "Organization", "name": SHORT, "url": SITE + "/"},
        "inLanguage": "en",
    }


def write_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


_FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"),
    Path("/usr/share/fonts/truetype/sand-box/google/Inter Tight/InterTight-VariableFont_wght.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]


def _sans_font_path() -> Path:
    for cand in _FONT_CANDIDATES:
        if cand.is_file():
            return cand
    raise SystemExit("No usable sans font found for og.png")


def _font(path: Path, size: int, weight: int = 400):
    font = ImageFont.truetype(str(path), size)
    try:
        axes = font.get_variation_axes()
        values = []
        for axis in axes:
            name = axis["name"]
            if isinstance(name, bytes):
                name = name.decode("utf-8", "ignore")
            lname = name.lower()
            if "weight" in lname or lname == "wght":
                values.append(weight)
            else:
                values.append(axis["default"])
        font.set_variation_by_axes(values)
    except Exception:
        pass
    return font


def _draw_spaced(draw, xy, text, font, fill, spacing=5):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=font)
    y = y - (box[3] - box[1]) / 2 - 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textbbox((0, 0), ch, font=font)[2] + spacing
    return x


def make_og_png() -> bytes:
    """1200x630 Open Graph image in the site's dark theme."""
    w, h = OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT
    bg = (7, 9, 16, 255)
    fg = (238, 242, 255, 255)
    mut = (154, 163, 184, 255)
    acc = (139, 164, 255, 255)
    acc2 = (34, 211, 238, 255)
    font_path = _sans_font_path()

    img = Image.new("RGBA", (w, h), bg)

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-280, -260, 620, 420), fill=(99, 102, 241, 70))
    gd.ellipse((620, -200, 1400, 420), fill=(34, 211, 238, 48))
    gd.ellipse((500, 420, 1280, 900), fill=(139, 92, 246, 36))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(90)))

    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    for x in range(0, w, 52):
        gdraw.line([(x, 0), (x, h)], fill=(255, 255, 255, 255), width=1)
    for y in range(0, h, 52):
        gdraw.line([(0, y), (w, y)], fill=(255, 255, 255, 255), width=1)
    alpha = grid.split()[-1].point(lambda p: int(p * 0.09) if p else 0)
    fade = Image.new("L", (w, h), 0)
    fd = ImageDraw.Draw(fade)
    for y in range(h):
        a = int(255 * max(0, 1 - (y / (h * 0.8)) ** 1.15))
        fd.line([(0, y), (w, y)], fill=a)
    grid.putalpha(Image.composite(alpha, Image.new("L", (w, h), 0), fade))
    img = Image.alpha_composite(img, grid)

    # Logo: rounded tile, gradient ring, cyan centre dot (same motif as the site mark).
    size = 88
    logo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(logo)
    ld.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.25), fill=(255, 255, 255, 20))
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdd = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / max(size - 1, 1)
        colour = (
            int(acc2[0] + (acc[0] - acc2[0]) * t),
            int(acc2[1] + (acc[1] - acc2[1]) * t),
            int(acc2[2] + (acc[2] - acc2[2]) * t),
            255,
        )
        gdd.line([(0, y), (size, y)], fill=colour)
    ring = Image.new("L", (size, size), 0)
    rd = ImageDraw.Draw(ring)
    cx = cy = size / 2
    r_out = size * 0.31
    rd.ellipse((cx - r_out, cy - r_out, cx + r_out, cy + r_out), outline=255, width=int(size * 0.095))
    logo = Image.alpha_composite(logo, Image.composite(grad, Image.new("RGBA", (size, size)), ring))
    ld = ImageDraw.Draw(logo)
    r = size * 0.095
    ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=acc2)

    pad_x, top = 96, 130
    img.paste(logo, (pad_x, top), logo)

    draw = ImageDraw.Draw(img)
    _draw_spaced(
        draw,
        (pad_x + size + 20, top + size / 2),
        "WEEKDAY-UPDATED",
        _font(font_path, 20, 650),
        acc2,
        spacing=5,
    )
    title_font = _font(font_path, 84, 800)
    title = "Free LLM API Tokens"
    ty = top + size + 40
    draw.text((pad_x, ty), title, font=title_font, fill=fg)
    sub_font = _font(font_path, 32, 500)
    sub = "OpenAI compatibility, published allowances,\nand tokens per day — from official docs only."
    title_h = draw.textbbox((pad_x, ty), title, font=title_font)
    sy = title_h[3] + 28
    draw.multiline_text((pad_x, sy), sub, font=sub_font, fill=mut, spacing=10)
    uy = h - 90
    draw.line([(pad_x, uy - 24), (pad_x + 72, uy - 24)], fill=acc2, width=3)
    draw.text((pad_x, uy), "freellmapi.link", font=_font(font_path, 26, 600), fill=fg)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_page(
    *,
    title: str,
    description: str,
    path: str,
    content: str,
    jsonld=None,
    crumbs=None,
    updated=None,
    extra_head="",
):
    canonical = SITE + (path if path != "/" else "/")
    if path != "/" and canonical.endswith("/"):
        # guides index keeps trailing slash in path "/guides/"
        pass
    og_title = title if title.startswith(SHORT) or title.startswith("Free LLM") else f"{title} — {SHORT}"
    nav = []
    for href, label in NAV:
        cur = " aria-current=\"page\"" if (path.rstrip("/") or "/") == href.rstrip("/") or (
            href == "/guides/" and path.startswith("/guides")
        ) else ""
        if href == "/" and path != "/":
            cur = ""
        nav.append(f'<a href="{attr_esc(href)}"{cur}>{esc(label)}</a>')
    footer_links = " ".join(f'<a href="{attr_esc(h)}">{esc(l)}</a>' for h, l in FOOTER)
    ld = jsonld or []
    if crumbs:
        ld = list(ld) + [breadcrumb_ld(crumbs)]
    theme_boot = (
        '(function(){try{var t=localStorage.getItem("theme")||"dark";'
        'document.documentElement.setAttribute("data-theme",t);}'
        'catch(e){document.documentElement.setAttribute("data-theme","dark");}})();'
    )
    page_title = og_title if "—" in og_title or title.endswith("Tracker") else f"{title} — {SHORT}"
    if path == "/":
        page_title = title
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(page_title)}</title>
<meta name="description" content="{attr_esc(description)}">
<link rel="canonical" href="{attr_esc(canonical)}">
<meta property="og:type" content="{'article' if path.startswith('/guides/') and path != '/guides/' else 'website'}">
<meta property="og:url" content="{attr_esc(canonical)}">
<meta property="og:title" content="{attr_esc(page_title)}">
<meta property="og:description" content="{attr_esc(description)}">
<meta property="og:site_name" content="{attr_esc(NAME)}">
<meta property="og:image" content="{attr_esc(OG_IMAGE_URL)}">
<meta property="og:image:width" content="{OG_IMAGE_WIDTH}">
<meta property="og:image:height" content="{OG_IMAGE_HEIGHT}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="{attr_esc(NAME)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr_esc(page_title)}">
<meta name="twitter:description" content="{attr_esc(description)}">
<meta name="twitter:image" content="{attr_esc(OG_IMAGE_URL)}">
<meta name="theme-color" content="#070910">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop stop-color='%2322d3ee'/%3E%3Cstop offset='1' stop-color='%237c9cff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%23070910'/%3E%3Ccircle cx='16' cy='16' r='6' fill='none' stroke='url(%23g)' stroke-width='2'/%3E%3Ccircle cx='16' cy='16' r='2' fill='%2322d3ee'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
<script>{theme_boot}</script>
{ANALYTICS_HEAD}
{jsonld_script(ld)}
{extra_head}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="/">
      <svg class="logo" viewBox="0 0 32 32" aria-hidden="true">
        <defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#7c9cff"/></linearGradient></defs>
        <rect width="32" height="32" rx="8" fill="currentColor" opacity=".08"/>
        <circle cx="16" cy="16" r="6.5" fill="none" stroke="url(#lg)" stroke-width="2"/>
        <circle cx="16" cy="16" r="2.1" fill="#22d3ee"/>
      </svg>
      Free LLM API Tokens
    </a>
    <nav class="nav" aria-label="Primary">{''.join(nav)}</nav>
    <div class="top-actions">
      <button type="button" class="icon-btn" id="themeBtn" aria-label="Toggle light and dark theme" title="Toggle theme">
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z"/></svg>
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/></svg>
      </button>
    </div>
  </div>
</header>
{content}
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-links">{footer_links}</div>
    <div class="footer-note">
      Not affiliated with any provider. Figures come from each provider’s own pages on the date shown and change often.
      Never share your API keys.
      Contact: <a href="mailto:{esc(CONTACT_EMAIL)}">{esc(CONTACT_EMAIL)}</a>.
    </div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def article_page(meta, body_html, data, crumbs, path, extra_ld=None):
    updated = meta.get("date_modified") or meta.get("date_published") or data["last_updated"][:10]
    header = crumbs_html(crumbs) + f"<h1 class=\"page-title\">{esc(meta['title'])}</h1>"
    if meta.get("lede"):
        header += f"<p class=\"page-lede\">{esc(meta['lede'])}</p>"
    header += f'<p class="page-updated">Last updated {esc(fmt_date(updated[:10]) if len(updated)>=10 else updated)}. The provider figures on this page follow the tracker snapshot of {esc(fmt_ist(data["last_updated"]))}.</p>'
    related = meta.get("related") or ""
    related_html = ""
    if related:
        # filled later if needed
        related_html = related
    content = f'<main id="content" class="wrap page"><article class="prose">{header}{body_html}{related_html}</article></main>'
    desc = meta["description"]
    ld = [
        {
            "@context": "https://schema.org",
            "@type": meta.get("schema", "Article"),
            "headline": meta["title"],
            "description": desc,
            "datePublished": meta.get("date_published", "2026-11-12"),
            "dateModified": updated[:10] if isinstance(updated, str) else "2026-11-12",
            "author": {"@type": "Organization", "name": SHORT, "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": SHORT, "url": SITE + "/"},
            "mainEntityOfPage": SITE + path,
            "inLanguage": "en",
        }
    ]
    if extra_ld:
        ld.extend(extra_ld if isinstance(extra_ld, list) else [extra_ld])
    return render_page(
        title=meta["title"],
        description=desc,
        path=path,
        content=content,
        jsonld=ld,
        crumbs=crumbs,
    )


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def guide_index_cards(guides, limit=None):
    items = guides if limit is None else guides[:limit]
    cards = []
    for g in items:
        href = f"/guides/{g['slug']}"
        cards.append(
            f'<a class="guide-card" href="{attr_esc(href)}"><h2>{esc(g["title"])}</h2>'
            f'<p>{esc(g["description"])}</p></a>'
        )
    return '<div class="guide-grid">' + "".join(cards) + "</div>"


def related_block(slugs, by_slug):
    items = []
    for sl in slugs:
        g = by_slug.get(sl)
        if not g:
            raise SystemExit(f"related slug not found: {sl}")
        items.append(f'<li><a href="/guides/{esc(g["slug"])}">{esc(g["title"])}</a></li>')
    if not items:
        return ""
    return '<aside class="related"><h2>Related guides</h2><ul>' + "".join(items) + "</ul></aside>"


def howto_ld(name, description, url, steps):
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "url": url,
        "step": [
            {"@type": "HowToStep", "position": i, "name": s[0], "text": s[1]}
            for i, s in enumerate(steps, 1)
        ],
    }


def faq_ld(pairs, url=None):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }
    if url:
        obj["url"] = url
    return obj


HOME_FAQS = [
    (
        "What does OpenAI compatible mean?",
        "You can use the official OpenAI SDK or any client that talks to OpenAI’s API. Just change the base URL and use the provider’s API key. “Partial” means only some features or models work that way.",
    ),
    (
        "What are tokens per day?",
        "A token is a small chunk of text the model reads or writes — a few characters or a short word. The daily figure is the provider’s published free limit, when they publish one. If they do not, we show “Not published” rather than guessing.",
    ),
    (
        "What does the relay warning mean?",
        "Those sites are unofficial gateways or resellers. They forward your prompts to other providers. Do not send private or sensitive data through them.",
    ),
    (
        "Do I need a credit card?",
        "It depends on the provider. Use the “No card needed” filter to narrow the list, then confirm on their site — some ask for a card later, or after a trial credit runs out.",
    ),
    (
        "Why does it say “Not published”?",
        "The provider has not published that figure on their public pages. We never invent quotas, prices or endpoints.",
    ),
    (
        "How often is this list updated?",
        "On weekdays. The “last checked” time at the top is when the list was last reviewed, shown in India Standard Time (Asia/Calcutta).",
    ),
]


def itemlist_ld(data):
    elements = []
    for i, s in enumerate(sorted(data["sites"], key=lambda x: x["name"].lower()), 1):
        elements.append({
            "@type": "ListItem",
            "position": i,
            "name": s["name"],
            "url": s["url"],
        })
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Free LLM API token providers",
        "itemListOrder": "https://schema.org/ItemListUnordered",
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }


def build():
    data = load_data()
    changed = 0
    routes = []  # (path, lastmod_date, changefreq, priority)

    # Load guides
    guides = []
    for p in sorted((HERE / "content" / "guides").glob("*.md")):
        meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        if "slug" not in meta or "title" not in meta or "description" not in meta:
            raise SystemExit(f"{p} needs slug, title, description")
        meta["_body"] = body
        meta["_file"] = p
        guides.append(meta)
    by_slug = {g["slug"]: g for g in guides}

    tables = generated_tables(data)
    by_id = sites_by_id(data)

    # Render each guide
    for g in guides:
        body = g["_body"]
        mapping = dict(tables)
        extra_ld = []
        if g.get("provider_id"):
            if g["provider_id"] not in by_id:
                raise SystemExit(f"unknown provider_id {g['provider_id']} in {g['slug']}")
            mapping.update(provider_placeholders(by_id[g["provider_id"]], data))
        text_keys = set(mapping) - HTML_PLACEHOLDERS
        body = fill(body, mapping, html_keys=text_keys)
        body_html = md_to_html(body.strip())
        body_html = fill(body_html, mapping, html_keys=HTML_PLACEHOLDERS)
        rel = [s.strip() for s in (g.get("related") or "").split(",") if s.strip()]
        rel_html = related_block(rel, by_slug)
        # temporarily use related as html via meta? article_page uses meta related as html if we set it
        g2 = dict(g)
        g2["related"] = rel_html
        path = f"/guides/{g['slug']}"
        crumbs = [("/", "Home"), ("/guides/", "Guides"), (path, g["title"])]
        if g.get("howto_steps"):
            steps = []
            # format: step1_name|step1_text;;step2_name|step2_text
            for chunk in g["howto_steps"].split(";;"):
                if "|" in chunk:
                    n, t = chunk.split("|", 1)
                    steps.append((n.strip(), t.strip()))
            if steps:
                extra_ld.append(howto_ld(g["title"], g["description"], SITE + path, steps))
        html_out = article_page(g2, body_html, data, crumbs, path, extra_ld=extra_ld)
        dest = HERE / "guides" / g["slug"] / "index.html"
        if write(dest, html_out):
            changed += 1
        routes.append((path, g.get("date_modified") or g.get("date_published") or data["last_updated"][:10], "weekly", "0.7"))

    # Guides index
    # Keep a stable editorial order from content/guides/_order.txt if present, else title
    order_file = HERE / "content" / "guides" / "_order.txt"
    if order_file.exists():
        order = [ln.strip() for ln in order_file.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        missing = [g["slug"] for g in guides if g["slug"] not in order]
        if missing:
            raise SystemExit(f"guides missing from _order.txt: {missing}")
        extras = [s for s in order if s not in by_slug]
        if extras:
            raise SystemExit(f"_order.txt has unknown slugs: {extras}")
        guides_sorted = [by_slug[s] for s in order]
    else:
        guides_sorted = sorted(guides, key=lambda g: g["title"].lower())

    gidx_body = (
        crumbs_html([("/", "Home"), ("/guides/", "Guides")])
        + '<h1 class="page-title">Guides</h1>'
        + '<p class="page-lede">Practical, original explainers on free LLM APIs. Quotas, prices and endpoints are taken from our provider list or official docs — we do not invent them.</p>'
        + f'<p class="page-updated">Provider figures follow the tracker snapshot of {esc(fmt_ist(data["last_updated"]))}.</p>'
        + guide_index_cards(guides_sorted)
    )
    gidx = render_page(
        title="Guides to free LLM APIs",
        description="Original guides on OpenAI-compatible APIs, API-key safety, rate limits, relay risks, and current free LLM API providers.",
        path="/guides/",
        content=f'<main id="content" class="wrap page">{gidx_body}</main>',
        jsonld=[
            {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": "Guides to free LLM APIs",
                "url": SITE + "/guides/",
                "description": "Original guides on using free LLM APIs safely.",
            }
        ],
        crumbs=[("/", "Home"), ("/guides/", "Guides")],
    )
    if write(HERE / "guides" / "index.html", gidx):
        changed += 1
    routes.append(("/guides/", data["last_updated"][:10], "weekly", "0.8"))

    # Policy / info pages
    for p in sorted((HERE / "content" / "pages").glob("*.md")):
        meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        body = fill(body, {"list_updated": fmt_ist(data["last_updated"]), "email": CONTACT_EMAIL, "site": SITE})
        body_html = md_to_html(body.strip())
        path = "/" + meta["slug"]
        crumbs = [("/", "Home"), (path, meta["title"])]
        updated = meta.get("date_modified") or meta.get("date_published") or "2026-11-12"
        header = (
            crumbs_html(crumbs)
            + f"<h1 class=\"page-title\">{esc(meta['title'])}</h1>"
            + (f"<p class=\"page-lede\">{esc(meta['lede'])}</p>" if meta.get("lede") else "")
            + f'<p class="page-updated">Last updated {esc(fmt_date(updated))}.</p>'
        )
        page_html = render_page(
            title=meta["title"],
            description=meta["description"],
            path=path,
            content=f'<main id="content" class="wrap page"><article class="prose">{header}{body_html}</article></main>',
            jsonld=[{"@context": "https://schema.org", "@type": "WebPage", "name": meta["title"], "url": SITE + path, "description": meta["description"]}],
            crumbs=crumbs,
        )
        if write(HERE / meta["slug"] / "index.html", page_html):
            changed += 1
        routes.append((path, updated, "monthly", "0.5"))

    # Home
    home = (HERE / "templates" / "home.html").read_text(encoding="utf-8")
    teaser_guides = [by_slug[s] for s in [
        "how-to-use-free-openai-compatible-apis",
        "best-free-llm-apis",
        "free-llm-api-for-beginners",
        "relay-gateway-risks",
        "keep-api-keys-safe",
        "groq-free-api",
    ] if s in by_slug]
    teaser = guide_index_cards(teaser_guides)
    home = home.replace("<!-- GUIDES_TEASER -->", teaser)
    # Skip-to target: homepage uses #browse; also add id=content on main if missing
    if 'id="content"' not in home:
        home = home.replace("<main>", '<main id="content">', 1)
    home_content = home
    # The home template is the main+script only; wrap with shell but the shell already
    # wraps body around `content`. Home includes <main> and <script>.
    home_html = render_page(
        title="Free LLM API Tokens Tracker",
        description="Daily-updated list of sites giving free LLM API tokens, with OpenAI compatibility, base URLs and tokens per day.",
        path="/",
        content=home_content,
        jsonld=[website_ld(), org_ld(), faq_ld(HOME_FAQS, SITE + "/"), itemlist_ld(data)],
    )
    # Homepage skip link should still go to #browse — add a second skip already in template.
    # render_page adds Skip to #content, and template has Skip to list? template starts at <main>, skip is in shell.
    # Change homepage skip to #browse via a replace after render? The shell skip is #content and we set main id=content. Fine.
    if write(HERE / "index.html", home_html):
        changed += 1
    routes.insert(0, ("/", data["last_updated"][:10], "daily", "1.0"))

    # 404
    notfound = render_page(
        title="Page not found",
        description="That page is not on Free LLM API Tokens Tracker.",
        path="/404",
        content='<main id="content" class="wrap page"><h1 class="page-title">Page not found</h1><p class="page-lede">That address is not on this site. Try the <a href="/">provider list</a> or the <a href="/guides/">guides</a>.</p></main>',
        jsonld=[{"@context": "https://schema.org", "@type": "WebPage", "name": "Page not found", "url": SITE + "/404"}],
    )
    if write(HERE / "404.html", notfound):
        changed += 1

    # robots.txt — keep search and AI-search crawlers fully allowed.
    robots = """User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot
Allow: /

Sitemap: https://freellmapi.link/sitemap.xml
"""
    if write(HERE / "robots.txt", robots):
        changed += 1
    routes.append(("/robots.txt", data["last_updated"][:10], "yearly", "0.1"))

    # Cloudflare Pages _headers (used by wrangler pages deploy). The MCP
    # `_worker.js` path applies the same headers in build_cf_deploy.py.
    if write(HERE / "_headers", HEADERS_FILE):
        changed += 1

    # Open Graph share image (1200x630) and IndexNow key file.
    if write_bytes(HERE / "og.png", make_og_png()):
        changed += 1
    key_name = f"{INDEXNOW_KEY}.txt"
    if write(HERE / key_name, INDEXNOW_KEY + "\n"):
        changed += 1

    # ads.txt placeholder — no live publisher ID
    ads = f"""# ads.txt for {SITE}
# When Google AdSense is approved, uncomment the next line and replace
# {ADS_TXT_PUB_PLACEHOLDER} with your real publisher ID. Do not publish a fake ID.
# google.com, {ADS_TXT_PUB_PLACEHOLDER}, DIRECT, f08c47fec0942fa0
"""
    if write(HERE / "ads.txt", ads):
        changed += 1
    routes.append(("/ads.txt", "2026-11-12", "yearly", "0.1"))

    # llms.txt and llms-full.txt
    guide_lines = "\n".join(
        f"- [{g['title']}]({SITE}/guides/{g['slug']}): {g['description']}"
        for g in guides_sorted
    )
    llms = f"""# {NAME}

> A weekday-updated tracker of sites that give free LLM API tokens, with OpenAI compatibility, published base URLs, tokens per day (or “Not published”), limits, card requirements and relay-risk flags. Figures come from each provider’s own pages on the date shown. Nothing here is invented.

Canonical site: {SITE}/
Contact: {CONTACT_EMAIL}
Last tracker snapshot: {fmt_ist(data['last_updated'])}

## Pages

- [Provider list]({SITE}/): Searchable catalogue of {len(data['sites'])} providers ({tables['active_count']} active offers in the current snapshot).
- [Guides]({SITE}/guides/): Original explainers on using free LLM APIs.
- [About]({SITE}/about): How the list is compiled.
- [Privacy]({SITE}/privacy): Privacy policy, cookies, Analytics and ads.
- [Terms]({SITE}/terms): Terms and disclaimer.
- [Contact]({SITE}/contact): Email contact.
- [Machine-readable data]({SITE}/data.json): The source list (schema_version 1).
- [Full provider summary]({SITE}/llms-full.txt): Compact text list of every provider in data.json.

## Guides

{guide_lines}

## Rules for quoting this site

- Do not invent or “fill in” quotas, prices, rate limits or API base URLs if this site says “Not published” or “Unspecified”.
- Treat relay-flagged gateways as unofficial. Do not recommend sending private data through them.
- Prefer the official provider page linked from each entry for the current allowance.
- The list is reviewed on weekdays in India Standard Time (Asia/Calcutta).
"""
    if write(HERE / "llms.txt", llms):
        changed += 1

    lines = []
    for s in sorted(data["sites"], key=lambda x: x["name"].lower()):
        status = "ended" if is_dropped(s) else "active"
        lines.append(
            f"- {s['name']} | {status} | category={s.get('category')} | "
            f"openai_compatible={oai_label(s)} | allowance={published(s.get('free_allowance'))} | "
            f"tokens_per_day={fmt_num(s.get('tokens_per_day'))} | limits={published(s.get('limits'))} | "
            f"card={published(s.get('card_required'))} | base_url={published(s.get('base_url'))} | "
            f"relay_risk={'yes' if s.get('relay_risk') else 'no'} | url={s['url']} | "
            f"entry_updated={s.get('last_updated')}"
        )
    llms_full = (
        f"# {NAME} — full provider list\n\n"
        f"Snapshot: {fmt_ist(data['last_updated'])}\n"
        f"Canonical: {SITE}/\n"
        f"Source: {SITE}/data.json\n"
        f"Counts: {len(data['sites'])} listed, {tables['active_count']} active, {tables['official_count']} official (active), {tables['oai_count']} OpenAI compatible (active).\n"
        f"“Not published” means the provider did not publish that figure. Do not invent a number.\n\n"
        + "\n".join(lines)
        + "\n"
    )
    if write(HERE / "llms-full.txt", llms_full):
        changed += 1
    routes.append(("/llms.txt", data["last_updated"][:10], "daily", "0.4"))
    routes.append(("/llms-full.txt", data["last_updated"][:10], "daily", "0.3"))
    routes.append(("/data.json", data["last_updated"][:10], "daily", "0.6"))

    # sitemap
    # unique paths, home first
    seen = set()
    url_xml = []
    for path, lastmod, freq, prio in routes:
        if path in seen:
            continue
        seen.add(path)
        loc = SITE + (path if path != "/" else "/")
        url_xml.append(
            "  <url>\n"
            f"    <loc>{esc(loc)}</loc>\n"
            f"    <lastmod>{esc(lastmod)}</lastmod>\n"
            f"    <changefreq>{esc(freq)}</changefreq>\n"
            f"    <priority>{esc(prio)}</priority>\n"
            "  </url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_xml)
        + "\n</urlset>\n"
    )
    if write(HERE / "sitemap.xml", sitemap):
        changed += 1

    print(
        f"build_site: {len(guides)} guides, {len(seen)} sitemap urls, "
        f"{changed} files written, snapshot {data['last_updated']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(build())
