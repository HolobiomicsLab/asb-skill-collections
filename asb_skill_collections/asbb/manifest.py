"""Track asbb install placements in ~/.asbb/installed.json."""

from __future__ import annotations

import json
from pathlib import Path

from .paths import resolve_within


def manifest_path(home: Path) -> Path:
    """Return the state path only when its existing links remain inside home."""
    return resolve_within(home, ".asbb/installed.json")


def load(home: Path) -> dict:
    p = manifest_path(home)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def save(home: Path, data: dict) -> None:
    p = manifest_path(home)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _transfer_entries(rec, dest_root, entries, owner):
    if rec.get("dest_root") != str(dest_root):
        return
    claimed = set(rec.get("entries", ())) & set(entries)
    rec["entries"] = [entry for entry in rec.get("entries", ()) if entry not in claimed]
    for entry in claimed:
        rec.get("entry_owners", {}).pop(entry, None)
        rec.setdefault("displaced_entries", {})[entry] = dict(owner)


def record(home, slug, runtime, dest_root, entries, mode, **details) -> None:
    """Record a placement and transfer overlapping entry claims to its new owner."""
    data = load(home)
    if details.get("entry_owners"):
        new_owner = {"pack": slug, "runtime": runtime, "version": details["version"]}
        for owner, runtimes in data.items():
            for owner_runtime, rec in runtimes.items():
                if (owner, owner_runtime) == (slug, runtime):
                    continue
                for placement in (rec, *rec.get("retained_units", ())):
                    _transfer_entries(placement, dest_root, entries, new_owner)
        for placement in details.get("retained_units", ()):
            _transfer_entries(placement, dest_root, entries, new_owner)
    data.setdefault(slug, {})[runtime] = {
        "dest_root": str(dest_root),
        "entries": [str(e) for e in entries],
        "mode": mode,
        **details,
    }
    save(home, data)


def get(home, slug, runtime):
    return load(home).get(slug, {}).get(runtime)


def remove(home, slug, runtime) -> None:
    data = load(home)
    if slug in data and runtime in data[slug]:
        del data[slug][runtime]
        if not data[slug]:
            del data[slug]
        save(home, data)
