"""The duplicate question is not the relatedness question (INT-ASB-038, §4.5).

``commands/propose-skill.md`` carried ``near_duplicates(skills, threshold=0.85)``
on the abandoned dev line and was never ported, so the check has never run. Two
things were wrong with it, and both are pinned here because both are invisible
from a green suite:

* **The document.** Skills distilled from one paper inherit that paper's whole
  tool list, so a ranking scored over ``skill_doc`` — tools included — puts
  co-provenance at the top instead of shared meaning. Over ``metabolomics/v2``
  the corpus's clearest genuine duplicate pair (``qc-summary-data-extraction`` /
  ``qc-summary-table-extraction``) sat *below* 59 tool-sharing skills.
  :func:`duplicate_candidates` scores the tool-free document instead.
* **The scale.** 0.85 was read off document-vs-document similarity, but the
  command scores a contributor's short *prose* against those documents, which
  runs about 0.2 lower. On that path 0.85 flags nothing at all — 0 of 5,859,
  with or without the tool list. A threshold from the wrong scale is a warning
  that can never fire, which is exactly what a suite cannot see.

So the assertions below are two-sided on purpose: the cut must flag the known
twins *and* leave unrelated prose alone, and the old cut must be shown inert
rather than merely different.
"""

import json
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import skill_match as sm  # noqa: E402

COLLECTION = REPO_ROOT / "collections" / "metabolomics" / "v2"

# Hand-identified duplicate pairs: same operation, two slugs. Each is a pair a
# reviewer would answer with "annotate or merge into the other", which is what
# the warning asks.
KNOWN_TWINS = [
    ("qc-summary-data-extraction", "qc-summary-table-extraction"),
    (
        "retention-time-and-mass-based-sorting",
        "retention-time-and-mass-sorting-of-chromatographic-peaks",
    ),
    (
        "structure-organism-pair-deduplication",
        "structure-organism-pair-counting-and-deduplication",
    ),
]

# Prose for skills this collection does not hold: the warning must stay silent.
UNRELATED_PROSE = [
    "Use when negotiating a data-transfer agreement with a clinical partner "
    "before any raw acquisition file leaves the hospital network.",
    "Use when converting a phylogenetic tree into a patristic distance matrix "
    "for downstream hierarchical clustering.",
]


# --------------------------------------------------------------------------- #
# The document: include_tools is what separates the two questions.             #
# --------------------------------------------------------------------------- #
ENTRY = {
    "slug": "peak-picking",
    "name": "Peak picking",
    "description": "Detect chromatographic peaks.",
    "tools": ["xcms", "mzmine"],
    "tools_used": ["openms"],
    "edam_topics": ["topic_3172"],
    "techniques": ["LC-MS"],
}


def test_skill_doc_drops_only_the_tool_inventory():
    full = sm.skill_doc(ENTRY)
    lean = sm.skill_doc(ENTRY, include_tools=False)
    for tool in ("xcms", "mzmine", "openms"):
        assert tool in full
        assert tool not in lean, "the tool inventory is what the dedup doc drops"
    # everything else survives — dropping tools must not quietly drop the rest
    for kept in ("peak-picking", "Peak picking", "chromatographic", "topic_3172", "LC-MS"):
        assert kept in lean, kept


def test_skill_doc_default_is_unchanged():
    """`build_related_skills.py` and `match_skills` call it positionally."""
    assert sm.skill_doc(ENTRY) == sm.skill_doc(ENTRY, include_tools=True)


def test_shared_tools_alone_stop_ranking_first_without_them():
    """The failure mode itself: two unrelated skills joined only by a tool list."""
    index = [
        {
            "slug": "co-provenance-a",
            "name": "Alpha",
            "description": "Count adducts in a feature table.",
            "tools": ["xcms", "mzmine", "openms", "msdial", "sirius"],
        },
        {
            "slug": "co-provenance-b",
            "name": "Beta",
            "description": "Render a treemap of compound classes.",
            "tools": ["xcms", "mzmine", "openms", "msdial", "sirius"],
        },
    ]
    query = "Alpha count adducts in a feature table"
    with_tools = {h["slug"]: h["score"] for h in sm.lexical_match(query, index)}
    without = {
        h["slug"]: h["score"]
        for h in sm.lexical_match(query, index, include_tools=False)
    }
    # with the tool list the unrelated sibling is pulled up towards the real hit;
    # without it, the gap opens
    gap_with = with_tools["co-provenance-a"] - with_tools["co-provenance-b"]
    gap_without = without["co-provenance-a"] - without["co-provenance-b"]
    assert gap_without > gap_with, (with_tools, without)


