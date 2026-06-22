# Author Opt-Out Policy

Paper authors may request removal of their work, and any skills / tools / claims
derived from it, from any ASB-Skill collection. This document defines who is
eligible, what we remove, what we retain, and the timelines we commit to.

## When this policy applies

You may request opt-out if you are a **named author** on a paper currently
ingested in (or staged for) an ASB-Skill collection. We verify authorship via
**either**:

- An **ORCID match** between the requester and the paper's author list
  (OpenAlex-resolved), **and** the GitHub account opening the request is listed
  on the requester's public ORCID record (the same L1 check used for curator
  vetting); **or**
- A request opened from an **institutional email address** matching the paper's
  corresponding-author affiliation, followed by an ORCID linkage step.

Pseudonymous requests, requests from third parties, and requests where identity
cannot be verified within 30 days are **not honored**.

## How to request opt-out

1. Open a "Request removal" issue using the
   [`.github/ISSUE_TEMPLATE/author-opt-out.md`](.github/ISSUE_TEMPLATE/author-opt-out.md)
   template. The template auto-applies the `author-opt-out` and
   `needs-lead-curator` labels.
2. Fill in the paper DOI, your ORCID, the affected collection(s), and the
   identity-proof link.
3. The relevant Lead Curator is automatically notified (label routing) and
   acknowledges the request within the SLA below.

## What we remove

On approval, the following changes land in a single PR labelled
`author-opt-out`:

- `corpus.yaml` entry for the paper is transitioned to
  `status: excluded` with a `rationale: author_opt_out` field and a link to
  the originating issue.
- Derived **skills** for which this DOI is the **sole source**
  (`provenance.source_papers` is a single-element list containing only this
  DOI) are deleted from `collections/<slug>/v<N>/skills/`.
- Derived skills with **multi-paper provenance** have this DOI stripped from
  `provenance.source_papers`. If the resulting list is empty, the skill is
  deleted; otherwise it is kept and its `derived_at` timestamp is bumped.
- Derived **tools** (`tools/<slug>.yaml`) follow the same rule: sole-source
  entries are deleted, multi-source entries have the DOI removed.
- The paper's benchmark / claims directory
  (`benchmark/claims/per_paper/<doi-slug>/`) is deleted in full.
- Per-paper attestations under `collections/<slug>/v<N>/reviews/<doi-slug>.yaml`
  are deleted.

## What we retain

For transparency and audit reasons we retain:

- The **bibliographic stub** (DOI + title + the
  `rationale: author_opt_out` marker) in
  `collections/<slug>/v<N>/excluded/<doi-slug>.yaml`. This documents *that*
  the paper was once included and was removed at author request, without
  republishing any derivative content.
- The original Zenodo deposit of the affected release (see below — we cannot
  delete Zenodo records). The deposit metadata is updated to
  `withdrawn` per `RELEASE_ROLLBACK.md`.

ORCID-verified opt-out requests, including the bibliographic stub and the
removal rationale, are **public**. We do not honor opt-outs that require us
to also conceal that the opt-out occurred.

## Timelines (SLA)

| Step | Target |
|---|---|
| Lead Curator acknowledgement | 14 days from issue open |
| Full removal in release branch | next release cycle, **<=60 days** from acknowledgement |
| Emergency removal (plagiarism, fraud, court order, retraction) | 7 days from acknowledgement |

If the Lead Curator is unreachable for 14 days, a maintainer (see
`MAINTAINERS.md`) takes over the request.

## Appeals

If the Lead Curator denies the request — e.g. identity verification fails, or
the request appears to come from a third party — the requester may appeal to
the maintainers by replying on the same issue with `cc @lfnothias` (or the
current lead maintainer). The maintainer decision is final at the project
level; statutory rights below are not affected.

## What we will not do

- We do **not** retroactively delete Zenodo records. Zenodo DOIs are
  permanent by design; instead, the affected release is marked
  `withdrawn` and a patched release is issued (see
  `RELEASE_ROLLBACK.md`).
- We do **not** rewrite or backdate prior release history. Tagged releases
  remain reachable in git history. The `excluded/` log truthfully records
  what changed and when.
- We do **not** silently scrub derived content without leaving the
  bibliographic stub. Authors who want to suppress *all* trace of inclusion
  should not have proposed the paper, or should request emergency removal
  with a documented legal basis (see below).

## Legal basis

We honor opt-outs under three frameworks, in order of precedence:

1. **GDPR right to erasure (Art. 17)** for personal data
   incidentally surfaced in derived content (author names, affiliations,
   biographies). This is processed within the GDPR statutory timeline
   regardless of release-cycle SLAs above.
2. **Retroactive honoring of restrictive licenses.** If a paper was ingested
   under a misread license (e.g. we treated CC-BY-NC content as permissive,
   or used CC-BY-ND content in a derivative form), we remove the derived
   content on request and document the license-handling error.
3. **Reputation-based requests** (the author objects to the framing or
   accuracy of derived content but not to inclusion per se) are handled
   case-by-case. In most such cases the appropriate route is
   `DISPUTE_RESOLUTION.md`, not opt-out.

For questions about this policy, contact the lead maintainer listed in
`MAINTAINERS.md`.
