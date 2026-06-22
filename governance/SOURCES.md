# Scientific Sources & Inclusion Criteria

**Status:** v0 · **Date:** 2026-06-22 · **Scope:** the *scientific* gate for ASB-Skill source papers.

> This document complements [`CONTENT_POLICY.md`](CONTENT_POLICY.md). **CONTENT_POLICY governs the *legal* gate** (open-access status, licensing, transformation bounds). **This document governs the *scientific* gate** (where a paper comes from and what makes it eligible). **Both gates apply to every paper** before it enters a collection's corpus.

## 1. Why this document

ASB-Skills are distilled from peer-reviewed **method papers**. To keep the corpus
principled and auditable, every source paper is anchored to a recognized field
inventory and screened against explicit scientific criteria — separately from,
and in addition to, the open-access/legal checks in `CONTENT_POLICY.md`.

## 2. Anchoring literature — the computational metabolomics review series

Our universe of candidate methods is anchored to the **computational metabolomics
review series**, a periodically updated inventory of the field's tools and
methods, in two eras:

**Misra-led era (~2014/2015–2020).** The annual "metabolomics tools & resources
updates" review series.

<!-- BEGIN Task-1 citations: Misra series -->
The annual "metabolomics tools & resources updates" review series by **B.B. Misra**
(with **J.J.J. van der Hooft** on the 2015 edition, per the Enveda repository's own
attribution). It periodically inventoried computational metabolomics methods,
tools, databases, and resources across roughly 2014/2015–2020.

- Named anchors cited by the Enveda repo: **Misra (2021)** and **Misra & van der Hooft (2015)**.
- Exact per-edition titles, venues, years, and DOIs:
  <!-- TO VERIFY via Perspicacité / Crossref — not recalled from memory -->
<!-- END Task-1 citations: Misra series -->

**Enveda-continued era (2021–2025).** [`github.com/enveda/computational-metabolomics-review`](https://github.com/enveda/computational-metabolomics-review)
— a curated inventory of computational metabolomics tools/software/databases
(`tools_list.tsv`; 40+ categories spanning annotation, GC-MS/LC-MS/NMR/imaging-MS/
ion-mobility, lipidomics, exposomics, multiomics, …). **License: GPL-3.0.** It
explicitly continues Misra (2021) and Misra–van der Hooft (2015). Associated
peer-reviewed paper:

<!-- BEGIN Task-1 citation: Enveda paper -->
**Domingo-Fernández D. et al.** (Enveda Biosciences). Computational metabolomics
review / tools inventory. *Analytical Chemistry*, **2026** (forthcoming).
DOI: <!-- TO VERIFY (paper forthcoming) -->
Repository: https://github.com/enveda/computational-metabolomics-review
(License **GPL-3.0**; `tools_list.tsv`; 40+ categories; continues Misra 2021 and
Misra & van der Hooft 2015).
<!-- END Task-1 citation: Enveda paper -->

**Tools vs. method papers.** The review series curates *tools/software*; ASB-Skills
distill *peer-reviewed method papers*. The provenance chain is:

> review series enumerates a method/tool → its peer-reviewed method paper is the
> inclusion candidate → curation (legal + scientific gates) → `corpus.yaml` →
> skills.

We cite these reviews as **named upstream sources of candidate methods**. We do
not import their lists automatically, and we add no per-paper provenance field
(provenance is documented here, at the corpus level).

## 3. Scientific inclusion criteria

A source paper is **eligible** when it meets all of:

1. **Method/tool-introducing** — it introduces a method, algorithm, tool, or
   resource (not a pure application or biological-result paper).
2. **Reproducible artifact** — it has a public code repository, dataset, or
   executable workflow that enables an agent task / benchmark.
3. **Thematic fit** — it fits a target collection's scope.
4. **Adoption or foundational signal** — it is widely used, foundational, or
   captures rare/valuable expertise.
5. **Traceable to the field inventory** — it is consistent with the
   computational-metabolomics review-series taxonomy (or an analogous curated
   inventory for non-metabolomics collections).
6. **Current** — not retracted, and not fully superseded by a later method that
   replaces it.

## 4. Exclusion criteria

A paper is **excluded** when any of:

- No method/tool/resource (pure application or result-only).
- No reproducible artifact (no code/data/workflow to ground an agent task).
- Out of the target collection's scope.
- Retracted (Crossref / Retraction Watch).
- Fails the **legal gate** in `CONTENT_POLICY.md` (paywalled/closed/unknown
  access, or a restrictive license). See [`OPEN_ACCESS_POLICY.md`](OPEN_ACCESS_POLICY.md).

## 5. How the corpus derives from sources

Each collection's source-of-truth is `collections/<slug>/v<N>/corpus.yaml`
(`schema: asb-corpus/1.0`). It records a corpus-level `source:` line and, per
paper, a `category` aligned to the review-series taxonomy plus an `access` block
(verified per `CONTENT_POLICY.md`). The pipeline is:

> review-series / proposal → candidate method paper → curation (this document's
> scientific gate **and** CONTENT_POLICY's legal gate) → `corpus.yaml` entry →
> distilled skills.

## 6. Contributing & related policies

- **Suggest or annotate a paper:** see [CONTRIBUTING → "Propose or annotate a paper"](../.github/CONTRIBUTING.md#propose-or-annotate-a-paper).
- **Legal/provenance policy:** [`CONTENT_POLICY.md`](CONTENT_POLICY.md).
- **Open-access verification:** [`OPEN_ACCESS_POLICY.md`](OPEN_ACCESS_POLICY.md).
