# Dispute Resolution

This document defines the process for disputing the **correctness** of a
derived skill, tool, claim, or benchmark task in an ASB-Skill collection.
It applies when someone — typically a paper author, but also a community
reader or a curator — believes the derived content **misrepresents** the
source paper or contains a factual error.

## Scope

**In scope:**

- "The derived skill says my method does X; my paper says Y."
- "The claim extraction reverses the sign of an effect reported in the paper."
- "The tool entry attributes a capability to my software that it does not have."
- "The benchmark task assumes a parameter range that is not what the paper describes."

**Out of scope** (handled elsewhere):

- Requests to remove a paper entirely -> `AUTHOR_OPT_OUT.md`
- COI accusations against a reviewer -> `COI_POLICY.md`
- License or attribution complaints -> open a maintainer issue
  (`MAINTAINERS.md`)
- Subjective preferences ("I would have framed this differently"),
  style debates, naming bikesheds — these are not disputes; open a
  regular PR with the proposed wording change.

## Process (4 steps)

### 1. Open a dispute issue

File a GitHub Issue using the `dispute-derived-content.md` template
(forthcoming; if not yet present, use a blank issue with the
`dispute` label). Include:

- Affected artifact path
  (e.g. `collections/metabolomics/v1/skills/<slug>/SKILL.md`)
- The specific text or field you dispute (quote it)
- The source-paper passage that contradicts it (DOI + page / section)
- Your relationship to the paper, if any (author, reader, curator)

### 2. Lead Curator response

The Lead Curator who **approved the original paper** for the collection
is automatically assigned. They must respond within the SLA below with
one of three outcomes:

- **Agree:** they open a correction PR amending the disputed content.
  The dispute issue stays open until the PR merges.
- **Disagree:** they post an explanation citing the source paper and
  explaining why the current derivation is faithful. **A bare "no" without
  rationale is grounds for appeal** under step 4.
- **Escalate:** they explicitly defer to step 3 (e.g. the question is
  outside their sub-domain expertise, or they have a COI on the paper).

### 3. Peer-curator review (if escalated)

Two additional curators — drawn from the same or a related domain, and
**not** the original Lead Curator — review the dispute. Each posts a
comment with their position and reasoning. **Majority opinion stands.**
A tie defers to step 4.

Peer reviewers must be at >=Curator tier in `contributors.jsonld` and must
have no COI on the affected paper (per `COI_POLICY.md` rules).

### 4. Maintainer appeal

If the disputant is not satisfied after step 2 or step 3, they may appeal
to the maintainers (see `MAINTAINERS.md`). The maintainer decision is
final at the project level.

## Response-time SLAs

| Disputant | Lead Curator first response | Peer-curator review | Maintainer appeal |
|---|---|---|---|
| Verified paper author (ORCID match) | 7 days | 14 days | 21 days |
| Anyone else | 14 days | 21 days | 28 days |

"Verified paper author" uses the same ORCID-match check as
`AUTHOR_OPT_OUT.md`. Paper-author disputes get priority because they
carry the most direct knowledge of the source content.

## Standards for Lead Curator responses

A "disagree" response must include:

- An explicit quotation or paraphrase from the source paper supporting
  the current derivation.
- Reasoning that addresses the disputant's specific claim, not just a
  general statement of confidence.

Responses that fail this standard (e.g. "looks fine to me", "we reviewed
this already") are grounds for **automatic escalation to step 3** at the
disputant's request, without going through the appeal in step 4 first.

## Record-keeping

All dispute resolutions are **public**. When a dispute is closed
(merged correction, rejection, or appeal outcome), a structured
record is appended to the affected paper's `corpus.yaml` entry under
`review_status.disputes[]`:

```yaml
review_status:
  disputes:
    - issue: "#142"
      opened: 2026-06-01
      closed: 2026-06-12
      outcome: corrected   # corrected | rejected | appealed-overturned | appealed-upheld
      affected: collections/metabolomics/v1/skills/<slug>/SKILL.md
      summary: "Claim direction was reversed; corrected in PR #143."
```

This makes the dispute history queryable as part of normal corpus tooling
and visible to future readers of the affected paper's record.

## Curator quality bar

If a Lead Curator accumulates **3 or more unresolved disputes** against
their decisions within a single release cycle (where "unresolved" means
the disputant appealed to step 4 and the maintainers overturned the
Curator's call), the maintainers conduct a **tier review** of that
Curator. The review may result in:

- No change (e.g. disputes were borderline)
- Mentorship pairing for the next release cycle
- Tier demotion per `CONTRIBUTING.md` tier rules

Tier reviews are not punitive by default — the goal is to identify
patterns of misderivation early and correct them before they propagate
into the next release.

## Questions

Open a GitHub Discussion or contact the lead maintainer
(see `MAINTAINERS.md`).
