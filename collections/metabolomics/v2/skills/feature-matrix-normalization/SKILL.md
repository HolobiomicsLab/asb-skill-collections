---
name: feature-matrix-normalization
description: Use when after aggregating Pfam domain hits from HMM scanning into a domain-feature matrix (rows = BGCs, columns = Pfam domains, cells = bit-scores or binary presence), and before computing pairwise distances or clustering BGCs into gene cluster families (GCFs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0780
  - http://edamontology.org/topic_0102
  tools:
  - pyHMMER
  - BiG-SLiCE
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans:
- Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_slice_cq
    doi: 10.1093/gigascience/giaa154
    title: BiG-SLiCE
  dedup_kept_from: coll_big_slice_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa154
  all_source_dois:
  - 10.1093/gigascience/giaa154
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-normalization

## Summary

L2-normalize biosynthetic domain feature vectors (presence/absence or bit-score counts per BGC) to enable cosine-like distance-based clustering of gene cluster families. This converts raw domain hit counts into unit-norm vectors suitable for downstream similarity computation.

## When to use

After aggregating Pfam domain hits from HMM scanning into a domain-feature matrix (rows = BGCs, columns = Pfam domains, cells = bit-scores or binary presence), and before computing pairwise distances or clustering BGCs into gene cluster families (GCFs). Use this when you need to compare BGCs by their biosynthetic domain composition in a way that is invariant to the total number of domains per cluster.

## When NOT to use

- Input is already a normalized or standardized feature table (e.g., already z-scored or l2-normalized)
- You require feature importance weighting by domain frequency or annotation quality (raw bit-scores may already encode this)
- BGC comparison should preserve absolute domain counts rather than compositional similarity (e.g., if presence of 10 domains vs. 100 domains is itself informative)

## Inputs

- Domain-feature matrix: tab-separated file with rows = BGC identifiers, columns = Pfam accessions, cells = bit-scores or binary presence/absence (0/1)
- Pfam domain hit table: aggregated HMM scan results (gene identifiers, Pfam accessions, bit-scores, e-values, domain coordinates)

## Outputs

- L2-normalized domain-feature matrix: TSV with same structure, each row sum-of-squares = 1
- Normalized feature vectors suitable for cosine-similarity-based clustering and BGC/GCF comparison

## How to apply

Take the raw domain-feature matrix where each row is a BGC and each column is a Pfam domain (with values representing bit-scores or presence/absence counts). Apply L2-normalization (Euclidean norm) to each row independently, dividing each row by its L2 norm (sqrt of sum of squares) to produce unit-norm vectors. This transformation ensures that BGCs with similar domain compositions but different total domain counts are treated as equally similar, and enables the use of cosine-like distance metrics (cosine distance = 1 − dot product of normalized vectors) in downstream clustering. The normalized matrix is then exported as TSV for use in clustering algorithms or similarity queries.

## Related tools

- **BiG-SLiCE** (Orchestrates domain detection and normalization as part of BGC clustering pipeline; applies l2-normalization after domain aggregation) — https://github.com/medema-group/bigslice
- **pyHMMER** (Performs HMM-based Pfam domain scanning to generate raw bit-scores that are aggregated and then normalized) — https://github.com/althonos/pyhmmer

## Evaluation signals

- Row-wise L2 norms of normalized matrix should all equal 1.0 (within floating-point precision, e.g., ±1e-6)
- Non-zero elements of normalized rows should be in the range [0, 1]
- Total sum of squares across all columns in each row should equal 1
- Cosine similarity between any two normalized rows should be in [-1, 1] and equal their dot product
- Normalized matrix should preserve the rank order of domain importance within each BGC (highest bit-scores remain highest after scaling)

## Limitations

- L2-normalization is sensitive to outliers: a single very high bit-score can dominate the norm; consider outlier filtering or robust normalization if domain predictions are of variable quality
- Information about absolute domain counts per BGC is lost after normalization; if biological significance depends on having 50 vs. 5 biosynthetic domains, this may obscure important differences
- Normalization assumes all domains contribute equally to cluster similarity; if domain weights should vary (e.g., by conservation or functional importance), use weighted normalization schemes
- Works only on numeric (bit-score or count) matrices; binary presence/absence matrices are also valid but will reduce sensitivity to bit-score magnitudes

## Evidence

- [readme] Clustering now uses cosine-like (via l2-normalization) distances: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [other] Domain feature extraction and normalization workflow: "Normalize domain presence/absence or bit-score vectors using l2-normalization to prepare for downstream cosine-like distance clustering."
- [other] Export of normalized domain-feature matrix: "Export the normalized domain-feature matrix and hit details to TSV output files."
- [readme] Rationale for l2-normalization in clustering: "Clustering now uses __cosine-like__ (via l2-normalization) distances (as in https://www.nature.com/articles/s41564-022-01110-2)"
