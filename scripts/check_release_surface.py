#!/usr/bin/env python3
"""Reject retracted phrases and foreign release identifiers in a candidate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_RULES = Path(__file__).with_name("release_surface_rules.yaml")
LINEAGE_RELATIONS = frozenset({"isNewVersionOf", "isPreviousVersionOf"})


class SurfaceCheckError(RuntimeError):
    """The candidate or rule inputs cannot be checked."""


@dataclass(frozen=True)
class Rule:
    """One configured phrase or identifier rule."""

    id: str
    text: str
    lineage_exception: bool = False


@dataclass(frozen=True)
class Finding:
    """One configured rule occurrence in a candidate file."""

    relative_path: str
    line: int
    rule_id: str
    matched_text: str
    offset: int


@dataclass(frozen=True)
class _JsonNode:
    value: Any
    start: int
    end: int
    members: tuple[tuple[str, _JsonNode], ...] | None = None
    elements: tuple[_JsonNode, ...] | None = None


class _JsonSpanParser:
    """Parse JSON while retaining source spans for scalar values."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.index = 0
        self.decoder = json.JSONDecoder()

    def parse(self) -> _JsonNode:
        """Parse exactly one JSON value and reject trailing content."""
        node = self._parse_value()
        self._skip_whitespace()
        if self.index != len(self.text):
            self._error("Extra data")
        return node

    def _error(self, message: str) -> None:
        raise json.JSONDecodeError(message, self.text, self.index)

    def _skip_whitespace(self) -> None:
        while self.index < len(self.text) and self.text[self.index] in " \t\r\n":
            self.index += 1

    def _take(self, token: str) -> bool:
        if self.index < len(self.text) and self.text[self.index] == token:
            self.index += 1
            return True
        return False

    def _expect(self, token: str) -> None:
        self._skip_whitespace()
        if not self._take(token):
            self._error(f"Expected {token!r}")

    def _parse_value(self) -> _JsonNode:
        self._skip_whitespace()
        if self.index >= len(self.text):
            self._error("Expecting value")
        if self.text[self.index] == "{":
            return self._parse_object()
        if self.text[self.index] == "[":
            return self._parse_array()
        start = self.index
        value, self.index = self.decoder.raw_decode(self.text, self.index)
        return _JsonNode(value, start, self.index)

    def _parse_key(self) -> str:
        self._skip_whitespace()
        if self.index >= len(self.text) or self.text[self.index] != '"':
            self._error("Expecting property name")
        key, self.index = self.decoder.raw_decode(self.text, self.index)
        return key

    def _parse_object(self) -> _JsonNode:
        start = self.index
        self.index += 1
        members: list[tuple[str, _JsonNode]] = []
        self._skip_whitespace()
        if self._take("}"):
            return _JsonNode({}, start, self.index, members=())
        while True:
            key = self._parse_key()
            self._expect(":")
            members.append((key, self._parse_value()))
            self._skip_whitespace()
            if self._take("}"):
                break
            self._expect(",")
        value = {key: node.value for key, node in members}
        return _JsonNode(value, start, self.index, members=tuple(members))

    def _parse_array(self) -> _JsonNode:
        start = self.index
        self.index += 1
        elements: list[_JsonNode] = []
        self._skip_whitespace()
        if self._take("]"):
            return _JsonNode([], start, self.index, elements=())
        while True:
            elements.append(self._parse_value())
            self._skip_whitespace()
            if self._take("]"):
                break
            self._expect(",")
        return _JsonNode(
            [node.value for node in elements],
            start,
            self.index,
            elements=tuple(elements),
        )


