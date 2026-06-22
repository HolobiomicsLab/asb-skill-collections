---
name: spectral-clustering-density-based
description: Use when you have computed a sparse pairwise distance matrix from MS/MS spectra (via nearest neighbor indexing) and need to partition spectra into homogeneous clusters—typically when clustering bottom-up proteomics data with the goal of grouping spectra from the same peptide sequence or when you.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - falcon
  - spectrum-utils
  - DBSCAN (scikit-learn or equivalent)
  - DBSCAN (sklearn.cluster or equivalent)
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
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
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

# Density-Based Clustering of MS/MS Spectra

## Summary

Apply DBSCAN or equivalent density-based clustering to a sparse pairwise distance matrix derived from nearest neighbor indexes to group MS/MS spectra into clusters. This final step in the falcon pipeline identifies spectra that are close to each other and form dense data subspaces, yielding cluster assignments suitable for downstream analysis.

## When to use

Use this skill when you have computed a sparse pairwise distance matrix from MS/MS spectra (via nearest neighbor indexing) and need to partition spectra into homogeneous clusters—typically when clustering bottom-up proteomics data with the goal of grouping spectra from the same peptide sequence or when you need representatives for each cluster.

## When NOT to use

- Input is not a distance or similarity matrix (e.g., raw peak lists or feature tables without pre-computed pairwise distances).
- Distance matrix is dense and exhaustively computed rather than sparse; DBSCAN will be inefficient and memory-intensive.
- Spectra have not been preprocessed (binned, feature-hashed, or converted to comparable vectors) or nearest neighbor indexes have not been constructed; density-based clustering requires meaningful distances.

## Inputs

- sparse pairwise distance matrix (scipy.sparse or equivalent format)
- spectrum identifiers (list or array of spectrum IDs)
- nearest neighbor index results

## Outputs

- cluster assignment table (CSV: spectrum ID, cluster label)
- cluster membership dictionary or array (spectrum index → cluster ID)
- representative spectra per cluster (optional MGF file)

## How to apply

Load the sparse pairwise distance matrix (output from the nearest neighbor indexing step) in a format compatible with DBSCAN. Apply density-based clustering, typically DBSCAN, using the cosine distance matrix as input. Tune the `eps` parameter (maximum cosine distance between neighbors) to control cluster purity; values between 0.05 and 0.15 typically yield pure clustering for proteomics, while values up to 0.30 can be used for more aggressive clustering. Assign each spectrum a cluster label and save the cluster assignment table to a CSV file with spectrum identifiers and corresponding cluster membership. Optionally export representative spectra (e.g., the medoid or centroid of each cluster) to an MGF file for further validation or use.

## Related tools

- **falcon** (end-to-end MS/MS spectrum clustering pipeline; implements density-based clustering as the final step after feature hashing and nearest neighbor indexing) — https://github.com/bittremieux/falcon
- **spectrum-utils** (supporting library for spectrum I/O and manipulation (version 0.3.5 or compatible))
- **DBSCAN (scikit-learn or equivalent)** (core density-based clustering algorithm applied to sparse distance matrix)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Cluster assignment file (CSV) contains all input spectrum IDs with no duplicates and no missing spectra.
- Cluster labels are integers or strings with at least one non-noise cluster (clusters with ≥2 members); noise points may be labeled separately (e.g., -1 in DBSCAN convention).
- For validation: compute the average cosine similarity within each cluster (should be high, >0.7 or >0.8 depending on eps); verify that pairwise distances between spectra in the same cluster respect the eps threshold.
- Representative spectra (if exported) are physically present in output MGF file with valid spectrum format and metadata matching their cluster assignments.
- Cluster size distribution is reasonable for the dataset; no single cluster dominates or is empty (unless aggressive parameter tuning is intentional).

## Limitations

- eps parameter is data-dependent and requires tuning; the optimal value depends on spectral characteristics, preprocessing settings (e.g., peak scaling), and the purity/completeness trade-off desired. Values between 0.05–0.15 are typical for proteomics, but metabolomics or top-down data may require adjustment.
- DBSCAN produces noise points (spectra that do not belong to any cluster) if local density thresholds are not met; these may need downstream handling or parameter re-tuning.
- Density-based clustering assumes clusters have similar densities; if spectra show multi-scale density variation, some clusters may be artificially split or merged.
- Computational complexity and memory use depend on sparse matrix density and the number of neighbors explored; very large datasets or highly dense distance matrices may exceed practical limits.

## Evidence

- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [readme] Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense"
- [readme] `eps`: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to only a single peptide). The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in _falcon_. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used.: "eps parameter crucially governs cluster purity. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used."
- [other] Assign each spectrum a cluster label and generate a cluster assignment table with spectrum identifiers and corresponding cluster membership. Save cluster assignments to a structured output file (CSV or equivalent tabular format).: "Assign each spectrum a cluster label and generate a cluster assignment table with spectrum identifiers and corresponding cluster membership. Save cluster assignments to a structured output file (CSV"
- [readme] _falcon_ takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line. Representative spectra for each cluster can optionally be exported to an MGF file.: "exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line. Representative spectra for each cluster can optionally be exported to an MGF"
