---
name: cascade-search-strategy-for-peptide-identification
description: Use when use this strategy when analyzing tandem mass spectrometry data
  where you expect both unmodified and modified peptide identifications and require
  high confidence assignments with controlled false discovery rates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary)
  is a spectral library search engine'
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

# cascade-search-strategy-for-peptide-identification

## Summary

A two-stage spectral library search strategy that first attempts to match query spectra against unmodified peptides using exact mass and cosine similarity, then performs open modification searching on spectra without confident unmodified matches. This approach maximizes identification of both unmodified and post-translationally modified peptides while maintaining strict false discovery rate control.

## When to use

Use this strategy when analyzing tandem mass spectrometry data where you expect both unmodified and modified peptide identifications and require high confidence assignments with controlled false discovery rates. This is particularly valuable when the frequency and nature of modifications are unknown or heterogeneous, and you want to avoid premature commitment to modification searches that may waste computational resources or introduce false positives.

## When NOT to use

- Input spectra are already pre-filtered to contain only known modified peptides; cascade search is inefficient when modification state is known a priori.
- Spectral library is extremely small or query set is very large relative to available computational resources; the cost of building the ANN index may not be justified.
- Analysis requires real-time or ultra-low-latency matching; the two-stage cascade and ANN index construction add latency compared to single-pass heuristics.

## Inputs

- Query spectra (mass spectrometry/MS2 format)
- Spectral library (reference peptide spectra with known sequences and modifications)

## Outputs

- List of peptide identifications with assigned peptide sequences, modification states, and FDR values
- Spectrum-to-peptide match pairs with match scores (cosine similarity or shifted dot product)

## How to apply

First, build an approximate nearest neighbor index on the spectral library and retrieve a limited candidate set for each query spectrum using ANN search to reduce computational cost. Then apply a cascade: (1) search the candidate set for exact unmodified peptide matches using cosine similarity scoring; (2) for spectra lacking confident unmodified matches, perform open modification search on the same candidates using shifted dot product scoring to allow variable mass shifts; (3) rank all identified matches (unmodified and modified) by score and apply false discovery rate control at spectrum-level or peptide-level to assign FDR values. The rationale is that the initial exact search filters out most queries efficiently, reserving the more expensive open modification search only for ambiguous spectra, thereby improving speed while maximizing sensitivity for modified peptides and maintaining strict FDR guarantees.

## Related tools

- **ANN-SoLo** (Implements cascade search strategy combined with approximate nearest neighbor indexing to perform fast open modification spectral library searching with FDR control) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- Verify that spectra with confident unmodified matches (high cosine similarity) do not proceed to the open modification search stage.
- Check that unmodified identifications have lower average match scores than modified identifications for spectra that triggered the second stage, confirming the cascade logic.
- Confirm that all reported identifications (unmodified and modified) have assigned FDR values ≤ the specified threshold (e.g., 1% or 5% FDR).
- Validate that the number of identified modified spectra is higher than would be achieved by open modification search alone, indicating the cascade strategy successfully enriches modified peptide detection.
- Inspect the distribution of spectrum-level vs. peptide-level FDR values to ensure the chosen FDR control level is consistently applied across the result set.

## Limitations

- Performance depends critically on the quality and comprehensiveness of the spectral library; sparse or incomplete libraries may reduce cascade effectiveness.
- The strategy assumes that unmodified peptides will be detected reliably in the first stage; rare or poorly-ionizing unmodified forms may be missed if they have low cosine similarity scores.
- Python version support is restricted to Python 3.6–3.9; GPU acceleration requires NVIDIA CUDA and is limited to Linux systems, which may constrain deployment.
- The shifted dot product scoring for open modification search may not perform equally well for all classes of modifications; performance is validated on common PTMs but behavior on novel modifications is not characterized.

## Evidence

- [other] cascade search strategy is combined with approximate nearest neighbor indexing and uses the shifted dot product score to sensitively match modified spectra: "cascade search strategy is combined with approximate nearest neighbor indexing and uses the shifted dot product score to sensitively match modified spectra to their unmodified counterparts"
- [readme] cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] first search candidates for exact unmodified peptide matches using cosine similarity scoring. 4. For spectra without confident unmodified matches, perform open modification search on the same candidates: "first search candidates for exact unmodified peptide matches using cosine similarity scoring. 4. For spectra without confident unmodified matches, perform open modification search on the same"
- [other] Rank all identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering: "Rank all identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering"
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra"
