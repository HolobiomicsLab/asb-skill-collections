"""Safe-by-default issue-wave tool to request license clarification upstream.

Default (no --create) is a dry-run that prints a plan but NEVER opens an issue.
Pass --create to actually file issues (rate-limited, 2 s between creates).

Usage:
    python3 -m scripts.license_clarification_issues \\
        --corpus collections/metabolomics/v2/corpus.yaml

    python3 -m scripts.license_clarification_issues \\
        --corpus collections/metabolomics/v2/corpus.yaml \\
        --create --limit 5 --out governance/license_clarification/wave.yaml
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Callable

import yaml

from scripts.derive_license_tiers import parse_repo

_COLLECTION_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"


# ---------------------------------------------------------------------------
# candidates
# ---------------------------------------------------------------------------

def candidates(corpus_path: str) -> list[dict]:
    """Return papers that are GitHub-hosted, restricted, and have no detected license.

    Selection criteria (ALL must be true):
    - license_tier == "restricted"
    - repo_url parses to a GitHub (owner, repo) via parse_repo
    - (p.get("access") or {}).get("license") is falsy
    """
    path = pathlib.Path(corpus_path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    result = []
    for p in doc.get("papers", []):
        if p.get("license_tier") != "restricted":
            continue
        repo_url = p.get("repo_url") or ""
        parsed = parse_repo(repo_url)
        if not parsed:
            continue
        # parse_repo returns (owner, repo) for GitHub URLs or 'owner/repo' shorthand,
        # but it also matches non-GitHub shorthand; we must confirm it is GitHub.
        if repo_url and "github.com" not in repo_url and "/" in repo_url:
            # shorthand owner/repo — parse_repo accepts these; treat as GitHub
            # only when there's no explicit hostname that contradicts GitHub.
            # For safety: if an explicit non-github hostname is present, skip.
            pass
        if repo_url and ("gitlab.com" in repo_url or "bitbucket" in repo_url
                         or "sourceforge" in repo_url):
            continue
        if (p.get("access") or {}).get("license"):
            continue
        owner, repo = parsed
        result.append({
            "name": p.get("name", ""),
            "owner": owner,
            "repo": repo,
            "doi": p.get("doi", ""),
        })
    return result


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
        "While cataloguing tools we noticed this repository doesn't appear to carry an explicit open-source license."
        " By default that means \"all rights reserved\", which leaves users unsure whether"
        " (and how) they may use it — including for commercial work.\n\n"
        "Would you be open to clarifying the intended license? Adding an OSI-approved `LICENSE` file"
        " (e.g. MIT / Apache-2.0 / BSD, or GPL/AGPL for copyleft) — or even a one-line note in the README —"
        " would let the community build on your work with confidence."
        " Nothing is required from us; this is just a friendly heads-up, and thank you for the tool! 🙏\n\n"
        "— Holobiomics Lab · ASB skill collection\n\n"
        "<!-- asb-license-clarification -->"
    )
    return title, body


# ---------------------------------------------------------------------------
# already_filed
# ---------------------------------------------------------------------------

def _default_list(owner: str, repo: str) -> list[str]:
    """Shell out to gh to list existing issue titles."""
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
        return []
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
    """File a GitHub issue and return the created issue URL."""
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
) -> list[dict]:
    """Build a plan from candidates and optionally execute it.

    Args:
        corpus_path: Path to corpus.yaml.
        create: If False (default), dry-run — never files issues.
        limit: Max number of candidates to process.
        _list: Injected list function (default: _default_list).
        _create: Injected create function (default: create_issue).
        _sleep: Injected sleep function (default: time.sleep).

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

    cands = candidates(corpus_path)
    if limit is not None:
        cands = cands[:limit]

    plan = []
    first_create = True
    for c in cands:
        owner, repo, name = c["owner"], c["repo"], c["name"]
        title, body = render_issue(name)

        if not create:
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "planned"})
            continue

        # create=True
        skipped = already_filed(owner, repo, _list=_list)
        if skipped:
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "skipped-exists"})
        else:
            if not first_create:
                _sleep(2)
            url = _create(owner, repo, title, body)
            plan.append({"name": name, "owner": owner, "repo": repo, "title": title, "action": "created", "url": url})
            first_create = False

    return plan


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", required=True, help="Path to corpus.yaml")
    ap.add_argument("--create", action="store_true", default=False,
                    help="Actually file issues (default: dry-run)")
    ap.add_argument("--limit", type=int, default=None, metavar="N",
                    help="Cap the number of issues to process")
    ap.add_argument("--out", default="governance/license_clarification/wave.yaml",
                    help="Write plan as YAML to this path")
    args = ap.parse_args(argv)

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
