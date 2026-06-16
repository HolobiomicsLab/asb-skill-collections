---
name: nearest-neighbor-index-querying
description: Use when you have millions of MS/MS spectra to cluster and have already constructed nearest neighbor indexes (partitioned Voronoi diagrams of spectrum vectors bucketed by precursor m/z).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3696
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
---

# nearest-neighbor-index-querying

## Summary

Query pre-constructed nearest neighbor indexes to retrieve candidate similar spectra and compute a sparse pairwise distance matrix, avoiding exhaustive all-versus-all comparison of MS/MS spectra. This skill enables efficient clustering of millions of spectra by trading off recall for speed through controlled exploration of index cells.

## When to use

You have millions of MS/MS spectra to cluster and have already constructed nearest neighbor indexes (partitioned Voronoi diagrams of spectrum vectors bucketed by precursor m/z). You want to compute pairwise distances only between spectra that are likely to be similar, rather than comparing every spectrum to every other spectrum. Your goal is to feed a sparse distance matrix downstream to density-based clustering (e.g., DBSCAN).

## When NOT to use

- You have not yet constructed nearest neighbor indexes — you must first partition spectrum vectors into buckets and build inverted index structures.
- You need exact all-versus-all pairwise distances — this skill deliberately omits many pairs to achieve speed; if cluster purity requires exhaustive comparison, use dense distance matrices instead.
- Your spectrum vectors are high-resolution (not hashed/low-dimensional) — nearest neighbor indexing is designed for hashed vectors; indexing will be less efficient or inaccurate on original high-dimensional representations.

## Inputs

- Pre-constructed nearest neighbor indexes (Voronoi partitions with inverted index, bucketed by precursor m/z)
- Low-dimensional hashed spectrum vectors (feature-hashed from binned spectra)

## Outputs

- Sparse pairwise distance matrix (cosine distances between each spectrum and its nearest neighbors)
- Spectrum-to-neighbor pairs suitable for DBSCAN input

## How to apply

Load the pre-constructed nearest neighbor indexes and the low-dimensional hashed spectrum vectors from the indexing stage. For each spectrum vector, query the appropriate nearest neighbor index (selected by precursor m/z bucket) to retrieve candidate neighbors, controlling accuracy versus speed using the `n_probe` parameter (number of inverted index lists to inspect) and `n_neighbors_ann` (number of neighbors to return). Compute cosine distances only between each spectrum and its retrieved neighbors, building a sparse distance matrix. Export the result in a format suitable for DBSCAN clustering (e.g., a sparse matrix or coordinate list). The accuracy of this sparse matrix depends on how thoroughly you explore the index cells: fewer probes runs faster but risks missing true neighbors in high-dimensional space.

## Related tools

- **falcon** (Spectrum clustering tool that performs nearest neighbor index construction, querying, and downstream DBSCAN clustering in a unified pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum preprocessing, hashing, and vector manipulation before and during nearest neighbor operations)

## Examples

```
# Implicit in falcon CLI after index construction; example inspection in Python:
from falcon import load_index, compute_sparse_distance_matrix
index = load_index('spectrum_vectors.npy', precursor_mz=precursor_values)
sparse_distances = compute_sparse_distance_matrix(index, n_probe=20, n_neighbors_ann=50)
```

## Evaluation signals

- The sparse distance matrix contains only distances between spectrum pairs that were returned as neighbors by the index queries; verify no exhaustive pairs were computed.
- The number of neighbors per spectrum should match or exceed `n_neighbors` setting; if substantially lower, index queries were incomplete.
- Downstream DBSCAN clustering produces clusters with expected purity and count; if too many singletons or fragmented clusters, increase `n_probe` or `n_neighbors_ann` to explore more index cells.
- Sparse matrix sparsity (fraction of zero/missing entries) should be high (>>90%) for million-scale datasets; sparsity << 50% suggests over-querying and loss of speedup.
- Runtime should scale roughly linearly with number of spectra and logarithmically with number of neighbors queried, not quadratically as exhaustive comparison would.

## Limitations

- Query accuracy and cluster purity depend heavily on `n_probe` and `n_neighbors_ann` settings: too few probes risks missing true neighbors (false negatives), degrading clustering quality.
- Sparse distance matrix is approximate — it does not capture all pairwise distances, so clustering results may differ from an exhaustive approach. For metabolomics or top-down data with smaller mass ranges, the index partitioning by precursor m/z may be too coarse.
- Index construction and querying are bucketed by precursor m/z; spectra with very different precursor masses will never be compared, even if fragment patterns are similar. This is by design but may miss valid clusters at broad precursor tolerances.
- Low-dimensional hashing (feature hashing) conserves cosine similarity approximately but not exactly; hash collisions and dimension reduction introduce quantization error that compounds through the clustering pipeline.

## Evidence

- [other] Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold.: "Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold."
- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index.: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index."
- [readme] The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time.: "The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a"
- [readme] n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results.: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results."
