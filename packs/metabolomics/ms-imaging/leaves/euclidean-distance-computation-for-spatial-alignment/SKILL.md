---
name: euclidean-distance-computation-for-spatial-alignment
description: Use when when you have preprocessed ST and SM AnnData objects with spatial coordinates and need to establish one-to-one spot correspondence between the two modalities prior to joint analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - spatialMETA
  - scikit-learn NearestNeighbors
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1038/s41467-025-63915-z
  title: SpatialMETA
evidence_spans:
- spatialMETA is a method for integrating spatial multi-omics data
- spatialmeta.pp.calculate_qc_metrics_sm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spatialmeta_cq
    doi: 10.1038/s41467-025-63915-z
    title: SpatialMETA
  dedup_kept_from: coll_spatialmeta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63915-z
  all_source_dois:
  - 10.1038/s41467-025-63915-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# euclidean-distance-computation-for-spatial-alignment

## Summary

Compute pairwise Euclidean distances between spatial transcriptomics (ST) and spatial metabolomics (SM) spot coordinates to identify nearest neighbors for unified resolution integration. This distance metric enables KNN-based spot correspondence in multi-omics spatial alignment.

## When to use

When you have preprocessed ST and SM AnnData objects with spatial coordinates and need to establish one-to-one spot correspondence between the two modalities prior to joint analysis. Specifically, use this skill as the distance computation step within the KNN query phase of spot_align_byknn, where SM spots must be mapped to their nearest ST counterparts.

## When NOT to use

- ST and SM spots are already aligned or on identical coordinate grids — direct correspondence lookup is sufficient without KNN distance computation.
- Spot correspondence is manually curated or known a priori — skip to joint_adata_sm_st without recomputing distances.
- One or both modalities lack valid spatial coordinates or have insufficient spot coverage — KNN index construction will fail.

## Inputs

- Preprocessed ST AnnData object with spatial coordinates (n_st_spots × 2)
- Preprocessed SM AnnData object with spatial coordinates (n_sm_spots × 2)
- Fitted NearestNeighbors index (scikit-learn KNN index on ST coordinates)

## Outputs

- SM-to-ST spot correspondence mapping (index pairs stored in joint AnnData metadata)
- Minimum Euclidean distance for each SM spot to its assigned ST spot
- Distance distribution statistics (for validation)

## How to apply

After constructing a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors, query the index with SM spot coordinates to compute Euclidean distances from each SM spot to all ST spots. The KNN query returns k nearest neighbors ranked by minimum Euclidean distance; assign each SM spot to the ST spot with the smallest distance. Validate that distance distributions are reasonable (e.g., no unexpected outliers or zero-distance conflicts that would indicate coordinate misalignment). Store the SM-to-ST index pairs and corresponding minimum distances in the joint AnnData object metadata for traceability.

## Related tools

- **scikit-learn NearestNeighbors** (Constructs KNN index on ST spot coordinates and computes Euclidean distances from SM query points) — https://scikit-learn.org
- **spatialMETA** (Orchestrates the spot_align_byknn workflow step that wraps KNN index construction and Euclidean distance queries) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from sklearn.neighbors import NearestNeighbors; knn = NearestNeighbors(n_neighbors=1, metric='euclidean').fit(st_adata.obsm['spatial']); distances, indices = knn.kneighbors(sm_adata.obsm['spatial']); joint_adata.obs['sm_to_st_index'] = indices.flatten(); joint_adata.obs['alignment_distance'] = distances.flatten()
```

## Evaluation signals

- All SM spots have been assigned to exactly one ST spot (no unmatched or multiply-assigned spots).
- Distance distribution exhibits expected range and shape (e.g., median and IQR are consistent with spatial resolution of both modalities; no extreme outliers indicating registration failure).
- SM-to-ST index pairs are stored in joint AnnData metadata and can be retrieved without error.
- Spot correspondence is symmetric or one-to-many without gaps (each SM spot has a valid ST counterpart).
- Distance values are non-negative and finite (no NaN, Inf, or negative values indicating computational error).

## Limitations

- KNN-based alignment assumes ST and SM spot distributions overlap substantially; if modalities have non-overlapping spatial extents, distance-based assignment may produce spurious matches.
- Euclidean distance treats all spatial dimensions equally; if ST and SM have different pixel/spot sizes or aspect ratios, rescaling may be needed prior to distance computation.
- No explicit handling of duplicate SM spots or ST spots at identical coordinates; ties in minimum distance may result in arbitrary tie-breaking.
- The method requires k (number of neighbors) and metric parameters; choice of k affects downstream one-to-one mapping if not restricted to k=1.

## Evidence

- [other] Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors. Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot. Assign each SM spot to its nearest ST spot based on minimum Euclidean distance.: "Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors. 3. Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot. 4. Assign each SM spot"
- [other] The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution integration in spatialMETA.: "The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution"
- [readme] SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns: "SMOI aligns ST and SM to a unified resolution, integrates single or multiple sample data to identify cross-modal spatial patterns"
- [other] Load preprocessed ST and SM AnnData objects with spatial coordinates and filtered features. Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata.: "Load preprocessed ST and SM AnnData objects with spatial coordinates and filtered features. 5. Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint"
- [other] Validate that all SM spots have been assigned and distance distributions are reasonable.: "Validate that all SM spots have been assigned and distance distributions are reasonable."
