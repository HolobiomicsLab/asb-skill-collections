"""Safe-by-default issue-wave tool to request license clarification upstream.

Default (no --create) is a dry-run that prints a plan but NEVER opens an issue.
Pass --create to actually file issues (rate-limited, 2 s between creates).

Usage:
    python3 -m scripts.license_clarification_issues \\
        --corpus collections/metabolomics/v2/corpus.yaml

    python3 -m scripts.license_clarification_issues \\
        --corpus collections/metabolomics/v2/corpus.yaml \\
        --create --limit 5 --out governance/license_clarification/wave.yaml

    python3 -m scripts.license_clarification_issues verify
"""
from __future__ import annotations

import datetime
import pathlib
import re
import subprocess
import sys
from typing import Callable

import yaml

from scripts.derive_license_tiers import parse_repo

_COLLECTION_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"

# F1 — safe identifier validator: must start with alphanumeric; allows dash, underscore, dot
# Starting with alphanumeric guards against shell-flag injection (e.g. "--label").
_VALID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")

# F3 — patterns for junk display names that should fall back to repo slug
_DOI_PAT = re.compile(r"^10\.\d")
_FILENAME_PAT = re.compile(r"\.(R|py|jar|ipynb)$")

# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------

LEDGER_PATH = pathlib.Path("governance/license_clarification/deployments.yaml")
_LEDGER_SCHEMA = "license-clarification-deployments/1"


def load_ledger(path: pathlib.Path = LEDGER_PATH) -> dict:
    """Load the deployments ledger, returning an empty-skeleton if missing."""
    if not path.exists():
        return {"schema": _LEDGER_SCHEMA, "deployments": []}
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if doc is None:
        return {"schema": _LEDGER_SCHEMA, "deployments": []}
    return doc


def append_deployment(path: pathlib.Path = LEDGER_PATH, record: dict = None) -> bool:
    """Append *record* to the ledger unless a deployment with the same repo exists.

    Returns True if the record was appended, False if it was a duplicate.
    Writes the updated ledger back to *path*.
    """
    if record is None:
        return False
    ledger = load_ledger(path)
    existing_repos = {d.get("repo") for d in ledger.get("deployments", [])}
    if record.get("repo") in existing_repos:
        return False
    ledger.setdefault("deployments", []).append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return True


# ---------------------------------------------------------------------------
# F3 — _display_name
# ---------------------------------------------------------------------------

def _display_name(name: str | None, repo: str) -> str:
    """Return a human-readable tool name, falling back to repo when name is junk.

    Falls back to `repo` when name is:
    - falsy (None, empty string)
    - equal to "NA"
    - looks like a DOI (starts with "10.")
    - looks like a filename (.R, .py, .jar, .ipynb extension)
    - starts with a non-letter character (e.g. "--", digit-led strings)
    """
    if not name:
        return repo
    if name == "NA":
        return repo
    if _DOI_PAT.match(name):
        return repo
    if _FILENAME_PAT.search(name):
        return repo
    if not name[0].isalpha():
        return repo
    return name


# ---------------------------------------------------------------------------
# candidates
# ---------------------------------------------------------------------------

