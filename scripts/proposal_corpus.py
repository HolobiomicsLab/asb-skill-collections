"""Validate and update version 1.0 paper and resource proposal queues."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlsplit

import yaml


SCHEMA = "asb-corpus/1.0"
STATUSES = ("candidate", "hold", "included", "rejected", "duplicate")
DOCUMENT_KEYS = (
    "schema", "collection", "version", "generated_on", "source", "policy",
    "wave", "summary", "papers",
)
ROW_KEYS = (
    "name", "doi", "title", "year", "category", "repo_url", "status",
    "license_tier", "wave", "resource_type", "source_issue", "links",
    "source_watch", "source_queries", "relevance", "relevance_basis",
    "priority", "priority_reasons", "receipt", "access", "triage",
)
ACCESS_KEYS = (
    "type", "license", "is_oa", "provenance", "oa_status", "verified_via",
    "verified_on", "code_license",
)
TRIAGE_KEYS = (
    "proposer", "authors", "conflict_declared", "rationale", "decision",
    "notes", "curated_by", "curated_on",
)
ALLOWED_TRANSITIONS = {
    ("candidate", "hold"),
    ("hold", "included"),
}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
PREPRINT_VERSION = re.compile(
    r"^(10\.1101/\d{4}\.\d{2}\.\d{2}\.\d+)v\d+$", re.IGNORECASE
)
TRAILING_JUNK = re.compile(r"[.,;:)\]}>'\"]+$")
URL_PREFIX = re.compile(r"^(?:https?://)?(?:dx\.)?doi\.org/", re.IGNORECASE)
NON_ALNUM = re.compile(r"[^a-z0-9]+")
ARXIV_ID = re.compile(
    r"^(?:arxiv[:/])(?:abs/)?((?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7}))"
    r"(?:v\d+)?$", re.IGNORECASE
)
UNICODE_DASHES = str.maketrans(
    {dash: "-" for dash in "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"}
)
ARXIV_DOI_PREFIX = "10." + "48550/arxiv."


@dataclass(frozen=True)
class Violation:
    """A content error at a precise document path."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


@dataclass(frozen=True)
class Duplicate:
    """A proposal identity collision, ordered by duplicate precedence."""

    source: str
    severity: str
    row_path: str
    doi: str | None
    match: str
    message: str


class ProposalError(ValueError):
    """An unsafe requested mutation, rather than invalid loaded content."""


class _Dumper(yaml.SafeDumper):
    """Preserve mapping insertion order and disable YAML aliases."""

    def ignore_aliases(self, data: Any) -> bool:
        return True


def _represent_string(dumper: yaml.SafeDumper, value: str) -> yaml.Node:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _represent_string)


def normalise_doi(doi: Any) -> str | None:
    """Return a bare lowercase DOI using the corpus normalization rule."""
    if not isinstance(doi, str) or not doi.strip():
        return None
    text = doi.strip().translate(UNICODE_DASHES)
    text = URL_PREFIX.sub("", text)
    if text.lower().startswith("doi:"):
        text = text[4:].strip()
    text = TRAILING_JUNK.sub("", text).strip().lower()
    text = PREPRINT_VERSION.sub(r"\1", text)
    arxiv = ARXIV_ID.match(text)
    if arxiv:
        return ARXIV_DOI_PREFIX + arxiv.group(1).lower()
    return text if DOI_RE.match(text) else None


def _doi_key(doi: Any) -> str | None:
    normalised = normalise_doi(doi)
    return NON_ALNUM.sub("-", normalised).strip("-") if normalised else None


def _repository_identity(url: Any) -> str | None:
    if not isinstance(url, str):
        return None
    parsed = urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    path = parsed.path.rstrip("/").lower()
    if path.endswith(".git"):
        path = path[:-4]
    return f"{parsed.netloc.lower()}{path}"


