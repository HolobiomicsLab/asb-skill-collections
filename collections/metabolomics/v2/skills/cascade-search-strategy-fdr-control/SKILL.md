---
name: cascade-search-strategy-fdr-control
description: Use when when searching high-resolution mass spectra against spectral libraries and you need to identify both unmodified and post-translationally modified peptides while maintaining strict control over false positive identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
---

# Cascade Search Strategy with False Discovery Rate Control

## Summary

A multi-stage spectral library search strategy that first queries unmodified peptides, then performs open modification searches, applying strict false discovery rate (FDR) control at each stage to maximize identifications while controlling error rates. This approach is particularly effective when combined with approximate nearest neighbor indexing to prioritize the most relevant library spectra.

## When to use

When searching high-resolution mass spectra against spectral libraries and you need to identify both unmodified and post-translationally modified peptides while maintaining strict control over false positive identifications. The cascade strategy is most valuable when you want to leverage the higher confidence of unmodified matches to improve downstream open modification searching without accumulating FDR across search stages.

## When NOT to use

- When spectral library already contains pre-computed modified peptide entries—the cascade strategy targets unknown modifications, not pre-enumerated variants.
- When computational cost of multi-stage searching is prohibitive; single-pass unmodified search may be more efficient for constrained resources.
- When input spectra are low-resolution (e.g., ion trap, triple-quadrupole) and modification mass shifts are difficult to resolve reliably.

## Inputs

- High-resolution mass spectra (in mzML, mzXML, or similar format)
- Spectral library (formatted for library search engine)
- Query spectrum set

## Outputs

- Ranked candidate peptide matches with modification assignments
- Identification scores per query spectrum
- False discovery rate-controlled confidence estimates

## How to apply

Structure the spectral library search as a multi-stage cascade: (1) Begin with unmodified peptide search against the full spectral library or ANN-indexed candidate subset, establishing a baseline set of high-confidence matches. (2) Apply FDR control to these unmodified results using target-decoy or similar statistical methods. (3) Transition to open modification search on remaining unidentified spectra, using the shifted dot product score to sensitively match modified spectra to their unmodified counterpart in the library. (4) Re-apply strict FDR control to the combined unmodified and modified identifications to prevent error accumulation. The rationale is that cascading reduces search space progressively while maintaining statistical rigor at each stage, and the shifted dot product enables sensitive detection of modifications without requiring pre-specification.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing cascade search strategy and FDR control via shifted dot product scoring for unmodified and open modification searches) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- FDR at each cascade stage (unmodified, modified) is ≤ specified threshold (typically 1–5%); verify via target-decoy q-value computation.
- Number of identifications increases monotonically or plateaus across cascade stages; verify no identifications are lost or duplicated between stages.
- Modification mass assignments in open modification results correspond to known PTM masses or mass shifts within instrument tolerance; verify consistency.
- Shifted dot product scores for modified matches fall in a distinct range (lower than unmodified, but above noise); verify score distribution is bimodal or appropriately separated.
- Comparison to single-pass open modification search shows comparable or superior sensitivity at matched FDR; verify cascade does not lose identifications.

## Limitations

- FDR control relies on target-decoy paradigm; sensitivity may degrade if decoy generation does not accurately model the null distribution.
- Cascade strategy assumes unmodified peptides are more abundant or easier to match; performance degrades if library is heavily enriched for modified forms.
- Shifted dot product score requires careful parameterization; suboptimal mass shift tolerance or scoring thresholds can miss true modifications or inflate false positives.
- Multi-stage FDR control increases computational cost; benefit diminishes if candidate pool is already very small (e.g., after strict ANN filtering).

## Evidence

- [intro] Cascade search strategy is combined to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [readme] ANN-SoLo uses cascade search strategy combining unmodified then open modification searches with FDR control and shifted dot product scoring: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
