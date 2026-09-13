"""Install complete units and remove only contained, unchanged, owned entries."""

from __future__ import annotations

import os
import json
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath

import yaml

from . import manifest
from .paths import recorded_root, resolve_within as _resolve
from .repo import PackRef, iter_skill_dirs
from .skillmd import parse_skill_md
from .targets import InstallOpts, Target
from .units import (
    ENTRIES_DIR,
    RECEIPT_FILE,
    UNITS_DIR,
    bind_body,
    content_identity,
    copy_assets,
    digest_assets,
    inventory,
    unit_relative,
)


def _remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _report_skip(path, reason):
    print(f"asbb: skipped {path}: {reason}", file=sys.stderr)


def _absent(final) -> bool:
    """Report whether nothing at all occupies an entry's destination path.

    An entry that is already gone is already cleaned: there is nothing to
    validate ownership of and nothing to remove. Validating first was the old
    behaviour and it failed twice over, because :func:`_owned_entry` reads the
    unit receipt that a deleted destination took with it. Every entry then
    raised ``FileNotFoundError`` and was reported as a skip — and since a
    skipped entry stays in ``entries``, the snapshot was retained forever, so
    *every later install of that pack* reprinted the same errors naming a
    directory the user no longer has.

    A broken symlink is not absent. It occupies the name, it is ours to remove
    if we own it, and reading it through ``exists()`` alone would silently
    abandon a dangling link the installer placed.
    """
    return not final.exists() and not final.is_symlink()


def _unit_identity(rec, slug, runtime):
    return {
        **{key: rec[key] for key in ("dest_root", "unit", "version", "source_digest")},
        "pack": slug,
        "runtime": runtime,
    }


def _recorded_unit(rec, slug, runtime, *, allow_missing=False, root=None):
    """Return the record's unit, by default beneath the root it records.

    ``root`` overrides only *where to look*, never *what counts*: the receipt is
    still compared against the identity the record states, recorded root
    included. That is deliberate. A unit that was moved carries its receipt
    unchanged, so the receipt keeps naming the root it was installed into even
    though it no longer sits there — matching it is how a moved unit is
    recognised as the same unit, and refusing to relax it is how a *copy*, whose
    original is still in place, stays unclaimable.
    """
    root = recorded_root(rec["dest_root"]) if root is None else root
    expected = unit_relative(slug, runtime, rec["version"], rec["source_digest"])
    if rec["unit"] != expected:
        raise ValueError("unit path does not match its recorded owner and revision")
    unit = _resolve(root, expected)
    if unit.resolve() != unit:
        raise ValueError(f"unit path follows a symlink: {unit}")
    if not unit.exists() and allow_missing:
        return unit
    marker = _resolve(unit, RECEIPT_FILE)
    if json.loads(marker.read_text()) != _unit_identity(rec, slug, runtime):
        raise ValueError("unit receipt does not match its recorded location and owner")
    return unit


def _owned_entry(rec, slug, runtime, rel, *, root=None):
    root = recorded_root(rec["dest_root"]) if root is None else root
    final = _resolve(root, rel)
    unit = _recorded_unit(rec, slug, runtime, root=root)
    owner = rec.get("entry_owners", {}).get(rel, {})
    if (owner.get("pack"), owner.get("runtime"), owner.get("version")) != (
        slug,
        runtime,
        rec["version"],
    ) or owner.get("unit") != rec["unit"]:
        raise ValueError(
            "entry has no matching ownership receipt; reinstall to adopt it"
        )
    expected = _resolve(unit, f"{ENTRIES_DIR}/{rel}")
    if not expected.exists() or content_identity(expected) != owner["sha256"]:
        raise ValueError("entry no longer has matching content in its own unit")
    if final.is_symlink():
        if rec["mode"] != "symlink" or final.resolve() != expected:
            raise ValueError("entry no longer resolves into its own unit")
    elif rec["mode"] == "symlink" and final.exists():
        raise ValueError("managed symlink was replaced")
    if final.exists() and content_identity(final) != owner["sha256"]:
        raise ValueError("entry content changed since installation")
    return final


def _holds_unit(rec, slug, runtime, root) -> bool:
    try:
        _recorded_unit(rec, slug, runtime, root=root)
    except (KeyError, ValueError, OSError):
        return False
    return True


