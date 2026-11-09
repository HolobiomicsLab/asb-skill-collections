"""Stage a paper proposal from an untrusted GitHub issue JSON object."""
from __future__ import annotations

if __package__ in (None, ""):
    import os.path as _path
    import sys as _sys

    _sys.path.insert(0, _path.dirname(_path.dirname(_path.abspath(__file__))))

import argparse
import datetime as dt
import glob
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from scripts import intake_resolvers
from scripts import proposal_corpus as corpus
from scripts.license_tier import tier_for_license

MAX_BODY_CHARS = 20_000
MAX_FIELD_CHARS = 4_000
MAX_TITLE_CHARS = 1_000
QUEUED_SENTENCE = "This is queued for curator review, not built. The issue remains open until its build lands."
NEW_WAVE_HEADER = "# Community proposal queue, staged for the next curation wave.\n\n"
REQUIRED_FIELDS = ("What is it?", "Link:", "Type:", "Target collection:",
                   "Why it matters (one or two sentences):")
FIELD_ALIASES = {name.lower(): name for name in REQUIRED_FIELDS}
FIELD_ALIASES.update({"open access?": "Open access?", "you:": "You:",
                      "conflict of interest?": "Conflict of interest?"})
ALLOWED_HOSTS = {
    "doi.org", "dx.doi.org", "github.com", "arxiv.org", "biorxiv.org", "medrxiv.org",
    "nature.com", "academic.oup.com", "sciencedirect.com", "linkinghub.elsevier.com",
    "mdpi.com", "pubs.rsc.org", "pubs.acs.org", "cell.com", "onlinelibrary.wiley.com",
    "journals.plos.org", "ieeexplore.ieee.org", "link.springer.com", "frontiersin.org",
    "bmcbioinformatics.biomedcentral.com", "researchsquare.com",
}
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FIELD_MARKER = re.compile(r"\*\*([^*\n]+)\*\*")
DOI_TEXT = re.compile(r"^(?:doi:\s*)?10\.\d{4,9}/", re.IGNORECASE)
OUTCOMES = {"staged": 0, "blocked": 1, "duplicate": 2}
OPEN_ACCESS_TYPES = {"open-access", "gold", "gold-oa", "hybrid", "green", "green-oa", "diamond"}


class IntakeError(ValueError):
    """An invalid issue or unsafe local input that blocks staging."""


def parse_fields(body: Any) -> dict[str, str]:
    """Read the exact bold template fields after removing HTML comments."""
    if not isinstance(body, str):
        raise IntakeError("Issue body must be a string.")
    if len(body) > MAX_BODY_CHARS:
        raise IntakeError(f"Issue body exceeds {MAX_BODY_CHARS} characters.")
    clean = COMMENT.sub("", body)
    markers = list(FIELD_MARKER.finditer(clean))
    fields: dict[str, str] = {}
    for index, marker in enumerate(markers):
        canonical = FIELD_ALIASES.get(marker.group(1).strip().lower())
        if canonical is None:
            continue
        end = markers[index + 1].start() if index + 1 < len(markers) else len(clean)
        value = clean[marker.end():end].strip()
        value = re.sub(r"^-+\s*$", "", value, flags=re.MULTILINE).strip()
        if len(value) > MAX_FIELD_CHARS:
            raise IntakeError(f"Field {canonical} exceeds {MAX_FIELD_CHARS} characters.")
        fields[canonical] = value
    return fields


def validate_issue(issue: Mapping[str, Any], domain: str, kind: str) -> dict[str, str]:
    """Validate required fields and return their untrusted string values."""
    if kind != "paper":
        raise IntakeError("Only --kind paper is implemented; workflow proposals are not supported.")
    if not isinstance(issue.get("number"), int) or isinstance(issue.get("number"), bool):
        raise IntakeError("Issue number must be an integer.")
    fields = parse_fields(issue.get("body"))
    for name in REQUIRED_FIELDS:
        if not fields.get(name):
            raise IntakeError(f"Required field {name} is missing or empty.")
    if fields["Type:"].strip().lower() not in {"paper", "tool", "data resource"}:
        raise IntakeError("Type must be paper, tool, or data resource for paper intake.")
    if fields["Target collection:"].strip().lower() != domain.lower():
        raise IntakeError(f"Target collection must be {domain}.")
    if fields.get("Link:"):
        validate_link(fields["Link:"])
    author = issue.get("author") or {}
    if not isinstance(author.get("login"), str) or not author["login"].strip():
        raise IntakeError("Issue author login is required.")
    return fields


