"""
Curator vetting script -- identity verification and expertise check.

Implements the 3-layer identity verification per section 9.2 of the Design Doc:
  L1: GitHub URL in ORCID public record (Websites & Social Links)
  L2: Candidate's ORCID matches author list on their proof_publications DOIs
  L3: Institutional affiliation check (Lead Curator only -- optional)

Called by vet-curator.yml GitHub Action.

Exit codes:
  0 -- vetting completed (report in stdout JSON)
  1 -- invocation error
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
import yaml
from dataclasses import dataclass, field, asdict
from pathlib import Path


ORCID_API = "https://pub.orcid.org/v3.0"
OPENALEX_API = "https://api.openalex.org"
USER_AGENT = "asb-skill-collections/0.1 (mailto:louisfelix.nothias@gmail.com)"


@dataclass
class VetResult:
    github: str
    orcid: str
    l1_pass: bool
    l2_pass: bool
    l3_pass: bool | None  # None = not checked (not Lead Curator)
    eligible_tiers: list[str]
    proof_pubs_checked: list[dict]
    errors: list[str] = field(default_factory=list)


def _get_json(url: str) -> dict | None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def check_l1_github_in_orcid(github_handle: str, orcid: str) -> bool:
    """
    L1: Check that github.com/<handle> appears in the candidate's ORCID
    public profile under Websites & Social Links.
    """
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    data = _get_json(f"{ORCID_API}/{orcid_bare}/person")
    if data is None:
        return False

    researcher_urls = (
        data.get("researcher-urls", {}) or {}
    ).get("researcher-url", []) or []

    github_url_expected = f"github.com/{github_handle}".lower()
    for entry in researcher_urls:
        url_value = (entry.get("url", {}) or {}).get("value", "") or ""
        if github_url_expected in url_value.lower():
            return True
    return False


def check_l2_orcid_on_publications(orcid: str, proof_dois: list[str]) -> list[dict]:
    """
    L2: For each proof DOI, verify that the candidate's ORCID appears
    in the author list via OpenAlex.

    Returns a list of per-DOI check results.
    """
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    results = []
    for doi in proof_dois:
        doi_bare = doi.replace("https://doi.org/", "").strip()
        work = _get_json(f"{OPENALEX_API}/works/doi:{doi_bare}")
        if work is None:
            results.append({"doi": doi_bare, "found": False, "error": "API failure"})
            continue

        authorships = work.get("authorships", [])
        found = False
        for authorship in authorships:
            author = authorship.get("author", {}) or {}
            author_orcid = (author.get("orcid", "") or "").replace(
                "https://orcid.org/", ""
            )
            if author_orcid == orcid_bare:
                found = True
                break
        results.append({"doi": doi_bare, "found": found, "error": None})
    return results


def vet_curator(candidate_path: Path) -> VetResult:
    """
    Vet a curator candidate from their candidates/<handle>.yaml file.

    Args:
        candidate_path: Path to the candidate YAML file.

    Returns:
        VetResult with tier eligibility and verification details.
    """
    with open(candidate_path) as f:
        candidate = yaml.safe_load(f)

    github = candidate.get("github", "").lstrip("@")
    orcid = candidate.get("orcid", "")
    proof_dois = [
        p.get("doi", p) if isinstance(p, dict) else p
        for p in candidate.get("proof_publications", [])
    ]

    errors: list[str] = []

    # L1
    l1 = check_l1_github_in_orcid(github, orcid)
    if not l1:
        errors.append(
            f"L1 FAIL: github.com/{github} not found in ORCID {orcid} Websites."
        )

    # L2
    pub_results = check_l2_orcid_on_publications(orcid, proof_dois)
    l2_pass_count = sum(1 for r in pub_results if r["found"])
    l2 = l2_pass_count >= 2 and len(proof_dois) >= 2
    if not l2:
        errors.append(
            f"L2 FAIL: only {l2_pass_count}/{len(proof_dois)} proof pubs verified."
        )

    # Determine eligible tiers
    eligible: list[str] = []
    if l1:
        eligible.append("reviewer")
    if l1 and l2:
        eligible.append("domain_contributor")
        eligible.append("curator")
        # Lead Curator also needs h-index + review count, checked separately
        eligible.append("lead_curator_candidate")

    return VetResult(
        github=github,
        orcid=orcid,
        l1_pass=l1,
        l2_pass=l2,
        l3_pass=None,
        eligible_tiers=eligible,
        proof_pubs_checked=pub_results,
        errors=errors,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Vet a curator candidate.")
    parser.add_argument("candidate_file", help="Path to candidates/<handle>.yaml")
    parser.add_argument(
        "--output", default="-", help="Output file path (- for stdout)"
    )
    args = parser.parse_args()

    result = vet_curator(Path(args.candidate_file))
    output = json.dumps(asdict(result), indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)


if __name__ == "__main__":
    main()
