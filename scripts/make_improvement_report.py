#!/usr/bin/env python3
"""Package an anonymized skill/workflow improvement report for the community.

The other half of the flywheel: when an agent (or its user) exercises a skill and
finds a fix — a wrong default, a missing step, an outdated tool, a better
procedure — this turns that into a clean, **anonymized** contribution: a Markdown
issue body and a pre-filled GitHub "new issue" URL the user can open with one
click (and a reviewer can later promote to a PR).

Anonymization is non-negotiable and follows the project's telemetry privacy stance
(`docs/design/skill-load-telemetry.md`: no user IDs, no file paths, nothing that
reconstructs an individual session). Free text is scrubbed of:
  * file paths (/Users/…, /home/…, ~/…, /private/…, C:\\…) and the username in them
  * email addresses and IP addresses
  * API keys / bearer tokens / `key=…`, `token=…`, `secret=…`, `password=…` pairs
The report records *what categories* were redacted (counts only) for transparency.

It is content-only: no machine info, no timestamps finer than the date.

Usage
-----
  python scripts/make_improvement_report.py \
      --collection metabolomics/v2 --skill feature-detection-xcms \
      --kind correction \
      --summary "Default ppm tolerance is too tight for Orbitrap data" \
      --detail "Steps 3-4 suggest 5 ppm; the source paper uses 10 ppm for ..." \
      [--diff path/to/change.patch] [--runtime claude-code] \
      [--repo HolobiomicsLab/asb-skill-collections] [--out report.md] [--print-url]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.parse

KINDS = ["correction", "enhancement", "new-skill", "bug", "tool-update", "other"]

# (label, compiled pattern, replacement) — general shapes only, never specific tokens.
_SCRUBBERS = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[email]"),
    ("ip", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "[ip]"),
    ("path", re.compile(r"(?:/Users/|/home/|/private/|~/)[^\s\"'`]+"), "[path]"),
    ("path", re.compile(r"\b[A-Za-z]:\\[^\s\"'`]+"), "[path]"),
    ("path", re.compile(r"(?<![\w.])/(?:usr|var|tmp|opt|etc|mnt|srv)/[^\s\"'`]+"), "[path]"),
    ("secret", re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"), "[secret]"),
    ("secret", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{12,}", re.I), "Bearer [secret]"),
    ("secret", re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?key|secret[_-]?key|token|secret|password|passwd|pwd|key)\b"
        r"\s*[:=]\s*\S+"), r"\1=[secret]"),
]


def scrub(text: str) -> tuple[str, dict[str, int]]:
    """Redact PII/secrets/paths. Returns (clean_text, {category: count})."""
    counts: dict[str, int] = {}
    out = text or ""
    for label, pat, repl in _SCRUBBERS:
        out, n = pat.subn(repl, out)
        if n:
            counts[label] = counts.get(label, 0) + n
    return out, counts


def build_report(
    collection: str,
    skill: str,
    kind: str,
    summary: str,
    detail: str,
    diff: str | None,
    runtime: str | None,
    target: str,
) -> tuple[str, dict[str, int]]:
    redacted: dict[str, int] = {}

    def _clean(t: str) -> str:
        c, counts = scrub(t)
        for k, v in counts.items():
            redacted[k] = redacted.get(k, 0) + v
        return c

    clean_summary = _clean(summary)
    clean_detail = _clean(detail or "")
    clean_diff = _clean(diff) if diff else ""

    item_label = "workflow" if target == "workflows" else "skill"
    lines = [
        f"## Improvement report — `{skill}`",
        "",
        f"- **collection:** `{collection}`",
        f"- **{item_label}:** `{skill}`",
        f"- **kind:** {kind}",
    ]
    if runtime:
        lines.append(f"- **agent runtime:** {runtime}")
    lines += [
        "",
        "### Summary",
        clean_summary or "_(none)_",
        "",
        "### Detail",
        clean_detail or "_(none)_",
    ]
    if clean_diff:
        lines += ["", "### Proposed change", "```diff", clean_diff, "```"]
    lines += [
        "",
        "---",
        "_Auto-generated, anonymized improvement report. "
        + (f"Redacted: {', '.join(f'{k}×{v}' for k, v in sorted(redacted.items()))}."
           if redacted else "No PII/secrets/paths detected.")
        + " Submitted via `make_improvement_report.py`._",
    ]
    return "\n".join(lines), redacted


def issue_url(repo: str, skill: str, kind: str, body: str) -> str:
    title = f"[improvement] {skill}: {kind}"
    params = {
        "title": title,
        "body": body,
        "labels": "improvement,needs-triage,auto-report",
    }
    return f"https://github.com/{repo}/issues/new?" + urllib.parse.urlencode(params)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--collection", required=True, help="e.g. metabolomics/v2")
    ap.add_argument("--skill", required=True, help="skill or workflow slug")
    ap.add_argument("--kind", default="correction", choices=KINDS)
    ap.add_argument("--target", default="skills", choices=["skills", "workflows"])
    ap.add_argument("--summary", required=True)
    ap.add_argument("--detail", default="")
    ap.add_argument("--diff", default=None, help="patch text, or @path to read a file")
    ap.add_argument("--runtime", default=None, help="agent runtime label (claude-code, cursor, codex, …)")
    ap.add_argument("--repo", default="HolobiomicsLab/asb-skill-collections")
    ap.add_argument("--out", default=None, help="write the Markdown body here")
    ap.add_argument("--print-url", action="store_true", help="print the pre-filled GitHub issue URL")
    a = ap.parse_args()

    diff = a.diff
    if diff and diff.startswith("@"):
        diff = pathlib.Path(diff[1:]).read_text()

    body, redacted = build_report(
        a.collection, a.skill, a.kind, a.summary, a.detail, diff, a.runtime, a.target
    )

    if a.out:
        pathlib.Path(a.out).write_text(body + "\n")
        print(f"report -> {a.out}", file=sys.stderr)
    else:
        print(body)

    if a.print_url:
        url = issue_url(a.repo, a.skill, a.kind, body)
        if len(url) > 8000:
            print("WARNING: URL exceeds ~8k chars; attach the body manually.", file=sys.stderr)
        print(url)

    print(json.dumps({"redacted": redacted}), file=sys.stderr)


if __name__ == "__main__":
    main()
