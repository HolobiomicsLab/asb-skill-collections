"""Ask the DOI registry what a *paper* grants, when its repository could not say.

`derive_license_tiers.py` resolves the licence of a corpus entry's **code
repository**. An entry with no repository therefore falls through to
`restricted` / `license_detection: none` — not because the source refuses reuse,
but because nobody asked it. Those entries land in the `link-only` access tier,
whose definition is "no reuse right is claimed", and the release gate then
applies (or fails to apply) verbatim caps on that basis.

This script closes the gap from the other side: for every entry whose reuse
rights are unestablished, it asks Crossref/DataCite for the work's declared
licence and records the answer. A licence that grants full reuse also promotes
`access.type` to `open-access`, because at that point the paper *is* open access
on the evidence of its own registry record.

Nothing is guessed. An unresolved or unrecognised licence leaves the entry
exactly as it was and is reported loudly, so "we could not establish this"
never reads as "this grants nothing" or as "this is fine".

    python scripts/resolve_paper_license.py --corpus collections/*/v*/corpus.yaml
    python scripts/resolve_paper_license.py --corpus <path> --apply
"""
from __future__ import annotations

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

import argparse
import glob as globlib
import json
import pathlib

import yaml

from scripts.license_tier import SUBJECT_PAPER, UNESTABLISHED_DETECTIONS, tier_for_license
from scripts.preprint_license import (
    STATUS_RESOLVED,
    fetch_json,
    resolve_registry_license,
)

# Re-exported for callers and tests; the vocabulary itself lives in
# scripts/license_tier.py, shared with the repository-side resolver.
UNESTABLISHED_DETECTIONS = UNESTABLISHED_DETECTIONS

# Access tiers this script may promote out of. `link-only` records that nothing
# was cloned, which a paper licence can legitimately supersede; a tier asserting
# a *clone* is evidence this script does not have, so it is never written here.
PROMOTABLE_ACCESS_TYPES = {"link-only", "", None}

OPEN_ACCESS_TYPE = "open-access"


def needs_paper_license(paper: dict) -> bool:
    """True when this entry has no repository and no established licence.

    An entry *with* a repository is out of scope even when its licence is
    unclassified: there, `license_tier` describes the tool's licence, and
    overwriting it with the paper's would conflate two axes the governance keeps
    apart (access.type / license_tier / source_reuse). Only an entry whose sole
    source is the paper can have its tier decided by the paper.
    """
    if paper.get("license_locked"):
        return False
    if str(paper.get("repo_url") or "").strip():
        return False
    return paper.get("license_detection") in UNESTABLISHED_DETECTIONS


def corpus_entries(patterns: list[str]):
    """Yield (path, paper) for every entry in every matching corpus file."""
    for pattern in patterns:
        for path in sorted(globlib.glob(pattern)):
            document = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
            for paper in document.get("papers") or []:
                yield path, paper


def outcome_for(paper: dict, fetch=fetch_json, _resolve=resolve_registry_license) -> dict:
    """Resolve one entry's paper licence into a typed, always-explicit record."""
    doi = str(paper.get("doi") or "").strip()
    if not doi:
        return {"doi": "", "status": "no_doi", "spdx": None, "source_reuse": None,
                "registry": None, "promotes": False}
    resolved = _resolve(doi, fetch, preprints_only=False)
    return {
        "doi": doi,
        "status": resolved.status,
        "spdx": resolved.spdx,
        "source_reuse": resolved.source_reuse,
        "registry": resolved.registry,
        "promotes": bool(
            resolved.admissible_as_open_access
            and (paper.get("access") or {}).get("type") in PROMOTABLE_ACCESS_TYPES
        ),
    }


def apply_outcome(paper: dict, outcome: dict) -> bool:
    """Write a resolved licence into one entry. Returns whether anything changed."""
    if outcome["status"] != STATUS_RESOLVED or not outcome["spdx"]:
        return False
    access = paper.setdefault("access", {})
    access["license"] = outcome["spdx"]
    paper["license_tier"] = tier_for_license(outcome["spdx"])
    paper["license_detection"] = f"{outcome['registry']}-paper"
    paper["license_subject"] = SUBJECT_PAPER
    paper["source_reuse"] = outcome["source_reuse"]
    if outcome["promotes"]:
        access["type"] = OPEN_ACCESS_TYPE
        access["is_oa"] = True
    return True


def run(patterns: list[str], apply: bool, cache_path: pathlib.Path,
        fetch=fetch_json, _resolve=resolve_registry_license) -> list[dict]:
    """Resolve every unestablished entry; write the corpus only when `apply`."""
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    findings: list[dict] = []
    for path in sorted({p for pattern in patterns for p in globlib.glob(pattern)}):
        document = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
        changed = False
        for paper in document.get("papers") or []:
            if not needs_paper_license(paper):
                continue
            doi = str(paper.get("doi") or "").strip()
            outcome = cache.get(doi) if doi else None
            if outcome is None:
                outcome = outcome_for(paper, fetch, _resolve)
                if doi and outcome["status"] == STATUS_RESOLVED:
                    cache[doi] = outcome
            else:
                # A cached record predates this entry's current access.type.
                outcome = dict(outcome)
                outcome["promotes"] = bool(
                    outcome["source_reuse"] == "full"
                    and (paper.get("access") or {}).get("type") in PROMOTABLE_ACCESS_TYPES
                )
            findings.append({"corpus": path, **outcome,
                             "was_access_type": (paper.get("access") or {}).get("type")})
            if apply:
                changed |= apply_outcome(paper, outcome)
        if apply and changed:
            pathlib.Path(path).write_text(
                yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    if cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    return findings


def summarize(findings: list[dict]) -> dict[str, int]:
    """Counts by outcome — the numbers a maintainer reads before applying."""
    summary: dict[str, int] = {"examined": len(findings)}
    for finding in findings:
        summary[finding["status"]] = summary.get(finding["status"], 0) + 1
    summary["promoted_to_open_access"] = sum(1 for f in findings if f["promotes"])
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", nargs="*", default=["collections/*/v*/corpus.yaml"],
                        help="glob(s) of corpus.yaml files")
    parser.add_argument("--apply", action="store_true", help="write the resolved licences back")
    parser.add_argument("--cache", default=".cache/paper_licenses.json")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any examined entry stayed unresolved")
    args = parser.parse_args(argv)

    findings = run(args.corpus, args.apply, pathlib.Path(args.cache))
    for finding in findings:
        if finding["status"] != STATUS_RESOLVED:
            print(f"  UNRESOLVED  {finding['doi']:44} {finding['status']}")
    for finding in findings:
        if finding["promotes"]:
            print(f"  -> open-access  {finding['doi']:44} {finding['spdx']}")
    print(json.dumps(summarize(findings), indent=2, sort_keys=True))
    unresolved = sum(1 for f in findings if f["status"] != STATUS_RESOLVED)
    return 1 if (args.strict and unresolved) else 0


if __name__ == "__main__":
    raise SystemExit(main())
