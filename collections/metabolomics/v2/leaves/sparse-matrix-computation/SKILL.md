---
name: sparse-matrix-computation
description: Use when clustering large collections of high-resolution MS/MS spectra
  (thousands to millions) and you have already converted spectra to low-dimensional
  vectors via feature hashing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
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

# Reconstruct nearest-neighbor index construction and sparse pairwise distance computation

## Summary

This skill constructs spatial indexes (k-d trees or LSH-based inverted indexes) from low-dimensional spectrum vectors and queries them to compute a sparse pairwise distance matrix, avoiding exhaustive all-vs-all comparisons. It is essential for scaling similarity clustering to millions of MS/MS spectra by reducing computational complexity from O(n²) to O(n·k) where k is the number of neighbors queried per spectrum.

## When to use

Apply this skill when clustering large collections of high-resolution MS/MS spectra (thousands to millions) and you have already converted spectra to low-dimensional vectors via feature hashing. Use it specifically when an exhaustive all-vs-all distance matrix is computationally prohibitive or when density-based clustering (e.g. DBSCAN) requires only local neighborhood information rather than global pairwise distances.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors; apply feature hashing first.
- Dataset size is small enough (<10k spectra) that an exhaustive all-vs-all distance matrix fits in memory and computation time is acceptable.
- You need the complete pairwise distance matrix for downstream analyses (e.g., hierarchical clustering, multi-dimensional scaling) that require dense distance information rather than sparse neighborhoods.

## Inputs

- Low-dimensional spectrum vectors (output from feature hashing; typically dense numpy arrays or scipy sparse matrices)
- Precursor m/z values for each spectrum (to enable bucketing)
- Spectrum comparison parameters (precursor_tol in ppm or Da, fragment_tol in Da)

## Outputs

- Sparse pairwise distance matrix in COO or CSR format, with shape (n_spectra, n_spectra)
- Index mapping from sparse matrix coordinates to original spectrum identifiers

## How to apply

Load the pre-computed low-dimensional spectrum vectors (output from feature hashing) as input. Partition the vectors by precursor m/z to create buckets, then construct a nearest neighbor index within each bucket using an inverted index based on Voronoi partitioning. Query each spectrum vector against its index to retrieve the k nearest neighbors (controlled by n_neighbors and n_probe parameters). Compute pairwise cosine distances only between each spectrum and its retrieved neighbors, storing results in sparse matrix format (e.g., COO or CSR). The accuracy of the sparse matrix depends on the n_probe parameter: inspecting more inverted index lists increases recall but increases runtime. The n_neighbors_ann parameter controls the breadth of the approximate nearest neighbor search and should be ≥ n_neighbors to preserve accuracy.

## Related tools

- **falcon** (Spectrum clustering tool that implements the complete pipeline including nearest neighbor index construction, sparse distance matrix computation, and DBSCAN clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum preprocessing and representation (required dependency for falcon))

## Examples

```
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10 --n_probe 10 --n_neighbors 50
```

## Evaluation signals

- Sparse matrix has correct shape (n_spectra, n_spectra) and contains only non-zero distances for nearest neighbor pairs.
- Number of non-zero entries per row approximately equals n_neighbors (within statistical variance due to tied distances or boundary effects).
- Downstream DBSCAN clustering produces clusters with high purity (spectra in each cluster correspond to a single peptide) as validated by comparing cluster assignments to reference peptide identities.
- Memory usage and runtime scale approximately linearly or sub-quadratically with the number of spectra (no O(n²) blowup).
- Cosine distances in the sparse matrix fall within expected range [0, 1] with distribution skewed toward low values (most neighbors are similar).

## Limitations

- Accuracy of sparse matrix depends on the n_probe parameter: inspecting fewer inverted index lists runs faster but misses some true nearest neighbors, potentially creating fragmented clusters.
- The sparse matrix approximates but does not guarantee that all true k-nearest neighbors are retrieved; some neighbors with cosine distance just above the threshold may be missed due to the Voronoi partitioning strategy.
- Performance is sensitive to the precursor m/z bucketing strategy; overlapping mass ranges or biased bucket populations can degrade index quality.
- The method assumes spectrum vectors preserve cosine similarity from the original high-resolution spectra after feature hashing; loss of information in the hashing step propagates to the distance matrix.

## Evidence

- [intro] Construction of nearest neighbor indexes from spectrum vectors: "the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching"
- [intro] Sparse matrix computation via neighbor queries: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other"
- [readme] Voronoi partitioning and inverted index method: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index"
- [readme] n_probe parameter trade-off: "The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a"
- [readme] Precursor m/z bucketing strategy: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes"
- [readme] n_neighbors parameter control: "n_neighbors and n_neighbors_ann: The final number of neighbors to consider for each spectrum and during nearest neighbor searching. Querying less neighbors will run faster but will give slightly less"
