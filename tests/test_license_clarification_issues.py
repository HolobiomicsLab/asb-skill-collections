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
    assert "point us to the license" in body
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
        _append=lambda path, record: True,  # prevent writing to real ledger
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
        _append=lambda path, record: True,  # prevent writing to real ledger
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


# ---------------------------------------------------------------------------
# F1 — Injection guard: create_issue raises on unsafe identifiers
# ---------------------------------------------------------------------------

def test_create_issue_raises_on_unsafe_owner():
    from scripts.license_clarification_issues import create_issue

    with pytest.raises(ValueError, match="unsafe repo identifier"):
        create_issue("--label", "repo", "title", "body")


def test_create_issue_raises_on_unsafe_repo():
    from scripts.license_clarification_issues import create_issue

    with pytest.raises(ValueError, match="unsafe repo identifier"):
        create_issue("owner", "repo;evil", "title", "body")


def test_candidates_excludes_invalid_owner_repo(tmp_path):
    """A corpus entry whose parsed owner fails _VALID must be excluded."""
    from scripts.license_clarification_issues import candidates

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "BadTool",
                "doi": "10.1000/bad",
                # craft a URL that parse_repo might accept but has bad chars in owner
                "repo_url": "https://github.com/--label/repo",
                "license_tier": "restricted",
                "access": {"license": None},
            },
            {
                "name": "GoodTool",
                "doi": "10.1000/good",
                "repo_url": "https://github.com/owner1/repoA",
                "license_tier": "restricted",
                "access": {"license": None},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)
    result = candidates(path)

    names = [c["name"] for c in result]
    assert "BadTool" not in names
    assert "GoodTool" in names


# ---------------------------------------------------------------------------
# F2 — Same-repo dedup: multiple corpus entries → one candidate per (owner, repo)
# ---------------------------------------------------------------------------

def test_candidates_deduplicates_same_repo(tmp_path):
    """Two restricted github-no-license entries sharing one repo → ONE candidate."""
    from scripts.license_clarification_issues import candidates

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "ToolAlpha",
                "doi": "10.1000/alpha",
                "repo_url": "https://github.com/sharedowner/sharedrepo",
                "license_tier": "restricted",
                "access": {"license": None},
            },
            {
                "name": "ToolBeta",
                "doi": "10.1000/beta",
                "repo_url": "https://github.com/sharedowner/sharedrepo",
                "license_tier": "restricted",
                "access": {"license": None},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)
    result = candidates(path)

    assert len(result) == 1
    assert result[0]["owner"] == "sharedowner"
    assert result[0]["repo"] == "sharedrepo"
    tool_names = result[0]["tool_names"]
    assert set(tool_names) == {"ToolAlpha", "ToolBeta"}


# ---------------------------------------------------------------------------
# F3 — Robust display name: _display_name fallback to repo
# ---------------------------------------------------------------------------

def test_display_name_na_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("NA", "QCCAssisted4DSterol") == "QCCAssisted4DSterol"


def test_display_name_filename_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("wscaling.R", "x") == "x"


def test_display_name_good_name_passes_through():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("Spec2Vec", "x") == "Spec2Vec"


def test_display_name_doi_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("10.1021/abc", "myrepo") == "myrepo"


def test_display_name_falsy_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("", "myrepo") == "myrepo"
    assert _display_name(None, "myrepo") == "myrepo"


def test_display_name_ipynb_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("analysis.ipynb", "myrepo") == "myrepo"


def test_display_name_py_falls_back_to_repo():
    from scripts.license_clarification_issues import _display_name

    assert _display_name("run.py", "myrepo") == "myrepo"


# ---------------------------------------------------------------------------
# Task 2 — candidates() excludes file-present-unclassified
# ---------------------------------------------------------------------------