def validate_link(link: str) -> None:
    """Allow bare DOIs and fixed HTTPS registry or public repository hosts."""
    if DOI_TEXT.match(link.strip()):
        return
    parsed = urlsplit(link.strip())
    if parsed.scheme != "https":
        raise IntakeError("Link must be a bare DOI or an HTTPS URL.")
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if parsed.username or parsed.password or parsed.port not in {None, 443}:
        raise IntakeError("Link must not contain credentials or a nonstandard port.")
    if host not in ALLOWED_HOSTS:
        raise IntakeError(f"Link host {host or '(missing)'} is not an allowed registry or repository host.")


def resolve_identity(fields: Mapping[str, str], resolver: intake_resolvers.Resolver) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve a direct DOI, publisher URL, repository, or exact-ish title."""
    link = fields["Link:"].strip()
    doi = intake_resolvers.doi_from_url(link, corpus.normalise_doi)
    warnings: list[str] = []
    if doi:
        return resolver.by_doi(doi), warnings
    if intake_resolvers.github_repository(link):
        title = fields["What is it?"].strip()
        metadata = resolver.by_title(title, None)
        if metadata:
            return metadata, warnings
        return {"doi": None, "title": title, "year": None, "repository": link,
                "type": fields["Type:"], "registry": "issue", "license_urls": []}, warnings
    title = fields["What is it?"].strip()
    metadata = resolver.by_title(title, intake_resolvers.expected_prefix(link))
    if metadata:
        return metadata, warnings
    raise IntakeError("The link is not a paper or public GitHub repository and its title did not resolve to a unique DOI.")


def follow_published_version(metadata: dict[str, Any], resolver: intake_resolvers.Resolver) -> tuple[dict[str, Any], list[str]]:
    """Prefer a registry-declared published DOI over a preprint DOI."""
    published = metadata.get("published_doi") or intake_resolvers.published_doi(metadata, corpus.normalise_doi)
    if not published or published == metadata.get("doi"):
        return metadata, []
    resolved = resolver.by_doi(published)
    if not resolved:
        return metadata, [f"Published DOI {published} was declared but could not be resolved."]
    return resolved, [f"Preprint replaced by its registry-declared published DOI {published}."]


def resolve_access(metadata: Mapping[str, Any], resolver: intake_resolvers.Resolver,
                   email: str | None, date: str) -> dict[str, Any]:
    """Combine Unpaywall access with registry reuse rights on separate evidence."""
    doi = metadata.get("doi")
    if not doi:
        return {"type": "not-applicable", "license": "unknown", "is_oa": False,
                "verified_via": "unresolved", "verified_on": date, "source_reuse": "unknown"}
    try:
        access = resolver.access(doi, email)
    except intake_resolvers.RegistryUnavailable as error:
        access = intake_resolvers._unresolved_access(str(error))
    registry = resolver.registry_license(metadata)
    if registry:
        access = apply_registry_license(access, registry)
    access["verified_on"] = date
    access["license"] = access.get("license") or "unknown"
    return access


def apply_registry_license(access: dict[str, Any], registry: Mapping[str, Any]) -> dict[str, Any]:
    """Use declared article rights when they provide stronger reuse evidence."""
    if registry.get("spdx"):
        access["registry_license"] = registry["spdx"]
        access["registry_source_reuse"] = registry.get("source_reuse") or "unknown"
        if access.get("license") in {None, "unknown"}:
            access["license"] = registry["spdx"]
            access["source_reuse"] = registry.get("source_reuse") or "unknown"
        if registry["source_reuse"] == "full" and access.get("verified_via") == "unresolved":
            access["registry_open_reuse"] = True
    return access


def proposal_paths(patterns: Sequence[str]) -> list[Path]:
    """Expand explicit proposal globs deterministically."""
    return [Path(name) for pattern in patterns for name in sorted(glob.glob(pattern))]


def validate_sources(wave_path: Path, paths: Sequence[Path], collection_path: Path) -> None:
    """Refuse malformed existing queues before calculating duplicates."""
    documents = [(path, corpus.load(path)) for path in paths]
    if wave_path.exists() and wave_path not in paths:
        documents.append((wave_path, corpus.load(wave_path)))
    for path, document in documents:
        violations = corpus.validate(document)
        if violations:
            raise IntakeError(f"Invalid proposal file {path.name}: {violations[0]}")
    if not collection_path.exists():
        raise IntakeError("Collection corpus file is required.")


def own_row(paths: Sequence[Path], wave_path: Path, issue_number: int) -> tuple[Path, dict[str, Any], int] | None:
    """Locate this issue's existing row before considering other duplicates."""
    candidates = list(dict.fromkeys([wave_path, *paths]))
    matches = []
    for path in candidates:
        if not path.exists():
            continue
        document = corpus.load(path)
        for index, row in enumerate(document.get("papers") or []):
            if row.get("source_issue") == issue_number:
                matches.append((path, document, index))
    if len(matches) > 1:
        raise IntakeError(f"Issue {issue_number} has multiple existing proposal rows.")
    return matches[0] if matches else None


