# Open-access policy

**Status:** DRAFT (pending CNRS legal counsel review)
**Last updated:** 2026-05-25

This policy governs which scientific papers can be included in ASB-Skill collections, what derived content the project stores, and how access tiers determine what's redistributable.

---

## TL;DR

| Access tier | Source examples | What ASB stores | What ASB shares |
|---|---|---|---|
| **Open-access** | PMC OA, eLife, F1000, MDPI, OA preprints | Full evidence spans, figure references, structured extractions, derivation chain | Everything — same license as source |
| **Hybrid / quotation** | Most Nature, Elsevier, Wiley, Springer | Bibliographic metadata, structured facts (parameters, methods, claims), ≤300-char verbatim quotes per `evidence_span` | Same — quotation is fair-use under Berne Convention art. 10 |
| **Closed (no abstract)** | Paywalled with no Crossref-served abstract | DOI + title + author list only | Bibliographic metadata only — uncopyrightable facts |
| **Retracted** | Any paper with a Crossref retraction notice | All current data + `status: retracted` flag | Marked retracted in `corpus.yaml`; skills sourced *only* from retracted papers carry a warning badge |

Every paper in `corpus.yaml` declares its access tier so downstream consumers can filter.

---

## What ASB derives and why it's legal

ASB processes published scientific papers to produce three classes of artifact:

1. **Bibliographic metadata** — DOI, title, authors, journal, year. These are uncopyrightable facts (US 17 U.S.C. § 102(b); EU Database Directive 96/9/EC art. 7(1)).
2. **Structured factual extractions** — parameters, methods, tools used, EDAM annotations. Facts about the science, not the copyrighted expression. Falls under the same uncopyrightable-facts doctrine.
3. **Short verbatim quotations** — `evidence_spans` capped at 300 characters per span, attributed to the source DOI. Reproduced under the quotation right (Berne Convention art. 10(1); US fair-use under 17 U.S.C. § 107 for purposes of criticism and commentary).

ASB does **not** store or redistribute:

- Full paper text or PDFs
- Figures from closed-access sources
- Tables verbatim (we store structured representations, not the original layout)
- Supplementary material verbatim beyond short quotations

For open-access papers (CC-BY, CC0, etc.), the license permits broader inclusion; we still observe the source paper's license terms when redistributing derived content.

---

## Per-paper access tier rules

### Open-access (`type: open-access`)

- **License declaration required** — SPDX identifier (CC-BY-4.0, CC-BY-NC-4.0, CC0-1.0, Apache-2.0, MIT, etc.)
- **Verification** — `verified_via: unpaywall` + `verified_at: <ISO date>` populated automatically by `verify-paper.yml` CI
- **Permitted inclusion** — full evidence spans, figure references, all structured extractions
- **Redistribution** — under the source paper's license; consumers of ASB-Skill collections inherit those terms

### Hybrid / quotation (`type: hybrid`)

The paper is published in a venue that retains traditional copyright but allows derivative scholarly use via fair-use / quotation rights.

- **License declaration** — `license: copyrighted` (publisher-held); no SPDX
- **Verification** — `verified_via: unpaywall` confirms paywalled access; `verified_at` populated
- **Permitted inclusion**:
  - Bibliographic metadata (always allowed)
  - Structured extractions (facts, uncopyrightable)
  - Verbatim quotes ≤300 chars per `evidence_span`, attributed via `source: <DOI>`