def test_candidates_excludes_file_present_unclassified(tmp_path):
    """Entry with license_detection='file-present-unclassified' must be excluded."""
    from scripts.license_clarification_issues import candidates

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "NoLic",
                "doi": "10.1/a",
                "repo_url": "https://github.com/a/nolic",
                "license_tier": "restricted",
                "license_detection": "none",
                "access": {},
            },
            {
                "name": "HasFile",
                "doi": "10.1/b",
                "repo_url": "https://github.com/b/hasfile",
                "license_tier": "restricted",
                "license_detection": "file-present-unclassified",
                "access": {},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)
    result = candidates(path)

    names = {c["repo"] for c in result}
    assert "nolic" in names and "hasfile" not in names


# ---------------------------------------------------------------------------
# F4 — _default_list raises RuntimeError on non-zero returncode;
#       run() catches it and marks action="skipped-error"
# ---------------------------------------------------------------------------

def test_run_skips_on_list_error(tmp_path):
    """A _list that raises RuntimeError → action='skipped-error'; _create not called."""
    from scripts.license_clarification_issues import run

    create_called = []

    def _raising_list(o, r):
        raise RuntimeError("gh failed: permission denied")

    def _fake_create(owner, repo, title, body, _run=None):
        create_called.append((owner, repo))
        return f"https://github.com/{owner}/{repo}/issues/1"

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
        ],
    }
    path = _write_corpus(tmp_path, corpus)

    plan = run(
        path,
        create=True,
        _list=_raising_list,
        _create=_fake_create,
        _sleep=lambda n: None,
        _append=lambda path, record: True,  # prevent writing to real ledger
    )

    assert len(plan) == 1
    assert plan[0]["action"] == "skipped-error"
    assert len(create_called) == 0


# ---------------------------------------------------------------------------
# F5 — GitHub-only host check: codeberg.org excluded
# ---------------------------------------------------------------------------

def test_candidates_excludes_codeberg(tmp_path):
    """A codeberg.org URL must be excluded even if parse_repo accepts it."""
    from scripts.license_clarification_issues import candidates

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "CodebergTool",
                "doi": "10.1000/cb",
                "repo_url": "https://codeberg.org/owner/repo",
                "license_tier": "restricted",
                "access": {"license": None},
            },
            {
                "name": "GithubTool",
                "doi": "10.1000/gh",
                "repo_url": "https://github.com/owner2/repoG",
                "license_tier": "restricted",
                "access": {"license": None},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)
    result = candidates(path)

    names = [c["name"] for c in result]
    assert "CodebergTool" not in names
    assert "GithubTool" in names


# ---------------------------------------------------------------------------
# F6 — Sleep before every create AFTER the first; leading skip doesn't waste pause
# ---------------------------------------------------------------------------

def test_sleep_called_before_second_create_not_first(tmp_path):
    """Sleep is called before the 2nd create, not before the 1st."""
    from scripts.license_clarification_issues import run

    sleep_calls = []
    create_calls = []

    def _fake_sleep(n):
        sleep_calls.append(n)

    def _fake_create(owner, repo, title, body, _run=None):
        create_calls.append((owner, repo))
        return f"https://github.com/{owner}/{repo}/issues/1"

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": f"Tool{i}",
                "doi": f"10.1000/{i}",
                "repo_url": f"https://github.com/owner{i}/repo{i}",
                "license_tier": "restricted",
                "access": {"license": None},
            }
            for i in range(3)
        ],
    }
    path = _write_corpus(tmp_path, corpus)

    plan = run(
        path,
        create=True,
        _list=lambda o, r: [],  # no pre-existing issues
        _create=_fake_create,
        _sleep=_fake_sleep,
        _append=lambda path, record: True,  # prevent writing to real ledger
    )

    # 3 creates happened
    assert len(create_calls) == 3
    # sleep called exactly twice (before 2nd and 3rd creates, not before 1st)
    assert len(sleep_calls) == 2


