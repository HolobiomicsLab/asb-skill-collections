---
name: dot-product-based-spectral-comparison
description: Use when when searching an unknown MS/MS spectrum against a spectral library and you need to rapidly identify the most relevant candidate library spectra before applying cascade scoring with false discovery rate control.
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
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
schema_version: 0.2.0
---

# dot-product-based-spectral-comparison

## Summary

A vectorized similarity scoring method that computes dot products between normalized spectrum intensity vectors to rank library spectra by relevance to a query spectrum, enabling fast approximate nearest-neighbor retrieval and sensitive matching of post-translationally modified peptides to their unmodified reference spectra.

## When to use

When searching an unknown MS/MS spectrum against a spectral library and you need to rapidly identify the most relevant candidate library spectra before applying cascade scoring with false discovery rate control. Use this when your input consists of normalized intensity vectors from query and library spectra, especially in open modification searches where mass offset variations must be detected across a range of possible modifications.

## When NOT to use

- Input spectra are not normalized or intensity vectors are missing; dot product scoring requires proper L2 normalization to be valid.
- You are performing targeted (known modification) searches only; shifted dot product scoring is optimized for open modification searching and will be over-engineered for closed searches.
- The spectral library is very small (<100 spectra); approximate nearest neighbor indexing provides speed gains primarily with large libraries.

## Inputs

- query spectrum (normalized intensity vector with m/z values)
- spectral library (collection of normalized intensity vectors with m/z values)
- mass offset range (for detection of post-translational modifications)

## Outputs

- ranked list of candidate library spectra (sorted by shifted dot product score)
- similarity scores (dot product values across mass offsets)
- filtered library subset for cascade scoring

## How to apply

Normalize intensity vectors for both the query spectrum and candidate library spectra (typically L2 normalization). Compute pairwise dot products between the query vector and library vectors across a range of mass offset values to detect post-translational modifications. Use the shifted dot product score—which evaluates alignment at multiple m/z shifts—to identify library spectra with the highest similarity scores. Rank candidates by these scores and select only the most relevant spectra for downstream cascade searching. The cascade strategy then applies stricter matching criteria and false discovery rate control on this reduced candidate set to maximize identification sensitivity while maintaining specificity.

## Related tools

- **ANN-SoLo** (spectral library search engine implementing shifted dot product scoring within a cascade search strategy for fast open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (approximate nearest neighbor indexing backend used by ANN-SoLo to accelerate candidate selection) — https://github.com/facebookresearch/faiss

## Evaluation signals

- True modified–unmodified spectrum pairs receive higher shifted dot product scores than random decoy matches (validation against known pairs).
- Score distribution shows separation between correct matches and random background with measurable sensitivity and specificity metrics.
- Selected candidate spectra from the top-ranked subset correctly identify the query spectrum's modification state in downstream cascade scoring.
- Vectorized computation produces identical scores across multiple runs (reproducibility check).
- False discovery rate remains controlled after cascade scoring on the ANN-SoLo-selected candidates, indicating no bias in candidate pre-filtering.

## Limitations

- Dot product scoring is sensitive to spectrum normalization; unnormalized or poorly normalized spectra will produce unreliable scores.
- Performance degrades when library spectra are from different MS platforms or collision energy settings than the query, as peak intensity distributions may differ substantially.
- The shifted dot product approach scans a fixed mass offset range; very large or unexpected modifications outside this range may be missed.
- Python 3.6–3.9 support only; Python 3.10+ is not currently supported (as noted in the README).
- GPU-accelerated version is Linux/NVIDIA-only; CPU-only version supports Linux and OSX.

## Evidence

- [other] The shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts: "shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts"
- [other] Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors.: "Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score"
- [other] Validate the scoring function against known modified–unmodified spectrum pairs by verifying that true matches receive higher scores than random decoy matches.: "Validate the scoring function against known modified–unmodified spectrum pairs by verifying that true matches receive higher scores than random decoy matches"
