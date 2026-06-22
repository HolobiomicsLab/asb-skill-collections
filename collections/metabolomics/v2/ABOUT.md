# About this collection — content & selection

**ASB Metabolomics Skill Collection v2** (`metabolomics-v0.1.0`) — 5,865
evidence-grounded skills across 909 software-tool records, distilled from 568
peer-reviewed method papers by the [AgenticScienceBuilder](https://github.com/HolobiomicsLab/AgenticScienceBuilder)
(ASB) pipeline. This page describes **what is in the collection** and **how it
was selected**. For the exact build command and models, see
[PROVENANCE.md](PROVENANCE.md); for usage, [USAGE.md](USAGE.md).

---

## What is in it

### Scope & analytical techniques

The collection covers **computational metabolomics**, predominantly LC-MS/MS but
spanning several analytical platforms. Each skill/tool is tagged with a
`techniques` facet (see [USAGE.md §2](USAGE.md)):

| Technique | Skills | Tools |
|---|---|---|
| LC-MS | 1,314 | 474 |
| tandem-MS (MS/MS) | 2,129 | 586 |
| GC-MS | 367 | 205 |
| CE-MS | 114 | 180 |
| direct-infusion-MS | 97 | 101 |
| MS-imaging | 292 | 157 |
| ion-mobility-MS | 390 | 241 |
| NMR | 276 | 192 |
| mass-spectrometry (generic) | 804 | 374 |

(Skills/tools may carry several tags; ~1,520 skills are technique-agnostic —
statistics, format conversion, general workflow.)

### Main EDAM topics

Skills and tools are annotated with [EDAM](https://edamontology.org) ontology
IRIs for retrieval. The most frequent **topics** across the collection:

| EDAM topic | Skills |
|---|---|
| Metabolomics | 1,838 |
| Proteomics experiment* | 2,583 |
| Proteomics* | 1,783 |
| Bioinformatics | 1,771 |
| Small molecules | 423 |
| Analytical chemistry | 347 |
| Endocrinology and metabolism | 308 |
| Molecular interactions, pathways and networks | 304 |
| Drug metabolism | 226 |
| Lipids | 120 |
| NMR | 97 |

\* EDAM's "Proteomics experiment"/"Proteomics" topics are commonly applied to
mass-spectrometry methodology in general; their high count reflects shared
MS-experiment tooling, not proteomics scope.

Most frequent **operations**: Filtering, Isotopic-distribution calculation,
Standardisation/normalisation, Deisotoping, Conversion, Clustering, Network
analysis, Peak detection, Quantification, Image analysis.

---

## How it was selected

### Sources (discovery)

Candidate tools/papers were gathered from complementary spines:

1. **Computational-metabolomics review tool lists** — an adoption-first pool of
   ~750 tools curated from recent community reviews.
2. **Author harvests** — works by leading method authors (van der Hooft,
   Dorrestein, Böcker, Zamboni, Wishart, Coley, Bittremieux), via OpenAlex +
   Unpaywall, with repositories verified through the GitHub API.
3. **Citation graph** — papers citing foundational tools (GNPS / molecular
   networking, matchms, XCMS).
4. **Review-series reference mining** — the Misra computational-metabolomics
   review series; reference lists mined via OpenAlex / Crossref where the PDFs
   were paywalled.
5. **The earlier metabolomics-100 corpus** — which contributes the broader-modality
   tools (GC-MS, NMR, MS-imaging, multi-omics).

### Inclusion criteria

A candidate was built into the collection when it had **all** of:

- a **computational metabolomics / mass-spectrometry method** (predominantly;
  with adjacent NMR and multi-omics/statistics tools);
- a **public, cloneable code repository** (GitHub, or Bitbucket / GitLab /
  institutional git);
- a **source method paper with a DOI**;
- a successful **ASB build** grounded on that repo + paper.

### Exclusion criteria

- **Restricted-reuse papers** — three non-open-access DOIs were explicitly held
  out of the release (`10.1021/acs.jproteome.0c00962`, `10.1002/jms.5040`,
  `10.21105/joss.04029`).
- **Ungrounded skills** — 21 skills with no resolvable source DOI were dropped.
- **PII** — non-author personal/email tokens were redacted from evidence spans.
- **Repository-less entries** — database-only / dataset-only tools (e.g. public
  spectral or compound databases) are preserved in the project bibliography but
  **not built** in this release (no code repository to ground against).

### Grounding, deduplication & gating

- **Grounding:** every build was grounded on the tool's public repository
  (cloned at build time) plus the source paper and its supplementary information
  (via a per-paper Perspicacité KB). The access basis recorded for each paper is
  **`repo-oa`** — the redistributable source repository is open.
- **Deduplication:** skills were deduplicated by slug across 622 build directories
  (1,200 duplicate skills merged into canonical records); tools deduplicated by name.
- **Release gate (CONTENT_POLICY):** the collection passes a strict release gate —
  access-tier (OA), verbatim-quote caps, PII / dual-use scan, and provenance
  (every skill carries a source DOI + license). See [gate_report.json](gate_report.json).

---

## Limitations

- This is a **preliminary** release; technique tags and EDAM annotations are
  heuristic/automated and may contain mis-tags.
- Skills are **distilled** from papers + repos by an LLM pipeline (mixed Opus 4.8
  / Haiku 4.5); always verify a parameter or claim against the source — the
  Perspicacité binder ([USAGE.md §4](USAGE.md)) makes this one command.
- The **benchmark layer** and **raw ASB capsules** (full end-to-end traceability)
  are not in this release; they follow later.

## Cite

Cite both the **collection** ([CITATION.cff](CITATION.cff) / Zenodo, once minted)
and the **original paper** behind each skill you use (`attribution.original_doi`).
Generation sponsored by **CNRS** and **Université Côte d'Azur**; curated by
**Holobiomics Lab** (holobiomicslab.cnrs.fr) and **MetaboLinkAI** (metabolinkai.net).
