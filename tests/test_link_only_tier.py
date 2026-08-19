"""The link-only access tier and the grounding labels derived from it.

`link-only` exists so a source with no public repository can be cited honestly
instead of carrying a `repo-oa` tier whose clone never happened. These tests
pin the two properties that keep it honest: it may not claim a clone, and the
skills resting on it must be labelled as weaker.
"""

from __future__ import annotations

import json
import pathlib

import pytest
import yaml

from scripts import label_grounding_tier as lg
from scripts import release_gate

V2 = pathlib.Path(__file__).resolve().parent.parent / "collections" / "metabolomics" / "v2"


def _corpus(tmp_path, papers):
    path = tmp_path / "corpus.yaml"
    path.write_text(yaml.safe_dump({"papers": papers}), encoding="utf-8")
    return path


def test_link_only_is_an_admitted_tier():
    assert "link-only" in release_gate._NORMALIZED_OA_TIERS
    assert "link-only" not in release_gate._REPO_OA_TIERS, (
        "link-only must not inherit the repo-oa clone-evidence requirement"
    )


def test_link_only_entry_may_not_claim_a_clone(tmp_path):
    corpus = yaml.safe_load(
        _corpus(tmp_path, [{
            "doi": "10.1/x", "status": "included", "repo_url": "",
            "access": {"type": "link-only", "verified_via": "git_clone_succeeded_at_build"},
        }]).read_text()
    )
    res = release_gate.check_access_tier(corpus, require_open_access=True)
    assert any("claims no clone" in str(d) for d in res.details)


def test_clean_link_only_entry_passes(tmp_path):
    corpus = yaml.safe_load(
        _corpus(tmp_path, [{
            "doi": "10.1/x", "status": "included", "repo_url": "",
            "access": {"type": "link-only", "is_oa": None},
        }]).read_text()
    )
    res = release_gate.check_access_tier(corpus, require_open_access=True)
    assert not [d for d in res.details if str(d.get("level", "")).lower() == "fail"]


@pytest.mark.parametrize(
    "dois, weak, expected",
    [
        ([], set(), "ungrounded"),
        (["10.1/a"], {"10.1/a"}, "link-only"),
        (["10.1/a", "10.1/b"], {"10.1/a"}, "repo"),
        (["10.1/a", "10.1/b"], {"10.1/a", "10.1/b"}, "link-only"),
    ],
)
def test_tier_grades_by_weakest_evidence(dois, weak, expected):
    assert lg.tier_for(dois, weak) == expected


def test_no_source_never_defaults_to_the_strong_tier():
    """A skill citing nothing must not be presented as repository-grounded."""
    assert lg.tier_for([], {"10.1/a"}) == lg.UNGROUNDED
    assert lg.tier_for([], set()) != lg.REPO_GROUNDED


def test_released_corpus_has_no_orphan_repo_oa():
    raw = yaml.safe_load((V2 / "corpus.yaml").read_text(encoding="utf-8"))
    papers = raw["papers"] if isinstance(raw, dict) else raw
    orphans = [
        p for p in papers
        if (p.get("access") or {}).get("type") in release_gate._REPO_OA_TIERS
        and p.get("status") == "included"
        and not (p.get("repo_url") or "").strip()
    ]
    assert not orphans, f"{len(orphans)} repo-oa entries still claim an unverifiable clone"


def test_released_link_only_entries_carry_no_clone_stamp():
    raw = yaml.safe_load((V2 / "corpus.yaml").read_text(encoding="utf-8"))
    papers = raw["papers"] if isinstance(raw, dict) else raw
    stamped = [
        p["doi"] for p in papers
        if (p.get("access") or {}).get("type") == "link-only"
        and (p.get("access") or {}).get("verified_via")
    ]
    assert not stamped, f"link-only entries still claiming a clone: {stamped[:3]}"


# --------------------------------------------------------------------------- #
# Repository-only grounding (CONTENT_POLICY.md §3): a public repo IS evidence. #
# --------------------------------------------------------------------------- #

def test_repo_url_satisfies_provenance_without_a_paper_doi(tmp_path):
    """A tool with no method paper is grounded on its published code."""
    col = tmp_path / "c"
    (col / "skills" / "toolskill").mkdir(parents=True)
    (col / "skills" / "toolskill" / "SKILL.md").write_text(
        "---\nname: toolskill\nlicense: CC-BY-4.0\n"
        "metadata:\n  repo_url: https://github.com/example/tool\n---\nbody\n",
        encoding="utf-8",
    )
    res = release_gate.check_provenance(col)
    assert not [d for d in res.details if str(d.get("level", "")).lower() == "fail"]


