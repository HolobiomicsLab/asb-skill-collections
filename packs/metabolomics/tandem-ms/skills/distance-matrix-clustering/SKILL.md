---
name: distance-matrix-clustering
description: Use when you have a sparse pairwise distance matrix derived from nearest neighbor indexing of MS/MS spectra (or similar high-dimensional objects) and need to partition spectra into groups based on local density and neighborhood connectivity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
  - DBSCAN
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

# Density-Based Clustering on Sparse Distance Matrices

## Summary

Apply density-based clustering (DBSCAN) to a sparse pairwise distance matrix computed from nearest neighbor indexes to group similar MS/MS spectra into clusters. This skill is the final step in large-scale spectrum clustering pipelines, converting similarity relationships into labeled cluster assignments.

## When to use

You have a sparse pairwise distance matrix derived from nearest neighbor indexing of MS/MS spectra (or similar high-dimensional objects) and need to partition spectra into groups based on local density and neighborhood connectivity. This is appropriate when you want to identify spectra that form dense regions without pre-specifying the number of clusters, and when your distance matrix is too large for exhaustive pairwise comparison but has been efficiently computed via nearest neighbor approximation.

## When NOT to use

- You have already assigned cluster labels or cluster membership is predetermined by experimental design.
- Your distance matrix is dense and small enough for alternative clustering methods (e.g., hierarchical clustering, k-means with known k).
- You require hard guarantees on cluster size or distribution; DBSCAN produces variable-sized clusters and identifies noise points as singletons.

## Inputs

- sparse pairwise distance matrix (scipy.sparse format or equivalent)
- spectrum identifiers (mapped to matrix rows)
- eps parameter value (maximum cosine distance threshold)

## Outputs

- cluster assignment table (CSV with spectrum ID and cluster label)
- cluster membership counts
- optional: representative spectra per cluster (MGF format)

## How to apply

Load the sparse pairwise distance matrix output from the nearest neighbor indexing step into a format compatible with DBSCAN (scipy.sparse or equivalent). Apply DBSCAN with the eps parameter set to control cluster purity: values between 0.05 and 0.15 typically yield pure clusters (single peptide per cluster), while values up to 0.30 enable more aggressive clustering depending on spectral characteristics and preprocessing. The eps threshold represents the maximum cosine distance for two spectra to be considered neighbors. After clustering, assign each spectrum a cluster label and save the cluster membership to a CSV file with spectrum identifiers and corresponding cluster assignments. Verify cluster quality by inspecting both the number of clusters formed and the density distribution within clusters.

## Related tools

- **falcon** (Complete spectrum clustering pipeline; performs feature hashing, nearest neighbor indexing, sparse distance matrix computation, and density-based clustering.) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for spectrum processing and I/O (mzML, mzXML, MGF formats) integrated with falcon.)
- **DBSCAN** (Density-based clustering algorithm applied to sparse distance matrices to identify spectrum clusters.)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output CSV contains all input spectrum identifiers with assigned non-negative cluster labels (or -1 for noise/singletons).
- Cluster sizes and counts are consistent with the eps threshold and spectral diversity of the input dataset (e.g., lower eps → more clusters).
- No spectrum appears twice in the assignment table and no spectrum is missing from the output.
- Cluster purity can be validated post-hoc if ground truth peptide identity is available: high-purity clustering (single peptide per cluster) should occur for eps in range 0.05–0.15.
- Sparse distance matrix structure is preserved (only neighbors referenced, not exhaustive comparisons), confirming computational efficiency was maintained.

## Limitations

- DBSCAN performance is sensitive to the eps parameter; optimal values depend on spectral characteristics and preprocessing (scaling, normalization) applied upstream. Values between 0.05 and 0.15 are typical for proteomics but may require tuning for metabolomics or top-down data.
- The algorithm produces variable-sized clusters and may classify low-density spectra as noise (cluster label -1), which may be undesirable for applications requiring complete spectrum assignment.
- Cluster quality depends critically on the quality and sparsity pattern of the input distance matrix; if nearest neighbor indexing missed true neighbors (due to low n_probe or n_neighbors_ann settings), subsequent clustering will be suboptimal.
- Density-based clustering does not provide confidence scores or posterior probabilities for cluster assignments; all cluster labels are equally definitive.

## Evidence

- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [other] Density-based clustering is performed as the final step to group similar spectra into clusters, using the sparse pairwise distance matrix computed from nearest neighbor indexes as input.: "Density-based clustering is performed as the final step to group similar spectra into clusters, using the sparse pairwise distance matrix computed from nearest neighbor indexes as input."
- [readme] The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters."
- [readme] eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to only a single peptide). The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in falcon. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used.: "Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used."
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line.: "exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line."