def _moved_root(rec, slug, runtime, candidate):
    """Return the root an installation was moved to, when the move is provable.

    An installed unit that is moved on disk takes its receipt with it, so the
    receipt still names the root it was installed into while the unit itself now
    sits under ``candidate``. Record, receipt and candidate then agree on pack,
    runtime, revision and unit path, and only the location differs — which is
    what makes the moved unit the *same* unit rather than a lookalike.

    Two conditions are load-bearing. The candidate is only ever the directory the
    caller named, never one read back out of a receipt, so no planted file can
    nominate what the installer operates on. And the recorded root must have
    stopped holding the unit: a copy leaves its original in place and therefore
    never qualifies, which is what keeps a byte-identical backup from being
    claimed and deleted.

    Returns None when there is no such proof, leaving every caller on the
    recorded root and the existing refusals intact. Detecting the move and
    writing the new root back into the manifest is a separate concern.
    """
    if not rec or candidate is None:
        return None
    try:
        recorded = recorded_root(rec["dest_root"])
    except (KeyError, TypeError, ValueError):
        return None
    if candidate == recorded or _holds_unit(rec, slug, runtime, recorded):
        return None
    return candidate if _holds_unit(rec, slug, runtime, candidate) else None


def _other_claims(home, slug, runtime, root, rel):
    return any(
        (owner, rid) != (slug, runtime)
        and placement.get("dest_root") == str(root)
        and rel in placement.get("entries", ())
        for owner, runtimes in manifest.load(home).items()
        for rid, rec in runtimes.items()
        for placement in (rec, *rec.get("retained_units", ()))
    )


def _overlapping(rel, other):
    """Report whether two destination-relative entry paths claim the same tree."""
    parts, others = PurePosixPath(rel).parts, PurePosixPath(other).parts
    return parts[: len(others)] == others or others[: len(parts)] == parts


def _plan_entries(pack, target, root, unit, assets):
    planned = {}
    shipped = {rel for rel, _ in assets}
    for directory in iter_skill_dirs(pack):
        name = directory.name
        if f"skills/{name}/SKILL.md" not in shipped:
            raise ValueError(
                f"advertised entry is excluded from the source snapshot: {name}"
            )
        rel = name if target.kind == "skill" else target.filename(name)
        if rel in (UNITS_DIR, ENTRIES_DIR):
            raise ValueError(f"entry name is reserved for installer state: {rel}")
        # Two advertised skills reaching the same destination path would leave
        # the dict holding one of them: the other is dropped without a word, and
        # a nested pair only surfaces as a FileExistsError once staging is under
        # way. Refuse the whole plan while nothing has been written.
        clash = next((other for other in planned if _overlapping(rel, other)), None)
        if clash is not None:
            raise ValueError(
                f"entry {name} resolves to {rel}, which overlaps the destination "
                f"{clash} already planned for this install"
            )
        fm, body = parse_skill_md(directory / "SKILL.md")
        entry_file = _resolve(root, rel)
        if target.kind == "skill":
            entry_file = entry_file / "SKILL.md"
        body = bind_body(body, unit, f"skills/{name}/SKILL.md", entry_file)
        planned[rel] = (
            f"---\n{yaml.safe_dump(fm, sort_keys=False)}---\n\n{body}"
            if target.kind == "skill"
            else target.render(fm, body, name)
        )
    return planned


def _check_conflicts(pack, target, opts, rec, planned, moved=None):
    root = target.dest(opts).resolve()
    for rel in planned:
        final = _resolve(root, rel)
        if not final.exists() and not final.is_symlink():
            continue
        owned = False
        here = bool(rec) and (rec.get("dest_root") == str(root) or moved == root)
        if here and rel in rec.get("entries", ()):
            try:
                # Competing claims are compared against the root every record
                # names, not the one this installation was moved to: a pack that
                # travelled alongside this one still records the old root.
                _owned_entry(rec, pack.slug, target.id, rel, root=root)
                owned = not _other_claims(
                    opts.home,
                    pack.slug,
                    target.id,
                    recorded_root(rec["dest_root"]),
                    rel,
                )
            except (KeyError, ValueError, OSError):
                pass
        if not owned and not opts.force:
            raise FileExistsError(
                f"{final} exists and is not owned by this pack; use --force to overwrite"
            )


def _write_unit(stage, assets, planned, target, identity):
    copy_assets(assets, stage)
    if digest_assets(inventory(stage)) != identity["source_digest"]:
        raise ValueError("source changed while its installed snapshot was being copied")
    _resolve(stage, RECEIPT_FILE).write_text(
        json.dumps(identity, sort_keys=True) + "\n"
    )
    for rel, text in planned.items():
        entry = _resolve(stage, f"{ENTRIES_DIR}/{rel}")
        if target.kind == "skill":
            entry = entry / "SKILL.md"
        entry.parent.mkdir(parents=True, exist_ok=True)
        entry.write_text(text, encoding="utf-8")


