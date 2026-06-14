# Content Provenance & Transformation Policy

**Status:** v0 Final · **Date:** 2026-06-14 · **Authority:** Lead Maintainer (Louis-Félix Nothias, ORCID: TODO-REAL-ORCID)

**Sign-off:** This policy authorizes the v0 release and gates all content publication. Override authority and hard-gate enforcement rules are legally binding.

---

## 1. Overview

This policy establishes the legal and operational boundaries for ingesting, storing, transforming, and publishing scientific content through the ASB (AgenticScienceBuilder) factory and registry. It covers three tiers of content, the open-access-first commitment for v0, licensing, transformation bounds, content safety gates, and the takedown procedure.

**Core principle:** ASB transforms copyrighted source papers into independently-authored structured artifacts (benchmarks, skills, capsules) grounded in facts and methods (not copyrightable) and attributable to their sources via DOIs and fair use. All public releases are legally defensible on fair-use grounds and explicitly license-compliant.

---

## 2. Three-Tier Content Model

### Tier 1: Private Corpus (Never Released)

- **What:** Full-text PDFs, bibtex, author metadata, multimedia, and preprint versions of source documents
- **Storage:** Private data repos (CNRS GitLab / koda) with access restricted to pipeline agents and curators
- **Visibility:** Closed; never published or uploaded to Zenodo/HF
- **Purpose:** Reproducible, citable anchor for the factory; legal defense for fair-use claims
- **v0 policy:** Corpus admits **only open-access papers** (OA-verified at ingestion). Non-OA papers are rejected at the curation gate (§7.4). This minimizes legal exposure while the gate matures.

### Tier 2: Private Intermediates (Koda Only)

- **What:** Perspicacité KB embeddings, chunked text, the verbatim **claim ledger** (anchored quotes with source spans), enriched entity graphs
- **Storage:** Private koda server (:8002, Chroma DB snapshots, git-ignored KB snapshots); never committed to public code repos
- **Visibility:** Closed; the claim ledger is discoverable internally only
- **Purpose:** Grounding for synthesis and claim attribution; source-fidelity checking at release time
- **Retention:** Snapshots timestamped and versioned per release; old snapshots archived per institutional retention policy

### Tier 3: Public Artifacts (Transformed, Published)

- **What:** Benchmark task JSON, skill SKILL.md files with YAML frontmatter, tool records, leaderboards, claims exports, RO-Crates, and indicium documents
- **Storage:** Public GitHub repos (this registry), HuggingFace Datasets/Spaces, Zenodo, w3id.org
- **Visibility:** Open; discoverable, downloadable, citable
- **Purpose:** Reusable, citable building blocks for AI agent development and evaluation
- **Content:** Transformed (never verbatim-heavy); claims as structured facts + DOI attribution; tools as metadata; workflows as own-words descriptions
- **Guarantee:** All Tier 3 artifacts pass the release gate (§5) before publication

---

## 3. Open-Access-First Commitment (v0)

**Locked decision (2026-06-14):** ASBB v0 ingests **only open-access papers** with verifiable OA status.

### Definition

**OA-tier enum (single source of truth).** The allowed open-access tier values are aligned to `src/agentic_science_builder/release/promote.py` (in the AgenticScienceBuilder repo). The allowed OA set is:

```
{open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond}
```

Both hyphen and underscore spellings are accepted; `green` normalizes to `green-oa` (see §7.5 verify-paper.yml normalization step).

A paper qualifies as **open-access** if its access tier is one of the values above, i.e. it is published under one of the following:

1. **Gold OA** (`gold-oa` / `gold_oa`) — published under a CC-BY, CC-BY-SA, CC0, or equivalent permissive CC license by the publisher
2. **Green OA** (`green-oa` / `green`) — self-archived by the author in an institutional or disciplinary repository (arXiv, PubMed Central, etc.) with explicit OA license or public-domain designation (e.g., PubMed Central NIH/USDA papers)
3. **Diamond OA** (`diamond`) — published in a no-fee, no-charge OA journal (no APC to author or reader)
4. **Generic OA** (`open-access` / `open_access` / `oa`) — verified open access where the specific tier is not further resolved
5. **Government works** — papers authored by U.S. federal employees in their official capacity (public domain by law); recorded with a generic OA tier plus a public-domain license tag

