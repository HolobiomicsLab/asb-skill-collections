#!/usr/bin/env python3
"""Build and stamp the three release indexes for one collected candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# ``python scripts/bootstrap_indexes.py`` puts only scripts/ on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import propagate_license_tiers, release_gate, router_shape, skill_index
from scripts import stamp_provenance, stamp_skill_license


INDEX_NAMES = ("skills_index.json", "kb_bundle.json", "tools_index.json")
HELPER_ORDER = (
    "propagate_license_tiers",
    "stamp_skill_license",
    "backfill_tool_license",
    "propagate_provenance_tiers",
    "stamp_provenance",
    "router_shape",
)
TRIAGE_FIELDS = ("triage_status", "yes_rate", "n_claims")


class BootstrapError(RuntimeError):
    """An invalid input prevents a deterministic bootstrap."""


class ConflictError(BootstrapError):
    """An existing output is not owned by this exact bootstrap run."""


@dataclass
class IndexPlan:
    """All deterministic pre-helper index payloads for one candidate."""

    skills: list[dict[str, Any]]
    provisional_skills: list[dict[str, Any]]
    kb_bundle: dict[str, Any]
    tools: list[dict[str, Any]]
    unmatched_tool_names: list[str]


def _json_bytes(value: Any) -> bytes:
    """Render deterministic readable JSON."""
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def _sha256_bytes(value: bytes) -> str:
    """Return a hexadecimal SHA-256 digest."""
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    """Hash a required regular file."""
    if not path.is_file() or path.is_symlink():
        raise BootstrapError(f"required regular file is missing: {path}")
    return _sha256_bytes(path.read_bytes())


def _file_hashes(root: Path) -> dict[str, str]:
    """Hash a regular candidate tree and reject symlinked content."""
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ConflictError(f"candidate contains a symlink: {path}")
        if path.is_file():
            hashes[path.relative_to(root).as_posix()] = _sha256_file(path)
    return hashes


def _normal_doi(value: object) -> str:
    """Normalize DOI identity consistently with the release gate."""
    normalized = release_gate._norm_doi(value)
    return normalized.split("#", 1)[0].split("?", 1)[0].strip()


def _stable_dois(values: list[object]) -> list[str]:
    """Normalize and de-duplicate DOI values without reordering them."""
    result: list[str] = []
    for value in values:
        normalized = _normal_doi(value)
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def _source_dois(frontmatter: dict[str, Any]) -> list[str]:
    """Read source-paper DOIs first, then legacy ``derived_from`` DOIs."""
    provenance = frontmatter.get("provenance") or {}
    papers = provenance.get("source_papers") or []
    values: list[object] = [
        paper.get("doi")
        for paper in papers
        if isinstance(paper, dict) and paper.get("doi")
    ]
    for source in frontmatter.get("derived_from") or []:
        value = source.get("doi") if isinstance(source, dict) else source
        if value:
            values.append(value)
    return _stable_dois(values)


def _tool_dois(record: dict[str, Any]) -> list[str]:
    """Read a tool record's paper DOIs from ``derived_from``."""
    values = [
        source.get("doi")
        for source in record.get("derived_from") or []
        if isinstance(source, dict) and source.get("doi")
    ]
    return _stable_dois(values)


