---
name: mass-shift-tolerance-scoring
description: Use when when searching for peptide spectra with unknown or open modifications (i.e., any mass shift within a broad tolerance range rather than a fixed set of known modifications).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-shift-tolerance-scoring

## Summary

A spectral matching technique that tests multiple mass shift values within a defined search tolerance window to identify peptide modifications. The method computes similarity scores across all possible mass shifts and returns the maximum, enabling sensitive matching of modified query spectra to unmodified library counterparts while maintaining false discovery rate control.

## When to use

When searching for peptide spectra with unknown or open modifications (i.e., any mass shift within a broad tolerance range rather than a fixed set of known modifications). Use this skill when you have a query spectrum suspected of containing a modification and need to match it against a spectral library of unmodified peptides, requiring both high sensitivity and strict FDR control.

## When NOT to use

- Input spectra are not normalized or cannot be normalized to unit vectors (e.g., empty or all-zero spectra).
- Search task involves only known, fixed modifications (e.g., phosphorylation at +79.97 Da); use directed modification searches instead.
- Library spectra are pre-filtered by mass and the mass shift tolerance is already constrained to near-zero (i.e., unmodified peptide matching); the overhead of testing multiple shifts provides no benefit.

## Inputs

- query spectrum (m/z and intensity pairs, normalized to unit vector)
- library spectrum (m/z and intensity pairs, normalized to unit vector)
- mass shift search tolerance window (Da)
- set of candidate library spectra from approximate nearest neighbor indexing

## Outputs

- shifted dot product similarity score (float, 0–1 range for unit-normalized vectors)
- optimal mass shift value corresponding to the maximum score (Da)

## How to apply

Normalize both the query spectrum and each library spectrum to unit vectors using L2 normalization to make scores invariant to spectrum intensity. For each candidate library spectrum within the approximate nearest neighbor result set, systematically test all possible mass shift values spanning the defined search tolerance window (e.g., ±500 Da or user-specified range). For each mass shift, compute the dot product between the normalized query spectrum and the mass-shifted normalized library spectrum. Retain the maximum dot product score across all tested shifts as the final similarity metric for that library entry. This approach is integrated within ANN-SoLo's cascade search strategy, which applies increasingly stringent scoring thresholds to maximize identified modified peptides while strictly controlling false discovery rate.

## Related tools

- **ANN-SoLo** (Spectral library search engine that integrates shifted dot product scoring within a cascade search strategy for open modification matching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Provides approximate nearest neighbor indexing to pre-select candidate library spectra before shifted dot product scoring) — https://github.com/facebookresearch/faiss

## Evaluation signals

- Dot product score is in the range [0, 1] for L2-normalized unit vectors (invariant check).
- Maximum score across all tested mass shifts is ≥ scores from individual shifts (monotonicity).
- Retrieved mass shift value lies within the specified search tolerance window.
- Identified modifications match known or biologically plausible mass shifts (e.g., oxidation +15.995 Da, phosphorylation +79.966 Da) when validated against external databases.
- False discovery rate of matched spectra remains below the configured threshold when cascade search strategy is applied downstream.

## Limitations

- Computational cost scales linearly with the size of the mass shift tolerance window; very broad windows (e.g., ±1000 Da) may require GPU acceleration for practical throughput.
- L2 normalization suppresses intensity information; spectra with markedly different peak heights may yield misleading high scores if peaks are aligned only by m/z.
- The method assumes library spectra are unmodified; matching a modified query to a pre-modified library entry will yield artificially high scores at the wrong mass shift.
- Approximate nearest neighbor pre-filtering may exclude the true best-matching library spectrum if it falls outside the ANN candidate set, preventing recovery even with shifted dot product scoring.
- False discovery rate control depends on the cascade search strategy and subsequent statistical post-processing; shifted dot product score alone does not guarantee FDR.

## Evidence

- [other] For each possible mass shift value within the search tolerance window, compute the dot product between the query spectrum and the mass-shifted library spectrum.: "For each possible mass shift value within the search tolerance window, compute the dot product between the query spectrum and the mass-shifted library spectrum."
- [other] Normalize both the query and library spectra to unit vectors using L2 normalization.: "Normalize both the query and library spectra to unit vectors using L2 normalization."
- [other] Return the maximum dot product score across all tested mass shifts as the shifted dot product similarity metric.: "Return the maximum dot product score across all tested mass shifts as the shifted dot product similarity metric."
- [other] ANN-SoLo uses the shifted dot product score as part of a cascade search strategy to sensitively match modified spectra to their unmodified counterparts while strictly controlling the false discovery rate.: "ANN-SoLo uses the shifted dot product score as part of a cascade search strategy to sensitively match modified spectra to their unmodified counterparts while strictly controlling the false discovery"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
