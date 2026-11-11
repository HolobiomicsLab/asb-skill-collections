"""Load, validate and apply governance/tool_licences_reviewed.yaml.

The reviewed map records, for names checked by hand against the tool's own
licence statement, what the name denotes and its licence. It takes precedence
over every registry: a name it lists is never looked up anywhere else, so a
reviewer's `leave_unknown` cannot be undone by a registry match.

An entry whose name denotes different things is `ambiguous: true` and lists
`contexts`. A context applies to a record only through machine-checkable keys
under `match`; the `when` sentence is for the reader and is never interpreted:

    match:
      any_terms: [dimensionality reduction, single-cell]   # one must occur
      none_terms: [mappability]                             # none may occur
      ecosystems: [python, r]                               # code evidence for one
      collections: [transcriptomics]                        # the record's collection

A record takes a context only when exactly one context matches it. No match,
two matches, or a context without `match` keys all leave the record unknown.
"""
from __future__ import annotations

import pathlib
import re

import yaml

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.license_tier import load_map
from scripts.tool_licence_text import read_licence
from scripts.tool_registry_sources import normalize

REVIEWED = pathlib.Path(__file__).resolve().parent.parent / "governance" / "tool_licences_reviewed.yaml"
ENTRY_KINDS = ("software", "vendor_product", "artefact")
CATEGORIES = ("language", "runtime", "package", "application", "web_service", "database",
              "method", "format")
MATCH_KEYS = ("any_terms", "none_terms", "ecosystems", "collections")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RESOLVED_FIELDS = ("entity", "entry_kind", "license", "license_tier", "repo_url", "evidence_url")


class ReviewedMapError(ValueError):
    """The reviewed map is malformed; the message lists every problem found."""


def load(path=None) -> dict:
    """The validated document, or an empty one when the file does not exist."""
    p = pathlib.Path(path or REVIEWED)
    if not p.is_file():
        return {"version": 1, "entries": []}
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    problems = validate(doc)
    if problems:
        raise ReviewedMapError(f"{p}: " + "; ".join(problems))
    return doc


def _check_resolution(where, block, tiers) -> list[str]:
    """Problems with one resolved reading (a plain entry, or one context)."""
    out = []
    kind = block.get("entry_kind")
    if kind not in ENTRY_KINDS:
        out.append(f"{where}: entry_kind {kind!r} not in {ENTRY_KINDS}")
    tier = block.get("license_tier")
    if tier not in tiers:
        out.append(f"{where}: license_tier {tier!r} not in {tiers}")
        return out
    licence = block.get("license")
    if kind == "artefact" and (licence or tier != "unknown"):
        out.append(f"{where}: an artefact has no licence and tier unknown")
    if kind == "vendor_product" and tier not in ("restricted", "unknown"):
        out.append(f"{where}: a vendor product is restricted or unknown, not {tier!r}")
    if licence:
        reading = read_licence(licence)
        if reading["tier"] is not None and reading["tier"] != tier:
            out.append(f"{where}: license {licence!r} reads as {reading['tier']!r}, "
                       f"the entry says {tier!r}")
        if tier == "open" and re.search(r"\bNC\b|non-?commercial|\bND\b", str(licence), re.I):
            out.append(f"{where}: a non-commercial or no-derivatives licence cannot be open")
    elif tier == "open":
        out.append(f"{where}: tier open needs a licence")
    if tier != "unknown" and not block.get("evidence_url"):
        out.append(f"{where}: a resolved tier needs evidence_url")
    category = block.get("category")
    if category is not None and category not in CATEGORIES:
        out.append(f"{where}: category {category!r} not in {CATEGORIES}")
    return out


