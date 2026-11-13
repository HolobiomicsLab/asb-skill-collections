#!/usr/bin/env python3
"""Pack and screen local ASB build capsules without depositing or uploading."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import capsule_screen, zenodo_deposit
try:
    from scripts.promote_benchmark_layer import _CAPSULE_KEEP
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from promote_benchmark_layer import _CAPSULE_KEEP
from scripts.release_capsule_truth import crate_problems, slug_from_build
from scripts.release_gate import _build_email_allowlist

BUILD_FILES = ("build_manifest.json", "workflow.yaml", "validation_assertions.jsonld")
INDICIUM_FILE = "indicium.jsonld"
# Build provenance shipped when the source build holds it; absence is not a failure.
BUILD_OPTIONAL_FILES = (
    "run_summary.md", "validation_summary.md", "build_fidelity.json", "workflow_score.json",
    "reproducibility_score.json", "certification_report.json", "external_enrichment.json",
    "repo_relationship.json", "data_accessions.json", "deps.lock", "package_index.json",
    "entity_spine.json", "anchor_corpus/manifest.json", "anchor_corpus/anchor_results.json",
)
BUILD_OPTIONAL_DIRS = ("cards", "astra", "exports", "certification")
# Anchor corpus text: the article text, the tool repository's README and API surface,
# and the enrichment documents. Shipped only when the paper's text is kept in full.
ANCHOR_TEXT_FILES = ("anchor_corpus/article.txt", "anchor_corpus/repo.txt", "anchor_corpus/enrichment_docs.txt")
ANCHOR_RECIPE = "anchor_recipe.json"
ANCHOR_RECIPE_STATEMENT = (
    "Existing builds did not pin the repository commit, so a rebuilt corpus is verifiable "
    "by hash but not guaranteed identical."
)
# Keys naming the machine a report ran on; removed like the Git branch of a manifest.
MACHINE_IDENTITY_KEYS = {"host", "hostname"}
CAPSULE_FILES = ("eval.json", "validation.json")
CAPSULE_OPTIONAL_FILES = ("resolved_inputs.json", "resources.json", "task_card.json", "task_card.md",
                          "metadata.json", "rubric.json")
CAPSULE_OPTIONAL_DIRS = ("scripts", "tables", "figures", "outputs", "nanopubs")
# Capsule folders whose files are extracted from the paper; their index.json is generated.
PAPER_DERIVED_DIRS = ("figures", "tables")
PAPER_DERIVED_INDEX = "index.json"
WITHHELD_INDEX = "withheld_files.json"
WITHHELD_NOTE = (
    "Files extracted from the paper are withheld because the paper's licence does not allow "
    "sharing its text verbatim; each entry gives the file's name, sha256 and size."
)
SHARD_SIZE = 40
# Zenodo accepts 100 files per record; the shards and the browsable receipts stay under this.
ZENODO_FILE_BUDGET = 90
ZENODO_MAX_BYTES = 50 * 10**9
ZENODO_RECEIPTS = ("README.md", "MANIFEST.json", "capsules.jsonl", "SCREEN.json", "benchmark-manifest.json")
HF_CONFIGS = (
    ("capsules", "capsules.jsonl", "every capsule row", None),
    ("validated_plus", "validated_plus.jsonl", "capsules whose readiness is validated, evaluable or executable",
     {"validated", "evaluable", "executable"}),
    ("evaluable_plus", "evaluable_plus.jsonl", "capsules whose readiness is evaluable or executable",
     {"evaluable", "executable"}),
    ("benchmark", "benchmark.jsonl", "the rows of benchmark-manifest.json", None),
)
READINESS_LEVELS = ("documented", "validated", "evaluable", "executable")
READINESS_STATEMENT = (
    "Readiness is computed from fields of each row. documented: validation present. validated: "
    "validation clean or strict, evaluation partial. evaluable: validation clean or strict, evaluation "
    "complete. executable: evaluable, every input of eval.json carries a sha256 and a download hint "
    "(at least one input), and the task card's reproducibility tier is certified. No capsule has been "
    "executed under a workflow engine: the task cards sampled on 13 November 2026 are type-checked or "
    "manual-only, none certified. "
    "Readiness is not the maturity scale: every capsule here is at most Iron (a documented task with "
    "structural checks), no reference solution or execution ships, and Bronze, Silver and Gold are "
    "assigned only through the maturity criteria and their records, Gold requiring expert review. "
    "Expert review is a separate axis, still being designed, and is not part of readiness."
)
EVAL_KEYS = {"task_id", "inputs", "expected_outputs", "checks"}
PIPELINE_NAME = "AgenticScienceBuilder"
# The pipeline repository is private: linked only with --pipeline-public.
PIPELINE_URL = f"https://github.com/HolobiomicsLab/{PIPELINE_NAME}"
# Citation keys that may point at a private domain repository.
PRIVATE_CITATION_KEYS = ("url", "repository-code")
REGISTRY = Path(__file__).resolve().parent.parent / "collections.yaml"
TOOLING_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"
ARTIFACT_MEMBERSHIP_FIELD = "included_in_capsule"
ARTIFACT_MEMBERSHIP_NOTE = (
    f"`{ARTIFACT_MEMBERSHIP_FIELD}` marks paths present in this shipped capsule; "
    "false entries name full-build files absent from this record."
)
VALIDATION_COUNT_KEYS = ("checked", "supported", "partial", "unsupported", "drift")
VALIDATION_STATE_ORDER = {"present": 0, "clean": 1, "strict": 2}
EVALUATION_LISTING_STATEMENT = (
    "This listing identifies capsules whose evaluation definition is structurally complete; "
    "it does not promise that they are runnable, their inputs are retrievable, or their checks are machine-scorable."
)
CAPSULE_FIELD_DEFINITIONS = {
    "access_class": ("category", "Source-paper access class used by the quotation screen."),
    "build_slug": ("identifier", "Build archive stem; its payload is builds/<build_slug>.zip."),

    "member": ("path", "Path of the build archive inside its shard, and under hf/ in the per-build layout."),
    "readiness": ("documented, validated, evaluable or executable", "Readiness computed from validation_state, eval_state, input readiness and reproducibility_tier; not the maturity scale. See the readiness rule."),
    "reproducibility_tier": ("tier or null", "reproducibility_tier of the capsule's task_card.json; null when absent."),
    "shard": ("file name", "Zenodo shard archive that holds the build archive."),
    "capsule_id": ("identifier", "Capsule directory name inside the build archive."),
    "claims": ("object", "Validation counts, separated by their source."),
    "claims.declared_summary": ("object", "Counts declared by validation.json summary."),
    "claims.declared_summary.checked": ("claims", "Claims the summary declares checked."),
    "claims.declared_summary.drift": ("claims", "Claims the summary declares affected by drift."),
    "claims.declared_summary.partial": ("claims", "Claims the summary declares partially supported."),
    "claims.declared_summary.supported": ("claims", "Claims the summary declares supported."),
    "claims.declared_summary.unsupported": ("claims", "Claims the summary declares unsupported."),
    "claims.from_entries": ("object or null", "Counts derived from claims_checked; null when that list is absent."),
    "claims.from_entries.checked": ("claims", "Claim entries checked, including unknown support values."),
    "claims.from_entries.drift": ("claims", "Claim entries explicitly recording drift."),
    "claims.from_entries.partial": ("claims", "Claim entries whose supported value is partial."),
    "claims.from_entries.supported": ("claims", "Claim entries whose supported value is yes."),
    "claims.from_entries.unknown": ("claims", "Claim entries with any other supported value."),
    "claims.from_entries.unsupported": ("claims", "Claim entries whose supported value is no."),
    "eval_checks": ("checks", "Number of checks in eval.json."),
    "eval_checks_by_kind": ("mapping of kind to checks", "Checks grouped by their kind; unknown means no usable kind."),
    "eval_input_assets": ("assets", "Input entries in eval.json."),
    "eval_input_assets_with_download_hint": ("assets", "Input entries with a non-empty download_hint."),
    "eval_input_assets_with_hash": ("assets", "Input entries with a non-empty sha256."),
    "eval_state": ("state", "complete means structurally complete; partial lacks a required structural element; invalid is unreadable JSON."),
    "eval_unresolved_references": ("references", "Entries in eval.json unresolved_references."),
    "license": ("licence identifier or null", "Licence of the source paper, not of the tools or generated metadata."),
    "paper_doi": ("DOI", "DOI of the source paper."),
    "quotes_after_screen": ("object", "Text of the paper in this capsule after the screen, measured on the output."),
    "quotes_after_screen.characters": ("characters", "Characters of paper text the capsule holds."),
    "quotes_after_screen.count": ("fields", "Fields that hold paper text."),
    "quotes_after_screen.dropped": ("fields", "Fields whose paper text was removed."),
    "quotes_after_screen.longest": ("characters", "Longest field of paper text held."),
    "quotes_after_screen.truncated": ("fields", "Fields whose paper text was shortened to the cap."),
    "task_id": ("identifier or null", "Evaluation task identifier."),
    "validation_state": ("state", "present has validation; clean has checked claims with no unsupported claim or drift; strict has only supported checked claims; invalid is unreadable or malformed."),
    "validation_summary_consistent": ("boolean", "True means claims_checked and the declared summary agree, or claims_checked is absent; false means they disagree."),
}
BENCHMARK_FIELD_DEFINITIONS = CAPSULE_FIELD_DEFINITIONS
SCREEN_COUNTER_DEFINITIONS = {
    "crates_pruned": "RO-Crates reduced to members shipped in the capsule",
    "deny_hits": "matches of content withheld by the maintainers; a build with one is left out",
    "emails_redacted": "email addresses redacted",
    "failures": "screen failures",
    "paper_files_withheld": "figure or table files extracted from a paper whose licence does not allow verbatim sharing, replaced by an index entry",
    "overlap_characters_trimmed": "characters of those runs",
    "overlap_runs_trimmed": "runs of at least 160 characters copied from the article of a paper whose text is not kept in full, cut from strings outside the quotation fields and replaced by a marker and an anchor",
    "paths_rewritten": "machine paths replaced with portable locators",
    "phones_redacted": "telephone numbers redacted",
    "private_urls_rewritten": "private repository URLs reduced to unlinked names",
    "spans_dropped": "quotation spans dropped",
    "spans_dropped_by_access_class": "quotation spans dropped because of source access class",
    "spans_truncated": "quotation spans truncated",
}


def write_json(path: Path, value) -> None:
    """Write stable, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    """Stream a file SHA-256 digest."""
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def normalize_doi(value) -> str | None:
    """Normalize a DOI for corpus and access-record joins."""
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        value = value.removeprefix(prefix)
    return value or None


