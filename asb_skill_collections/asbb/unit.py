"""Snapshot the distributable contents of one marketplace source unit."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import yaml

PUBLIC_HIDDEN_NAMES = {".claude-plugin", ".zenodo.json"}
LOCAL_NAMES = {"__pycache__", "proposals", "outputs"}


def _is_distributable(path: Path) -> bool:
    return (not path.name.startswith(".") or path.name in PUBLIC_HIDDEN_NAMES) and (
        path.name not in LOCAL_NAMES and path.suffix not in {".pyc", ".pyo"}
    )


def unit_files(root: Path) -> list[Path]:
    """List distributable relative paths, rejecting links and special files.

    Local hidden content, bytecode, proposals and outputs are excluded at every
    depth. Links are refused rather than copying a dependency outside the unit.
    Directories are included so empty published directories survive a copy.
    """
    paths = []
    for child in sorted(root.iterdir()):
        if not _is_distributable(child):
            continue
        if child.is_symlink() or not (child.is_dir() or child.is_file()):
            raise ValueError(f"refusing non-regular unit asset: {child}")
        paths.append(Path(child.name))
        if child.is_dir():
            paths.extend(Path(child.name) / rel for rel in unit_files(child))
    return paths


def unit_digest(root: Path, paths: list[Path]) -> str:
    """Return a SHA256 over relative names, entry types and file content hashes."""
    records = []
    for rel in paths:
        path = root / rel
        digest = None
        if path.is_file():
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
        records.append([rel.as_posix(), digest])
    return hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()


def copy_unit(root: Path, destination: Path, paths: list[Path]) -> None:
    """Copy a previously inspected unit inventory into a new destination."""
    destination.mkdir(parents=True)
    for rel in paths:
        source = root / rel
        if source.is_dir():
            (destination / rel).mkdir()
        else:
            shutil.copy2(source, destination / rel)


def unit_version(root: Path, fallback=None) -> str | None:
    """Read a collection or plugin version, falling back to the marketplace."""
    for rel in ("collection.yaml", ".claude-plugin/plugin.json"):
        path = root / rel
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"refusing linked source metadata: {path}")
        if path.is_file():
            metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(metadata, dict) and metadata.get("version") is not None:
                return str(metadata["version"])
    return str(fallback) if fallback is not None else None


def adapter_body(unit_rel: str, name: str) -> str:
    """Describe a relocatable asset root relative to the host-facing file."""
    return (
        f"Collection root: `{unit_rel}` (relative to this instruction file).\n\n"
        f"Read `{unit_rel}/skills/{name}/SKILL.md` and follow it. "
        "Resolve collection paths and run its commands from that collection root, "
        "regardless of the current working directory. Bundled executables are in "
        "`bin/`; use those for checkout-only `scripts/` examples.\n\n"
    )
