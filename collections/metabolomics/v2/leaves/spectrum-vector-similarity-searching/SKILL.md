---
name: spectrum-vector-similarity-searching
description: Use when when clustering large collections (thousands to millions) of
  tandem mass spectra and you need to compute a sparse pairwise distance matrix for
  density-based clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
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
- pip install falcon-ms spectrum-utils==0.3.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
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

# spectrum-vector-similarity-searching

## Summary

Efficiently retrieve k nearest neighbors for each spectrum vector using spatial indexing structures (k-d trees, LSH-based inverted indexes) to enable sparse pairwise distance computation without exhaustive all-vs-all comparisons. This skill is critical for scaling spectrum clustering to millions of MS/MS spectra.

## When to use

When clustering large collections (thousands to millions) of tandem mass spectra and you need to compute a sparse pairwise distance matrix for density-based clustering. Specifically, use this skill after spectrum vectors have been converted to low-dimensional representations via feature hashing, and you must avoid the O(n²) cost of comparing every spectrum to every other spectrum.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors via feature hashing; preprocessing is required first.
- Clustering dataset is small (< 1000 spectra) where exhaustive all-vs-all comparison is computationally acceptable.
- You require dense pairwise distance computation (all spectrum pairs) rather than sparse similarity; use exhaustive cosine distance instead.

## Inputs

- spectrum vectors (low-dimensional, hashed representations derived from binned high-resolution MS/MS spectra)
- precursor m/z values (for bucketing and nearest neighbor index construction)
- k parameter (number of nearest neighbors to retrieve per spectrum)

## Outputs

- sparse pairwise distance matrix (cosine distance between each spectrum and its k nearest neighbors)
- nearest neighbor index structure (Voronoi diagram with inverted index for future queries)

## How to apply

Construct nearest neighbor indexes from spectrum vectors by partitioning them into buckets (typically by precursor m/z) and building a Voronoi diagram with an inverted index structure. Query each spectrum vector against the index to retrieve its k nearest neighbors (controlled by `n_neighbors` and `n_probe` parameters). Compute pairwise distances only between each spectrum and its retrieved neighbors, storing results in sparse matrix format. The trade-off between speed and accuracy is governed by `n_probe` (number of inverted index lists to inspect) and `low_dim` (length of low-dimensional vectors); higher values increase accuracy at the cost of computation time.

## Related tools

- **falcon** (spectrum clustering tool that constructs and queries nearest neighbor indexes to compute sparse pairwise distance matrices and perform density-based clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils** (utility library for spectrum preprocessing and manipulation, integrated as a dependency for spectrum vector construction)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Sparse distance matrix is populated only for spectrum pairs within the retrieved k nearest neighbors; verify sparsity ratio matches expected density for chosen k and dataset size.
- Nearest neighbor index construction completes without error and memory usage scales with bucketed partitions rather than O(n²) full distance matrix.
- Cosine distances in sparse matrix fall within expected range [0, 2] and respect precursor m/z tolerance (`precursor_tol` constraint) when index was bucketed by precursor mass.
- Downstream density-based clustering (DBSCAN) produces cluster assignments that are stable under small changes to `eps` threshold, indicating the sparse distance matrix accurately captured spectrum similarity structure.
- Retrieved nearest neighbors have cosine similarity (1 - cosine_distance) that is consistent with true similarity; verify by spot-checking against exhaustive computation on a subset.

## Limitations

- Accuracy depends on exploration depth (`n_probe`): inspecting fewer inverted index lists runs faster but risks missing true nearest neighbors in high-dimensional space.
- Low-dimensional vector length (`low_dim`) trades off accuracy against memory and query speed; shorter vectors approximate true cosine distance less accurately.
- Performance is sensitive to bucketing strategy (e.g., by precursor m/z): poor bucket separation may lead to sparse index and missed neighbors.
- LSH-based indexes are probabilistic and may occasionally fail to retrieve a true nearest neighbor; increasing `n_probe` reduces but does not eliminate this risk.
- Settings are tuned for bottom-up proteomics data (minimum 5 peaks, 250 m/z range, 101–500 m/z window); metabolomics and top-down data may require adjusted preprocessing (`min_peaks`, `min_mz_range`, `scaling`).

## Evidence

- [intro] Nearest neighbor indexes enable sparse distance computation: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] Index construction from spectrum vectors via Voronoi partitioning: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index."
- [readme] Accuracy vs speed trade-off via probe and neighbor parameters: "The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a"
- [readme] n_probe and low_dim tuning guidance: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results. low_dim: The"
- [readme] Bucketing by precursor m/z for index construction: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison."