> **NOTE — `preprint` is NOT an OA tier.** "Preprint" is a value on a **separate provenance axis** (the version/stage of the document: preprint vs. accepted-manuscript vs. version-of-record), recorded in `provenance.version` / `provenance.source`. It is NOT a member of the OA set above and MUST NOT be used as `access.type`. A bioRxiv/medRxiv/arXiv preprint is admitted because its access tier is open (`open-access` / `gold-oa` as applicable) AND its provenance is `preprint`; the two axes are recorded independently. Do not conflate the open-access axis with the provenance axis.

### Non-OA Exclusion

Papers with the following status are **rejected at curation**:

- Closed/paywalled (Elsevier, Springer, Wiley, etc. without OA marking)
- Hybrid (tagged as hybrid OA but underlying license is restrictive)
- Unknown (access status unresolved)
- Green OA with restrictive manuscript license (author-accepted manuscript under All Rights Reserved)

### Verification Procedure

1. **Automated check:** OpenAlex API lookup; flag `is_oa: true|false`
2. **Manual spot-check:** Sample papers in the final corpus (≥10% per domain) to confirm OA license accuracy
3. **Red-flag gate:** CI verify-paper.yml (stage §7.5) enforces `access.type ∈ {open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond}` (after hyphen/underscore + `green`→`green-oa` normalization) for all `status:included` papers; unknown/non-OA triggers a hard fail. `preprint` is rejected as an `access.type` value because it is a provenance value, not an OA tier.

### Exception Procedure (Post-v0)

Admission of closed-access or hybrid papers is deferred to v1. If a post-v0 release includes closed sources:

1. A legal review must be completed (recommend institutional counsel)
2. The decision is recorded in a new `CLOSED_ACCESS_POLICY.md` addendum
3. The release notes must explicitly label affected artifacts as "mixed" or "closed" tier (§4)
4. The `benchmark_tier.openness` axis defaults to `closed` or `mixed` for that release

---

## 4. License & Rights Split

### Code & Synthesis Layer

**License:** MIT (skills, tools, benchmarks, Zenodo source artifacts)

- Script bundles (`skill.md`, `tool.json`, `collection.yaml`, `CITATION.cff`)
- Structured metadata (EDAM annotations, parameter schemas, RO-Crates)
- ASB-generated prose (descriptions, validation notes, methods summaries)

**Rights:** Fully reusable, modifiable, redistributable without restriction.

### Verbatim Paper Quotations

**License:** Fair use (UK Copyright Act §30, EU Directive 2001/29/EC Art. 5.3(d), US Copyright 17 U.S.C. §107)

- Quotations are **minimal** (single sentences, <150 characters)
- **Non-substitutive** (not reproduced as a substitute for reading the original)
- **Properly attributed** (source DOI, author list, page/section pointer in frontmatter)
- **Non-commercial** (no commercial re-licensing or resale of quote collections)

### Benchmark Tasks & Expected Outputs

**License:** MIT (same as code)

- Task descriptions, workflows, expected outputs
- Claim assertions (structured as `[claim, evidence_span_doi, evidence_span_metadata]`)
- Evaluation rubrics and scoring logic

### Paper-Derived Data Artifacts

**License:** Dual — CC-BY for benchmarks; fair use for embedded quotes

- Benchmark datasets (task JSON, claim retrieval sets): CC-BY 4.0 International
- Leaderboards: CC0 (public domain) to allow unrestricted reuse
- Zenodo deposition: CC-BY 4.0; w3id IRI redirects: CC0

### Empirical Results & Metrics

**License:** CC0 (public domain) to encourage reproducibility and remixing

- Leaderboard scores, solver evaluation results, failure-mode catalogs
- Metadata tables (paper statistics, openness tier distribution)

---

## 5. Release Gate: Transformation & Attribution

The release gate is the checkpoint between private Tier 2 and public Tier 3. Every artifact must pass before publication to Zenodo, HF, or the public GitHub `collections/` directory.

### Gate Procedure

**Entry:** Capsule paths + corpus metadata, run on local ASB checkout
**Exit:** `release-gate-report.json` (PASS|WARN|FAIL) + artifacts for promotion to `staged-collections/`
**Enforcement:** Advisory on PRs to `staged-collections/`; **hard-blocking** on promotion to `collections/` and on the release tag

