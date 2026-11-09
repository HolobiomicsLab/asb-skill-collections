#!/usr/bin/env python3
"""Domain-neutral synthesis of bounded skill descriptions."""

from __future__ import annotations

import re

APPROVED_PREFIXES = ("Use when", "Reference for", "Explains", "Decision support for")
MIN_LEN = 50
MAX_LEN = 300
MARKETING_TERMS = [
    "best",
    "state-of-the-art",
    "revolutionary",
    "leading",
    "superior",
    "cutting-edge",
    "best-in-class",
    "powerful",
    "amazing",
    "groundbreaking",
    "world-class",
    "unparalleled",
]


def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _strip_trailing_marketing(desc: str) -> str:
    """Remove banned marketing substrings, matching the shared description lint.

    The collector's historical list is a stricter superset of the shared
    normalizer's list, so generated descriptions satisfy both policies.
    """
    out = desc
    for term in sorted(MARKETING_TERMS, key=len, reverse=True):
        out = re.sub(re.escape(term), "", out, flags=re.IGNORECASE)
    return _collapse_ws(out)


def _split_description_opening(text: str) -> tuple[str, str] | None:
    """Return a canonical approved opening and its remaining source text."""
    aliases = (
        ("Apply this skill when", "Use when"),
        ("Use this skill when", "Use when"),
        ("Apply this skill", "Use when"),
    )
    for source, canonical in (*aliases, *((p, p) for p in APPROVED_PREFIXES)):
        match = re.match(rf"^{re.escape(source)}\b", text, flags=re.IGNORECASE)
        if match:
            remainder = re.sub(r"^[\s:;,.–—-]+", "", text[match.end():])
            return canonical, remainder
    return None


def _canonicalize_description_opening(text: str) -> str | None:
    """Normalize one existing opening and collapse repeated copies of it."""
    split = _split_description_opening(text)
    if split is None:
        return None
    opening, remainder = split
    nested = _split_description_opening(remainder)
    while nested is not None and nested[0] == opening:
        _, remainder = nested
        nested = _split_description_opening(remainder)
    return f"{opening} {remainder}".strip()


def _truncate_description(description: str) -> str:
    """Bound a description, preferring a real sentence or word boundary."""
    if len(description) <= MAX_LEN:
        return description.strip()
    cut = description[:MAX_LEN]
    ends = [
        match for match in re.finditer(r"[.;]", cut)
        if not re.search(r"\b(e\.g|i\.e|vs|etc|cf|Fig)\.?$", cut[:match.end()])
    ]
    if ends and ends[-1].end() >= MIN_LEN:
        return cut[:ends[-1].end()].strip()
    word_end = cut[: MAX_LEN - 1].rfind(" ")
    if word_end >= MIN_LEN:
        return cut[:word_end].rstrip(".,;:(- ") + "."
    return cut[: MAX_LEN - 1].rstrip(".,;:(- ") + "."


def _description_contexts(domain_label: str | None) -> tuple[str, str]:
    """Return workflow and analysis phrases for an optional domain label."""
    label = _strip_trailing_marketing(_collapse_ws(domain_label or ""))
    if label:
        return f"in a {label} workflow", f"in {label} analysis"
    return "in the workflow it documents", "in the analysis it documents"


#: A leading "when", "use when" or "if/when" clause opener. A source that opens
#: with one loses it before "Use when" is added, or the description reads
#: "Use when when ...".
_LEADING_WHEN_RE = re.compile(r"^(?:use\s+)?(?:if\s*/\s*when|when)\b[\s,:]*", re.IGNORECASE)


def _strip_leading_when(text: str) -> str:
    """Drop one leading when-clause opener ("When", "Use when", "If/when")."""
    return _LEADING_WHEN_RE.sub("", text, count=1)


def _use_when(text: str, bridge: str) -> str:
    """Give ``text`` one canonical opening, never a doubled "Use when"."""
    canonical = _canonicalize_description_opening(text)
    if canonical is not None:
        if not canonical.startswith("Use when"):
            return canonical
        rest = canonical[len("Use when"):].strip()
        return f"Use when {_strip_leading_when(rest)}".strip()
    stripped = _strip_leading_when(text)
    if stripped != text:
        bridge = ""
    if not stripped:
        return ""
    return f"Use when {bridge}{stripped[0].lower()}{stripped[1:]}"


def _description_from_sources(when_to_use: str, fallback_desc: str) -> str:
    """Choose the richest source and give it one canonical opening."""
    core = _strip_trailing_marketing(_collapse_ws(when_to_use))
    if core:
        return _use_when(core, "")
    fallback = _strip_trailing_marketing(_collapse_ws(fallback_desc))
    if not fallback:
        return ""
    return _use_when(fallback, "you need to ")


def _pad_description(description: str, pretty_name: str, context: str) -> str:
    """Pad a short description with neutral, documented procedure context."""
    description = _truncate_description(description)
    if len(description) >= MIN_LEN:
        return description
    subject = f"the {pretty_name} procedure" if pretty_name else "the documented procedure"
    description = (
        description.rstrip(".") + f". Applies {subject} {context} as documented."
    )
    if len(description) < MIN_LEN:
        description = description.rstrip(".") + ". Follow the documented procedure."
    return _truncate_description(description)


def _build_description(
    skill_name: str,
    when_to_use: str,
    fallback_desc: str,
    domain_label: str | None = None,
) -> str:
    """Synthesize a description accepted by the shared description lint."""
    pretty_name = _strip_trailing_marketing(
        _collapse_ws(skill_name.replace("-", " "))
    )
    workflow_context, analysis_context = _description_contexts(domain_label)
    desc = _description_from_sources(when_to_use, fallback_desc)
    if not desc:
        action = f"apply {pretty_name}" if pretty_name else "follow the procedure"
        desc = f"Use when you need to {action} {workflow_context}"
    return _pad_description(desc, pretty_name, analysis_context)


# ---------------------------------------------------------------------------
# Loading the build corpus mapping
# ---------------------------------------------------------------------------