def candidates(corpus_path: str) -> list[dict]:
    """Return papers that are GitHub-hosted, restricted, and have no detected license.

    Selection criteria (ALL must be true):
    - license_tier == "restricted"
    - repo_url is a github.com URL (F5: positive GitHub-only check)
    - repo_url parses to a valid GitHub (owner, repo) via parse_repo
    - both owner and repo pass _VALID injection guard (F1)
    - (p.get("access") or {}).get("license") is falsy
    - license_detection != "file-present-unclassified" (Task 2: skip if unclassified file exists)

    Deduplication: emits ONE entry per (owner, repo), collecting all tool_names (F2).
    """
    path = pathlib.Path(corpus_path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))

    # ordered dict keyed by (owner, repo) to collect all names (F2 dedup)
    seen: dict[tuple[str, str], dict] = {}

    for p in doc.get("papers", []):
        if p.get("license_tier") != "restricted":
            continue
        repo_url = p.get("repo_url") or ""

        # F5 — positive GitHub-only check:
        # Accept only if github.com is in the URL, OR it is a bare "owner/repo" shorthand
        # with no explicit hostname.
        bare_shorthand = bool(re.match(r"^[\w.-]+/[\w.-]+$", repo_url.strip()))
        if not ("github.com" in repo_url or bare_shorthand):
            continue

        parsed = parse_repo(repo_url)
        if not parsed:
            continue

        if (p.get("access") or {}).get("license"):
            continue

        # Task 2 — skip entries where a license file exists but couldn't be classified
        if p.get("license_detection") == "file-present-unclassified":
            continue

        owner, repo = parsed

        # F1 — injection guard: skip entries with unsafe owner/repo
        if not (_VALID.match(owner) and _VALID.match(repo)):
            continue

        name = p.get("name", "") or ""
        doi = p.get("doi", "")
        key = (owner, repo)

        if key not in seen:
            seen[key] = {
                "name": _display_name(name, repo),
                "owner": owner,
                "repo": repo,
                "doi": doi,
                "tool_names": [name] if name else [],
            }
        else:
            # F2 — accumulate tool names; upgrade display name if current is junk
            if name and name not in seen[key]["tool_names"]:
                seen[key]["tool_names"].append(name)
            # upgrade to a better display name if current one fell back to repo
            if seen[key]["name"] == repo and _display_name(name, repo) != repo:
                seen[key]["name"] = _display_name(name, repo)

    return list(seen.values())


# ---------------------------------------------------------------------------
# render_issue
# ---------------------------------------------------------------------------

def render_issue(
    tool_name: str,
    collection_url: str = _COLLECTION_URL,
) -> tuple[str, str]:
    """Return (title, body) for a license-clarification issue."""
    title = f"License clarification for {tool_name}?"
    body = (
        f"Hi! 👋 We maintain the open **ASB Metabolomics skill collection** ({collection_url}),"
        f" which references **{tool_name}** as a community method/tool for computational metabolomics.\n\n"
        "While cataloguing tools we couldn't find an explicit open-source license for this repository."
        " **If we missed it, could you point us to the license?** And if there isn't one yet, would you consider adding one?\n\n"
        "Without a clear license the default is \"all rights reserved\", which leaves users unsure whether"
        " (and how) they may use your work — including for commercial use. An OSI-approved `LICENSE` file"
        " (e.g. MIT / Apache-2.0 / BSD, or GPL/AGPL for copyleft), or even a one-line note in the README, resolves it."
        " Nothing is required from us — just a friendly heads-up, and thank you for the tool! 🙏\n\n"
        "— Holobiomics Lab · ASB skill collection\n\n"
        "<!-- asb-license-clarification -->"
    )
    return title, body


# ---------------------------------------------------------------------------
# already_filed
# ---------------------------------------------------------------------------

def _default_list(owner: str, repo: str) -> list[str]:
    """Shell out to gh to list existing issue titles.

    Raises RuntimeError (F4) on non-zero returncode so callers cannot silently
    skip duplicate-prevention.
    """
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--repo", f"{owner}/{repo}",
            "--state", "all",
            "--search", "License clarification",
            "--json", "title",
            "-q", ".[].title",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh issue list failed for {owner}/{repo} (exit {result.returncode}): "
            f"{result.stderr.strip()}"
        )
    return [line for line in result.stdout.splitlines() if line.strip()]


def already_filed(
    owner: str,
    repo: str,
    _list: Callable[[str, str], list[str]] = _default_list,
) -> bool:
    """Return True if a prior clarification issue exists in the repo."""
    titles = _list(owner, repo)
    return any(t.startswith("License clarification for") for t in titles)


