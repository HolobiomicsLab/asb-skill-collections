---
name: ms-ms-spectrum-pairwise-comparison
description: Use when you have millions of MS/MS spectra in mzML, mzXML, or MGF format
  that have been converted to low-dimensional vectors via feature hashing, and you
  need to identify which spectra are similar enough to cluster together.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - LC-MS
  license_tier: open
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

# MS/MS Spectrum Pairwise Comparison via Nearest Neighbor Indexing

## Summary

Use nearest neighbor indexes to efficiently compute pairwise distances between MS/MS spectra without exhaustive all-versus-all comparison. This skill enables sparse distance matrix construction for large-scale spectrum clustering by querying pre-built indexes rather than computing distances for every spectrum pair.

## When to use

You have millions of MS/MS spectra in mzML, mzXML, or MGF format that have been converted to low-dimensional vectors via feature hashing, and you need to identify which spectra are similar enough to cluster together. The input spectra have been indexed by precursor m/z, and you want to avoid the O(n²) cost of comparing every spectrum to every other spectrum.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors or indexed; use the feature hashing and nearest neighbor indexing stages first.
- You require exhaustive all-versus-all distance computation (e.g., for validation or when spectrum count is small enough that O(n²) is acceptable) rather than a sparse approximation.
- Input spectra are in their native high-resolution form rather than as pre-indexed, low-dimensional vectors; preprocessing and indexing must precede this skill.

## Inputs

- Pre-constructed nearest neighbor indexes (Voronoi-partitioned, inverted index structure, organized by precursor m/z bucket)
- Low-dimensional spectrum vectors (feature-hashed representation from preceding step)
- Configuration parameters: n_probe, n_neighbors, n_neighbors_ann, distance threshold (eps)

## Outputs

- Sparse pairwise distance matrix (spectrum pairs and their cosine distances)
- Index of neighbor relationships suitable for density-based clustering (DBSCAN input)

## How to apply

Load the pre-constructed nearest neighbor indexes (partitioned by precursor m/z into Voronoi subspaces with inverted index lookup) and the corresponding low-dimensional spectrum vectors from the preceding indexing stage. For each query spectrum vector, probe the nearest neighbor index with a configurable n_probe parameter (number of inverted index lists to inspect) to retrieve the k nearest neighbors within a user-defined distance threshold. Compute pairwise cosine distances only between the query spectrum and its retrieved neighbors, accumulating results into a sparse distance matrix. The sparsity and accuracy trade-off is governed by n_probe (fewer probes = faster but potentially missed neighbors) and n_neighbors_ann (the number of candidate neighbors to evaluate during search). Export the resulting sparse distance matrix in a format compatible with downstream density-based clustering (e.g., DBSCAN).

## Related tools

- **falcon** (Spectrum clustering tool that implements nearest neighbor indexing and sparse pairwise distance matrix computation as part of its full pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum I/O and manipulation; version 0.3.5 is a dependency for falcon and handles mzML/mzXML/MGF parsing)

## Examples

```
# In falcon, this skill is embedded in the main clustering workflow; nearest neighbor querying and sparse distance matrix computation occur during execution. Command-line example:
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10 --n_probe 50 --n_neighbors 50
```

## Evaluation signals

- Sparse distance matrix contains only spectrum pairs where at least one spectrum was retrieved as a neighbor; no entries for distant spectrum pairs (validates sparsity and that index queries were performed correctly)
- Cosine distance values between retrieved neighbors fall within the user-specified threshold (eps parameter, typically 0.05–0.30); values outside this range indicate query or distance computation errors
- Row/column counts in the sparse matrix match the number of input spectra; every spectrum should have at least one neighbor entry (or zero if truly isolated, depending on eps and n_probe settings)
- Downstream density-based clustering (DBSCAN) produces cluster assignments; cluster quality can be assessed by comparing cluster compositions (e.g., verifying that spectra within a cluster correspond to a single peptide or compound)
- Matrix is symmetric or nearly symmetric (distance(A,B) ≈ distance(B,A)) if computed from bidirectional nearest neighbor queries; asymmetry may indicate index retrieval or distance computation bugs

## Limitations

- Accuracy of neighbor retrieval depends critically on n_probe; too few probes risk missing true neighbors in high-dimensional space, leading to underclustering or fragmented clusters.
- The method assumes spectra have been binned, feature-hashed, and indexed beforehand; raw spectra or spectra in non-indexed formats cannot be queried directly.
- Cluster purity (i.e., whether all spectra in a cluster correspond to the same peptide/compound) is sensitive to the eps threshold and spectrum preprocessing settings (min_peaks, min_mz_range, scaling); poor parameter choices can yield heterogeneous clusters despite correct pairwise distances.
- The method is optimized for bottom-up proteomics by default; metabolomics or top-down data require adjustment of min_peaks, min_mz_range, and other preprocessing parameters, which may affect index quality and neighbor retrieval.
- Memory and I/O overhead can be significant for millions of spectra; large datasets may require distributed or streaming implementations not covered in the base falcon tool.

## Evidence

- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [other] Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold.: "Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold."
- [readme] A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time.: "A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the"
- [readme] The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index.: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index."
- [readme] n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results.: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results."
