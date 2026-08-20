---
name: open-modification-spectrum-matching
description: Use when when you have a query mass spectrum with unknown or unanticipated post-translational modifications and need to match it against an unmodified spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# open-modification-spectrum-matching

## Summary

Match mass spectra bearing unknown post-translational modifications to unmodified library spectra by computing shifted dot product scores across a tolerance window of mass shifts, enabling sensitive identification while controlling false discovery rate. This skill combines approximate nearest neighbor indexing with a cascade search strategy and shifted dot product scoring to handle open modification searching efficiently.

## When to use

When you have a query mass spectrum with unknown or unanticipated post-translational modifications and need to match it against an unmodified spectral library. Use this skill when you want to detect modified peptides without pre-defining the modification masses, while strictly controlling the false discovery rate across identified spectra.

## When NOT to use

- When all possible modifications are known in advance and pre-defined modification masses are available; use standard unshifted dot product scoring instead.
- When query spectra are already known to be unmodified; standard library matching without mass shift iteration is more efficient.
- When working with low-resolution spectra where mass shift discrimination is impossible due to insufficient m/z precision.

## Inputs

- query spectrum (m/z–intensity pairs, L2-normalized)
- spectral library (collection of unmodified reference spectra, L2-normalized)
- mass shift tolerance window (Da)
- candidate library spectra from approximate nearest neighbor pre-filter

## Outputs

- shifted dot product score (maximum score across all mass shifts tested)
- matched library spectrum identity
- inferred mass shift value (Da)
- FDR-controlled match assignment

## How to apply

Normalize both query and library spectra to unit vectors using L2 normalization. For each possible mass shift value within the search tolerance window (e.g., ±500 Da or study-specific bounds), compute the dot product between the normalized query spectrum and the mass-shifted library spectrum. Return the maximum dot product score across all tested mass shifts as the primary similarity metric. Integrate this scoring into a cascade search strategy: first perform approximate nearest neighbor indexing to select only the most relevant library spectra, then apply shifted dot product scoring to those candidates, and finally apply statistical filtering to control false discovery rate. The cascade approach maximizes sensitivity for both unmodified and modified spectra while maintaining strict FDR control.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing approximate nearest neighbor indexing, cascade search strategy, shifted dot product scoring, and FDR control for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Approximate nearest neighbor indexing backend used by ANN-SoLo to rapidly select relevant library spectra before shifted dot product scoring) — https://github.com/facebookresearch/faiss

## Evaluation signals

- Shifted dot product scores should range between −1 and 1 (inner product of unit-normalized vectors); verify L2 normalization was applied to both query and library spectra.
- Maximum shifted dot product score across all tested mass shifts should be ≥ the unshifted (zero mass shift) score; if not, verify mass shift iteration logic.
- Inferred mass shifts should fall within the user-specified tolerance window; out-of-bounds shifts indicate configuration or implementation error.
- False discovery rate of assigned matches should not exceed the user-specified threshold (e.g., 1% or 5%); verify cascade strategy and FDR filtering stages were applied.
- Performance comparison: fewer library spectra should require dot product computation (via approximate nearest neighbor pre-filtering) than in brute-force matching, with minimal loss of sensitivity for ground-truth modified peptide matches.

## Limitations

- Shifted dot product scoring requires exhaustive iteration over all mass shift values in the tolerance window; wide tolerance windows (e.g., ±500 Da with 0.1 Da step) significantly increase computational cost.
- Approximate nearest neighbor pre-filtering may exclude the true unmodified library match if the query spectrum is heavily modified, resulting in reduced sensitivity for extreme modifications; the cascade strategy mitigates this by progressively relaxing filters.
- Sensitivity depends on spectral quality and fragmentation pattern conservation between modified and unmodified forms; peptides with modifications that substantially alter fragmentation (e.g., charge state changes) may not match well to unmodified counterparts.
- The method is optimized for open modification searching of unmodified library spectra; pre-indexed modified libraries may require different or additional scoring strategies.
- Python 3.6–3.9 only; GPU support (NVIDIA CUDA) requires Linux; CPU-only version supports Linux and OSX but with reduced speed.

## Evidence

- [other] shifted dot product score: "the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [other] L2 normalization and dot product computation across mass shifts: "Normalize both the query and library spectra to unit vectors using L2 normalization. 2. For each possible mass shift value within the search tolerance window, compute the dot product between the"
- [other] cascade search strategy and FDR control: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] approximate nearest neighbor pre-filtering rationale: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
