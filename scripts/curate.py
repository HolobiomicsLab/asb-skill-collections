#!/usr/bin/env python3
"""curate — static curation auditor for an ASB skill collection.

Domain-general structural + grounding audit over ``collections/<slug>/v<N>/``.
Emits ``curation_report.json`` (schema mirrors ``gate_report.json``). Advisory by
default; ``--strict`` exits 1 when any check has FAIL findings.

Two disciplines this file must keep (both from the 2026-06-17 overfit audit):
  * ``None`` != ``0`` — a target a check cannot evaluate is reported
    ``not_applicable``, never a silent clean pass.
  * No domain vocabulary in this file (generalize-or-stop rule 5) — every check
    keys off schema and structure, never a metabolomics/omics token.

Usage:
  python curate.py <collection_dir> [--strict] [--report PATH] [--quiet]
"""
from __future__ import annotations

import argparse
import difflib
import glob
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

import yaml

import validate_workflows as vw

# A leaf carrying more tools than this is an over-aggregated "meta-leaf" artifact
# (the 7 purged in v0.2.0). Matches compose_workflows.MAX_TOOLS_PER_LEAF.
MAX_TOOLS_PER_LEAF = 25
# Two leaves count as duplicates only when their full descriptions are this
# similar AND they share tools+DOIs. A prefix/boilerplate match is not enough:
# distinct skills from one paper share tools, so a loose gate over-fires.
_DUP_SIM_THRESHOLD = 0.90
_WORKFLOW_SKIP = ("bin", "_archive")


def norm_doi(doi: str) -> str:
    """Lower-case a DOI and drop any resolver prefix, for set membership."""
    d = str(doi).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d


def finding(check: str, severity: str, target: str, detail: str) -> dict:
    """One problem the auditor found. severity is 'fail' or 'warn'."""
    return {"check": check, "severity": severity, "target": target, "detail": detail}


def result(name: str, findings: list, n_evaluated: int, n_na: int,
           status: str | None = None) -> dict:
    """Assemble one check's outcome, deriving status from findings if unset."""
    if status is None:
        sev = {f["severity"] for f in findings}
        status = "fail" if "fail" in sev else "warn" if "warn" in sev else "pass"
    return {"name": name, "status": status, "n_evaluated": n_evaluated,
            "n_not_applicable": n_na, "n_findings": len(findings),
            "findings": findings}


def load_index(collection_dir: str) -> list:
    """Load the leaf skills_index.json for a collection."""
    with open(os.path.join(collection_dir, "skills_index.json")) as fh:
        return json.load(fh)


def load_corpus_dois(collection_dir: str) -> set:
    """Collect every DOI from the collection's corpus.yaml (empty set if none)."""
    path = os.path.join(collection_dir, "corpus.yaml")
    if not os.path.exists(path):
        return set()
    with open(path) as fh:
        corpus = yaml.safe_load(fh) or {}
    dois = set()
    for paper in corpus.get("papers", []) or []:
        if isinstance(paper, dict) and paper.get("doi"):
            dois.add(norm_doi(paper["doi"]))
    return dois


def read_frontmatter(path: str):
    """Return (frontmatter_dict, None) or (None, error_str).

    Parses the block between the first two lines that are exactly '---', so a
    stray '---' inside an evidence span cannot truncate it (the v0.2.0 bug).
    """
    with open(path) as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no opening frontmatter fence"
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                return yaml.safe_load("\n".join(lines[1:i])) or {}, None
            except yaml.YAMLError as exc:
                return None, f"yaml error: {exc}".splitlines()[0]
    return None, "no closing frontmatter fence"


def iter_leaf_frontmatter(collection_dir: str):
    """Yield (slug, frontmatter_or_None, error_or_None) for every leaf SKILL.md."""
    for md in sorted(glob.glob(os.path.join(collection_dir, "skills", "*", "SKILL.md"))):
        slug = os.path.basename(os.path.dirname(md))
        fm, err = read_frontmatter(md)
        yield slug, fm, err


def check_leaf_grounding(index: list) -> dict:
    """Flag indexed leaves with no source DOI. Absent field warns; empty fails."""
    findings = []
    for leaf in index:
        dois = leaf.get("dois")
        if dois is None:
            findings.append(finding("leaf_grounding", "warn", leaf["slug"],
                                    "no 'dois' field (grounding unknown)"))
        elif len(dois) == 0:
            findings.append(finding("leaf_grounding", "fail", leaf["slug"],
                                    "empty 'dois' (ungrounded leaf)"))
    return result("leaf_grounding", findings, len(index), 0)


