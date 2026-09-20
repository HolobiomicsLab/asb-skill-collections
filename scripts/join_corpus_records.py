#!/usr/bin/env python3
"""Join per-paper build metadata to a tracked domain corpus inventory.

This stage is offline. It does not call ``derive_license_tiers.py`` or
``resolve_paper_license.py``; those network licence derivers run separately.
"""

from __future__ import annotations

if __package__ in (None, ""):
    import os.path as _path
    import sys as _sys

    _sys.path.insert(0, _path.dirname(_path.dirname(_path.abspath(__file__))))

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from scripts import license_tier, release_gate


SCHEMA = "asb-corpus/1.0"
RECEIPT_SCHEMA = "asbb-corpus-join-receipt/1.0"
DEFAULT_ACCESS_MAP = Path(__file__).with_name("access_map_p1.yaml")
SPDX_BY_UNPAYWALL = {
    "cc-by": "CC-BY-4.0",
    "cc-by-nc": "CC-BY-NC-4.0",
    "cc-by-nc-nd": "CC-BY-NC-ND-4.0",
    "public-domain": "CC0-1.0",
}


class JoinFailure(Exception):
    """An invalid or incomplete input prevents the join."""


class JoinConflict(Exception):
    """Ambiguous source evidence or existing output prevents the join."""


