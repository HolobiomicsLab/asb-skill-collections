---
name: sparse-distance-matrix-construction
description: Use when you have a large collection of MS/MS spectra (hundreds of thousands
  to millions) that need to be clustered, you have already constructed nearest neighbor
  indexes on low-dimensional spectrum vectors (via feature hashing), and you need
  to compute only the relevant pairwise distances between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# Sparse Pairwise Distance Matrix Construction via Nearest Neighbor Indexing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill constructs a sparse pairwise distance matrix for large MS/MS spectrum datasets by querying pre-built nearest neighbor indexes, avoiding exhaustive all-versus-all comparison. It is essential for scaling density-based clustering to millions of spectra without prohibitive computational cost.

## When to use

Use this skill when you have a large collection of MS/MS spectra (hundreds of thousands to millions) that need to be clustered, you have already constructed nearest neighbor indexes on low-dimensional spectrum vectors (via feature hashing), and you need to compute only the relevant pairwise distances between spectra that are likely similar (within a precursor m/z bucket and a distance threshold) rather than comparing every spectrum to every other.

## When NOT to use

- Input spectra have not yet been converted to low-dimensional vectors via feature hashing; the indexing stage must precede this skill.
- Nearest neighbor indexes have not been constructed; this skill requires pre-indexed data, not raw spectra.
- The analysis goal requires all pairwise distances (e.g., full hierarchical clustering or all-vs-all comparison); sparse approximation would be inappropriate.

## Inputs

- Pre-constructed nearest neighbor indexes (partitioned by precursor m/z bucket)
- Low-dimensional spectrum vectors (hashed via feature hashing to length low_dim)
- Spectrum identifiers and precursor masses
- Distance threshold or eps parameter (cosine distance, typically 0.05–0.30)

## Outputs

- Sparse pairwise distance matrix (triplet or COO format: spectrum_i, spectrum_j, cosine_distance)
- Neighbor adjacency lists for each spectrum

## How to apply

Load the pre-constructed nearest neighbor indexes and low-dimensional spectrum vector representations from the indexing stage. Query each spectrum vector against the nearest neighbor indexes using a probe parameter (typically n_probe, controlling how many inverted index lists to inspect) to retrieve candidate neighbors within the user-defined distance threshold. Compute pairwise cosine distances only between each spectrum and its retrieved nearest neighbors, building a sparse matrix where most entries are zero or undefined. Export the sparse distance matrix in a format (e.g., coordinate triplet: spectrum_i, spectrum_j, distance) suitable for downstream DBSCAN or other density-based clustering algorithms. The trade-off between n_probe and accuracy is critical: higher n_probe values decrease the risk of missing true neighbors but increase computation time; typical settings depend on the dataset and desired cluster purity.

## Related tools

- **falcon** (CLI tool that orchestrates spectrum clustering including sparse distance matrix construction via nearest neighbor querying) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum I/O and preprocessing, used in the falcon pipeline)

## Evaluation signals

- Sparsity ratio: verify that the number of non-zero entries in the distance matrix is significantly smaller than m × m (where m is the number of spectra), confirming that exhaustive comparison was avoided.
- Neighbor count distribution: check that each spectrum has approximately n_neighbors candidate neighbors in the sparse matrix, consistent with the indexing configuration.
- Distance value range: confirm that all distances are in the range [0, 1] and respect the cosine similarity metric (distances between hashed vectors).
- Clustering quality: run DBSCAN on the sparse matrix and verify that the resulting cluster purity and recall match expectations for the eps threshold (values between 0.05 and 0.15 typically yield pure clusters for proteomics data).
- Symmetry check: for a subset of entries, verify that distance(i, j) ≈ distance(j, i), reflecting the symmetric nature of cosine distance.

## Limitations

- The sparse matrix construction is sensitive to n_probe and n_neighbors_ann settings; too few probes or neighbors may miss true nearby spectra, reducing clustering completeness.
- Accuracy of sparse distances depends on the quality of the hashing step; feature hashing with insufficient low_dim length may not preserve cosine similarity well, increasing distance approximation error.
- Precursor m/z bucketing assumes that similar spectra have precursor masses within the specified tolerance (precursor_tol); spectra with very different precursor masses will never be compared, which is intentional for peptide/metabolite clustering but may exclude true isobaric matches.
- The method is optimized for bottom-up proteomics defaults (min_peaks=5, min_mz_range=250 Da, min_mz=101, max_mz=500); metabolomics and top-down data require adjusted preprocessing parameters to avoid filtering out relevant spectra before indexing.

## Evidence

- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time.: "A sparse pairwise distance matrix is computed by retrieving similarities to neighboring spectra using the nearest neighbor indexes. The accuracy and speed of similarity searching is governed by the"
- [other] Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold. Compute pairwise distances only between each spectrum and its retrieved nearest neighbors, building a sparse distance matrix.: "Query each spectrum vector against the nearest neighbor indexes to retrieve candidate similar spectra within a user-defined distance threshold. Compute pairwise distances only between each spectrum"
- [readme] n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results.: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results."
- [readme] n_neighbors and n_neighbors_ann: The final number of neighbors to consider for each spectrum and during nearest neighbor searching. Querying less neighbors will run faster but will give slightly less accurate clustering results.: "n_neighbors and n_neighbors_ann: The final number of neighbors to consider for each spectrum and during nearest neighbor searching. Querying less neighbors will run faster but will give slightly less"
