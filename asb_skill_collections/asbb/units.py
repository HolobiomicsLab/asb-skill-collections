"""Copy complete pack snapshots and bind host entries to their asset root."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from .paths import resolve_within

UNITS_DIR = ".asbb-units"
ENTRIES_DIR = ".asbb-entries"
RECEIPT_FILE = ".asbb-unit.json"
LOCAL_STATE = frozenset(
    {".git", ".cache", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}
)


def _walk(root, directory, ancestors, excluded):
    actual = directory.resolve()
    if actual in ancestors:
        raise ValueError(f"cyclic source directory: {directory}")
    for child in sorted(directory.iterdir()):
        if child.name in excluded:
            continue
        rel = child.relative_to(root).as_posix()
        path = resolve_within(root, rel)
        if excluded and set(path.resolve().relative_to(root).parts) & set(excluded):
            raise ValueError(f"source alias reaches excluded local state: {path}")
        if not path.is_dir() and not path.is_file():
            raise ValueError(f"unsupported or missing pack asset: {path}")
        yield rel, path
        if path.is_dir():
            yield from _walk(root, path, ancestors | {actual}, excluded)


def inventory(root: Path, *, source=False) -> list[tuple[str, Path]]:
    """List contained assets, materialising internal links and excluding local caches."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"pack directory does not exist: {root}")
    return list(_walk(root, root, set(), LOCAL_STATE if source else ()))


def _hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_assets(assets: list[tuple[str, Path]]) -> str:
    """Hash asset paths, directory shape, executable bits and file bytes."""
    rows = [
        (rel, "dir")
        if path.is_dir()
        else (rel, path.stat().st_mode & 0o111, _hash_file(path))
        for rel, path in assets
    ]
    return hashlib.sha256(json.dumps(rows, ensure_ascii=True).encode()).hexdigest()


def content_identity(path: Path) -> str:
    """Return a content identity for a file or complete contained directory."""
    if path.is_dir():
        return digest_assets(inventory(path))
    if not path.is_file():
        raise ValueError(f"unsupported or missing installed entry: {path}")
    return digest_assets([("", path)])


def unit_relative(slug, runtime, version, source_digest) -> str:
    """Derive a bounded, traversal-free name for one pack/runtime revision."""
    identity = json.dumps([slug, runtime, version, source_digest]).encode()
    return f"{UNITS_DIR}/{hashlib.sha256(identity).hexdigest()}"


def copy_assets(assets, destination):
    """Materialise the validated source inventory without links back to its checkout."""
    for rel, source in assets:
        final = resolve_within(destination, rel)
        if source.is_dir():
            final.mkdir(parents=True, exist_ok=True)
        else:
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, final)


def bind_body(body: str, unit: Path, source_entry: str) -> str:
    """Prefix instructions with the installed working directory and original entry."""
    import shlex

    return (
        f"<!-- asbb-unit: {json.dumps(str(unit))} -->\n"
        "## Installed pack location\n\n"
        f"This pack's asset root is `{unit}`. Resolve pack-relative paths here, "
        "including indexes, leaves and helper scripts. Before running the commands "
        "below, change the working directory in the same shell:\n\n"
        f"```sh\ncd -- {shlex.quote(str(unit))}\n```\n\n"
        f"The original entry is `{unit / source_entry}`; resolve entry-local "
        "supporting files beside that file.\n\n"
        f"{body}"
    )
