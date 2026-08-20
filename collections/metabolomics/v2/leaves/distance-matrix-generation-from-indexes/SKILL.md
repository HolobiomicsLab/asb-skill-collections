---
name: distance-matrix-generation-from-indexes
description: Use when you have pre-computed feature-hashed spectrum vectors and nearest
  neighbor indexes constructed from those vectors, and you need a pairwise distance
  matrix as input to density-based clustering (e.g., DBSCAN).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3071
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

# distance-matrix-generation-from-indexes

## Summary

Generate a sparse pairwise distance matrix by querying nearest neighbor indexes for each spectrum vector, computing distances only between each spectrum and its retrieved k nearest neighbors rather than exhaustively comparing all spectra. This enables scalable clustering of millions of MS/MS spectra by reducing the computational burden from O(n²) all-vs-all comparisons to O(n·k) sparse comparisons.

## When to use

You have pre-computed feature-hashed spectrum vectors and nearest neighbor indexes constructed from those vectors, and you need a pairwise distance matrix as input to density-based clustering (e.g., DBSCAN). Use this skill when you aim to cluster large MS/MS datasets (thousands to millions of spectra) and cannot afford exhaustive all-vs-all cosine similarity computation.

## When NOT to use

- Input spectra are already clustered or assigned to groups — distance matrix generation is redundant.
- You have fewer than ~1000 spectra and can afford O(n²) all-vs-all comparisons without performance concerns.
- Nearest neighbor indexes have not been constructed (e.g., you have only raw spectrum vectors) — construct indexes first using feature hashing and spatial partitioning.

## Inputs

- feature-hashed spectrum vectors (low-dimensional numeric array, typically from binned high-resolution m/z spectra)
- nearest neighbor indexes constructed from spectrum vectors (spatial/inverted index structure partitioned by precursor m/z)

## Outputs

- sparse pairwise distance matrix (COO, CSR, or similar sparse format; rows and columns indexed by spectrum ID)
- distance values (typically cosine distances in range [0, 1] or [0, 2])

## How to apply

For each spectrum vector in the dataset, query its corresponding nearest neighbor index to retrieve the k most similar candidate neighbors (controlled by parameters like `n_probe` for inverted index lists to inspect and `n_neighbors_ann` for maximum neighbors during searching). Compute the cosine distance (or other metric) only between that spectrum and each retrieved neighbor. Store these pairwise distances in sparse matrix format (e.g., COO or CSR) rather than a dense n×n matrix. The sparsity is governed by the number of neighbors retrieved: larger `n_neighbors` and `n_probe` values yield denser matrices with higher recall but longer computation time; smaller values prioritize speed at the risk of missing true nearest neighbors in high-dimensional space. Return the sparse distance matrix for downstream DBSCAN clustering with the `eps` threshold set according to your data characteristics (typically 0.05–0.15 for proteomics, adjustable up to 0.30 for aggressive clustering).

## Related tools

- **falcon** (spectrum clustering tool that constructs nearest neighbor indexes and uses them to compute sparse distance matrices for MS/MS clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils** (utility library for spectrum processing and comparison, required dependency for falcon distance computation)

## Examples

```
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10 --n_neighbors 50 --n_probe 100
```

## Evaluation signals

- Sparse matrix has correct dimensions (n_spectra × n_spectra) with density ≈ k/n where k is mean neighbors per spectrum; verify via matrix shape and nnz() count.
- All distance values fall within expected range [0, 1] for normalized cosine distance or [0, 2] for unnormalized; check min/max and histogram of nonzero entries.
- Sparse matrix is symmetric (d[i,j] ≈ d[j,i]) when computed from reciprocal neighbors; spot-check symmetry on random pairs.
- Downstream DBSCAN clustering with appropriate `eps` threshold (0.05–0.15 for typical proteomics) yields reasonable cluster sizes and purity (clusters contain spectra of single peptide/compound); validate against known ground truth or manual inspection if available.
- Computation time scales approximately linearly with spectrum count (O(n·k)) rather than quadratically; profile runtime and confirm it is orders of magnitude faster than all-vs-all comparison on the same dataset.

## Limitations

- Sparse matrix construction is approximate: if `n_probe` or `n_neighbors_ann` are too small, true nearest neighbors may be missed, leading to fragmented clusters or false negatives in downstream clustering.
- Performance depends critically on quality of the nearest neighbor index; poorly constructed or low-dimensional feature hashing may cause the index to scatter similar spectra across distant cells, reducing recall.
- The method assumes that the nearest neighbor index has been partitioned by precursor m/z, which may not be optimal for all mass spectrometry datasets (e.g., when precursor mass tolerance is very large or data spans multiple charge states).
- Parameter tuning (especially `n_probe`, `n_neighbors`, and `eps`) is empirical and data-dependent; recommended values (0.05–0.15 for `eps`, default `n_probe`) are intended for bottom-up proteomics and may need adjustment for metabolomics or top-down data.

## Evidence

- [intro] nearest neighbor indexes enable computation of sparse pairwise distance matrix: "Nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] workflow for constructing and querying nearest neighbor indexes: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison. The spectrum vectors in each"
- [readme] sparse distance matrix computation via index queries: "A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the"
- [readme] input vectors are feature-hashed spectra: "High-resolution MS/MS spectra are converted to low-dimensional vectors using feature hashing. First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment"
- [readme] parameter tuning for data type: "The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in falcon. Values between 0.05 and 0.15 will typically generate a"
- [readme] nearest neighbor index parameter effects: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results."