def discover_builds(view: Path, limit: int | None) -> list[Path]:
    """Return immediate build directories or paper-view symlinks in sorted order."""
    builds = [entry for entry in sorted(view.iterdir()) if entry.is_dir() and (entry / "build_manifest.json").is_file()]
    return builds[:limit] if limit is not None else builds


def load_access_records(path: Path | None) -> dict[str, dict]:
    """Index same-DOI access overrides without depending on registry paths."""
    if path is None:
        return {}
    records = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(records, dict):
        records = records.get("papers") or records.get("records") or []
    return {normalize_doi(row.get("doi")): row for row in records if normalize_doi(row.get("doi"))}


def resolve_paper(build_name: str, corpus: dict, overrides: dict) -> dict:
    """Join released corpus metadata first, then apply a same-DOI override."""
    papers = {paper.get("name"): paper for paper in corpus.get("papers") or []}
    paper = dict(papers.get(build_name) or {})
    doi = normalize_doi(paper.get("doi"))
    access = dict(paper.get("access") or {})
    source = "released_corpus" if access else "unmatched"
    override = overrides.get(doi)
    if override:
        access = dict(override.get("access") or access)
        source = "access_override"
    return {"doi": doi, "access": access, "access_source": source, "matched": bool(paper)}


def copy_selected(source: Path, destination: Path, relative: str) -> bool:
    """Copy one regular file into the staged build."""
    origin = source / relative
    if not origin.is_file():
        return False
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origin, target)
    return True


def project_build_manifest(manifest: dict) -> dict:
    """Remove local-state fields recursively from the manifest's Git entry."""
    def project(value):
        if isinstance(value, dict):
            return {
                key: project(item)
                for key, item in value.items()
                if key not in {"branch", "is_dirty"}
            }
        if isinstance(value, list):
            return [project(item) for item in value]
        return value

    projected = dict(manifest)
    if "git" in projected:
        projected["git"] = project(projected["git"])
    return projected


def mark_artifact_membership(capsule: Path) -> None:
    """Mark each artifact path against the staged capsule's shipped files."""
    path = capsule / "artifact_provenance.json"
    if not path.is_file():
        return
    try:
        manifest = read_json(path)
    except (ValueError, TypeError):
        return  # unreadable: the screen reports it
    members = {
        member.relative_to(capsule).as_posix()
        for member in capsule.rglob("*")
        if member.is_file()
    }
    artifacts = manifest.get("artifacts", []) if isinstance(manifest, dict) else None
    if not isinstance(artifacts, list) or any(not isinstance(entry, dict) for entry in artifacts):
        return  # another shape: left as written, nothing is claimed about it
    for entry in artifacts:
        target = entry.get("path")
        entry[ARTIFACT_MEMBERSHIP_FIELD] = (
            isinstance(target, str) and target.split("#", 1)[0] in members
        )
    manifest["artifact_membership_note"] = ARTIFACT_MEMBERSHIP_NOTE
    write_json(path, manifest)


def tree_files(root: Path) -> list[str]:
    """Return the regular files below a directory, relative to it, in sorted order."""
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def select_members(source: Path, with_indicium: bool, ship_anchor_text: bool) -> tuple[list[str], list[str]]:
    """Return the source files a build archive takes, relative to the build, and the
    required members the source lacks. Staging and the input receipt share this list."""
    selected, missing = [], []
    for name in BUILD_FILES + ((INDICIUM_FILE,) if with_indicium else ()):
        (selected if (source / name).is_file() else missing).append(name)
    if (source / "ledger").is_dir():
        selected += [f"ledger/{name}" for name in tree_files(source / "ledger")]
    else:
        missing.append("ledger/")
    optional = BUILD_OPTIONAL_FILES + (ANCHOR_TEXT_FILES if ship_anchor_text else ())
    selected += [name for name in optional if (source / name).is_file()]
    for directory in BUILD_OPTIONAL_DIRS:
        if (source / directory).is_dir():
            selected += [f"{directory}/{name}" for name in tree_files(source / directory)]
    for capsule in sorted(path for path in (source / "capsules").iterdir() if path.is_dir()):
        prefix = f"capsules/{capsule.name}"
        for name in list(_CAPSULE_KEEP) + list(CAPSULE_OPTIONAL_DIRS):
            if (capsule / name).is_dir():
                selected += [f"{prefix}/{name}/{inner}" for inner in tree_files(capsule / name)]
            elif (capsule / name).is_file():
                selected.append(f"{prefix}/{name}")
            elif name in _CAPSULE_KEEP:
                missing.append(f"{prefix}/{name}")
        for name in CAPSULE_FILES:
            (selected if (capsule / name).is_file() else missing).append(f"{prefix}/{name}")
        selected += [f"{prefix}/{name}" for name in CAPSULE_OPTIONAL_FILES if (capsule / name).is_file()]
    return sorted(set(selected)), missing


