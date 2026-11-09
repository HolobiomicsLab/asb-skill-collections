"""Pure content transformations for the local build-capsule packer."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from scripts.pii_config import PII_CONFIG, _is_notation_not_email
from scripts.release_capsule_truth import _build_locator, prune_crate

QUOTE_KEYS = {"source_excerpt", "evidence_quote", "quote", "quoted_text", "verbatim", "snippet"}
TEXT_SUFFIXES = {".json", ".jsonl", ".jsonld", ".md", ".txt", ".yaml", ".yml", ".csv", ".tsv"}
QUOTE_CAP = 300
DOI_QUOTE_CAP = 1500
EMAIL_RE = re.compile(PII_CONFIG["email_regex"], re.IGNORECASE)
PHONE_RE = re.compile(
    r"(?<!\w)(?:\+\d{1,3}[ .-]?)?(?:\(\d{2,4}\)[ .-]?)?"
    r"\d{2,4}[ .-]\d{3,4}[ .-]\d{3,4}(?:[ .-]\d{2,4})?(?!\w)"
)
PATH_RE = re.compile(
    r"(?:file://)?(?:/(?:Users|Volumes|private|tmp|var/folders)/[^\s\"'<>()\[\]{},]+"
    r"|(?<![A-Za-z0-9+.-])[A-Za-z]:[\\/][^\s\"'<>()\[\]{},]+)"
)
SPACED_USER_PATH_RE = re.compile(
    r"(?:file://)?/Users/\s*<\s*user\s*name\s*>\s*/[^\s\"'<>()\[\]{},]+",
    re.IGNORECASE,
)
RESIDUAL_PATH_RE = re.compile(r"file://|/(?:Users|Volumes|private|tmp|var/folders)/|(?<![A-Za-z0-9+.-])[A-Za-z]:[\\/]")
OPEN_ACCESS = {"open", "open-access", "open_access", "oa", "gold", "gold-oa", "gold_oa", "green", "green-oa", "diamond"}
PERMISSIVE_LICENSE_PREFIXES = ("cc-by", "cc0", "public-domain", "public_domain")


def empty_counts() -> Counter:
    """Return a fresh counter with the stable screen receipt keys."""
    return Counter({
        "spans_truncated": 0,
        "spans_dropped": 0,
        "emails_redacted": 0,
        "phones_redacted": 0,
        "paths_rewritten": 0,
        "crates_pruned": 0,
        "deny_hits": 0,
        "failures": 0,
    })


@dataclass
class ScreenContext:
    """Access and allowlist rules shared by all files of one build."""

    doi: str
    access_class: str
    license: str | None
    drop_quotes: bool
    redacted_reason: str
    cap_quotes: bool = True
    email_allowlist: set[str] = field(default_factory=set)
    email_role: re.Pattern | None = None
    deny_patterns: tuple[str, ...] = ()

    @property
    def retention(self) -> str:
        """Name the G2 regime applied to quoted text: dropped, capped or full."""
        if self.drop_quotes:
            return "dropped"
        return "capped" if self.cap_quotes else "full"


@dataclass
class QuoteBudget:
    """Track the cumulative retained quotation characters for one DOI."""

    retained: int = 0

    def allowance(self) -> int:
        """Return the characters available to the next quoted field."""
        return min(QUOTE_CAP, max(0, DOI_QUOTE_CAP - self.retained))


@dataclass
class ScreenResult:
    """A transformed document and its non-sensitive measurements."""

    text: str
    counts: Counter
    quotes: dict[str, int]
    failures: list[str]


def context_for(doi: str, access: dict[str, Any]) -> ScreenContext:
    """Map access metadata to the G2 text-retention decision.

    Open-access sources under a permissive licence (the CC-BY family, CC0,
    public domain, or an explicit reuse grant) keep their attributed text in
    full. Open-access sources under any other licence string keep it under the
    caps. Restricted, unresolved and licence-less sources, and preprints without
    a reuse grant, drop the text and keep the anchor.
    """
    access_class = access_class_for(access)
    licence = access.get("license") or access.get("licence")
    is_preprint = access_class == "preprint" or bool(access.get("preprint"))
    has_grant = bool(access.get("reuse_grant") or access.get("reuse_allowed"))
    has_grant = has_grant or bool(licence and str(licence).lower().startswith(PERMISSIVE_LICENSE_PREFIXES))
    drop = access_class not in OPEN_ACCESS or not licence or (is_preprint and not has_grant)
    cap = drop or not has_grant
    if is_preprint and not has_grant:
        reason = "preprint_without_reuse_grant"
    elif not licence:
        reason = "missing_license"
    elif access_class not in OPEN_ACCESS:
        reason = f"access_{access_class}"
    else:
        reason = ""
    return ScreenContext(doi, access_class, str(licence) if licence else None, drop, reason, cap_quotes=cap)


def access_class_for(access: dict[str, Any]) -> str:
    """Normalize released and registry access vocabulary as m30 did."""
    value = str(access.get("type") or "unknown").lower()
    if value == "link-only":
        value = str(access.get("oa_status_raw") or "closed").lower()
    return {"gold-oa": "gold", "gold_oa": "gold", "oa": "gold"}.get(value, value)


def redact_pii(text: str, context: ScreenContext, counts: Counter) -> str:
    """Redact non-allowlisted emails and phone-shaped numbers."""
    def email_replacement(match: re.Match) -> str:
        value = match.group(0)
        if _is_notation_not_email(value, match):
            return value
        if value.lower() in context.email_allowlist:
            return value
        if context.email_role and context.email_role.fullmatch(value):
            return value
        counts["emails_redacted"] += 1
        return "[redacted-email]"

    text = EMAIL_RE.sub(email_replacement, text)
    def phone_replacement(match: re.Match) -> str:
        counts["phones_redacted"] += 1
        return "[redacted-phone]"
    return PHONE_RE.sub(phone_replacement, text)


def rewrite_paths(text: str, counts: Counter) -> str:
    """Replace embedded build-machine paths with stable build locators."""
    def replacement(match: re.Match) -> str:
        value = match.group(0)
        suffix = ""
        while value and value[-1] in ".;:":
            suffix = value[-1] + suffix
            value = value[:-1]
        if not _is_machine_path(value):
            return match.group(0)
        counts["paths_rewritten"] += 1
        return _build_locator(value) + suffix
    text = SPACED_USER_PATH_RE.sub(replacement, text)
    return PATH_RE.sub(replacement, text)


def _is_machine_path(value: str) -> bool:
    """Accept a drive only as a path, never as a URI scheme."""
    if not re.match(r"^[A-Za-z]:", value):
        return True
    prefix = value[:value.find(":")]
    return len(prefix) == 1


def residual_findings(text: str, context: ScreenContext) -> Counter:
    """Count only sensitive residuals, never return their values."""
    findings = empty_counts()
    redact_pii(text, context, findings)
    findings["paths_rewritten"] = len(RESIDUAL_PATH_RE.findall(text))
    findings["deny_hits"] = count_deny_hits(text, context.deny_patterns)
    return findings


def count_deny_hits(text: str, patterns: tuple[str, ...]) -> int:
    """Count literal case-insensitive deny-list matches without exposing them."""
    return sum(len(re.findall(re.escape(pattern), text, re.IGNORECASE)) for pattern in patterns if pattern)


def prune_crate_document(crate: dict, capsule_dir: Path) -> dict:
    """Apply the release's canonical crate pruning rule to a parsed crate."""
    return prune_crate(crate, capsule_dir)