def existing_identity_row(metadata: Mapping[str, Any], own: tuple[Path, dict[str, Any], int] | None) -> dict[str, Any] | None:
    """Find this issue's existing row by DOI, title, or repository after an edit."""
    if not own:
        return None
    row = own[1]["papers"][own[2]]
    for key in ("doi", "repository", "title"):
        incoming = metadata.get("repository" if key == "repository" else key)
        previous = row.get("repo_url" if key == "repository" else key)
        if key == "doi" and incoming and doi_key(previous) == doi_key(incoming):
            return row
        if key != "doi" and incoming and str(previous).casefold() == str(incoming).casefold():
            return row
    return None


def duplicate_match(metadata: Mapping[str, Any], inputs: Mapping[str, Any],
                    own: tuple[Path, dict[str, Any], int] | None) -> dict[str, Any] | None:
    """Check covered, released corpus, then other proposals in fixed order."""
    doi = corpus.normalise_doi(metadata.get("doi"))
    if not doi:
        return None
    key = doi_key(doi)
    covered = json.loads(Path(inputs["covered"]).read_text(encoding="utf-8"))
    if key in covered_keys(covered):
        return {"where": "covered", "path": Path(inputs["covered"]).name, "doi": doi,
                "stage": "covered"}
    released = corpus.load(inputs["collection_corpus"])
    for row in released.get("papers", released.get("corpus", [])) or []:
        if doi_key(row.get("doi")) == key:
            return {"where": "corpus", "path": Path(inputs["collection_corpus"]).name,
                    "doi": doi, "stage": row.get("status") or "included"}
    for path in inputs["proposal_paths"]:
        document = corpus.load(path)
        for index, row in enumerate(document.get("papers") or []):
            if own and path == own[0] and index == own[2]:
                continue
            if doi_key(row.get("doi")) == key:
                return {"where": "proposal", "path": path.name, "doi": doi,
                        "stage": row.get("status") or "candidate"}
    return None


def repository_duplicate_warning(metadata: Mapping[str, Any], paths: Sequence[Path],
                                 own: tuple[Path, dict[str, Any], int] | None) -> str | None:
    """Warn about a shared repository without treating it as the same paper."""
    incoming = intake_resolvers.github_repository(metadata.get("repository"))
    if not incoming:
        return None
    for path in paths:
        for index, row in enumerate(corpus.load(path).get("papers") or []):
            if own and path == own[0] and index == own[2]:
                continue
            if intake_resolvers.github_repository(row.get("repo_url")) == incoming:
                return f"Same repository identity as {path.name}; verify whether papers differ."
    return None


def doi_key(value: Any) -> str | None:
    """Use the same punctuation-folded identity as proposal_corpus."""
    doi = corpus.normalise_doi(value)
    return re.sub(r"[^a-z0-9]+", "-", doi).strip("-") if doi else None


def covered_keys(covered: Any) -> set[str]:
    """Read the covered registry's map or list forms."""
    if isinstance(covered, dict) and isinstance(covered.get("covered"), dict):
        covered = covered["covered"]
    if isinstance(covered, dict):
        return set(covered)
    if isinstance(covered, list):
        return {key for item in covered if (key := doi_key(item))}
    return set()


