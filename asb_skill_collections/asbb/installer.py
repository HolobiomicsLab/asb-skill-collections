"""Install/uninstall complete units and their small runtime advertisements."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import yaml

from . import manifest
from .repo import PackRef, iter_skill_dirs
from .skillmd import parse_skill_md
from .targets import InstallOpts, Target
from .unit import adapter_body, copy_unit, unit_digest, unit_files


def _resolve(root: Path, rel: str, link_target: str | None = None) -> Path:
    """Validate one placement without following a link during deletion.

    Parent symlink escapes are always rejected. A final external symlink is
    allowed only when it matches its recorded install-time target; callers
    unlink that entry, never operate through it.
    """
    root = Path(root).resolve()
    if not isinstance(rel, str) or not rel or "\0" in rel:
        raise ValueError(f"refusing invalid managed entry: {rel!r}")
    path = Path(rel)
    if path.is_absolute() or not path.parts or ".." in path.parts or str(path) != rel:
        raise ValueError(f"refusing invalid managed entry: {rel!r}")
    final = root / path
    if not final.parent.resolve().is_relative_to(root):
        raise ValueError(f"refusing path outside {root}: {final}")
    if final.is_symlink() and os.readlink(final) == link_target:
        return final
    if not final.resolve().is_relative_to(root):
        raise ValueError(f"refusing path outside {root}: {final}")
    return final


def _record_paths(root: Path, record: dict | None) -> dict[str, Path]:
    if record is None:
        return {}
    if record.get("dest_root") != str(root):
        raise ValueError("refusing changed destination; uninstall from the recorded root first")
    entries = record.get("entries")
    links = record.get("symlinks", {}) if record.get("mode") == "symlink" else {}
    if not isinstance(entries, list) or not isinstance(links, dict):
        raise ValueError("refusing malformed install record")
    return {rel: _resolve(root, rel, links.get(rel) if isinstance(rel, str) else None)
            for rel in entries}


def _remove_existing(p: Path) -> None:
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)


def _plan(pack: PackRef, target: Target, opts: InstallOpts) -> list[tuple]:
    planned = []
    copied = opts.copy or target.kind == "rules"
    unit_rel = f".asbb-units/{pack.slug}"
    if copied:
        planned.append((unit_rel, "unit", pack.unit_dir))
    for directory in iter_skill_dirs(pack):
        name = directory.name
        if not copied:
            planned.append((name, "link", directory))
            continue
        fm, body = parse_skill_md(directory / "SKILL.md")
        if target.kind == "skill":
            text = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\n"
            planned.append((name, "adapter", text + adapter_body(f"../{unit_rel}", name)))
        else:
            text = adapter_body(unit_rel, name) + body
            planned.append((target.filename(name), "file", target.render(fm, text, name)))
    return planned


def _check_collisions(finals: list[tuple], previous: dict, opts: InstallOpts) -> None:
    for final, rel, _kind, _payload in finals:
        if (final.exists() or final.is_symlink()) and rel not in previous and not opts.force:
            raise FileExistsError(
                f"{final} exists and is not managed by asbb; use --force to overwrite")


def _check_plan(finals: list[tuple]) -> None:
    seen = set()
    for final, _rel, _kind, _payload in finals:
        if any(final == other or final in other.parents or other in final.parents
               for other in seen):
            raise ValueError(f"refusing overlapping planned destinations: {final}")
        seen.add(final)


def _check_ownership(home: Path, owner: tuple[str, str], paths: list[Path]) -> None:
    for slug, runtimes in manifest.load(home).items():
        for runtime, record in runtimes.items():
            if (slug, runtime) == owner:
                continue
            root = Path(record["dest_root"])
            for rel in record["entries"]:
                other = root / rel
                # Ownership reserves links, never their targets.
                link = os.readlink(other) if other.is_symlink() else None
                other = _resolve(root, rel, link)
                if any(path == other or path in other.parents or other in path.parents
                       for path in paths):
                    raise ValueError(f"refusing entry owned by {slug}/{runtime}: {other}")


def _write_entry(final: Path, kind: str, payload) -> None:
    _remove_existing(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    if kind == "link":
        os.symlink(payload, final, target_is_directory=True)
    elif kind == "adapter":
        final.mkdir()
        (final / "SKILL.md").write_text(payload, encoding="utf-8")
    else:
        final.write_text(payload, encoding="utf-8")


def install(pack: PackRef, target: Target, opts: InstallOpts) -> list[str]:
    """Install or sync a pack, validating every placement before any mutation."""
    dest_root = target.dest(opts).resolve()
    source_root = pack.unit_dir.resolve()
    if dest_root.is_relative_to(source_root) or source_root.is_relative_to(dest_root):
        raise ValueError("refusing overlapping source unit and destination")
    prev = manifest.get(opts.home, pack.slug, target.id)
    previous = _record_paths(dest_root, prev)
    paths = unit_files(source_root)
    planned = _plan(pack, target, opts)
    links = prev.get("symlinks", {}) if prev and prev.get("mode") == "symlink" else {}
    finals = [(_resolve(dest_root, rel, links.get(rel)), rel, kind, payload)
              for rel, kind, payload in planned]
    _check_plan(finals)
    _check_ownership(opts.home, (pack.slug, target.id),
                     list(previous.values()) + [row[0] for row in finals])
    _check_collisions(finals, previous, opts)
    source = {"path": pack.source, "version": pack.version,
              "sha256": unit_digest(pack.unit_dir, paths)}
    written = [rel for _final, rel, _kind, _payload in finals]
    stale = {rel: path for rel, path in previous.items() if rel not in written}
    if opts.dry_run:
        for final, _rel, _kind, _payload in finals:
            print(f"would write {final}")
        for path in stale.values():
            print(f"would remove {path}")
        return written
    for final, _rel, kind, payload in finals:
        if kind == "unit":
            _remove_existing(final)
            copy_unit(payload, final, paths)
        else:
            _write_entry(final, kind, payload)
    for path in stale.values():
        _remove_existing(path)
    mode = "render" if target.kind == "rules" else ("copy" if opts.copy else "symlink")
    symlinks = {rel: str(payload) for rel, kind, payload in planned if kind == "link"}
    manifest.record(opts.home, pack.slug, target.id, dest_root, written, mode,
                    source=source, symlinks=symlinks)
    return written


def uninstall(slug: str, target: Target, opts: InstallOpts) -> list[str]:
    """Remove recorded entries after validating the whole record; honor dry-run."""
    record = manifest.get(opts.home, slug, target.id)
    if not record:
        return []
    root = target.dest(opts).resolve()
    paths = _record_paths(root, record)
    _check_ownership(opts.home, (slug, target.id), list(paths.values()))
    if opts.dry_run:
        for path in paths.values():
            print(f"would remove {path}")
        return list(paths)
    for path in paths.values():
        _remove_existing(path)
    manifest.remove(opts.home, slug, target.id)
    return list(paths)
