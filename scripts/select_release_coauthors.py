#!/usr/bin/env python3
"""Propose release co-authors from the contributor leaderboard.

The community flywheel: people who review/curate the collection earn authorship on
the next versioned release's DOI. This script turns the *measured* contribution
record (`leaderboard/career.jsonld`, built by `regen_career_stats.py` from
`contributors.jsonld` + merged review attestations) into a **proposed** author list
for a release — both in `CITATION.cff` person-author form and Zenodo `creators`
form.

It is deliberately a *proposal*, not an automatic edit. Default mode writes a
human-readable report + a machine-readable JSON proposal; nothing is published.
`--apply` injects the proposed authors into `CITATION.cff` and/or `.zenodo.json`
for a maintainer who has reviewed the proposal.

Selection policy (all transparent, all from declarative fields — no contributor is
named in code; see generalize-or-stop):

  * ORCID required        — authorship needs a resolvable identity.
  * Tier gate             — tier must be >= --min-tier (default: domain_contributor),
                            i.e. beyond a one-off reviewer.
  * Substantive non-self  — external_reviews (reviews of papers the contributor did
                            NOT co-author) must be >= --min-external. Authorship
                            reflects contribution to *others'* content, per COI_POLICY.
  * Recency (optional)    — with --recent-years N, require >=1 review within the last
                            N years (from leaderboard/annual-<year>.jsonld).

Ranking blends "recently and over time": primary key external_reviews (cumulative),
tie-broken by recent-window reviews, then name. The existing CORE authors already in
the target file are always preserved at the front; qualifying contributors are
appended, de-duplicated by ORCID. `--max-coauthors` caps the appended list.

Usage
-----
  python scripts/select_release_coauthors.py --repo-root . \
      [--collection metabolomics] [--min-tier curator] [--recent-years 2] \
      [--report release_coauthors.md] [--json release_coauthors.json]

  # after review, inject into the release metadata files:
  python scripts/select_release_coauthors.py --repo-root . --collection metabolomics \
      --apply --citation collections/metabolomics/v2/CITATION.cff \
      --zenodo collections/metabolomics/v2/.zenodo.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

import yaml

TIER_ORDER = {"reviewer": 0, "domain_contributor": 1, "curator": 2, "lead_curator": 3}


def _load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def _orcid_bare(orcid: str) -> str:
    return (orcid or "").replace("https://orcid.org/", "").strip().rstrip("/")


def _split_name(full: str) -> tuple[str, str]:
    """Best-effort given/family split (last token = family). Heuristic — names in a
    proposal should be eyeballed before publishing."""
    parts = (full or "").split()
    if len(parts) < 2:
        return ("", full or "")
    return (" ".join(parts[:-1]), parts[-1])


def _zenodo_name(full: str) -> str:
    given, family = _split_name(full)
    return f"{family}, {given}".strip(", ") if given else (family or full)


def _recent_counts(repo_root: pathlib.Path, recent_years: int) -> dict[str, int]:
    """Per-ORCID review count within the recent window (for tie-breaking/ranking)."""
    counts: dict[str, int] = {}
    if recent_years <= 0:
        return counts
    current = datetime.now(timezone.utc).year
    for year in range(current - recent_years + 1, current + 1):
        p = repo_root / "leaderboard" / f"annual-{year}.jsonld"
        if not p.exists():
            continue
        for c in _load_json(p).get("contributors", []):
            o = _orcid_bare(c.get("orcid", ""))
            if o:
                counts[o] = counts.get(o, 0) + int(c.get("reviews_this_year", 0))
    return counts


def select_coauthors(
    repo_root: pathlib.Path,
    collection: str | None,
    min_tier: str,
    min_external: int,
    recent_years: int,
    max_coauthors: int,
) -> dict:
    career_path = repo_root / "leaderboard" / "career.jsonld"
    if not career_path.exists():
        return {
            "selected": [],
            "considered": 0,
            "note": f"no leaderboard at {career_path} — run regen_career_stats.py first",
        }
    contributors = _load_json(career_path).get("contributors", [])
    min_tier_rank = TIER_ORDER.get(min_tier, 1)
    recent_counts = _recent_counts(repo_root, recent_years)
    recent_set = set(recent_counts)

    selected = []
    for c in contributors:
        orcid = _orcid_bare(c.get("orcid", ""))
        tier = c.get("tier", "reviewer")
        external = int(c.get("external_reviews", c.get("total_reviews", 0)))
        # collection scoping: contributor must have a role in this collection
        if collection:
            cols = (
                (c.get("lead_curator_of") or [])
                + (c.get("curator_of") or [])
                + (c.get("domain_contributor_of") or [])
                + (c.get("reviewer_of") or [])
            )
            if not any(str(x).split("/")[0] == collection for x in cols):
                continue
        reasons = []
        if not orcid:
            reasons.append("no ORCID")
        if TIER_ORDER.get(tier, 0) < min_tier_rank:
            reasons.append(f"tier {tier} < {min_tier}")
        if external < min_external:
            reasons.append(f"external_reviews {external} < {min_external}")
        if recent_years > 0 and orcid not in recent_set:
            reasons.append(f"no review in last {recent_years}y")
        if reasons:
            continue
        selected.append({
            "name": c.get("name", ""),
            "orcid": orcid,
            "github": c.get("github", ""),
            "tier": tier,
            "external_reviews": external,
            "total_reviews": int(c.get("total_reviews", 0)),
            "recent_reviews": recent_counts.get(orcid, 0),
            "self_authored_percentage": c.get("self_authored_percentage", 0.0),
        })

    selected.sort(key=lambda s: (-s["external_reviews"], -s["recent_reviews"], s["name"]))
    if max_coauthors > 0:
        selected = selected[:max_coauthors]
    return {"selected": selected, "considered": len(contributors), "note": ""}


def _render_report(result: dict, args) -> str:
    lines = [
        "# Proposed release co-authors",
        "",
        f"- collection scope: `{args.collection or 'ALL'}`",
        f"- policy: tier >= `{args.min_tier}`, external_reviews >= `{args.min_external}`, "
        f"recent-years = `{args.recent_years}`, cap = `{args.max_coauthors or 'none'}`",
        f"- considered: {result['considered']} contributor(s); selected: {len(result['selected'])}",
        "",
    ]
    if result["note"]:
        lines += [f"> {result['note']}", ""]
    if not result["selected"]:
        lines += ["_No contributors qualify yet._ The mechanism is live; the list "
                  "populates as review attestations are merged.", ""]
        return "\n".join(lines)
    lines += ["| # | name | tier | external | recent | total | self-authored % | ORCID |",
              "|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(result["selected"], 1):
        lines.append(
            f"| {i} | {s['name']} | {s['tier']} | {s['external_reviews']} | "
            f"{s['recent_reviews']} | {s['total_reviews']} | {s['self_authored_percentage']} | "
            f"{s['orcid']} |"
        )
    lines += ["", "## Proposed CITATION.cff authors (appended after existing core authors)", "```yaml"]
    for s in result["selected"]:
        given, family = _split_name(s["name"])
        lines.append(f"- family-names: {family}")
        if given:
            lines.append(f"  given-names: {given}")
        lines.append(f"  orcid: https://orcid.org/{s['orcid']}")
    lines += ["```", ""]
    return "\n".join(lines)


def _citation_author_yaml(selected: list[dict]) -> list[dict]:
    out = []
    for s in selected:
        given, family = _split_name(s["name"])
        a = {"family-names": family}
        if given:
            a["given-names"] = given
        a["orcid"] = f"https://orcid.org/{s['orcid']}"
        out.append(a)
    return out


def _apply_citation(path: pathlib.Path, selected: list[dict]) -> int:
    """Surgically append proposed authors to the `authors:` block of a CITATION.cff,
    de-duplicated by ORCID, preserving everything else in the file verbatim."""
    text = path.read_text()
    doc = yaml.safe_load(text)
    existing = doc.get("authors", []) or []
    have = {_orcid_bare(a.get("orcid", "")) for a in existing if a.get("orcid")}
    additions = [a for s, a in zip(selected, _citation_author_yaml(selected))
                 if _orcid_bare(a["orcid"]) not in have]
    if not additions:
        return 0
    # Locate the authors: block (from "authors:" to the next top-level key).
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if re.match(r"^authors:\s*$", ln)), None)
    if start is None:
        raise SystemExit(f"{path}: no top-level 'authors:' block to append to")
    end = start + 1
    while end < len(lines) and (lines[end].startswith((" ", "\t", "-")) or not lines[end].strip()):
        end += 1
    block = yaml.safe_dump(additions, sort_keys=False, allow_unicode=True).rstrip("\n").splitlines()
    new_lines = lines[:end] + block + lines[end:]
    path.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""))
    return len(additions)


def _apply_zenodo(path: pathlib.Path, selected: list[dict]) -> int:
    meta = _load_json(path)
    creators = meta.get("creators", []) or []
    have = {_orcid_bare(c.get("orcid", "")) for c in creators if c.get("orcid")}
    added = 0
    for s in selected:
        if s["orcid"] in have:
            continue
        creators.append({"name": _zenodo_name(s["name"]), "orcid": s["orcid"]})
        added += 1
    meta["creators"] = creators
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return added


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--collection", default=None, help="scope to one collection slug")
    ap.add_argument("--min-tier", default="domain_contributor", choices=list(TIER_ORDER))
    ap.add_argument("--min-external", type=int, default=3)
    ap.add_argument("--recent-years", type=int, default=0, help="require a review within N years (0 = off)")
    ap.add_argument("--max-coauthors", type=int, default=0, help="cap appended authors (0 = no cap)")
    ap.add_argument("--report", default=None, help="write markdown report here (else stdout)")
    ap.add_argument("--json", dest="json_out", default=None, help="write JSON proposal here")
    ap.add_argument("--apply", action="store_true", help="inject into --citation / --zenodo files")
    ap.add_argument("--citation", default=None, help="CITATION.cff to append authors to (with --apply)")
    ap.add_argument("--zenodo", default=None, help=".zenodo.json to append creators to (with --apply)")
    a = ap.parse_args()

    repo_root = pathlib.Path(a.repo_root).resolve()
    result = select_coauthors(
        repo_root, a.collection, a.min_tier, a.min_external, a.recent_years, a.max_coauthors
    )

    report = _render_report(result, a)
    if a.report:
        pathlib.Path(a.report).write_text(report + "\n")
        print(f"report -> {a.report}")
    else:
        print(report)
    if a.json_out:
        pathlib.Path(a.json_out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"json -> {a.json_out}")

    if a.apply:
        if not result["selected"]:
            print("--apply: nothing to inject (no qualifying contributors)")
            return
        if a.citation:
            n = _apply_citation(pathlib.Path(a.citation), result["selected"])
            print(f"--apply: appended {n} author(s) to {a.citation}")
        if a.zenodo:
            n = _apply_zenodo(pathlib.Path(a.zenodo), result["selected"])
            print(f"--apply: appended {n} creator(s) to {a.zenodo}")
        if not (a.citation or a.zenodo):
            print("--apply set but neither --citation nor --zenodo given", file=sys.stderr)


if __name__ == "__main__":
    main()
