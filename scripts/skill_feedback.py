"""Turn friction met while *using* a skill into a filable, dedupable report.

A collection improves fastest when the people running it in anger tell it what
broke. The obstacle is not willingness — it is that writing a good issue costs
more than working around the problem once. This module removes that cost: it
renders a structured report, redacts what should not leave the user's machine,
and computes a fingerprint so the tenth person to hit a problem **corroborates
the existing issue instead of opening an eleventh**.

That aggregation is the point. A hundred separate "this did not work" issues is
worse for a maintainer than ten issues carrying a hundred corroborations, and it
is worse for the reporter, whose report disappears into a pile.

Redaction is a safety net, not a guarantee. It removes the categories that leak
by accident — home paths, credentials, hostnames, and the clinical identifiers
the release gate already knows about — but no pattern set can recognise every
sensitive sample name in every lab. The calling skill must show the user the
exact rendered body and get explicit consent before anything is posted. See
`skills/asb-contribute/SKILL.md`.
"""
from __future__ import annotations

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

import argparse
import hashlib
import json
import re
import sys

from scripts.release_gate import PII_CONFIG

# What kind of friction this is. The kind decides where the report goes and what
# a maintainer can do with it, so it is a closed vocabulary, not free text.
KINDS: dict[str, str] = {
    "defect": "an existing skill is wrong, stale, or does not work as written",
    "gap": "no skill covers the task; a new one is warranted",
    "composition": "the leaves exist but nothing composes them; a workflow is warranted",
    "efficiency": "the skill works but costs far more than it needs to",
    "drift": "the underlying tool changed and the skill no longer matches it",
}

# Redaction beyond the release gate's clinical set. These are the categories that
# leak from a *session transcript* rather than from published prose: the gate
# never sees a home directory or a bearer token, so its patterns do not cover
# them. Ordered longest-match-first where two could overlap.
OUTBOUND_PATTERNS: dict[str, str] = {
    "credential": r"\b(?:sk-|ghp_|gho_|github_pat_|xox[baprs]-)[A-Za-z0-9_\-]{10,}",
    "authorization_header": r"(?i)\b(?:authorization|api[_-]?key|token|password)\b\s*[:=]\s*\S+",
    "posix_home": r"/(?:Users|home)/[^/\s\"']+",
    "windows_home": r"[A-Za-z]:\\\\?Users\\\\?[^\\\s\"']+",
    "url_userinfo": r"(?i)\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s@]+@",
}

REDACTED = "<redacted:{name}>"
FINGERPRINT_LENGTH = 12

# Generic English function words, dropped before fingerprinting so that two
# people describing one problem in different words still collide. Deliberately
# domain-neutral: a metabolomics term dropped here would silently merge two
# unrelated reports, which is the worse error.
STOPWORDS = frozenset(
    "a an and are as at be but by for from has have how in into is it its no not "
    "of on or that the then there these this to was were when which with".split()
)


def _pii_patterns() -> dict[str, str]:
    """The release gate's clinical/personal set — one canonical source, not a copy."""
    return dict(PII_CONFIG["hard_fail_patterns"])


def redact(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, categories_removed).

    Categories are reported so the calling skill can tell the user *what* was
    removed. Silence would leave them unable to judge whether the remainder is
    safe, which is the whole decision they are being asked to make.
    """
    removed: list[str] = []
    out = text or ""
    for name, pattern in {**OUTBOUND_PATTERNS, **_pii_patterns()}.items():
        out, n = re.subn(pattern, REDACTED.format(name=name), out)
        if n:
            removed.append(name)
    return out, sorted(removed)


def fingerprint(kind: str, target: str, symptom: str) -> str:
    """A stable id for "this same friction", so reports can be merged.

    Keyed on the *kind*, the skill or capability it concerns, and the set of
    content words in the symptom — not on the reporter, the timestamp, or the
    surrounding prose, none of which two people hitting one problem would share.

    This catches close restatements, not arbitrary paraphrase: "the flag is
    wrong in the example" and "The example's flag is WRONG!" collide, but two
    genuinely different descriptions of one bug will not. The fingerprint is
    therefore a cheap merge, not a substitute for searching open issues — the
    calling skill must do both.
    """
    words = re.sub(r"[^a-z0-9 ]+", " ", (symptom or "").lower()).split()
    content = sorted({w for w in words if len(w) > 2 and w not in STOPWORDS})
    payload = "␟".join((kind, (target or "").strip().lower(), " ".join(content)))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:FINGERPRINT_LENGTH]


def labels_for(kind: str) -> list[str]:
    """Labels a maintainer can filter on. `needs-triage` is always present."""
    base = ["usage-feedback", "needs-triage"]
    return base + {"gap": ["propose"], "composition": ["propose", "workflow"]}.get(kind, [])


def render_issue(
    kind: str,
    target: str,
    symptom: str,
    expected: str = "",
    context: str = "",
    collection: str = "",
) -> dict:
    """Render the report a maintainer reads, with everything redacted.

    Raises ValueError on an unknown `kind`: a report that cannot be routed is
    worse than no report, and silently relabelling it would hide the mistake.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; expected one of {sorted(KINDS)}")
    if not (target or "").strip() or not (symptom or "").strip():
        raise ValueError("a report needs both a target and a symptom")

    fields = {k: redact(v) for k, v in
              {"symptom": symptom, "expected": expected, "context": context}.items()}
    stripped = sorted({c for _, cats in fields.values() for c in cats})
    fid = fingerprint(kind, target, symptom)

    body = [
        f"**Kind:** `{kind}` — {KINDS[kind]}",
        f"**Target:** `{target}`" + (f"  ·  **Collection:** `{collection}`" if collection else ""),
        f"**Fingerprint:** `{fid}`  <!-- corroborate this issue rather than opening a new one -->",
        "",
        "### What happened",
        fields["symptom"][0].strip(),
    ]
    if fields["expected"][0].strip():
        body += ["", "### What the skill led me to expect", fields["expected"][0].strip()]
    if fields["context"][0].strip():
        body += ["", "### Context", fields["context"][0].strip()]
    if stripped:
        body += ["", f"*Redacted before posting: {', '.join(stripped)}.*"]

    return {
        "title": f"{kind}: {target} — {' '.join(symptom.split())[:80]}",
        "body": "\n".join(body).rstrip() + "\n",
        "labels": labels_for(kind),
        "fingerprint": fid,
        "redacted": stripped,
    }


def corroboration(fid: str, symptom: str, context: str = "") -> str:
    """The comment that strengthens an existing issue instead of duplicating it."""
    detail, _ = redact(symptom)
    extra, _ = redact(context)
    lines = [f"Hit this too (`{fid}`).", "", detail.strip()]
    if extra.strip():
        lines += ["", extra.strip()]
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--target", required=True, help="skill slug, or the capability that is missing")
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--expected", default="")
    parser.add_argument("--context", default="")
    parser.add_argument("--collection", default="")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(render_issue(args.kind, args.target, args.symptom,
                                      args.expected, args.context, args.collection), indent=2))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