### Gate Checklist (14 gates; v0 activates gates 1,2,5,6,8,9,10,12,15; gates 3,4,7,11-14 documented but non-blocking)

| # | Gate | Owner | Criterion | Trigger | v0 Enforcement |
|---|---|---|---|---|---|
| **1** | **asb-schema published** | A+H | LinkML `asb-schema` repo public + registered | gate check: lookup on GitHub | warn-only (schema not published yet) |
| **2** | **Paper access tier resolved** | A | Every `status:included` paper has `access.type` in the OA set `{open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond}` (post-normalization) | CI verify-paper.yml | hard-block non-OA / unknown |
| **3** | **Indicium schema version pinned** | A | Collection YAML lists `schema_versions.indicium: <real-tag>` from indicium repo | gate check: git tag exists | warn-only (gate 3 not activated v0) |
| **4** | **Profile reproducibility** | A | Generation manifest includes `profile_hash`, `llm`, `seed` enabling exact rebuild | manifest validation | warn-only (gate 4 not activated v0) |
| **5** | **Verbatim quotation caps** | A | Sum of `evidence_span` lengths across all skills/claims ≤ corpus-size-dependent cap (§5.3) | gate check: char count | hard-block (fail if exceeded) |
| **6** | **Similarity check (verbatim vs original)** | A | N-gram overlap + embedding cosine for each `evidence_span` vs Tier-1 source ≤ threshold (§5.4) | gate check: automated similarity scan | hard-block (flag/block spans for rewrite) |
| **7** | **Claim fidelity (indicium round-trip)** | A | Every skill claim resolves in `benchmark/claims/` ground truth; `trace_status: exact_match` | gate check: indicium `verify-claims` | warn-only (gate 7 not activated v0) |
| **8** | **DOI & license resolution** | A | Every artifact lists source DOI(s) + license SPDX tag; Zenodo lookup succeeds or entry is public preprint | gate check: CrossRef/Zenodo API | hard-block (fail if DOI invalid) |
| **9** | **Indicium adapters published** | A | All four indicium adapters (sepio, sssom, prov, claims) are publicly available + versioned | gate check: lookup on PyPI/GitHub | warn-only (adapters not published yet) |
| **10** | **Registry consistency** | A | `marketplace.json` ↔ `catalogue.jsonld` ↔ filesystem reconciliation passes; no duplicates, IRI conflicts, or missing files | CI validate.yml → asbb registry verify | hard-block (fail if drift) |
| **11** | **Leaderboard schema valid** | A | `benchmark/leaderboard.jsonld` validates against JSONLD context; CiTO link types recognized | gate check: JSONLD parser + CiTO vocab | warn-only (gate 11 not activated v0) |
| **12** | **Contamination / held-out audit** | A | For open-tier releases: no held-out test splits mixed into public outputs; for closed-tier: held-out marker present (v1+ only; v0 open-only) | gate check: output file audit | hard-block (fail if contamination detected) |
| **13** | **Independent co-reviewer (gate §9 waiver)** | A+H | (v1) If `is_coauthor: true` on any collection attestation, a second verified reviewer (non-coauthor, ≥Reviewer tier) has signed off | CR-P0-02 attestation review | **FORMALLY WAIVED for v0** — self-merge permitted; no second reviewer required pre-tag (waiver logged in §9 + release notes) |
| **14** | **≥20 external reviews (gate §9 waiver)** | A+H | (v1 TARGET) Lead Curator's external-review count (papers with `is_coauthor:false`) ≥ 20 | tier-update.yml CI + manual audit | **FORMALLY WAIVED for v0** — ≥20 external reviews is the v1 target, NOT enforced at v0 (waiver logged in §9 + release notes) |
| **15** | **v0 OA-only access tier** | A | All included papers `access.type` in the OA set `{open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond}` (post-normalization); no closed/hybrid/unknown mixed in. Gate 15 asserts ONLY the paper-access (`require_open_access`) axis; it does NOT assert workflow openness (`benchmark_tier.openness`) | verify-paper.yml CI | hard-block v0 (non-OA auto-fail) |

### 5.1 Verbatim Quotation Cap

**Purpose:** Prevent transforming a paper summary into a thinly-paraphrased republication (fair-use ceiling).

