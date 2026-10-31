# Call for curators: the first ASB skill-collection releases

Draft prepared 2026-09-19; status checked 2026-10-06; cut re-dated 2026-10-29. The
authorship cut for the first releases is **2026-12-15, 23:59 CET**. The public opening
date and reviewer access must be confirmed before this call is circulated.

Ten domain collections of agent skills are being prepared for release by the Holobiomics
Lab (CNRS / Université Côte d'Azur): metabolomics (v3), epigenomics, transcriptomics,
proteomics, genomics, metagenomics, metabarcoding, multi-omics, agentic AI and astronomy
(v1). As of 2026-10-06, five private candidate collections have passed the blocking
automated checks: astronomy, genomics, metabarcoding, metagenomics and multi-omics.
They contain 9,261 skills and ten composed workflows. Genomics retains four
non-blocking placeholder-subject warnings for review. Transcriptomics, epigenomics,
agentic AI and proteomics remain stopped by a content-screening gate; the
metabolomics v3 rebuild has not been completed.

Skills are generated from available research-article packages, with source
references and evidence records. Passing automated checks does not establish that
every source is peer-reviewed, that public code is available, or that a skill is
scientifically correct or runnable. Expert reading remains necessary: does the
skill describe the method as its authors would, are the defaults right, and is the
tool record current. That reading is what this call asks for, and it is credited.

The model is the one Terminal-Bench used for its task collection: an open call with a
fixed deadline, every contribution reviewed, and the contributors above a stated
threshold named on the release and on the paper.

## What counts as a contribution

Each is one pull request or one issue, reviewed by a maintainer with a conflict-of-interest
check (`governance/COI_POLICY.md`).

1. **Expert review of a skill.** Read a skill and its source paper; accept it, edit it or
   reject it, with a one-line reason. Copy `templates/attestation.yaml.template` to
   `collections/<slug>/v<N>/reviews/<paper-doi-slug>.yaml`, put the verdict and its reason in
   `summary`, and open a pull request (`.github/CONTRIBUTING.md`, "How to contribute a
   review"). To ask for a paper to be reviewed without reviewing it yourself, open an issue
   from the request-paper-review template (`.github/ISSUE_TEMPLATE/request-paper-review.md`).
2. **Correction.** A wrong default, a missing step, an outdated tool, a better procedure:
   an improvement report (`scripts/make_improvement_report.py`, anonymised) followed by a
   pull request.
3. **Adapter or tool record.** A domain adapter, a licence clarification obtained from a
   tool's maintainers, or a tool record with the fields the collection lacks.

Reviews of skills you co-authored (as an author of the source paper or of the tool) are
allowed with disclosure and a second reviewer; they are counted separately from external
reviews and both counts are public.

## How credit works

Credit is granted only to a verified identity (`governance/AUTHORSHIP.md`): an ORCID and a
GitHub account linked in `contributors.jsonld`. The three steps below are cumulative.

| Step | Threshold | Where the credit appears |
|---|---|---|
| Contributor | one accepted review or one merged correction | `contributors.jsonld`, the `Co-authored-by` trailer of the merged commit, the `contributors` block of the skill, and the Zenodo record of the version as `DataCurator` |
| Creator | three external reviews in one domain, or one adapter, by the deadline | creator (author) of the version DOI of that collection, injected by `scripts/select_release_coauthors.py --apply` before the tag; listed in the collection `CITATION.cff` |
| Curator | creator of two consecutive versions, or lead curator of a domain | co-author of the methods paper; entry in `governance/MAINTAINERS.md` |

Everyone at the Creator step by 2026-12-15 is named a **founding curator** of the domain in
its README and on its first DOI. The leaderboard (`leaderboard/career.jsonld`) ranks by
external reviews and is rebuilt on every merge; counts, not judgements, decide the steps.

The starting author list of every collection is the lead and the framework as an entity
author; it grows only through the steps above. Opting out at any time:
`governance/AUTHOR_OPT_OUT.md`.

## Rules of the road

- Content policy: `governance/CONTENT_POLICY.md`. Contributed prose is licensed CC-BY-4.0
  like the rest of the collection content (`LICENSING.md`).
- Disputes: `governance/DISPUTE_RESOLUTION.md`.
- No credit for volume alone: a review that says "accept" without having read the paper is
  rejected, and repeated ones remove the contributor from the call.

## How to start

1. Pick an available domain. During private review, obtain repository access from
   the maintainers and use the exact candidate commit they provide. Public install
   instructions will accompany a published candidate or release.
2. Use the skills on a real question; note what is wrong or missing.
3. Review or correct (above), one pull request per skill or per fix.
4. Register your ORCID in `contributors.jsonld` with the pull request.

## Timeline

| Date | Event |
|---|---|
| 2026-09-19 | draft call and publication metadata prepared |
| 2026-10-06 | five candidates remain private; public call not yet confirmed |
| 2026-10-29 | cut moved from 2026-10-31 to 2026-12-15 (owner decision; nobody had been invited by the first date) |
| November 2026 | proposed first tags and Zenodo deposits, subject to release readiness and authorisation |
| 2026-12-15 | authorship cut for the first releases; confirm that reviewers have sufficient access and time before announcing |
| 2027 | proposed subsequent versions; schedule to be confirmed |