def normalize_doi(value: Any) -> str:
    """Return the gate's DOI identity without a query or fragment suffix."""
    identity = release_gate._norm_doi(value)
    return re.split(r"[?#]", identity, maxsplit=1)[0].strip()


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of one input file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    """Read one JSON input and identify its path on failure."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise JoinFailure(f"cannot read JSON {path}: {exc}") from exc


def _read_access_map(path: Path) -> dict[str, Any]:
    """Load and validate the Decision 7 P1 data table."""
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise JoinFailure(f"cannot read access map {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise JoinFailure("access map must be a YAML object")
    allowed = document.get("allowed_types")
    mapping = document.get("mapping")
    if not isinstance(allowed, list) or not all(
        isinstance(item, str) for item in allowed
    ):
        raise JoinFailure("access map allowed_types must be a list of strings")
    if not allowed or not isinstance(mapping, dict):
        raise JoinFailure("access map must contain allowed_types and mapping")
    return {"allowed_types": allowed, "mapping": mapping}


def _choose_rule(rule: Any, selector: str, allowed: set[str]) -> str:
    """Resolve a scalar or conditional access rule to an allowed type."""
    if isinstance(rule, str):
        result = rule
    elif isinstance(rule, dict):
        result = rule.get(selector, rule.get("otherwise"))
    else:
        result = None
    if result not in allowed:
        raise JoinFailure(f"access rule for {selector!r} produced {result!r}")
    return result


def map_access_type(
    raw_status: Any,
    source_reuse: Any,
    spdx: str | None,
    access_map: dict[str, Any],
) -> str:
    """Apply the data-backed Decision 7 P1 access mapping."""
    status = str(raw_status or "unknown").strip().lower() or "unknown"
    mapping = access_map["mapping"]
    rule = mapping.get(status, mapping.get("otherwise"))
    if status == "gold":
        reuse = str(source_reuse or "").strip().lower()
        selector = "permissive" if reuse == "permissive" else "otherwise"
    elif status == "hybrid":
        selector = "cc" if str(spdx or "").upper().startswith("CC-") else "otherwise"
    else:
        selector = status
    return _choose_rule(rule, selector, set(access_map["allowed_types"]))


def _normalize_license(value: Any) -> str | None:
    """Map known Unpaywall tokens to SPDX and preserve explicit SPDX values."""
    raw = str(value or "").strip()
    if not raw:
        return None
    return SPDX_BY_UNPAYWALL.get(raw.lower(), raw)


def _build_directories(root: Path) -> list[Path]:
    """Return visible child directories that contain a build manifest."""
    if not root.is_dir():
        raise JoinFailure(f"build root is not a directory: {root}")
    builds = [
        child
        for child in root.iterdir()
        if child.is_dir()
        and not child.name.startswith((".", "_"))
        and (child / "build_manifest.json").is_file()
    ]
    if not builds:
        raise JoinFailure(f"no visible build directories under {root}")
    return sorted(builds, key=lambda child: child.name)


def _manifest_flags(manifest: dict[str, Any], path: Path) -> dict[str, Any]:
    """Extract resolved invocation flags from a build manifest."""
    flags = (manifest.get("cli_invocation") or {}).get("flags_resolved")
    if not isinstance(flags, dict):
        raise JoinFailure(f"missing cli_invocation.flags_resolved in {path}")
    return flags


def _read_build(path: Path) -> tuple[dict[str, Any], list[Path]]:
    """Read one manifest and its optional external enrichment."""
    manifest_path = path / "build_manifest.json"
    enrichment_path = path / "external_enrichment.json"
    manifest = _read_json(manifest_path)
    enrichment = _read_json(enrichment_path) if enrichment_path.is_file() else {}
    sources = [manifest_path]
    if enrichment_path.is_file():
        sources.append(enrichment_path)
    return {
        "dir": path,
        "flags": _manifest_flags(manifest, manifest_path),
        "enrichment": enrichment,
    }, sources


def _build_doi(build: dict[str, Any]) -> str:
    """Resolve one unambiguous DOI from manifest and enrichment evidence."""
    enrichment = build["enrichment"]
    values = (
        build["flags"].get("doi"),
        (enrichment.get("unpaywall") or {}).get("doi"),
        (enrichment.get("crossref") or {}).get("doi"),
    )
    identities = {normalize_doi(value) for value in values if normalize_doi(value)}
    if len(identities) > 1:
        raise JoinConflict(
            f"DOI disagreement in {build['dir'].name}: {sorted(identities)}"
        )
    if not identities:
        raise JoinFailure(f"no DOI in build {build['dir'].name}")
    return identities.pop()


def _index_tiered(rows: Any) -> dict[str, dict[str, Any]]:
    """Index tier inventory rows and reject duplicate DOI policy evidence."""
    if not isinstance(rows, list):
        raise JoinFailure("tiered corpus JSON must contain a list")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if not isinstance(row, dict):
            continue
        doi = normalize_doi(row.get("doi"))
        if doi:
            grouped[doi].append(row)
    duplicates = sorted(doi for doi, values in grouped.items() if len(values) > 1)
    if duplicates:
        raise JoinConflict(f"tiered inventory has duplicate DOI rows: {duplicates}")
    return {doi: values[0] for doi, values in grouped.items()}


def _github_url(flags: dict[str, Any]) -> str:
    """Normalize the first resolved GitHub repository to an HTTPS URL."""
    repositories = flags.get("github_repo") or []
    if isinstance(repositories, str):
        repositories = [repositories]
    if not repositories:
        return ""
    raw = str(repositories[0]).strip().rstrip("/")
    raw = re.sub(r"^(?:https?://|git@)github\.com[:/]", "", raw, flags=re.I)
    raw = raw.removeprefix("github.com/").removesuffix(".git")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", raw):
        return ""
    return f"https://github.com/{raw}"


def _paper_title(tiered: dict[str, Any], enrichment: dict[str, Any]) -> str:
    """Choose the best tracked or enriched title without inventing one."""
    access = tiered.get("access") or {}
    crossref = enrichment.get("crossref") or {}
    values = (
        access.get("title"),
        tiered.get("title"),
        crossref.get("title"),
        tiered.get("display"),
        tiered.get("name"),
    )
    return next(
        (str(value).strip() for value in values if str(value or "").strip()), ""
    )


def _paper_access(
    tiered: dict[str, Any] | None,
    access_map: dict[str, Any],
    verified_on: str,
) -> tuple[dict[str, Any], str, str | None]:
    """Build access fields plus the paper licence tier and detection."""
    if tiered is None:
        return (
            {
                "type": "link-only",
                "license": None,
                "is_oa": None,
                "oa_status_raw": "unknown",
                "verified_on": verified_on,
            },
            "unknown",
            None,
        )
    source = tiered.get("access") or {}
    spdx = _normalize_license(source.get("license"))
    raw_status = str(source.get("type") or "unknown").strip().lower() or "unknown"
    access_type = map_access_type(
        raw_status, source.get("source_reuse"), spdx, access_map
    )
    access = {
        "type": access_type,
        "license": spdx,
        "is_oa": source.get("is_oa"),
        "oa_status_raw": raw_status,
        "verified_on": verified_on,
    }
    if "source_reuse" in source:
        access["source_reuse"] = source["source_reuse"]
    if access_type != "link-only":
        access["verified_via"] = "unpaywall_oa_locations"
    tier = license_tier.tier_for_license(spdx) if spdx else "unknown"
    return access, tier, "unpaywall"


def _make_paper(
    build: dict[str, Any],
    tiered: dict[str, Any] | None,
    domain: str,
    access_map: dict[str, Any],
    verified_on: str,
) -> dict[str, Any]:
    """Create one asb-corpus/1.0 row from joined source records."""
    access, tier, detection = _paper_access(tiered, access_map, verified_on)
    build_name = build["dir"].name
    return {
        "name": build_name,
        "doi": build["doi"],
        "title": _paper_title(tiered or {}, build["enrichment"]),
        "category": domain,
        "repo_url": _github_url(build["flags"]),
        "status": "included",
        "wave": build_name.split("__", 1)[0],
        "access": access,
        "license_subject": "paper",
        "license_tier": tier,
        "license_detection": detection,
    }


def _deduplicate_builds(
    builds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Select one sorted build per DOI and reject repository disagreement."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for build in builds:
        grouped[build["doi"]].append(build)
    selected: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    for doi, variants in sorted(grouped.items()):
        _check_repositories(doi, variants)
        ordered = sorted(variants, key=lambda item: item["dir"].name)
        selected.append(ordered[0])
        if len(ordered) > 1:
            duplicates.append(
                {
                    "doi": doi,
                    "selected": ordered[0]["dir"].name,
                    "builds": [item["dir"].name for item in ordered],
                }
            )
    return selected, duplicates


def _check_repositories(doi: str, builds: list[dict[str, Any]]) -> None:
    """Reject conflicting known repository identities for one DOI."""
    repositories = {
        repository.casefold()
        for item in builds
        if (repository := _github_url(item["flags"]))
    }
    if len(repositories) > 1:
        raise JoinConflict(
            f"duplicate DOI {doi} has conflicting repositories: {sorted(repositories)}"
        )


def _capped_rows(papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """List rows covered by the Decision 7 P2/P3 quotation cap."""
    result = []
    for paper in papers:
        access = paper["access"]
        reasons = []
        if access["type"] == "link-only":
            reasons.append("access.type=link-only")
        if access.get("source_reuse") != "permissive":
            reasons.append("source_reuse!=permissive")
        if reasons:
            result.append({"doi": paper["doi"], "reasons": reasons})
    return result


def _counter(values: Any) -> dict[str, int]:
    """Return a sorted, JSON-ready frequency table."""
    return dict(sorted(Counter(values).items()))


def _make_receipt(
    domain: str,
    access_map: dict[str, Any],
    input_digests: dict[str, str],
    build_count: int,
    papers: list[dict[str, Any]],
    duplicates: list[dict[str, Any]],
    unmatched: list[dict[str, str]],
) -> dict[str, Any]:
    """Create the minimal deterministic S4 receipt."""
    caps = _capped_rows(papers)
    counts = {
        "builds": build_count,
        "unique_dois": len(papers),
        "access.type": _counter(paper["access"]["type"] for paper in papers),
        "license_tier": _counter(paper["license_tier"] for paper in papers),
        "oa_status_raw": _counter(paper["access"]["oa_status_raw"] for paper in papers),
        "unmatched": len(unmatched),
        "capped": len(caps),
    }
    return {
        "schema": RECEIPT_SCHEMA,
        "stage": "S4",
        "domain": domain,
        "inputs": dict(sorted(input_digests.items())),
        "access_map": access_map["mapping"],
        "counts": counts,
        "duplicate_dois": duplicates,
        "unmatched_rows": unmatched,
        "capped_rows": caps,
    }


def _version_number(value: str) -> int:
    """Parse the required v<N> collection version spelling."""
    match = re.fullmatch(r"v([1-9][0-9]*)", value)
    if not match:
        raise JoinFailure(f"version must have the form v<N>: {value!r}")
    return int(match.group(1))


def _verified_date(value: str) -> str:
    """Validate a caller-supplied canonical calendar date."""
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise JoinFailure(f"verified-on must be YYYY-MM-DD: {value!r}") from exc
    if parsed != value:
        raise JoinFailure(f"verified-on must be canonical: {value!r}")
    return parsed


def _yaml_bytes(value: Any) -> bytes:
    """Serialize deterministic, readable Unicode YAML."""
    return yaml.safe_dump(
        value, sort_keys=False, allow_unicode=True, width=1000
    ).encode()


def _json_bytes(value: Any) -> bytes:
    """Serialize deterministic, readable Unicode JSON."""
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode()


def _output_state(path: Path, expected: bytes) -> str:
    """Classify a planned output as create, identical, or conflict."""
    if not path.exists() and not path.is_symlink():
        return "create"
    if path.is_symlink() or not path.is_file():
        return "conflict"
    return "identical" if path.read_bytes() == expected else "conflict"


def _preflight_parent_chain(path: Path) -> None:
    """Reject symlink or non-directory components before any output write."""
    for parent in path.parents:
        if parent.is_symlink():
            raise JoinConflict(f"output parent is a symlink: {parent}")
        if parent.exists() and not parent.is_dir():
            raise JoinConflict(f"output parent is not a directory: {parent}")


def _write_outputs(outputs: dict[Path, bytes], dry_run: bool) -> dict[str, str]:
    """Preflight every target, then create only absent identical-safe outputs."""
    for path in outputs:
        _preflight_parent_chain(path)
    states = {path: _output_state(path, content) for path, content in outputs.items()}
    conflicts = [str(path) for path, state in states.items() if state == "conflict"]
    if conflicts:
        raise JoinConflict(f"existing output differs: {', '.join(conflicts)}")
    if not dry_run:
        for path, content in outputs.items():
            if states[path] == "create":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    return {str(path): state for path, state in states.items()}


def _prepare(
    arguments: argparse.Namespace,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    """Load, validate, and join all inputs without writing outputs."""
    builds_root = arguments.builds.resolve()
    tiered_path = arguments.tiered.resolve()
    access_map_path = arguments.access_map.resolve()
    access_map = _read_access_map(access_map_path)
    tier_index = _index_tiered(_read_json(tiered_path))
    input_digests = {
        "access_map": _sha256_file(access_map_path),
        "tiered": _sha256_file(tiered_path),
    }
    loaded = []
    for build_dir in _build_directories(builds_root):
        build, sources = _read_build(build_dir)
        build["doi"] = _build_doi(build)
        loaded.append(build)
        for source in sources:
            logical = f"builds/{build_dir.name}/{source.name}"
            input_digests[logical] = _sha256_file(source)
    selected, duplicates = _deduplicate_builds(loaded)
    unmatched = [
        {"build": build["dir"].name, "doi": build["doi"]}
        for build in selected
        if build["doi"] not in tier_index
    ]
    papers = [
        _make_paper(
            build,
            tier_index.get(build["doi"]),
            arguments.domain,
            access_map,
            _verified_date(arguments.verified_on),
        )
        for build in selected
    ]
    papers.sort(key=lambda paper: paper["doi"])
    corpus = {
        "schema": SCHEMA,
        "collection": arguments.domain,
        "version": _version_number(arguments.version),
        "summary": {"total": len(papers), "included": len(papers), "hold": 0},
        "papers": papers,
    }
    receipt = _make_receipt(
        arguments.domain,
        access_map,
        input_digests,
        len(loaded),
        papers,
        duplicates,
        unmatched,
    )
    output = arguments.out.absolute()
    receipt_root = arguments.receipts or output.parent / "receipts"
    return corpus, receipt, output, receipt_root.absolute() / "corpus_join_receipt.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the S4 corpus-join command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--builds", type=Path, required=True)
    parser.add_argument("--tiered", type=Path, required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verified-on", required=True)
    parser.add_argument("--access-map", type=Path, default=DEFAULT_ACCESS_MAP)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the join; return 0 for success, 1 for failure, or 2 for conflict."""
    arguments = parse_args(argv)
    try:
        corpus, receipt, output, receipt_path = _prepare(arguments)
        states = _write_outputs(
            {output: _yaml_bytes(corpus), receipt_path: _json_bytes(receipt)},
            arguments.dry_run,
        )
    except JoinConflict as exc:
        print(f"CONFLICT: {exc}", file=sys.stderr)
        return 2
    except (JoinFailure, OSError, TypeError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "dry-run" if arguments.dry_run else "ok",
                "outputs": states,
                "summary": corpus["summary"],
                "receipt": str(receipt_path),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
