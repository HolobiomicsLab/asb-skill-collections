---
name: spectrum-vector-similarity-searching
description: Use when you have millions of MS/MS spectra represented as low-dimensional vectors (via feature hashing) and need to compute pairwise distances only between similar spectra rather than comparing every spectrum to every other spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
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

# Spectrum Vector Similarity Searching

## Summary

Use nearest neighbor indexes to efficiently retrieve candidate similar spectra for a query spectrum without exhaustive all-versus-all comparison. This skill enables fast similarity searching on low-dimensional hashed spectrum vectors, drastically reducing the computational cost of building sparse pairwise distance matrices for large-scale MS/MS clustering.

## When to use

Apply this skill when you have millions of MS/MS spectra represented as low-dimensional vectors (via feature hashing) and need to compute pairwise distances only between similar spectra rather than comparing every spectrum to every other spectrum. Typical trigger: clustering scale >100k spectra where exhaustive O(n²) comparison is prohibitively expensive, or when downstream analysis (e.g., density-based clustering) requires a sparse similarity graph.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors; use feature hashing or another vectorization step first.
- Nearest neighbor indexes have not been pre-constructed; you must build and partition the index before querying.
- Analysis requires exhaustive all-versus-all comparison (e.g., building a complete distance matrix); sparse searching will undercount true neighbors and bias downstream clustering.

## Inputs

- Nearest neighbor indexes (Voronoi-partitioned inverted index structure, indexed by precursor m/z bucket)
- Low-dimensional spectrum vectors (feature-hashed representations)
- Query spectrum vector(s) with known precursor m/z

## Outputs

- Sparse pairwise distance matrix (query spectrum ID vs. candidate neighbor IDs and their cosine distances)
- List of retrieved nearest neighbors per query spectrum (with similarity scores)

## How to apply

First, load pre-constructed nearest neighbor indexes that partition spectrum vectors into buckets by precursor m/z and assign each vector to Voronoi cells via an inverted index structure. For each query spectrum vector, probe the nearest neighbor index by inspecting a configurable number of neighboring cells (controlled by `n_probe` parameter) to retrieve the k nearest neighbors within a user-defined distance threshold (e.g., cosine distance < 0.10–0.15 for peptide clustering). Compute the actual cosine distances only between the query and its retrieved candidates, not against all spectra. Tune the trade-off between speed and recall by adjusting `n_probe` (fewer lists = faster but risk missing true neighbors) and `n_neighbors_ann` (number of candidate neighbors to evaluate). The result is a sparse pairwise distance matrix suitable for input to DBSCAN or other density-based clustering algorithms.

## Related tools

- **falcon** (Command-line tool that implements nearest neighbor indexing, querying, and sparse distance matrix construction for spectrum clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum I/O and preprocessing (version 0.3.5 or compatible) used alongside falcon)

## Examples

```
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10 --n_probe 10 --n_neighbors 20
```

## Evaluation signals

- Sparse distance matrix contains only non-zero distances between query spectra and their retrieved neighbors; all other entries are absent or zero, reducing memory footprint by orders of magnitude compared to dense matrices.
- Neighbor retrieval is consistent with precursor m/z bucketing: queries return candidates whose precursor m/z differs by ≤ the specified tolerance (e.g., 20 ppm).
- Recall metric: percentage of true neighbors (by cosine similarity threshold) actually retrieved should be ≥ 95–99% depending on `n_probe` and `n_neighbors_ann` settings; lower recall indicates insufficient probe depth.
- Downstream clustering purity: spectra clustered together should have cosine distance ≤ eps threshold (e.g., 0.10–0.15) and represent the same peptide; clusters should not contain mixed peptides (evaluate against reference annotations if available).
- Runtime scales linearly or near-linearly with number of spectra, not quadratically; if wall-clock time grows as O(n²), the sparse index is not being used correctly.

## Limitations

- Accuracy and speed are governed by `n_probe`: inspecting fewer lists reduces computation time but increases risk of missing true neighbors in high-dimensional space, leading to fragmentation of clusters.
- Nearest neighbor index construction itself requires upfront cost; for small datasets (<100k spectra) exhaustive comparison may be faster than indexing overhead.
- Performance depends critically on the quality of low-dimensional vector representation (via feature hashing); poor hashing can cause high-dimensional neighbors to collide spuriously, degrading clustering recall.
- The sparse matrix construction is most effective when spectrum similarity is truly sparse (i.e., most spectra are dissimilar); highly uniform datasets may not benefit from the sparse approach.

## Evidence

- [intro] Nearest neighbor indexes enable efficient computation without exhaustive comparison: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [other] Workflow: query indexes, retrieve candidates, compute distances only for neighbors: "Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold. Compute pairwise distances only between each spectrum"
- [readme] Vectors partitioned by Voronoi diagram and inverted index for fast searching: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index."
- [readme] n_probe parameter controls speed vs accuracy trade-off: "The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a"
- [readme] Tunable parameters for nearest neighbor indexing: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results. n_neighbors and"
