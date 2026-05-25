"""
Rebuild career-stats leaderboard files from contributors.jsonld + per-collection reviews.

Outputs:
  leaderboard/career.jsonld              -- all-time career stats per contributor
  leaderboard/annual-<year>.jsonld       -- per-year breakdown (uses review_date)
  leaderboard/by-domain/<domain>.jsonld  -- domain-scoped contributor list

Aggregated fields per contributor entry:
  total_reviews, lead_curator_of[], curator_of[], domain_contributor_of[],
  reviewer_of[], self_authored_percentage

Usage:
    python scripts/regen_career_stats.py [--repo-root .]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

import yaml


def _load_json(path: pathlib.Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(data: dict, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _load_review_yaml(path: pathlib.Path) -> dict | None:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as exc:
        print(f"WARNING: skipping review {path}: {exc}", file=sys.stderr)
        return None


def _collect_reviews(repo_root: pathlib.Path) -> list[dict]:
    """Walk all reviews/*.yaml files under collections/ and return list of parsed dicts."""
    reviews: list[dict] = []
    collections_dir = repo_root / "collections"
    if not collections_dir.exists():
        return reviews
    for review_path in sorted(collections_dir.glob("**/reviews/*.yaml")):
        review = _load_review_yaml(review_path)
        if review is None:
            continue
        # Annotate with collection slug (parent of reviews/)
        # Path pattern: collections/<slug>/v<N>/reviews/<doi>.yaml
        parts = review_path.parts
        try:
            col_idx = parts.index("collections")
            slug = parts[col_idx + 1]
        except (ValueError, IndexError):
            slug = "unknown"
        review["_collection_slug"] = slug
        reviews.append(review)
    return reviews


def _build_contributor_stats(
    contributors: list[dict],
    reviews: list[dict],
) -> list[dict]:
    """Build aggregated career stats for each contributor."""
    result: list[dict] = []
    for contrib in contributors:
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        tier = contrib.get("asb:tier", "reviewer")
        collections = contrib.get("asb:collections", []) or []
        total = int(contrib.get("asb:total_reviews", 0))
        self_authored = int(contrib.get("asb:self_authored_reviews", 0))

        # Self-authored percentage
        pct = (self_authored / total * 100) if total > 0 else 0.0

        # Role lists: assign collection to the appropriate role bucket
        lead_curator_of: list[str] = []
        curator_of: list[str] = []
        domain_contributor_of: list[str] = []
        reviewer_of: list[str] = []

        for col in collections:
            if tier == "lead_curator":
                lead_curator_of.append(col)
            elif tier == "curator":
                curator_of.append(col)
            elif tier == "domain_contributor":
                domain_contributor_of.append(col)
            else:
                reviewer_of.append(col)

        result.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": tier,
            "total_reviews": total,
            "self_authored_percentage": round(pct, 4),
            "lead_curator_of": lead_curator_of,
            "curator_of": curator_of,
            "domain_contributor_of": domain_contributor_of,
            "reviewer_of": reviewer_of,
        })
    return result


def _build_annual(
    contributors: list[dict],
    reviews: list[dict],
    year: int,
) -> list[dict]:
    """Build per-year stats for the given year using review_date fields."""
    # Count reviews per orcid for this year
    year_counts: dict[str, int] = defaultdict(int)
    year_collections: dict[str, set] = defaultdict(set)

    for review in reviews:
        rd = review.get("review_date", "") or ""
        try:
            review_year = int(str(rd)[:4])
        except (ValueError, TypeError):
            continue
        if review_year != year:
            continue
        reviewer_info = review.get("reviewer", {}) or {}
        orcid = reviewer_info.get("orcid", "").replace("https://orcid.org/", "").strip()
        if orcid:
            year_counts[orcid] += 1
            year_collections[orcid].add(review.get("_collection_slug", "unknown"))

    # Build contributor entries for this year
    year_contributors: list[dict] = []
    for contrib in contributors:
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        n = year_counts.get(orcid, 0)
        if n == 0:
            continue
        year_contributors.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": contrib.get("asb:tier", "reviewer"),
            "reviews_this_year": n,
            "collections": sorted(year_collections.get(orcid, set())),
        })
    year_contributors.sort(key=lambda c: -c["reviews_this_year"])
    return year_contributors


def _build_by_domain(
    contributors: list[dict],
    domain: str,
) -> list[dict]:
    """Return contributor entries scoped to one domain/collection slug."""
    result: list[dict] = []
    for contrib in contributors:
        collections = contrib.get("asb:collections", []) or []
        if domain not in collections:
            continue
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        result.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": contrib.get("asb:tier", "reviewer"),
            "total_reviews": int(contrib.get("asb:total_reviews", 0)),
        })
    result.sort(key=lambda c: -c["total_reviews"])
    return result


JSONLD_CONTEXT = {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "generated_at": {"@id": "asb:generatedAt", "@type": "xsd:dateTime"},
}


def regen_career_stats(repo_root: pathlib.Path) -> None:
    """
    Rebuild all leaderboard/*.jsonld files.

    Args:
        repo_root: Path to the repository root.
    """
    contributors_path = repo_root / "contributors.jsonld"
    if not contributors_path.exists():
        print(f"ERROR: contributors.jsonld not found at {contributors_path}", file=sys.stderr)
        sys.exit(1)

    registry = _load_json(contributors_path)
    contributors: list[dict] = registry.get("contributors", [])

    reviews = _collect_reviews(repo_root)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    current_year = datetime.now(timezone.utc).year

    # 1. career.jsonld
    career_stats = _build_contributor_stats(contributors, reviews)
    career_data: dict[str, Any] = {
        "@context": JSONLD_CONTEXT,
        "@type": "asb:CareerLeaderboard",
        "@id": "https://w3id.org/holobiomicslab/asb-skill/leaderboard/career",
        "name": "ASB Contributor Career Stats",
        "generated_at": now_utc,
        "contributors": career_stats,
    }
    _write_json(career_data, repo_root / "leaderboard" / "career.jsonld")

    # 2. annual-<year>.jsonld for current year (and any year with reviews)
    years_seen: set[int] = set()
    years_seen.add(current_year)
    for review in reviews:
        rd = review.get("review_date", "") or ""
        try:
            years_seen.add(int(str(rd)[:4]))
        except (ValueError, TypeError):
            pass

    for year in sorted(years_seen):
        year_contribs = _build_annual(contributors, reviews, year)
        annual_data = {
            "@context": JSONLD_CONTEXT,
            "@type": "asb:AnnualLeaderboard",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/leaderboard/annual-{year}",
            "name": f"ASB Contributor Leaderboard {year}",
            "year": year,
            "generated_at": now_utc,
            "contributors": year_contribs,
        }
        _write_json(annual_data, repo_root / "leaderboard" / f"annual-{year}.jsonld")

    # 3. by-domain/<slug>.jsonld — one per unique domain in asb:collections
    domains: set[str] = set()
    for contrib in contributors:
        for col in (contrib.get("asb:collections") or []):
            if col:
                domains.add(col)

    for domain in sorted(domains):
        domain_contribs = _build_by_domain(contributors, domain)
        domain_data = {
            "@context": JSONLD_CONTEXT,
            "@type": "asb:DomainLeaderboard",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/leaderboard/by-domain/{domain}",
            "name": f"ASB {domain.title()} Domain Contributors",
            "domain": domain,
            "generated_at": now_utc,
            "contributors": domain_contribs,
        }
        _write_json(
            domain_data,
            repo_root / "leaderboard" / "by-domain" / f"{domain}.jsonld",
        )

    print(
        f"Career stats written: {len(contributors)} contributors, "
        f"{len(years_seen)} year(s), {len(domains)} domain(s)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild leaderboard career stats from contributors.jsonld + reviews."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    args = parser.parse_args()
    repo_root = pathlib.Path(args.repo_root).resolve()
    regen_career_stats(repo_root)


if __name__ == "__main__":
    main()
