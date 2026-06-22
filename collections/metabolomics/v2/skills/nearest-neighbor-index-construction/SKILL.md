---
name: nearest-neighbor-index-construction
description: Use when when you have millions of high-resolution MS/MS spectra converted to low-dimensional vectors (via feature hashing) and need to compute a sparse pairwise distance matrix for downstream density-based clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nearest-neighbor-index-construction

## Summary

Construct spatial indexes (e.g., inverted index with Voronoi partitioning) over low-dimensional spectrum vectors to enable fast similarity searching and sparse pairwise distance computation without exhaustive all-vs-all comparison. This skill accelerates large-scale MS/MS spectrum clustering by trading off memory and preprocessing cost for query-time efficiency.

## When to use

When you have millions of high-resolution MS/MS spectra converted to low-dimensional vectors (via feature hashing) and need to compute a sparse pairwise distance matrix for downstream density-based clustering. Specifically, use this skill when exhaustive all-vs-all spectrum comparison is computationally prohibitive (e.g., >100k spectra) and you can tolerate a small accuracy trade-off in exchange for dramatic runtime reduction.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors; feature hashing (or similar dimensionality reduction) must be applied first.
- Dataset is small (<10k spectra); exhaustive all-vs-all comparison may be faster and simpler than index construction overhead.
- You need exact all-vs-all pairwise distances; sparse indexing will miss some pairs, violating completeness requirements.

## Inputs

- low-dimensional spectrum vectors (output from feature hashing)
- precursor m/z values for each spectrum
- desired number of nearest neighbors (n_neighbors, n_neighbors_ann)
- maximum number of inverted index lists to probe (n_probe)

## Outputs

- sparse pairwise distance matrix
- nearest neighbor indexes (Voronoi-partitioned inverted index structure)
- list of k nearest neighbor spectra per query spectrum

## How to apply

First, bin and convert high-resolution spectra to low-dimensional vectors using feature hashing (e.g., MurmurHash3 to map mass bins to hash bins), which preserves cosine similarity while reducing dimensionality. Split vectors into buckets by precursor m/z to isolate spectra with similar masses. Within each bucket, partition vectors into data subspaces (Voronoi diagram) and assign all vectors to their nearest representative in an inverted index. During querying, retrieve the k nearest neighbors for each spectrum by inspecting up to n_probe lists in the inverted index (tuning n_probe controls the accuracy–speed trade-off). Compute pairwise distances only between each spectrum and its retrieved neighbors, storing results in sparse matrix format. Higher n_probe and n_neighbors values improve recall but increase search time; typical settings are n_neighbors=20, n_neighbors_ann=25, and n_probe adjusted based on dataset size and latency constraints.

## Related tools

- **falcon** (Performs nearest neighbor index construction and sparse distance matrix computation as part of end-to-end spectrum clustering pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Provides utilities for spectrum I/O, preprocessing, and cosine similarity computation used in conjunction with nearest neighbor indexing)

## Examples

```
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Sparse distance matrix contains only k nearest-neighbor distances per spectrum (verify sparsity by row count); confirm no exhaustive comparisons are stored.
- Cosine similarity between hashed vectors approximates true cosine similarity of original spectra; validate by sampling and comparing a subset of hashed vs. original pairs.
- Nearest neighbor indexes partition vectors into balanced Voronoi subspaces; inspect bucket sizes and inverted index load to confirm no extreme skew.
- Query times scale sublinearly with dataset size (O(log n) or O(n^0.5) rather than O(n)); benchmark runtime as dataset grows.
- Downstream DBSCAN clustering produces clusters with expected purity (single-peptide clusters) at configured eps threshold; compare cluster assignments against reference peptide IDs if available.

## Limitations

- Accuracy depends on n_probe and n_neighbors settings; inspecting fewer inverted index lists or considering fewer neighbors increases risk of missing true nearest neighbors in high-dimensional space.
- Feature hashing introduces quantization loss; cosine similarity of hashed vectors is an approximation that depends on hash table size (low_dim parameter) — larger vectors are more accurate but increase memory and query time.
- Precursor m/z bucketing assumes spectra with sufficiently different precursor masses are unlikely to be similar; violates this assumption if fragment patterns dominate and precursor masses are noisy or ambiguous.
- Method is optimized for bottom-up proteomics (MS/MS peptide spectra); spectrum preprocessing defaults (min_peaks=5, min_mz_range=250, m/z range 101–500) require adjustment for metabolomics or top-down data.

## Evidence

- [readme] Feature hashing approach and rationale: "High-resolution MS/MS spectra are converted to low-dimensional vectors using feature hashing. First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment"
- [readme] Voronoi partitioning and inverted index construction: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison. The spectrum vectors in each"
- [readme] Sparse distance matrix computation via neighbor retrieval: "A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the"
- [readme] Key parameter tuning for accuracy–speed trade-off: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results. n_neighbors and"
- [intro] Core finding on avoiding exhaustive comparison: "Nearest neighbor indexes are constructed from spectrum vectors and used to efficiently compute a sparse pairwise distance matrix by avoiding exhaustive all-vs-all spectrum comparisons."