def screen_text(
    text: str,
    relative_path: str,
    context: ScreenContext,
    budget: QuoteBudget,
    capsule_dir: Path | None = None,
) -> ScreenResult:
    """Screen one staged text document in the required operation order."""
    counts = empty_counts()
    quotes = {"count": 0, "characters": 0, "longest": 0, "truncated": 0, "dropped": 0}
    suffix = Path(relative_path).suffix.lower()
    failures: list[str] = []
    try:
        if suffix in {".json", ".jsonld"}:
            payload = json.loads(text)
            if Path(relative_path).name == "ro-crate-metadata.json" and capsule_dir is not None:
                payload = prune_crate_document(payload, capsule_dir)
            transformed = _screen_json(payload, relative_path, context, budget, counts, quotes, text)
            text = json.dumps(transformed, ensure_ascii=False, indent=2) + "\n"
        elif suffix == ".jsonl":
            text = _screen_json_lines(text, relative_path, context, budget, counts, quotes)
        elif suffix in {".yaml", ".yml"}:
            payload = yaml.safe_load(text)
            transformed = _screen_json(payload, relative_path, context, budget, counts, quotes, text)
            if transformed != payload:
                text = yaml.safe_dump(transformed, allow_unicode=True, sort_keys=False)
        elif suffix == ".md" and {"evidence", "ledger"}.intersection(Path(relative_path).parts):
            text = _screen_markdown(text, relative_path, context, budget, counts, quotes)
    except (ValueError, TypeError, yaml.YAMLError) as exc:
        failures.append(f"{relative_path}: parse_{type(exc).__name__}")
    text = redact_pii(text, context, counts)
    text = rewrite_paths(text, counts)
    counts["deny_hits"] = count_deny_hits(text, context.deny_patterns)
    residuals = residual_findings(text, context)
    for key in ("emails_redacted", "phones_redacted", "paths_rewritten", "deny_hits"):
        if residuals[key]:
            failures.append(f"{relative_path}: residual_{key}")
    counts["failures"] = len(failures)
    return ScreenResult(text, counts, quotes, failures)


