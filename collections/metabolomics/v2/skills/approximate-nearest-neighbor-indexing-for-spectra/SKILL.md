---
name: approximate-nearest-neighbor-indexing-for-spectra
description: Use when when you have a large spectral library (hundreds of thousands or millions of spectra) and need to search unknown query spectra against it for both unmodified and post-translationally modified peptides.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# approximate-nearest-neighbor-indexing-for-spectra

## Summary

Use approximate nearest neighbor (ANN) indexing to accelerate open modification spectral library searching by retrieving only the most relevant library spectra for each query spectrum, combined with cascade search and FDR control to maximize identification of both unmodified and modified peptides. This reduces computational cost while maintaining or improving sensitivity and specificity.

## When to use

When you have a large spectral library (hundreds of thousands or millions of spectra) and need to search unknown query spectra against it for both unmodified and post-translationally modified peptides. Use ANN indexing when exhaustive comparison of every query–library pair is computationally prohibitive but approximate ranking of candidates is acceptable. Particularly applicable to high-resolution mass spectrometry data where modified peptides may exhibit shifted m/z or fragmentation patterns.

## When NOT to use

- When your spectral library is small (<1000 spectra) — exhaustive search is faster and more accurate than ANN overhead.
- When you require guaranteed optimal (global) matches — ANN indexing is approximate and may miss low-scoring true matches if they fall outside the retrieved candidate set.
- When query spectra are of very low resolution or high noise — index construction and nearest neighbor ranking rely on stable feature representations; noisy or low-resolution input degrades candidate retrieval quality.

## Inputs

- spectral library in high-resolution format (e.g., mzML, mzXML, or formatted spectral list)
- query mass spectra in high-resolution format
- spectral library metadata (peptide sequences, modifications, precursor m/z, retention time if available)

## Outputs

- ranked list of candidate matches per query spectrum (peptide sequence, modification state, score, FDR q-value)
- spectrum-level or peptide-level FDR-controlled identification assignments
- ANN index (serialized) for reuse across future searches

## How to apply

Build an approximate nearest neighbor index on your spectral library using Faiss (or equivalent ANN backend). For each query spectrum, use the index to retrieve a limited candidate set (e.g., top-k most similar library spectra) rather than scoring all library members. Apply a cascade search strategy: first perform cosine similarity scoring against candidates to identify exact unmodified peptide matches; for spectra without confident unmodified hits, perform an open modification search on the same candidates using the shifted dot product score to sensitively detect mass-shifted variants. Rank all identified matches (unmodified and modified) by score and apply spectrum- or peptide-level false discovery rate (FDR) filtering to control false positives. The rationale is that true matches cluster in feature space, so retrieving only nearest neighbors preserves sensitivity while dramatically reducing computation.

## Related tools

- **ANN-SoLo** (Spectral library search engine that implements approximate nearest neighbor indexing combined with cascade search strategy, cosine similarity scoring for unmodified matches, and shifted dot product scoring for open modification detection, with integrated FDR control.) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library for building and querying approximate nearest neighbor indices; supports GPU acceleration for index construction and candidate retrieval on NVIDIA CUDA devices.) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --query_spectra query.mzML --library library.mzML --output results.csv --fdr 0.01
```

## Evaluation signals

- Verify that the number of candidate spectra retrieved per query is significantly smaller than the total library size (e.g., top-k << total spectra), confirming dimensionality reduction.
- Check that spectrum-level or peptide-level FDR values are properly computed and that the proportion of identifications passing the FDR threshold (e.g., q < 0.01) is calibrated correctly.
- Confirm that both unmodified and modified peptide identifications are reported, with cascade search evidenced by unmodified matches appearing before open modification searches in the ranking.
- Validate that shifted dot product scores for modified matches are positive and within expected range, indicating genuine mass-shifted peptide similarity.
- Cross-validate a subset of high-confidence identifications (high score, low FDR) against orthogonal data (e.g., retention time, fragmentation pattern libraries) to ensure index approximation did not filter out true matches.

## Limitations

- ANN indexing is approximate; true matches may be missed if they rank outside the retrieved candidate set, particularly for low-scoring or uncommon modifications.
- Requires Python 3.6–3.9; Python 3.10+ not currently supported (per README), limiting deployment on newer systems without version management.
- GPU acceleration available only on Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX but is significantly slower.
- Feature hashing and GPU acceleration (task_004) require high-resolution spectra; application to low-resolution data or non-standard m/z formats not discussed.
- FDR control is applied post hoc to ranked matches; if cascade search or index retrieval is misconfigured, downstream FDR estimates may be invalid.

## Evidence

- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra"
- [readme] Cascade search strategy is combined to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match"
- [other] The cascade search strategy is combined with approximate nearest neighbor indexing and uses the shifted dot product score to sensitively match modified spectra to their unmodified counterparts while maximizing identified unmodified and modified spectra and strictly controlling the false discovery rate.: "cascade search strategy is combined with approximate nearest neighbor indexing and uses the shifted dot product score to sensitively match modified spectra to their unmodified counterparts while"
- [other] For each query spectrum, retrieve a limited set of candidate library matches using ANN search. Apply cascade search: first search candidates for exact unmodified peptide matches using cosine similarity scoring. For spectra without confident unmodified matches, perform open modification search on the same candidates, allowing variable mass shifts.: "For each query spectrum, retrieve a limited set of candidate library matches using ANN search. Apply cascade search: first search candidates for exact unmodified peptide matches using cosine"
- [readme] The Faiss installation depends on a specific GPU version. The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms.: "GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms"
