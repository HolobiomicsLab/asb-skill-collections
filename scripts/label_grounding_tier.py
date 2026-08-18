#!/usr/bin/env python3
"""Stamp each skill with the strength of the evidence behind it.

A skill's grounding is only as strong as the corpus entries it derives from.
An entry whose access tier claims a cloned repository grounds a skill on that
repository; a ``link-only`` entry grounds it on nothing but a resolvable,
citable DOI. Skills that derive *solely* from link-only entries must say so,
rather than being presented alongside repository-grounded ones.

Writes ``metadata.grounding_tier`` into each ``SKILL.md`` and a matching
``grounding_tier`` field into ``skills_index.json``. Idempotent.

    python scripts/label_grounding_tier.py collections/metabolomics/v2
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

from scripts import layout

LINK_ONLY = "link-only"
REPO_GROUNDED = "repo"
UNGROUNDED = "ungrounded"


def link_only_dois(corpus_path: Path) -> set[str]:
    """DOIs of corpus entries that claim no cloned repository."""
    raw = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))
    papers = raw.get("papers") if isinstance(raw, dict) else raw
    return {
        str(p.get("doi"))
        for p in papers or []
        if ((p.get("access") or {}).get("type") or "").strip().lower() == LINK_ONLY
        and p.get("doi")
    }


def skill_dois(frontmatter: dict) -> list[str]:
    """Source DOIs a skill declares, from its derived_from entries."""
    return [
        str(e.get("doi"))
        for e in frontmatter.get("derived_from") or []
        if isinstance(e, dict) and e.get("doi")
    ]


def tier_for(dois: list[str], weak: set[str]) -> str:
    """Grade a skill by the weakest thing its evidence rests on.

    A skill citing no source at all is ``ungrounded`` — never the repo default,
    which would present missing evidence as the strongest kind.
    """
    if not dois:
        return UNGROUNDED
    if all(d in weak for d in dois):
        return LINK_ONLY
    return REPO_GROUNDED


def stamp_skill(path: Path, tier: str) -> bool:
    """Write metadata.grounding_tier into a SKILL.md. True when changed."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return False
    block = match.group(1)
    if re.search(r"^  grounding_tier: .*$", block, re.M):
        new_block = re.sub(
            r"^  grounding_tier: .*$", f"  grounding_tier: {tier}", block, flags=re.M
        )
    elif re.search(r"^metadata:$", block, re.M):
        new_block = re.sub(
            r"^metadata:$", f"metadata:\n  grounding_tier: {tier}", block, count=1, flags=re.M
        )
    else:
        new_block = f"metadata:\n  grounding_tier: {tier}\n" + block
    if new_block == block:
        return False
    path.write_text(text.replace(block, new_block, 1), encoding="utf-8")
    return True


def run(collection: Path) -> dict:
    """Label every skill in the collection and its index."""
    weak = link_only_dois(collection / "corpus.yaml")
    tiers, stamped = {}, 0
    for md in layout.iter_skill_md(collection):
        fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"), re.S).group(1)) or {}
        tier = tier_for(skill_dois(fm), weak)
        tiers[md.parent.name] = tier
        # Only the weaker tier is stamped into the file: repo-grounding is the
        # default, and stamping 5,000 files with it would bury the exception.
        if tier != REPO_GROUNDED:
            stamped += stamp_skill(md, tier)
    index_path = collection / "skills_index.json"
    rows = json.loads(index_path.read_text(encoding="utf-8"))
    for row in rows:
        row["grounding_tier"] = tiers.get(row.get("slug"), REPO_GROUNDED)
    index_path.write_text(
        json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    from collections import Counter
    return {"link_only_dois": len(weak), "skills": len(tiers),
            "tiers": dict(Counter(tiers.values())), "stamped": stamped}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("collection")
    args = p.parse_args(argv)
    print(run(Path(args.collection)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