def _screen_json_lines(text, relative_path, context, budget, counts, quotes) -> str:
    lines = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        location = f"{relative_path}:{line_number}"
        transformed = _screen_json(payload, location, context, budget, counts, quotes, line)
        lines.append(json.dumps(transformed, ensure_ascii=False))
    return "\n".join(lines) + ("\n" if lines else "")


def _screen_json(value, location, context, budget, counts, quotes, source, pointer=""):
    if isinstance(value, dict):
        output = {}
        for key in sorted(value):
            child_pointer = f"{pointer}/{_pointer_escape(key)}"
            if key in QUOTE_KEYS and isinstance(value[key], str):
                output[key], anchor = _screen_quote(
                    value[key], location, child_pointer, context, budget, counts, quotes, source
                )
                if anchor:
                    output.setdefault("_screen_redactions", []).append(anchor)
            else:
                output[key] = _screen_json(value[key], location, context, budget, counts, quotes, source, child_pointer)
        return output
    if isinstance(value, list):
        return [
            _screen_json(item, location, context, budget, counts, quotes, source, f"{pointer}/{index}")
            for index, item in enumerate(value)
        ]
    return value


def _screen_quote(value, location, pointer, context, budget, counts, quotes, source):
    if context.drop_quotes:
        allowed = 0
    elif context.cap_quotes:
        allowed = budget.allowance()
    else:
        allowed = len(value)
    retained = value[:allowed]
    if context.cap_quotes and not context.drop_quotes:
        budget.retained += len(retained)
    quotes["count"] += 1
    quotes["characters"] += len(retained)
    quotes["longest"] = max(quotes["longest"], len(retained))
    anchor = None
    if len(retained) < len(value):
        reason = context.redacted_reason if context.drop_quotes else "quotation_cap"
        anchor = _redaction_anchor(value, location, pointer, context.doi, reason, source)
        if retained:
            counts["spans_truncated"] += 1
            quotes["truncated"] += 1
        else:
            counts["spans_dropped"] += 1
            quotes["dropped"] += 1
    return retained, anchor


def _redaction_anchor(value, location, pointer, doi, reason, source) -> dict:
    encoded = json.dumps(value, ensure_ascii=False)
    start = source.find(encoded)
    line = source.count("\n", 0, start) + 1 if start >= 0 else None
    return {
        "doi": doi,
        "location": f"{location}#{pointer}",
        "line": line,
        "offsets": {"start": max(start, 0), "end": max(start, 0) + len(encoded)},
        "length": len(value),
        "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
        "redacted_reason": reason,
    }


def _screen_markdown(text, location, context, budget, counts, quotes) -> str:
    blocks = re.split(r"((?:^|\n)(?:[ \t]*>.*(?:\n|$))+)", text)
    for index in range(1, len(blocks), 2):
        block = blocks[index]
        lines = block.strip("\n").splitlines()
        value = "\n".join(re.sub(r"^\s*>\s?", "", line) for line in lines)
        pointer = f"blockquote_{index // 2 + 1}"
        retained, anchor = _screen_quote(value, location, pointer, context, budget, counts, quotes, text)
        replacement = "> " + retained.replace("\n", "\n> ") if retained else "> [redacted-quote]"
        if anchor:
            replacement += "\n<!-- asb-redaction " + json.dumps(anchor, sort_keys=True) + " -->"
        blocks[index] = replacement + ("\n" if block.endswith("\n") else "")
    return "".join(blocks)


def _pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")