def drop_keys(value, names: set[str]):
    """Remove the named keys at any depth of a parsed document."""
    if isinstance(value, dict):
        return {key: drop_keys(item, names) for key, item in value.items() if key not in names}
    if isinstance(value, list):
        return [drop_keys(item, names) for item in value]
    return value


def project_machine_identity(destination: Path) -> None:
    """Remove the host name from the certification reports of a staged build."""
    reports = [destination / "certification_report.json"]
    if (destination / "certification").is_dir():
        reports += sorted((destination / "certification").rglob("*.json"))
    for path in reports:
        if not path.is_file():
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue  # unreadable: the screen reports it
        projected = drop_keys(value, MACHINE_IDENTITY_KEYS)
        if projected != value:
            write_json(path, projected)


def withhold_paper_files(capsule: Path) -> int:
    """Replace files extracted from the paper with an index entry; return how many."""
    withheld = 0
    for directory in PAPER_DERIVED_DIRS:
        folder = capsule / directory
        if not folder.is_dir():
            continue
        entries = []
        for name in tree_files(folder):
            if name in (PAPER_DERIVED_INDEX, WITHHELD_INDEX):
                continue
            path = folder / name
            entries.append({"name": name, "sha256": digest(path), "bytes": path.stat().st_size})
            path.unlink()
        if entries:
            write_json(folder / WITHHELD_INDEX, {"note": WITHHELD_NOTE, "files": entries})
            withheld += len(entries)
    for directory in sorted((path for path in capsule.rglob("*") if path.is_dir()), reverse=True):
        if not any(directory.iterdir()):
            directory.rmdir()
    return withheld