def load(path: str | Path) -> Any:
    """Load YAML data without imposing validity on malformed content."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as error:
        return {"__load_error__": str(error)}


def _check_type(
    container: Mapping[str, Any], key: str, expected: type | tuple[type, ...],
    path: str, required: bool,
) -> list[Violation]:
    if key not in container:
        return [Violation(path, f"missing required field {key!r}")] if required else []
    value = container[key]
    valid = isinstance(value, expected)
    if expected is int:
        valid = valid and not isinstance(value, bool)
    return [] if valid else [Violation(
        f"{path}.{key}", f"expected {getattr(expected, '__name__', 'valid type')}"
    )]


def _check_string(container: Mapping[str, Any], key: str, path: str) -> list[Violation]:
    violations = _check_type(container, key, str, path, True)
    if not violations and not container[key].strip():
        violations.append(Violation(f"{path}.{key}", "must not be empty"))
    return violations


def _check_keys(
    container: Mapping[str, Any], allowed: Sequence[str], path: str,
) -> list[Violation]:
    return [Violation(f"{path}.{key}", "unknown field") for key in container
            if key not in allowed]


def _check_date(value: Any, path: str) -> list[Violation]:
    if not isinstance(value, str):
        return [Violation(path, "expected YYYY-MM-DD string")]
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return [Violation(path, "expected YYYY-MM-DD string")]
    return []


def _validate_access(access: Any, path: str) -> list[Violation]:
    if not isinstance(access, dict):
        return [Violation(path, "expected mapping")]
    violations = _check_keys(access, ACCESS_KEYS, path)
    for key in ("type", "license", "verified_via"):
        violations.extend(_check_string(access, key, path))
    violations.extend(_check_type(access, "is_oa", bool, path, True))
    if "verified_on" in access:
        violations.extend(_check_date(access["verified_on"], f"{path}.verified_on"))
    for key in ("provenance", "oa_status", "code_license"):
        violations.extend(_check_type(access, key, str, path, False))
    return violations


def _validate_triage(triage: Any, path: str) -> list[Violation]:
    if not isinstance(triage, dict):
        return [Violation(path, "expected mapping")]
    violations = _check_keys(triage, TRIAGE_KEYS, path)
    for key in ("proposer", "rationale", "decision", "notes"):
        violations.extend(_check_string(triage, key, path))
    violations.extend(_check_type(triage, "authors", str, path, False))
    violations.extend(_check_type(triage, "conflict_declared", bool, path, False))
    for key in ("curated_by",):
        violations.extend(_check_type(triage, key, str, path, False))
    if "curated_on" in triage:
        violations.extend(_check_date(triage["curated_on"], f"{path}.curated_on"))
    return violations


def _validate_row(row: Any, index: int) -> list[Violation]:
    path = f"papers[{index}]"
    if not isinstance(row, dict):
        return [Violation(path, "expected mapping")]
    violations = _check_keys(row, ROW_KEYS, path)
    for key in ("name", "title", "category", "repo_url", "status", "license_tier",
                "wave", "resource_type"):
        violations.extend(_check_string(row, key, path))
    if "year" not in row:
        violations.append(Violation(path, "missing required field 'year'"))
    elif row["year"] is not None and not isinstance(row["year"], int):
        violations.append(Violation(f"{path}.year", "expected integer or null"))
    if isinstance(row.get("year"), bool):
        violations.append(Violation(f"{path}.year", "expected integer or string"))
    violations.extend(_check_type(row, "source_issue", int, path, True))
    if "doi" in row and row["doi"] is not None:
        if not isinstance(row["doi"], str) or normalise_doi(row["doi"]) is None:
            violations.append(Violation(f"{path}.doi", "invalid DOI"))
    if row.get("status") not in STATUSES:
        violations.append(Violation(f"{path}.status", f"must be one of {STATUSES}"))
    for key in ("links", "source_queries", "priority_reasons"):
        violations.extend(_check_type(row, key, list, path, False))
        if isinstance(row.get(key), list):
            for item_index, item in enumerate(row[key]):
                if not isinstance(item, str):
                    violations.append(Violation(
                        f"{path}.{key}[{item_index}]", "expected string"
                    ))
    for key in ("source_watch", "relevance", "relevance_basis", "receipt"):
        violations.extend(_check_type(row, key, str, path, False))
    if "source_watch" in row:
        violations.extend(_check_date(row["source_watch"], f"{path}.source_watch"))
    violations.extend(_check_type(row, "priority", int, path, False))
    if "access" in row:
        violations.extend(_validate_access(row["access"], f"{path}.access"))
    else:
        violations.append(Violation(path, "missing required field 'access'"))
    if "triage" in row:
        violations.extend(_validate_triage(row["triage"], f"{path}.triage"))
    else:
        violations.append(Violation(path, "missing required field 'triage'"))
    return violations


def _validate_summary(document: Mapping[str, Any]) -> list[Violation]:
    summary = document.get("summary")
    if not isinstance(summary, dict):
        return [Violation("summary", "expected mapping")]
    violations = _check_type(summary, "total", int, "summary", True)
    for key in summary:
        if key != "total" and key not in STATUSES:
            violations.append(Violation(f"summary.{key}", "unknown status"))
        elif key != "total":
            violations.extend(_check_type(summary, key, int, "summary", True))
    papers_valid = isinstance(document.get("papers"), list) and all(
        isinstance(row, dict) and row.get("status") in STATUSES
        for row in document["papers"]
    )
    if papers_valid and not violations:
        expected = recompute_summary(document)
        if any(summary.get(key) != value for key, value in expected.items()
               if key == "total" or key in summary):
            violations.append(Violation(
                "summary", f"stale summary; expected {expected!r}"
            ))
    return violations


def validate(document: Any) -> list[Violation]:
    """Return all schema and consistency errors without raising for content."""
    if not isinstance(document, dict):
        return [Violation("$", "expected mapping")]
    if "__load_error__" in document:
        return [Violation("$", f"invalid YAML: {document['__load_error__']}")]
    violations = _check_keys(document, DOCUMENT_KEYS, "$")
    if document.get("schema") != SCHEMA:
        violations.append(Violation("schema", f"must be {SCHEMA!r}"))
    for key in ("collection", "source", "policy", "wave"):
        violations.extend(_check_string(document, key, "$"))
    violations.extend(_check_type(document, "version", int, "$", True))
    if "generated_on" in document:
        violations.extend(_check_date(document["generated_on"], "generated_on"))
    else:
        violations.append(Violation("$", "missing required field 'generated_on'"))
    papers = document.get("papers")
    if isinstance(papers, list):
        for index, row in enumerate(papers):
            violations.extend(_validate_row(row, index))
    else:
        violations.append(Violation("papers", "expected list"))
    if "summary" in document:
        violations.extend(_validate_summary(document))
    else:
        violations.append(Violation("$", "missing required field 'summary'"))
    return violations


def recompute_summary(document: Mapping[str, Any]) -> dict[str, int]:
    """Calculate total and all five status counts from the current rows."""
    rows = document.get("papers", [])
    if not isinstance(rows, list):
        raise ProposalError("papers must be a list")
    summary = {status: 0 for status in STATUSES}
    for row in rows:
        status = row.get("status") if isinstance(row, dict) else None
        if status in STATUSES:
            summary[status] += 1
    return {"total": len(rows), **summary}


def _covered_keys(covered: Any) -> set[str]:
    if isinstance(covered, dict) and isinstance(covered.get("covered"), dict):
        covered = covered["covered"]
    if isinstance(covered, dict):
        return {key for key in covered if isinstance(key, str)}
    if isinstance(covered, (list, tuple, set)):
        return {key for item in covered if (key := _doi_key(item))}
    return set()


def _corpus_rows(corpus_rows: Any) -> list[Mapping[str, Any]]:
    if isinstance(corpus_rows, dict):
        corpus_rows = corpus_rows.get("papers", corpus_rows.get("corpus", []))
    return [row for row in corpus_rows or [] if isinstance(row, dict)]


def _proposal_rows(documents: Any) -> list[tuple[int, int, Mapping[str, Any]]]:
    if isinstance(documents, dict):
        documents = [documents]
    return [(doc_index, row_index, row)
            for doc_index, document in enumerate(documents or [])
            for row_index, row in enumerate(document.get("papers", []))
            if isinstance(row, dict)]


def find_duplicates(
    documents: Any, covered: Any, corpus_rows: Any,
) -> list[Duplicate]:
    """Find DOI collisions first, then warn about matching repositories."""
    errors: list[Duplicate] = []
    warnings: list[Duplicate] = []
    covered_keys = _covered_keys(covered)
    released = {_doi_key(row.get("doi")): normalise_doi(row.get("doi"))
                for row in _corpus_rows(corpus_rows) if _doi_key(row.get("doi"))}
    released_repos = {_repository_identity(row.get("repo_url")): normalise_doi(row.get("doi")) or "released row"
                      for row in _corpus_rows(corpus_rows) if _repository_identity(row.get("repo_url"))}
    proposal_identities: dict[str, str] = {}
    proposal_dois: dict[str, str] = {}
    for index, row_index, row in _proposal_rows(documents):
        path = f"documents[{index}].papers[{row_index}]"
        doi = normalise_doi(row.get("doi"))
        key = _doi_key(doi)
        source = None
        match = None
        if key and key in covered_keys:
            source, match = "covered", doi or key
        elif key and key in released:
            source, match = "corpus", released[key]
        elif key and key in proposal_dois:
            source, match = "proposal", proposal_dois[key]
        if source:
            errors.append(Duplicate(source, "error", path, doi, match or "",
                                    f"duplicate DOI in {source}"))
        if doi and key not in covered_keys and key not in released and key not in proposal_dois:
            proposal_dois[key] = doi
        repo = _repository_identity(row.get("repo_url"))
        repo_match = released_repos.get(repo) or proposal_identities.get(repo)
        if repo and repo_match:
            warnings.append(Duplicate("repository", "warning", path, doi, repo_match,
                                      "same repository identity; verify whether papers differ"))
        if repo and repo not in released_repos:
            proposal_identities.setdefault(repo, doi or f"row {path}")
    return errors + warnings


def _row_sort_key(row: Mapping[str, Any]) -> tuple[int, str, int]:
    doi = normalise_doi(row.get("doi"))
    issue = row.get("source_issue")
    return (doi is None, doi or "", issue if isinstance(issue, int) else -1)


def add_row(document: dict[str, Any], row: Mapping[str, Any]) -> dict[str, Any]:
    """Add a distinct row in stable DOI/issue order and refresh the summary."""
    if not isinstance(document.get("papers"), list):
        raise ProposalError("document.papers must be a list")
    key = _doi_key(row.get("doi"))
    if key and any(_doi_key(item.get("doi")) == key for item in document["papers"]
                   if isinstance(item, dict)):
        raise ProposalError(f"duplicate DOI: {normalise_doi(row.get('doi'))}")
    document["papers"].append(dict(row))
    document["papers"].sort(key=_row_sort_key)
    document["summary"] = recompute_summary(document)
    return document


def set_status(
    document: dict[str, Any], doi: str, status: str, decision: str,
    by: str, on: str, notes: str,
) -> dict[str, Any]:
    """Apply one allowed transition and record its curator evidence."""
    target = normalise_doi(doi)
    matches = [row for row in document.get("papers", [])
               if isinstance(row, dict) and normalise_doi(row.get("doi")) == target]
    if target is None or len(matches) != 1:
        raise ProposalError("DOI must identify exactly one proposal row")
    row = matches[0]
    current = row.get("status")
    terminal = status in {"rejected", "duplicate"}
    if (current, status) not in ALLOWED_TRANSITIONS and not (terminal and current != status):
        raise ProposalError(f"transition {current!r} to {status!r} is not allowed")
    if not all(isinstance(value, str) and value.strip()
               for value in (decision, by, on, notes)):
        raise ProposalError("decision, curator, date and notes are required")
    if _check_date(on, "on"):
        raise ProposalError("date must be YYYY-MM-DD")
    row["status"] = status
    triage = row.setdefault("triage", {})
    triage.update(decision=decision, notes=notes, curated_by=by, curated_on=on)
    document["summary"] = recompute_summary(document)
    return document


def _ordered_mapping(value: Mapping[str, Any], keys: Sequence[str]) -> dict[str, Any]:
    ordered = {key: value[key] for key in keys if key in value}
    ordered.update((key, item) for key, item in value.items() if key not in ordered)
    return ordered


def _canonical_document(document: Mapping[str, Any]) -> dict[str, Any]:
    result = _ordered_mapping(document, DOCUMENT_KEYS)
    if isinstance(result.get("summary"), dict):
        summary = result["summary"]
        result["summary"] = _ordered_mapping(summary, ("total", *STATUSES))
    if isinstance(result.get("papers"), list):
        result["papers"] = [_canonical_row(row) if isinstance(row, dict) else row
                            for row in result["papers"]]
    return result


def _canonical_row(row: Mapping[str, Any]) -> dict[str, Any]:
    result = _ordered_mapping(row, ROW_KEYS)
    if isinstance(result.get("access"), dict):
        result["access"] = _ordered_mapping(result["access"], ACCESS_KEYS)
    if isinstance(result.get("triage"), dict):
        result["triage"] = _ordered_mapping(result["triage"], TRIAGE_KEYS)
    return result


def dump(document: Mapping[str, Any]) -> str:
    """Return deterministic block-style YAML, without aliases or sorted keys."""
    return yaml.dump(
        _canonical_document(document), Dumper=_Dumper, sort_keys=False,
        default_flow_style=False, allow_unicode=True, width=88,
    )


def _load_corpus(path: str) -> Any:
    return load(path)


def _summary_command(path: str, write: bool) -> int:
    document = load(path)
    violations = validate(document)
    structural = [item for item in violations if item.path == "summary"]
    if len(violations) != len(structural):
        for violation in violations:
            print(f"{path}: {violation}", file=sys.stderr)
        return 1
    summary = recompute_summary(document)
    print(f"{path}: {json.dumps(summary, sort_keys=True)}")
    if write:
        document["summary"] = summary
        Path(path).write_text(dump(document), encoding="utf-8")
    return 0


def _validate_command(paths: Iterable[str]) -> int:
    failed = False
    for path in paths:
        violations = validate(load(path))
        if violations:
            failed = True
            print(f"FAIL {path}:")
            for violation in violations:
                print(f"  - {violation}")
        else:
            print(f"OK   {path}")
    return int(failed)


def _duplicates_command(args: argparse.Namespace) -> int:
    documents = [load(path) for path in args.files]
    if any(validate(document) for document in documents):
        return _validate_command(args.files)
    covered = json.loads(Path(args.covered).read_text(encoding="utf-8"))
    duplicates = find_duplicates(documents, covered, _load_corpus(args.corpus))
    for duplicate in duplicates:
        print(f"{duplicate.severity.upper()} {duplicate.row_path}: {duplicate.message}; "
              f"match={duplicate.match}; source={duplicate.source}")
    return int(any(item.severity == "error" for item in duplicates))


def main(argv: Sequence[str] | None = None) -> int:
    """Run the proposal validation, summary, or duplicate-check command."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("files", nargs="+")
    summary_parser = commands.add_parser("summary")
    summary_parser.add_argument("file")
    summary_parser.add_argument("--write", action="store_true")
    duplicate_parser = commands.add_parser("check-duplicates")
    duplicate_parser.add_argument("--covered", required=True)
    duplicate_parser.add_argument("--corpus", required=True)
    duplicate_parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    if args.command == "validate":
        return _validate_command(args.files)
    if args.command == "summary":
        return _summary_command(args.file, args.write)
    return _duplicates_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