# ---------------------------------------------------------------------------
# create_issue
# ---------------------------------------------------------------------------

def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    _run=subprocess.run,
) -> str:
    """File a GitHub issue and return the created issue URL.

    Raises ValueError (F1) if owner or repo contains unsafe characters.
    The guard runs BEFORE any subprocess call.
    """
    # F1 — injection guard (must be first, before any subprocess call)
    if not (_VALID.match(owner) and _VALID.match(repo)):
        raise ValueError(f"unsafe repo identifier: {owner}/{repo}")

    result = _run(
        [
            "gh", "issue", "create",
            "--repo", f"{owner}/{repo}",
            "--title", title,
            "--body", body,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

def run(
    corpus_path: str,
    create: bool = False,
    limit: int | None = None,
    _list: Callable[[str, str], list[str]] | None = None,
    _create: Callable | None = None,
    _sleep: Callable | None = None,
    ledger_path: pathlib.Path = LEDGER_PATH,
    wave_label: str = "manual",
    today: str | None = None,
    _append: Callable = append_deployment,
) -> list[dict]:
    """Build a plan from candidates and optionally execute it.

    Args:
        corpus_path: Path to corpus.yaml.
        create: If False (default), dry-run — never files issues.
        limit: Max number of candidates to process.
        _list: Injected list function (default: _default_list).
        _create: Injected create function (default: create_issue).
        _sleep: Injected sleep function (default: time.sleep).
        ledger_path: Path to deployments.yaml ledger.
        wave_label: Wave identifier stored in the ledger record.
        today: ISO date string for filed_on (default: today).
        _append: Injected append function (default: append_deployment).

    Returns:
        List of dicts with keys: name, owner, repo, title, action, [url].
    """
    import time

    if _list is None:
        _list = _default_list
    if _create is None:
        _create = create_issue
    if _sleep is None:
        _sleep = time.sleep
    if today is None:
        today = datetime.date.today().isoformat()

    # F7 — guard _create is callable when create=True
    if create:
        assert _create is not None, "_create must not be None when create=True"

    cands = candidates(corpus_path)
    if limit is not None:
        cands = cands[:limit]

    plan = []
    created_count = 0  # F6 — counter instead of first_create flag
    for c in cands:
        owner, repo, name = c["owner"], c["repo"], c["name"]
        title, body = render_issue(name)

        if not create:
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "planned"})
            continue

        # create=True
        try:
            skipped = already_filed(owner, repo, _list=_list)
        except RuntimeError:
            # F4 — don't swallow list failures; mark as skipped-error and continue
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "skipped-error"})
            continue

        if skipped:
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "skipped-exists"})
        else:
            # F6 — sleep before every create after the first actual create
            if created_count > 0:
                _sleep(2)
            url = _create(owner, repo, title, body)
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "created", "url": url})
            created_count += 1  # F6 — increment on each successful create

            # Append to ledger (dry-run=False only)
            _append(
                ledger_path,
                {
                    "repo": f"{owner}/{repo}",
                    "tool_names": c.get("tool_names", [name]),
                    "doi": c.get("doi") or None,
                    "issue_url": url,
                    "filed_on": today,
                    "wave": wave_label,
                    "status": "open",
                    "license_after": None,
                    "last_checked": None,
                },
            )

    return plan


# ---------------------------------------------------------------------------
# verify_deployments
# ---------------------------------------------------------------------------