**Rule:** Cumulative character count of all `evidence_span` values in a collection's skills ≤ 15% of the corpus's **total publicly-available** text (i.e., sum of word-counts × 4.7 chars/word).

- **Formula:** `sum(evidence_span_lengths) / (corpus_word_count * 4.7) ≤ 0.15`
- **Per-paper cap:** No single paper's evidence spans exceed 20% of its own published abstract + introduction (prevents over-quoting a single source)
- **Exception:** Preprints on bioRxiv/medRxiv (text publicly available) count toward corpus size; paywalled paper abstracts count at abstract length only (conservative)

**Gate action:** If exceeded, halt promotion with a list of spans to remove/paraphrase. Curator rewrites spans and re-runs gate.

### 5.2 Evidence Span Definition & Attribution

An `evidence_span` is:

```yaml
evidence_span:
  text: "exact verbatim quote from source"
  doi: "10.xxxx/source-doi"                    # required
  section: "Introduction / Methods / Results"  # optional but recommended
  page_or_line: "p.5 / line 247"               # if available
```

**Attribution requirement:** Every skill markdown includes a `derived_from` block:

```yaml
derived_from:
  - doi: "10.xxxx/paper1"
    role: methods_extraction
    citation_key: "Smith2020"
  - doi: "10.yyyy/paper2"
    role: parameter_values
    citation_key: "Jones2021"
```

### 5.3 Similarity Check (n-gram overlap + embedding cosine)

**Purpose:** Flag text spans that are too close to original wording and trigger a rewrite.

**Method:**

1. **N-gram overlap:** 3-gram Jaccard similarity between `evidence_span` and the paragraph it derives from in the source
   - Threshold: Jaccard ≤ 0.30 (i.e., <30% n-gram overlap with source paragraph)
   - Interpretation: >30% overlap suggests paraphrasing has not occurred; flag for rewrite

2. **Embedding cosine similarity:** Encode `evidence_span` + 100-char source context with `text-embedding-3-small`
   - Threshold: cosine ≥ 0.92 (i.e., >92% semantic overlap)
   - Interpretation: High cosine suggests the span is a near-synonymous restatement rather than transformative extraction

**Gate action:**
- **Automatic block:** If BOTH conditions exceed threshold (n-gram >0.30 AND cosine >0.92), halt promotion
- **Manual review:** If ONE exceeds, flag in the gate report with a WARN; curator assesses and either removes the span or provides rewrite + justification
- **Acceptable pairs:** <30% n-gram overlap OR <0.92 cosine (OR both below) passes automatically

**Tool:** `src/agentic_science_builder/release/similarity_check.py` (integrated into `release_gate.py`).

---

## 6. Content Safety Gates: PII & Dual-Use

### Two-Tier PII / Human-Subjects Gate

**Purpose:** Prevent release of identifiable personal information and dual-use research of concern (DURC).

#### Tier 1: Hard Fail (Blocking)

**Gate fails if ANY of the following are detected in verbatim quote spans or expected outputs:**

1. **Named clinical identifiers** — patient names, hospital IDs, medical record numbers, account numbers matching regex patterns for clinical systems (NHS, HIPAA-sensitive formats)
2. **Explicit health information** — "Patient XYZ has [diagnosis]", "Subject ID 12345 showed [phenotype]" within verbatim quote spans
3. **Emails of individuals** (non-author) — personal email addresses (name@domain) embedded in quotes, EXCEPT:
   - Author/corresponding-author emails (allowlisted in frontmatter)
   - Institutional lab-group emails (role@institution.ac.uk)
4. **Confirmed dual-use content** — synthesis instructions, weaponization methods, organism-enhancement protocols flagged by human review as belonging to DURC categories per NIH/NSF DURC definitions

**Detection method:**
- Regex scan of verbatim quote spans against a versioned PII pattern library (config: `src/agentic_science_builder/release/pii_patterns.json`)
- LLM-judge secondary pass for context (e.g., "is this a real patient name or a placeholder?")
- Keyword screen for dual-use red-flag terms (pathogen enhancement, gain-of-function, weaponizable, etc.; curated list in same config)

**Action:** Block promotion; list flagged spans; route to human curator for inspection + removal.

#### Tier 2: Warning + Human Route (Advisory)

**Gate emits a WARN (does not block) if:**

