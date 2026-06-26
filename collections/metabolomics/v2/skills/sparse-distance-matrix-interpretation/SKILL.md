---
name: sparse-distance-matrix-interpretation
description: Use when you have computed a sparse pairwise distance matrix from nearest
  neighbor indexes (containing only cosine distances between neighboring spectra,
  not exhaustive pairwise comparisons) and need to partition spectra into groups of
  similar ions or peptides.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - Python 3.8+
  - spectrum-utils
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sparse-distance-matrix-interpretation

## Summary

Interpret and apply density-based clustering to a sparse pairwise distance matrix computed from nearest neighbor indexes to group similar MS/MS spectra into clusters. This skill bridges the transition from similarity searching to final cluster assignment in high-throughput spectrum analysis.

## When to use

You have computed a sparse pairwise distance matrix from nearest neighbor indexes (containing only cosine distances between neighboring spectra, not exhaustive pairwise comparisons) and need to partition spectra into groups of similar ions or peptides. Use this skill when processing millions of MS/MS spectra where exhaustive pairwise comparisons are computationally prohibitive, and you want to identify clusters of spectra with cosine similarity above a defined threshold while maintaining cluster purity (spectra in each cluster correspond to a single peptide/compound).

## When NOT to use

- Input is a dense pairwise distance matrix or full exhaustive comparison — use sparse-distance-matrix-interpretation only if the matrix is sparse and computed from nearest neighbor indexes.
- Spectra have not been preprocessed (binned, hashed to low-dimensional vectors, and indexed) — apply earlier falcon steps first.
- You require hierarchical tree output or dendrogram visualization rather than flat cluster labels — DBSCAN does not produce hierarchical structure.

## Inputs

- Sparse pairwise distance matrix (condensed distance matrix or sparse CSR format)
- Nearest neighbor indexes from preceding step
- Spectrum identifiers or scan numbers

## Outputs

- Cluster assignments table (spectrum ID to cluster ID mapping)
- Cluster summary statistics (cluster sizes, number of clusters)
- Optionally: representative spectra per cluster (in MGF format)

## How to apply

Load the sparse distance matrix (in condensed or sparse CSR format) computed from nearest neighbor indexes in the preceding falcon pipeline step. Apply DBSCAN density-based clustering using the sparse matrix and tune the `eps` parameter (maximum cosine distance for neighbor pairs) to control cluster purity; values between 0.05 and 0.15 typically yield pure clustering for proteomics data, while 0.05–0.30 range supports more aggressive clustering for other applications. The algorithm identifies spectra that form dense subspaces and assigns each spectrum a cluster ID or label. Output cluster assignments as a table mapping spectrum identifiers (or scan numbers) to cluster IDs, and compute summary statistics including cluster sizes and total number of clusters formed to validate clustering quality.

## Related tools

- **falcon** (Primary tool implementing density-based clustering (DBSCAN) on sparse distance matrices for spectrum clustering) — https://github.com/bittremieux/falcon
- **Python 3.8+** (Runtime environment required for falcon execution)
- **spectrum-utils** (Supporting library for spectrum I/O and manipulation (version 0.3.5 specified))

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Cluster assignments are complete (every spectrum in input is assigned to exactly one cluster ID or marked as noise)
- Cluster sizes follow expected distribution for your domain (e.g., no singleton clusters if `eps` is too stringent, no enormous clusters if `eps` is too permissive)
- Summary statistics are internally consistent (total spectrum count equals sum of all cluster sizes plus noise points)
- Spot-check representative spectra from a few clusters and verify via manual inspection or cross-reference that spectra within clusters have cosine similarity ≥ (1 − eps) and correspond to the same peptide/compound
- Cluster purity metric (if ground truth available): fraction of spectra in each cluster that share the same true label (target > 0.95 for proteomics with eps=0.05–0.15)

## Limitations

- DBSCAN cluster quality depends critically on `eps` parameter tuning; ideal value is data-dependent and varies with spectrum preprocessing choices (scaling, bin width, feature hashing), so cross-validation or manual tuning is often required.
- Spectra that do not belong to any dense region are labeled as noise and not assigned to clusters, which may be desirable for outlier removal but can result in loss of valid spectra.
- The sparse distance matrix must be accurately computed from nearest neighbor indexes in the preceding step; errors or insufficient nearest neighbor exploration will propagate and degrade clustering accuracy.
- Clustering performance assumes spectra have been properly preprocessed (binning, feature hashing, low-dimensional vectorization); unpreprocessed or poorly preprocessed spectra will yield poor clustering results.

## Evidence

- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [readme] The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters."
- [readme] `eps`: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to only a single peptide). The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in _falcon_. Values between 0.05 and 0.15 will typically generate a pure clustering result.: "Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used."
- [readme] _falcon_ takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line.: "_falcon_ takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line."
- [other] Apply density-based clustering (e.g., DBSCAN or hierarchical clustering) using the sparse distance matrix to partition spectra into groups, with cluster membership encoded by cluster ID or label.: "Apply density-based clustering (e.g., DBSCAN or hierarchical clustering) using the sparse distance matrix to partition spectra into groups, with cluster membership encoded by cluster ID or label."
