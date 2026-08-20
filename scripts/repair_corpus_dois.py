"""Repair corpus DOIs that are scraping artefacts, but only when a registry agrees.

A DOI harvested from a landing page or a README badge sometimes arrives with
something extra glued on: the numeric article id a publisher appends to its URL,
carried through as one more path segment, or the `.svg` extension of a badge
image. Neither resolves anywhere, so the entry cannot be grounded and its licence
comes back unresolved — while looking, in the corpus, like an ordinary DOI.

`tests/test_corpus_doi_hygiene.py` already bans `?` and `#` cruft. These two
shapes slipped past it because they are made of characters a real DOI may
contain, which is exactly why the repair here is **not** a string transformation:
the patterns only *propose* candidates, and nothing is written unless the
registry says the original does not resolve and a candidate does. A DOI that
resolves is left alone even if it looks odd, and an entry where nothing resolves
is reported rather than guessed at.

    python scripts/repair_corpus_dois.py --corpus 'collections/*/v*/corpus.yaml'
    python scripts/repair_corpus_dois.py --corpus <path> --apply
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
import re
import urllib.parse

import yaml

from asb_skill_collections import layout
from scripts.preprint_license import CROSSREF_WORK_URL, DATACITE_DOI_URL, fetch_json

# Derived artefacts that key on a DOI. Repairing corpus.yaml alone would leave
# every one of these pointing at a DOI the corpus no longer contains, which is
# worse than the artefact: the join silently finds nothing.
DERIVED_INDEXES = ("skills_index.json", "kb_bundle.json", "tools_index.json")

# Candidate generators. Each proposes a *possible* canonical form; none of them
# decides anything. Keep them shape-based and publisher-neutral — a rule naming
# one registrant would miss the next aggregator that glues on a path segment.
TRAILING_EXTENSION = re.compile(r"\.(?:svg|png|jpg|jpeg|pdf|xml|html?)$", re.IGNORECASE)
TRAILING_ID_SEGMENT = re.compile(r"^(10\.\d{4,9}/.+/[^/]*[A-Za-z][^/]*)/\d{4,}$")

STATUS_OK = "resolves"
STATUS_REPAIRABLE = "repairable"
STATUS_DEAD = "unresolvable"
STATUS_AMBIGUOUS = "ambiguous"


def repair_candidates(doi: str) -> list[str]:
    """Possible canonical forms of a DOI, best-guess first. Never authoritative."""
    seen: list[str] = []
    for candidate in (TRAILING_EXTENSION.sub("", doi),
                      TRAILING_ID_SEGMENT.sub(r"\1", doi)):
        if candidate != doi and candidate not in seen:
            seen.append(candidate)
    return seen


def resolves(doi: str, fetch=fetch_json) -> bool:
    """True when either registry knows this DOI. Network; no side effects."""
    quoted = urllib.parse.quote(doi, safe="/")
    for url in (CROSSREF_WORK_URL.format(doi=quoted), DATACITE_DOI_URL.format(doi=quoted)):
        if fetch(url):
            return True
    return False


def classify(doi: str, fetch=fetch_json) -> dict:
    """Decide what to do with one DOI, asking the registry before anything else.

    A resolving DOI is never touched, however unusual it looks. A candidate is
    accepted only when exactly one of them resolves — two would mean the repair
    is a guess between real works, which is worse than leaving it broken.
    """
    if resolves(doi, fetch):
        return {"doi": doi, "status": STATUS_OK, "repaired": None}
    working = [c for c in repair_candidates(doi) if resolves(c, fetch)]
    if len(working) == 1:
        return {"doi": doi, "status": STATUS_REPAIRABLE, "repaired": working[0]}
    if len(working) > 1:
        return {"doi": doi, "status": STATUS_AMBIGUOUS, "repaired": None, "candidates": working}
    return {"doi": doi, "status": STATUS_DEAD, "repaired": None}


def _suspect(doi: str) -> bool:
    """Cheap pre-filter, so a healthy corpus costs no network calls."""
    return bool(repair_candidates(doi))


def propagate_repairs(collection_dir, mapping: dict[str, str]) -> int:
    """Rewrite a repaired DOI everywhere the collection keys on it.

    The corpus is the source of truth, but skills carry the DOI in
    `derived_from` and every index carries it in `dois`. Repairing one and not
    the others turns a visibly broken DOI into an invisibly broken join.
    Returns the number of files changed.
    """
    if not mapping:
        return 0
    base = pathlib.Path(collection_dir)
    targets = [base / name for name in DERIVED_INDEXES]
    targets += list(layout.iter_skill_md(base, include_infrastructure=True))
    changed = 0
    for target in targets:
        if not target.is_file():
            continue
        text = original = target.read_text(encoding="utf-8")
        for old, new in mapping.items():
            text = text.replace(old, new)
        if text != original:
            target.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def run(patterns: list[str], apply: bool, fetch=fetch_json) -> list[dict]:
    """Classify every suspect DOI; rewrite the corpus and its indexes when `apply`."""
    findings: list[dict] = []
    for path in sorted({p for pattern in patterns for p in globlib.glob(pattern)}):
        document = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
        mapping: dict[str, str] = {}
        for paper in document.get("papers") or []:
            doi = str(paper.get("doi") or "").strip()
            if not doi or not _suspect(doi):
                continue
            outcome = {"corpus": path, **classify(doi, fetch)}
            findings.append(outcome)
            if apply and outcome["status"] == STATUS_REPAIRABLE:
                repaired = outcome["repaired"]
                mapping[doi] = repaired
                paper["doi"] = repaired
                # The harvester filled name/title from the DOI string when it had
                # nothing better; leaving those behind keeps the artefact visible.
                for field in ("name", "title"):
                    if str(paper.get(field) or "").strip() == doi:
                        paper[field] = repaired
        if apply and mapping:
            pathlib.Path(path).write_text(
                yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
            propagate_repairs(pathlib.Path(path).parent, mapping)
    return findings


def summarize(findings: list[dict]) -> dict[str, int]:
    summary = {"suspect": len(findings)}
    for finding in findings:
        summary[finding["status"]] = summary.get(finding["status"], 0) + 1
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", nargs="*", default=["collections/*/v*/corpus.yaml"])
    parser.add_argument("--apply", action="store_true", help="write the repaired DOIs back")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if any suspect DOI is left unrepaired")
    args = parser.parse_args(argv)

    findings = run(args.corpus, args.apply)
    for finding in findings:
        if finding["status"] == STATUS_REPAIRABLE:
            print(f"  repair   {finding['doi']}  ->  {finding['repaired']}")
        elif finding["status"] != STATUS_OK:
            print(f"  {finding['status']:12} {finding['doi']}  ({finding['corpus']})")
    print(json.dumps(summarize(findings), indent=2, sort_keys=True))
    left = sum(1 for f in findings if f["status"] in (STATUS_DEAD, STATUS_AMBIGUOUS))
    if args.strict and (left or (not args.apply and
                                 any(f["status"] == STATUS_REPAIRABLE for f in findings))):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
