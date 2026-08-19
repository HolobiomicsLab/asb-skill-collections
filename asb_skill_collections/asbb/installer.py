"""Install/uninstall packs into runtime targets (symlink/copy/render)."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from . import manifest
from .repo import PackRef, iter_skill_dirs
from .skillmd import parse_skill_md
from .targets import InstallOpts, Target


def _resolve(root: Path, rel: str) -> Path:
    root = Path(root).resolve()
    # Use Path(...) without .resolve() to avoid following existing symlinks,
    # but normalise away any ".." components via os.path.normpath.
    final = Path(os.path.normpath(root / rel))
    if final != root and root not in final.parents:
        raise ValueError(f"refusing to write outside {root}: {final}")
    return final


def _remove_existing(p: Path) -> None:
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.is_dir():
        shutil.rmtree(p)


def install(pack: PackRef, target: Target, opts: InstallOpts) -> list[str]:
    dest_root = target.dest(opts)
    prev = manifest.get(opts.home, pack.slug, target.id)
    prev_entries = set(prev["entries"]) if prev else set()

    # Build the plan: (rel, kind, payload)
    planned = []
    for sd in iter_skill_dirs(pack):
        name = sd.name
        if target.kind == "skill":
            planned.append((name, "dir", sd))
        else:
            fm, body = parse_skill_md(sd / "SKILL.md")
            rel = target.filename(name)
            planned.append((rel, "file", target.render(fm, body, name)))

    # Conflict check (unmanaged existing path => needs --force)
    finals = [(_resolve(dest_root, rel), rel, kind, payload)
              for rel, kind, payload in planned]
    for final, rel, _kind, _payload in finals:
        if (final.exists() or final.is_symlink()) and \
                rel not in prev_entries and not opts.force:
            raise FileExistsError(
                f"{final} exists and is not managed by asbb; use --force to overwrite")

    if opts.dry_run:
        for final, rel, _kind, _payload in finals:
            print(f"would write {final}")
        return [rel for _f, rel, _k, _p in finals]

    Path(dest_root).mkdir(parents=True, exist_ok=True)
    written = []
    for final, rel, kind, payload in finals:
        _remove_existing(final)
        final.parent.mkdir(parents=True, exist_ok=True)
        if kind == "dir":
            if opts.copy:
                shutil.copytree(payload, final)
            else:
                os.symlink(payload, final, target_is_directory=True)
        else:
            final.write_text(payload, encoding="utf-8")
        written.append(rel)

    # Drop stale entries from a prior install that are no longer produced.
    for rel in prev_entries - set(written):
        _remove_existing(_resolve(dest_root, rel))

    mode = "render" if target.kind == "rules" else ("copy" if opts.copy else "symlink")
    manifest.record(opts.home, pack.slug, target.id, dest_root, written, mode)
    return written


def uninstall(slug: str, target: Target, opts: InstallOpts) -> list[str]:
    rec = manifest.get(opts.home, slug, target.id)
    if not rec:
        return []
    dest_root = Path(rec["dest_root"])
    removed = []
    for rel in rec["entries"]:
        _remove_existing(dest_root / rel)
        removed.append(rel)
    manifest.remove(opts.home, slug, target.id)
    return removed