def test_sleep_not_called_when_first_entry_skipped(tmp_path):
    """If first entry is skipped-exists, first real create should have no sleep."""
    from scripts.license_clarification_issues import run

    sleep_calls = []
    create_calls = []

    def _fake_sleep(n):
        sleep_calls.append(n)

    def _fake_create(owner, repo, title, body, _run=None):
        create_calls.append((owner, repo))
        return f"https://github.com/{owner}/{repo}/issues/1"

    corpus = {
        "schema": "asb-corpus/1.0",
        "papers": [
            {
                "name": "SkipMe",
                "doi": "10.1000/skip",
                "repo_url": "https://github.com/owner0/repo0",
                "license_tier": "restricted",
                "access": {"license": None},
            },
            {
                "name": "CreateMe",
                "doi": "10.1000/create",
                "repo_url": "https://github.com/owner1/repo1",
                "license_tier": "restricted",
                "access": {"license": None},
            },
        ],
    }
    path = _write_corpus(tmp_path, corpus)

    def _fake_list(o, r):
        if r == "repo0":
            return ["License clarification for SkipMe?"]
        return []

    plan = run(
        path,
        create=True,
        _list=_fake_list,
        _create=_fake_create,
        _sleep=_fake_sleep,
        _append=lambda path, record: True,  # prevent writing to real ledger
    )

    # SkipMe skipped, CreateMe created
    actions = {item["name"]: item["action"] for item in plan}
    assert actions["SkipMe"] == "skipped-exists"
    assert actions["CreateMe"] == "created"

    # No sleep before the first (and only) create
    assert len(sleep_calls) == 0
    assert len(create_calls) == 1


# ---------------------------------------------------------------------------
# Ledger — load_ledger / append_deployment
# ---------------------------------------------------------------------------

def test_load_ledger_returns_empty_skeleton_when_missing(tmp_path):
    """load_ledger returns the empty schema skeleton when the file doesn't exist."""
    from scripts.license_clarification_issues import load_ledger

    ledger_path = tmp_path / "deployments.yaml"
    result = load_ledger(ledger_path)
    assert result["schema"] == "license-clarification-deployments/1"
    assert result["deployments"] == []


def test_append_deployment_appends_new_repo(tmp_path):
    """append_deployment adds a new record and returns True."""
    from scripts.license_clarification_issues import append_deployment, load_ledger

    ledger_path = tmp_path / "deps.yaml"
    record = {
        "repo": "owner1/repoA",
        "tool_names": ["ToolA"],
        "doi": "10.1000/aaa",
        "issue_url": "https://github.com/owner1/repoA/issues/1",
        "filed_on": "2026-06-24",
        "wave": "trial-2026-06-24",
        "status": "open",
        "license_after": None,
        "last_checked": None,
    }
    result = append_deployment(ledger_path, record)
    assert result is True

    ledger = load_ledger(ledger_path)
    assert len(ledger["deployments"]) == 1
    assert ledger["deployments"][0]["repo"] == "owner1/repoA"


def test_append_deployment_dedup_same_repo(tmp_path):
    """append_deployment returns False and does NOT duplicate when repo already exists."""
    from scripts.license_clarification_issues import append_deployment, load_ledger

    ledger_path = tmp_path / "deps.yaml"
    record = {
        "repo": "owner1/repoA",
        "tool_names": ["ToolA"],
        "doi": "10.1000/aaa",
        "issue_url": "https://github.com/owner1/repoA/issues/1",
        "filed_on": "2026-06-24",
        "wave": "trial",
        "status": "open",
        "license_after": None,
        "last_checked": None,
    }
    append_deployment(ledger_path, record)
    second_result = append_deployment(ledger_path, record)

    assert second_result is False
    ledger = load_ledger(ledger_path)
    assert len(ledger["deployments"]) == 1  # still only 1


# ---------------------------------------------------------------------------
# Ledger — run() wires _append on created issues, skips on dry-run
# ---------------------------------------------------------------------------