def build_row(fields: Mapping[str, str], metadata: Mapping[str, Any], access: Mapping[str, Any],
              repository: Mapping[str, Any] | None, issue: Mapping[str, Any], date: str) -> dict[str, Any]:
    """Construct one schema-valid candidate or held proposal row."""
    repo_url = (repository or {}).get("repository") or metadata.get("repository")
    code_license = (repository or {}).get("code_license")
    if code_license in {None, "NOASSERTION"}:
        code_license = None
    tier = tier_for_license(code_license) if code_license else "unknown"
    reasons = hold_reasons(metadata, access, repository)
    row = {
        "name": fields["What is it?"].strip()[:MAX_TITLE_CHARS],
        "doi": metadata.get("doi"), "title": metadata.get("title"),
        "year": metadata.get("year"), "category": category_for(metadata),
        "repo_url": repo_url, "status": "candidate" if reasons else "hold",
        "license_tier": tier, "wave": f"community-{date[:7]}",
        "resource_type": resource_type_for(metadata),
        "source_issue": issue["number"],
        "links": [fields["Link:"].strip()],
        "access": {key: value for key, value in access.items() if key in corpus.ACCESS_KEYS},
        "triage": {
            "proposer": issue["author"]["login"],
            "conflict_declared": has_conflict(fields.get("Conflict of interest?", "")),
            "rationale": fields["Why it matters (one or two sentences):"].strip(),
            "decision": "pending",
            "notes": "; ".join(reasons) if reasons else "Machine checks passed; awaiting curator review.",
        },
    }
    row["access"]["code_license"] = code_license or "unknown"
    return row


def hold_reasons(metadata: Mapping[str, Any], access: Mapping[str, Any],
                 repository: Mapping[str, Any] | None) -> list[str]:
    """Explain every condition that prevents a verified held paper."""
    reasons = []
    if not metadata.get("doi") or not metadata.get("title") or metadata.get("year") is None:
        reasons.append("identity or publication year is unresolved")
    if access.get("verified_via") == "unresolved":
        reasons.append("paper access resolution is unresolved")
    elif access.get("type") not in OPEN_ACCESS_TYPES or access.get("is_oa") is not True:
        reasons.append(f"paper access is {access.get('type') or 'unknown'}")
    if access.get("source_reuse") != "permissive" and access.get("source_reuse") != "full":
        reasons.append("paper reuse licence is not established as fully reusable")
    if repository and repository.get("status") in {"gone", "moved", "unknown"}:
        reasons.append(f"repository status is {repository['status']}")
    if not (repository or {}).get("repository") and not metadata.get("repository"):
        reasons.append("no repository established; a held row needs one")
    return reasons


def category_for(metadata: Mapping[str, Any]) -> str:
    """Assign a transparent coarse category for curator refinement."""
    kind = str(metadata.get("type") or "").lower()
    return "Software" if kind in {"software", "tool"} else "Annotation"


def resource_type_for(metadata: Mapping[str, Any]) -> str:
    """Distinguish software resources from ordinary papers."""
    kind = str(metadata.get("type") or "").lower()
    return "software-tool" if kind in {"software", "tool"} else "paper"


def has_conflict(statement: str) -> bool:
    """Record whether the proposer supplied a substantive conflict statement."""
    cleaned = statement.strip().lower().strip(".")
    return bool(cleaned and cleaned not in {"no", "none", "n/a", "not applicable", "no conflict"})


def new_document(domain: str, date: str, version: int) -> dict[str, Any]:
    """Create a monthly community wave using the live document conventions."""
    document = {"schema": corpus.SCHEMA, "collection": domain, "version": version,
                "generated_on": date, "source": "community proposals (GitHub issues), automated intake",
                "policy": "OPEN_ACCESS_POLICY.md (OA verified per entry)",
                "wave": f"community-{date[:7]}", "papers": []}
    document["summary"] = corpus.recompute_summary(document)
    return document