def check_oversized_leaf(index: list) -> dict:
    """Flag leaves carrying more than MAX_TOOLS_PER_LEAF tools (meta-leaf smell)."""
    findings = []
    for leaf in index:
        n = len(leaf.get("tools") or [])
        if n > MAX_TOOLS_PER_LEAF:
            findings.append(finding("oversized_leaf", "warn", leaf["slug"],
                                    f"{n} tools (> {MAX_TOOLS_PER_LEAF})"))
    return result("oversized_leaf", findings, len(index), 0)


def _norm_desc(leaf: dict) -> str:
    """Lower-cased, whitespace-collapsed description for similarity comparison."""
    return " ".join((leaf.get("description") or "").lower().split())


def _dup_pairs(members: list) -> list:
    """Duplicate findings within one (tools+DOIs) bucket, gated on description similarity."""
    descs = [_norm_desc(m) for m in members]
    out = []
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            if not descs[i] and not descs[j]:
                continue
            ratio = difflib.SequenceMatcher(None, descs[i], descs[j]).ratio()
            if ratio >= _DUP_SIM_THRESHOLD:
                pair = ", ".join(sorted([members[i]["slug"], members[j]["slug"]]))
                out.append(finding("duplicate_leaf", "warn", pair,
                                    f"descriptions {ratio:.2f} similar + shared tools/DOIs"))
    return out


def check_duplicate_leaf(index: list) -> dict:
    """Flag leaf pairs that share tools+DOIs AND have near-identical descriptions.

    Bucketing on (tools, dois) keeps this O(sum bucket^2); the description
    similarity gate is the discriminating signal, so two distinct skills that
    merely share a paper's tools are not flagged (precision over recall).
    """
    buckets = defaultdict(list)
    n_na = 0
    for leaf in index:
        tools = leaf.get("tools") or []
        dois = leaf.get("dois") or []
        if not tools and not dois:
            n_na += 1  # nothing to fingerprint → not applicable, not "unique"
            continue
        key = (tuple(sorted(map(str, tools))), tuple(sorted(map(str, dois))))
        buckets[key].append(leaf)
    findings = []
    for members in buckets.values():
        if len(members) > 1:
            findings.extend(_dup_pairs(members))
    return result("duplicate_leaf", findings, len(index) - n_na, n_na)


def check_doi_in_corpus(index: list, corpus_dois: set) -> dict:
    """Flag leaf DOIs absent from corpus.yaml. No corpus => not applicable."""
    if not corpus_dois:
        return result("doi_in_corpus", [], 0, len(index), status="not_applicable")
    findings, n = [], 0
    for leaf in index:
        for doi in (leaf.get("dois") or []):
            n += 1
            if norm_doi(doi) not in corpus_dois:
                findings.append(finding("doi_in_corpus", "warn", leaf["slug"],
                                        f"DOI not in corpus: {doi}"))
    return result("doi_in_corpus", findings, n, 0)


def check_frontmatter_health(collection_dir: str) -> dict:
    """Parse every leaf SKILL.md; a parse failure fails, a missing license warns."""
    findings, n = [], 0
    for slug, fm, err in iter_leaf_frontmatter(collection_dir):
        n += 1
        if err:
            findings.append(finding("frontmatter_health", "fail", slug, err))
            continue
        if not fm.get("name"):
            findings.append(finding("frontmatter_health", "fail", slug, "missing 'name'"))
        if not fm.get("license"):
            findings.append(finding("frontmatter_health", "warn", slug, "missing 'license'"))
    if n == 0:
        return result("frontmatter_health", [], 0, 0, status="not_applicable")
    return result("frontmatter_health", findings, n, 0)


def check_workflow_integrity(collection_dir: str) -> dict:
    """Run validate_workflows over the collection's workflows/ subtree."""
    wf_dir = os.path.join(collection_dir, "workflows")
    if not os.path.isdir(wf_dir):
        return result("workflow_integrity", [], 0, 1, status="not_applicable")
    idx = {r["slug"] for r in load_index(collection_dir)}
    findings, n = [], 0
    for d in sorted(glob.glob(os.path.join(wf_dir, "*"))):
        base = os.path.basename(d)
        if not os.path.isdir(d) or base.startswith("_") or base in _WORKFLOW_SKIP:
            continue
        n += 1
        for err in vw.validate_one(d, idx):
            findings.append(finding("workflow_integrity", "fail", base, err))
    if n == 0:
        return result("workflow_integrity", [], 0, 1, status="not_applicable")
    return result("workflow_integrity", findings, n, 0)


