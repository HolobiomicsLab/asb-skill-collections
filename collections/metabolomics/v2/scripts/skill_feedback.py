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
by accident — paths, credentials, email addresses, and the clinical identifiers
the release gate already knows about — but no pattern set can recognise every
sensitive sample name in every lab. The calling skill must show the exact title,
labels, and body and get explicit consent before anything is posted. See
`collections/metabolomics/v2/skills/asb-contribute/SKILL.md`.
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

from scripts.pii_config import PII_CONFIG, _is_notation_not_email

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
    "url_userinfo": r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s@]+@",
    "authorization_header": (
        r"(?<![A-Za-z0-9])(?:authorization|api[_-]?key|access[_-]?key|secret[_-]?key|"
        r"token|secret|password|passwd|pwd|key)\s*[:=]\s*\S+"
    ),
    "credential": (
        r"\b(?:(?:sk|pk)-[A-Za-z0-9_\-]{10,}|"
        r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_\-]{10,}|"
        r"github_pat_[A-Za-z0-9_\-]{10,}|xox[baprs]-[A-Za-z0-9_\-]{10,}|"
        r"AKIA[0-9A-Z]{12,})\b"
    ),
    "posix_home": r"(?<![A-Za-z0-9_])/(?:Users|home)/[^\s\"'`]+",
    "windows_home": r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]+Users[\\/]+[^\s\"'`]+",
    "posix_path": r"(?<![A-Za-z0-9_:/])/(?!/)[^\s\"'`]+",
    "windows_path": r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]+[^\s\"'`]+",
}

REDACTED = "<redacted:{name}>"
REDACTED_PATH = REDACTED.format(name="absolute_path")
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
    patterns = dict(PII_CONFIG["hard_fail_patterns"])
    patterns["email"] = PII_CONFIG["email_regex"]
    return patterns


def _redact_pattern(text: str, name: str, pattern: str) -> tuple[str, int]:
    """Apply one pattern while preserving canonical non-email notation."""
    replacement_count = 0

    def replacement(match: re.Match) -> str:
        nonlocal replacement_count
        if name == "email" and _is_notation_not_email(match.group(0)):
            return match.group(0)
        replacement_count += 1
        return REDACTED.format(name=name)

    return re.sub(pattern, replacement, text, flags=re.IGNORECASE), replacement_count


def redact(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, categories_removed).

    Categories are reported so the calling skill can tell the user *what* was
    removed. Silence would leave them unable to judge whether the remainder is
    safe, which is the whole decision they are being asked to make.
    """
    removed: list[str] = []
    out = text or ""
    for name, pattern in {**OUTBOUND_PATTERNS, **_pii_patterns()}.items():
        out, n = _redact_pattern(out, name, pattern)
        if n:
            removed.append(name)
    return out, sorted(removed)


def _slash_path(value: str) -> str:
    """Return a lexical path form without reading the filesystem."""
    return (value or "").strip().replace("\\", "/")


def _is_absolute_path(value: str) -> bool:
    """Whether a string is an absolute or home-relative filesystem path."""
    path = _slash_path(value)
    return path.startswith(("/", "~/")) or bool(re.match(r"^[A-Za-z]:/", path))


def _collection_suffix(value: str) -> str | None:
    """Return the non-machine-specific suffix following a collections directory."""
    path = _slash_path(value)
    if path.startswith("collections/"):
        return path.removeprefix("collections/")
    marker = "/collections/"
    return path.split(marker, 1)[1] if marker in path else None


def _target_candidate(target: str, collection: str) -> str:
    """Keep an identifying collection suffix; replace unrelated absolute paths."""
    target_path = _slash_path(target)
    suffix = _collection_suffix(target_path)
    if suffix is not None:
        return suffix
    if not _is_absolute_path(target_path):
        return REDACTED_PATH if ".." in target_path.split("/") else target_path
    collection_path = _slash_path(collection).rstrip("/")
    if collection_path and target_path.startswith(collection_path + "/"):
        relative = target_path[len(collection_path) + 1 :]
        collection_id = _collection_suffix(collection_path)
        return "/".join(part for part in (collection_id, relative) if part)
    return REDACTED_PATH


def _collection_candidate(collection: str) -> str:
    """Keep a collection/version identifier without retaining its absolute prefix."""
    suffix = _collection_suffix(collection)
    if suffix is not None:
        return suffix
    return (
        REDACTED_PATH if _is_absolute_path(collection) else (collection or "").strip()
    )


def _path_redactions(raw: str, candidate: str) -> list[str]:
    """Describe machine-specific path material removed during normalisation."""
    if _slash_path(raw) == candidate:
        return []
    return ["absolute_path" if candidate == REDACTED_PATH else "path_prefix"]


def _has_separator_evasive_pii(value: str) -> str | None:
    """Find canonical PII shapes hidden behind identifier punctuation."""
    identifier_words = re.sub(r"[-_.]+", " ", value)
    for name, pattern in _pii_patterns().items():
        if re.search(pattern, identifier_words, flags=re.IGNORECASE):
            return name
    return None


def _redact_identifier(value: str) -> tuple[str, list[str]]:
    """Redact an identifier, including PII split by slug punctuation."""
    clean, removed = redact(value)
    evasive_category = _has_separator_evasive_pii(value)
    if evasive_category and evasive_category not in removed:
        return REDACTED.format(name=evasive_category), sorted(
            [*removed, evasive_category]
        )
    return clean, removed


def _redact_report_fields(values: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Apply the single outbound redaction boundary to every supplied field."""
    clean: dict[str, str] = {}
    removed: set[str] = set()
    for name, value in values.items():
        clean[name], categories = (
            _redact_identifier(value)
            if name in {"target", "collection"}
            else redact(value)
        )
        removed.update(categories)
    return clean, sorted(removed)


