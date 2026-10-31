"""Public docs and scripts must not carry a maintainer's local paths.

This repository is public. A path such as ``/Users/<name>/git/...`` in a doc
tells a reader nothing they can open, and it publishes the layout of one
maintainer's machine. Two docs pointed readers at a specification under such a
path, and one release-train step named a checkout under ``~/git/``.

The guard scans every tracked text file under ``docs/`` and ``scripts/`` for a
home directory written out (``/Users/<name>/``, ``/home/<name>/``) or the
``~/git/`` checkout layout. Code that *matches* such paths in order to redact
them (``/Users/|/home/``) is not a path and is not reported, because the
pattern requires a name segment after the home prefix.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCANNED = ("docs", "scripts")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".txt", ".html", ".js", ".toml"}

LOCAL_PATH = re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|~/git/")

# Files whose local defaults are removed by a separate change. The collector's
# --builds-root and --corpus become required arguments with no default there;
# remove the entry once that change is merged.
PENDING = {"scripts/collect_metabolomics_collection.py"}


def tracked_text_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", *SCANNED],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    return [p for p in out.splitlines() if pathlib.PurePosixPath(p).suffix in TEXT_SUFFIXES]


def local_paths(text: str) -> list[tuple[int, str]]:
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = LOCAL_PATH.search(line)
        if match:
            hits.append((number, match.group(0)))
    return hits


@pytest.mark.parametrize(
    "line",
    [
        "see `/Users/someone/git/project/SPEC.md`",
        "default=\"/home/someone/data/batch.json\"",
        "Pin a commit: `~/git/indicium` has no tags",
    ],
)
def test_pattern_reports_a_local_path(line):
    assert local_paths(line)


@pytest.mark.parametrize(
    "line",
    [
        r'("path", re.compile(r"(?:/Users/|/home/|/private/|~/)[^\s]+"), "[path]"),',
        "file paths (/Users/…, /home/…, ~/…) and the username in them",
        "git clone https://github.com/HolobiomicsLab/asb-skill-collections",
    ],
)
def test_pattern_ignores_redaction_code_and_urls(line):
    assert not local_paths(line)


def test_docs_and_scripts_carry_no_local_path():
    files = tracked_text_files()
    assert any(f.startswith("docs/") for f in files), "no tracked file under docs/"
    offenders = []
    for rel in files:
        if rel in PENDING:
            continue
        text = (REPO / rel).read_text(encoding="utf-8", errors="replace")
        offenders.extend(f"{rel}:{n}: {hit}" for n, hit in local_paths(text))
    assert not offenders, (
        "local paths in public docs or scripts; name the resource instead "
        "(for example 'the ASB specification (private repository, to be "
        "published)'):\n  " + "\n  ".join(offenders)
    )