def test_no_doi_and_no_repo_still_fails(tmp_path):
    col = tmp_path / "c"
    (col / "skills" / "bare").mkdir(parents=True)
    (col / "skills" / "bare" / "SKILL.md").write_text(
        "---\nname: bare\nlicense: CC-BY-4.0\n---\nbody\n", encoding="utf-8"
    )
    res = release_gate.check_provenance(col)
    assert any("no provenance" in str(d) for d in res.details)


@pytest.mark.parametrize("bogus", ["", "   ", "example/tool", "git@github.com:x/y"])
def test_a_non_url_repo_field_is_not_evidence(bogus):
    """Only a real http(s) URL counts; a bare slug or empty string does not."""
    assert release_gate._skill_repo_url({"metadata": {"repo_url": bogus}}) == ""


def test_repo_grounding_outranks_link_only():
    assert lg.tier_for([], set(), "https://github.com/x/y") == lg.REPO_GROUNDED
    assert lg.tier_for(["10.1/a"], {"10.1/a"}, "https://github.com/x/y") == lg.REPO_GROUNDED
    assert lg.tier_for(["10.1/a"], {"10.1/a"}, "") == lg.LINK_ONLY


def test_stamp_is_cleared_when_evidence_improves(tmp_path):
    """Re-running after a skill gains evidence must not leave a stale label."""
    md = tmp_path / "SKILL.md"
    md.write_text(
        "---\nname: s\nmetadata:\n  grounding_tier: ungrounded\n  role: x\n---\nbody\n",
        encoding="utf-8",
    )
    assert lg.stamp_skill(md, lg.REPO_GROUNDED) is True
    assert "grounding_tier" not in md.read_text(encoding="utf-8")
    assert lg.stamp_skill(md, lg.REPO_GROUNDED) is False  # idempotent


def test_released_collection_has_no_ungrounded_skill():
    import yaml as _yaml
    from asb_skill_collections import layout
    weak = lg.link_only_dois(V2 / "corpus.yaml")
    import re as _re
    bad = []
    for md in layout.iter_skill_md(V2):
        fm = _yaml.safe_load(
            _re.match(r"^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"), _re.S).group(1)
        ) or {}
        if lg.tier_for(lg.skill_dois(fm), weak, lg.repo_url(fm)) == lg.UNGROUNDED:
            bad.append(md.parent.name)
    assert not bad, f"skills with no evidence at all: {bad}"


def _labelling_collection(tmp_path, extra_rows=()):
    """A minimal router-shaped collection `lg.run` can label end to end."""
    col = tmp_path / "c"
    (col / "leaves" / "alpha").mkdir(parents=True)
    (col / "leaves" / "alpha" / "SKILL.md").write_text(
        "---\nname: alpha\nderived_from:\n- doi: 10.1/a\n---\nbody\n", encoding="utf-8"
    )
    _corpus(col, [{"doi": "10.1/a", "repo_url": "https://example.org/r",
                   "access": {"type": "repo-oa"}}])
    rows = [{"slug": "alpha"}, *extra_rows]
    (col / "skills_index.json").write_text(json.dumps(rows), encoding="utf-8")
    return col


def test_an_index_row_with_no_file_on_disk_is_not_called_repo_grounded(tmp_path):
    """The strongest tier must never be the default for evidence never seen.

    A row can outlive its file (a purge, an index/disk skew). Defaulting it to
    `repo` would advertise missing evidence as cloned source code.
    """
    col = _labelling_collection(tmp_path, extra_rows=[{"slug": "vanished"}])
    lg.run(col)
    rows = {r["slug"]: r["grounding_tier"]
            for r in json.loads((col / "skills_index.json").read_text())}
    assert rows["alpha"] == lg.REPO_GROUNDED
    assert rows["vanished"] == lg.UNGROUNDED, (
        "an unlabelled row inherited the strongest grounding tier"
    )


def test_a_skill_without_a_frontmatter_fence_does_not_abort_labelling(tmp_path):
    """One malformed leaf must not take the whole labelling run down."""
    col = _labelling_collection(tmp_path)
    (col / "leaves" / "broken").mkdir()
    (col / "leaves" / "broken" / "SKILL.md").write_text("no fence here\n", encoding="utf-8")
    lg.run(col)  # raised AttributeError before the canonical parser was adopted