def _parse_rules(document: Any, key: str, *, identifiers: bool) -> list[Rule]:
    """Validate and return one named rule list."""
    if not isinstance(document, dict) or not isinstance(document.get(key), list):
        raise SurfaceCheckError(f"rules field {key!r} must be a list")
    rules: list[Rule] = []
    for entry in document[key]:
        if not isinstance(entry, dict):
            raise SurfaceCheckError(f"rules field {key!r} has a non-object entry")
        rule_id, text = entry.get("id"), entry.get("text")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise SurfaceCheckError(f"rules field {key!r} has an invalid id")
        if not isinstance(text, str) or not text.strip():
            raise SurfaceCheckError(f"rule {rule_id!r} has invalid text")
        exception = entry.get("lineage_exception")
        if identifiers and not isinstance(exception, bool):
            raise SurfaceCheckError(f"rule {rule_id!r} has an invalid exception")
        rules.append(Rule(rule_id, text, exception if identifiers else False))
    return rules


def _load_rules(path: Path) -> tuple[list[Rule], list[Rule]]:
    """Load and validate the canonical YAML rule document."""
    if path.is_symlink() or not path.is_file():
        raise SurfaceCheckError("rules must be an existing regular file")
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SurfaceCheckError("rules file is not valid UTF-8 YAML") from exc
    phrases = _parse_rules(document, "retracted_phrases", identifiers=False)
    identifiers = _parse_rules(document, "foreign_identifiers", identifiers=True)
    rule_ids = [rule.id for rule in [*phrases, *identifiers]]
    if len(rule_ids) != len(set(rule_ids)):
        raise SurfaceCheckError("rule ids must be unique")
    return phrases, identifiers


