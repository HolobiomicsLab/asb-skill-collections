"""CI gate: every ``related_skills`` reference resolves to a real skill.

The embedding similarity graph (scripts.build_related_skills) writes a
``related_skills`` neighbour list onto each ``skills_index.json`` entry. This gate
checks referential integrity: every slug listed in any entry's ``related_skills``
must itself be a slug present in ``skills_index.json``.

The field is *optional* — it is absent until a maintainer runs the
embedding precompute (``pip install '.[embed]'`` then
``python -m scripts.build_related_skills``). A collection with no
``related_skills`` anywhere (the default real-data state) yields no violations,
so the gate passes vacuously, which is correct.

``main`` exits 1 on any dangling reference, 0 otherwise. Mirrors
scripts/check_proposals.py and scripts/check_provenance_tiers.py.
"""
from __future__ import annotations

import json
import pathlib
import sys


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    si_path = d / "skills_index.json"
    if not si_path.is_file():
        return violations

    si = json.loads(si_path.read_text(encoding="utf-8"))
    if isinstance(si, dict):
        si = si.get("skills") or si.get("entries") or []
    if not isinstance(si, list):
        return violations

    known = {e.get("slug") for e in si if isinstance(e, dict)}

    for entry in si:
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug")
        related = entry.get("related_skills")
        if related is None:
            continue
        if not isinstance(related, list):
            violations.append(
                f"skills_index {slug!r}: related_skills is not a list"
            )
            continue
        for ref in related:
            if ref not in known:
                violations.append(
                    f"skills_index {slug!r}: related_skills {ref!r} "
                    f"not in skills_index.json"
                )

    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_related_skills <collection_dir> [...]", file=sys.stderr)
        return 2
    failed = False
    for col in argv:
        v = check_collection(col)
        if v:
            failed = True
            print(f"FAIL {col}:")
            for x in v:
                print(f"  - {x}")
        else:
            print(f"OK   {col}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
