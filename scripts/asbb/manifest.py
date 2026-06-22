"""Track asbb install placements in ~/.asbb/installed.json."""
from __future__ import annotations

import json
from pathlib import Path


def manifest_path(home: Path) -> Path:
    return Path(home) / ".asbb" / "installed.json"


def load(home: Path) -> dict:
    p = manifest_path(home)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def save(home: Path, data: dict) -> None:
    p = manifest_path(home)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def record(home, slug, runtime, dest_root, entries, mode) -> None:
    data = load(home)
    data.setdefault(slug, {})[runtime] = {
        "dest_root": str(dest_root),
        "entries": [str(e) for e in entries],
        "mode": mode,
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