def _normalize_with_offsets(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace and lowercase while retaining raw character offsets."""
    normalized: list[str] = []
    offsets: list[int] = []
    in_whitespace = False
    for offset, character in enumerate(text):
        if character.isspace():
            if not in_whitespace:
                normalized.append(" ")
                offsets.append(offset)
            in_whitespace = True
            continue
        lowered = character.lower()
        normalized.extend(lowered)
        offsets.extend([offset] * len(lowered))
        in_whitespace = False
    return "".join(normalized), offsets


def _line_number(text: str, offset: int) -> int:
    """Return the one-based line containing a raw character offset."""
    return text.count("\n", 0, offset) + 1


def _phrase_findings(text: str, relative_path: str, rules: list[Rule]) -> list[Finding]:
    """Find normalized phrase occurrences and map them back to source lines."""
    normalized, offsets = _normalize_with_offsets(text)
    findings: list[Finding] = []
    for rule in rules:
        needle, _ = _normalize_with_offsets(rule.text)
        cursor = 0
        while (match := normalized.find(needle, cursor)) >= 0:
            raw_offset = offsets[match]
            findings.append(
                Finding(
                    relative_path,
                    _line_number(text, raw_offset),
                    rule.id,
                    rule.text,
                    raw_offset,
                )
            )
            cursor = match + len(needle)
    return findings


def _entry_lineage_span(entry: _JsonNode, identifier: str) -> tuple[int, int] | None:
    """Return an allowed identifier-value span from one related entry."""
    if entry.members is None:
        return None
    identifiers = [node for key, node in entry.members if key == "identifier"]
    relations = [node for key, node in entry.members if key == "relation"]
    if len(identifiers) != 1 or len(relations) != 1:
        return None
    identifier_node, relation_node = identifiers[0], relations[0]
    if not isinstance(identifier_node.value, str):
        return None
    if identifier_node.value.lower() != identifier.lower():
        return None
    if relation_node.value not in LINEAGE_RELATIONS:
        return None
    return identifier_node.start, identifier_node.end


def _collect_lineage_spans(
    node: _JsonNode, identifier: str, spans: list[tuple[int, int]]
) -> None:
    """Collect allowed spans from every related-identifiers array."""
    if node.members is not None:
        for key, child in node.members:
            if key == "related_identifiers" and child.elements is not None:
                for entry in child.elements:
                    if span := _entry_lineage_span(entry, identifier):
                        spans.append(span)
            _collect_lineage_spans(child, identifier, spans)
    elif node.elements is not None:
        for child in node.elements:
            _collect_lineage_spans(child, identifier, spans)


def _lineage_spans(text: str, identifier: str) -> tuple[tuple[int, int], ...]:
    """Return allowed JSON source spans, or none for malformed metadata."""
    try:
        root = _JsonSpanParser(text).parse()
    except (json.JSONDecodeError, TypeError, ValueError):
        return ()
    spans: list[tuple[int, int]] = []
    _collect_lineage_spans(root, identifier, spans)
    return tuple(spans)


def _is_allowed(match: re.Match[str], spans: tuple[tuple[int, int], ...]) -> bool:
    """Return whether a raw match lies wholly inside an allowed JSON value."""
    return any(start <= match.start() and match.end() <= end for start, end in spans)


def _identifier_findings(
    text: str, relative_path: str, filename: str, rules: list[Rule]
) -> list[Finding]:
    """Find exact case-insensitive identifiers outside permitted lineage values."""
    findings: list[Finding] = []
    for rule in rules:
        spans = (
            _lineage_spans(text, rule.text)
            if filename == ".zenodo.json" and rule.lineage_exception
            else ()
        )
        for match in re.finditer(re.escape(rule.text), text, flags=re.IGNORECASE):
            if _is_allowed(match, spans):
                continue
            findings.append(
                Finding(
                    relative_path,
                    _line_number(text, match.start()),
                    rule.id,
                    rule.text,
                    match.start(),
                )
            )
    return findings


def _candidate_files(candidate: Path) -> list[Path]:
    """Return every regular non-symlink candidate file in path order."""
    if candidate.is_symlink() or not candidate.is_dir():
        raise SurfaceCheckError("candidate must be an existing regular directory")
    pending = [candidate]
    files: list[Path] = []
    while pending:
        directory = pending.pop()
        try:
            entries = list(directory.iterdir())
        except OSError as exc:
            relative = directory.relative_to(candidate).as_posix() or "."
            raise SurfaceCheckError(
                f"could not read candidate directory {relative}"
            ) from exc
        for path in entries:
            if path.is_symlink():
                continue
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                files.append(path)
    return sorted(files, key=lambda path: path.relative_to(candidate).as_posix())


def _check(candidate: Path, rules_path: Path) -> tuple[list[Finding], int, int]:
    """Scan a candidate and return findings, file count, and decode skips."""
    phrases, identifiers = _load_rules(rules_path)
    files = _candidate_files(candidate)
    findings: list[Finding] = []
    skipped = 0
    for path in files:
        relative = path.relative_to(candidate).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            skipped += 1
            continue
        except OSError as exc:
            raise SurfaceCheckError(
                f"could not read candidate file {relative}"
            ) from exc
        findings.extend(_phrase_findings(text, relative, phrases))
        findings.extend(_identifier_findings(text, relative, path.name, identifiers))
    findings.sort(
        key=lambda finding: (
            finding.relative_path,
            finding.line,
            finding.rule_id,
            finding.offset,
        )
    )
    return findings, len(files), skipped


def _parser() -> argparse.ArgumentParser:
    """Build the public release-surface argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--rules", default=DEFAULT_RULES, type=Path)
    return parser


def _run(options: argparse.Namespace) -> int:
    """Print deterministic findings and return their gate status."""
    findings, scanned, skipped = _check(options.candidate, options.rules)
    for finding in findings:
        print(
            f"{finding.relative_path}:{finding.line}: {finding.rule_id}: "
            f"{finding.matched_text}"
        )
    print(
        f"surface: {len(findings)} findings in {scanned} files scanned "
        f"({skipped} skipped undecodable)"
    )
    return 1 if findings else 0


def main(argv: list[str] | None = None) -> int:
    """Run the check with exit 0 clean, 1 findings, and 2 invalid input."""
    try:
        return _run(_parser().parse_args(argv))
    except SurfaceCheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValueError, TypeError):
        print("ERROR: invalid input", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