def _materialise_unit(unit, assets, planned, target, previous, identity, moved=None):
    if unit.exists():
        try:
            owned = (
                previous
                and _recorded_unit(
                    previous,
                    identity["pack"],
                    identity["runtime"],
                    root=moved,
                )
                == unit
            )
            owned = owned and content_identity(unit) == previous["unit_digest"]
        except (KeyError, ValueError, OSError):
            owned = False
        if not owned:
            raise FileExistsError(
                f"refusing to replace unowned or modified unit: {unit}"
            )
    unit.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".staging-", dir=unit.parent))
    try:
        _write_unit(stage, assets, planned, target, identity)
        if unit.exists():
            _remove_existing(unit)
        stage.rename(unit)
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def _place_entries(root, unit, planned, target, opts):
    owners = {}
    for rel in planned:
        final = _resolve(root, rel)
        source = _resolve(unit, f"{ENTRIES_DIR}/{rel}")
        _remove_existing(final)
        if target.kind == "rules":
            shutil.copy2(source, final)
        elif opts.copy:
            shutil.copytree(source, final)
        else:
            final.symlink_to(
                os.path.relpath(source, final.parent), target_is_directory=True
            )
        owners[rel] = {"sha256": content_identity(source)}
    return owners


def _clean_entries(rec, slug, runtime, entries, home, *, root=None):
    removed = []
    for rel in entries:
        try:
            recorded = recorded_root(rec["dest_root"])
            actual = recorded if root is None else root
            if not _absent(_resolve(actual, rel)):
                final = _owned_entry(rec, slug, runtime, rel, root=actual)
                # Competing claims are still read against the recorded root: a
                # pack that moved alongside this one records that same root.
                if _other_claims(home, slug, runtime, recorded, rel):
                    raise ValueError("another installed pack claims this entry")
                _remove_existing(final)
            removed.append(rel)
        except (KeyError, ValueError, OSError, RuntimeError) as exc:
            _report_skip(rel, str(exc))
    return removed


def _clean_unit(rec, slug, runtime, *, root=None):
    try:
        unit = _recorded_unit(rec, slug, runtime, allow_missing=True, root=root)
        if not unit.exists():
            return True
        if content_identity(unit) != rec["unit_digest"]:
            raise ValueError("unit content changed since installation")
        _remove_existing(unit)
        if unit.parent.is_dir() and not any(unit.parent.iterdir()):
            unit.parent.rmdir()
        return True
    except (KeyError, ValueError, OSError, RuntimeError) as exc:
        _report_skip(rec.get("unit", "legacy unit"), str(exc))
        return False


def _clean_snapshot(rec, slug, runtime, home, *, root=None):
    removed = _clean_entries(
        rec, slug, runtime, rec.get("entries", ()), home, root=root
    )
    remaining = {key: value for key, value in rec.items() if key != "retained_units"}
    remaining["entries"] = [rel for rel in rec.get("entries", ()) if rel not in removed]
    if not remaining["entries"] and _clean_unit(rec, slug, runtime, root=root):
        return None, removed
    return remaining, removed


def _clean_previous(previous, current, home):
    """Retire what the superseded record still owns, at the root it records.

    No relocation here, on purpose. The superseded record names the place this
    installation was moved *from*; pointing its cleanup at where the unit is now
    would aim it straight at the entries this install has just written.
    """
    if not previous:
        return []
    snapshots = list(previous.get("retained_units", ()))
    if (previous.get("dest_root"), previous.get("unit")) != (
        current["dest_root"],
        current["unit"],
    ):
        stale = dict(previous)
        if previous.get("dest_root") == current["dest_root"]:
            stale["entries"] = [
                rel
                for rel in previous.get("entries", ())
                if rel not in current["entries"]
            ]
        snapshots.append(stale)
    else:
        stale = set(previous.get("entries", ())) - set(current["entries"])
        _clean_entries(previous, current["pack"], current["runtime"], stale, home)
    retained = []
    for snapshot in snapshots:
        pending, _ = _clean_snapshot(
            snapshot, current["pack"], current["runtime"], home
        )
        if pending:
            retained.append(pending)
    return retained