def test_run_create_true_appends_to_ledger(tmp_path):
    """run(create=True) calls _append once per created issue."""
    from scripts.license_clarification_issues import run

    append_calls = []

    def _spy_append(path, record):
        append_calls.append(record)
        return True

    def _fake_create(owner, repo, title, body, _run=None):
        return f"https://github.com/{owner}/{repo}/issues/42"

    path = _write_corpus(tmp_path)  # 1 candidate: owner1/repoA

    plan = run(
        path,
        create=True,
        _list=lambda o, r: [],
        _create=_fake_create,
        _sleep=lambda n: None,
        ledger_path=tmp_path / "deps.yaml",
        wave_label="test-wave",
        today="2026-06-24",
        _append=_spy_append,
    )

    created = [item for item in plan if item["action"] == "created"]
    assert len(created) == 1
    assert len(append_calls) == 1

    rec = append_calls[0]
    assert rec["repo"] == "owner1/repoA"
    assert rec["wave"] == "test-wave"
    assert rec["filed_on"] == "2026-06-24"
    assert rec["status"] == "open"
    assert rec["issue_url"] == "https://github.com/owner1/repoA/issues/42"


def test_run_dry_run_does_not_append(tmp_path):
    """run(create=False) never calls _append."""
    from scripts.license_clarification_issues import run

    append_calls = []

    def _spy_append(path, record):
        append_calls.append(record)
        return True

    path = _write_corpus(tmp_path)

    run(
        path,
        create=False,
        _list=lambda o, r: [],
        _create=None,
        _sleep=lambda n: None,
        ledger_path=tmp_path / "deps.yaml",
        _append=_spy_append,
    )

    assert len(append_calls) == 0


# ---------------------------------------------------------------------------
# verify_deployments
# ---------------------------------------------------------------------------

def _make_ledger(tmp_path, deployments: list[dict]) -> "pathlib.Path":
    import pathlib
    p = tmp_path / "deployments.yaml"
    doc = {
        "schema": "license-clarification-deployments/1",
        "deployments": deployments,
    }
    p.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return p


def test_verify_license_added(tmp_path):
    """Repo that now has a license → status=license-added, license_after=MIT."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "owner1/repoA",
            "tool_names": ["ToolA"],
            "doi": "10.x/y",
            "issue_url": "https://github.com/owner1/repoA/issues/1",
            "filed_on": "2026-06-24",
            "wave": "trial",
            "status": "open",
            "license_after": None,
            "last_checked": None,
        }
    ])

    summary = verify_deployments(
        ledger_path=ledger_path,
        _issue_state=lambda url: {"state": "OPEN", "comments": 0},
        _repo_license=lambda o, r: "MIT",
        today="2026-06-24",
    )

    assert summary.get("license-added") == 1

    ledger = yaml.safe_load(ledger_path.read_text())
    d = ledger["deployments"][0]
    assert d["status"] == "license-added"
    assert d["license_after"] == "MIT"
    assert d["last_checked"] == "2026-06-24"


def test_verify_closed_issue(tmp_path):
    """Closed issue with no license → status=closed."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "owner2/repoB",
            "tool_names": ["ToolB"],
            "doi": None,
            "issue_url": "https://github.com/owner2/repoB/issues/5",
            "filed_on": "2026-06-24",
            "wave": "trial",
            "status": "open",
            "license_after": None,
            "last_checked": None,
        }
    ])

    summary = verify_deployments(
        ledger_path=ledger_path,
        _issue_state=lambda url: {"state": "CLOSED", "comments": 0},
        _repo_license=lambda o, r: None,
        today="2026-06-24",
    )

    assert summary.get("closed") == 1
    ledger = yaml.safe_load(ledger_path.read_text())
    assert ledger["deployments"][0]["status"] == "closed"