1. **Suspected PII but low confidence** — name-like string in clinical context (>50% char overlap with common names) but not a confirmed match; placeholder-like patterns (Subject_123, Patient_A); initials only
2. **Ambiguous dual-use** — mentions of controlled organisms or methods in a neutral/defensive context (e.g., "risk factors in [pathogen] infection") without active instruction
3. **Author emails** not in the allowlist but recognizable as institutional (guessable from paper header)

**Action:** Gate passes with WARN; curator reviews and either:
- Adds email to author allowlist if legitimate
- Removes span if error-prone
- Escalates to institutional compliance officer if genuine DURC concern
- Documents decision in the gate report

### 6.1 Red-Team Test Fixture

**Requirement (v0):** A small curated fixture of **seeded PII + benign dual-use examples** must be maintained and gate-tested before every release.

**Fixture location:** `/tests/fixtures/pii_dual_use_red_team.jsonl`

**Fixture contents:**
```jsonl
{"name": "clinical_identifier", "span": "Patient John Doe, age 47, MRN 123456789", "category": "PII", "expected_gate_result": "HARD_FAIL"}
{"name": "placeholder_safe", "span": "Subject 12 in the control group", "category": "placeholder", "expected_gate_result": "WARN"}
{"name": "dual_use_defensive", "span": "Mechanisms of pathogen X transmission in respiratory epithelium", "category": "dual_use_defensive", "expected_gate_result": "WARN"}
{"name": "benign_organism", "span": "E. coli K-12 is a common laboratory strain", "category": "safe", "expected_gate_result": "PASS"}
```

**Test:** `pytest tests/test_pii_dual_use_gate.py` must achieve ≥95% recall on the HARD_FAIL category (i.e., ≤1 false negative per 20 red-team samples). Gate is permitted to ship only if test passes.

### 6.2 Pattern Library Versioning

PII patterns, dual-use keywords, and author allowlist are versioned in a committed config file: `src/agentic_science_builder/release/pii_patterns.json`. Every release documents which version was used.

---

## 7. Enforcement Points & Gate Workflow

### 7.1 Advisory Gate: Pull Requests to `staged-collections/`

**Trigger:** Any PR that adds or modifies files in `staged-collections/`.

**Workflow:** `.github/workflows/validate.yml` runs:
- `asbb registry verify` (gates 1,2,5,6,8,10)
- `release_gate.py` with `--advisory` flag (gates 3,4,7,11-14 suppress hard-blocks; all output as PR comments)

**Result:** One PR comment listing all WARN + FAIL findings, with links to line numbers. Merge is **NOT blocked**; curator reviews and may merge if they accept the warnings.

**No override needed:** Curator can merge a PR with WARNs at any time (this is a staging area).

### 7.2 Hard-Block Gate: Promotion from Staged → Collections

**Trigger:** Curator opens a promotion PR (`promote-collection.yml`) moving a collection from `staged-collections/` to `collections/`.

**Workflow:** `.github/workflows/promote-collection.yml` runs:
- `release_gate.py` with `--strict` flag (all gates 1,2,5,6,8,10,12,15 hard-block on FAIL)
- COI verification (if collection includes attestations)
- Leaderboard consistency check

**Result:** All FAIL gates must be resolved before merge. WARNs are listed but do not block; curator signs off.

**Override:** Lead Maintainer may set `coi_override: true` in the attestation or `degraded_release: true` in the promotion PR description, **except for hard gates (2,5,6,8,10,12,15) which are never overridable** (see §8).

### 7.3 Hard-Block Gate: Release Tag

**Trigger:** A maintainer creates a release tag `<slug>-v<N>` and pushes it.

**Workflow:** `.github/workflows/release.yml` runs:
- Full `release_gate.py` (all 15 gates, hard-block on gates 1,2,5,6,8,10,12,15)
- Zenodo deposition + DOI mint
- HF mirror trigger (`mirror-to-hf.yml`)
- Catalogue regeneration + w3id IRI assertion

**Result:** If any hard gate fails, the action aborts; tag is not pushed; Zenodo deposition is reverted (fail-soft).

### 7.4 DOI Topology (locked decision, 2026-06-14)

**Exactly ONE Zenodo concept-DOI per collection-release.** Each tagged collection-release (`<slug>-v<N>`) is a single versioned Zenodo deposition under one concept-DOI; all versions of a collection live under that one concept.

