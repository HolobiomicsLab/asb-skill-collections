"""Cross-collection check: the same tool carries the same licence everywhere.

Each collection resolves its tool records on its own, in its own context, so the
same name may legitimately resolve to two different tools in two collections.
The same *entity*, though, may not carry two licences. The entity is the address
the licence was read from (`license_evidence`: a registry package page or a
reviewed statement), and this check fails when one address carries two licences
or two tiers across the collections given.

It also reports, without failing, names that resolve to different entities in
different collections, for a reviewer to confirm that they are different tools.

Offline; reads only each collection's tool_licenses.json.

    python scripts/check_tool_licence_consistency.py <collection_dir> [...]
"""
from __future__ import annotations

import json
import pathlib
import sys

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p

    sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.tool_registry_sources import normalize


def _load(collection_dir) -> dict:
    path = pathlib.Path(collection_dir) / "tool_licenses.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check(collection_dirs) -> tuple[list[str], list[str]]:
    """(violations, notes) across the collections."""
    by_entity: dict[str, dict] = {}
    by_name: dict[str, dict] = {}
    for col in collection_dirs:
        label = str(col)
        tools_index = pathlib.Path(col) / "tools_index.json"
        names = {}
        if tools_index.is_file():
            names = {t["slug"]: t.get("name") for t in
                     json.loads(tools_index.read_text(encoding="utf-8"))}
        for slug, ev in _load(col).items():
            if ev.get("license_tier") in (None, "unknown"):
                continue
            entity = ev.get("license_evidence") or f"{ev.get('route')}:{ev.get('matched')}"
            reading = (ev.get("license"), ev.get("license_tier"))
            by_entity.setdefault(entity, {}).setdefault(reading, []).append(f"{label}:{slug}")
            key = normalize(names.get(slug) or slug)
            by_name.setdefault(key, {}).setdefault(entity, []).append(f"{label}:{slug}")
    violations = []
    for entity, readings in sorted(by_entity.items()):
        if len(readings) > 1:
            detail = "; ".join(f"{lic!r} ({tier}) in {', '.join(where)}"
                               for (lic, tier), where in sorted(readings.items(), key=str))
            violations.append(f"{entity}: {detail}")
    notes = []
    for key, entities in sorted(by_name.items()):
        if len(entities) > 1:
            detail = "; ".join(f"{e} in {', '.join(w)}" for e, w in sorted(entities.items()))
            notes.append(f"name {key!r} resolves to {len(entities)} entities: {detail}")
    return violations, notes


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_tool_licence_consistency <collection_dir> [...]", file=sys.stderr)
        return 2
    violations, notes = check(argv)
    for note in notes:
        print(f"NOTE {note}")
    for v in violations:
        print(f"FAIL {v}")
    if not violations:
        print(f"OK   {len(argv)} collections: every resolved entity carries one licence")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
