"""Local file snapshots for the release gate and the asb-cut/v0 contract.

SHA-256 covers canonical JSON records of sorted relative paths, directories,
file sizes and file hashes, matching ASB's cut writer. These are integrity
receipts, not signatures or scientific validation.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from asb_skill_collections import layout

MANIFEST_NAME = "MANIFEST.gen.json"
INVENTORY_KEYS = ("skills", "tools", "workflows", "papers", "dois")
WORKFLOW_NAMES = ("workflow.smk", "workflow.nf", "workflow.cwl", "workflow.yaml")


def digest(value: Any) -> str:
    """Return SHA-256 of a value serialized as canonical UTF-8 JSON."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_record(path: Path, label: str) -> dict:
    """Hash one file's bytes and return its labelled size/digest record."""
    checksum = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
            size += len(block)
    record = {"path": label, "bytes": size, "sha256": checksum.hexdigest()}
    if path.is_symlink():
        record["link"] = os.readlink(path)
    return record


def tree_records(root: Path, excluded: tuple[Path, ...] = (), *, output_tree=True) -> list[dict]:
    """Snapshot a tree, rejecting output symlinks and unavailable entries."""
    records = []
    for path in sorted(root.rglob("*")):
        if any(path == item or item in path.parents for item in excluded):
            continue
        label = path.relative_to(root).as_posix()
        if path.is_symlink() and (output_tree or not path.is_file()):
            raise ValueError(f"Unsupported tree symlink: {label}")
        if path.is_file():
            records.append(file_record(path, label))
        elif path.is_dir():
            records.append({"path": label, "directory": True})
        else:
            raise OSError(f"Unreadable tree entry: {label}")
    return records


def capture_target(root: Path, report_path: Path) -> dict:
    """Bind the complete output tree, excluding only this receipt and the manifest."""
    if report_path.is_dir():
        raise ValueError("A receipt exclusion must be a file, never a payload directory")
    excluded = [root / MANIFEST_NAME]
    if root in report_path.parents:
        excluded.append(report_path)
    entries = tree_records(root, tuple(excluded))
    manifest_path = root / MANIFEST_NAME
    if manifest_path.is_symlink() or report_path.is_symlink():
        raise ValueError("A manifest or receipt cannot be a symlink")
    return {
        "payload": {"sha256": digest(entries), "entries": entries,
                    "excluded_paths": sorted(path.relative_to(root).as_posix() for path in excluded)},
        "manifest": file_record(manifest_path, MANIFEST_NAME) if manifest_path.exists() else None,
    }


def corpus_record(root: Path, corpus: Path | None) -> dict | None:
    """Bind corpus bytes, preserving whether the input is inside the collection."""
    if corpus is None or not corpus.is_file():
        return None
    corpus = corpus.resolve()
    internal = root in corpus.parents
    record = file_record(corpus, corpus.relative_to(root).as_posix() if internal else str(corpus))
    return {**record, "location": "collection" if internal else "external"}


def _ancestor_records(root: Path) -> list[dict]:
    records = []
    for filename in ("build_manifest.json", "repo_relationship.json"):
        if (root / filename).exists():
            continue
        for depth, parent in enumerate(root.parents, 1):
            candidate = parent / filename
            if candidate.exists():
                label = "../" * depth + filename
                records.append(file_record(candidate, label) if candidate.is_file()
                               else {"path": label, "directory": True})
                break
            if filename == "repo_relationship.json" and (
                (parent / "build_manifest.json").exists() or depth >= 6
            ):
                break
    return records


def capture_inputs(paths: list[Path], target: Path) -> dict:
    """Recompute ASB input closure, including its upward metadata lookups."""
    roots = []
    for path in paths:
        root = path.resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"Input directory is missing: {path}")
        if root == target:
            raise ValueError("The collection cannot also be an input root")
        excluded = (target,) if root in target.parents else ()
        roots.append({"name": root.name,
                      "excluded_paths": [p.relative_to(root).as_posix() for p in excluded],
                      "entries": tree_records(root, excluded, output_tree=False),
                      "ancestors": _ancestor_records(root)})
    return {"sha256": digest(roots), "roots": roots}


def read_cut_record(root: Path) -> dict:
    """Read and validate the digests and format of an asb-cut/v0 record."""
    record = json.loads((root / MANIFEST_NAME).read_text(encoding="utf-8"))
    if record["schema"] != "asb-cut/v0":
        raise ValueError("Unsupported cut manifest schema")
    if record["sha256"] != digest({k: v for k, v in record.items() if k != "sha256"}):
        raise ValueError("Cut manifest record digest mismatch")
    if record["output"]["excluded_paths"] != [MANIFEST_NAME]:
        raise ValueError("Unsupported cut output exclusions")
    if record["inputs"]["sha256"] != digest(record["inputs"]["roots"]):
        raise ValueError("Cut input digest mismatch")
    if record["output"]["sha256"] != digest(record["output"]["entries"]):
        raise ValueError("Cut output digest mismatch")
    if set(record["inventory"]) != set(INVENTORY_KEYS):
        raise ValueError("Malformed cut inventory")
    if any(type(value) is not int or value < 0 for value in record["inventory"].values()):
        raise ValueError("Cut inventory counts must be non-negative integers")
    return record


def input_file_count(inputs: dict) -> int:
    """Count files, excluding directory entries, in an ASB input closure."""
    return sum("sha256" in entry for root in inputs["roots"]
               for entry in root["entries"] + root["ancestors"])


def read_inventory(root: Path, corpus: dict) -> dict[str, int]:
    """Recompute inventory in legacy, router and ASB cut layouts.

    ASB source_capsules IDs distinguish papers sharing a DOI. Legacy corpora
    use their declared paper identity, falling back to the complete row.
    """
    papers = corpus.get("papers") or []
    sources = corpus.get("source_capsules")
    identities = ({row["id"] for row in sources} if sources is not None else
                  {str(row.get("id") or row.get("capsule_id") or row.get("doi")
                       or row.get("name") or digest(row)) for row in papers})
    dois = {str(row["doi"]).lower().removeprefix("https://doi.org/") for row in papers if row.get("doi")}
    tools = list((root / "tools").glob("*.yaml"))
    if not (root / "tools").is_dir() and (root / "tools_index.json").is_file():
        tools = json.loads((root / "tools_index.json").read_text(encoding="utf-8"))
        if not isinstance(tools, list):
            raise ValueError("tools_index.json must contain a list of tool records")
    workflows = sum(len(list(root.glob(f"benchmark/tasks/*/{name}"))) for name in WORKFLOW_NAMES)
    workflows += sum((p / "workflow.yaml").is_file() for p in (root / "workflows").glob("*")
                     if p.is_dir() and not p.name.startswith("_") and p.name != "bin")
    return {"skills": len(list(layout.iter_skill_md(root))), "tools": len(tools),
            "workflows": workflows, "papers": len(identities), "dois": len(dois)}