def _load_tool_records(candidate: Path) -> list[dict[str, Any]]:
    """Load and validate every candidate tool record in slug order."""
    records: list[dict[str, Any]] = []
    for path in sorted((candidate / "tools").glob("*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise BootstrapError(f"tool record is not a mapping: {path}")
        if record.get("slug") != path.stem or not record.get("name"):
            raise BootstrapError(f"tool record slug/name mismatch: {path}")
        records.append(record)
    return records


def _name_to_tool_slugs(
    records: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Map exact recorded tool names to their catalogue slugs."""
    result: defaultdict[str, list[str]] = defaultdict(list)
    for record in records:
        result[str(record["name"])].append(str(record["slug"]))
    return {name: sorted(slugs) for name, slugs in result.items()}


def _skill_payloads(
    candidate: Path, name_to_slugs: dict[str, list[str]]
) -> tuple[list, list, dict, dict, set[str]]:
    """Build skill, provisional, KB and reciprocal-use payloads."""
    skills, provisional, bundle_skills = [], [], {}
    users: defaultdict[str, list[str]] = defaultdict(list)
    unmatched: set[str] = set()
    for slug, frontmatter in sorted(skill_index.indexable_skills(candidate).items()):
        entry = skill_index.entry_from_frontmatter(slug, frontmatter)
        entry["dois"] = _source_dois(frontmatter)
        old_entry = dict(entry)
        old_entry["license_tier"] = "unknown"
        provisional.append(old_entry)
        names = [str(name) for name in entry["tools"]]
        entry["tools_used"] = sorted(
            {tool_slug for name in names for tool_slug in name_to_slugs.get(name, [])}
        )
        unmatched.update(name for name in names if name not in name_to_slugs)
        entry.update({field: frontmatter.get(field) for field in TRIAGE_FIELDS})
        skills.append(entry)
        bundle = skill_index.kb_entry_from_frontmatter(frontmatter)
        bundle.update(
            dois=entry["dois"],
            kb_slugs=[skill_index.kb_slug_for_doi(doi) for doi in entry["dois"]],
            tools_used=entry["tools_used"],
        )
        bundle_skills[slug] = bundle
        for tool_slug in entry["tools_used"]:
            users[tool_slug].append(slug)
    return skills, provisional, bundle_skills, users, unmatched


def _tool_payloads(
    records: list[dict[str, Any]], users: dict[str, list[str]]
) -> list[dict[str, Any]]:
    """Build exact release tool-index rows with reciprocal skill links."""
    return [
        {
            "slug": record["slug"],
            "name": record["name"],
            "edam_topics": record.get("edam_topics") or [],
            "dois": _tool_dois(record),
            "techniques": [],
            "license_tier": "unknown",
            "license": None,
            "license_detection": None,
            "license_subject": None,
            "repo_url": record.get("repo_url"),
            "used_by_skills": sorted(users.get(record["slug"], [])),
        }
        for record in records
    ]


def _build_plan(candidate: Path) -> IndexPlan:
    """Construct all index payloads solely from candidate-owned records."""
    records = _load_tool_records(candidate)
    skills, provisional, bundle_skills, users, unmatched = _skill_payloads(
        candidate, _name_to_tool_slugs(records)
    )
    if not skills:
        raise BootstrapError("cannot bootstrap an empty leaf collection")
    descriptor = yaml.safe_load(
        (candidate / "collection.yaml").read_text(encoding="utf-8")
    )
    if not isinstance(descriptor, dict):
        raise BootstrapError("collection.yaml is not a mapping")
    bundle = {
        "collection": descriptor["slug"],
        "version": descriptor["version"],
        "kb_prefix": skill_index.DEFAULT_KB_PREFIX,
        "distinct_dois": sorted({doi for row in skills for doi in row["dois"]}),
        "skills": bundle_skills,
    }
    return IndexPlan(
        skills,
        provisional,
        bundle,
        _tool_payloads(records, users),
        sorted(unmatched),
    )


def _load_json(path: Path) -> Any:
    """Load one required JSON document with a contextual error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"invalid JSON in {path}: {exc}") from exc


def _validate_provisional_indexes(candidate: Path, plan: IndexPlan) -> None:
    """Allow only the collector's provisional index before first bootstrap."""
    skills_path = candidate / "skills_index.json"
    if not skills_path.is_file() or skills_path.is_symlink():
        raise ConflictError("collector provisional skills_index.json is missing")
    if _load_json(skills_path) != plan.provisional_skills:
        raise ConflictError("skills_index.json is not the collector provisional index")
    for name in INDEX_NAMES[1:]:
        if (candidate / name).exists():
            raise ConflictError(
                f"existing non-provisional index output differs: {name}"
            )


def _write_base_indexes(staged: Path, plan: IndexPlan) -> None:
    """Write the three pre-helper indexes to an isolated candidate copy."""
    payloads = {
        "skills_index.json": plan.skills,
        "kb_bundle.json": plan.kb_bundle,
        "tools_index.json": plan.tools,
    }
    for name, payload in payloads.items():
        (staged / name).write_bytes(_json_bytes(payload))


def _run_helpers(staged: Path, corpus: Path) -> dict[str, Any]:
    """Apply the six canonical helper operations in their required order."""
    index_path = staged / "skills_index.json"
    bundle_path = staged / "kb_bundle.json"
    tiers = propagate_license_tiers.corpus_tier_by_doi(corpus)
    declared = propagate_license_tiers.declared_tiers(staged)
    summaries: dict[str, Any] = {}
    summaries["propagate_license_tiers"] = propagate_license_tiers.propagate_indices(
        index_path, bundle_path, tiers, declared
    )
    summaries["stamp_skill_license"] = stamp_skill_license.stamp_all(staged, index_path)
    summaries["backfill_tool_license"] = propagate_license_tiers.backfill_tool_license(
        staged, corpus_path=corpus, index_path=index_path
    )
    if summaries["backfill_tool_license"]["skipped"]:
        raise BootstrapError(
            "licence block backfill could not resolve: "
            f"{summaries['backfill_tool_license']['skipped']}"
        )
    summaries["propagate_provenance_tiers"] = stamp_provenance.propagate_indices(
        index_path, bundle_path, stamp_provenance.repo_urls(staged)
    )
    summaries["stamp_provenance"] = stamp_provenance.stamp_all(staged, index_path)
    shape = router_shape.shape(staged, index_path, set())
    summaries["router_shape"] = {
        key: value for key, value in shape.items() if key != "unit"
    }
    return summaries


def _sync_stage(candidate: Path, staged: Path, before: dict[str, str]) -> None:
    """Copy only staged additions and changes after a concurrency check."""
    if _file_hashes(candidate) != before:
        raise ConflictError("candidate changed during bootstrap")
    after = _file_hashes(staged)
    removed = set(before) - set(after)
    if removed:
        raise BootstrapError(f"bootstrap unexpectedly removed files: {sorted(removed)}")
    for relative, digest in after.items():
        if before.get(relative) == digest:
            continue
        destination = candidate / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((staged / relative).read_bytes())


def _receipt_path(candidate: Path, receipts: Path | None) -> Path:
    """Resolve the optional receipt root outside the candidate tree."""
    root = receipts or candidate.parent / "receipts"
    root = Path(os.path.abspath(root))
    try:
        root.relative_to(candidate)
    except ValueError:
        return root / "bootstrap_receipt.json"
    raise BootstrapError("receipts directory must not be inside the candidate")


def _preflight_receipt_path(receipt_path: Path) -> None:
    """Reject unsafe receipt targets before any candidate mutation."""
    if receipt_path.is_symlink():
        raise ConflictError(f"receipt target is a symlink: {receipt_path}")
    if receipt_path.exists() and not receipt_path.is_file():
        raise ConflictError(f"receipt target is not a regular file: {receipt_path}")
    for parent in receipt_path.parents:
        if parent.is_symlink():
            raise ConflictError(f"receipt parent is a symlink: {parent}")
        if parent.exists() and not parent.is_dir():
            raise ConflictError(f"receipt parent is not a directory: {parent}")


def _completed_receipt(
    candidate: Path, corpus: Path, receipt_path: Path
) -> dict[str, Any] | None:
    """Validate and return an existing completed receipt, if present."""
    if not receipt_path.exists():
        return None
    receipt = _load_json(receipt_path)
    if not isinstance(receipt, dict) or receipt.get("stage") != "S5-bootstrap":
        raise ConflictError(f"existing bootstrap receipt differs: {receipt_path}")
    if receipt.get("corpus_sha256") != _sha256_file(corpus):
        raise ConflictError("corpus changed since bootstrap")
    if receipt.get("output_sha256") != _file_hashes(candidate):
        raise ConflictError("candidate changed since bootstrap")
    return receipt


def _build_receipt(
    plan: IndexPlan,
    summaries: dict[str, Any],
    corpus: Path,
    staged: Path,
    provisional_hash: str,
) -> dict[str, Any]:
    """Create the deterministic S5 bootstrap receipt."""
    final_skills = _load_json(staged / "skills_index.json")
    return {
        "stage": "S5-bootstrap",
        "counts": {
            "skills": len(final_skills),
            "tools": len(plan.tools),
            "dois": len(plan.kb_bundle["distinct_dois"]),
        },
        "helpers": summaries,
        "unmatched_leaf_tool_names": plan.unmatched_tool_names,
        "provisional_skills_index_sha256_before": provisional_hash,
        "skills_index_sha256_after": _sha256_file(staged / "skills_index.json"),
        "corpus_sha256": _sha256_file(corpus),
        "output_sha256": _file_hashes(staged),
    }


def _dry_run_payload(plan: IndexPlan) -> dict[str, Any]:
    """Describe a bootstrap without invoking mutating helpers."""
    return {
        "stage": "S5-bootstrap",
        "dry_run": True,
        "indexes": sorted(INDEX_NAMES),
        "counts": {
            "skills": len(plan.skills),
            "tools": len(plan.tools),
            "dois": len(plan.kb_bundle["distinct_dois"]),
        },
        "helper_order": list(HELPER_ORDER),
        "unmatched_leaf_tool_names": plan.unmatched_tool_names,
    }


def _parser() -> argparse.ArgumentParser:
    """Build the public S5 bootstrap argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _run(options: argparse.Namespace) -> int:
    """Execute one validated bootstrap invocation."""
    candidate = Path(os.path.abspath(options.candidate))
    corpus = Path(os.path.abspath(options.corpus))
    if not candidate.is_dir() or candidate.is_symlink() or not corpus.is_file():
        raise BootstrapError("candidate directory and corpus file must exist")
    receipt_path = _receipt_path(candidate, options.receipts)
    _preflight_receipt_path(receipt_path)
    completed = _completed_receipt(candidate, corpus, receipt_path)
    if completed is not None:
        print(json.dumps({"stage": "S5-bootstrap", "status": "identical"}))
        return 0
    plan = _build_plan(candidate)
    _validate_provisional_indexes(candidate, plan)
    if options.dry_run:
        print(json.dumps(_dry_run_payload(plan), sort_keys=True))
        return 0
    before = _file_hashes(candidate)
    provisional_hash = _sha256_file(candidate / "skills_index.json")
    with tempfile.TemporaryDirectory(prefix="asb-bootstrap-") as temporary:
        staged = Path(temporary) / "candidate"
        shutil.copytree(candidate, staged)
        _write_base_indexes(staged, plan)
        summaries = _run_helpers(staged, corpus)
        receipt = _build_receipt(plan, summaries, corpus, staged, provisional_hash)
        _preflight_receipt_path(receipt_path)
        if receipt_path.exists():
            raise ConflictError(f"existing bootstrap receipt differs: {receipt_path}")
        _sync_stage(candidate, staged, before)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(_json_bytes(receipt))
    print(json.dumps({"stage": "S5-bootstrap", "counts": receipt["counts"]}))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic index bootstrap with the 0/1/2 stage contract."""
    try:
        return _run(_parser().parse_args(argv))
    except ConflictError as exc:
        print(f"CONFLICT: {exc}", file=sys.stderr)
        return 2
    except (
        BootstrapError,
        OSError,
        UnicodeError,
        ValueError,
        KeyError,
        TypeError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
