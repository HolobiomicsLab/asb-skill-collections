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

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout
from scripts.skill_index import split_frontmatter

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


def repo_url(frontmatter: dict) -> str:
    """The repository a skill grounds on, if it declares a usable one."""
    for source in (frontmatter.get("metadata") or {}, frontmatter):
        raw = str((source or {}).get("repo_url") or "").strip()
        if raw.startswith(("https://", "http://")):
            return raw
    return ""


def tier_for(dois: list[str], weak: set[str], repo: str = "") -> str:
    """Grade a skill by the weakest thing its evidence rests on.

    A declared repository is full grounding, not a fallback: repository-only
    grounding is the project's primary basis (CONTENT_POLICY.md §3). A skill
    with neither a source nor a repository is ``ungrounded`` — never the repo
    default, which would present missing evidence as the strongest kind.
    """
    if not dois:
        return REPO_GROUNDED if repo else UNGROUNDED
    if all(d in weak for d in dois):
        return LINK_ONLY if not repo else REPO_GROUNDED
    return REPO_GROUNDED


def stamp_skill(path: Path, tier: str) -> bool:
    """Write metadata.grounding_tier into a SKILL.md. True when changed.

    Passing the default tier *removes* any existing stamp, so a skill whose
    evidence later improves does not keep a stale weaker label.
    """
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return False
    block = match.group(1)
    has_stamp = bool(re.search(r"^  grounding_tier: .*$", block, re.M))
    if tier == REPO_GROUNDED:
        if not has_stamp:
            return False
        new_block = re.sub(r"^  grounding_tier: .*\n", "", block + "\n", flags=re.M).rstrip("\n")
    elif has_stamp:
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
        fm = split_frontmatter(md.read_text(encoding="utf-8"))[0] or {}
        tier = tier_for(skill_dois(fm), weak, repo_url(fm))
        tiers[md.parent.name] = tier
        # Weak tiers are written; the default tier only ever clears a stale
        # stamp, so repo-grounded files stay clean rather than all carrying it.
        stamped += stamp_skill(md, tier)
    index_path = collection / "skills_index.json"
    rows = json.loads(index_path.read_text(encoding="utf-8"))
    for row in rows:
        # A row with no labelled file on disk has no evidence behind it; the
        # repo default would present that absence as the strongest grounding.
        row["grounding_tier"] = tiers.get(row.get("slug"), UNGROUNDED)
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
