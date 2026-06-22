---
name: anndata-object-integration-and-metadata-mapping
description: Use when you have preprocessed and filtered ST and SM AnnData objects with spatial coordinates and features, and you need to establish spot-level correspondence between the two modalities to enable downstream joint analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3179
  - http://edamontology.org/topic_3520
  tools:
  - spatialMETA
  - scikit-learn NearestNeighbors
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# anndata-object-integration-and-metadata-mapping

## Summary

Combines preprocessed spatial transcriptomics (ST) and spatial metabolomics (SM) AnnData objects into a unified joint object by aligning spots via KNN-based coordinate mapping and storing correspondence metadata. This enables cross-modal spatial pattern analysis on integrated multi-omics data at a common resolution.

## When to use

You have preprocessed and filtered ST and SM AnnData objects with spatial coordinates and features, and you need to establish spot-level correspondence between the two modalities to enable downstream joint analysis. Specifically, when SM spots do not natively align to ST spots and you need to create a unified feature matrix indexed by a common set of spatial locations.

## When NOT to use

- ST and SM spots are already co-registered or come from the same coordinate system without alignment drift
- SM spatial coordinates are missing or unreliable (e.g., from low-resolution imaging)
- The analysis goal is modality-specific and does not require cross-modal spatial comparison

## Inputs

- Preprocessed ST AnnData object with .obsm['spatial'] coordinates and filtered genes
- Preprocessed SM AnnData object with .obsm['spatial'] coordinates and filtered metabolites
- k parameter (number of nearest neighbors to query; default typically 1 for assignment)

## Outputs

- Joint AnnData object integrating ST and SM with unified spot indexing
- Spot correspondence metadata mapping (SM spot index → ST spot index)
- Distance distribution statistics for alignment validation

## How to apply

Load preprocessed ST and SM AnnData objects containing spatial coordinates and filtered features. Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors, then query this index with SM spot coordinates to identify k nearest ST neighbors for each SM spot. Assign each SM spot to its closest ST spot based on minimum Euclidean distance. Store the resulting spot correspondence (SM-to-ST index pairs) as metadata in a new joint AnnData object. Validate that all SM spots have been successfully assigned and that the distance distributions are reasonable (no anomalously large nearest-neighbor distances suggesting coordinate misalignment). The unified joint object becomes the input for downstream normalization and cross-modal analysis steps.

## Related tools

- **spatialMETA** (Provides the spot_align_byknn workflow step and joint_adata_sm_st integration function for KNN-based spot alignment and joint AnnData construction) — https://github.com/WanluLiuLab/SpatialMETA
- **scikit-learn NearestNeighbors** (Constructs the KNN index on ST coordinates and performs nearest-neighbor queries for SM spot assignment)

## Examples

```
from spatialmeta.pp import spot_align_byknn, joint_adata_sm_st; sm_st_index = spot_align_byknn(st_adata, sm_adata, k=1); joint_adata = joint_adata_sm_st(st_adata, sm_adata, spot_mapping=sm_st_index)
```

## Evaluation signals

- All SM spots have a valid assignment to an ST spot (no unmatched SM spots remain)
- Nearest-neighbor distances are within expected range for the tissue section geometry (e.g., no outliers >2–3× median distance suggesting coordinate errors)
- Spot correspondence metadata is present in joint AnnData object and contains no null or duplicate mappings
- Joint object dimensions match the expected union/intersection of ST and SM spot counts depending on assignment strategy (typically SM spots ≤ ST spots)
- Spatial coordinates in joint AnnData .obsm['spatial'] are consistent with original ST coordinates (alignment does not distort relative geometry)

## Limitations

- KNN assignment assumes ST spot density is sufficient to serve as reference; sparse ST data may cause multiple SM spots to map to single ST spot, losing spatial resolution
- Distance-based assignment is sensitive to coordinate scale and units; inconsistent or uncalibrated spatial coordinates (e.g., different magnification between modalities) will produce misalignments
- Method does not account for missing spots or tissue artifacts; contaminated or damaged regions in either modality may bias assignments
- k=1 assignment is hard; soft probabilistic assignment (e.g., based on distance weighting) is not described and may be necessary for overlapping spot patterns

## Evidence

- [other] Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors.: "Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors."
- [other] Assign each SM spot to its nearest ST spot based on minimum Euclidean distance.: "Assign each SM spot to its nearest ST spot based on minimum Euclidean distance."
- [other] Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata.: "Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata."
- [other] Validate that all SM spots have been assigned and distance distributions are reasonable.: "Validate that all SM spots have been assigned and distance distributions are reasonable."
- [intro] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [other] spatialmeta.pp.spot_align_byknn: "spatialmeta.pp.spot_align_byknn"
- [other] spatialmeta.pp.joint_adata_sm_st: "spatialmeta.pp.joint_adata_sm_st"