def write_row(destination: Path, document: dict[str, Any], row: dict[str, Any],
              existing_index: int | None, dry_run: bool) -> None:
    """Canonicalize once, then leave an unchanged document byte-identical."""
    original = destination.read_text(encoding="utf-8") if destination.exists() else None
    if existing_index is not None:
        previous = document["papers"][existing_index]
        if previous.get("triage", {}).get("decision") in {"accept", "reject"}:
            row["triage"]["decision"] = previous["triage"]["decision"]
            row["triage"]["notes"] = previous["triage"].get("notes", row["triage"]["notes"])
        if previous.get("status") in {"included", "rejected"}:
            row["status"] = previous["status"]
        document["papers"][existing_index] = row
        document["papers"].sort(key=lambda item: (item.get("doi") is None, item.get("doi") or "",
                                                  item.get("source_issue", -1)))
    else:
        corpus.add_row(document, row)
    violations = corpus.validate(document)
    if violations:
        raise IntakeError(f"Generated proposal is invalid: {violations[0]}")
    rendered = corpus.dump(document)
    if original and original.startswith(NEW_WAVE_HEADER):
        rendered = NEW_WAVE_HEADER + rendered
    if original == rendered:
        return
    if original and not original.startswith(NEW_WAVE_HEADER):
        rendered = corpus.dump(document)
        if original == rendered:
            return
    if dry_run:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(rendered, encoding="utf-8")


