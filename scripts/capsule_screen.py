"""Pure content transformations for the local build-capsule packer."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from scripts.pii_config import (PII_CONFIG, _is_git_ssh_clone, _is_notation_not_email, _is_placeholder_email,
                                _is_r_slot_access)
from scripts.release_capsule_truth import _build_locator, prune_crate

QUOTE_KEYS = {"source_excerpt", "evidence_quote", "quote", "quoted_text", "verbatim", "snippet",
              # Task cards and the entity spine of a build carry the paper span a
              # finding or an entity rests on under these names.
              "evidence_span", "finding_evidence_span",
              # Certification reports restate a data-availability span of the paper.
              "open_data_evidence"}
# A text-quote selector (W3C Web Annotation) below a quote property holds paper
# text in its exact, prefix and suffix parts, as ASTRA files write it.
QUOTE_SELECTOR_KEYS = {"exact", "prefix", "suffix"}
# A nanopublication's provenance names the paper sentence a claim was extracted
# from as the description of the activity that generated the assertion.
GENERATION_DESCRIPTION = ("wasgeneratedby", "description")
# Every string below these keys is paper text: the entity spine's section texts, and
# the evidence of a reproducibility score's open-data component.
SOURCE_TEXT_CONTAINERS = {"section_text"}
EVIDENCE_PARENTS = {"open_data"}
# List items whose `text` is retrieved or quoted paper text.
PASSAGE_LISTS = {"passages_used", "substring_hits", "evidence_snippets"}
TEXT_SUFFIXES = {".json", ".jsonl", ".jsonld", ".md", ".txt", ".yaml", ".yml", ".csv", ".tsv"}
# Members that cannot hold text: never decoded, never screened as text. Any other
# member that decodes as UTF-8 (a Snakefile, main.nf, a CWL file, a shell script,
# deps.lock) is screened as plain text.
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".bmp", ".webp", ".pdf",
                   ".zip", ".gz", ".bz2", ".xz", ".tar", ".parquet", ".npy", ".npz", ".h5",
                   ".hdf5", ".pkl", ".mzml", ".raw"}
QUOTE_CAP = 300
DOI_QUOTE_CAP = 1500
REDACTED_QUOTE = "[redacted-quote]"
EMAIL_RE = re.compile(PII_CONFIG["email_regex"], re.IGNORECASE)
TLD_FILE = Path(__file__).with_name("data") / "iana_tlds.txt"
# Last labels the shared check keeps as R slot notation (`object@meta.data`) although the root zone also holds
# them as top-level domains. An address that ends in one of these is left alone; any other root-zone label is
# an address.
SLOT_LAST_LABELS = frozenset({"data", "name"})
# Last labels of a machine name on a private network, which are not in the root zone: `login@host-name.local` is
# the user and the machine of someone's terminal prompt, never an R slot.
HOST_LAST_LABELS = frozenset({"local", "lan", "localdomain", "internal", "intranet", "home", "corp"})
# An address written to defeat harvesters: `name[at]host.org`, `name (at) lab.example.edu`, `name {at} host [dot] org`. The
# same allowlist and role rule as for a plain address decide whether it stays.
_OBFUSCATED_SEPARATOR = r"(?:[ \t]?(?:\[dot\]|\(dot\)|\{dot\})[ \t]?|\.)"
OBFUSCATED_EMAIL_RE = re.compile(
    r"(?<![\w.+-])([\w.+-]{2,})[ \t]?(?:\[at\]|\(at\)|\{at\})[ \t]?"
    rf"([\w-]+(?:{_OBFUSCATED_SEPARATOR}[\w-]+)*{_OBFUSCATED_SEPARATOR}[A-Za-z]{{2,}})(?![\w])",
    re.IGNORECASE,
)
OBFUSCATED_DOT_RE = re.compile(r"[ \t]?(?:\[dot\]|\(dot\)|\{dot\})[ \t]?", re.IGNORECASE)
GLUED_LAST_LABEL = re.compile(r"([a-z]{2,})(?=[A-Z])")
CONTINUED_DOMAIN = re.compile(r"-[A-Za-z0-9]")
PHONE_RE = re.compile(
    r"(?<!\w)(?:\+\d{1,3}[ .-]?)?(?:\(\d{2,4}\)[ .-]?)?"
    r"\d{2,4}[ .-]\d{3,4}[ .-]\d{3,4}(?:[ .-]\d{2,4})?(?!\w)"
)
# Digit groups alone are the numeric data of a paper (masses, axis ticks, page
# ranges, identifiers), so a phone-shaped number is redacted only with a cue: an
# international prefix, a parenthesised area code that is not a year, or a
# telephone or fax label shortly before it on the same line.
PHONE_LABEL = r"(?<![^\W\d_])(?:t[eé]l(?:[eé]phone|efon|efax)?|phone|fax)(?![^\W\d_])"
PHONE_LABEL_BEFORE_RE = re.compile(PHONE_LABEL + r"[^\n]{0,30}\Z", re.IGNORECASE)
# Right after a label any grouping counts ("04 92 07 61 00"), within the digit
# count of a telephone number. A plus sign may stand apart from the country code
# ("Phone: + 44 (0)1865 000000", as letter heads print it). The value may sit in an opening bracket or
# quotation mark, as a correspondence block extracted from a journal page prints it ("Tel: [886-2-12345678]").
LABELLED_PHONE_RE = re.compile(
    PHONE_LABEL + r"\.?[ \t]*(?:(?:number|no|nr|n°|#)\.?)?[ \t]*[:=]?[ \t]*[\[{<\"'“‘]?[ \t]*"
    r"((?:\+[ \t]?)?\(?\d[\d ().\-/]{5,22}\d)",
    re.IGNORECASE,
)
PHONE_DIGITS = range(7, 16)
# An international prefix is a cue on its own, whatever the grouping that follows ("P: +43 1-4277-12345 M: +43 (0)664.1234567",
# a contact line with one-letter labels). A space or a hyphen must follow the country code: "+1.234567" is a number.
INTERNATIONAL_PHONE_RE = re.compile(r"(?<![\w.])\+\d{1,3}[ \-](?:\(\d{1,4}\)[ .\-]?)?\d[\d .\-]{5,16}\d(?!\w)")
INTERNATIONAL_PHONE_DIGITS = range(9, 16)
# An area code in parentheses has three to five digits and is not a year; shorter
# ones are issue numbers of a reference list.
AREA_CODE = r"\((?!(?:19|20)\d\d\))\d{3,5}\)"
AREA_CODE_RE = re.compile(AREA_CODE)
AREA_CODE_PHONE_RE = re.compile(rf"(?<!\w){AREA_CODE}[ .-]?\d{{3,4}}[ .-]\d{{3,4}}(?!\w)")
# A machine path is a root marker followed by path characters. Users, Volumes,
# var/folders and the macOS /private tree are distinctive and count anywhere. home,
# root and tmp are ordinary directory names and count only where an absolute path
# starts: not as the continuation of a longer path ("test/tmp/", "~/tmp/",
# "${HOME}/tmp/"), but after a one-letter option ("-I/home/...").
PATH_CHARACTER = r"""[^\s"'<>()\[\]{},]"""
DISTINCTIVE_ROOT = r"/(?:Users|Volumes|var/folders|private/(?:tmp|var|etc))/"
ORDINARY_ROOT = r"(?:(?<![\w.~}-])|(?<=(?<![\w-])-[A-Za-z]))/(?:home|root|tmp)/"
# Drive letters are relevant only for home directories. In particular, a
# variable followed by a LaTeX command is not a machine path.
DRIVE_ROOT = r"(?<![\w+.-])[A-Za-z]:[\\/](?i:Users|Documents and Settings)[\\/]"
MACHINE_ROOT = rf"(?:{DISTINCTIVE_ROOT}|{ORDINARY_ROOT}|{DRIVE_ROOT})"
FILE_SCHEME = r"(?<![\w+.-])file:"
# A local file URI ("file:///opt/conda/conda-bld/x/work") names a path of the build
# machine whatever its root, so it is rewritten like one. It stops before a backtick, an
# asterisk or a backslash, which close the mention in Markdown or shell quoting, and it
# needs a word character: "file:///." and "file:///*" name no path.
FILE_URI_CHARACTER = r"""[^\s"'<>()\[\]{},`*\\]"""
FILE_URI_PATH = rf"{FILE_SCHEME}///{FILE_URI_CHARACTER}*[\w~]"
PATH_RE = re.compile(rf"(?:{FILE_SCHEME}(?://)?)?{MACHINE_ROOT}{PATH_CHARACTER}+|{FILE_URI_PATH}")
SPACED_USER_PATH_RE = re.compile(
    r"(?:file://)?/Users/\s*<\s*user\s*name\s*>\s*/[^\s\"'<>()\[\]{},]+",
    re.IGNORECASE,
)
# The residual check is wider than the rewrite, so what the rewrite cannot handle
# leaves the build out instead of passing: any root marker counts unless the mention
# ends there ("in the /tmp/ directory", "D:/ ") or a placeholder follows
# ("/tmp/<name>"). A bare scheme in prose ("served from file:// needs a flag", "the
# `file://` scheme") names no path either, so a file URI counts only when a path or a
# host follows it.
#
# A placeholder after the root is generic text, not a machine: an angle-bracket
# placeholder, a template field ("/tmp/{task_id}", "/tmp/{{task_id}}") and the
# placeholder for the user name of a home directory ("/home/[USER]/", "C:\Users\[$UserName]\",
# '/Users/"username"/'). Any other bracketed word ("/Users/[example]/") may be a real
# name and still leaves the build out.
MENTION_END = r"""[)\]}"'`.,;:!?*]*(?:\s|\Z)"""
TEMPLATE_FIELD = r"\{{1,2}\$?\w+\}{1,2}"
USER_PLACEHOLDER = r"""(?i:[\[("'%][$%]?(?:your[_-]?)?user(?:[_-]?name)?[\])"'%](?=[/\\\s"']|\Z))"""
PLACEHOLDER_AFTER_ROOT = rf"<|{TEMPLATE_FIELD}|{USER_PLACEHOLDER}"
FILE_SCHEME_RESIDUAL = (
    rf"{FILE_SCHEME}(?:///(?={FILE_URI_CHARACTER}*[\w~])"
    r"""|//(?=[^\s"'<>()\[\]{},.;:`*!?/\\])"""
    r"""|/(?!/)(?=[^\s"'<>()\[\]{},.;:]))"""
)
RESIDUAL_PATH_RE = re.compile(
    rf"{FILE_SCHEME_RESIDUAL}|{MACHINE_ROOT}(?!{MENTION_END})(?!{PLACEHOLDER_AFTER_ROOT})"
)
# Characters a URL path can hold inside JSON, YAML or Markdown text; a
# backslash is excluded so a JSON escape is never cut in half.
URL_TAIL = r"""[^\s"'<>()\[\]{},\\]*"""
URL_TRAILING_PUNCTUATION = ".;:"
OPEN_ACCESS = {"open", "open-access", "open_access", "oa", "gold", "gold-oa", "gold_oa", "green", "green-oa", "diamond"}


def allows_verbatim_sharing(licence: str) -> bool:
    """Tell whether a paper licence lets its text be shared verbatim with attribution.

    Every Creative Commons licence does (BY, BY-SA, BY-NC, BY-ND, BY-NC-SA,
    BY-NC-ND), and so do CC0 and the public domain. The text stays under the
    paper's licence, NonCommercial and NoDerivatives terms included, which the
    record guides state. Any other licence string is not recognised here.
    """
    value = licence.strip().lower()
    if re.fullmatch(
        r"https?://(?:www\.)?creativecommons\.org/"
        r"(?:licenses/by(?:-nc)?(?:-nd|-sa)?/|publicdomain/(?:zero|mark)/)"
        r"\d+(?:\.\d+)*/?(?:legalcode/?)?", value
    ):
        return True
    value = re.sub(r"[\s_]+", "-", value)
    return bool(re.fullmatch(r"(?:cc-by(?:-nc)?(?:-nd|-sa)?|cc0)(?:-\d+(?:\.\d+)*)?|public-domain", value))


def is_text_member(name: str, data: bytes) -> bool:
    """Tell whether a member is screened as text: a known text suffix, or UTF-8 bytes
    without a NUL byte and without a known binary suffix."""
    suffix = Path(name).suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return True
    if suffix in BINARY_SUFFIXES or b"\0" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


OVERLAP_RUN = 160
OVERLAP_MARKER = "[trimmed-overlap]"
OVERLAP_REASON = "article_overlap"


def normalise_with_map(text: str) -> tuple[str, list[int]]:
    """Lowercase and collapse whitespace, returning each output character's source index."""
    chars: list[str] = []
    index: list[int] = []
    space_at = None
    for position, character in enumerate(text):
        if character.isspace():
            if chars and space_at is None:
                space_at = position
            continue
        if space_at is not None:
            chars.append(" ")
            index.append(space_at)
            space_at = None
        for lowered in character.lower():
            chars.append(lowered)
            index.append(position)
    return "".join(chars), index


class ArticleIndex:
    """Every OVERLAP_RUN-character window of a normalised article, held as hashes only.

    The article text itself is not kept: only window hashes, which find a copied
    run in a shipped string without carrying the text further.
    """

    def __init__(self, article: str, run: int = OVERLAP_RUN):
        normalised, _ = normalise_with_map(article)
        self.run = run
        self.windows = {hash(normalised[start:start + run]) for start in range(len(normalised) - run + 1)}

    def runs(self, text: str) -> list[tuple[int, int]]:
        """Return the source-character spans of `text` covered by windows of the article,
        merged where they touch or overlap."""
        if len(text) < self.run:
            return []
        normalised, index = normalise_with_map(text)
        spans: list[list[int]] = []
        for start in range(len(normalised) - self.run + 1):
            # A window never opens on a space, and windows merge only where they
            # overlap, so two separate copies joined by whitespace stay two runs.
            if normalised[start] == " " or hash(normalised[start:start + self.run]) not in self.windows:
                continue
            end = start + self.run
            if spans and start < spans[-1][1]:
                spans[-1][1] = max(spans[-1][1], end)
            else:
                spans.append([start, end])
        # A run ends after the source character of its last normalised character; the
        # whitespace at its edges stays, so the marker keeps the surrounding spacing.
        result = []
        for start, end in spans:
            first, last = index[start], index[end - 1] + 1
            while first < last and text[first].isspace():
                first += 1
            while last > first and text[last - 1].isspace():
                last -= 1
            # A run counts OVERLAP_RUN characters of text, never a whitespace edge.
            if len(normalise_with_map(text[first:last])[0]) >= self.run:
                result.append((first, last))
        return result


def trim_overlap(text: str, context: "ScreenContext", counts: Counter, marker=None):
    """Cut each run copied from the article; return the text and the removed spans' anchors.

    `marker`, given an anchor, returns the replacement; by default OVERLAP_MARKER.
    """
    if context.article is None:
        return text, []
    runs = context.article.runs(text)
    if not runs:
        return text, []
    parts, previous, removed = [], 0, []
    for start, end in runs:
        span = text[start:end]
        anchor = {"doi": context.doi, "length": len(span), "offsets": {"start": start, "end": end},
                  "sha256": hashlib.sha256(span.encode("utf-8")).hexdigest(),
                  "redacted_reason": OVERLAP_REASON}
        parts += [text[previous:start], marker(anchor) if marker else OVERLAP_MARKER]
        removed.append(anchor)
        counts["overlap_runs_trimmed"] += 1
        counts["overlap_characters_trimmed"] += len(span)
        previous = end
    parts.append(text[previous:])
    return "".join(parts), removed


def trim_overlap_document(text: str, relative_path: str, context: "ScreenContext", counts: Counter) -> str:
    """Trim copied runs from a Markdown or plain-text member outside its quotation fields.

    Markdown keeps an `asb-redaction` comment after each marker; other text, where a
    comment could break the syntax, carries the length and digest in the marker.
    """
    if context.article is None:
        return text
    protected = [(span.start, span.end) for span in _markdown_quotes(text, relative_path)] \
        if source_text_kind(relative_path) else []
    markdown = Path(relative_path).suffix.lower() == ".md"
    parts, previous = [], 0
    for start, end in sorted(protected) + [(len(text), len(text))]:
        offset = previous

        def marker(anchor, offset=offset):
            anchor["location"] = f"{relative_path}#offset_{offset + anchor['offsets']['start']}"
            if markdown:
                return OVERLAP_MARKER + " <!-- asb-redaction " + json.dumps(anchor, sort_keys=True) + " -->"
            return f"[trimmed-overlap length={anchor['length']} sha256={anchor['sha256']}]"
        segment, _ = trim_overlap(text[previous:start], context, counts, marker)
        parts += [segment, text[start:end]]
        previous = end
    return "".join(parts)


def empty_counts() -> Counter:
    """Return a fresh counter with the stable screen receipt keys."""
    return Counter({
        "spans_truncated": 0,
        "spans_dropped": 0,
        "emails_redacted": 0,
        "phones_redacted": 0,
        "paths_rewritten": 0,
        "private_urls_rewritten": 0,
        "crates_pruned": 0,
        "deny_hits": 0,
        "failures": 0,
        "overlap_runs_trimmed": 0,
        "overlap_characters_trimmed": 0,
    })


def empty_quotes() -> dict[str, int]:
    """Return output measurements and transformation counts for source text."""
    return {"count": 0, "characters": 0, "longest": 0, "truncated": 0, "dropped": 0}


def _local_name(key) -> str:
    """Resolve compact names and expanded JSON-LD property names alike."""
    return re.split(r"[:/#]", key)[-1].lower() if isinstance(key, str) else ""


def source_text_kind(relative_path: str, path: tuple = ()) -> str | None:
    """Recognize paper text by its schema, shared by screening and verification.

    Quote properties use their local name, including JSON-LD value objects and
    lists. Retrieved text is the text of a passages_used or substring_hits
    list item. Other text, value, claim, note, prompt and data-preview fields
    are not quotations.
    The evidence/source_snippets.md member carries plain snippet bodies after
    its entry headings and Source/Reason metadata. Other evidence and ledger
    Markdown carries source text only in blockquotes. A dataset preview's
    fenced paper.md or article_fulltext.md payload is paper text; other
    preview payloads are data.
    """
    if path:
        if Path(relative_path).parts[-2:] == ("inputs", "dataset_preview.md") and path[0] == "preview":
            return "paper_preview" if re.split(r"[\\/:]", path[-1])[-1] in {"paper.md", "article_fulltext.md"} else None
        names = tuple(_local_name(key) if isinstance(key, str) else key for key in path)
        field_path = names[:-1] if names[-1] == "@value" else names
        while field_path and isinstance(field_path[-1], int):
            field_path = field_path[:-1]
        if field_path and field_path[-1] in QUOTE_KEYS:
            return "quote"
        if len(field_path) >= 2 and field_path[-2] in QUOTE_KEYS and field_path[-1] in QUOTE_SELECTOR_KEYS:
            return "quote"
        if tuple(field_path[-2:]) == GENERATION_DESCRIPTION:
            return "quote"
        if len(field_path) >= 2 and field_path[-2] in EVIDENCE_PARENTS and field_path[-1] == "evidence":
            return "quote"
        # The screen's own redaction anchors, written beside the removed text, are not paper text.
        if SOURCE_TEXT_CONTAINERS.intersection(name for name in field_path if isinstance(name, str)) \
                and "_screen_redactions" not in field_path:
            return "quote"
        # A nanopublication describes its assertion and the activity that produced it
        # with the paper sentence the claim was extracted from.
        if "nanopubs" in Path(relative_path).parts[:-1] and field_path and field_path[-1] == "description":
            return "quote"
        if (len(field_path) >= 3 and field_path[-3] in PASSAGE_LISTS
                and isinstance(field_path[-2], int) and field_path[-1] == "text"):
            return "passage"
        return None
    member = Path(relative_path)
    if member.suffix.lower() == ".md":
        if member.parts[-2:] == ("evidence", "source_snippets.md"):
            return "snippets"
        if member.parts[-2:] == ("inputs", "dataset_preview.md"):
            return "previews"
        if "cards" in member.parts[:-1] or member.name == "task_card.md":
            return "card_snippets"
        if member.parts[-2:] == ("astra", "provenance.myst.md"):
            return "provenance_evidence"
        if {"evidence", "ledger"}.intersection(member.parts):
            return "blockquotes"
    return None


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
    private_repositories: tuple[str, ...] = ()
    # The article of a paper whose text is not kept in full; runs copied from it are trimmed.
    article: "ArticleIndex | None" = None

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

    Open-access sources under a Creative Commons licence (NC and ND variants
    included), CC0, the public domain, or an explicit reuse grant keep their
    attributed text in full. Open-access sources under any other licence string keep it under the
    caps. Restricted, unresolved and licence-less sources, and preprints without
    a reuse grant, drop the text and keep the anchor.
    """
    access_class = access_class_for(access)
    licence = access.get("license") or access.get("licence")
    is_preprint = access_class == "preprint" or bool(access.get("preprint"))
    has_grant = bool(access.get("reuse_grant") or access.get("reuse_allowed"))
    has_grant = has_grant or bool(licence and allows_verbatim_sharing(str(licence)))
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


@lru_cache(maxsize=1)
def root_zone_labels() -> frozenset[str]:
    """Top-level domains an address can end in, read from the IANA root zone file next to the screen."""
    lines = TLD_FILE.read_text(encoding="utf-8").splitlines()
    return frozenset(line.strip() for line in lines if line.strip() and not line.startswith("#")) - SLOT_LAST_LABELS


def is_kept_for_its_slot_shape_only(value: str, match: re.Match) -> bool:
    """True when the shared check keeps a token only because it reads as R slot notation, while its last label is
    a top-level domain, alone or run into the word that follows an address in extracted text (`.deYutong`), or the
    domain goes on after the token with a hyphen."""
    local, _, domain = value.partition("@")
    if not _is_r_slot_access(local, domain):
        return False
    if _is_git_ssh_clone(value, local, match) or _is_placeholder_email(local):
        return False
    if local.lower() in {token.lower() for token in PII_CONFIG["email_notation_localparts"]}:
        return False
    last_label = domain.rsplit(".", 1)[-1]
    glued = GLUED_LAST_LABEL.match(last_label)
    if last_label.lower() in root_zone_labels() or last_label.lower() in HOST_LAST_LABELS:
        return True
    if glued and glued.group(1) in root_zone_labels():
        return True
    # The expression stops at a hyphen when the end of the domain is broken by extraction ("@med.uni-example. de"):
    # a hyphen and a letter right after the token mean the domain goes on, which a slot name never does.
    return last_label.lower() not in SLOT_LAST_LABELS and bool(CONTINUED_DOMAIN.match(match.string, match.end()))


def redact_pii(text: str, context: ScreenContext, counts: Counter) -> str:
    """Redact non-allowlisted emails and phone-shaped numbers."""
    def email_replacement(match: re.Match) -> str:
        value = match.group(0)
        if _is_notation_not_email(value, match) and not is_kept_for_its_slot_shape_only(value, match):
            return value
        if value.lower() in context.email_allowlist:
            return value
        if context.email_role and context.email_role.fullmatch(value):
            return value
        counts["emails_redacted"] += 1
        return "[redacted-email]"

    text = EMAIL_RE.sub(email_replacement, text)

    def obfuscated_replacement(match: re.Match) -> str:
        address = f"{match.group(1)}@{OBFUSCATED_DOT_RE.sub('.', match.group(2))}"
        if address.lower() in context.email_allowlist or (context.email_role and context.email_role.fullmatch(address)):
            return match.group(0)
        counts["emails_redacted"] += 1
        return "[redacted-email]"

    text = OBFUSCATED_EMAIL_RE.sub(obfuscated_replacement, text)

    def labelled_replacement(match: re.Match) -> str:
        number = match.group(1)
        if sum(character.isdigit() for character in number) not in PHONE_DIGITS:
            return match.group(0)
        counts["phones_redacted"] += 1
        return match.group(0)[: match.start(1) - match.start()] + "[redacted-phone]"

    def phone_replacement(match: re.Match) -> str:
        if not _has_phone_cue(match):
            return match.group(0)
        counts["phones_redacted"] += 1
        return "[redacted-phone]"

    def area_code_replacement(match: re.Match) -> str:
        counts["phones_redacted"] += 1
        return "[redacted-phone]"

    def international_replacement(match: re.Match) -> str:
        if sum(character.isdigit() for character in match.group(0)) not in INTERNATIONAL_PHONE_DIGITS:
            return match.group(0)
        counts["phones_redacted"] += 1
        return "[redacted-phone]"

    text = LABELLED_PHONE_RE.sub(labelled_replacement, text)
    text = INTERNATIONAL_PHONE_RE.sub(international_replacement, text)
    text = AREA_CODE_PHONE_RE.sub(area_code_replacement, text)
    return PHONE_RE.sub(phone_replacement, text)


def _has_phone_cue(match: re.Match) -> bool:
    """Tell a telephone number from numeric data by what introduces it."""
    value = match.group(0)
    if value.startswith("+"):
        return True
    if AREA_CODE_RE.match(value):
        return True
    return bool(PHONE_LABEL_BEFORE_RE.search(match.string[max(0, match.start() - 60):match.start()]))


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


def private_url_pattern(repositories) -> re.Pattern | None:
    """Match a GitHub URL of a private repository and capture its owner/name.

    Web, raw and SSH forms are matched, with or without a scheme, `.git` and a
    trailing path, fragment or query; the trailing part is part of the match.
    """
    if not repositories:
        return None
    names = "|".join(re.escape(name) for name in sorted(repositories))
    return re.compile(
        r"(?:(?:git\+)?(?:https?|ssh|git)://)?(?:[\w.-]+@)?"
        r"(?:www\.|raw\.|api\.)?(?:github\.com|githubusercontent\.com)[/:](?:repos/)?"
        rf"(?P<repository>{names})(?:\.git)?(?![\w.-])(?:[/#?]{URL_TAIL})?",
        re.IGNORECASE,
    )


def private_repository_hits(text: str, repositories) -> int:
    """Count GitHub URLs of private repositories, in any form, without returning them."""
    pattern = private_url_pattern(repositories)
    return len(pattern.findall(text)) if pattern else 0


def rewrite_private_urls(text: str, repositories, counts: Counter) -> str:
    """Replace each GitHub URL of a private repository with its bare owner/name.

    The canonical spelling comes from the repository list, so the output does
    not depend on the case the URL was written in. Trailing sentence punctuation
    is kept outside the URL.
    """
    pattern = private_url_pattern(repositories)
    if pattern is None:
        return text
    canonical = {name.lower(): name for name in repositories}

    def replacement(match: re.Match) -> str:
        value = match.group(0)
        stripped = value.rstrip(URL_TRAILING_PUNCTUATION)
        counts["private_urls_rewritten"] += 1
        return canonical[match.group("repository").lower()] + value[len(stripped):]
    return pattern.sub(replacement, text)


def _is_machine_path(value: str) -> bool:
    """Accept a drive only as a path, never as a URI scheme."""
    if not re.match(r"^[A-Za-z]:", value):
        return True
    prefix = value[:value.find(":")]
    return len(prefix) == 1


def screen_string(text: str, context: ScreenContext, counts: Counter) -> str:
    """Apply the three text rewrites to one string in their required order."""
    # Before PII: an SSH URL user part reads as an email.
    text = rewrite_private_urls(text, context.private_repositories, counts)
    text = redact_pii(text, context, counts)
    return rewrite_paths(text, counts)


def residual_findings(text: str, context: ScreenContext) -> Counter:
    """Count only sensitive residuals, never return their values."""
    findings = empty_counts()
    redact_pii(text, context, findings)
    findings["paths_rewritten"] = len(RESIDUAL_PATH_RE.findall(text))
    findings["private_urls_rewritten"] = private_repository_hits(text, context.private_repositories)
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
    """Screen one staged text document in the required operation order.

    A JSON, JSON Lines or YAML document is rewritten and checked on its decoded
    strings (values and mapping keys), then serialized, so a rewrite never runs
    through an escape or a line break of the serialization. Other text, and a
    document that does not parse, is rewritten and checked as text. Deny-list
    patterns are counted on the final text.
    """
    counts = empty_counts()
    quotes = empty_quotes()
    budget_before = budget.retained
    suffix = Path(relative_path).suffix.lower()
    failures: list[str] = []
    screened = None
    try:
        if suffix not in {".json", ".jsonld", ".jsonl", ".yaml", ".yml"}:
            text = trim_overlap_document(text, relative_path, context, counts)
        if suffix in {".json", ".jsonld"}:
            payload = json.loads(text)
            if Path(relative_path).name == "ro-crate-metadata.json" and capsule_dir is not None:
                payload = prune_crate_document(payload, capsule_dir)
            screened = [_screen_json(payload, relative_path, context, budget, counts, quotes, text)]
            text = json.dumps(screened[0], ensure_ascii=False, indent=2) + "\n"
        elif suffix == ".jsonl":
            text, screened = _screen_json_lines(text, relative_path, context, budget, counts, quotes)
        elif suffix in {".yaml", ".yml"}:
            payload = yaml.safe_load(text)
            screened = [_screen_json(payload, relative_path, context, budget, counts, quotes, text)]
            # The source text is kept only when nothing changed and it holds nothing to
            # screen outside its values, in a comment for example.
            if screened[0] != payload or _has_findings(text, context):
                text = yaml.safe_dump(screened[0], allow_unicode=True, sort_keys=False)
        elif source_text_kind(relative_path):
            text = _screen_markdown(text, relative_path, context, budget, counts, quotes)
    except (ValueError, TypeError, AttributeError, RecursionError, yaml.YAMLError) as exc:
        failures.append(f"{relative_path}: parse_{type(exc).__name__}")
        screened = None
    if screened is None:
        text = screen_string(text, context, counts)
        residual_text = text
    else:
        failures += _still_parses(text, suffix, relative_path)
        residual_text = "\n".join(_strings(screened))
    counts["deny_hits"] = count_deny_hits(text, context.deny_patterns)
    residuals = residual_findings(residual_text, context)
    residuals["deny_hits"] = counts["deny_hits"]
    for key in ("emails_redacted", "phones_redacted", "paths_rewritten", "private_urls_rewritten", "deny_hits"):
        if residuals[key]:
            failures.append(f"{relative_path}: residual_{key}")
    if not any(": parse_" in failure for failure in failures):
        verified_budget = QuoteBudget(budget_before)
        measured, problems = verify_quote_policy(text, relative_path, context, verified_budget)
        quotes.update({key: measured[key] for key in ("count", "characters", "longest")})
        failures.extend(problems)
        if context.cap_quotes and not context.drop_quotes:
            budget.retained = verified_budget.retained
    counts["failures"] = len(failures)
    return ScreenResult(text, counts, quotes, failures)


def _still_parses(text: str, suffix: str, relative_path: str) -> list[str]:
    """Report a JSON document that the text rewrites left unparsable."""
    try:
        if suffix in {".json", ".jsonld"}:
            json.loads(text)
        elif suffix == ".jsonl":
            for line in text.splitlines():
                if line.strip():
                    json.loads(line)
    except ValueError:
        return [f"{relative_path}: invalid_json_after_rewrite"]
    return []


def _has_findings(text: str, context: ScreenContext) -> bool:
    findings = residual_findings(text, context)
    return any(findings[key] for key in ("emails_redacted", "phones_redacted", "paths_rewritten", "private_urls_rewritten"))


def _strings(value):
    """Yield every string of a parsed document: mapping keys and values."""
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key
            yield from _strings(item)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, bytes):
        yield value.decode("latin-1")
    elif isinstance(value, str):
        yield value


def _screen_json_lines(text, relative_path, context, budget, counts, quotes) -> tuple[str, list]:
    lines, screened = [], []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        location = f"{relative_path}:{line_number}"
        screened.append(_screen_json(payload, location, context, budget, counts, quotes, line))
        lines.append(json.dumps(screened[-1], ensure_ascii=False))
    return "\n".join(lines) + ("\n" if lines else ""), screened


class RewrittenKeyCollision(ValueError):
    """Two mapping keys became the same key once screened; one value would be lost."""


def _screen_json(value, location, context, budget, counts, quotes, source, pointer="", path=(), anchors=None):
    if isinstance(value, dict):
        output = {}
        # JSON-LD value objects permit only their defined @ properties. Put
        # their anchors on the containing record, beside the quoted property.
        value_object = "@value" in value
        redactions = anchors if value_object and anchors is not None else []
        for key in sorted(value):
            name = screen_string(key, context, counts) if isinstance(key, str) else key
            if name in output:
                raise RewrittenKeyCollision(pointer)
            child_pointer = f"{pointer}/{_pointer_escape(str(name))}"
            output[name] = _screen_json(
                value[key], location, context, budget, counts, quotes, source,
                child_pointer, path + (key,), redactions,
            )
        if redactions and not value_object:
            output.setdefault("_screen_redactions", []).extend(redactions)
        return output
    if isinstance(value, (list, tuple, set, frozenset)):
        # YAML pairs and sets load as tuples and sets; a set has no order of its own.
        items = sorted(value, key=repr) if isinstance(value, (set, frozenset)) else value
        return [
            _screen_json(item, location, context, budget, counts, quotes, source,
                         f"{pointer}/{index}", path + (index,), anchors)
            for index, item in enumerate(items)
        ]
    if isinstance(value, str):
        if source_text_kind(location, path):
            retained, anchor = _screen_quote(value, location, pointer, context, budget, counts, quotes, source)
            if anchor:
                anchor["doi"] = screen_string(anchor["doi"], context, counts)
                anchors.append(anchor)
            return retained
        value, removed = trim_overlap(value, context, counts)
        for anchor in removed:
            anchor["location"] = f"{location}#{pointer}"
            anchor["doi"] = screen_string(anchor["doi"], context, counts)
            if anchors is not None:
                anchors.append(anchor)
        return screen_string(value, context, counts)
    return value


def _screen_quote(value, location, pointer, context, budget, counts, quotes, source):
    if context.drop_quotes:
        allowed = 0
    elif context.cap_quotes:
        allowed = budget.allowance()
    else:
        allowed = len(value)
    candidate = value[:allowed]
    # Rewrites can change the length, so both the budget and the receipt use
    # the actual retained string. A replacement cannot extend a capped field.
    rewritten = screen_string(candidate, context, counts)
    retained = rewritten[:allowed] if context.cap_quotes else rewritten
    if context.cap_quotes and not context.drop_quotes:
        budget.retained += len(retained)
    quotes["count"] += 1
    quotes["characters"] += len(retained)
    quotes["longest"] = max(quotes["longest"], len(retained))
    anchor = None
    if len(candidate) < len(value) or len(retained) < len(rewritten):
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


@dataclass
class MarkdownQuote:
    """One source-text body, with offsets into its Markdown member."""

    start: int
    end: int
    value: str
    pointer: str
    blockquote: bool = False
    inline: bool = False


def _markdown_quotes(text: str, relative_path: str):
    """Locate bodies without treating their scaffold or redactions as prose."""
    kind = source_text_kind(relative_path)
    if kind == "snippets":
        entries = list(re.finditer(r"(?m)^##[ \t]+ev_\d+[ \t]*\r?$", text))
        regions = [(match.end(), entries[index + 1].start() if index + 1 < len(entries) else len(text))
                   for index, match in enumerate(entries)]
        if not entries:
            # An unstructured source-snippet member is still a source field.
            regions = [(0, len(text))]
        for index, (start, end) in enumerate(regions, 1):
            # These two producer metadata lines precede each plain snippet.
            prefix = re.match(r"(?:[ \t]*\r?\n|[ \t]*-[ \t]*(?:Source|Reason):[^\n]*(?:\n|$))*", text[start:end])
            start += prefix.end()
            while end > start and text[end - 1].isspace():
                end -= 1
            value = re.sub(r"<!-- asb-redaction [^\n]* -->", "", text[start:end]).strip()
            yield MarkdownQuote(start, end, "" if value == REDACTED_QUOTE else value, f"snippet_{index}")
    elif kind == "previews":
        sections = []
        for section in re.finditer(r"(?m)^###[ \t]+`([^`\n]+)`[ \t]*$", text):
            before = text[:section.start()].rstrip()
            previous_line = before.rsplit("\n", 1)[-1] if before else ""
            follows_wrapper = not before or bool(re.fullmatch(r"[ \t]*(?:`{3,}|~{3,})[ \t]*", previous_line))
            opens_wrapper = re.match(r"\s*\n[ \t]*(?:`{3,}|~{3,})[ \t]*\n", text[section.end():])
            if follows_wrapper and opens_wrapper:
                sections.append(section)
        for index, section in enumerate(sections, 1):
            if not source_text_kind(relative_path, ("preview", section.group(1))):
                continue
            end = sections[index].start() if index < len(sections) else len(text)
            opening = re.search(r"(?m)^[ \t]*(`{3,}|~{3,})[^\n]*\n", text[section.end():end])
            if opening is None:
                start = section.end()
            else:
                start = section.end() + opening.end()
                fence = opening.group(1)
                # The preview renderer embeds Markdown without escaping its
                # internal fences. Only the final fence closes the wrapper.
                closings = list(re.finditer(rf"(?m)^[ \t]*{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$", text[start:end]))
                if closings:
                    end = start + closings[-1].start()
            while start < end and text[start].isspace():
                start += 1
            while end > start and text[end - 1].isspace():
                end -= 1
            value = re.sub(r"<!-- asb-redaction [^\n]* -->", "", text[start:end]).strip()
            yield MarkdownQuote(start, end, "" if value == REDACTED_QUOTE else value, f"paper_preview_{index}")
    elif kind == "card_snippets":
        # A task card's "Evidence Snippets" entries end with the paper span in single
        # quotes: "- `ev_001` from `agent` (mode): [section] claim: 'span'". The span
        # starts at the first ": '" of the entry, so a colon inside it widens it.
        section = re.search(r"(?m)^##[ \t]+Evidence Snippets[ \t]*$", text)
        if section is None:
            return
        following = re.search(r"(?m)^#{1,2}[ \t]", text[section.end():])
        end_of_section = section.end() + following.start() if following else len(text)
        entries = re.finditer(r"(?m)^[ \t]*[-*][ \t]+`ev_[^`\n]+`[^\n]*?: '(?P<span>[^\n]*)'[ \t]*$",
                              text[section.end():end_of_section])
        for index, match in enumerate(entries, 1):
            start, end = section.end() + match.start("span"), section.end() + match.end("span")
            value = re.sub(r"\s*<!-- asb-redaction [^\n]* -->", "", text[start:end]).strip()
            yield MarkdownQuote(start, end, "" if value == REDACTED_QUOTE else value, f"card_snippet_{index}",
                                inline=True)
    elif kind == "provenance_evidence":
        # An ASTRA provenance page cites each claim's paper span in double quotes:
        # "  - evidence: doi `10.x/y` <U+2014> "span"" (an em dash before the span).
        entries = re.finditer(r'(?m)^[ \t]*[-*][ \t]+evidence:[^\n]*?\u2014 "(?P<span>[^\n]*)"[ \t]*$', text)
        for index, match in enumerate(entries, 1):
            start, end = match.start("span"), match.end("span")
            value = re.sub(r"\s*<!-- asb-redaction [^\n]* -->", "", text[start:end]).strip()
            yield MarkdownQuote(start, end, "" if value == REDACTED_QUOTE else value, f"provenance_evidence_{index}",
                                inline=True)
    elif kind == "blockquotes":
        for index, match in enumerate(re.finditer(r"(?m)^(?:[ \t]*>[^\n]*(?:\n|$))+", text), 1):
            end = match.end() - int(match.group().endswith("\n"))
            value = "\n".join(re.sub(r"^[ \t]*>[ \t]?", "", line) for line in text[match.start():end].splitlines())
            yield MarkdownQuote(match.start(), end, "" if value == REDACTED_QUOTE else value,
                                f"blockquote_{index}", True)


def _screen_markdown(text, location, context, budget, counts, quotes) -> str:
    parts, previous = [], 0
    for span in _markdown_quotes(text, location):
        parts.append(text[previous:span.start])
        retained, anchor = _screen_quote(span.value, location, span.pointer, context, budget, counts, quotes, text)
        if retained == span.value and anchor is None:
            parts.append(text[span.start:span.end])
        else:
            replacement = retained or REDACTED_QUOTE
            if span.blockquote:
                replacement = "> " + replacement.replace("\n", "\n> ")
            if anchor:
                anchor["line"] = text.count("\n", 0, span.start) + 1
                anchor["offsets"] = {"start": span.start, "end": span.end}
                separator = " " if span.inline else "\n"
                replacement += separator + "<!-- asb-redaction " + json.dumps(anchor, sort_keys=True) + " -->"
            parts.append(replacement)
        previous = span.end
    parts.append(text[previous:])
    return "".join(parts)


def _structured_quotes(value, relative_path, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _structured_quotes(item, relative_path, path + (key,))
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            yield from _structured_quotes(item, relative_path, path + (index,))
    elif isinstance(value, str) and source_text_kind(relative_path, path):
        yield value


def source_text_values(text: str, relative_path: str):
    """Read recognised source fields from a serialized member without changing it."""
    suffix = Path(relative_path).suffix.lower()
    if suffix in {".json", ".jsonld"}:
        yield from _structured_quotes(json.loads(text), relative_path)
    elif suffix == ".jsonl":
        for line in text.splitlines():
            if line.strip():
                yield from _structured_quotes(json.loads(line), relative_path)
    elif suffix in {".yaml", ".yml"}:
        yield from _structured_quotes(yaml.safe_load(text), relative_path)
    else:
        for span in _markdown_quotes(text, relative_path):
            yield span.value


def verify_quote_policy(text: str, relative_path: str, context: ScreenContext, budget: QuoteBudget) -> tuple[dict, list[str]]:
    """Count what the output holds and reject residual text or an exceeded cap.

    This pass reads the serialized output independently of the transformation
    counters. The packer supplies one verification budget across all members.
    Empty fields and Markdown redaction markers contribute no source text.
    """
    quotes, failures = empty_quotes(), []
    try:
        for value in source_text_values(text, relative_path):
            if value:
                quotes["count"] += 1
                quotes["characters"] += len(value)
                quotes["longest"] = max(quotes["longest"], len(value))
    except (ValueError, TypeError, AttributeError, RecursionError, yaml.YAMLError) as exc:
        failures.append(f"{relative_path}: quote_inventory_{type(exc).__name__}")
        return quotes, failures
    if context.drop_quotes and quotes["characters"]:
        failures.append(f"{relative_path}: residual_source_text")
    elif context.cap_quotes and not context.drop_quotes:
        budget.retained += quotes["characters"]
        if quotes["longest"] > QUOTE_CAP:
            failures.append(f"{relative_path}: quotation_field_cap_exceeded")
        if budget.retained > DOI_QUOTE_CAP:
            failures.append(f"{relative_path}: quotation_doi_cap_exceeded")
    return quotes, failures


def _pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")