# --------------------------------------------------------------------------- #
# The threshold, on the path that actually runs.                               #
# --------------------------------------------------------------------------- #
def test_the_threshold_is_a_positive_opt_in():
    assert 0.0 < sm.DUPLICATE_THRESHOLD < 1.0
    # near_duplicates keeps its documented no-op default; the cut is explicit at
    # the call site, so a caller cannot inherit one by accident.
    assert sm.near_duplicates([{"slug": "a", "score": 0.99}]) == []


@pytest.mark.skipif(
    not (COLLECTION / "skills_index.json").is_file(), reason="collection not present"
)
class TestAgainstTheShippedCollection:
    @pytest.fixture(scope="class")
    def index(self):
        entries = json.loads((COLLECTION / "skills_index.json").read_text())
        return {e["slug"]: e for e in entries if e.get("slug")}

    @staticmethod
    def _prose(entry):
        """What a contributor supplies: the skill's own words, no tool names."""
        return f"{entry.get('name', '')} {entry.get('description', '')}".strip()

    @pytest.mark.parametrize("a,b", KNOWN_TWINS, ids=[a for a, _ in KNOWN_TWINS])
    def test_a_known_twin_is_flagged(self, index, a, b):
        assert a in index and b in index, "the fixture pair must still be shipped"
        flagged = sm.near_duplicates(
            sm.duplicate_candidates(self._prose(index[a]), COLLECTION),
            threshold=sm.DUPLICATE_THRESHOLD,
        )
        assert b in flagged, f"{b} should be offered as the merge target for {a}"

    @pytest.mark.parametrize("prose", UNRELATED_PROSE)
    def test_unrelated_prose_is_not_flagged(self, prose):
        assert (
            sm.near_duplicates(
                sm.duplicate_candidates(prose, COLLECTION),
                threshold=sm.DUPLICATE_THRESHOLD,
            )
            == []
        )

    @pytest.mark.parametrize("a,b", KNOWN_TWINS, ids=[a for a, _ in KNOWN_TWINS])
    def test_the_dev_line_threshold_was_inert_on_this_path(self, index, a, b):
        """0.85 is not merely stricter — on prose queries it flags nothing.

        Both rankings are checked, so this pins the *scale* error rather than the
        document error: neither document reaches 0.85 from a prose query.
        """
        prose = self._prose(index[a])
        for candidates in (
            sm.duplicate_candidates(prose, COLLECTION),
            sm.match_skills(prose, COLLECTION),
        ):
            others = [c for c in candidates if c["slug"] != a]
            assert sm.near_duplicates(others, threshold=0.85) == []

    def test_the_separate_ranking_is_load_bearing_not_ceremony(self, index):
        """The same cut on the relatedness ranking would miss a real twin.

        The two rankings often agree on *order* at small k — what differs is the
        scale, and the scale is what a threshold reads. Scored on the tool-free
        document every known twin clears the cut; scored on the relatedness
        document at least one falls under it. That gap is the whole reason the
        duplicate question gets its own call rather than reusing ``match_skills``.
        """
        caught_dup, caught_related = [], []
        for a, b in KNOWN_TWINS:
            prose = self._prose(index[a])
            for call, bucket in (
                (sm.duplicate_candidates, caught_dup),
                (sm.match_skills, caught_related),
            ):
                flagged = sm.near_duplicates(
                    call(prose, COLLECTION), threshold=sm.DUPLICATE_THRESHOLD
                )
                bucket.append(b in flagged)
        assert all(caught_dup), caught_dup
        assert not all(caught_related), (
            "if the relatedness ranking caught every twin too, the tool-free "
            "document would be buying nothing"
        )


# --------------------------------------------------------------------------- #
# The commands that make the check reachable at all.                           #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "command,symbols",
    [
        ("propose-skill.md", ("duplicate_candidates", "DUPLICATE_THRESHOLD")),
        ("claim-skill.md", ("duplicate_candidates", "DUPLICATE_THRESHOLD")),
        ("synthesize-meta-skill.md", ("near_duplicates",)),
    ],
)
def test_the_command_that_runs_the_check_ships(command, symbols):
    """The defect was a missing caller, not a wrong number — pin the caller.

    ``governance/COMMUNITY_SKILLS.md``, ``META_SKILLS.md`` and ``AUTHORSHIP.md``
    each link one of these; a release that drops them again turns those links
    into 404s and the prose into an unbacked claim.
    """
    path = COLLECTION / "commands" / command
    assert path.is_file(), f"{path} is linked from governance/ and must ship"
    text = path.read_text()
    for symbol in symbols:
        assert symbol in text, f"{command} must drive {symbol}"


def test_no_command_carries_the_dev_line_threshold():
    for path in (COLLECTION / "commands").glob("*.md"):
        assert "threshold=0.85" not in path.read_text(), path


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