The following ride as **FILES inside that single deposition** — they do NOT receive separate DOIs:

- the **KB snapshot** (the pinned grounding knowledge base for the collection),
- the **indicium schema version** (recorded as `indicium_version.txt` / pin file), and
- the **asb: ontology Turtle** snapshot (`asb_ontology.ttl`) at this release.

**indicium has its own, separate concept-DOI** (minted from the indicium repository's own releases). The collection deposition only *pins/attaches the indicium schema version as a file*; it does not re-mint a DOI for indicium. Do not create per-file or per-export DOIs (no DOI matrix explosion).

### 7.5 Install Surface vs. asbb CLI (Phase 1.7)

The **install surface** is the Claude Code plugin marketplace, NOT the `asbb` CLI:

```
/plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections
```

resolved via `.claude-plugin/marketplace.json` (note: the manifest lives at `.claude-plugin/marketplace.json`, not at the repo root). The `asbb` CLI is **to-build (Phase 1.7)** and covers **registry / verify / doctor ONLY** — it is NOT the install path.

### 7.6 Two Independent Axes: OA-access vs. Workflow-openness

The OA-access axis and the workflow-openness axis are **separate and independent**:

- **`require_open_access`** — the paper-access axis (is the *source paper* open access?). Gates 2 / 15 enforce this against the OA set in §3. Always `true` for v0.
- **`benchmark_tier.openness`** (`open` | `mixed` | `closed`) — the *workflow*-openness axis (are the benchmark's held-out splits/workflow open?). Used by the contamination gate (12), NOT by the access gates.

A collection can be OA-only (`require_open_access: true`) while its `benchmark_tier.openness` is independently `open`, `mixed`, or `closed`. Never collapse these two axes into one field.

---

## 8. Override Authority & Hard-Gate Enforcement

### 8.1 Who Has Override Authority

**v0 rule (locked decision, 2026-06-14):**

- **Lead Maintainer (Louis-Félix Nothias)** has sole authority to override soft gates (1,3,4,7,9,11,13,14) for valid reasons (e.g., "asb-schema is not published yet, but gate 1 is documented as warn-only in v0")
- **Hard gates (2,5,6,8,10,12,15) are NEVER overridable**, not even by the Lead Maintainer

### 8.2 Hard Gates (Never Overridable)

These gates protect core content integrity and legal compliance:

| # | Gate | Why Non-Overridable |
|---|---|---|
| **2** | Paper access tier | v0 is legally defensible only on open-access grounds; non-OA papers expose the lab to copyright claims |
| **5** | Quotation caps | Fair-use ceiling; exceeding it risks legal challenge from rights holders |
| **6** | Similarity check | Flags passages that are too close to original for fair use; overriding would admit indefensible copies |
| **8** | DOI & license resolution | Artifacts without source DOI are unattributable and unpublishable; license mismatch is a license violation |
| **10** | Registry consistency | Broken marketplace/catalogue creates silent user confusion; unacceptable even for single-release |
| **12** | Contamination check | Mixing held-out test data into public outputs violates the evaluation covenant; unforgivable |
| **15** | v0 OA-only | Core v0 commitment; any non-OA inclusion invalidates the "legally clean first release" claim |

### 8.3 Override Procedure (Soft Gates Only)

If a soft gate fails and the Lead Maintainer decides override is justified:

1. **Document the override in the promotion PR or release tag description:**
   ```markdown
   coi_override: true
   degraded_release: true

   Justification: Gate 3 (indicium version pinned) fails because the indicium
   co-release is not yet tagged. This is acceptable for v0 because the indicium
   version is locked in the generation manifest and can be re-resolved post-release.
   
   See IMPLEMENTATION-PLAN.md task RT-P1-06 for indicium co-release schedule.
   ```

2. **Publish the override rationale in the release notes** (CHANGELOG / tag description)

3. **Log the override in a new section of this policy** (below, for audit trail)

### 8.4 Hard-Gate Violations: Immediate Takedown

If a hard-gate violation is discovered **after release** (e.g., a non-OA paper slipped through verify-paper.yml, or a PII span made it into public artifacts):

1. **Lead Maintainer declares a takedown** (issue, email to maintainers@...)
2. **Within 48 hours:** Remove the artifact from GitHub, HF, and w3id.org
3. **Within 1 week:** Notify Zenodo and request deposition retraction + DOI suppression (note in Zenodo UI: "retracted for [reason]")
4. **HF Datasets:** Mark dataset as private; post a deprecation notice to the dataset card
5. **w3id.org:** Deprecate the IRI (HTTP 410 Gone or 301 redirect to a deprecation notice)
6. **Postmortem:** Document root cause and corrective action in `CHANGES.md` or a new `INCIDENT_LOG.md`

---

## 9. Governance: Review Gates 13 & 14 (v0 Waiver)

The full spec (§9 Community/Public Expert Review, SPEC.md §9.7.6) defines gates 13 and 14:

- **Gate 13:** Independent co-reviewer present when `is_coauthor: true` on any attestation
- **Gate 14:** ≥20 external reviews (Lead-Curator non-self minimum)

### v0 Waiver Justification (LOCKED 2026-06-14)

**Context:** ASB v0 is a single-maintainer, single-lead-curator release. Gates 13 & 14 are designed for a mature multi-curator governance model with multiple independent reviewers. Enforcing them at launch would be a structural impossibility.

**v0 Exception (BOTH gates FORMALLY WAIVED):**

1. **Gate 13 (independent co-reviewer) — FORMALLY WAIVED for v0**
   - v0 permits self-review of papers where the reviewer is a co-author (with full disclosure in attestation)
   - A second/independent co-reviewer is NOT required at v0
   - **Self-merge is PERMITTED** for v0: the Lead Maintainer may self-merge PRs they authored, with the waiver logged in the release. There is NO "no self-merge" invariant at v0 — any such invariant is superseded for v0.
   - Lead Curator signs off on all attestations (single authority)

2. **Gate 14 (≥20 external reviews) — FORMALLY WAIVED for v0**
   - ≥20 external reviews is the **v1 target**, NOT enforced at v0
   - v0 sets no minimum external-review count; the gate is waived rather than lowered
   - v0 releases are labeled "pre-peer-review" / "community-review-eligible" in release notes

**Waiver logging:** This waiver is logged here (§9 + §13 waiver summary) and MUST also be recorded in the release notes / CHANGELOG of each v0 collection release.

### v0 Release Label

All v0 releases include a banner in README and collection.yaml:

```markdown
### Community Review Notice

This collection was curated and published under v0 governance (single lead curator, 
community-review-eligible). The full peer-review gates (external-review minimum, 
multi-curator consensus) are enabled for v1. 

**To request a community review of a collection**, open an issue with label 
`review-requested` and reference the DOI.
```

### v1 Enforcement

Starting with v1 (scheduled ~Q4 2026):

- Gate 13 becomes a hard requirement (independent co-reviewer if `is_coauthor:true`); self-merge is disallowed once v1 governance is in force
- Gate 14 becomes a hard requirement (≥20 external reviews, verified in `tier-update.yml`)
- Single-maintainer exception is removed; minimum two curators per release

---

## 10. Attribution & Credit Accounting

### Credit Types

1. **Curator credit** — a human submits an attestation (`collections/<slug>/v<N>/reviews/<doi>.yaml`)
2. **Reviewer credit** — a GitHub-verified human posts an approval comment on the attestation PR
3. **External-review credit** — an ASB `--peer-review` run flags a claim + evidence pair; imported via `import_external_reviews.py`
4. **Tier advancement** — curators with N qualifying reviews + M external-review + 0 COI conflicts advance to Reviewer/Lead-Curator tier (per `COI_POLICY.md`)

### Public Credit Surface

All credit is public and tracked in `contributors.jsonld`:

```jsonld
{
  "@id": "urn:asb:curator:orcid:0000-0000-0000-0000",
  "type": "Person",
  "name": "Jane Smith",
  "orcid": "0000-0000-0000-0000",
  "affiliation": "UC Davis",
  "total_reviews": 25,
  "self_authored_reviews": 5,
  "external_reviews": 20,
  "tier": "lead_curator",
  "last_review_date": "2026-06-14"
}
```

### Attribution in Artifacts

Every published skill or benchmark includes a `curators` block:

```yaml
curators:
  - orcid: "0000-0000-0000-0000"
    name: "Jane Smith"
    role: curator
  - orcid: "0000-0001-0000-0000"
    name: "John Doe"
    role: reviewer
```

---

## 11. Dispute Resolution & Amendment

### Dispute: Curator vs. External Review Disagreement

If a curator attestation (`curator.evidence_spans_accurate: true`) contradicts an external review (LLM judge flags a claim as `disputes`), the attestation PR is labeled `disputed`. Resolution steps:

1. Curator and external-review originator comment on the PR with evidence
2. A second verified curator (non-coauthor of the paper) posts a tie-break comment
3. The attestation status is updated: `disputed_resolution: "<curator-name> tie-break: curator claim upheld"` or `"...external review upheld"`
4. Status advances to `signed-off` and tier-update proceeds

### Amendment: Correcting a Published Release

If an error is discovered in a published artifact (Zenodo, HF, GitHub):

1. **Minor fix** (typo, broken link, metadata) — issue a `v<N>.1` patch release with corrected artifact
2. **Content error** (wrong parameter value, incorrect attribution) — issue a `v<N>.1` with corrected artifact + explanation in CHANGES.md
3. **Hard-gate violation** (PII, non-OA mixed in) — takedown (§8.4) + post-mortem + v<N+1> with preventive gate

---

## 12. Implementation Checklist

These items are required for v0 release:

- [ ] TODO: Confirm real ORCID for lead maintainer (replace `TODO-REAL-ORCID` above in header)
- [ ] TODO: Corpus paper lists locked (metabolomics, epigenomics, transcriptomics) with spot-check OA verification ≥10% per domain
- [ ] TODO: PII red-team fixture (`tests/fixtures/pii_dual_use_red_team.jsonl`) committed; gate test ≥95% recall passing
- [ ] TODO: `release_gate.py` wired with gates 1,2,5,6,8,10,12,15 hard-blocking (gate test coverage + PR comments)
- [ ] TODO: `.github/workflows/promote-collection.yml` deployed (staged→collections gating)
- [ ] TODO: `.github/workflows/verify-paper.yml` deployed (gate 15, access-tier enforcement)
- [ ] TODO: `asb` CLI integration (`asbb doctor`, `asbb registry verify`) tested end-to-end
- [ ] TODO: First collection (metabolomics) promoted to `collections/` and passes full CI
- [ ] TODO: `CHANGELOG.md` / release notes updated with this policy
- [ ] TODO: Contributor allowlist (author/affiliation emails) seeded in PII config
- [ ] TODO: Lead maintainer ORCID added to `MAINTAINERS.md`, `marketplace.json`, Zenodo depositor profile

---

## 13. Change Log & Override Log (v0)

### v0 Waiver Summary

| Gate | Status | Justification | Expires |
|---|---|---|---|
| 13 (independent co-reviewer) | **FORMALLY WAIVED** | Single-maintainer v0; self-merge permitted, no second reviewer required pre-tag | v1 (Q4 2026) |
| 14 (≥20 external reviews) | **FORMALLY WAIVED** | ≥20 external reviews is the v1 target, not enforced at v0; releases labeled "pre-peer-review" | v1 (Q4 2026) |

### Soft-Gate Overrides (None Recorded Yet)

(This section fills with overrides as they are approved; none for v0 release so far.)

---

## 14. Acknowledgments & Next Steps

This policy is inspired by:

- **Fair Use & Copyright:** UK Copyright Act §30, EU Copyright Directive Art. 5.3(d), US 17 U.S.C. §107
- **Data Governance:** FAIR principles (Wilkinson et al., 2016)
- **Open Access:** PLOS Community Standards, Wellcome Open Research license requirements
- **PII/DURC:** NIH/NSF DURC guidelines, Data Privacy Impact Assessment frameworks
- **Credit:** CRediT taxonomy (contributor roles)

**Next steps (v1):**

1. Recruit a second Lead Curator/Reviewer to enable gates 13 & 14
2. Document closed-access admission policy (`CLOSED_ACCESS_POLICY.md` addendum)
3. Publish `asb-schema` + `indicium-adapters` to make gates 1 & 9 hard-blocking
4. File w3id.org PRs to resolve persistent IRIs
5. Activate contamination gate (gate 12) with held-out split enforcement per `benchmark_tier.openness`

---

**Policy Authority:** Louis-Félix Nothias, Lead Maintainer
**Effective Date:** 2026-06-14 (v0 release)
**Last Reviewed:** 2026-06-14
**Next Review:** v1 release planning (Q3 2026)