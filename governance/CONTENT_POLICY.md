# Content Provenance & Transformation Policy

**Status:** v0 Final · **Date:** 2026-06-14 · **Authority:** Lead Maintainer (Louis-Félix Nothias, ORCID: 0000-0001-6711-6719)

**Sign-off:** This policy authorizes the v0 release and gates all content publication. Override authority and hard-gate enforcement rules are legally binding.

---

## 1. Overview

This policy establishes the legal and operational boundaries for ingesting, storing, transforming, and publishing scientific content through the ASB (AgenticScienceBuilder) factory and registry. It covers three tiers of content, the open-access-first commitment for v0, licensing, transformation bounds, content safety gates, and the takedown procedure.

**Core principle:** ASB transforms copyrighted source papers into independently-authored structured artifacts (benchmarks, skills, capsules) grounded in facts and methods (not copyrightable) and attributable to their sources via DOIs and fair use. All public releases are legally defensible on fair-use grounds and explicitly license-compliant.

> **Scientific gate:** this policy is the *legal* gate. The *scientific* gate —
> where source papers come from and what makes them eligible — is documented in
> [`SOURCES.md`](SOURCES.md). Both gates apply to every paper.

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

> **NOTE — software / dataset / tutorial DOIs (e.g. Zenodo).** A source's citable identifier need not be a journal paper DOI (see [`SOURCES.md` §3.1](SOURCES.md)). For a software/dataset/tutorial deposition, the OA tier is read from the **deposition license**: a CC-BY / CC-BY-SA / CC0 Zenodo release qualifies as `gold-oa`; a public git repository cloned at build qualifies as `repo-oa`. This is the *paper-access* axis only — what a consumer may do with the tool is the separate `license_tier` axis (§4 "Tool License Tier", §7.7).
>
> **`repo-oa` requires evidence, not a stamp.** The tier asserts a clone was possible, so an entry carrying it MUST have a non-empty `repo_url`. `access.verified_via` is a constant string, not evidence: it reads `git_clone_succeeded_at_build` even on entries with no `repo_url`. The promotion gate (`scripts/release_gate.py --strict`) FAILs any `repo-oa` entry with an empty `repo_url`; such an entry is set `status: needs-evidence` and excluded, never silently admitted.
>
> **`link-only` — a citable DOI and nothing more.** When a source has no public repository to clone — a paywalled book or chapter, a journal placeholder with no code-availability statement, an archived deposit not bound to its source — the honest tier is `link-only`. It asserts only that the DOI resolves and the work is citable: no clone happened, no reuse right is claimed, and `access.is_oa` is left `null` unless separately established. Because it claims no clone, a `link-only` entry MUST NOT carry `access.verified_via`; the release gate FAILs one that does, mirroring the evidence rule for `repo-oa`. Skills deriving *solely* from `link-only` entries are stamped `metadata.grounding_tier: link-only`, and a skill with neither a source nor a repository is stamped `ungrounded` — neither is presented alongside repository-grounded skills as if equivalent. **A declared repository is full provenance, not a fallback:** because grounding is repository-only, a skill for a tool with no method paper is grounded on its published code, and the provenance gate accepts a non-empty http(s) `metadata.repo_url` in place of a source DOI. A bare slug or non-URL value is not evidence.

> **Repository-only grounding.** Skills built from a `repo-oa` entry ground **only on the cloned repository** — code, README, in-repo docs — which is what the entry's licence covers. They never ground on the paper's text, whatever its licence. This holds uniformly for every entry, so a preprint that grants no text-reuse rights (e.g. a bioRxiv `cc_no` deposit) is still admissible on its repository basis, and no per-entry licence resolution can turn a grounding into a rights violation. `access.license` on a `repo-oa` entry therefore records the *tool's code* licence, not a right over the paper text.

> **NOTE — `preprint` is NOT an OA tier.** "Preprint" is a value on a **separate provenance axis** (the version/stage of the document: preprint vs. accepted-manuscript vs. version-of-record), recorded in `provenance.version` / `provenance.source`. It is NOT a member of the OA set above and MUST NOT be used as `access.type`. A bioRxiv/medRxiv/arXiv preprint is admitted because its access tier is open (`open-access` / `gold-oa` as applicable) AND its provenance is `preprint`; the two axes are recorded independently. Do not conflate the open-access axis with the provenance axis.

