"""Tests for scripts.promote_proposals — the proposals → published promotion tool.

A tiny fixture collection is built in a tmp dir (skills_index.json, kb_bundle.json,
tools_index.json, corpus.yaml, one published skill, one *staged* community
proposal). We then exercise:

* ``staged_slugs`` finds the held proposal;
* ``promote`` moves it into ``skills/`` with ``status: included``, appends a
  skills_index entry + kb_bundle record, and the result is gate-clean under the
  four CI gates;
* ``check_proposals`` no longer sees the promoted slug;
* re-running ``promote`` is a no-op (idempotent);
* ``--dry-run`` writes nothing.

No git/gh, no network. Mirrors the propose_skill / check_proposals discipline.
"""
from __future__ import annotations

import json

import yaml

from scripts import (
    check_license_tiers,
    check_proposals,
    check_provenance_tiers,
    check_tools_index,
    promote_proposals,
)

DATE = "2026-06-26"


# --------------------------------------------------------------------------- #
# fixture                                                                      #
# --------------------------------------------------------------------------- #
def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def _published_skill_md(slug):
    fm = {
        "name": slug,
        "description": (
            "Use when you need to detect and align LC-MS features across samples "
            "as the first stage of an untargeted metabolomics workflow."
        ),
        "license": "CC-BY-4.0",
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_3172"],
            "tools": ["xcms"],
            "techniques": ["LC-MS"],
            "license_tier": "open",
            "provenance_tier": "literature",
            "tools_used": ["xcms"],
        },
    }
    return (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        + "---\n"
        + "Published skill body.\n"
    )


def _staged_proposal_md(slug):
    """A held *community* proposal: status hold, related_skills present, valid
    frontmatter discipline, tools_used resolvable in the fixture tool catalog."""
    fm = {
        "name": slug,
        "description": (
            "Use when you need to annotate molecular network nodes against a "
            "reference spectral library and propagate the matches to neighbours."
        ),
        "license": "CC-BY-4.0",
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3631",
            "edam_topics": ["http://edamontology.org/topic_3172"],
            "tools": ["matchms"],
            "techniques": ["LC-MS/MS"],
            "license_tier": "open",
            "provenance_tier": "community",
            "tools_used": ["matchms"],
        },
        "status": "hold",
        "related_skills": ["lc-ms-feature-extraction-and-alignment"],
    }
    return (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        + "---\n"
        + "Staged community proposal body.\n"
    )


