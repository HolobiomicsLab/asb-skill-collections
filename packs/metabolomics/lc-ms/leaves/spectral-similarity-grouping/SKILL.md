---
name: spectral-similarity-grouping
description: Use when when you have computed a sparse pairwise distance matrix from nearest neighbor indexes of high-resolution MS/MS spectra and need to partition them into clusters such that spectra within each cluster correspond to similar fragmentation patterns (e.g., same peptide or metabolite).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - DBSCAN
  - spectrum-utils
  techniques:
  - LC-MS
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
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

# spectral-similarity-grouping

## Summary

Density-based clustering of mass spectra using a sparse pairwise distance matrix to partition similar MS/MS spectra into homogeneous groups. This skill is applied as the final step of the falcon pipeline to assign cluster membership based on cosine similarity thresholds and neighborhood density.

## When to use

When you have computed a sparse pairwise distance matrix from nearest neighbor indexes of high-resolution MS/MS spectra and need to partition them into clusters such that spectra within each cluster correspond to similar fragmentation patterns (e.g., same peptide or metabolite). This is appropriate after nearest neighbor indexing has been completed and you wish to group spectra with cosine similarity above a configurable threshold.

## When NOT to use

- Input is a dense all-vs-all distance matrix from exhaustive pairwise comparison; use sparse indexing first to avoid quadratic memory and time complexity.
- Spectra have not been preprocessed (binned, hashed to low-dimensional vectors, or indexed); apply feature hashing and nearest neighbor indexing before clustering.
- The goal is to find peptide sequences rather than to group spectra by similarity; clustering groups spectra, not sequences.

## Inputs

- Sparse pairwise distance matrix (condensed distance matrix or sparse CSR format)
- Spectrum identifiers corresponding to rows/columns of the distance matrix
- Clustering parameters (eps threshold, minimum samples per cluster)

## Outputs

- Cluster assignment table (spectrum ID → cluster ID mapping)
- Cluster summary statistics (cluster sizes, number of clusters)
- Optional: representative spectra per cluster (exported to MGF format)

## How to apply

Load the sparse pairwise distance matrix (in condensed or sparse CSR format) computed from the preceding nearest neighbor indexing step. Apply density-based clustering—typically DBSCAN—using the maximum cosine distance parameter (eps) as the neighborhood radius; values between 0.05 and 0.15 typically yield pure clusters (one peptide per cluster), while values up to 0.30 enable more aggressive clustering. The algorithm identifies spectra that are close to each other in the high-dimensional space and form dense subspaces, assigning each spectrum a cluster ID (or label for noise points). Output a mapping of spectrum identifiers to cluster IDs and compute summary statistics such as cluster sizes and total number of clusters formed.

## Related tools

- **falcon** (End-to-end MS/MS spectrum clustering pipeline that integrates feature hashing, nearest neighbor indexing, sparse distance matrix computation, and density-based clustering as its final step) — https://github.com/bittremieux/falcon
- **DBSCAN** (Density-based clustering algorithm applied by falcon to partition spectra into clusters based on the sparse distance matrix and eps threshold)
- **spectrum-utils** (Utility library for spectrum handling and preprocessing, installed as a dependency of falcon)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- All spectra are assigned a cluster ID or marked as noise; no spectrum is left unclassified.
- Cluster sizes are reasonable (not dominated by a single cluster or fragmented into singletons); summary statistics reflect the eps and min_samples parameters used.
- Spot-check: inspect a few representative spectra per cluster and verify they exhibit similar fragmentation patterns (high cosine similarity).
- Output file format is correct: comma-separated table with spectrum identifier and cluster label on each line, matching input spectrum count.
- DBSCAN hyperparameters (eps, min_samples) are documented and justified based on expected cluster purity (peptide homogeneity) and data characteristics (proteomics vs. metabolomics).

## Limitations

- Clustering quality depends critically on the eps threshold; values must be tuned per dataset. Values between 0.05–0.15 are recommended for proteomics, but metabolomics or top-down proteomics data may require different thresholds.
- DBSCAN does not guarantee that all spectra are clustered; outlier spectra with few neighbors are marked as noise rather than assigned to a cluster, which may inflate the apparent number of clusters.
- The sparse distance matrix captures only nearest neighbors, so two spectra separated by more than the k-nearest neighbors are unlikely to be directly compared; global clustering structure may be lost if the nearest neighbor index is too sparse (low n_neighbors or n_probe settings).
- Spectrum preprocessing (min_peaks, min_mz_range, m/z bounds, peak intensity scaling) must be appropriate for the data type; default settings are tuned for bottom-up proteomics and may produce poor results for metabolomics or top-down data without adjustment.

## Evidence

- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [intro] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense"
- [readme] eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to only a single peptide). The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in falcon. Values between 0.05 and 0.15 will typically generate a pure clustering result.: "eps: The maximum cosine distance between two spectra for them to be considered as neighbors. Values between 0.05 and 0.15 will typically generate a pure clustering result."
- [readme] falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10: "This will cluster all MS/MS spectra in mzML files in the `peak` directory with the specified settings and write (i) the cluster assignments to the `falcon.csv` file, and (ii) the cluster"