> **NOTE — software tools have their own tier family.** The enum above governs
> **papers**. A corpus entry that is a *software tool* is admitted on the openness
> of its **code repository**, not the paper's reuse license, via the
> `repo-oa` / `repo-permissive` / `repo-copyleft` tiers (`scripts/release_gate.py`
> `_REPO_OA_TIERS`, layered on top of promote.py's `_OA_TIERS`). See
> [OPEN_ACCESS_POLICY.md → *Software tools — repository-OA tier*](OPEN_ACCESS_POLICY.md)
> for the rationale and requirements.

### Non-OA Exclusion

Papers with the following status are **rejected at curation**:

- Closed/paywalled (Elsevier, Springer, Wiley, etc. without OA marking)
- Hybrid (tagged as hybrid OA but underlying license is restrictive)
- Unknown (access status unresolved)
- Green OA with restrictive manuscript license (author-accepted manuscript under All Rights Reserved)

### Verification Procedure

1. **Automated check:** OpenAlex API lookup; flag `is_oa: true|false`
2. **Manual spot-check:** Sample papers in the final corpus (≥10% per domain) to confirm OA license accuracy
3. **Red-flag gate:** CI verify-paper.yml (stage §7.5) enforces `access.type ∈ {open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond} ∪ {repo-oa, repo-permissive, repo-copyleft} ∪ {link-only}` (after hyphen/underscore + `green`→`green-oa` normalization) for all `status:included` papers; unknown/non-OA triggers a hard fail. `preprint` is rejected as an `access.type` value because it is a provenance value, not an OA tier. The three `repo-*` values are the repository-access tiers from the software/dataset note above, and `link-only` is the no-repository tier; `tests/test_oa_tier_parity.py` keeps these sets identical to `scripts/release_gate.py:_REPO_OA_TIERS` and `_LINK_ONLY_TIERS`, so the push gate and the release gate cannot drift apart.

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

### Tool License Tier (consumer-use axis)

**Locked decision (2026-06-24).** Separately from the *paper* open-access axis
(§3) and the *workflow*-openness axis (§7.6), every source/tool carries a
**`license_tier`** describing what a **consumer** may do with the underlying tool.
This is a distinct, third axis — see §7.7. Canonical SPDX→tier map and fallback
rule: [`LICENSE_TIERS.md`](LICENSE_TIERS.md).

- **`open`** — commercial use permitted (MIT, Apache-2.0, BSD, MPL-2.0, CC-BY/CC0,
  and copyleft GPL/AGPL/LGPL). Copyleft is `open` here: it governs derivative
  *distribution*, not whether a consumer may use the tool commercially.
- **`noncommercial`** — academic/noncommercial use only (CC-BY-NC*,
  PolyForm-Noncommercial, and similar).
- **`restricted`** — no grant / proprietary / no license (all-rights-reserved or a
  non-OSI custom license that is not clearly noncommercial). Unknown → `restricted`.

Three binding rules attach to non-open tiers:

1. **Link-only grounding.** For `noncommercial` and `restricted` tiers a shipped
   grounding bundle MUST reference the source (DOI / repo URL + citation) and MUST
   NOT embed its code or text. Embedding non-open source into a publicly
   distributed bundle would exceed the redistribution/relicensing the tool's
   license grants. Assembling a *private, local* bundle is the consumer's own
   responsibility. (Enforced in the grounding binder; CI enforcement is Phase 2.)
2. **Runtime use acknowledgment (`noncommercial` only).** A skill grounded on a
   `noncommercial` tool sets `requires_ack: true` and surfaces the tier + license
   to the user, who must confirm a permitted (e.g. noncommercial) use **before**
   the skill is applied. The `asb-metabolomics` meta-skill enforces this blocking
   gate. Commercial use is forbidden without a separate license.
3. **Non-blocking soft note (`restricted` only).** A skill grounded on a
   `restricted` tool (no LICENSE file, all-rights-reserved, or non-OSI custom
   license that is not clearly noncommercial) does **not** set `requires_ack: true`
   and does NOT trigger a blocking interrupt. Instead the skill surfaces a soft
   note: "no clear license detected — verify before commercial use or
   redistribution." Absence of a license is an unknown, not an explicit
   prohibition; the consumer bears responsibility for verifying permitted use.

`license_tier` does **not** relicense the skill prose, which remains the
collection's own work (CC-BY-4.0, per "Code & Synthesis Layer" above). A
`noncommercial` tool may therefore be described by an openly-licensed skill — the
restriction lands on the consumer's *use of the tool*, surfaced via the
acknowledgment gate, not on our description of it.

---

## 5. Release Gate: Transformation & Attribution

The release gate is the checkpoint between private Tier 2 and public Tier 3. Every artifact must pass before publication to Zenodo, HF, or the public GitHub `collections/` directory.

### Gate Procedure

**Entry:** Capsule paths + corpus metadata, run on local ASB checkout
**Exit:** `gate_report.json` (PASS|WARN|FAIL) + artifacts for promotion to `staged-collections/`
**Enforcement:** Advisory on PRs to `staged-collections/`; **hard-blocking** on promotion to `collections/` and on the release tag

### Gate Checklist (15 gates)

At v0, `release_gate.py` hard-blocks on gates **2, 5, 6, 8, 10, 15** — the
`hard_gate_ids` field of every gate report, and the authority when this table and the
code disagree. Gates **1, 3, 4, 7, 9, 11** are warn-only. Gates **13** and **14** are
formally waived for v0 (§9), and so, as of 2026-09-13, is gate **12** — it is declared
hard-blocking in the row below but has **no implementation**: no contamination check
exists, and no collection file declares `benchmark_tier` or `openness`. The row states a
v1 intention, not a v0 check (§9).

| # | Gate | Owner | Criterion | Trigger | v0 Enforcement |
|---|---|---|---|---|---|
| **1** | **asb-schema published** | A+H | LinkML `asb-schema` repo public + registered | gate check: lookup on GitHub | warn-only (schema not published yet) |
| **2** | **Paper access tier resolved** | A | Every `status:included` paper has `access.type` in the OA set `{open-access, open_access, oa, gold-oa, gold_oa, green-oa, green, diamond}` (post-normalization) | CI verify-paper.yml | hard-block non-OA / unknown |
| **3** | **Indicium schema version pinned** | A | Collection YAML lists `schema_versions.indicium: <real-tag>` from indicium repo | gate check: git tag exists | warn-only (gate 3 not activated v0). **Unachievable as written:** the indicium repository has zero tags and no collection declares `schema_versions`. At v1 the pin is a commit SHA — §7.4 |
| **4** | **Profile reproducibility** | A | Generation manifest includes `profile_hash`, `llm`, `seed` enabling exact rebuild | manifest validation | warn-only (gate 4 not activated v0) |
| **5** | **Verbatim quotation caps** | A | Sum of `evidence_span` lengths across all skills/claims ≤ corpus-size-dependent cap (§5.3) | gate check: char count | hard-block (fail if exceeded) |
| **6** | **Similarity check (verbatim vs original)** | A | N-gram overlap + embedding cosine for each `evidence_span` vs Tier-1 source ≤ threshold (§5.4) | gate check: `check_strip_verbatim_similarity` | **caps half: hard-block, live.** **Similarity half: inert** — it compares each span to the skill's own body, not the Tier-1 source, and cannot reach either threshold; 0 FAIL / 0 WARN over 47,241 spans. Measured 2026-09-13, §5.3a |
| **7** | **Claim fidelity (indicium round-trip)** | A | Every skill claim resolves in `benchmark/claims/` ground truth; `trace_status: exact_match` | gate check: indicium `verify-claims` | warn-only (gate 7 not activated v0) |
| **8** | **DOI & license resolution** | A | Every artifact lists source DOI(s) + license SPDX tag; Zenodo lookup succeeds or entry is public preprint | gate check: CrossRef/Zenodo API | hard-block (fail if DOI invalid) |
| **9** | **Indicium adapters published** | A | All four indicium adapters (sepio, sssom, prov, claims) are publicly available + versioned | gate check: lookup on PyPI/GitHub | warn-only (adapters not published yet) |
| **10** | **Registry consistency** | A | `marketplace.json` ↔ `catalogue.jsonld` ↔ filesystem reconciliation passes; no duplicates, IRI conflicts, or missing files | release_gate.py `check_catalogue_membership` + `check_layout` + `check_unit_closure` (**not** `asbb registry verify`: that verb never existed, and `asbb registry` itself was removed on 2026-09-14 — §7.1 and `docs/REGISTRY.md` §4.1) | hard-block (fail if drift) |
| **11** | **Leaderboard schema valid** | A | `benchmark/leaderboard.jsonld` validates against JSONLD context; CiTO link types recognized | gate check: JSONLD parser + CiTO vocab | warn-only (gate 11 not activated v0) |
| **12** | **Contamination / held-out audit** | A | For open-tier releases: no held-out test splits mixed into public outputs; for closed-tier: held-out marker present (v1+ only; v0 open-only) | (v1) gate check: output file audit | **FORMALLY WAIVED for v0** — no contamination check is implemented and no held-out split is declared; v0 is open-tier only, so the criterion's closed-tier half does not apply (waiver logged in §9 + release notes) |
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

**Tool:** ~~`src/agentic_science_builder/release/similarity_check.py` (integrated into
`release_gate.py`).~~ **That file does not exist**, in this repository or in the
framework. The check is `check_strip_verbatim_similarity` in `scripts/release_gate.py`.

### 5.3a What the shipped check actually does (measured 2026-09-13)

The section above describes an intended gate. Three things differ in the code, and the
third means the similarity half of gate 6 **has never fired and cannot fire**.

1. **No embedding cosine.** `_similarity_ratio` is
   `difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()` — a character-level
   edit-similarity proxy, not `text-embedding-3-small`. The code says so itself
   (`release_gate.py:306-310`: *"NOT a semantic embedding cosine"*). No embedding model
   is called anywhere in the gate, and no API key is required to run it.
2. **The comparand is not the source paragraph.** Both the Jaccard and the ratio compare
   each span against **the skill's own `SKILL.md` body**, because the Tier-1 source
   paragraph is not available at gate time — the gate's own comment
   (`release_gate.py:637-643`) records this.
3. **The arithmetic cannot reach either threshold.** A span is compared to a document
   one to two orders of magnitude longer, so `SequenceMatcher`'s `2M/(L+N)` is bounded
   near `2L/(L+N)`: even a *perfect copy* of body text scores 0.043–0.059, and
   `difflib`'s `autojunk` heuristic (active for bodies ≥200 characters) drops it to
   0.005–0.018. Measured over all 35,670 spans ≥60 characters in
   `collections/metabolomics/v2`: ratio median 0.0074, max **0.3042**; Jaccard median
   0.0208, max **0.0702**. The FAIL condition needs Jaccard >0.30 **and** ratio ≥0.92;
   the WARN condition needs either. Neither is reachable. Across all four collections —
   7,715 skills, 47,241 spans — the similarity half has produced **0 FAIL and 0 WARN**,
   and that is a property of the arithmetic, not of the corpus.

**Gate 5 is unaffected and is live.** The per-span (150 char) and cumulative (1500 char)
caps in the same check are enforced and do fail. Only the similarity half is inert.

**Why it was not "fixed" for v0.** The obvious repair — compare the span against the
best-matching body window of the span's own length instead of the whole body — was
implemented and measured on 2026-09-13 over the full released collection. It is
arithmetically correct and it is unusable: it produces **28,510 FAIL + 382 WARN** on
`metabolomics/v2` (99.6% of skills red; 37,747 findings across all four collections)
with a **0% true-positive rate**. Every finding was classified, not sampled: 28,289 of
them match on the very `- [sec] paraphrase: "quote"` line the span was *extracted
from*, because `_collect_evidence_spans` reads spans out of the body's own Evidence
bullets — 79.3% of spans are literal substrings of their own body by construction, so
the best-matching window is the extraction site and scores exactly 1.000. The rest are
the frontmatter span's own rendered Evidence block, attributed quotations, code inside
fenced examples, and sentences of the skill's own generated prose. A real
`--strict` run with only the window swapped was verified to exit 1 and set
`release_verified: false` on `transcriptomics/v1` and `metabolomics/v2`.

**Decision (2026-09-13): do not rescale the window; do not ship the repair.** The
defect is *what* is compared, not *how far*. Rescaling does not supply the Tier-1
source paragraph; it only makes the self-comparison succeed. Closing this properly at
v1 requires either fetching the source paragraph at gate time, or — at minimum —
excluding the span's own extraction site, the Evidence block, fenced code and
attributed quotations from the window set before any rescale. Until then this section
stands as the honest record: **gate 6's similarity half is inert, and the release does
not rely on it.** Gate 6's other half, the PII/dual-use scan (§6), is live and passing.

### 5.3b Known limits of the span scan (measured 2026-09-13)

Two coverage facts, recorded so that "the gate scanned every quoted span" is not read
into §5.3 or §6.

- **Evidence lines whose label contains a colon are never scanned.**
  `_EVIDENCE_VERBATIM_RE` is `^(\s*-\s+\[[^\]]*\][^:]*?):\s*"[^"]*"\s*$` — the
  `[^:]*?` forbids a colon before the separating one, so a bullet such as
  `- [other] Workflow step: aggregate peak counts…: "…"` is not recognised as evidence.
  **2,324 verbatim-shaped lines across 1,664 of the 5,861 skill files** are invisible to
  both the PII scan and the verbatim caps. Running the full Tier-1 and Tier-2 pattern
  set plus the email regex over all 2,324 of them yields **zero findings of any
  severity**, and none exceeds the 1500-char cumulative cap on its own (largest
  per-file unscanned total: 910 characters), so nothing about the v0 verdict changes.
  The regex is left alone for v0: it is shared with `promote.py`, and widening it moves
  `policy.config_sha256` (it is recorded there as `verbatim_pattern`) for no measured
  benefit.
- **Composite-workflow `SKILL.md` files are excluded, vacuously.** `layout.iter_skill_md`
  always skips `workflows/`, so the 22 workflow skill files are scanned by neither the
  PII check nor the provenance check. They carry **0 evidence spans between them**, so
  including them would add nothing to scan. The real gap there is that their
  `license:` field is declared and never verified — tracked separately, not a span
  issue.

**One latent hazard, recorded with its margin.** The Tier-1 hard-fail pattern
`nhs_number` matches any bare 10-digit run, and a DOI suffix is a bare digit run: it
matches `1608041113` inside `10.1073/pnas.1608041113`. 34 evidence spans in the
released collection quote a DOI; the longest digit run in any of them is **8**. The
release therefore clears a hard gate by two digits, and a future span quoting a
10-digit DOI suffix would hard-block a release on a false positive. Fix at v1 by
excluding a digit run preceded by `10.\d{4,9}/\S*` before applying `nhs_number`.

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
- Regex scan of verbatim quote spans against a versioned PII pattern library (config: `scripts/pii_config.py`, the `PII_CONFIG` dict — see §6.2)
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

PII patterns, dual-use keywords and author allowlist are versioned in a committed
config file: `scripts/pii_config.py` (the `PII_CONFIG` dict, currently
`version: 2026-09-13.1`, 14 hard-fail/advisory patterns). It is mirrored byte-for-byte
into the released collection at `collections/<slug>/v<N>/scripts/pii_config.py`, and
`tests/test_pack_closure.py` fails if the two copies drift.

Every release records which version ran, and the record is tamper-evident.
`release_gate.py` writes ~~`policy.pii.version`~~ **`policy.pii_config_version`** into
`gate_report.json` and folds the whole `PII_CONFIG` dict into `policy.config_sha256`,
which in turn enters `receipt_sha256`. A reviewer asking *which patterns gated this
release* reads those two fields — ~~`policy.pii`~~, **which the report does not
carry**: schema `asbb-release-gate/1.1` emits the version string and the digest, not
the pattern bodies — and re-checks them with `release_gate.py <collection> --verify`.
The pattern set cannot be swapped after the fact without breaking the receipt, but
recovering *what the patterns were* needs the committed `pii_config.py` at that
version, not the report alone. (Corrected 2026-09-13; the `policy.pii` key was
described from an earlier schema.) Note also that `policy.implementation_sha256`
hashes `release_gate.py`, `release_receipt.py` and `layout.py` — **not**
`pii_config.py`, whose integrity rides on `config_sha256` alone.

**Version history.** `2026-09-13.1` tightened `placeholder_subject` to
`(?-i:[A-Z])` for its label letter. The gate compiles every pattern with
`IGNORECASE`, so the bare `[A-Z]` also matched lowercase and the trailing *s* of an
ordinary plural satisfied it: the rule fired on the phrase "weighting by number of
participants" in three skills, quoted verbatim from a CC-BY paper. That is the same
defect `named_patient_dx` was already fixed for. All the enumerated-individual cases
the rule exists for (`Subject 12`, `Patient_A`, `Subject_123`, `Participant B`,
including §6.1's own fixture) still match; the three false positives no longer do,
and `pii_dual_use` is PASS with zero findings across all four collections.

---

## 7. Enforcement Points & Gate Workflow

### 7.1 Advisory Gate: Pull Requests to `staged-collections/`

**Trigger:** Any PR that adds or modifies files in `staged-collections/`.

**Workflow (corrected 2026-09-13).** ~~`.github/workflows/validate.yml` runs
`asbb registry verify` (gates 1,2,5,6,8,10) and `release_gate.py --advisory`
(gates 3,4,7,11-14 suppress hard-blocks; all output as PR comments).~~
Neither command runs in that workflow. What `validate.yml` actually runs, on every
PR to `main` and every push to `main` — not on a `staged-collections/` path filter —
is: the test suite; `scripts.skill_index`; `marketplace.json` validation;
`scripts.lint_skill_descriptions`; a sampled `derived_from` DOI resolution; EDAM IRI
resolution; RO-Crate validation (inert — no collection ships an
`ro-crate-metadata.json`, so the step validates zero files, emits a `::warning::` and
never blocks, while every `collection.yaml` declares `ro_crate_path`); the indicium
round-trip (inert — the CLI is not on PyPI, so it emits a `::warning::` and never
blocks); LinkML schema validation; the pack-derivation gate
(`scripts.build_packs --check`); the advertised-count gate
(`scripts.check_advertised_counts`); and the license-tier, provenance-tier and
tool-catalogue gates — the first two over `collections/metabolomics/v2` and every
pack, the third over the collection.

Three separate errors are corrected here.

1. **`asbb registry verify` is not a command — and since 2026-09-14 neither is
   `asbb registry`.** Until then `asbb registry` accepted only `list` and `validate`
   (`verify` was an `invalid choice`), and both were Phase-1.7 stubs that printed a
   placeholder and — since 2026-09-13 — exited 1 rather than 0, so that a caller could
   not read "consistent" out of a command that looked at nothing. Fixing the verb
   would not have enforced anything either. On 2026-09-14 the owner removed the
   advertised surface rather than leave a documented command that answers nothing:
   `asbb registry <anything>` is now an argparse `invalid choice` on the top-level
   parser and exits 2. `docs/REGISTRY.md` §4.1 records what the two subcommands
   claimed and which script does each job.
2. **`release_gate.py` is not wired into this workflow at all** — in advisory mode or
   any other. The gate runs at promotion (§7.2) and at release, never on a
   `staged-collections/` PR.
3. **The gate numbers in that list are not this document's gate numbers.** They are
   `validate.yml`'s own header numbering, which follows Release Design Doc v2 §14.
   The two schemes collide rather than agree: in that header gate 6 is *EDAM IRI
   resolution* and gate 10 is *plugin manifest validation*, where §5 above numbers
   gate 6 the *similarity check* and gate 10 *registry consistency*. Read any gate
   number in a workflow file against that workflow's own header, never against §5.

**What actually reconciles the registry** is the release gate, not a registry
subcommand: `check_catalogue_membership` (each `collection.yaml`'s advertised members
against `catalogue.jsonld` and the files on disk), `check_layout` (each skill
directory's permitted file set and byte budget, and `skills_index.json` against the
leaf directories), and `check_unit_closure` (each pack index against its leaves, and
every declared helper against its declaring unit). All three run only where
`release_gate.py` runs.

**Result:** there is no advisory PR comment today, because no advisory run is wired.
Merge is **NOT blocked** by a release-gate finding for the trivial reason that the
release gate is not consulted. Curator review of a staged PR is unassisted.

**Wiring it is drafted and held for v1.** A `--advisory` run over a workflows-only
tree such as `staged-collections/metabolomics` exits 1 today: five collection-scoped
checks (`access_tier_oa`, `strip_verbatim_similarity`, `pii_dual_use`,
`provenance_doi_license`, `gate_input_files`) have no subject in a tree with no
`collection.yaml`, no `corpus.yaml` and no leaf skills, and `CheckResult.finish()`
cannot distinguish *the subject is missing* from *there is no subject of this kind
here* — both give `checked == 0` and report `uncheckable`, and
`blocking_fail = overall == UNCHECKABLE` is deliberately unconditioned on `--strict`
(pinned by `tests/test_release_gate_receipt.py::test_advisory_empty_target_also_blocks`).
So the exit code is correct and the classification is the gap. A patch adding a
`not_applicable` verdict for workflows-only targets, plus the `validate.yml` steps to
post one PR comment, was drafted and measured on 2026-09-13: it matches exactly one
directory in the repository, leaves all four shipped collections byte-identical in
their gate summaries (only `policy.implementation_sha256` moves, because the gate
file itself is hashed), and keeps the suite at 1618 passed / 3 skipped. It is held
out of the v0 release train because it changes the gate for no v0 benefit; it lands
with the v1 wiring.

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
- Full `release_gate.py --strict` (hard-block on gates 2,5,6,8,10,15 — see the §5 checklist)
- Zenodo deposition + DOI mint
- HF mirror trigger (`mirror-to-hf.yml`)
- Catalogue regeneration + w3id IRI assertion

**Result:** If any hard gate fails, the action aborts; tag is not pushed; Zenodo deposition is reverted (fail-soft).

### 7.4 DOI Topology (locked decision, 2026-06-14)

**Exactly ONE Zenodo concept-DOI per collection-release.** Each tagged collection-release (`<slug>-v<N>`) is a single versioned Zenodo deposition under one concept-DOI; all versions of a collection live under that one concept.

The following ride as **FILES inside that single deposition** — they do NOT receive separate DOIs:

- the **KB snapshot** (the pinned grounding knowledge base for the collection) — this ships as
  `kb_bundle.json` inside the collection directory, and therefore inside the zip. It is a DOI-list
  binder manifest rather than an archive of the grounding KB itself; it pins *which* KB, not its
  contents.

**indicium has its own, separate concept-DOI** (minted from the indicium repository's own releases). Do not create per-file or per-export DOIs (no DOI matrix explosion).

**Struck 2026-09-13: the `indicium_version.txt` pin file and the `asb_ontology.ttl` snapshot.**
Both were listed here from the start, neither ever existed, and `release.yml`'s Zenodo step has no
stage that would attach them. They are struck rather than built, because **the deposition contains
nothing that conforms to that ontology.** A v0 collection is 5,917 Markdown files, 934 YAML, 8 JSON
and a `CITATION.cff`: **zero JSON-LD documents, zero claim records, zero indicium exports.** The
`asb:` term base that `asb_spine.ttl` declares (`https://w3id.org/asb#`) appears nowhere in a shipped
collection. Depositing an ontology beside artefacts that do not use it would assert a conformance
that does not exist — the same failure this policy's other corrected claims produced, in the one
place where a reader is most entitled to trust the record.

**What the deposition actually needs pinned, and already has.** The IRI space a v0 collection uses is
`https://w3id.org/holobiomicslab/asb-skill/`, bound as the `asb:` prefix at `collection.yaml:3` and
stamped into the `@id` of every skill — 5,884 occurrences in `metabolomics/v2` alone. Its JSON-LD
context is the repository's `catalogue.jsonld`, which pins `schema.org` as `@vocab` plus the EDAM and
XSD prefixes. Both ship. No third file is required.

> **Open, and it is a registration, not a decision.** Neither `https://w3id.org/holobiomicslab/asb-skill/`
> nor `https://w3id.org/asb` resolves — both return 404 (checked 2026-09-13). A w3id IRI is designed to
> be minted before it redirects, so this does not block a tag and the identifiers stay stable, but every
> `@id` in the deposited collection is a dead link until the redirect config is submitted to the w3id.org
> repository. Tracked as the `w3id-registration` register item.
>
> **Corrected 2026-09-14.** This line used to end "the PR text is already drafted". What was
> drafted (`W3ID_REDIRECT_PRS.md` in the hub) registers `/asb` and `/indicium`, which appear in
> **0** files of the published tree -- their contexts are in the staged, unpublished
> `metabolomics/v1`. The namespace this release binds, `holobiomicslab/asb-skill`, had no draft
> until `W3ID_HOLOBIOMICSLAB_PR.md`, which also records two corrections that apply to all three:
> `perma-id/w3id.org` now takes `ids/<name>/`, not a root-level directory, and the two older
> drafts remain blocked on `HolobiomicsLab/indicium` being public (still private, all four of
> their targets 404 on 2026-09-14). The `/holobiomicslab` targets all return 200.

**If v1 ships claim records**, the ontology pin becomes real and belongs here — at that point snapshot the
generated Turtle from the framework (`docs/ontology/asb_spine.ttl`), not a hand-copy in this repo. The
indicium pin should then be a **commit SHA, not a tag**: the indicium repository has zero tags, and its
two version strings disagree (`pyproject.toml` says 2.0.0, the installed distribution reports 1.12.0), so
"the tag" as `RELEASE_TRAIN_v0.md:309` asks for is unproducible today.

### 7.5 Install Surface vs. asbb CLI (Phase 1.7)

The **install surface** is the Claude Code plugin marketplace, NOT the `asbb` CLI:

```
/plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections
```

resolved via `.claude-plugin/marketplace.json` (note: the manifest lives at `.claude-plugin/marketplace.json`, not at the repo root). The `asbb` CLI is **to-build (Phase 1.7)** and covers **verify / doctor ONLY** — it is NOT the install path.

> **Corrected 2026-09-14.** This paragraph used to read "**registry / verify / doctor ONLY**". `registry` was the third Phase-1.7 stub: advertised in `asbb --help` and documented with two subcommands, doing neither. It was removed on 2026-09-14 — see `docs/REGISTRY.md` §4.1, which names the script that performs each job it claimed. (The "NOT the install path" half of the sentence is separately superseded by the shipped, tested `asbb install` / `asbb uninstall` for non-Claude runtimes; that correction is held in `docs/REGISTRY.md` §4 pending the owner's restatement of the locked caveat, and is not touched here.)

### 7.6 Two Independent Axes: OA-access vs. Workflow-openness

The OA-access axis and the workflow-openness axis are **separate and independent**:

- **`require_open_access`** — the paper-access axis (is the *source paper* open access?). Gates 2 / 15 enforce this against the OA set in §3. Always `true` for v0.
- **`benchmark_tier.openness`** (`open` | `mixed` | `closed`) — the *workflow*-openness axis (are the benchmark's held-out splits/workflow open?). Used by the contamination gate (12), NOT by the access gates.

A collection can be OA-only (`require_open_access: true`) while its `benchmark_tier.openness` is independently `open`, `mixed`, or `closed`. Never collapse these two axes into one field.

### 7.7 Tool License Tier — a third, independent axis

Beyond the two axes in §7.6, a **third** independent axis records what a consumer may do with the *tool* a skill grounds on:

- **`license_tier`** (`open` | `noncommercial` | `restricted`) — the tool/source consumer-use axis (defined in §4 "Tool License Tier"; map in [`LICENSE_TIERS.md`](LICENSE_TIERS.md)).

It is orthogonal to both `require_open_access` (is the *source* open access?) and `benchmark_tier.openness` (is the *workflow* open?). A source can be OA (`access.type: gold-oa`) yet `license_tier: noncommercial` — e.g. an open-access paper or CC-BY Zenodo deposition describing a noncommercially-licensed tool — or the reverse. Never collapse these axes: **OA-access** governs *our* right to redistribute the source; **`license_tier`** governs the *consumer's* right to use the tool.

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

## 9. Governance: Gates 12, 13 & 14 (v0 Waiver)

The full spec (§9 Community/Public Expert Review, SPEC.md §9.7.6) defines gates 13 and 14;
gate 12 is defined in §5's checklist:

- **Gate 12:** Contamination / held-out audit (no held-out split mixed into public outputs)
- **Gate 13:** Independent co-reviewer present when `is_coauthor: true` on any attestation
- **Gate 14:** ≥20 external reviews (Lead-Curator non-self minimum)

### Gates 13 & 14 — v0 Waiver Justification (LOCKED 2026-06-14)

**Context:** ASB v0 is a single-maintainer, single-lead-curator release. Gates 13 & 14 are designed for a mature multi-curator governance model with multiple independent reviewers. Enforcing them at launch would be a structural impossibility.

**v0 Exception (BOTH gates FORMALLY WAIVED):**  
*(Gate 12 is waived separately, under its own justification below, LOCKED 2026-09-13.)*

1. **Gate 13 (independent co-reviewer) — FORMALLY WAIVED for v0**
   - v0 permits self-review of papers where the reviewer is a co-author (with full disclosure in attestation)
   - A second/independent co-reviewer is NOT required at v0
   - **Self-merge is PERMITTED** for v0: the Lead Maintainer may self-merge PRs they authored, with the waiver logged in the release. There is NO "no self-merge" invariant at v0 — any such invariant is superseded for v0.
   - Lead Curator signs off on all attestations (single authority)

2. **Gate 14 (≥20 external reviews) — FORMALLY WAIVED for v0**
   - ≥20 external reviews is the **v1 target**, NOT enforced at v0
   - v0 sets no minimum external-review count; the gate is waived rather than lowered
   - v0 releases are labeled "pre-peer-review" / "community-review-eligible" in release notes

### Gate 12 Waiver Justification (LOCKED 2026-09-13)

**Context:** gate 12 asks whether a held-out evaluation split leaked into public output. That
question is not answerable for v0, because **no split was ever declared**: `benchmark_tier` and
`openness` occur zero times in any collection file, there is no `benchmark/` directory, and no
contamination logic exists in `scripts/` or in the package. The gate's own criterion scopes its
closed-tier half to "v1+ only; v0 open-only", and v0 is open-tier throughout. Building the check
is not the work — declaring the split it would audit is, and that belongs with the benchmark, not
with this release.

**Gate 12 (contamination / held-out audit) — FORMALLY WAIVED for v0**

   - v0 ships open-tier only; there is no closed-tier release for the held-out marker to protect
   - No held-out split is declared in any v0 collection, so there is nothing a contamination audit
     could compare against
   - `release_gate.py`'s `hard_gate_ids` is `(2, 5, 6, 8, 10, 15)` and does **not** include 12;
     this waiver makes the document agree with the code rather than the reverse
   - **Do not wire this gate to `--exclude-doi`.**
     `collect_metabolomics_collection.py:715-746` contains the phrase "held out of release"; that is
     a **licence** exclusion, it leaves no marker in the shipped artefact, and it is not an
     evaluation split

**Waiver logging:** All three waivers are logged here (§9 + §13 waiver summary) and MUST also be recorded in the release notes / CHANGELOG of each v0 collection release.

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

- Gate 12 becomes enforceable **only once a held-out split exists to audit**: the prerequisite is a
  declared benchmark split plus `benchmark_tier.openness` in the collection schema, populated. The
  audit itself is the small part
- Gate 13 becomes a hard requirement (independent co-reviewer if `is_coauthor:true`); self-merge is disallowed once v1 governance is in force
- Gate 14 becomes a hard requirement (≥20 external reviews, verified in `tier-update.yml`)
- Single-maintainer exception is removed; minimum two curators per release

---

## 10. Attribution & Credit Accounting

### Credit Types

1. **Curator credit** — a human submits an attestation (`collections/<slug>/v<N>/reviews/<doi>.yaml`)
2. **Reviewer credit** — a GitHub-verified human posts an approval comment on the attestation PR
3. **External-review credit** — an ASB `--peer-review` run flags a claim + evidence pair. **(v1; see the gate 14 waiver in §9.)** The producing half ships — `peer_review.py` writes `peer_reviews.json` with `"source": "peer_review"`, and `claim_ledger.py` declares `peer_review` a valid `EvaluationSource` — but **no importer exists**: `import_external_reviews.py` is named here and nowhere else, in any repository. Nothing is blocked by its absence at v0, because its only consumer is gate 14, which is formally waived, and `contributors.jsonld` holds zero records, so there is no one to credit
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

- [ ] TODO: Confirm real ORCID for lead maintainer (replace `0000-0001-6711-6719` above in header)
- [ ] TODO: Corpus paper lists locked (metabolomics, epigenomics, transcriptomics) with spot-check OA verification ≥10% per domain
- [ ] TODO: PII red-team fixture (`tests/fixtures/pii_dual_use_red_team.jsonl`) committed; gate test ≥95% recall passing
- [ ] TODO: `release_gate.py` wired with gates 1,2,5,6,8,10,12,15 hard-blocking (gate test coverage + PR comments)
- [ ] TODO: `.github/workflows/promote-collection.yml` deployed (staged→collections gating)
- [ ] TODO: `.github/workflows/verify-paper.yml` deployed (gate 15, access-tier enforcement)
- [ ] TODO: `asb` CLI integration (`asbb doctor`, `asbb verify`) tested end-to-end. ~~`asbb registry verify`~~ — that verb never existed and `asbb registry` was removed on 2026-09-14 (`docs/REGISTRY.md` §4.1); registry consistency is gate 10 above, carried by `release_gate.py`, not by the CLI
- [ ] TODO: First collection (metabolomics) promoted to `collections/` and passes full CI
- [ ] TODO: `CHANGELOG.md` / release notes updated with this policy
- [ ] TODO: Contributor allowlist (author/affiliation emails) seeded in PII config
- [ ] TODO: Lead maintainer ORCID added to `MAINTAINERS.md`, `marketplace.json`, Zenodo depositor profile

---

## 13. Change Log & Override Log (v0)

### v0 Waiver Summary

| Gate | Status | Justification | Expires |
|---|---|---|---|
| 12 (contamination / held-out audit) | **FORMALLY WAIVED** | No held-out split is declared anywhere in v0 and no contamination logic exists; v0 is open-tier only, so the criterion's closed-tier half does not apply. Waived 2026-09-13 | v1, and only once a split exists to audit |
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