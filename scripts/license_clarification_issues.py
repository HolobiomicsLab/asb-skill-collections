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
