#!/usr/bin/env python3
"""What's-new changelog and per-model SEO pages, used by build_site.py.

The changelog is computed from git history of data.json (UTC dates).
A copy is written to changes.json so later builds stay fresh even if git is
missing. Dates and entries are never invented.

Model pages are built only for families named by at least two providers in
data.json. A provider is listed only when the family name already appears in
that provider's own fields; availability is not guessed.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from collections import defaultdict
from email.utils import format_datetime
from pathlib import Path

UTC = dt.timezone.utc

COMPARE_FIELDS = (
    "name",
    "url",
    "openai_compatible",
    "base_url",
    "free_allowance",
    "tokens_per_day",
    "limits",
    "card_required",
    "notes",
    "relay_risk",
    "category",
    "free_type",
    "phone_required",
    "data_training",
)

FIELD_LABELS = {
    "name": "name",
    "url": "official URL",
    "openai_compatible": "OpenAI compatibility",
    "base_url": "base URL",
    "free_allowance": "free allowance",
    "tokens_per_day": "tokens per day",
    "limits": "rate limits",
    "card_required": "card requirement",
    "notes": "notes",
    "relay_risk": "relay warning",
    "category": "category",
    "free_type": "offer type",
    "phone_required": "phone requirement",
    "data_training": "training-data policy",
}

DEFAULTISH = {None, "", "Unspecified", "unspecified"}

# Popular families to consider. A page is emitted only when 2+ providers
# in the current data actually name the family.
MODEL_FAMILY_SPECS = (
    {
        "slug": "deepseek",
        "name": "DeepSeek",
        "pattern": r"deepseek",
    },
    {
        "slug": "llama",
        "name": "Llama",
        "pattern": r"\bllama\b",
    },
    {
        "slug": "qwen",
        "name": "Qwen",
        "pattern": r"\bqwen\d*|\bqwen\b",
    },
    {
        "slug": "gemma",
        "name": "Gemma",
        "pattern": r"\bgemma\b",
    },
    {
        "slug": "gemini",
        "name": "Gemini",
        "pattern": r"\bgemini\b",
    },
    {
        "slug": "gpt-oss",
        "name": "GPT-OSS",
        "pattern": r"\bgpt[ -]?oss\b",
    },
    {
        "slug": "mistral",
        "name": "Mistral",
        "pattern": r"\bmistral\b",
    },
    {
        "slug": "glm",
        "name": "GLM",
        "pattern": r"\bglm(?:[- ]?\d|\b)",
    },
    {
        "slug": "kimi",
        "name": "Kimi",
        "pattern": r"\bkimi\b",
    },
    {
        "slug": "minimax",
        "name": "MiniMax",
        "pattern": r"\bminimax\b",
    },
)

NEG_CLAUSE = re.compile(
    r"no longer(?:\s+\w+){0,8}\s+free"
    r"|no longer free"
    r"|\bnot (?:currently )?free\b"
    r"|\bis not free\b"
    r"|\bretired\b"
    r"|\bremoved\b"
    r"|\bended\b",
    re.I,
)

USELESS_NOTE = re.compile(r"^New \d", re.I)

TEXT_FIELDS = ("name", "free_allowance", "limits", "notes")


def _git(repo: Path, args: list[str]) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None


def _load_data_at(repo: Path, sha: str) -> dict | None:
    raw = _git(repo, ["show", f"{sha}:data.json"])
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _utc_date(iso: str) -> str:
    d = dt.datetime.fromisoformat(iso)
    if d.tzinfo is None:
        d = d.replace(tzinfo=UTC)
    return d.astimezone(UTC).date().isoformat()


def _utc_dt(iso: str) -> dt.datetime:
    d = dt.datetime.fromisoformat(iso)
    if d.tzinfo is None:
        d = d.replace(tzinfo=UTC)
    return d.astimezone(UTC)


def _sites_map(data: dict | None) -> dict:
    if not data:
        return {}
    return {s["id"]: s for s in data.get("sites") or []}


def _field_diff(old: dict, new: dict) -> list[str]:
    changed = []
    for key in COMPARE_FIELDS:
        if key not in old and key not in new:
            continue
        if key not in old:
            # Newly introduced optional field with a blank/default value
            # is a schema addition, not a provider change.
            if new.get(key) in DEFAULTISH:
                continue
        if old.get(key) != new.get(key):
            changed.append(key)
    return changed


def _human_fields(fields: list[str]) -> str:
    labels = [FIELD_LABELS.get(f, f.replace("_", " ")) for f in fields]
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + " and " + labels[-1]



def _split_name_list(rest: str) -> list[str]:
    """Split a comma/and list without breaking on commas inside parentheses."""
    parts, buf, depth = [], [], 0
    i, s = 0, rest
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif depth == 0 and s.startswith(" and ", i):
            parts.append("".join(buf).strip())
            buf = []
            i += 5
            continue
        elif ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def _strip_tail_paren(part: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", part).strip()


def _note_covered(note: str, added_names: list[str], removed_names: list[str]) -> bool:
    text = note.strip().rstrip(".")
    low = text.lower()
    names = added_names + removed_names
    if low.startswith("added "):
        rest = text[6:]
        parts = [p.strip() for p in _split_name_list(rest) if p.strip()]
        if parts and added_names:
            def matches(part: str) -> bool:
                pl = _strip_tail_paren(part).lower() or part.lower()
                return any(
                    pl == n.lower()
                    or pl == _strip_tail_paren(n).lower()
                    or n.lower().startswith(pl)
                    or _strip_tail_paren(n).lower().startswith(pl)
                    or pl.startswith(_strip_tail_paren(n).lower())
                    for n in added_names
                )
            if all(matches(p) for p in parts):
                return True
    if low.startswith("updated "):
        rest = _strip_tail_paren(text[8:]).lower()
        if any(rest == n.lower() or rest == _strip_tail_paren(n).lower() or n.lower().startswith(rest) for n in names):
            return True
    return False


def collect_changes(repo: Path, data: dict) -> dict:
    """Build a dated changelog from git history of data.json, merged with
    human notes already stored in data.json. Never invents dates or entries.
    """
    log = _git(repo, ["log", "--follow", "--format=%H %cI", "--", "data.json"])
    days: dict[str, dict] = {}
    source = "none"

    if log and log.strip():
        source = "git"
        commits = []
        for line in log.strip().splitlines():
            sha, iso = line.split(" ", 1)
            commits.append((sha, iso.strip()))
        commits.reverse()  # oldest first

        prev_sites: dict | None = None
        for sha, iso in commits:
            current = _load_data_at(repo, sha)
            cur_sites = _sites_map(current)
            day = _utc_date(iso)
            stamp = _utc_dt(iso)
            bucket = days.setdefault(
                day,
                {
                    "date": day,
                    "latest_iso": stamp.isoformat(),
                    "commits": [],
                    "added": [],
                    "removed": [],
                    "changed": [],
                    "catalogue_notes": [],
                    "notes": [],
                    "initial": None,
                },
            )
            if stamp.isoformat() > bucket["latest_iso"]:
                bucket["latest_iso"] = stamp.isoformat()
            if sha not in bucket["commits"]:
                bucket["commits"].append(sha)

            if prev_sites is None:
                bucket["initial"] = {
                    "count": len(cur_sites),
                    "text": (
                        f"First published copy of this list in the repository "
                        f"({len(cur_sites)} providers)."
                    ),
                }
                prev_sites = cur_sites
                continue

            added, removed, changed = [], [], []
            for pid, site in cur_sites.items():
                if pid not in prev_sites:
                    added.append({"id": pid, "name": site.get("name") or pid})
            for pid, site in prev_sites.items():
                if pid not in cur_sites:
                    removed.append({"id": pid, "name": site.get("name") or pid})
            for pid, site in cur_sites.items():
                if pid not in prev_sites:
                    continue
                fields = _field_diff(prev_sites[pid], site)
                if fields:
                    changed.append(
                        {
                            "id": pid,
                            "name": site.get("name") or pid,
                            "fields": fields,
                        }
                    )

            # Collapse mass schema-only updates into one catalogue note.
            if len(changed) >= 8:
                from collections import Counter

                sets = Counter(tuple(c["fields"]) for c in changed)
                fields, n = sets.most_common(1)[0]
                if n >= 8:
                    bucket["catalogue_notes"].append(
                        "Updated "
                        + _human_fields(list(fields))
                        + f" across {n} existing providers."
                    )
                    changed = [c for c in changed if tuple(c["fields"]) != fields]

            _merge_uniq(bucket["added"], added, key="id")
            _merge_uniq(bucket["removed"], removed, key="id")
            _merge_changed(bucket["changed"], changed)
            prev_sites = cur_sites

    # Merge human-written data.json notes onto the matching dates.
    # Notes dated before the first git commit are kept separately so we
    # do not invent a git event for them.
    git_dates = set(days)
    first_git = min(git_dates) if git_dates else None
    earlier_notes = []
    for entry in data.get("changelog") or []:
        date = entry.get("date")
        items = [i for i in (entry.get("items") or []) if i and not USELESS_NOTE.match(i.strip())]
        if not date or not items:
            continue
        if date in days:
            added_names = [a["name"] for a in days[date]["added"]]
            removed_names = [a["name"] for a in days[date]["removed"]]
            for item in items:
                if _note_covered(item, added_names, removed_names):
                    continue
                if item not in days[date]["notes"]:
                    days[date]["notes"].append(item)
        elif first_git and date < first_git:
            earlier_notes.append({"date": date, "items": items})
        elif source != "git":
            # No git history available: surface the recorded changelog only.
            bucket = days.setdefault(
                date,
                {
                    "date": date,
                    "latest_iso": f"{date}T00:00:00Z",
                    "commits": [],
                    "added": [],
                    "removed": [],
                    "changed": [],
                    "catalogue_notes": [],
                    "notes": [],
                    "initial": None,
                },
            )
            for item in items:
                if item not in bucket["notes"]:
                    bucket["notes"].append(item)

    # Drop days that ended up with no visible content (e.g. docs-only commits).
    cleaned = []
    for date in sorted(days, reverse=True):
        b = days[date]
        if not (
            b["added"]
            or b["removed"]
            or b["changed"]
            or b["notes"]
            or b["catalogue_notes"]
            or b["initial"]
        ):
            continue
        cleaned.append(b)

    earlier_notes.sort(key=lambda x: x["date"], reverse=True)
    return {
        "source": source,
        "last_updated": data.get("last_updated"),
        "days": cleaned,
        "earlier_notes": earlier_notes,
    }


def _merge_uniq(dest: list, incoming: list, key: str) -> None:
    seen = {item[key] for item in dest}
    for item in incoming:
        if item[key] not in seen:
            dest.append(item)
            seen.add(item[key])


def _merge_changed(dest: list, incoming: list) -> None:
    by_id = {item["id"]: item for item in dest}
    for item in incoming:
        if item["id"] in by_id:
            existing = by_id[item["id"]]
            fields = list(existing["fields"])
            for f in item["fields"]:
                if f not in fields:
                    fields.append(f)
            existing["fields"] = fields
            existing["name"] = item["name"]
        else:
            dest.append(item)
            by_id[item["id"]] = item


def changes_to_json(changes: dict) -> str:
    payload = {
        "source": changes["source"],
        "last_updated": changes.get("last_updated"),
        "days": changes["days"],
        "earlier_notes": changes.get("earlier_notes") or [],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _split_clauses(text: str) -> list[str]:
    outer = []
    parens = []
    buf: list[str] = []
    inner: list[str] = []
    depth = 0
    for ch in text:
        if ch == "(":
            if depth == 0:
                depth = 1
                inner = []
                continue
            depth += 1
            inner.append(ch)
        elif ch == ")":
            if depth == 1:
                parens.append("".join(inner))
                buf.append(" ")
                depth = 0
                inner = []
            elif depth > 1:
                depth -= 1
                inner.append(ch)
            else:
                buf.append(ch)
        else:
            (inner if depth else buf).append(ch)
    if inner:
        parens.append("".join(inner))
    chunks = re.split(r"[.;]\s+|\n+", "".join(buf))
    return [c.strip() for c in chunks + parens if c.strip()]


def _family_mentions(site: dict, pattern: str) -> list[tuple[str, str]]:
    """Return (field, clause) pairs where the family is named positively."""
    cre = re.compile(pattern, re.I)
    hits = []
    for field in TEXT_FIELDS:
        value = site.get(field)
        if not value:
            continue
        text = str(value)
        for clause in _split_clauses(text):
            if not cre.search(clause):
                continue
            if NEG_CLAUSE.search(clause):
                continue
            hits.append((field, clause))
    return hits


def collect_model_families(data: dict, is_dropped) -> tuple[list[dict], list[dict], dict]:
    """Return (pages, skipped, models_by_provider_id).

    pages: families with 2+ positive mentions.
    skipped: families named by fewer than 2 providers (no page).
    models_by_provider: id -> [{slug, name}, ...] for families that have a page.
    """
    pages = []
    skipped = []
    for spec in MODEL_FAMILY_SPECS:
        providers = []
        for site in data["sites"]:
            hits = _family_mentions(site, spec["pattern"])
            if not hits:
                continue
            providers.append(
                {
                    "site": site,
                    "dropped": bool(is_dropped(site)),
                    "mentions": hits,
                }
            )
        record = {
            "slug": spec["slug"],
            "name": spec["name"],
            "providers": providers,
            "active_count": sum(1 for p in providers if not p["dropped"]),
            "total_count": len(providers),
        }
        if len(providers) >= 2:
            pages.append(record)
        elif providers:
            skipped.append(record)

    by_provider: dict[str, list[dict]] = defaultdict(list)
    for fam in pages:
        for item in fam["providers"]:
            pid = item["site"]["id"]
            by_provider[pid].append({"slug": fam["slug"], "name": fam["name"]})
    return pages, skipped, dict(by_provider)


def excerpt_for(item: dict, pattern: str, limit: int = 160) -> str:
    """Short verbatim clause that named the family, for display only."""
    cre = re.compile(pattern, re.I)
    for field, clause in item["mentions"]:
        if cre.search(clause):
            text = " ".join(clause.split())
            if len(text) > limit:
                # Prefer a window around the match.
                m = cre.search(text)
                if m:
                    start = max(0, m.start() - 40)
                    end = min(len(text), m.end() + 80)
                    text = text[start:end].strip()
                    if start > 0:
                        text = "…" + text
                    if end < len(clause):
                        text = text + "…"
            return text
    return ""


def family_spec(slug: str) -> dict:
    for spec in MODEL_FAMILY_SPECS:
        if spec["slug"] == slug:
            return spec
    raise KeyError(slug)
