"""CI gate: every corpus + skills_index entry carries a valid license_tier, every
SKILL.md whose tier demands an acknowledgment carries a tool_license block, and
each such block is internally consistent. Exit 1 on violations.

Runs over a collection or over a pack derived from one. A pack ships the tiers
and not the corpus they were derived from, so the corpus half applies only to
the unit that owns a corpus — see :func:`corpus_violations` for why that is a
conditional check and not a silent skip.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout
from scripts.license_tier import ack_required, load_map

# The tier vocabulary has one home: governance/license_tiers.yaml. A hand-copied
# set here silently rejects any tier added there.
_VALID = set(load_map()["tiers"])


def corpus_violations(unit_dir: pathlib.Path) -> list[str]:
    """Tier violations in the unit's own corpus, when it is a unit that owns one.

    A collection ships the corpus its tiers are derived from; a pack ships the
    tiers and derives both from its parent, so it has no corpus of its own.
    Reading `corpus.yaml` unconditionally raised FileNotFoundError on every
    pack, which is why this gate was only ever aimed at the collection while
    the packs -- what most installs actually get -- went unchecked.

    An absent corpus is therefore not a violation *for a pack*. It is one for a
    collection: `collection.yaml` is what a unit uses to declare itself the
    owner of a corpus, so a collection that has lost its corpus fails here
    rather than quietly passing a gate that checked half of what it claims to.
    """
    corpus_path = unit_dir / "corpus.yaml"
    if not corpus_path.is_file():
        if (unit_dir / "collection.yaml").is_file():
            return [
                "corpus.yaml missing: a collection must ship the corpus its "
                "license tiers are derived from"
            ]
        return []
    corpus = yaml.safe_load(corpus_path.read_text(encoding="utf-8")) or {}
    return [
        f"corpus entry {p.get('name')!r}: missing/invalid license_tier"
        for p in corpus.get("papers", [])
        if p.get("license_tier") not in _VALID
    ]


def scope(unit_dir) -> str:
    """What the last run actually covered, for the CLI's own pass line.

    Printed on a pass as well as a failure: a gate whose corpus half silently
    does not apply must say so in the log, or "OK" reads as "all of it passed".
    """
    d = pathlib.Path(unit_dir)
    entries = len(json.loads((d / "skills_index.json").read_text(encoding="utf-8")))
    corpus = "corpus checked" if (d / "corpus.yaml").is_file() else "no corpus of its own"
    return f"{entries} index entries, {corpus}"


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = corpus_violations(d)

    si = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))
    # Build slug→index_tier map for cross-check
    slug_to_index_tier = {}
    for e in si:
        if e.get("license_tier") not in _VALID:
            violations.append(f"skills_index {e.get('slug')!r}: missing/invalid license_tier")
        else:
            slug_to_index_tier[e.get("slug")] = e.get("license_tier")

    for md in layout.iter_skill_md(d):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}

        # Cross-check: frontmatter tier vs index tier
        slug = md.parent.name
        if slug in slug_to_index_tier:
            fm_tier = (fm.get("metadata") or {}).get("license_tier")
            index_tier = slug_to_index_tier[slug]
            if fm_tier not in _VALID:
                violations.append(f"{md}: metadata.license_tier missing/invalid")
            elif fm_tier != index_tier:
                violations.append(f"{md}: metadata.license_tier {fm_tier!r} != skills_index {index_tier!r}")

        tl = (fm.get("metadata") or {}).get("tool_license")
        if not tl:
            # An absent block is not a neutral absence. `asb-metabolomics` reads
            # this block to decide whether to raise the blocking use
            # acknowledgment, so a leaf whose tier demands one but carries no
            # block is applied with no acknowledgment at all -- while its
            # frontmatter still reads `license_tier: noncommercial`. Skipping it
            # here is what let 37 such leaves ship. Tiers that raise no ack are
            # exempt by the same rule: their block gates nothing, and the soft
            # note they do owe the user is carried by the body banner.
            if ack_required((fm.get("metadata") or {}).get("license_tier")):
                violations.append(f"{md}: tool_license block missing, required by tier")
            continue
        if tl.get("tier") not in _VALID:
            violations.append(f"{md}: tool_license.tier invalid")
        elif tl.get("requires_ack") != ack_required(tl["tier"]):
            violations.append(f"{md}: requires_ack inconsistent with tier {tl['tier']}")
    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_license_tiers <collection_dir> [...]", file=sys.stderr)
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
            print(f"OK   {col}  ({scope(col)})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
