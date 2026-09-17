---
name: knn-nearest-neighbor-matching-for-spot-correspondence
description: Use when when integrating two spatial omics modalities (ST and SM) measured
  on the same tissue sample but at different spatial resolutions or spot coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3391
  tools:
  - spatialMETA
  - scikit-learn (NearestNeighbors)
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# knn-nearest-neighbor-matching-for-spot-correspondence

## Summary

Aligns spatial transcriptomics (ST) and spatial metabolomics (SM) spots to a unified resolution by constructing a k-nearest-neighbor index on ST coordinates and assigning each SM spot to its nearest ST neighbor based on Euclidean distance. This establishes one-to-one spot correspondence required for downstream joint multi-omics analysis.

## When to use

When integrating two spatial omics modalities (ST and SM) measured on the same tissue sample but at different spatial resolutions or spot coordinates. Apply this skill immediately after loading and filtering both modality datasets as AnnData objects with validated spatial coordinates, and before joint normalization or cross-modal analysis.

## When NOT to use

- ST and SM modalities are measured at identical spatial resolution and spot coordinates—alignment is already unified; use direct concatenation instead.
- Spatial coordinates are missing, malformed, or in different coordinate systems without prior registration—preprocessing and coordinate validation required first.
- One modality has dramatically fewer spots than the other (e.g., <10% coverage)—many SM spots may map to distant ST spots, violating co-localization assumptions.

## Inputs

- Preprocessed ST AnnData object with spatial coordinates (obsm['spatial'] or .obs columns)
- Preprocessed SM AnnData object with spatial coordinates
- SM and ST spot coordinates as 2D arrays (n_spots × 2)

## Outputs

- SM-to-ST spot correspondence mapping (index pairs stored in joint AnnData metadata)
- Aligned coordinate mappings and distance metrics for validation
- Joint AnnData object with spot correspondence metadata

## How to apply

Build a KNN index on preprocessed ST spot coordinates using scikit-learn's NearestNeighbors with Euclidean distance metric. Query this index with SM spot coordinates to find k nearest ST neighbors for each SM spot. Assign each SM spot to its single nearest ST spot (k=1 by default) based on minimum Euclidean distance in the spatial plane. Record the SM-to-ST index pair mappings in the joint AnnData object metadata. Validate that all SM spots have been successfully assigned and inspect distance distributions to confirm reasonable alignment—large mean distances or bimodal distributions may indicate tissue drift, registration artifacts, or incompatible coordinate systems.

## Related tools

- **spatialMETA** (Framework implementing the spot_align_byknn workflow step for multi-omics integration) — https://github.com/WanluLiuLab/SpatialMETA
- **scikit-learn (NearestNeighbors)** (Constructs KNN index on ST spot coordinates and queries for nearest neighbors) — https://scikit-learn.org

## Examples

```
from spatialmeta.pp import spot_align_byknn; spot_align_byknn(st_adata, sm_adata, k=1)
```

## Evaluation signals

- All SM spots have a valid ST assignment (no unassigned or null mappings in correspondence table).
- Euclidean distance distribution between matched pairs is unimodal with reasonable mean and variance (no long tail indicating outlier alignments).
- SM-to-ST correspondence is injective (each SM spot maps to exactly one ST spot, though multiple SM spots may map to the same ST spot).
- Spatial continuity check: adjacent SM spots in original space map to ST spots that are also spatially proximal, confirming no 'jumps' or topology violations.
- Joint AnnData object successfully created and preserves both ST and SM feature matrices linked via spot correspondence metadata.

## Limitations

- Method assumes ST and SM modalities measure overlapping tissue regions; misaligned or non-overlapping samples will produce spurious correspondences.
- KNN matching is greedy and does not enforce one-to-one mapping if requested; multiple SM spots can map to the same ST spot, potentially diluting SM signal during aggregation.
- Euclidean distance in 2D spatial coordinates ignores tissue topology, z-depth, or tissue distortion; if samples are warped or rotated relative to each other, coordinate-based matching will fail.
- No built-in outlier detection or distance thresholding; unusually distant matches are accepted without warning, requiring manual post-hoc validation.

## Evidence

- [other] Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors.: "Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors."
- [other] Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot.: "Query the KNN index with SM spot coordinates to find k nearest ST neighbors for each SM spot."
- [other] Assign each SM spot to its nearest ST spot based on minimum Euclidean distance.: "Assign each SM spot to its nearest ST spot based on minimum Euclidean distance."
- [other] Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata.: "Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata."
- [other] Validate that all SM spots have been assigned and distance distributions are reasonable.: "Validate that all SM spots have been assigned and distance distributions are reasonable."
- [other] The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution integration in spatialMETA.: "The spot_align_byknn workflow step is the mechanism that performs spatial spot alignment between spatial transcriptomics (ST) and spatial metabolomics (SM) modalities to achieve unified resolution"