def _default_issue_state(issue_url: str) -> dict:
    """Fetch issue state and comments count via gh CLI."""
    result = subprocess.run(
        [
            "gh", "issue", "view", issue_url,
            "--json", "state,comments",
            "-q", "{state: .state, comments: (.comments | length)}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {"state": "unknown", "comments": 0}
    import json
    try:
        return json.loads(result.stdout.strip())
    except Exception:
        return {"state": "unknown", "comments": 0}


def _default_repo_license(owner: str, repo: str) -> str | None:
    """Fetch the SPDX license identifier for owner/repo via gh CLI."""
    result = subprocess.run(
        [
            "gh", "repo", "view", f"{owner}/{repo}",
            "--json", "licenseInfo",
            "-q", ".licenseInfo.spdxId // empty",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    spdx = result.stdout.strip()
    if not spdx or spdx.upper() == "NOASSERTION":
        return None
    return spdx


def verify_deployments(
    ledger_path: pathlib.Path = LEDGER_PATH,
    _issue_state: Callable | None = None,
    _repo_license: Callable | None = None,
    today: str | None = None,
) -> dict:
    """Check each deployment and update status/license_after in the ledger.

    Args:
        ledger_path: Path to deployments.yaml.
        _issue_state: Injected fn(issue_url) -> {"state": str, "comments": int}.
        _repo_license: Injected fn(owner, repo) -> spdx_id | None.
        today: ISO date string for last_checked (default: today).

    Returns:
        Summary dict mapping status -> count.
    """
    if _issue_state is None:
        _issue_state = _default_issue_state
    if _repo_license is None:
        _repo_license = _default_repo_license
    if today is None:
        today = datetime.date.today().isoformat()

    ledger = load_ledger(ledger_path)
    deployments = ledger.get("deployments", [])

    summary: dict[str, int] = {}
    for d in deployments:
        d["last_checked"] = today
        repo_slug = d.get("repo", "")
        owner, _, repo = repo_slug.partition("/")

        # Check if repo now has a license
        spdx = _repo_license(owner, repo) if (owner and repo) else None
        if spdx:
            d["status"] = "license-added"
            d["license_after"] = spdx
        else:
            # Check issue state
            issue_url = d.get("issue_url", "")
            state_info = _issue_state(issue_url) if issue_url else {"state": "unknown", "comments": 0}
            issue_state = state_info.get("state", "unknown")
            comments = state_info.get("comments", 0)

            if issue_state == "CLOSED":
                d["status"] = "closed"
            elif comments and int(comments) > 0:
                d["status"] = "responded"
            # else keep existing status (open or whatever it was)

        summary[d["status"]] = summary.get(d["status"], 0) + 1

    # Write back
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(
        yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return summary


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    import argparse

    # Dispatch to verify subcommand before full argparse
    _argv = argv if argv is not None else sys.argv[1:]
    if _argv and _argv[0] == "verify":
        summary = verify_deployments()
        print("Verify summary:")
        for status, count in sorted(summary.items()):
            print(f"  {status}: {count}")
        newly_notable = [
            d for d in load_ledger().get("deployments", [])
            if d.get("status") in ("license-added", "responded")
        ]
        if newly_notable:
            print("\nNotable updates:")
            for d in newly_notable:
                print(f"  {d['repo']}  status={d['status']}  license_after={d.get('license_after')}")
        return 0

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", required=True, help="Path to corpus.yaml")
    ap.add_argument("--create", action="store_true", default=False,
                    help="Actually file issues (default: dry-run)")
    ap.add_argument("--limit", type=int, default=None, metavar="N",
                    help="Cap the number of issues to process")
    ap.add_argument("--out", default="governance/license_clarification/wave.yaml",
                    help="Write plan as YAML to this path")
    args = ap.parse_args(_argv)

    if args.create:
        print("⚠️  --create is set: issues WILL be filed. Ctrl-C to abort.")
    else:
        print("ℹ️  Dry-run mode (default). Pass --create to file issues.")

    plan = run(
        args.corpus,
        create=args.create,
        limit=args.limit,
    )

    # Write output YAML
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        yaml.safe_dump({"plan": plan}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"→ Plan written to {out_path}")

    counts: dict[str, int] = {}
    for item in plan:
        counts[item["action"]] = counts.get(item["action"], 0) + 1

    print("\nSummary:")
    for action, n in sorted(counts.items()):
        print(f"  {action}: {n}")
    print(f"  total candidates: {len(plan)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