def test_verify_responded(tmp_path):
    """Open issue with comments > 0 → status=responded."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "owner3/repoC",
            "tool_names": ["ToolC"],
            "doi": None,
            "issue_url": "https://github.com/owner3/repoC/issues/7",
            "filed_on": "2026-06-24",
            "wave": "trial",
            "status": "open",
            "license_after": None,
            "last_checked": None,
        }
    ])

    summary = verify_deployments(
        ledger_path=ledger_path,
        _issue_state=lambda url: {"state": "OPEN", "comments": 2},
        _repo_license=lambda o, r: None,
        today="2026-06-24",
    )

    assert summary.get("responded") == 1
    ledger = yaml.safe_load(ledger_path.read_text())
    assert ledger["deployments"][0]["status"] == "responded"


def test_verify_still_open(tmp_path):
    """Open issue, no comments, no license → status stays open."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "owner4/repoD",
            "tool_names": ["ToolD"],
            "doi": None,
            "issue_url": "https://github.com/owner4/repoD/issues/3",
            "filed_on": "2026-06-24",
            "wave": "trial",
            "status": "open",
            "license_after": None,
            "last_checked": None,
        }
    ])

    summary = verify_deployments(
        ledger_path=ledger_path,
        _issue_state=lambda url: {"state": "OPEN", "comments": 0},
        _repo_license=lambda o, r: None,
        today="2026-06-24",
    )

    assert summary.get("open") == 1
    ledger = yaml.safe_load(ledger_path.read_text())
    assert ledger["deployments"][0]["status"] == "open"
    assert ledger["deployments"][0]["last_checked"] == "2026-06-24"


def test_verify_mixed_summary(tmp_path):
    """Mixed deployments produce correct summary counts."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "o/r1", "tool_names": [], "doi": None,
            "issue_url": "https://github.com/o/r1/issues/1",
            "filed_on": "2026-06-24", "wave": "t", "status": "open",
            "license_after": None, "last_checked": None,
        },
        {
            "repo": "o/r2", "tool_names": [], "doi": None,
            "issue_url": "https://github.com/o/r2/issues/2",
            "filed_on": "2026-06-24", "wave": "t", "status": "open",
            "license_after": None, "last_checked": None,
        },
        {
            "repo": "o/r3", "tool_names": [], "doi": None,
            "issue_url": "https://github.com/o/r3/issues/3",
            "filed_on": "2026-06-24", "wave": "t", "status": "open",
            "license_after": None, "last_checked": None,
        },
        {
            "repo": "o/r4", "tool_names": [], "doi": None,
            "issue_url": "https://github.com/o/r4/issues/4",
            "filed_on": "2026-06-24", "wave": "t", "status": "open",
            "license_after": None, "last_checked": None,
        },
    ])

    def _fake_license(o, r):
        if r == "r1":
            return "Apache-2.0"
        return None

    def _fake_state(url):
        if "r2" in url:
            return {"state": "CLOSED", "comments": 0}
        if "r3" in url:
            return {"state": "OPEN", "comments": 3}
        return {"state": "OPEN", "comments": 0}

    summary = verify_deployments(
        ledger_path=ledger_path,
        _issue_state=_fake_state,
        _repo_license=_fake_license,
        today="2026-06-24",
    )

    assert summary.get("license-added") == 1
    assert summary.get("closed") == 1
    assert summary.get("responded") == 1
    assert summary.get("open") == 1


def test_verify_writes_ledger_back(tmp_path):
    """verify_deployments writes the updated ledger back to disk."""
    from scripts.license_clarification_issues import verify_deployments

    ledger_path = _make_ledger(tmp_path, [
        {
            "repo": "o/r1", "tool_names": [], "doi": None,
            "issue_url": "https://github.com/o/r1/issues/1",
            "filed_on": "2026-06-24", "wave": "t", "status": "open",
            "license_after": None, "last_checked": None,
        }
    ])

    verify_deployments(
        ledger_path=ledger_path,
        _issue_state=lambda url: {"state": "OPEN", "comments": 0},
        _repo_license=lambda o, r: None,
        today="2026-07-01",
    )

    ledger = yaml.safe_load(ledger_path.read_text())
    assert ledger["deployments"][0]["last_checked"] == "2026-07-01"