def sha256(path: Path) -> str | None:
    """Hash an input file, or report its absence."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def safe_text(value: Any) -> str:
    """Render untrusted field text as one escaped Markdown line."""
    text = str(value) if value is not None else "unresolved"
    text = re.sub(r"[\r\n\x00-\x1f]+", " ", text).strip()
    return text.replace("`", "\\`")[:MAX_FIELD_CHARS]


def comment_markdown(receipt: Mapping[str, Any]) -> str:
    """Compose the complete public issue comment without local paths."""
    lines = ["## ASB paper intake", ""]
    if receipt["outcome"] == "blocked":
        lines.extend(["**Outcome: blocked.**", "", *[f"- {safe_text(item)}" for item in receipt["warnings"]]])
    elif receipt["outcome"] == "duplicate":
        duplicate = receipt["duplicate_of"]
        lines.extend(["**Outcome: duplicate.**", "",
                      f"- Existing stage: {safe_text(duplicate.get('stage'))}",
                      f"- Existing file: {safe_text(duplicate['path'])}",
                      f"- DOI: {safe_text(receipt['doi'])}"])
    else:
        access = receipt["access"] or {}
        lines.extend([f"**Outcome: staged as {receipt['row']['status']}.**", "",
                      f"- Title: {safe_text(receipt['title'])}",
                      f"- DOI: {safe_text(receipt['doi'])}",
                      f"- Repository: {safe_text(receipt['repository'])}",
                      f"- Open access: {safe_text(access.get('is_oa'))} ({safe_text(access.get('type'))})",
                      f"- Article reuse licence: {safe_text(access.get('license'))}",
                      f"- Code licence: {safe_text(receipt['code_license'])}"])
        for warning in receipt["warnings"]:
            lines.append(f"- Warning: {safe_text(warning)}")
        conflict = receipt.get("conflict_statement") or "None declared"
        lines.append(f"- Conflict of interest: {safe_text(conflict)}")
        lines.extend(["", QUEUED_SENTENCE])
    return "\n".join(lines) + "\n"


def make_receipt(issue: Mapping[str, Any], options: Mapping[str, Any], outcome: str) -> dict[str, Any]:
    """Create the complete receipt envelope shared with the issue Action."""
    number = issue.get("number") if isinstance(issue.get("number"), int) else 0
    return {"schema": "asb-intake-receipt/1", "outcome": outcome, "kind": options["kind"],
            "issue": number, "domain": options["domain"], "date": options["date"],
            "doi": None, "title": None, "repository": None, "access": None,
            "code_license": None, "warnings": [], "duplicate_of": None, "row": None,
            "wave_file": None,
            "inputs_sha256": {"issue_json": sha256(Path(options["issue_json"])),
                              "wave_file_before": sha256(Path(options["wave_file"]))},
            "comment_markdown": "", "labels_add": [], "labels_remove": []}


def write_receipt(path: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    """Finish comment and labels, then always persist the receipt."""
    receipt["comment_markdown"] = comment_markdown(receipt)
    if receipt["outcome"] == "staged":
        receipt.update(labels_add=["intake-staged"], labels_remove=["intake-blocked", "needs-triage"])
    elif receipt["outcome"] == "blocked":
        receipt.update(labels_add=["intake-blocked"], labels_remove=["intake-staged"])
    else:
        receipt.update(labels_add=["duplicate"], labels_remove=["intake-staged", "intake-blocked"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


def run_intake(*, kind: str, issue_json: str, domain: str, wave_file: str, covered: str,
               collection_corpus: str, proposal_glob: Sequence[str], date: str, out: str,
               dry_run: bool = False, fetcher: intake_resolvers.Fetch | None = None,
               email: str | None = None, sleep: intake_resolvers.Sleep = lambda seconds: None) -> dict[str, Any]:
    """Run paper intake with explicit paths and an injected network transport."""
    issue_path = Path(issue_json)
    options = {"kind": kind, "issue_json": issue_json, "domain": domain, "date": date,
               "wave_file": wave_file}
    receipt = make_receipt({}, options, "blocked")
    try:
        issue = json.loads(issue_path.read_text(encoding="utf-8"))
        if not isinstance(issue, dict):
            raise IntakeError("Issue JSON must contain an object.")
        receipt = make_receipt(issue, options, "blocked")
        dt.date.fromisoformat(date)
        fields = validate_issue(issue, domain, kind)
        paths = proposal_paths(proposal_glob)
        wave_path = Path(wave_file)
        validate_sources(wave_path, paths, Path(collection_corpus))
        resolver = intake_resolvers.Resolver(fetcher or intake_resolvers.http_json, sleep, corpus.normalise_doi)
        metadata, warnings = resolve_identity(fields, resolver)
        if not metadata:
            raise IntakeError(f"DOI {corpus.normalise_doi(fields['Link:']) or fields['Link:']} could not be resolved.")
        metadata, published_warnings = follow_published_version(metadata, resolver)
        warnings.extend(published_warnings)
        receipt.update(doi=metadata.get("doi"), title=metadata.get("title"),
                       repository=metadata.get("repository"), warnings=warnings)
        inputs = {"covered": covered, "collection_corpus": collection_corpus, "proposal_paths": paths}
        own = own_row(paths, wave_path, issue["number"])
        duplicate = duplicate_match(metadata, inputs, own)
        repository_warning = repository_duplicate_warning(metadata, paths, own)
        if repository_warning:
            warnings.append(repository_warning)
        if duplicate and not existing_identity_row(metadata, own):
            receipt.update(outcome="duplicate", duplicate_of=duplicate)
            return write_receipt(Path(out), receipt)
        if duplicate:
            warnings.append("An edited identity matched this issue's own existing proposal row.")
        access = resolve_access(metadata, resolver, email, date)
        repository = resolver.repository(metadata.get("repository"))
        if repository:
            receipt["repository"] = repository.get("repository") or metadata.get("repository")
        if repository and repository.get("status") != "exists":
            warnings.append(f"Repository is {repository.get('status')}; build availability needs curator review.")
        row = build_row(fields, metadata, access, repository, issue, date)
        receipt["conflict_statement"] = fields.get("Conflict of interest?", "").strip()
        if own:
            destination, document, index = own
        else:
            destination, document, index = wave_path, new_document(domain, date, collection_version(collection_corpus)), None
            if wave_path.exists():
                document = corpus.load(wave_path)
        write_row(destination, document, row, index, dry_run)
        receipt.update(outcome="staged", access=access, row=row,
                       code_license=(repository or {}).get("code_license"),
                       wave_file=str(destination))
    except (IntakeError, json.JSONDecodeError, OSError, intake_resolvers.RegistryUnavailable) as error:
        receipt["warnings"].append(str(error))
    return write_receipt(Path(out), receipt)


def collection_version(path: str) -> int:
    """Derive the wave version from its explicit released corpus path."""
    match = re.search(r"(?:^|/)v(\d+)(?:/|$)", path)
    return int(match.group(1)) if match else 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the stable interface consumed by the separate issue Action."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["paper", "workflow"], required=True)
    parser.add_argument("--issue-json", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--wave-file", required=True)
    parser.add_argument("--covered", required=True)
    parser.add_argument("--collection-corpus", required=True)
    parser.add_argument("--proposal-glob", action="append", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--email-env")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run intake and return 0 staged, 1 blocked, or 2 duplicate."""
    args = parse_args(argv)
    email = None
    if args.email_env:
        import os

        email = os.environ.get(args.email_env)
    receipt = run_intake(kind=args.kind, issue_json=args.issue_json, domain=args.domain,
                         wave_file=args.wave_file, covered=args.covered,
                         collection_corpus=args.collection_corpus, proposal_glob=args.proposal_glob,
                         date=args.date, out=args.out, email=email, dry_run=args.dry_run)
    return OUTCOMES[receipt["outcome"]]


if __name__ == "__main__":
    raise SystemExit(main())
