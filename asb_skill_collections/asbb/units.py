"""Copy complete pack snapshots and bind host entries to their asset root."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from .paths import resolve_within

UNITS_DIR = ".asbb-units"
ENTRIES_DIR = ".asbb-entries"
RECEIPT_FILE = ".asbb-unit.json"

#: The installed asset root, written into every bound entry. The absolute form
#: is what readers have always looked for; the relative form is the same
#: directory seen from the entry's own directory, and is the only one of the two
#: that survives the installation being moved on disk.
ABSOLUTE_MARKER = re.compile(r"<!-- asbb-unit: (.+?) -->")
RELATIVE_MARKER = re.compile(r"<!-- asbb-unit-relative: (.+?) -->")
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


def entry_relative_unit(unit: Path, entry_dir: Path) -> str:
    """Return the unit as seen from the directory holding one bound entry.

    Skill-native entries are directories beside ``.asbb-units``, so the unit is
    one hop up; rules entries are files in the destination itself, so it is not.
    The depth is derived, never assumed: a fixed ``../`` would miss one of the
    two by exactly one directory, and miss it silently.
    """
    return Path(os.path.relpath(Path(unit), Path(entry_dir))).as_posix()


def bind_body(body: str, unit: Path, source_entry: str, entry_file: Path) -> str:
    """Prefix instructions with the installed working directory and original entry.

    Two markers are written, not one. The absolute path is what every reader has
    always looked for and it is exact while nothing has moved — but it is also
    the single fact that stops being true the moment the installation is moved on
    disk, and a moved install used to leave its own documented first step naming
    a directory that no longer exists. The relative marker is the same unit seen
    from this entry's own directory, so it survives any move of the install root.
    Readers resolve the relative marker against the directory they read the entry
    from and fall back to the absolute one; see :func:`unit_from_entry`.
    """
    import shlex

    relative = entry_relative_unit(unit, Path(entry_file).parent)
    return (
        f"<!-- asbb-unit: {json.dumps(str(unit))} -->\n"
        f"<!-- asbb-unit-relative: {json.dumps(relative)} -->\n"
        "## Installed pack location\n\n"
        f"This pack's asset root is `{relative}`, resolved against the directory "
        "holding this file. That is the form to prefer: it stays correct if this "
        f"installation is moved. While it has not moved it is `{unit}`. Resolve "
        "pack-relative paths there, including indexes, leaves and helper scripts. "
        "Before running the commands below, change the working directory in the "
        "same shell — set `ENTRY` to the path you read this file from, which is "
        "the line below unless the installation has moved:\n\n"
        f"```sh\nENTRY={shlex.quote(str(entry_file))}\n"
        f'cd -- "$(dirname -- "$ENTRY")/{relative}"\n```\n\n'
        f"The original entry is `{source_entry}` beneath that root; resolve "
        "entry-local supporting files beside that file.\n\n"
        f"{body}"
    )


def _marker(text: str, pattern) -> str | None:
    """Return one marker's decoded path, or None when it is absent or unreadable."""
    found = pattern.search(text)
    if not found:
        return None
    try:
        value = json.loads(found[1])
    except (json.JSONDecodeError, TypeError):
        return None
    return value if isinstance(value, str) and value else None


def _unit_candidates(entry: Path, text: str):
    relative = _marker(text, RELATIVE_MARKER)
    if relative:
        # The lexical parent, normalised without touching the filesystem. Under
        # the default symlink mode the host entry is a link into the unit, so
        # resolving it first would walk *inside* the unit and lose the
        # `.asbb-units` sibling that the relative path names.
        yield Path(os.path.normpath(Path(entry.parent) / relative))
    absolute = _marker(text, ABSOLUTE_MARKER)
    if absolute:
        yield Path(absolute)
    # Last resort, for a reader that resolved the entry's symlink before reading
    # it: that reader is standing inside the unit already, where neither marker
    # points back at it. The unit is then the nearest ancestor carrying a receipt.
    try:
        physical = entry.resolve(strict=True)
    except (OSError, RuntimeError):
        return
    yield from physical.parents


def unit_from_entry(entry: Path) -> Path | None:
    """Locate an installed entry's asset root from the entry's own markers.

    Candidates are tried in order and the first one that is actually an
    installed unit — proved by its receipt, not by existing — wins. Returns None
    when the entry carries no marker, or when every path it names is gone.
    """
    entry = Path(entry)
    try:
        text = entry.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for candidate in _unit_candidates(entry, text):
        try:
            if (candidate / RECEIPT_FILE).is_file():
                return candidate
        except OSError:
            continue
    return None