def install(pack: PackRef, target: Target, opts: InstallOpts) -> list[str]:
    """Install one complete snapshot and its advertised entries; return entry names."""
    root = target.dest(opts).resolve()
    previous = manifest.get(opts.home, pack.slug, target.id)
    source_root = pack.source_dir.resolve()
    if root == source_root or source_root in root.parents:
        raise ValueError("destination cannot be inside its source pack")
    if root in source_root.parents:
        # The reverse containment is the same hazard read the other way: entries
        # are placed by removing whatever occupies their name, so a destination
        # holding the pack can delete the source it is still reading.
        raise ValueError("destination cannot contain its source pack")
    assets = inventory(pack.source_dir, source=True)
    if any(
        Path(rel).parts[0] in (ENTRIES_DIR, UNITS_DIR, RECEIPT_FILE)
        for rel, _ in assets
    ):
        raise ValueError("pack contains reserved installer directories")
    source_digest = digest_assets(assets)
    unit_rel = unit_relative(pack.slug, target.id, pack.version, source_digest)
    unit = _resolve(root, unit_rel)
    if unit.resolve() != unit:
        raise ValueError(f"unit path follows a symlink: {unit}")
    planned = _plan_entries(pack, target, root, unit, assets)
    # Only an explicitly named destination states where an installation is now;
    # without one the record remains the sole statement, as uninstall documents.
    moved = (
        _moved_root(previous, pack.slug, target.id, root)
        if opts.dest_override is not None
        else None
    )
    _check_conflicts(pack, target, opts, previous, planned, moved)
    if opts.dry_run:
        print(f"would copy complete unit to {unit}")
        for rel in planned:
            print(f"would write {_resolve(root, rel)}")
        return list(planned)
    identity = dict(
        dest_root=str(root),
        unit=unit_rel,
        version=pack.version,
        source_digest=source_digest,
        pack=pack.slug,
        runtime=target.id,
    )
    _materialise_unit(unit, assets, planned, target, previous, identity, moved)
    owners = _place_entries(root, unit, planned, target, opts)
    retained = _clean_previous(
        previous, {**identity, "entries": list(planned)}, opts.home
    )
    for owner in owners.values():
        owner.update(
            pack=pack.slug, runtime=target.id, version=pack.version, unit=unit_rel
        )
    mode = "render" if target.kind == "rules" else ("copy" if opts.copy else "symlink")
    manifest.record(
        opts.home,
        pack.slug,
        target.id,
        root,
        list(planned),
        mode,
        version=pack.version,
        source=pack.source,
        source_digest=source_digest,
        unit=unit_rel,
        unit_digest=content_identity(unit),
        entry_owners=owners,
        retained_units=retained,
    )
    return list(planned)


def uninstall(slug: str, target: Target, opts: InstallOpts) -> list[str]:
    """Remove unchanged owned entries and their unit, reporting every refused path."""
    rec = manifest.get(opts.home, slug, target.id)
    if not rec:
        return []
    moved = None
    if opts.dest_override is not None:
        # --dest names the directory to operate on. When the record contradicts
        # it, the command is ambiguous: refuse rather than empty the other one —
        # unless the directory named holds the very unit the record placed, and
        # the recorded root no longer does. That is an installation that was
        # moved wholesale, and refusing it left no way to remove one at all.
        # Without --dest the record is the only statement of where to look, and
        # each entry is validated against it below.
        root = target.dest(opts).resolve()
        moved = _moved_root(rec, slug, target.id, root)
        if rec.get("dest_root") != str(root) and moved != root:
            raise ValueError(
                f"{slug} is installed at {rec.get('dest_root')}, not at {root}; "
                "uninstall it from the destination it was installed into"
            )
    active, removed = _clean_snapshot(rec, slug, target.id, opts.home, root=moved)
    retained = []
    for snapshot in rec.get("retained_units", ()):
        pending, cleaned = _clean_snapshot(
            snapshot,
            slug,
            target.id,
            opts.home,
            root=_moved_root(snapshot, slug, target.id, moved) if moved else None,
        )
        removed.extend(rel for rel in cleaned if rel not in removed)
        if pending:
            retained.append(pending)
    if not active and not retained:
        manifest.remove(opts.home, slug, target.id)
    else:
        data = manifest.load(opts.home)
        data[slug][target.id] = active or {**rec, "entries": []}
        data[slug][target.id]["retained_units"] = retained
        manifest.save(opts.home, data)
    return removed