def anchor_repository(source: Path) -> dict | None:
    """Return the anchor repository's name, branch, last push and licence from the
    build's enrichment, choosing the repository the relationship check names."""
    try:
        enrichment = json.loads((source / "external_enrichment.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    repositories = [entry for entry in (enrichment.get("github_repos") or []) if isinstance(entry, dict)] \
        if isinstance(enrichment, dict) else []
    chosen = None
    try:
        named = json.loads((source / "repo_relationship.json").read_text(encoding="utf-8")).get("repo")
    except (OSError, ValueError, AttributeError):
        named = None
    if named:
        chosen = next((entry for entry in repositories
                       if str(entry.get("full_name", "")).lower() == str(named).lower()), {"full_name": named})
    elif len(repositories) == 1:
        chosen = repositories[0]
    if chosen is None:
        return None
    return {"full_name": chosen.get("full_name"), "default_branch": chosen.get("default_branch"),
            "pushed_at": chosen.get("pushed_at"), "license_spdx": chosen.get("license_spdx")}


def anchor_recipe(source: Path, doi: str | None, shipped: list[str], pipeline_public: bool) -> dict:
    """Describe how the build's anchor corpus can be rebuilt and checked by hash."""
    try:
        manifest = json.loads((source / "anchor_corpus" / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        manifest = None
    manifest = manifest if isinstance(manifest, dict) else {}
    return {
        "schema": "asb-anchor-recipe/1",
        "doi": doi,
        "anchor_manifest_present": bool(manifest),
        "source_kind": manifest.get("source_kind"),
        "partitions": manifest.get("partitions"),
        "partition_sha256": manifest.get("hashes"),
        "repository": anchor_repository(source),
        "commit_pinned": False,
        "text_shipped": bool(shipped),
        "text_files": shipped,
        "text_policy": "Anchor text ships only when the paper's quoted text is kept in full "
                       "(Creative Commons, CC0, public domain or a reuse grant); otherwise only these hashes ship.",
        "pipeline": PIPELINE_URL if pipeline_public else f"{PIPELINE_NAME} (private repository)",
        "statement": ANCHOR_RECIPE_STATEMENT,
    }


def stage_build(source: Path, destination: Path, with_indicium: bool, permissive: bool = False,
                doi: str | None = None, pipeline_public: bool = False) -> tuple[list[str], list[Path], dict]:
    """Copy the selected members, apply the projections, and return missing files,
    capsules and the staging facts (paper files withheld, anchor text shipped).

    `permissive` is true when the paper's quoted text is kept in full; it decides
    whether anchor text and paper-derived figure and table files ship.
    """
    selected, missing = select_members(source, with_indicium, permissive)
    for relative in selected:
        copy_selected(source, destination, relative)
    capsules = sorted(path for path in (source / "capsules").iterdir() if path.is_dir())
    withheld = 0
    for capsule in capsules:
        target = destination / "capsules" / capsule.name
        if not permissive and target.is_dir():
            withheld += withhold_paper_files(target)
        if target.is_dir():
            mark_artifact_membership(target)
    manifest_path = destination / "build_manifest.json"
    if manifest_path.is_file():
        write_json(manifest_path, project_build_manifest(read_json(manifest_path)))
    project_machine_identity(destination)
    shipped = [name for name in ANCHOR_TEXT_FILES if name in selected]
    write_json(destination / ANCHOR_RECIPE, anchor_recipe(source, doi, shipped, pipeline_public))
    return missing, capsules, {"paper_files_withheld": withheld, "anchor_text_shipped": bool(shipped)}


def tooling_commit() -> str:
    """Read the current tooling revision without changing Git state."""
    root = Path(__file__).resolve().parent.parent
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def input_digests(access_records: Path | None, deny_file: Path | None) -> dict:
    """Digest the optional runtime inputs whose content must not be written."""
    digests = {}
    if access_records:
        digests["access_records_sha256"] = digest(access_records)
    if deny_file:
        digests["deny_patterns_file_sha256"] = digest(deny_file)
    return digests


def source_receipt(view_name: str, collection: Path, extra_digests: dict) -> dict:
    """Bind the run to input trees and exact record files, not machine locators."""
    return {
        "view": view_name,
        "collection": collection.name,
        "collection_files": {
            name: digest(collection / name) for name in ("corpus.yaml", "collection.yaml", "CITATION.cff", ".zenodo.json")
            if (collection / name).is_file()
        },
        **extra_digests,
    }


def load_collection(root: Path) -> dict:
    """Read the four released-collection files the packer and the deposit tool use."""
    return {
        "collection": yaml.safe_load((root / "collection.yaml").read_text(encoding="utf-8")),
        "corpus": yaml.safe_load((root / "corpus.yaml").read_text(encoding="utf-8")),
        "citation": yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8")),
        "template": json.loads((root / ".zenodo.json").read_text(encoding="utf-8")),
    }


def collection_version_doi(loaded: dict) -> str:
    """Return the collection's current version DOI, read from its citation first."""
    citation, collection = loaded["citation"], loaded["collection"]
    doi = normalize_doi(citation.get("doi") or collection.get("version_doi") or collection.get("doi"))
    if not doi:
        raise ValueError("The collection has no version DOI")
    return doi


def released_names(corpus: dict) -> set[str]:
    """Return the build names of the papers the released corpus includes."""
    return {paper.get("name") for paper in corpus.get("papers") or [] if paper.get("status") == "included"}


def build_slug(source_name: str) -> str:
    """Return the archive slug of a build directory name."""
    return slug_from_build(source_name.split("__")[-1])


def build_input_receipt(source: Path, with_indicium: bool, ship_anchor_text: bool = False) -> dict:
    """Digest exactly the selected source members before screening."""
    selected, _ = select_members(source, with_indicium, ship_anchor_text)
    return {name: digest(source / name) for name in selected}


def private_repositories(registry: Path = REGISTRY, pipeline_public: bool = False) -> tuple[str, ...]:
    """Return the private repositories: every domain repository of the registry and the pipeline.

    The screen rewrites their URLs and `capsules_deposit.py plan` refuses any
    that remains. With `pipeline_public` the pipeline is left out of the list.
    """
    document = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
    names = {domain["repository"] for domain in (document.get("domains") or {}).values()
             if isinstance(domain, dict) and domain.get("repository")}
    if not pipeline_public:
        names.add(f"HolobiomicsLab/{PIPELINE_NAME}")
    return tuple(sorted(names))


def screen_build(root: Path, paper: dict, collection_meta: dict, options: dict,
                 article: str | None = None) -> tuple[dict, dict]:
    """Screen every staged text file and return counts and per-capsule quotes.

    `article`, the paper's article text, is given for a paper whose text is not kept
    in full: runs of at least `capsule_screen.OVERLAP_RUN` characters copied from it
    are trimmed from every shipped string outside the quotation fields.
    """
    context = capsule_screen.context_for(paper.get("doi") or "", paper.get("access") or {})
    if article is not None and context.retention != "full":
        context.article = capsule_screen.ArticleIndex(article)
    context.email_allowlist, context.email_role = _build_email_allowlist(collection_meta)
    context.deny_patterns = options["deny_patterns"]
    context.private_repositories = options["private_repositories"]
    budget = capsule_screen.QuoteBudget()
    verified_budget = capsule_screen.QuoteBudget()
    counts = capsule_screen.empty_counts()
    failures = []
    quotes_by_capsule = {}
    build_quotes = capsule_screen.empty_quotes()
    for path in sorted(member for member in root.rglob("*") if member.is_file()):
        relative = path.relative_to(root).as_posix()
        if not capsule_screen.is_text_member(relative, path.read_bytes()):
            continue
        capsule_dir = path.parent if path.name == "ro-crate-metadata.json" else None
        if capsule_dir is not None:
            original = json.loads(path.read_text(encoding="utf-8"))
            pruned = capsule_screen.prune_crate_document(original, capsule_dir)
            counts["crates_pruned"] += int(pruned != original)
        result = capsule_screen.screen_text(
            path.read_text(encoding="utf-8"), relative, context, budget, capsule_dir
        )
        path.write_text(result.text, encoding="utf-8")
        counts.update(result.counts)
        failures.extend(result.failures)
        measured, problems = capsule_screen.verify_quote_policy(
            path.read_text(encoding="utf-8"), relative, context, verified_budget
        )
        failures.extend(problem for problem in problems if problem not in failures)
        measured.update({key: result.quotes[key] for key in ("truncated", "dropped")})
        for key, value in measured.items():
            build_quotes[key] = max(build_quotes[key], value) if key == "longest" else build_quotes[key] + value
        if "capsules" in path.relative_to(root).parts:
            capsule_id = path.relative_to(root).parts[1]
            aggregate = quotes_by_capsule.setdefault(capsule_id, capsule_screen.empty_quotes())
            for key, value in measured.items():
                aggregate[key] = max(aggregate[key], value) if key == "longest" else aggregate[key] + value
    for crate in sorted(root.glob("capsules/*/ro-crate-metadata.json")):
        problems = crate_problems(crate.parent)
        failures.extend(f"{crate.relative_to(root).as_posix()}: {problem}" for problem in problems)
    counts["failures"] = len(failures)
    counts["spans_dropped_by_access_class"] = counts["spans_dropped"] if context.drop_quotes else 0
    return {"counts": dict(sorted(counts.items())), "failures": failures,
            "quote_retention": context.retention, "quotes_after_screen": build_quotes}, quotes_by_capsule


def validation_label(counts: dict) -> str:
    """Apply the present, clean, and strict rules to one set of counts."""
    state = "present"
    if counts["checked"] > 0 and counts["unsupported"] == 0 and counts["drift"] == 0:
        state = "clean"
    if counts["checked"] > 0 and counts["supported"] == counts["checked"] \
            and not any(counts[key] for key in ("partial", "unsupported", "drift")):
        state = "strict"
    return state


def declared_validation_counts(summary: dict) -> dict:
    """Normalize the five counts declared by validation.json summary."""
    names = {"checked": "n_claims_checked", "supported": "n_supported", "partial": "n_partial",
             "unsupported": "n_unsupported", "drift": "n_drift"}
    return {name: int(summary.get(source, 0) or 0) for name, source in names.items()}


def entry_validation_counts(entries: list) -> dict:
    """Count support and explicit drift from claims_checked entries."""
    counts = {key: 0 for key in (*VALIDATION_COUNT_KEYS, "unknown")}
    counts["checked"] = len(entries)
    for entry in entries:
        support = entry.get("supported") if isinstance(entry, dict) else None
        name = {"yes": "supported", "partial": "partial", "no": "unsupported"}.get(support, "unknown")
        counts[name] += 1
        counts["drift"] += int(isinstance(entry, dict) and entry.get("drift") is True)
    return counts


def validation_state(path: Path) -> tuple[str, dict, bool]:
    """Derive validation state from entries and conservatively compare the summary."""
    try:
        payload = read_json(path)
        declared = declared_validation_counts(payload.get("summary") or {})
    except (AttributeError, ValueError, TypeError):
        return "invalid", {}, False
    if "claims_checked" not in payload:
        return validation_label(declared), {"from_entries": None, "declared_summary": declared}, True
    if not isinstance(payload["claims_checked"], list):
        return "invalid", {"from_entries": None, "declared_summary": declared}, False
    entries = entry_validation_counts(payload["claims_checked"])
    consistent = all(entries[key] == declared[key] for key in VALIDATION_COUNT_KEYS)
    states = validation_label(entries), validation_label(declared)
    state = min(states, key=VALIDATION_STATE_ORDER.get)
    return state, {"from_entries": entries, "declared_summary": declared}, consistent


def evaluation_details(payload: dict) -> dict:
    """Count evaluation checks, unresolved references, and input readiness."""
    checks = payload.get("checks") if isinstance(payload.get("checks"), list) else []
    inputs = payload.get("inputs") if isinstance(payload.get("inputs"), list) else []
    kinds = Counter(
        check.get("kind") if isinstance(check, dict) and isinstance(check.get("kind"), str) else "unknown"
        for check in checks
    )
    unresolved = payload.get("unresolved_references")
    return {
        "task_id": payload.get("task_id"), "checks": len(checks),
        "checks_by_kind": dict(sorted(kinds.items())),
        "unresolved_references": len(unresolved) if isinstance(unresolved, list) else 0,
        "input_assets": len(inputs),
        "input_assets_with_hash": sum(bool(item.get("sha256")) for item in inputs if isinstance(item, dict)),
        "input_assets_with_download_hint": sum(bool(item.get("download_hint")) for item in inputs if isinstance(item, dict)),
    }


def eval_state(path: Path) -> tuple[str, dict]:
    """Apply the existing structural-completeness rule and report readiness."""
    try:
        payload = read_json(path)
    except (ValueError, TypeError):
        return "invalid", evaluation_details({})
    complete = EVAL_KEYS.issubset(payload) and isinstance(payload.get("checks"), list) and bool(payload["checks"]) and not payload.get("validation_errors")
    return ("complete" if complete else "partial"), evaluation_details(payload)


def read_json(path: Path) -> dict:
    """Read a required staged JSON object, failing loudly on invalid input."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} is not a JSON object")
    return value


def zip_build(root: Path, target: Path) -> dict:
    """Write a sorted deterministic archive with canonical timestamps and modes."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as archive:
        for source in sorted(path for path in root.rglob("*") if path.is_file()):
            name = source.relative_to(root).as_posix()
            archive.writestr(zenodo_deposit._zip_info(name, source), source.read_bytes(), compresslevel=9)
    return {"bytes": target.stat().st_size, "sha256": digest(target)}


def article_text(source: Path) -> str | None:
    """Read the paper's main article from the source build, for trimming only; never shipped.

    The package index names it (role `main_article`) inside `synthesized_package/`;
    without an index, `synthesized_package/article_fulltext.md` is read.
    """
    package = source / "synthesized_package"
    relative = "article_fulltext.md"
    try:
        index = json.loads((source / "package_index.json").read_text(encoding="utf-8"))
        relative = next(entry["relative_path"] for entry in index.get("files") or []
                        if isinstance(entry, dict) and entry.get("role") == "main_article")
    except (OSError, ValueError, AttributeError, StopIteration, KeyError):
        pass
    path = package / relative
    if not path.is_file() or package.resolve() not in path.resolve().parents:
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if text.strip() else None


def paper_text_shared(paper: dict) -> bool:
    """Tell whether the paper's text is shared verbatim: the screen's rule for keeping
    quoted text in full (`capsule_screen.context_for`), applied unchanged."""
    return capsule_screen.context_for(paper.get("doi") or "", paper.get("access") or {}).retention == "full"


def pack_one(source: Path, stage_parent: Path, out: Path, paper: dict, collection_meta: dict, options: dict) -> tuple[dict, list[dict], dict]:
    """Stage, screen, and archive one build, returning its receipt rows."""
    started = time.monotonic()
    slug = build_slug(source.name)
    stage_root = stage_parent / slug
    stage_root.mkdir()
    permissive = paper_text_shared(paper)
    missing, capsules, facts = stage_build(source, stage_root, options["with_indicium"], permissive,
                                           paper.get("doi"), options.get("pipeline_public", False))
    article = None if permissive else article_text(source)
    if not permissive and article is None:
        missing.append("article_text")
    screen, quotes = screen_build(stage_root, paper, collection_meta, options, article)
    del article
    screen["counts"]["paper_files_withheld"] = facts["paper_files_withheld"]
    screen["counts"] = dict(sorted(screen["counts"].items()))
    screen["anchor_text_shipped"] = facts["anchor_text_shipped"]
    screen["failures"].extend(f"missing:{name}" for name in missing)
    screen["counts"]["failures"] = len(screen["failures"])
    rows = capsule_rows(stage_root, slug, paper, capsules, quotes)
    for row in rows:
        if "invalid" in {row["validation_state"], row["eval_state"]}:
            screen["failures"].append(f"capsules/{row['capsule_id']}: invalid_validation_or_eval")
    screen["counts"]["failures"] = len(screen["failures"])
    entry = {
        "build_slug": slug,
        "source_name": source.name,
        "paper_doi": paper.get("doi"),
        "access_class": capsule_screen.access_class_for(paper.get("access") or {}),
        "license": (paper.get("access") or {}).get("license"),
        "access_source": paper.get("access_source"),
        "capsule_ids": [row["capsule_id"] for row in rows],
        "zip_member": f"builds/{slug}.zip",
        "validation_state": aggregate_validation(rows),
        "eval_state": "complete" if rows and all(row["eval_state"] == "complete" for row in rows) else "partial",
        "screen": screen,
        "input_sha256": build_input_receipt(source, options["with_indicium"], permissive),
    }
    if not screen["failures"]:
        entry.update(zip_build(stage_root, out / "hf" / "builds" / f"{slug}.zip"))
    else:
        entry.update({"bytes": 0, "sha256": None})
    entry["wall_seconds"] = round(time.monotonic() - started, 3)
    return entry, rows, screen


def capsule_rows(root, build_slug, paper, capsules, quotes) -> list[dict]:
    """Create one metadata-table row per staged capsule."""
    rows = []
    for capsule in capsules:
        validation, claims, summary_consistent = validation_state(
            root / "capsules" / capsule.name / "validation.json"
        )
        evaluation, eval_details = eval_state(root / "capsules" / capsule.name / "eval.json")
        tier = reproducibility_tier(root / "capsules" / capsule.name / "task_card.json")
        rows.append({
            "build_slug": build_slug,
            "capsule_id": capsule.name,
            "paper_doi": paper.get("doi"),
            "access_class": capsule_screen.access_class_for(paper.get("access") or {}),
            "license": (paper.get("access") or {}).get("license"),
            "task_id": eval_details["task_id"],
            "eval_state": evaluation,
            "eval_checks": eval_details["checks"],
            "eval_checks_by_kind": eval_details["checks_by_kind"],
            "eval_unresolved_references": eval_details["unresolved_references"],
            "eval_input_assets": eval_details["input_assets"],
            "eval_input_assets_with_hash": eval_details["input_assets_with_hash"],
            "eval_input_assets_with_download_hint": eval_details["input_assets_with_download_hint"],
            "validation_state": validation,
            "validation_summary_consistent": summary_consistent,
            "claims": claims,
            "quotes_after_screen": quotes.get(capsule.name, {}),
            "reproducibility_tier": tier,
        })
        rows[-1]["readiness"] = capsule_readiness(rows[-1])
    return rows


def reproducibility_tier(path: Path) -> str | None:
    """Read the task card's reproducibility tier; None when the card or the field is absent."""
    try:
        value = read_json(path).get("reproducibility_tier")
    except (OSError, ValueError, TypeError):
        return None
    return value if isinstance(value, str) else None


def capsule_readiness(row: dict) -> str | None:
    """Readiness of one capsule row from its own fields; None when validation or evaluation is invalid.

    documented: validation present. validated: validation clean or strict, evaluation
    partial. evaluable: validation clean or strict, evaluation complete. executable:
    evaluable, at least one input in eval.json, every input with a sha256 and a download
    hint, and a certified reproducibility tier. Readiness is not the maturity scale.
    """
    validation, evaluation = row["validation_state"], row["eval_state"]
    if "invalid" in (validation, evaluation):
        return None
    if validation not in ("clean", "strict"):
        return "documented"
    if evaluation != "complete":
        return "validated"
    inputs = row.get("eval_input_assets") or 0
    ready = inputs > 0 and row.get("eval_input_assets_with_hash") == inputs \
        and row.get("eval_input_assets_with_download_hint") == inputs
    return "executable" if ready and row.get("reproducibility_tier") == "certified" else "evaluable"


def readiness_counts(rows: list[dict]) -> dict:
    """Count rows per readiness level, every level listed."""
    counts = Counter(row.get("readiness") for row in rows)
    return {level: counts.get(level, 0) for level in READINESS_LEVELS}


def aggregate_validation(rows: list[dict]) -> str:
    """Summarize build validation conservatively from its capsules."""
    states = {row["validation_state"] for row in rows}
    if states == {"strict"}:
        return "strict"
    if states <= {"strict", "clean"}:
        return "clean"
    return "present"


def make_manifest(args, collection, builds, rows, layout: dict) -> dict:
    """Build the versioned archive-set manifest.

    `not_released` lists the slugs of builds whose paper is not an included
    paper of the released corpus; they are neither staged nor zipped.
    """
    return {
        "schema": "asb-capsules-manifest/1",
        "domain": collection.get("domain") or collection.get("slug"),
        "collection_version": str(collection["version"]),
        "collection_version_doi": args.version_doi,
        "cut_id": collection.get("cut_id"),
        "tooling_commit": tooling_commit(),
        "generation_date": args.date,
        "inclusion_policy": {
            "capsule_members": _CAPSULE_KEEP + list(CAPSULE_FILES) + list(CAPSULE_OPTIONAL_FILES)
            + [f"{name}/" for name in CAPSULE_OPTIONAL_DIRS],
            "build_members": ["ledger"] + list(BUILD_FILES) + list(BUILD_OPTIONAL_FILES)
            + [f"{name}/" for name in BUILD_OPTIONAL_DIRS] + [ANCHOR_RECIPE]
            + ([INDICIUM_FILE] if args.with_indicium else []),
            "anchor_text_members": list(ANCHOR_TEXT_FILES),
            "anchor_text_rule": "shipped only for builds whose quoted paper text is kept in full",
            "paper_derived_capsule_dirs": [f"{name}/" for name in PAPER_DERIVED_DIRS],
            "paper_derived_rule": f"replaced by {WITHHELD_INDEX} unless quoted paper text is kept in full",
            "with_indicium": args.with_indicium,
            "pipeline_public": args.pipeline_public,
        },
        "layout": layout,
        "readiness_counts": readiness_counts(rows),
        "build_count": len(builds),
        "builds_packed": sum(bool(build.get("sha256")) for build in builds),
        "builds_left_out": sum(not build.get("sha256") for build in builds),
        "capsule_count": len(rows),
        "capsules_left_out": sum(len(build["capsule_ids"]) for build in builds if not build.get("sha256")),
        "total_bytes": sum(build["bytes"] for build in builds),
        "not_released_count": len(args.not_released),
        "not_released": args.not_released,
        "source_inputs": source_receipt(args.view_name, args.collection, args.receipt_digests),
        "builds": builds,
    }


def make_screen(builds: list[dict], strict: bool) -> dict:
    """Aggregate non-sensitive screen measurements."""
    totals = Counter()
    for build in builds:
        totals.update(build["screen"]["counts"])
    return {
        "schema": "asb-capsules-screen/1",
        "strict": strict,
        "totals": dict(sorted(totals.items())),
        "builds": [{"build_slug": build["build_slug"], **build["screen"]} for build in builds],
    }


def make_zenodo(collection, template, args) -> dict:
    """Create deposit-ready metadata without contacting Zenodo."""
    domain = collection.get("domain") or collection.get("slug")
    description = (
        f"Screened build capsules and build provenance supplementing ASB {domain} v{collection['version']}, "
        "in shard archives of per-build zips. "
        f"The builds were produced by the {PIPELINE_NAME} pipeline. "
        "Anchor-corpus text and figure or table files extracted from a paper ship only when that "
        "paper's text may be shared verbatim; otherwise their hashes ship. "
        "Generated metadata is CC-BY-4.0. Text quoted from each paper stays under that paper's licence: "
        "kept for Creative Commons, CC0 and public-domain papers, capped by field and DOI or removed "
        "otherwise. Rights holders may request takedown "
        "through the asb-skill-collections issue tracker."
    )
    related = [
        {"relation": "isSupplementTo", "identifier": args.version_doi, "scheme": "doi"},
        {"relation": "references", "identifier": TOOLING_URL, "scheme": "url"},
    ]
    if args.pipeline_public:
        related.append({"relation": "isCompiledBy", "identifier": PIPELINE_URL, "scheme": "url"})
    return {
        "title": f"ASB {domain} v{collection['version']} build capsules",
        "upload_type": "dataset",
        "publication_date": args.date,
        "description": description,
        "access_right": "open",
        "license": "cc-by-4.0",
        "creators": collection_creators(collection, args.citation, Path(__file__).resolve().parent.parent),
        "keywords": template.get("keywords") or [],
        "subjects": template.get("subjects") or [],
        "communities": [{"identifier": "asb_skill_collections"}],
        "related_identifiers": related,
        "version": f"{domain}-v{collection['version']}-capsules",
        "language": template.get("language", "eng"),
    }


def collection_creators(collection, citation, tooling_root: Path) -> list[dict]:
    """Use collection-declared creators, with the release creator file as fallback."""
    declared = (collection.get("roles") or {}).get("zenodo_authors")
    if declared:
        return [zenodo_deposit._zenodo_creator(entry) for entry in declared]
    authors = citation.get("authors") or []
    if authors:
        creators = []
        for author in authors:
            if author.get("name"):
                creators.append({"name": author["name"]})
            else:
                creators.append({"name": f"{author['family-names']}, {author['given-names']}"})
        return creators
    return zenodo_deposit.expected_creators(tooling_root)


def make_hf_card(collection, citation, manifest, args) -> str:
    """Render a local dataset card with JSONL or optional Parquet configuration."""
    domain = collection.get("domain") or collection.get("slug")
    tables = {name: hf_table(args.out / "hf", stem) for name, stem, _, _ in HF_CONFIGS}
    table = tables["capsules"]
    configs = "\n".join(f'  - config_name: {name}\n    data_files: "{tables[name]}"' for name, _, _, _ in HF_CONFIGS)
    config_lines = "\n".join(f"- `{name}` (`{tables[name]}`): {meaning}." for name, _, meaning, _ in HF_CONFIGS)
    levels = ", ".join(f"{level} {count}" for level, count in manifest["readiness_counts"].items())
    public_citation = {key: value for key, value in citation.items() if key not in PRIVATE_CITATION_KEYS}
    pipeline = PIPELINE_URL if args.pipeline_public else f"{PIPELINE_NAME} (private repository)"
    capsules_doi = normalize_doi(getattr(args, "capsules_doi", None))
    capsules_record = (
        f"Capsules record: https://doi.org/{capsules_doi}"
        if capsules_doi else
        "Capsules record: the Zenodo record for these capsules is listed on the collection's registry row."
    )
    return f"""---
license: cc-by-4.0
task_categories: [question-answering]
size_categories: [{size_category(manifest['capsule_count'])}]
language: [en]
pretty_name: "ASB {domain} v{collection['version']} build capsules"
configs:
{configs}
---

# ASB {domain} v{collection['version']} build capsules

This dataset holds {manifest['builds_packed']} per-build deterministic zips and {manifest['capsule_count']} capsule metadata rows. The metadata table is `{table}`. {EVALUATION_LISTING_STATEMENT}

Zenodo is the archival record of these capsules: it holds the same build zips grouped in shard archives, with a DOI. This dataset is the day-to-day access point: one zip per build, and one table per configuration.

## Configurations

{config_lines}

## Readiness

{READINESS_STATEMENT}

Capsules per readiness level: {levels}.

## Layout

- `builds/<build-slug>.zip`: the screened capsules of one build (ledgers, evaluations, evidence, inputs, task cards, scripts, tables, figures, outputs, nanopublications, provenance and pruned RO-Crates) and its build provenance (ledger, manifests, task cards, ASTRA files, workflow exports, reports, scores, certification, the indicium graph, the anchor-corpus hashes and `{ANCHOR_RECIPE}`).
- A row's `member` is the path of its build zip in this layout; `shard` names the Zenodo archive that holds the same zip.

## Records and licence

Collection: https://doi.org/{args.version_doi}

{capsules_record}

Generated metadata is CC-BY-4.0. The `license` table field is the source paper's licence; text quoted from that paper stays under the paper's own terms, NonCommercial and NoDerivatives terms included; it is kept in full for Creative Commons, CC0 and public-domain papers, and shortened or removed otherwise. The same rule decides whether a build ships its anchor-corpus text and the figure and table files extracted from its paper; otherwise their hashes ship. Tools retain their own licences, which this record does not alter.

Pipeline: {pipeline}

Tooling: {TOOLING_URL}

## Citation

Cite the capsules record by its Zenodo DOI and the collection at https://doi.org/{args.version_doi}. If the capsules DOI is not shown above, obtain it from the collection's registry row.

```yaml
{yaml.safe_dump(public_citation, sort_keys=False).strip()}
```

Local generation only: no dataset repository is created or uploaded by the packer.
"""


def hf_table(hf: Path, stem: str) -> str:
    """Return the data file of one configuration: Parquet when it was written, JSON Lines otherwise."""
    parquet = Path(stem).with_suffix(".parquet").name
    return parquet if (hf / parquet).is_file() else stem


def render_field_dictionary() -> str:
    """Render the shared row-field dictionary for both public tables."""
    def table(definitions):
        lines = ["| Field | Unit or values | Meaning |", "|---|---|---|"]
        lines += [f"| `{name}` | {unit} | {meaning} |" for name, (unit, meaning) in definitions.items()]
        return "\n".join(lines)

    text = "## Table field dictionary\n\n### `capsules.jsonl` rows\n\n" + table(CAPSULE_FIELD_DEFINITIONS)
    if BENCHMARK_FIELD_DEFINITIONS is CAPSULE_FIELD_DEFINITIONS:
        return text + "\n\nThe capsule rows of `benchmark-manifest.json` carry the same fields."
    return text + "\n\n### `benchmark-manifest.json` capsule rows\n\n" + table(BENCHMARK_FIELD_DEFINITIONS)


def render_screen_counters(screen: dict) -> str:
    """Render each SCREEN.json total on one reader-facing line."""
    totals = screen.get("totals") or {}
    return "\n".join(
        f"- `{name}` ({value}): {SCREEN_COUNTER_DEFINITIONS.get(name, 'screen events')}."
        for name, value in sorted(totals.items())
    )


def size_category(count: int) -> str:
    """Map row counts to HuggingFace size categories."""
    if count < 1000:
        return "n<1K"
    if count < 10000:
        return "1K<n<10K"
    if count < 100000:
        return "10K<n<100K"
    return "100K<n<1M"


def write_archive_readme(out: Path, manifest: dict, screen: dict) -> None:
    """Write the archive-set guide."""
    text = f"""# ASB {manifest['domain']} v{manifest['collection_version']} build capsules

Local screened archive set generated on {manifest['generation_date']}. No deposit, upload, or collection-record change was performed.

- `hf/builds/`: one deterministic zip per build that passed the screen (the HuggingFace layout), with `hf/README.md` and one table per dataset configuration.
- `zenodo/`: the shard archives, each holding up to {manifest['layout']['shard_size']} build zips stored under `builds/`, and `zenodo/metadata.json`. {len(manifest['layout']['shards'])} shards; with the five receipts below the record holds {manifest['layout']['zenodo_files']} files.
- `MANIFEST.json`: build, shard and archive receipt.
- `capsules.jsonl`: one metadata row per capsule; `shard` and `member` locate its build zip.
- `SCREEN.json`: content-screen counts and failures.
- `benchmark-manifest.json`: structurally complete evaluation-definition subset.

Zenodo is the archival record; HuggingFace is the day-to-day access point.

Builds considered: {manifest['build_count']}. Builds packed: {manifest['builds_packed']}. Builds left out by the screen: {manifest['builds_left_out']}.

Capsules packed: {manifest['capsule_count']}. Capsules left out with their builds: {manifest['capsules_left_out']}.

Builds left out because their paper is not an included paper of the released corpus: {manifest['not_released_count']}. They are listed by slug under `not_released` in `MANIFEST.json`.

{EVALUATION_LISTING_STATEMENT}

## Readiness

{READINESS_STATEMENT}

Capsules per readiness level: {", ".join(f"{level} {count}" for level, count in manifest['readiness_counts'].items())}.

In each capsule's `artifact_provenance.json`, `{ARTIFACT_MEMBERSHIP_FIELD}` says whether the named full-build artifact is present in the shipped capsule.

Each build zip holds `{ANCHOR_RECIPE}`: the paper DOI, the anchor repository, the per-partition sha256 of its anchor corpus and whether the corpus text ships. {ANCHOR_RECIPE_STATEMENT}

## `SCREEN.json` counters

{render_screen_counters(screen)}

{render_field_dictionary()}
"""
    (out / "README.md").write_text(text, encoding="utf-8")


def maybe_write_parquet(rows: list[dict], path: Path) -> bool:
    """Write Parquet only when the optional dependency is already available."""
    try:
        import pyarrow
        import pyarrow.parquet
    except ImportError:
        return False
    table = pyarrow.Table.from_pylist(rows)
    pyarrow.parquet.write_table(table, path)
    return True


def packed_capsule_rows(builds: list[dict], rows: list[dict]) -> list[dict]:
    """Return only capsule rows whose build has a zip in the record."""
    packed_slugs = {build["build_slug"] for build in builds if build.get("sha256")}
    return [row for row in rows if row["build_slug"] in packed_slugs]


def write_records(args, loaded: dict, builds: list[dict], rows: list[dict]) -> None:
    """Write every descriptive file of a pack from its build entries and capsule rows.

    The packer and `capsules_deposit.py refresh` both call this, so a refreshed
    pack holds what a full pack with the same inputs would write. `args` carries
    out, date, version_doi, citation, view_name, receipt_digests, with_indicium,
    strict, not_released, pipeline_public, shard_size and the collection root.
    Packed build zips are read from `out/hf/builds/`; the shards are written
    under `out/zenodo/`.
    """
    collection = loaded["collection"]
    rows = packed_capsule_rows(builds, rows)
    domain = collection.get("domain") or collection.get("slug")
    layout = assign_shards(builds, rows, domain, str(collection["version"]),
                           getattr(args, "shard_size", SHARD_SIZE) or SHARD_SIZE)
    check_zenodo_layout(layout)
    write_shards(args.out, builds, layout)
    check_zenodo_layout(layout)
    for row in rows:
        row["readiness"] = capsule_readiness(row)
    manifest = make_manifest(args, collection, builds, rows, layout)
    screen = make_screen(builds, args.strict)
    write_json(args.out / "MANIFEST.json", manifest)
    write_json(args.out / "SCREEN.json", screen)
    write_rows(args.out / "capsules.jsonl", rows)
    maybe_write_parquet(rows, args.out / "capsules.parquet")
    metadata = make_zenodo(collection, loaded["template"], args)
    problems = zenodo_deposit.validate_metadata(metadata)
    if problems:
        raise ValueError("Invalid Zenodo metadata: " + "; ".join(problems))
    write_json(args.out / "zenodo" / "metadata.json", metadata)
    benchmark = make_benchmark(builds, rows, args.version_doi)
    write_hf_tables(args.out / "hf", rows, benchmark["capsules"])
    (args.out / "hf" / "README.md").write_text(make_hf_card(collection, loaded["citation"], manifest, args), encoding="utf-8")
    write_json(args.out / "benchmark-manifest.json", benchmark)
    write_archive_readme(args.out, manifest, screen)


def write_rows(path: Path, rows: list[dict]) -> None:
    """Write table rows as sorted-key JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_hf_tables(hf: Path, rows: list[dict], benchmark_rows: list[dict]) -> None:
    """Write one data file per HuggingFace configuration, and Parquet copies when available."""
    for name, stem, _, levels in HF_CONFIGS:
        selected = benchmark_rows if name == "benchmark" else \
            [row for row in rows if levels is None or row.get("readiness") in levels]
        write_rows(hf / stem, selected)
        maybe_write_parquet(selected, hf / Path(stem).with_suffix(".parquet").name)


def shard_name(domain: str, version: str, index: int) -> str:
    """Return the file name of one Zenodo shard, numbered from 1."""
    return f"asb-{domain}-v{version}-builds-{index:03d}.zip"


def assign_shards(builds: list[dict], rows: list[dict], domain: str, version: str, shard_size: int) -> dict:
    """Group packed builds, sorted by slug, into shards of `shard_size` and set `shard`
    and `member` on each packed build entry and capsule row."""
    if shard_size < 1:
        raise ValueError("--shard-size must be at least 1")
    packed = sorted((build for build in builds if build.get("sha256")), key=lambda build: build["build_slug"])
    shards = []
    for index, start in enumerate(range(0, len(packed), shard_size), 1):
        members = packed[start:start + shard_size]
        name = shard_name(domain, version, index)
        for build in members:
            build["shard"], build["member"] = name, build["zip_member"]
        shards.append({"name": name, "builds": [build["build_slug"] for build in members],
                       "bytes": None, "sha256": None,
                       "build_bytes": sum(build["bytes"] for build in members)})
    by_slug = {build["build_slug"]: build for build in packed}
    for row in rows:
        build = by_slug.get(row["build_slug"])
        row["shard"] = build["shard"] if build else None
        row["member"] = build["member"] if build else None
    return {"shard_size": shard_size, "shards": shards,
            "zenodo_files": len(shards) + len(ZENODO_RECEIPTS),
            "zenodo_file_budget": ZENODO_FILE_BUDGET,
            "hf_builds": "hf/builds/<build_slug>.zip"}


def write_shards(out: Path, builds: list[dict], layout: dict) -> None:
    """Write the shards of a pack under `zenodo/` from its `hf/builds/` zips.

    Nothing is written when a packed build zip is missing (a strict pass that failed
    removed them); the shard entries then keep a null size and digest.
    """
    by_slug = {build["build_slug"]: build for build in builds}
    sources = {slug: out / "hf" / by_slug[slug]["zip_member"] for shard in layout["shards"] for slug in shard["builds"]}
    if not all(path.is_file() for path in sources.values()):
        return
    for shard in layout["shards"]:
        target = write_shard(out / "zenodo" / shard["name"],
                             {by_slug[slug]["zip_member"]: sources[slug].read_bytes() for slug in shard["builds"]})
        shard.update(bytes=target.stat().st_size, sha256=digest(target))


def write_shard(target: Path, members: dict[str, bytes]) -> Path:
    """Write one shard: build zips stored without recompression, sorted, with fixed
    timestamps and modes, so the same build zips give the same bytes."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=zenodo_deposit.ZIP_EPOCH)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, members[name])
    return target


def check_zenodo_layout(layout: dict) -> None:
    """Refuse a layout whose record would exceed the file budget or Zenodo's size limit."""
    if layout["zenodo_files"] > ZENODO_FILE_BUDGET:
        raise ValueError(
            f"the Zenodo record would hold {layout['zenodo_files']} files ({len(layout['shards'])} shards "
            f"and {len(ZENODO_RECEIPTS)} receipts), over the budget of {ZENODO_FILE_BUDGET}; "
            "raise --shard-size")
    total = sum(shard["bytes"] or shard["build_bytes"] for shard in layout["shards"])
    if total > ZENODO_MAX_BYTES:
        raise ValueError(f"the shards hold {total} bytes, over Zenodo's limit of {ZENODO_MAX_BYTES} bytes per record")


def make_benchmark(builds: list[dict], rows: list[dict], version_doi: str) -> dict:
    """Select the complete-evaluation capsules without copying their payloads.

    Rows keep the sorted key order of capsules.jsonl, so a pack refreshed from
    that file writes the same bytes.
    """
    benchmark_rows = [json.loads(json.dumps(row, sort_keys=True)) for row in rows if row["eval_state"] == "complete"]
    benchmark_ids = {(row["build_slug"], row["capsule_id"]) for row in benchmark_rows}
    benchmark_builds = [
        dict(build, capsule_ids=[value for value in build["capsule_ids"] if (build["build_slug"], value) in benchmark_ids])
        for build in builds
        if build.get("sha256") and any((build["build_slug"], value) in benchmark_ids for value in build["capsule_ids"])
    ]
    totals = {
        "checks_by_kind": dict(sorted(sum(
            (Counter(row["eval_checks_by_kind"]) for row in benchmark_rows), Counter()
        ).items())),
        "unresolved_references": sum(row["eval_unresolved_references"] for row in benchmark_rows),
        "input_assets": sum(row["eval_input_assets"] for row in benchmark_rows),
        "input_assets_with_hash": sum(row["eval_input_assets_with_hash"] for row in benchmark_rows),
        "input_assets_with_download_hint": sum(row["eval_input_assets_with_download_hint"] for row in benchmark_rows),
    }
    return {
        "schema": "asb-capsules-benchmark/1", "collection_version_doi": version_doi,
        "listing_statement": EVALUATION_LISTING_STATEMENT, "capsule_count": len(benchmark_rows),
        "totals": totals, "capsules": benchmark_rows, "builds": benchmark_builds,
    }


def bind_collection(args) -> dict:
    """Load the collection and set the receipt values every writer reads from args."""
    loaded = load_collection(args.collection)
    args.citation = loaded["citation"]
    args.version_doi = collection_version_doi(loaded)
    return loaded


def run(args) -> int:
    """Run the local packer and return a process status."""
    loaded = bind_collection(args)
    args.view_name = args.view.name
    args.receipt_digests = input_digests(args.access_records, args.deny_patterns_file)
    args.out.mkdir(parents=True, exist_ok=True)
    released = released_names(loaded["corpus"])
    sources = discover_builds(args.view, args.limit)
    args.not_released = sorted(build_slug(source.name) for source in sources if source.name not in released)
    overrides = load_access_records(args.access_records)
    deny_patterns = tuple(line.strip() for line in args.deny_patterns_file.read_text(encoding="utf-8").splitlines() if line.strip()) if args.deny_patterns_file else ()
    options = {"with_indicium": args.with_indicium, "deny_patterns": deny_patterns,
               "pipeline_public": args.pipeline_public,
               "private_repositories": private_repositories(pipeline_public=args.pipeline_public)}
    builds, rows = [], []
    with tempfile.TemporaryDirectory(prefix="capsules-stage-", dir=args.out) as temporary:
        for source in (source for source in sources if source.name in released):
            paper = resolve_paper(source.name, loaded["corpus"], overrides)
            entry, capsule_data, _ = pack_one(source, Path(temporary), args.out, paper, loaded["collection"], options)
            builds.append(entry)
            rows.extend(capsule_data)
    timings = [{"build_slug": build["build_slug"], "wall_seconds": build.pop("wall_seconds")} for build in builds]
    failed = any(build["screen"]["failures"] for build in builds)
    if args.strict and failed:
        shutil.rmtree(args.out / "hf" / "builds", ignore_errors=True)
    write_records(args, loaded, builds, rows)
    packed_rows = packed_capsule_rows(builds, rows)
    left_out = sum(len(build["capsule_ids"]) for build in builds if not build.get("sha256"))
    layout = json.loads((args.out / "MANIFEST.json").read_text(encoding="utf-8"))["layout"]
    print(json.dumps({"builds": len(builds), "capsules": len(packed_rows), "capsules_left_out": left_out,
                      "not_released": len(args.not_released), "shards": len(layout["shards"]),
                      "zenodo_files": layout["zenodo_files"], "readiness_counts": readiness_counts(packed_rows),
                      "wall_seconds_by_build": timings}))
    return int(args.strict and failed)


def parse_args(argv=None):
    """Parse the packer command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", type=Path, required=True)
    parser.add_argument("--collection", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--access-records", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--with-indicium", action="store_true", default=True,
                        help="ship each build's indicium.jsonld (the default)")
    parser.add_argument("--no-indicium", dest="with_indicium", action="store_false",
                        help="leave indicium.jsonld out of the build zips")
    parser.add_argument("--shard-size", type=int, default=SHARD_SIZE,
                        help=f"build zips per Zenodo shard (default {SHARD_SIZE})")
    parser.add_argument("--deny-patterns-file", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--pipeline-public", action="store_true",
                        help=f"link the {PIPELINE_NAME} repository and keep its URLs; leave off while it is private")
    parser.add_argument("--capsules-doi", help="published DOI of this capsules record for the dataset card")
    args = parser.parse_args(argv)
    args.view = args.view.resolve()
    args.collection = args.collection.resolve()
    args.out = args.out.resolve()
    return args


def main(argv=None) -> int:
    """Command-line entry point."""
    return run(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