def validate(doc) -> list[str]:
    """Every problem in the document; empty when it is well formed."""
    problems: list[str] = []
    if not isinstance(doc, dict):
        return ["the document is not a mapping"]
    if doc.get("version") != 1:
        problems.append(f"version {doc.get('version')!r} is not 1")
    if doc.get("reviewed") is not None and not _DATE.match(str(doc.get("reviewed"))):
        problems.append("reviewed is not a YYYY-MM-DD date")
    entries = doc.get("entries")
    if not isinstance(entries, list):
        return problems + ["entries is not a list"]
    tiers = list(load_map()["tiers"])
    seen: dict[str, int] = {}
    for i, entry in enumerate(entries):
        where = f"entries[{i}]"
        if not isinstance(entry, dict):
            problems.append(f"{where}: not a mapping")
            continue
        names = entry.get("names")
        if not isinstance(names, list) or not names or not all(isinstance(n, str) and normalize(n)
                                                               for n in names):
            problems.append(f"{where}: names must be a non-empty list of names")
            names = []
        where = f"entries[{i}] ({names[0] if names else '?'})"
        for name in names:
            key = normalize(name)
            if key in seen and seen[key] != i:
                problems.append(f"{where}: name {name!r} is also in entries[{seen[key]}]")
            seen[key] = i
        if not _DATE.match(str(entry.get("verified") or "")):
            problems.append(f"{where}: verified is not a YYYY-MM-DD date")
        if entry.get("ambiguous"):
            contexts = entry.get("contexts")
            if not isinstance(contexts, list) or len(contexts) < 2:
                problems.append(f"{where}: an ambiguous entry lists at least two contexts")
                continue
            for j, context in enumerate(contexts):
                cwhere = f"{where} contexts[{j}]"
                if not isinstance(context, dict) or not context.get("when"):
                    problems.append(f"{cwhere}: needs a `when` sentence")
                    continue
                match = context.get("match")
                if match is not None:
                    if not isinstance(match, dict) or set(match) - set(MATCH_KEYS):
                        problems.append(f"{cwhere}: match keys must be among {MATCH_KEYS}")
                    elif not any(match.get(k) for k in MATCH_KEYS if k != "none_terms"):
                        problems.append(f"{cwhere}: match needs a positive key")
                if context.get("leave_unknown"):
                    continue
                problems.extend(_check_resolution(cwhere, context, tiers))
        else:
            problems.extend(_check_resolution(where, entry, tiers))
    return problems


def index(doc) -> dict:
    """``{normalized_name: entry}``."""
    return {normalize(n): e for e in doc.get("entries") or [] for n in e.get("names") or []}


def _term_present(term, text) -> bool:
    pattern = r"(?<![\w-])" + r"[\s_-]?".join(re.escape(p) for p in str(term).split()) + r"(?![\w-])"
    return re.search(pattern, text, re.I) is not None


def context_matches(match, ctx, code) -> bool:
    """Whether one context's machine-checkable keys all hold for this record."""
    if not match:
        return False
    text = ctx.all_text()
    if match.get("any_terms") and not any(_term_present(t, text) for t in match["any_terms"]):
        return False
    if any(_term_present(t, text) for t in match.get("none_terms") or []):
        return False
    if match.get("ecosystems") and not set(match["ecosystems"]) & set(code):
        return False
    if match.get("collections") and ctx.collection not in match["collections"]:
        return False
    return True


def apply(entry, ctx) -> tuple[dict | None, str]:
    """(reading, reason) for a record whose name the reviewed map lists.

    ``reading`` is the plain entry or the single matching context, or None when
    the record stays unknown; ``reason`` says which.
    """
    if not entry.get("ambiguous"):
        if entry.get("leave_unknown"):
            return None, "reviewed-leave-unknown"
        return entry, "reviewed"
    code = ctx.code_evidence()
    hits = [c for c in entry.get("contexts") or [] if context_matches(c.get("match"), ctx, code)]
    if len(hits) != 1:
        return None, "reviewed-ambiguous-no-single-context" if not hits else \
            "reviewed-ambiguous-several-contexts"
    if hits[0].get("leave_unknown"):
        return None, "reviewed-context-leave-unknown"
    return hits[0], "reviewed-context"