def _one_line(value: str) -> str:
    """Collapse a redacted value for a title or metadata line."""
    return " ".join((value or "").split())


def _fingerprint_redacted(kind: str, target: str, symptom: str) -> str:
    """Hash canonical text after reporter-specific material has been redacted."""
    symptom = re.sub(r"<redacted:[^>]+>", " ", symptom)
    target = re.sub(r"<redacted:[^>]+>", " ", target)
    words = re.sub(r"[^a-z0-9 ]+", " ", symptom.lower()).split()
    content = sorted(
        {word for word in words if len(word) > 2 and word not in STOPWORDS}
    )
    payload = "␟".join((kind, _one_line(target).lower(), " ".join(content)))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:FINGERPRINT_LENGTH]


def fingerprint(kind: str, target: str, symptom: str, collection: str = "") -> str:
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
    target_candidate = _target_candidate(target, collection)
    clean, _ = _redact_report_fields({"target": target_candidate, "symptom": symptom})
    return _fingerprint_redacted(kind, clean["target"], clean["symptom"])


def labels_for(kind: str) -> list[str]:
    """Labels a maintainer can filter on. `needs-triage` is always present."""
    base = ["usage-feedback", "needs-triage"]
    return base + {"gap": ["propose"], "composition": ["propose", "workflow"]}.get(
        kind, []
    )


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

    candidates = {
        "target": _target_candidate(target, collection),
        "symptom": symptom,
        "expected": expected,
        "context": context,
        "collection": _collection_candidate(collection),
    }
    fields, stripped = _redact_report_fields(candidates)
    stripped = sorted(
        {
            *stripped,
            *_path_redactions(target, candidates["target"]),
            *_path_redactions(collection, candidates["collection"]),
        }
    )
    fid = _fingerprint_redacted(kind, fields["target"], fields["symptom"])

    body = [
        f"**Kind:** `{kind}` — {KINDS[kind]}",
        f"**Target:** `{_one_line(fields['target'])}`"
        + (
            f"  ·  **Collection:** `{_one_line(fields['collection'])}`"
            if collection
            else ""
        ),
        f"**Fingerprint:** `{fid}`  <!-- corroborate this issue rather than opening a new one -->",
        "",
        "### What happened",
        fields["symptom"].strip(),
    ]
    if fields["expected"].strip():
        body += ["", "### What the skill led me to expect", fields["expected"].strip()]
    if fields["context"].strip():
        body += ["", "### Context", fields["context"].strip()]
    if stripped:
        body += ["", f"*Redacted before posting: {', '.join(stripped)}.*"]

    payload = {
        "title": f"{kind}: {_one_line(fields['target'])} — {_one_line(fields['symptom'])[:80]}",
        "labels": labels_for(kind),
        "body": "\n".join(body).rstrip() + "\n",
    }
    return {
        **payload,
        "payload": payload,
        "preview": payload,
        "fingerprint": fid,
        "redacted": stripped,
    }


def corroboration(fid: str, symptom: str, context: str = "") -> str:
    """The comment that strengthens an existing issue instead of duplicating it."""
    fields, _ = _redact_report_fields(
        {"fingerprint": fid, "symptom": symptom, "context": context}
    )
    lines = [
        f"Hit this too (`{_one_line(fields['fingerprint'])}`).",
        "",
        fields["symptom"].strip(),
    ]
    if fields["context"].strip():
        lines += ["", fields["context"].strip()]
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="render the redacted payload without publishing (the helper's only mode)",
    )
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument(
        "--target", required=True, help="skill slug, or the capability that is missing"
    )
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--expected", default="")
    parser.add_argument("--context", default="")
    parser.add_argument("--collection", default="")
    args = parser.parse_args(argv)
    try:
        print(
            json.dumps(
                render_issue(
                    args.kind,
                    args.target,
                    args.symptom,
                    args.expected,
                    args.context,
                    args.collection,
                ),
                indent=2,
            )
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
