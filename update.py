#!/usr/bin/env python3
"""Daily-job helper for data.json. No dependencies.

Add a site:
  python3 update.py add --id flexlora --name "Flexlora" --url https://flexlora.com/ \
    --oai yes --base https://api.flexlora.com/v1 --allowance "7M tokens/day" --tpd 7000000 \
    --limits "15 RPM" --card No --notes "..." [--relay] [--official]
Change fields of an existing site (only the flags you pass are changed):
  python3 update.py set --id apinex --tpd 3000000 --allowance "3M tokens/day" --note-change "APInex cut 10M -> 3M tokens/day"
Add a free-text changelog line only:
  python3 update.py log "Something changed"
Every add/set bumps last_updated (IST) and writes a changelog line for today.
"""
import argparse, json, sys, datetime as dt
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
F = "data.json"

def load(): return json.load(open(F, encoding="utf-8"))
def save(d):
    d["last_updated"] = dt.datetime.now(IST).replace(microsecond=0).isoformat()
    json.dump(d, open(F, "w", encoding="utf-8"), indent=2, ensure_ascii=False); open(F, "a").write("\n")
def today(): return dt.datetime.now(IST).date().isoformat()
def log(d, msg):
    t = today()
    for c in d["changelog"]:
        if c["date"] == t:
            if msg not in c["items"]: c["items"].append(msg)
            break
    else: d["changelog"].insert(0, {"date": t, "items": [msg]})
    d["changelog"].sort(key=lambda c: c["date"], reverse=True)

p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
for name in ("add", "set"):
    a = sub.add_parser(name); a.add_argument("--id", required=True)
    for f in ("name", "url", "base", "allowance", "limits", "card", "notes", "note-change"): a.add_argument("--" + f)
    a.add_argument("--oai", choices=["yes", "no", "partial", "unspecified"])
    a.add_argument("--tpd", help="integer tokens/day, or 'none' for unspecified")
    a.add_argument("--relay", action="store_true"); a.add_argument("--no-relay", action="store_true")
    a.add_argument("--official", action="store_true")
l = sub.add_parser("log"); l.add_argument("msg")
A = p.parse_args(); d = load(); sites = {s["id"]: s for s in d["sites"]}

def tpd(v): return None if v in (None, "none", "") else int(v)
if A.cmd == "log":
    log(d, A.msg)
elif A.cmd == "add":
    if A.id in sites: sys.exit(f"id {A.id} exists; use set")
    for req in ("name", "url", "allowance"):
        if not getattr(A, req): sys.exit(f"--{req} is required for add")
    s = dict(id=A.id, name=A.name, url=A.url,
             openai_compatible=None if A.oai in (None, "unspecified") else A.oai,
             base_url=A.base or "Unspecified", free_allowance=A.allowance, tokens_per_day=tpd(A.tpd),
             limits=A.limits or "Unspecified", card_required=A.card or "Unspecified", notes=A.notes or "",
             relay_risk=bool(A.relay), category="official" if A.official else "gateway",
             first_reported=today(), last_updated=today())
    d["sites"].append(s); log(d, A.note_change or f"Added {A.name}.")
else:
    if A.id not in sites: sys.exit(f"no site with id {A.id}")
    s = sites[A.id]
    m = {"name": "name", "url": "url", "base": "base_url", "allowance": "free_allowance", "limits": "limits", "card": "card_required", "notes": "notes"}
    for k, f in m.items():
        v = getattr(A, k)
        if v is not None: s[f] = v
    if A.oai: s["openai_compatible"] = None if A.oai == "unspecified" else A.oai
    if A.tpd is not None: s["tokens_per_day"] = tpd(A.tpd)
    if A.relay: s["relay_risk"] = True
    if A.no_relay: s["relay_risk"] = False
    if A.official: s["category"] = "official"
    s["last_updated"] = today(); log(d, A.note_change or f"Updated {s['name']}.")
save(d); print("ok:", A.cmd, getattr(A, "id", ""), "| sites:", len(d["sites"]))