- **Per-quote attribution required** — every `evidence_span` includes the source DOI so users can trace back
- **Cumulative cap** — across all evidence_spans from a single paper, ≤2% of paper word count or ≤1500 chars total (whichever is smaller). This margin keeps quotation within fair-use bounds under all major jurisdictions.
- **Enforcement** — `asb collection promote` runs `_sanitize_quotations_for_release()` after all artifacts are emitted. For any paper with `access.type` ∈ {hybrid, closed, unknown}:
  - SKILL.md `## Evidence` lines are stripped of the trailing `: "verbatim quote"` portion (paraphrase prefix retained — it's independently authored and discriminative).
  - `benchmark/claims/per_paper/*/ground_truth.jsonl` rows where `source_excerpt == text` have the redundant `source_excerpt` field dropped; otherwise truncated to ≤150 chars.
  - A per-DOI accounting written to `quotation_audit.json` for transparent verification.
  - Tool YAMLs are NOT stripped (per-tool excerpts are ≤300 chars and serve attribution purpose; they fall under fair use as critical commentary).
- The sanitizer is **idempotent** — running twice produces no further changes. Running on a pure-OA collection is a no-op.

### Closed (no abstract, `type: closed`)

- **License** — `license: copyrighted-no-access`
- **Permitted inclusion** — DOI, title, author list, journal, year ONLY. No abstract, no quotes, no derived skills/tools/claims.
- **Use case** — citation completeness when a paper is referenced by another included paper but isn't itself processable.

### Unknown (`type: unknown`)

- Default state for newly-promoted papers awaiting `verify-paper.yml` CI assessment.
- **Block from inclusion** — corpus.yaml entries with `access.type: unknown` AND `status: accepted/included` are flagged by CI and require manual resolution before release.

---

## Retraction handling

We monitor Crossref's retraction watch monthly (CI workflow `corpus-freshness.yml`, planned v1.1).

**On detecting a retraction:**

1. `corpus.yaml`: set `status: retracted`, add `retracted_at: <date>` and `retraction_notice_doi: <doi>` fields.
2. Skills sourced **only** from the retracted paper: keep the skill but add `metadata.retracted_sources: true` warning, prepend a `[RETRACTED SOURCE]` notice to the skill body.
3. Skills sourced from the retracted paper **plus** non-retracted sources: drop the retracted DOI from `derived_from`, log the change in `metadata.merge_audit.retraction_events[]`.

Retracted papers are NOT removed from `corpus.yaml` — git history preserves the original entry, and the public record is part of the scholarly trail.

---

## Paper-proposal workflow

To add a paper to a collection's corpus:

1. **Open an issue** using the `Propose paper` template at <`https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=propose-paper.md`>. Include: DOI, title, intended collection, rationale (why this paper).
2. **Discussion** happens on the issue. Anyone may comment with reasoning for or against inclusion.
3. **PR adds the paper** to `corpus.yaml` with `status: proposed`. `verify-paper.yml` CI:
   - Resolves the DOI via Crossref
   - Queries Unpaywall to determine access tier
   - Populates `access.{type, license, verified_via, verified_at}`
   - Flags duplicates (paper already in corpus)
   - Checks for retraction status
4. **Lead Curator review** — confirms thematic fit, rationale quality, access-tier handling. Merging the PR transitions the paper to `status: accepted`.
5. **Next ASB processing run** picks up accepted papers; promoted output transitions them to `status: included` (auto, by `asb collection promote`).

A Lead Curator can solo-approve papers in their domain. For papers spanning multiple domains, two-curator sign-off is recommended (not strictly enforced; up to maintainer judgment).

### Proposal SLA

To keep the queue moving and avoid contributions stalling indefinitely:

| Event | Target | Hard cap |
|---|---|---|
| Lead Curator acknowledges proposal (initial comment) | **7 days** | 14 days |
| First substantive review (accept / request-changes / reject) | **30 days** | 60 days |
| Decision finalised (PR merged or closed) | **45 days** | 90 days |

**Stale handling:** if a `propose-paper` PR has had no maintainer activity in 90 days, a maintainer or any Curator may mark it `stale` and close. The proposer can re-open with new rationale or a different Lead Curator assignment. Closing a stale PR is non-final — the proposal can always be resubmitted.

**Acceleration:** retracted-source detection, security-relevant content, and time-critical methodological corrections can bypass the standard SLA; tag the proposal `expedite` and the lead maintainer assigns directly.

**Volume protection:** during release-cycle freeze (2 weeks before a tag), Lead Curators may pause new-proposal review and resume after the tag. The freeze is announced in `CHANGELOG.md` and on the Discussion forum.

---

## Curator review of derived content

Once a paper is `included`, the skills and tools derived from it can be **reviewed for accuracy** by curators (not the same as the proposal acceptance above):

- Each curator review touches `collections/<slug>/v<N>/reviews/<paper-doi>.yaml`
- The review attests that evidence_spans match the paper's text, parameter values are correct, EDAM annotations are appropriate, tools attributions are accurate
- `verify-coi.yml` enforces non-coauthor sign-off when the reviewer's ORCID is on the paper (see [`COI_POLICY.md`](COI_POLICY.md))
- Reviewers earn tier credit (`Reviewer` / `Domain Contributor` / `Curator` / `Lead Curator`) per [`MAINTAINERS.md`](MAINTAINERS.md)

The static page at <https://holobiomicslab.github.io/asb-skill-collections/paper.html?doi=...> shows all extracted content per paper with one-click "verify" / "flag" buttons that open prefilled PRs/Issues.

---

## Special cases

### Pre-prints

Pre-prints (bioRxiv, medRxiv, ChemRxiv, arXiv) are treated as **open-access** (always CC-BY by repository policy) and may be included. When the peer-reviewed version is later published with a different DOI, the corpus entry is updated to point at the canonical DOI (linking back to the preprint as `source_history`).

### Books and book chapters

Out of scope for v1. Add to backlog if demand emerges.

### Self-published / institutional reports

Case-by-case. Lead Curator decides based on rigor + relevance.

### Multi-author conflicting versions

If two papers describe the same workflow with differing parameters or claims, **both are included**. The skill collection captures the divergence via separate evidence spans with attribution. Reviewers can flag which version is more authoritative; the skill body presents the consensus or notes the disagreement.

---

## Out-of-scope clarifications

- **Citing ASB-Skill collections does NOT require citing every source paper.** The collection's Zenodo DOI is the primary citation; individual paper DOIs are accessible via `corpus.yaml` for those who need finer-grained citation.
- **Inclusion in an ASB collection is NOT an endorsement of the paper's conclusions.** ASB extracts methodology + structured facts, not editorial judgment.
- **Excluded papers (`status: excluded`) remain in `corpus.yaml`** with a rationale. This documents the decision-making, not censorship.

---

## Open questions (resolved by Lead Curator / maintainers)

- Do we accept conference papers / workshop abstracts? **Default: yes if peer-reviewed and DOI-registered; case-by-case otherwise.**
- Do we accept grey literature (technical reports, theses)? **Default: no for v1; revisit if requested.**
- What's the SLA on retraction detection? **Default: monthly automated check; reactive on community report.**
- How are disputes about inclusion resolved? **Default: discussion on the proposal issue; Lead Curator has final call; appeals go to the asb-skill-collections maintainers.**

---

## License of this policy

This document is released under CC0; reuse it for your own scientific-AI corpus governance.
