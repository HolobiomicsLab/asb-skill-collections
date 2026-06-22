---
name: spectral-peak-normalization
description: Use when when preparing query spectra and library spectra for similarity-based matching via dot product scoring, particularly in open modification spectral library searches where you need to match modified query spectra to unmodified library counterparts without the results being biased by.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - mass-spectrometry
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

# spectral-peak-normalization

## Summary

L2 normalization of mass spectra to unit vectors, converting raw peak intensities into a scale-invariant representation suitable for dot-product-based similarity scoring. This preprocessing step enables fair comparison of spectra with different total intensities and is essential for cascade search strategies in open modification spectral library matching.

## When to use

When preparing query spectra and library spectra for similarity-based matching via dot product scoring, particularly in open modification spectral library searches where you need to match modified query spectra to unmodified library counterparts without the results being biased by differences in total ion intensity between samples.

## When NOT to use

- When comparing spectra using operations that are inherently intensity-scale-sensitive (e.g., Euclidean distance, raw dot product without normalization) where you want to preserve absolute intensity differences.
- When the input spectrum has zero total intensity (degenerate case); ensure pre-filtering to exclude empty or noise-only spectra.
- When relative peak intensity patterns are not the primary matching criterion (e.g., if absolute quantitation or intensity ratios carry biological meaning that must be preserved).

## Inputs

- raw mass spectrum (peaks with m/z and intensity values)
- library spectrum (peaks with m/z and intensity values)

## Outputs

- normalized spectrum as unit vector (L2-normalized peak intensities)
- normalized query spectrum (L2-normalized unit vector)
- normalized library spectrum (L2-normalized unit vector)

## How to apply

For each spectrum (both query and library), compute the L2 norm of the intensity vector and divide all peak intensities by this norm to produce a unit vector. This converts absolute peak intensities into a scale-invariant representation. The normalized spectra are then used as input to the shifted dot product computation: for each candidate mass shift within the search tolerance window, compute the dot product between the normalized query spectrum and the mass-shifted normalized library spectrum, retaining the maximum score. L2 normalization ensures that two spectra with identical peak patterns but different total intensities yield identical similarity scores, which is critical for controlling false discovery rates across diverse sample conditions.

## Related tools

- **ANN-SoLo** (spectral library search engine that applies L2 normalization to both query and library spectra as part of its cascade search strategy for open modification matching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (approximate nearest neighbor indexing backend used by ANN-SoLo for fast candidate selection; requires normalized vector inputs) — https://github.com/facebookresearch/faiss

## Evaluation signals

- Verify that the L2 norm of each normalized spectrum equals 1.0 (within floating-point tolerance ~1e-6).
- Confirm that two spectra with identical peak patterns but different absolute intensities (e.g., one scaled by 10×) yield identical dot product scores after normalization.
- Check that the dot product between a normalized spectrum and itself equals 1.0, and dot products between distinct spectra fall in the range [−1, 1].
- Verify that shifted dot product scores computed on normalized spectra are invariant to global intensity scaling of the query or library spectrum.
- Inspect cascade search results to confirm that false discovery rate remains controlled across samples with widely varying total ion current, indicating normalization is preventing spurious high-intensity matches.

## Limitations

- L2 normalization discards absolute intensity information; low-abundance peaks receive equal weight to high-abundance peaks after normalization, which may reduce sensitivity to bona fide low-intensity ions in some biological contexts.
- The method requires that spectra contain at least one non-zero peak; completely silent or zero-intensity spectra will cause division-by-zero errors or undefined results.
- L2 normalization is sensitive to noise and outlier peaks; a single very-high-intensity noise spike can dampen all other normalized peak intensities, potentially reducing sensitivity to genuine signal peaks.
- The README notes that ANN-SoLo requires Python 3.6–3.9 and specific Faiss installations; CPU-only and GPU versions have different platform support (Linux for GPU, Linux/OSX for CPU), which may limit deployment flexibility.

## Evidence

- [other] 1. Normalize both the query and library spectra to unit vectors using L2 normalization.: "Normalize both the query and library spectra to unit vectors using L2 normalization"
- [other] 2. For each possible mass shift value within the search tolerance window, compute the dot product between the query spectrum and the mass-shifted library spectrum.: "For each possible mass shift value within the search tolerance window, compute the dot product between the query spectrum and the mass-shifted library spectrum"
- [other] 3. Return the maximum dot product score across all tested mass shifts as the shifted dot product similarity metric.: "Return the maximum dot product score across all tested mass shifts as the shifted dot product similarity metric"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
