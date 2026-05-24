"""
COI (Conflict of Interest) check for reviewer attestation PRs.

Checks whether the reviewer ORCID is a co-author of the paper DOI
via OpenAlex. Called by verify-coi.yml GitHub Action.

Exit codes:
  0 -- check completed (result in stdout JSON)
  1 -- invocation error (missing args, API unreachable)
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
USER_AGENT = "asb-skill-collections/0.1 (mailto:louisfelix.nothias@gmail.com)"


@dataclass
class CoiResult:
    orcid: str
    doi: str
    is_coauthor: bool
    author_position: int | None  # 1-based; None if not found
    is_corresponding: bool
    openalex_work_id: str | None
    error: str | None = None


def fetch_work_by_doi(doi: str) -> dict | None:
    """Fetch OpenAlex Work record for a DOI. Returns None on failure."""
    url = f"{OPENALEX_WORKS_URL}/doi:{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None


def check_coi(orcid: str, doi: str) -> CoiResult:
    """
    Check whether the reviewer (identified by ORCID) is a co-author of
    the paper (identified by DOI) using the OpenAlex API.

    Args:
        orcid: Reviewer's ORCID (with or without https://orcid.org/ prefix).
        doi: Paper DOI (with or without https://doi.org/ prefix).

    Returns:
        CoiResult with is_coauthor, author_position, is_corresponding.
    """
    # Normalize inputs
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    doi_bare = doi.replace("https://doi.org/", "").strip()

    work = fetch_work_by_doi(doi_bare)
    if work is None:
        return CoiResult(
            orcid=orcid_bare,
            doi=doi_bare,
            is_coauthor=False,
            author_position=None,
            is_corresponding=False,
            openalex_work_id=None,
            error=f"Could not fetch OpenAlex work for DOI {doi_bare}",
        )

    work_id = work.get("id")
    authorships = work.get("authorships", [])

    for idx, authorship in enumerate(authorships, start=1):
        author = authorship.get("author", {})
        author_orcid = author.get("orcid", "") or ""
        # OpenAlex stores ORCIDs as full URLs
        author_orcid_bare = author_orcid.replace("https://orcid.org/", "").strip()

        if author_orcid_bare == orcid_bare:
            is_corresponding = authorship.get("is_corresponding", False)
            return CoiResult(
                orcid=orcid_bare,
                doi=doi_bare,
                is_coauthor=True,
                author_position=idx,
                is_corresponding=is_corresponding,
                openalex_work_id=work_id,
            )

    return CoiResult(
        orcid=orcid_bare,
        doi=doi_bare,
        is_coauthor=False,
        author_position=None,
        is_corresponding=False,
        openalex_work_id=work_id,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Check COI between reviewer and paper.")
    parser.add_argument("--orcid", required=True, help="Reviewer ORCID")
    parser.add_argument("--doi", required=True, help="Paper DOI")
    parser.add_argument(
        "--output", default="-", help="Output file path (- for stdout)"
    )
    args = parser.parse_args()

    result = check_coi(args.orcid, args.doi)
    output = json.dumps(asdict(result), indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)

    if result.error:
        sys.exit(1)


if __name__ == "__main__":
    main()
