"""
Tier update script -- called by tier-update.yml on merge of review PRs.

Two credit paths, both keyed on a contributor's ORCID in contributors.jsonld:

* **Review path** (``--orcid ...``, the default): increments review counters
  (``asb:total_reviews`` + ``asb:external_reviews``/``asb:self_authored_reviews``)
  on merge of a review attestation, then re-evaluates the tier.
* **Author-credit path** (``--credit-author``): a contributor listed as a skill
  ``author`` (role ``author`` in a merged skill's ``contributors`` block) is
  credited via a separate ``asb:authored_skills`` counter, then the tier is
  re-evaluated. This never touches the review counters and never downgrades an
  already-higher tier. See governance/AUTHORSHIP.md.

Both re-evaluate the contributor's tier per curator-criteria.yaml for the
collection.

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
    authored_skills: int = 0,
) -> str:
    """
    Return the highest tier the contributor qualifies for based on review counts.
    Note: pub count + h-index are checked during candidacy vetting, not here.

    The higher tiers (domain_contributor and above) are earned through
    **reviews**. ``authored_skills`` participates only at the **reviewer** entry
    tier: a contributor who has authored >=1 merged skill qualifies as a
    reviewer even with zero reviews, matching the author-credit path. Backward
    compatible — the default ``authored_skills=0`` reproduces the old behavior.
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
    if total_reviews >= reviewer.get("min_reviews", 1) or authored_skills >= 1:
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
    authored = contrib.get("asb:authored_skills", 0)

    # Re-evaluate tier (authored skills count toward the reviewer entry tier).
    new_tier = evaluate_tier(total, external, criteria, authored_skills=authored)
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
                "authored_skills": authored,
            }
        )
    )


def credit_author(
    contributors_path: Path,
    criteria_path: Path,
    orcid: str,
    collection_slug: str,
) -> None:
    """Credit a skill **author** on merge of their authored skill.

    Increments the contributor's ``asb:authored_skills`` counter and
    re-evaluates the tier. This path is independent of the review counters and,
    by construction of :func:`evaluate_tier`, never downgrades an already-higher
    tier (authored skills only reach the reviewer entry tier). See
    governance/AUTHORSHIP.md.
    """
    registry = load_contributors(contributors_path)
    criteria = load_criteria(criteria_path)

    contrib = find_contributor(registry, orcid)
    if contrib is None:
        print(
            f"ERROR: contributor {orcid} not found in contributors.jsonld",
            file=sys.stderr,
        )
        sys.exit(1)

    contrib["asb:authored_skills"] = contrib.get("asb:authored_skills", 0) + 1

    total = contrib.get("asb:total_reviews", 0)
    external = contrib.get("asb:external_reviews", 0)
    authored = contrib["asb:authored_skills"]

    new_tier = evaluate_tier(total, external, criteria, authored_skills=authored)
    contrib["asb:tier"] = new_tier

    save_contributors(registry, contributors_path)
    print(
        json.dumps(
            {
                "orcid": orcid,
                "collection": collection_slug,
                "credited": "author",
                "new_tier": new_tier,
                "authored_skills": authored,
            }
        )
    )


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Update contributor tier after a review or authored-skill merge."
    )
    parser.add_argument("--orcid", required=True)
    parser.add_argument(
        "--collection", required=True, help="Collection slug (e.g., metabolomics)"
    )
    parser.add_argument("--is-self-authored", action="store_true")
    parser.add_argument(
        "--credit-author",
        action="store_true",
        help=(
            "Author-credit path: credit the contributor as a merged-skill author "
            "(increments asb:authored_skills) instead of a reviewer."
        ),
    )
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
    args = parser.parse_args(argv)

    if args.credit_author:
        credit_author(
            Path(args.contributors),
            Path(args.criteria),
            args.orcid,
            args.collection,
        )
    else:
        update_contributor(
            Path(args.contributors),
            Path(args.criteria),
            args.orcid,
            args.collection,
            args.is_self_authored,
        )


if __name__ == "__main__":
    main()
