---
name: candidate-spectrum-retrieval-and-ranking
description: Use when when you have a large reference MS/MS spectral library (>10k spectra) and need to perform open modification searches on query spectra without exhaustively comparing against every library entry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - CE-MS
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

# Candidate Spectrum Retrieval and Ranking

## Summary

Use approximate nearest neighbor (ANN) indexing to rapidly select a limited subset of the most relevant library spectra for comparison to an unknown query spectrum, accelerating open modification searching while maintaining sensitivity. This skill combines ANN retrieval with cascade search and shifted dot product scoring to identify both unmodified and post-translationally modified peptides while controlling false discovery rate.

## When to use

When you have a large reference MS/MS spectral library (>10k spectra) and need to perform open modification searches on query spectra without exhaustively comparing against every library entry. Particularly valuable when searching for unknown or unexpected chemical modifications where you cannot pre-filter the library by precursor mass alone.

## When NOT to use

- Spectral library is very small (<1000 spectra) — exhaustive comparison may be more efficient and sufficient.
- Query spectrum has extremely high-quality precursor mass information and narrow mass tolerance; traditional narrow-window precursor mass filtering is already sufficient.
- Only searching for known, fixed modifications — use standard spectral library search with pre-filtering by modification mass shift.

## Inputs

- MS/MS spectral library (collection of reference spectra in vector or peak list format)
- Unknown query MS/MS spectrum (vectorized or peak intensity representation)
- Precursor mass tolerance parameter (for optional mass filtering)
- K parameter (number of candidate spectra to retrieve)

## Outputs

- Ranked list of candidate library spectra (limited subset, K entries)
- Similarity scores (shifted dot product or cosine similarity) for each candidate
- FDR-controlled match significance for modified and unmodified peptides

## How to apply

Load the spectral library and query spectrum; preprocess and vectorize spectra into numerical representations (e.g., intensity vectors or spectral features) suitable for distance-based indexing. Build an approximate nearest neighbor index over the library spectra using a space-partitioning or hashing-based algorithm (e.g., Faiss). Query the ANN index with the unknown spectrum to retrieve the K most similar library spectra (candidate set). Rank candidates using a cascade search strategy: first apply unmodified peptide scoring, then apply shifted dot product scoring to sensitively match modified spectra. Return the ranked candidate spectra with FDR-controlled significance thresholds for downstream validation.

## Related tools

- **ANN-SoLo** (Primary tool implementing approximate nearest neighbor indexing for spectral library search; combines ANN retrieval with cascade search strategy and shifted dot product scoring for open modification identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing approximate nearest neighbor index construction and querying (space-partitioning and hashing-based algorithms)) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --library spectral_lib.msp --spectra query.mgf --candidates 500 --fdr 0.01
```

## Evaluation signals

- Candidate set size matches the specified K parameter and retrieves only the K most similar library spectra.
- Similarity scores are monotonically decreasing across the ranked candidate list (highest similarity first).
- Cascade search correctly identifies both unmodified peptides (primary scoring) and modified peptides (shifted dot product scoring) with distinct score distributions.
- False discovery rate for final matches is ≤ target FDR threshold (e.g., 1% or 5%) as reported in cascade search validation.
- Execution time is substantially reduced compared to exhaustive library search (typically >10-fold speedup for large libraries) while maintaining or improving sensitivity.

## Limitations

- Python version support is restricted (3.6–3.9); Python 3.10+ not supported at time of publication.
- GPU-powered acceleration requires Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX.
- Retrieval quality depends on the quality of spectral preprocessing and vectorization; poor feature representation will degrade candidate ranking.
- K parameter must be tuned per experiment; too-small K risks missing true matches; too-large K reduces computational benefit.
- Cascade search FDR control assumes independence of scores across candidates, which may not hold for highly similar spectra in the candidate set.

## Evidence

- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra"
- [intro] Cascade search strategy combined with FDR control: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] Workflow: Preprocess spectra, build ANN index, query index, return ranked candidates: "Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features). 3. Build an approximate nearest neighbor index over the"
- [readme] Shifted dot product score for modified spectrum matching: "the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [readme] Faiss dependency for ANN implementation: "The **Faiss** installation depends on a specific GPU version. Please refer to the [Faiss installation instructions]"