def run_curation(collection_dir: str) -> list:
    """Run every check over a collection and return the list of check results."""
    index = load_index(collection_dir)
    corpus_dois = load_corpus_dois(collection_dir)
    return [
        check_leaf_grounding(index),
        check_oversized_leaf(index),
        check_duplicate_leaf(index),
        check_doi_in_corpus(index, corpus_dois),
        check_frontmatter_health(collection_dir),
        check_workflow_integrity(collection_dir),
    ]


def build_report(collection_dir: str, checks: list) -> dict:
    """Assemble the curation_report.json payload from check results."""
    order = {"pass": 0, "not_applicable": 0, "warn": 1, "fail": 2}
    overall = max(checks, key=lambda c: order[c["status"]])["status"] if checks else "pass"
    if overall == "not_applicable":
        overall = "pass"
    counts = defaultdict(int)
    for c in checks:
        counts[c["status"]] += 1
    return {
        "schema": "asbb-curation-report/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection_dir": collection_dir,
        "overall_status": overall,
        "summary_counts": dict(counts),
        "checks": checks,
    }


def print_summary(report: dict) -> None:
    """Print a one-line-per-check human summary to stdout."""
    print(f"curation: {report['collection_dir']} -> {report['overall_status'].upper()}")
    for c in report["checks"]:
        print(f"  [{c['status']:>14}] {c['name']:<22} "
              f"{c['n_findings']} findings / {c['n_evaluated']} evaluated"
              f" / {c['n_not_applicable']} n/a")


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="curate.py",
        description="Static curation auditor for an ASB skill collection.")
    parser.add_argument("collection_dir", type=str,
                        help="Collection directory, e.g. collections/metabolomics/v2")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 if any check has FAIL findings.")
    parser.add_argument("--report", type=str, default=None,
                        help="Where to write curation_report.json "
                             "(default: <collection_dir>/curation_report.json).")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress the human summary (still writes JSON).")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.collection_dir):
        print(f"error: not a directory: {args.collection_dir}", file=sys.stderr)
        return 2

    checks = run_curation(args.collection_dir)
    report = build_report(args.collection_dir, checks)
    out = args.report or os.path.join(args.collection_dir, "curation_report.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)
    if not args.quiet:
        print_summary(report)
        print(f"  report: {out}")

    has_fail = any(c["status"] == "fail" for c in checks)
    return 1 if (args.strict and has_fail) else 0


def _selftest() -> None:
    """Smoke check on synthetic data — no filesystem, no domain vocabulary."""
    idx = [
        {"slug": "a", "dois": ["10.1/x"], "tools": ["T1"], "description": "does a thing"},
        {"slug": "b", "dois": [], "tools": [], "description": "ungrounded"},
        {"slug": "c", "tools": [f"t{i}" for i in range(30)], "description": "meta"},
        {"slug": "d", "dois": ["10.1/x"], "tools": ["T1"], "description": "does a thing"},
        {"slug": "e", "dois": ["10.1/x"], "tools": ["T1"],
         "description": "an entirely different unrelated procedure for another purpose"},
    ]
    grounding = check_leaf_grounding(idx)
    assert grounding["status"] == "fail", grounding  # 'b' has empty dois
    assert check_oversized_leaf(idx)["n_findings"] == 1  # 'c'
    # Two-sided: a&d have identical descriptions -> flagged; 'e' shares tools+DOI
    # but a distinct description -> NOT flagged (over-fire guard).
    dup = check_duplicate_leaf(idx)
    assert dup["n_findings"] == 1, dup
    # None != 0: absent corpus => not_applicable, not a clean pass.
    assert check_doi_in_corpus(idx, set())["status"] == "not_applicable"
    assert check_doi_in_corpus(idx, {"10.1/x"})["status"] == "pass"
    assert norm_doi("https://doi.org/10.1/X") == "10.1/x"
    print("curate self-test: OK")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
