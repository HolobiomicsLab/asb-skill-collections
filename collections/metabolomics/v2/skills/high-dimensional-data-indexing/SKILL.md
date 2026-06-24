---
name: high-dimensional-data-indexing
description: Use when when you have millions of high-dimensional objects (e.g., MS/MS
  spectra converted to feature-hashed vectors) and need to compute pairwise similarities
  or retrieve nearest neighbors efficiently.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - LC-MS
  license_tier: restricted
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
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
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

# high-dimensional-data-indexing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct nearest neighbor indexes from low-dimensional vector representations to enable efficient similarity searching and sparse pairwise distance computation without exhaustive comparisons. Essential for scaling clustering and retrieval tasks to millions of high-dimensional spectra.

## When to use

When you have millions of high-dimensional objects (e.g., MS/MS spectra converted to feature-hashed vectors) and need to compute pairwise similarities or retrieve nearest neighbors efficiently. Specifically: after converting high-resolution spectra to low-dimensional vectors via feature hashing, before density-based clustering or distance matrix computation, when exhaustive pairwise comparison is computationally infeasible.

## When NOT to use

- Input vectors are already sparse or categorical (e.g., discrete molecular fingerprints); use approximate nearest neighbor methods designed for discrete spaces.
- Data size is small (< 100k spectra) or compute budget is generous; exhaustive pairwise comparison may be simpler and faster.
- You require exact nearest neighbors under all circumstances; LSH-based indexing is approximate and may skip true neighbors if n_probe or n_neighbors_ann are set too low.

## Inputs

- Low-dimensional spectrum vectors (feature-hashed binned spectra, typically 1000–10000 dimensions per spectrum)
- Bucket assignment keys (e.g., precursor m/z values for stratification)
- Candidate neighbor count and search parameters (n_neighbors, n_neighbors_ann, n_probe)

## Outputs

- Serialized nearest neighbor index (inverted index structure with Voronoi partitions per bucket)
- Sparse pairwise distance matrix (computed via nearest neighbor lookups, not exhaustive comparison)
- Neighbor lists for each spectrum (k nearest neighbors with distances)

## How to apply

Load preprocessed spectrum vectors (low-dimensional representations produced by feature hashing of binned spectra, typically 1000–10000 dimensions). Partition vectors into buckets by a covariate (e.g., precursor m/z) to reduce index size and search complexity. Build a nearest neighbor index by partitioning each bucket into data subspaces using a Voronoi diagram and constructing an inverted index of representative vectors. Tune the `n_probe` parameter (number of inverted index lists to inspect during query; typical range 5–50) and `n_neighbors_ann` (number of candidates returned per query) to balance search speed versus recall accuracy. Serialize the index and per-bucket metadata to disk for fast downstream retrieval. Query the index by retrieving the k nearest neighbors for each spectrum vector without computing the full pairwise distance matrix.

## Related tools

- **falcon** (Spectrum clustering tool that implements the full pipeline including nearest neighbor index construction and querying for MS/MS spectrum clustering.) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum preprocessing and I/O (mzML, mzXML, MGF formats) prior to feature hashing and indexing.)

## Examples

```
# After feature hashing spectra to low-dimensional vectors, build and query index via falcon:
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10 --n_probe 10 --n_neighbors_ann 50 --low_dim 10000
```

## Evaluation signals

- Index construction completes without memory errors on the target spectrum count; index file size is reasonable (typically < 2× input vector size).
- Query latency per spectrum is orders of magnitude faster than exhaustive comparison (e.g., milliseconds vs. seconds for millions of spectra).
- Nearest neighbor recall at rank k matches expected values for the chosen n_probe and n_neighbors_ann; spot-check via small test set with known neighbors.
- Sparse pairwise distance matrix has expected sparsity (typically 0.01–0.1% density); density-based clustering (DBSCAN) on the resulting distances produces pure clusters (single peptide per cluster) with the chosen eps threshold.
- Index is reproducible: querying the same vector twice returns identical neighbor sets and distances.

## Limitations

- Approximate method: not all true nearest neighbors are guaranteed to be returned if n_probe or n_neighbors_ann are too small; false negatives increase with aggressive parameter tuning.
- Bucketization by precursor m/z (or other covariate) introduces a hard boundary; neighbors just outside the bucket are never returned, potentially causing missed spectrum matches near bucket edges.
- Feature hashing conserves cosine similarity between hashed vectors but introduces collisions; collision frequency increases with lower dimensionality (low_dim parameter). Values < 1000 may degrade accuracy.
- Index construction assumes vectors fit in memory during partitioning; very large datasets (> 100M spectra) may require external-memory or streaming variants.
- Performance is sensitive to vector quality; poor feature hashing or noisy binning will yield poor nearest neighbor results regardless of index parameters.

## Evidence

- [other] Spectrum vectors are used to construct nearest neighbor indexes that enable efficient computation of sparse pairwise distance matrices without exhaustively comparing all spectra to each other.: "Spectrum vectors are used to construct nearest neighbor indexes that enable efficient computation of sparse pairwise distance matrices without exhaustively comparing all spectra to each other."
- [readme] First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing. Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching.: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing. Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity"
- [readme] Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison. The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index.: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison. The spectrum vectors in each"
- [readme] The settings for nearest neighbor indexing can be modified to tune clustering time versus accuracy. Changing these settings is only recommended for advanced users. n_probe: The maximum number of lists in the inverted index to inspect during querying.: "The settings for nearest neighbor indexing can be modified to tune clustering time versus accuracy. n_probe: The maximum number of lists in the inverted index to inspect during querying."
- [readme] n_neighbors and n_neighbors_ann: The final number of neighbors to consider for each spectrum and during nearest neighbor searching. Querying less neighbors will run faster but will give slightly less accurate clustering results.: "n_neighbors and n_neighbors_ann: The final number of neighbors to consider for each spectrum and during nearest neighbor searching. Querying less neighbors will run faster but will give slightly less"
- [readme] This feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra.: "This feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra."
- [readme] low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest neighbor searching and memory requirements.: "low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest"
