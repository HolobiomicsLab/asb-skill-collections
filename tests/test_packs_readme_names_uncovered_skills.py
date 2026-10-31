"""The packs README says which v2 skills no pack holds, with the true count.

A pack holds the skills tagged with its technique, so the skills with an
empty ``techniques`` list are in none of the eight packs. The README listed
the packs as lighter installs of the collection without saying so; it now
names those skills and the routes that install them, and this test keeps
its count equal to the on-disk census.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
V2_INDEX = REPO / "collections" / "metabolomics" / "v2" / "skills_index.json"
PACKS = REPO / "packs" / "metabolomics"


def _slugs(index: Path) -> set[str]:
    return {row["slug"] for row in json.loads(index.read_text(encoding="utf-8"))}


def test_the_readme_counts_the_skills_no_pack_holds() -> None:
    in_a_pack = set().union(*(_slugs(p) for p in PACKS.glob("*/skills_index.json")))
    rows = json.loads(V2_INDEX.read_text(encoding="utf-8"))
    uncovered = {row["slug"] for row in rows} - in_a_pack
    agnostic = {row["slug"] for row in rows if not row.get("techniques")}

    readme = (PACKS / "README.md").read_text(encoding="utf-8")
    match = re.search(r"the ([\d,]+) technique-agnostic skills", readme)

    assert uncovered == agnostic
    assert match, "the README does not name the skills no pack holds"
    assert int(match.group(1).replace(",", "")) == len(uncovered)
    assert "(../../docs/partial-install.md)" in readme
    assert (REPO / "docs" / "partial-install.md").is_file()
