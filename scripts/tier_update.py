"""
Tier update script -- called by tier-update.yml on merge of review PRs.

Increments review counters in contributors.jsonld and re-evaluates
the contributor's tier per curator-criteria.yaml for the collection.

Exit codes:
  0 -- update applied
  1 -- contributor not found or invocation error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_contributors(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_contributors(data: dict, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_criteria(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def find_contributor(registry: dict, orcid: str) -> dict | None:
    bare = orcid.replace("https://orcid.org/", "").strip()
    for contrib in registry.get("contributors", []):
        c_orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        if c_orcid == bare:
            return contrib
    return None


def evaluate_tier(
    total_reviews: int,
    external_reviews: int,
    criteria: dict,
) -> str:
    """
    Return the highest tier the contributor qualifies for based on review counts.
    Note: pub count + h-index are checked during candidacy vetting, not here.
    """
    thresholds = criteria.get("thresholds", {})

    lead = thresholds.get("lead_curator", {})
    if (
        total_reviews >= lead.get("min_reviews", 9999)
        and external_reviews >= lead.get("min_external_reviews", 9999)
    ):
        return "lead_curator"

    curator = thresholds.get("curator", {})
    if total_reviews >= curator.get("min_reviews", 9999):
        return "curator"

    dc = thresholds.get("domain_contributor", {})
    if total_reviews >= dc.get("min_reviews", 9999):
        return "domain_contributor"

    reviewer = thresholds.get("reviewer", {})
    if total_reviews >= reviewer.get("min_reviews", 1):
        return "reviewer"

    return "none"


def update_contributor(
    contributors_path: Path,
    criteria_path: Path,
    orcid: str,
    collection_slug: str,
    is_self_authored: bool,
) -> None:
    registry = load_contributors(contributors_path)
    criteria = load_criteria(criteria_path)

    contrib = find_contributor(registry, orcid)
    if contrib is None:
        print(
            f"ERROR: contributor {orcid} not found in contributors.jsonld",
            file=sys.stderr,
        )
        sys.exit(1)

    # Increment totals
    contrib["asb:total_reviews"] = contrib.get("asb:total_reviews", 0) + 1
    if is_self_authored:
        contrib["asb:self_authored_reviews"] = (
            contrib.get("asb:self_authored_reviews", 0) + 1
        )
    else:
        contrib["asb:external_reviews"] = contrib.get("asb:external_reviews", 0) + 1

    total = contrib["asb:total_reviews"]
    external = contrib.get("asb:external_reviews", 0)

    # Re-evaluate tier
    new_tier = evaluate_tier(total, external, criteria)
    contrib["asb:tier"] = new_tier

    save_contributors(registry, contributors_path)
    print(
        json.dumps(
            {
                "orcid": orcid,
                "collection": collection_slug,
                "new_tier": new_tier,
                "total_reviews": total,
                "external_reviews": external,
            }
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update contributor tier after review merge."
    )
    parser.add_argument("--orcid", required=True)
    parser.add_argument(
        "--collection", required=True, help="Collection slug (e.g., metabolomics)"
    )
    parser.add_argument("--is-self-authored", action="store_true")
    parser.add_argument(
        "--contributors",
        default="contributors.jsonld",
        help="Path to contributors.jsonld",
    )
    parser.add_argument(
        "--criteria",
        required=True,
        help="Path to curator-criteria.yaml for this collection",
    )
    args = parser.parse_args()

    update_contributor(
        Path(args.contributors),
        Path(args.criteria),
        args.orcid,
        args.collection,
        args.is_self_authored,
    )


if __name__ == "__main__":
    main()