def build_fixture(tmp_path):
    """Materialize a minimal but gate-valid collection with one staged proposal."""
    col = tmp_path / "collections" / "demo" / "v2"
    pub = "lc-ms-feature-extraction-and-alignment"
    proposal = "library-match-annotation"

    # published skill on disk
    (col / "skills" / pub).mkdir(parents=True, exist_ok=True)
    (col / "skills" / pub / "SKILL.md").write_text(
        _published_skill_md(pub), encoding="utf-8"
    )

    # staged community proposal on disk
    (col / "proposals" / "skills" / proposal).mkdir(parents=True, exist_ok=True)
    (col / "proposals" / "skills" / proposal / "SKILL.md").write_text(
        _staged_proposal_md(proposal), encoding="utf-8"
    )

    # tools_index.json — two resolvable tools
    _write_json(
        col / "tools_index.json",
        [
            {
                "slug": "xcms",
                "name": "xcms",
                "dois": [],
                "license_tier": "open",
                "license": None,
                "license_detection": None,
                "used_by_skills": [pub],
            },
            {
                "slug": "matchms",
                "name": "matchms",
                "dois": [],
                "license_tier": "open",
                "license": None,
                "license_detection": None,
                "used_by_skills": [],
            },
        ],
    )

    # skills_index.json — just the published skill
    _write_json(
        col / "skills_index.json",
        [
            {
                "slug": pub,
                "name": pub,
                "description": "Use when you need to detect and align LC-MS features.",
                "edam_operation": "http://edamontology.org/operation_3215",
                "edam_topics": ["http://edamontology.org/topic_3172"],
                "tools": ["xcms"],
                "dois": ["10.1000/demo"],
                "techniques": ["LC-MS"],
                "license_tier": "open",
                "provenance_tier": "literature",
                "tools_used": ["xcms"],
            }
        ],
    )

    # kb_bundle.json
    _write_json(
        col / "kb_bundle.json",
        {
            "collection": "demo",
            "version": "v2",
            "perspicacite_kb_mode": "paper",
            "kb_prefix": "asb-paper",
            "distinct_dois": 1,
            "skills": {
                pub: {
                    "dois": ["10.1000/demo"],
                    "tools": ["xcms"],
                    "kb_slugs": ["asb-paper-10-1000-demo"],
                    "repo_urls": [],
                    "license_tier": "open",
                    "provenance_tier": "literature",
                    "tools_used": ["xcms"],
                }
            },
        },
    )

    # corpus.yaml — one paper so check_license_tiers' corpus loop is happy
    (col / "corpus.yaml").write_text(
        yaml.safe_dump(
            {
                "papers": [
                    {
                        "name": "demo",
                        "doi": "10.1000/demo",
                        "license_tier": "open",
                        "access": {"license": "CC-BY-4.0"},
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    return col, pub, proposal


def _assert_gates_clean(col):
    assert check_license_tiers.check_collection(str(col)) == []
    assert check_provenance_tiers.check_collection(str(col)) == []
    assert check_tools_index.check_collection(str(col)) == []
    assert check_proposals.check_collection(str(col)) == []


# --------------------------------------------------------------------------- #
# tests                                                                        #
# --------------------------------------------------------------------------- #
def test_fixture_starts_gate_clean(tmp_path):
    col, _, _ = build_fixture(tmp_path)
    _assert_gates_clean(col)


def test_staged_slugs_finds_held_proposal(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    assert promote_proposals.staged_slugs(str(col)) == [proposal]


def test_promote_moves_into_skills_with_included_status(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    res = promote_proposals.promote(str(col), [proposal], date=DATE)

    assert res["promoted"] == [proposal]
    assert res["skipped"] == []

    # SKILL.md now lives under skills/ and is gone from proposals/skills/
    new_md = col / "skills" / proposal / "SKILL.md"
    old_md = col / "proposals" / "skills" / proposal / "SKILL.md"
    assert new_md.is_file()
    assert not old_md.exists()

    fm = yaml.safe_load(new_md.read_text(encoding="utf-8").split("---\n", 2)[1])
    assert fm["status"] == "included"

    # appears in skills_index.json with status-independent fields populated
    si = json.loads((col / "skills_index.json").read_text(encoding="utf-8"))
    entry = next(e for e in si if e["slug"] == proposal)
    assert entry["provenance_tier"] == "community"
    assert entry["license_tier"] == "open"
    assert entry["tools_used"] == ["matchms"]
    assert "related_skills" in entry  # community invariant carried onto the index

    # appears in kb_bundle.json
    kb = json.loads((col / "kb_bundle.json").read_text(encoding="utf-8"))
    assert proposal in kb["skills"]
    assert kb["skills"][proposal]["provenance_tier"] == "community"


def test_promote_is_gate_clean(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    promote_proposals.promote(str(col), [proposal], date=DATE)
    _assert_gates_clean(col)


def test_check_proposals_no_longer_sees_promoted(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    promote_proposals.promote(str(col), [proposal], date=DATE)
    # the proposal is gone from the proposals rail
    assert promote_proposals.staged_slugs(str(col)) == []
    assert check_proposals.check_collection(str(col)) == []


def test_promote_is_idempotent(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    promote_proposals.promote(str(col), [proposal], date=DATE)
    si_before = (col / "skills_index.json").read_text(encoding="utf-8")
    kb_before = (col / "kb_bundle.json").read_text(encoding="utf-8")
    md_before = (col / "skills" / proposal / "SKILL.md").read_text(encoding="utf-8")

    res2 = promote_proposals.promote(str(col), [proposal], date=DATE)
    assert res2["promoted"] == []
    assert res2["skipped"] == [proposal]

    assert (col / "skills_index.json").read_text(encoding="utf-8") == si_before
    assert (col / "kb_bundle.json").read_text(encoding="utf-8") == kb_before
    assert (col / "skills" / proposal / "SKILL.md").read_text(
        encoding="utf-8"
    ) == md_before
    # still single index entry for the slug (no duplication)
    si = json.loads(si_before)
    assert sum(1 for e in si if e["slug"] == proposal) == 1


def test_dry_run_writes_nothing(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    si_before = (col / "skills_index.json").read_text(encoding="utf-8")
    kb_before = (col / "kb_bundle.json").read_text(encoding="utf-8")

    res = promote_proposals.promote(str(col), [proposal], date=DATE, dry_run=True)
    assert res["promoted"] == [proposal]  # the *plan*

    # nothing moved, nothing appended
    assert (col / "proposals" / "skills" / proposal / "SKILL.md").is_file()
    assert not (col / "skills" / proposal / "SKILL.md").exists()
    assert (col / "skills_index.json").read_text(encoding="utf-8") == si_before
    assert (col / "kb_bundle.json").read_text(encoding="utf-8") == kb_before


def test_main_dry_run_writes_nothing(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    si_before = (col / "skills_index.json").read_text(encoding="utf-8")

    rc = promote_proposals.main(
        [
            "--collection",
            str(col),
            "--slug",
            proposal,
            "--date",
            DATE,
            "--dry-run",
        ]
    )
    assert rc == 0
    assert not (col / "skills" / proposal / "SKILL.md").exists()
    assert (col / "skills_index.json").read_text(encoding="utf-8") == si_before


def test_main_promotes_all_staged_when_no_slug(tmp_path):
    col, _, proposal = build_fixture(tmp_path)
    rc = promote_proposals.main(["--collection", str(col), "--date", DATE])
    assert rc == 0
    assert (col / "skills" / proposal / "SKILL.md").is_file()
    _assert_gates_clean(col)
