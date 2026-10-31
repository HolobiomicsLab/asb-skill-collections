#!/usr/bin/env python3
"""Scan every ref a remote serves before its repository is made public.

Making a private repository public publishes every ref its remote serves, not
only the branch someone checked: GitHub keeps ``refs/pull/<n>/head`` and
``refs/pull/<n>/merge`` for every pull request, open or closed, and a branch
deleted after its merge stays reachable through them. This script lists the
remote's refs with ``git ls-remote``, fetches the objects of any commit missing
from the local repository without writing a ref or ``FETCH_HEAD``, and reads
each commit's tree for three defects:

- an evidence trim receipt (any ``evidence_trim_receipt.json``) that carries a
  span text field, or a string longer than ``--max-string`` characters. Only
  the writer's digest keys may hold a string (``DIGEST_STRING_KEYS``, and the
  DOIs listed under ``strict_dois``); a string under any other key, whatever
  its length, counts as span text, so a quote held as ``raw_block`` or
  ``excerpt`` is reported even when it is short;
- an absolute local path (``/Users/``, ``/home/``, ``/private/``, ``/tmp/`` or
  ``/var/folders/``) in a text file under the ``--paths-in`` pathspecs
  (``receipts`` by default; ``.`` scans the whole tree);
- a routing scaffold ``SKILL.md`` (in a ``_``-prefixed directory) whose YAML
  frontmatter does not parse to a mapping, by the release gate's own rule.

The JSON report gives, per ref, the commit, the files and the counts. A trim
receipt finding is reported by field name, JSON location, length and SHA-256,
never by its text. Absolute path findings quote the matched line, and a
receipt that keys a map by local path yields pointers naming that path: keep
the report out of the repository it describes.

Exit codes: 0 when every ref was scanned and none has a finding, 1 when a ref
has a finding, 2 when a ref could not be scanned or the remote could not be
listed.

    python scripts/scan_remote_refs.py --repo ../asb-skills-genomics --out scan.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p

    sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.release_gate import _frontmatter_error


TRIM_RECEIPT_NAME = "evidence_trim_receipt.json"
# The string fields `collect_from_cut.py` writes into a trim receipt: span rows
# (kind, leaf, tool, build, doi, source, sha256, reason) and the top-level
# description (status, cut_id, order, span_identity, policy_source). Lengths,
# line numbers and flags are not strings. Any other string field is span text.
DIGEST_STRING_KEYS = frozenset({
    "kind", "leaf", "tool", "build", "doi", "source", "sha256", "reason",
    "status", "cut_id", "order", "span_identity", "policy_source",
})
DIGEST_STRING_LISTS = frozenset({"strict_dois"})
DEFAULT_MAX_STRING = 200
DEFAULT_PATHS_IN = ("receipts",)
# Extended regular expression for `git grep -E`: a POSIX root that does not
# follow a word, dot or URL character, so `https://host/home/` does not match.
ABSOLUTE_PATH_ERE = r"(^|[^A-Za-z0-9._~/-])(/Users/|/home/|/private/|/tmp/|/var/folders/)"
LINE_LIMIT = 240


class ScanError(RuntimeError):
    """A git operation the scan depends on failed."""


@dataclass
class RefReport:
    """What one remote ref holds."""

    ref: str
    sha: str
    commit: str | None = None
    scanned: bool = False
    error: str | None = None
    trim_receipts: list[dict[str, Any]] = field(default_factory=list)
    absolute_paths: list[dict[str, Any]] = field(default_factory=list)
    router_frontmatter: list[dict[str, Any]] = field(default_factory=list)

    def findings(self) -> int:
        """Count the defects found on this ref."""
        span_rows = sum(
            len(row["span_text_fields"]) + len(row["long_strings"])
            for row in self.trim_receipts
        )
        return span_rows + len(self.absolute_paths) + len(self.router_frontmatter)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref": self.ref,
            "sha": self.sha,
            "commit": self.commit,
            "scanned": self.scanned,
            "error": self.error,
            "findings": self.findings(),
            "trim_receipts": self.trim_receipts,
            "absolute_paths": self.absolute_paths,
            "router_frontmatter": self.router_frontmatter,
        }


def _git(repo: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ScanError(f"git {' '.join(arguments[:2])} failed: {detail}")
    return result


def list_remote_refs(repo: Path, remote: str) -> list[tuple[str, str]]:
    """Return ``(ref, sha)`` for every ref the remote advertises, peeled tags apart."""
    output = _git(repo, "ls-remote", remote).stdout.decode("utf-8")
    refs = []
    for line in output.splitlines():
        sha, _, ref = line.partition("\t")
        if sha and ref and not ref.endswith("^{}"):
            refs.append((ref, sha))
    return refs


def _commit_of(repo: Path, sha: str) -> str | None:
    result = _git(repo, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}", check=False)
    if result.returncode:
        return None
    return result.stdout.decode("ascii").strip() or None


def fetch_missing(repo: Path, remote: str, refs: list[tuple[str, str]]) -> None:
    """Fetch the objects of refs whose commit is absent, writing no ref.

    An empty ``--refmap`` stops git from updating remote-tracking branches as a
    side effect, and ``--no-write-fetch-head`` keeps ``FETCH_HEAD`` unchanged.
    """
    missing = [ref for ref, sha in refs if ref != "HEAD" and _commit_of(repo, sha) is None]
    if not missing:
        return
    _git(
        repo,
        "fetch",
        "--quiet",
        "--no-tags",
        "--no-write-fetch-head",
        "--refmap=",
        remote,
        *missing,
        check=False,
    )


def _tree_paths(repo: Path, commit: str) -> list[str]:
    output = _git(repo, "ls-tree", "-r", "-z", "--name-only", commit).stdout
    return [path.decode("utf-8", "replace") for path in output.split(b"\0") if path]


def _blob_text(repo: Path, commit: str, path: str) -> str:
    return _git(repo, "show", f"{commit}:{path}").stdout.decode("utf-8", "replace")


def _strings(
    node: Any, pointer: str = "", owner: str | None = None
) -> Iterator[tuple[str, str | None, bool, str]]:
    """Yield ``(json_pointer, key, in_list, value)`` for every string in a JSON value.

    For a string inside a list, ``key`` is the key that holds the list.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{pointer}/{key}"
            if isinstance(value, str):
                yield child, str(key), False, value
            else:
                yield from _strings(value, child, str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            child = f"{pointer}/{index}"
            if isinstance(value, str):
                yield child, owner, True, value
            else:
                yield from _strings(value, child, None)


def _is_digest_string(key: str | None, in_list: bool) -> bool:
    if in_list:
        return key in DIGEST_STRING_LISTS
    return key in DIGEST_STRING_KEYS


def scan_trim_receipt(text: str, max_string: int) -> dict[str, Any]:
    """Describe a trim receipt's span text without quoting it."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return {"error": f"not JSON: {exc.msg}", "span_text_fields": [], "long_strings": [],
                "longest_string": 0}
    span_fields: list[dict[str, Any]] = []
    long_strings: list[dict[str, Any]] = []
    longest = 0
    for pointer, key, in_list, value in _strings(payload):
        longest = max(longest, len(value))
        row = {
            "pointer": pointer,
            "characters": len(value),
            "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
        }
        if not _is_digest_string(key, in_list):
            span_fields.append(row)
        elif len(value) > max_string:
            long_strings.append(row)
    return {
        "span_text_fields": span_fields,
        "span_text_characters": sum(row["characters"] for row in span_fields),
        "long_strings": long_strings,
        "longest_string": longest,
    }


def _absolute_path_hits(repo: Path, commit: str, pathspecs: tuple[str, ...]) -> list[dict[str, Any]]:
    result = _git(
        repo,
        "grep",
        "-I",
        "-n",
        "-z",
        "-E",
        ABSOLUTE_PATH_ERE,
        commit,
        "--",
        *pathspecs,
        check=False,
    )
    if result.returncode not in (0, 1):
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ScanError(f"git grep failed: {detail}")
    hits = []
    prefix = f"{commit}:"
    for line in result.stdout.decode("utf-8", "replace").splitlines():
        # -z output: "<commit>:<path>\0<line>\0<text>"
        parts = line.split("\0", 2)
        if len(parts) != 3:
            continue
        path = parts[0][len(prefix):] if parts[0].startswith(prefix) else parts[0]
        hits.append({"file": path, "line": int(parts[1]), "text": parts[2].strip()[:LINE_LIMIT]})
    return hits


def _is_routing_scaffold(path: str) -> bool:
    pure = PurePosixPath(path)
    return pure.name == "SKILL.md" and pure.parent.name.startswith("_")


def scan_commit(
    repo: Path,
    report: RefReport,
    *,
    max_string: int,
    paths_in: tuple[str, ...],
) -> None:
    """Fill ``report`` with the defects of its commit's tree."""
    commit = report.commit
    if commit is None:
        raise ScanError(f"no local commit for {report.ref}")
    for path in _tree_paths(repo, commit):
        name = PurePosixPath(path).name
        if name == TRIM_RECEIPT_NAME:
            row = {"file": path, **scan_trim_receipt(_blob_text(repo, commit, path), max_string)}
            report.trim_receipts.append(row)
        elif _is_routing_scaffold(path):
            error = _frontmatter_error(_blob_text(repo, commit, path))
            if error:
                report.router_frontmatter.append({"file": path, "error": error})
    report.absolute_paths = _absolute_path_hits(repo, commit, paths_in)
    report.scanned = True


def scan_repository(
    repo: Path,
    remote: str,
    *,
    fetch: bool,
    max_string: int,
    paths_in: tuple[str, ...],
) -> dict[str, Any]:
    """List, fetch and scan every ref of one repository's remote."""
    try:
        refs = list_remote_refs(repo, remote)
    except ScanError as exc:
        return {"repo": repo.name, "remote": remote, "error": str(exc), "refs": []}
    if fetch:
        fetch_missing(repo, remote, refs)
    rows = []
    for ref, sha in refs:
        report = RefReport(ref=ref, sha=sha, commit=_commit_of(repo, sha))
        if report.commit is None:
            report.error = "commit not available locally; run with --fetch"
        else:
            try:
                scan_commit(repo, report, max_string=max_string, paths_in=paths_in)
            except ScanError as exc:
                report.error = str(exc)
        rows.append(report.to_dict())
    return {"repo": repo.name, "remote": remote, "error": None, "refs": rows}


def _exit_code(repositories: list[dict[str, Any]]) -> int:
    if any(repo["error"] for repo in repositories) or any(
        not ref["scanned"] for repo in repositories for ref in repo["refs"]
    ):
        return 2
    if any(ref["findings"] for repo in repositories for ref in repo["refs"]):
        return 1
    return 0


def _summary(repositories: list[dict[str, Any]]) -> dict[str, Any]:
    refs = [ref for repo in repositories for ref in repo["refs"]]
    receipts = [row for ref in refs for row in ref["trim_receipts"]]
    return {
        "repositories": len(repositories),
        "refs": len(refs),
        "refs_scanned": sum(ref["scanned"] for ref in refs),
        "refs_with_findings": sum(bool(ref["findings"]) for ref in refs),
        "trim_receipts": len(receipts),
        "trim_receipts_with_span_text": sum(bool(row["span_text_fields"]) for row in receipts),
        "span_text_characters": sum(row.get("span_text_characters", 0) for row in receipts),
        "longest_trim_receipt_string": max((row["longest_string"] for row in receipts), default=0),
        "absolute_path_lines": sum(len(ref["absolute_paths"]) for ref in refs),
        "unparsable_routers": sum(len(ref["router_frontmatter"]) for ref in refs),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scan_remote_refs.py",
        description=(
            "List every ref a remote serves (refs/pull/* included) and scan each "
            "commit for span text in trim receipts, absolute local paths and "
            "unparsable router frontmatter."
        ),
    )
    parser.add_argument("--repo", type=Path, action="append", required=True,
                        help="Local repository whose remote is scanned (repeatable).")
    parser.add_argument("--remote", default="origin", help="Remote name or URL (default: origin).")
    parser.add_argument("--out", type=Path, required=True, help="Where to write the JSON report.")
    parser.add_argument("--no-fetch", dest="fetch", action="store_false",
                        help="Do not fetch commits missing locally; such refs are reported unscanned.")
    parser.add_argument("--max-string", type=int, default=DEFAULT_MAX_STRING,
                        help=f"Longest string a trim receipt may hold (default: {DEFAULT_MAX_STRING}).")
    parser.add_argument("--paths-in", action="append", default=None,
                        help="Pathspec scanned for absolute paths (repeatable; default: receipts).")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Scan the remotes, write the report, and return 0, 1 or 2."""
    options = _parser().parse_args(argv)
    paths_in = tuple(options.paths_in or DEFAULT_PATHS_IN)
    repositories = [
        scan_repository(
            repo.resolve(),
            options.remote,
            fetch=options.fetch,
            max_string=options.max_string,
            paths_in=paths_in,
        )
        for repo in options.repo
    ]
    report = {
        "schema": "asbb-remote-ref-scan/1.0",
        "max_string": options.max_string,
        "paths_in": list(paths_in),
        "summary": _summary(repositories),
        "repositories": repositories,
    }
    report["exit_code"] = _exit_code(repositories)
    options.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = report["summary"]
    print(
        f"scanned {summary['refs_scanned']}/{summary['refs']} refs in "
        f"{summary['repositories']} repositories; {summary['refs_with_findings']} with findings "
        f"(exit {report['exit_code']})"
    )
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
