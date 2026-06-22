---
name: dot-product-similarity-computation
description: Use when when performing open modification spectral library searching and you need to sensitively match query spectra that may carry unknown post-translational or chemical modifications to an unmodified spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
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

# dot-product-similarity-computation

## Summary

Compute shifted dot product similarity scores between mass spectra by normalizing both query and library spectra to unit vectors, then evaluating dot products across a range of mass shift values to match modified peptide spectra to unmodified library counterparts. This metric is central to cascade-based open modification spectral library searching.

## When to use

When performing open modification spectral library searching and you need to sensitively match query spectra that may carry unknown post-translational or chemical modifications to an unmodified spectral library. Apply this skill when searching tolerance windows span multiple Daltons and you want to avoid exhaustively scoring all possible modification shifts while maintaining strict false discovery rate control.

## When NOT to use

- When the spectral library and query spectra are already aligned and no mass shift is expected (use standard dot product instead to reduce computation).
- When strict linear time complexity is required and the mass shift window is extremely large (>1000 Da with fine granularity), as the method scales with the number of shift hypotheses tested.
- When dealing with low-resolution spectra where mass shift granularity cannot be resolved (e.g., ion trap data with ±0.5 Da precision may not distinguish shifts < 1 Da reliably).

## Inputs

- query spectrum (m/z-intensity pairs, normalized to unit vector)
- library spectrum (m/z-intensity pairs, normalized to unit vector)
- mass shift search tolerance window (in Daltons, e.g., ±500 Da for open modification searches)

## Outputs

- shifted dot product similarity score (scalar, typically 0–1 range post-normalization)
- optimal mass shift value (Dalton offset at which maximum dot product was achieved)

## How to apply

Normalize both the query spectrum and each candidate library spectrum to unit vectors using L2 normalization. For each possible mass shift value within the user-defined search tolerance window, compute the dot product between the normalized query spectrum and the mass-shifted library spectrum. Return the maximum dot product score observed across all tested mass shifts as the final similarity metric. This approach ensures that spectra differing by a consistent mass offset (indicative of a modification) still achieve high similarity scores, while the L2 normalization makes scores comparable across different spectral intensities.

## Related tools

- **ANN-SoLo** (Spectral library search engine that integrates shifted dot product scoring within a cascade search strategy to match modified query spectra to unmodified library spectra while controlling FDR) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- Verify that both input spectra are normalized to unit vectors (L2 norm = 1.0) before dot product computation.
- Confirm that dot product scores fall in the expected range [0, 1] for normalized spectra.
- Check that the reported optimal mass shift lies within the specified search tolerance window.
- Validate that spectra with a true modification (known mass delta) achieve higher shifted dot product scores than unmodified counterparts, and that FDR remains controlled when integrated into a cascade strategy.
- Confirm that the maximum dot product returned is ≥ all other shift-specific dot products tested.

## Limitations

- The method requires exhaustive enumeration of mass shift hypotheses, so computational cost scales linearly with the tolerance window width and inversely with shift step size; very wide windows (>1000 Da) may become expensive.
- Sensitivity depends on spectral quality and peak alignment; noisy spectra with few intense peaks may yield artificially high dot products even for incorrect shifts.
- The approach assumes that modifications cause systematic mass shifts; complex modifications involving intensity redistribution or peak splitting may not be detected solely by mass shifting.
- L2 normalization makes the metric insensitive to absolute peak intensities, which can be both a strength (robustness) and a weakness (loss of intensity-based discrimination for similar-mass modifications).

## Evidence

- [other] Normalize both the query and library spectra to unit vectors using L2 normalization. For each possible mass shift value within the search tolerance window, compute the dot product between the query spectrum and the mass-shifted library spectrum. Return the maximum dot product score across all tested mass shifts as the shifted dot product similarity metric.: "Normalize both the query and library spectra to unit vectors using L2 normalization. For each possible mass shift value within the search tolerance window, compute the dot product between the query"
- [other] ANN-SoLo uses the shifted dot product score as part of a cascade search strategy to sensitively match modified spectra to their unmodified counterparts while strictly controlling the false discovery rate.: "ANN-SoLo uses the shifted dot product score as part of a cascade search strategy to sensitively match modified spectra to their unmodified counterparts while strictly controlling the false discovery"
- [readme] the shifted dot product score to sensitively match modified spectra to their unmodified counterpart: "the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
