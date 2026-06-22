---
name: Author opt-out request
about: Request removal of your paper from an ASB-Skill collection
title: "[opt-out] <Paper DOI>"
labels: ["author-opt-out", "needs-lead-curator"]
assignees: []
---

<!--
Before filing: please read AUTHOR_OPT_OUT.md. Identity verification
(ORCID + GitHub linkage, or institutional email) is required. Pseudonymous
requests are not honored.
-->

## Paper

- **DOI (required):** <!-- e.g. 10.1186/s13321-024-00878-1 -->
- **Title (required):** <!-- full title from the publication -->

## Requester identity

- **Full name (required):** <!-- as it appears on the paper -->
- **ORCID (required):** <!-- 0000-0000-0000-0000 -->
- **GitHub handle filing this request:** <!-- @your-handle -->

## Scope

- **Collection(s) to remove from:** <!-- e.g. "metabolomics", or "all" -->
- **Versions affected:** <!-- e.g. "metabolomics/v1", or "all versions" -->

## Reason (optional but encouraged)

<!--
Free text. Examples:
- "I withdrew this paper at the journal level."
- "The derived skill misrepresents the method."
- "License restriction I want enforced retroactively."
- "GDPR Art. 17 erasure request."
You do not have to give a reason; identity is what we verify.
-->

## Identity proof (at least one required)

- [ ] **ORCID + GitHub linkage:** my GitHub URL (above) is listed on my
  public ORCID record under "Websites & Social Links".
- [ ] **Institutional email confirmation:** I will follow up from
  `<name>@<institution-domain>` (the corresponding-author affiliation on
  the paper). Reply to this issue from that email's GitHub account.

## Acknowledgement (required)

- [ ] I understand that **bibliographic metadata** (DOI + title +
  `rationale: author_opt_out`) may be retained in
  `collections/<slug>/v<N>/excluded/` for transparency.
- [ ] I understand that **Zenodo records of prior releases cannot be
  deleted**; the affected release will be marked `withdrawn` per
  `RELEASE_ROLLBACK.md`, and a patched release will be issued.
- [ ] I understand the **acknowledgement SLA is 14 days** (7 days for
  emergency removals: plagiarism, fraud, court order, journal retraction).

## For the Lead Curator (leave unchecked when filing)

- [ ] Identity verified (ORCID match + GitHub linkage, or institutional email)
- [ ] Affected derived content enumerated (skills / tools / claims / reviews)
- [ ] Removal PR opened
- [ ] Excluded/ log entry added
- [ ] Release rollback triggered if a tagged release is affected
