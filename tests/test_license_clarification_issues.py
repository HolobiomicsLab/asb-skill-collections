"""Tests for scripts/license_clarification_issues.py — written RED-first (TDD)."""
from __future__ import annotations

import yaml
import pytest


# ---------------------------------------------------------------------------
# Fixture corpus (in-memory)
# ---------------------------------------------------------------------------

FIXTURE_CORPUS = {
    "schema": "asb-corpus/1.0",
    "papers": [
        # 1. GitHub, restricted, NO license → should be selected
        {
            "name": "ToolA",
            "doi": "10.1000/aaa",
            "repo_url": "https://github.com/owner1/repoA",
            "license_tier": "restricted",
            "access": {"license": None},
        },
        # 2. GitHub, restricted, HAS license → excluded
        {
            "name": "ToolB",
            "doi": "10.1000/bbb",
            "repo_url": "https://github.com/owner2/repoB",
            "license_tier": "restricted",
            "access": {"license": "MIT"},
        },
        # 3. No repo, restricted → excluded
        {
            "name": "ToolC",
            "doi": "10.1000/ccc",
            "repo_url": "",
            "license_tier": "restricted",
            "access": {"license": None},
        },
        # 4. Non-GitHub URL, restricted → excluded
        {
            "name": "ToolD",
            "doi": "10.1000/ddd",
            "repo_url": "https://gitlab.com/some/repo",
            "license_tier": "restricted",
            "access": {"license": None},
        },
        # 5. GitHub, open → excluded
        {
            "name": "ToolE",
            "doi": "10.1000/eee",
            "repo_url": "https://github.com/owner5/repoE",
            "license_tier": "open",
            "access": {"license": "Apache-2.0"},
        },
    ],
}


def _write_corpus(tmp_path, corpus=None):
    if corpus is None:
        corpus = FIXTURE_CORPUS
    p = tmp_path / "corpus.yaml"
    p.write_text(yaml.safe_dump(corpus, allow_unicode=True), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# Test 1 — candidates()
# ---------------------------------------------------------------------------

def test_candidates_selects_only_github_nolicense_restricted(tmp_path):
    from scripts.license_clarification_issues import candidates

    path = _write_corpus(tmp_path)
    result = candidates(path)

    assert len(result) == 1
    c = result[0]
    assert c["name"] == "ToolA"
    assert c["owner"] == "owner1"
    assert c["repo"] == "repoA"
    assert c["doi"] == "10.1000/aaa"


# ---------------------------------------------------------------------------
# Test 2 — render_issue()
# ---------------------------------------------------------------------------

def test_render_issue_title_and_body():
    from scripts.license_clarification_issues import render_issue

    collection_url = "https://github.com/HolobiomicsLab/asb-skill-collections"
    title, body = render_issue("MyTool", collection_url)

    assert title == "License clarification for MyTool?"
    assert "MyTool" in body
    assert collection_url in body
    assert "explicit open-source license" in body or "explicit" in body
    assert "<!-- asb-license-clarification -->" in body


# ---------------------------------------------------------------------------
# Test 3 — already_filed()
# ---------------------------------------------------------------------------

def test_already_filed_true_when_matching_title():
    from scripts.license_clarification_issues import already_filed

    result = already_filed("owner", "repo", _list=lambda o, r: ["License clarification for X?"])
    assert result is True


def test_already_filed_false_when_no_titles():
    from scripts.license_clarification_issues import already_filed

    result = already_filed("owner", "repo", _list=lambda o, r: [])
    assert result is False


def test_already_filed_false_when_no_matching_title():
    from scripts.license_clarification_issues import already_filed

    result = already_filed("owner", "repo", _list=lambda o, r: ["Some other issue"])
    assert result is False


# ---------------------------------------------------------------------------
# Test 4 — run(create=False) dry-run never calls _create
# ---------------------------------------------------------------------------

def test_run_dry_run_never_calls_create(tmp_path):
    from scripts.license_clarification_issues import run

    def _evil_create(*a, **kw):
        raise AssertionError("_create must NOT be called in dry-run mode")

    path = _write_corpus(tmp_path)
    plan = run(
        path,
        create=False,
        _list=lambda o, r: [],
        _create=_evil_create,
        _sleep=lambda n: None,
    )

    assert len(plan) >= 1
    for item in plan:
        assert item["action"] == "planned"
        assert "url" not in item


# ---------------------------------------------------------------------------
# Test 5 — run(create=True) calls _create and handles skips
# ---------------------------------------------------------------------------

def test_run_create_true_calls_create_and_skips(tmp_path):
    from scripts.license_clarification_issues import run

    created = []

    def _fake_create(owner, repo, title, body, _run=None):
        created.append((owner, repo))
        return f"https://github.com/{owner}/{repo}/issues/42"

    # Add a second github-restricted-nolicense entry to test partial skip
    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "ToolA",
                "doi": "10.1000/aaa",
                "repo_url": "https://github.com/owner1/repoA",
                "license_tier": "restricted",
                "access": {"license": None},
            },
            {
                "name": "ToolF",
                "doi": "10.1000/fff",
                "repo_url": "https://github.com/owner6/repoF",
                "license_tier": "restricted",
                "access": {"license": None},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)

    # _list: ToolF already has an issue; ToolA does not
    def _fake_list(o, r):
        if r == "repoF":
            return ["License clarification for ToolF?"]
        return []

    plan = run(
        path,
        create=True,
        _list=_fake_list,
        _create=_fake_create,
        _sleep=lambda n: None,
    )

    assert len(plan) == 2
    actions = {item["name"]: item["action"] for item in plan}
    assert actions["ToolA"] == "created"
    assert actions["ToolF"] == "skipped-exists"

    # _create called only for ToolA
    assert len(created) == 1
    assert created[0] == ("owner1", "repoA")

    # created item has url
    tool_a = next(i for i in plan if i["name"] == "ToolA")
    assert "url" in tool_a
    assert "owner1/repoA" in tool_a["url"]


# ---------------------------------------------------------------------------
# Test 6 — run(limit=1) processes at most 1 candidate
# ---------------------------------------------------------------------------

def test_run_limit(tmp_path):
    from scripts.license_clarification_issues import run

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": f"Tool{i}",
                "doi": f"10.1000/{i:03d}",
                "repo_url": f"https://github.com/owner{i}/repo{i}",
                "license_tier": "restricted",
                "access": {"license": None},
            }
            for i in range(5)
        ],
    }
    path = _write_corpus(tmp_path, corpus)

    plan = run(
        path,
        create=False,
        limit=1,
        _list=lambda o, r: [],
        _create=None,
        _sleep=lambda n: None,
    )

    assert len(plan) == 1
