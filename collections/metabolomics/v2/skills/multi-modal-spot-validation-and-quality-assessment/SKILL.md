---
name: multi-modal-spot-validation-and-quality-assessment
description: Use when after performing spot_align_byknn to map SM spots to ST spots, validate that all SM spots have been successfully assigned and that the Euclidean distance distributions between SM spots and their assigned nearest ST neighbors are reasonable (no outliers or failed assignments that would.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0080
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
---

# multi-modal-spot-validation-and-quality-assessment

## Summary

Validate and assess quality of aligned spatial spots across spatial transcriptomics (ST) and spatial metabolomics (SM) modalities after KNN-based alignment to unified resolution. This skill ensures alignment integrity and detects anomalies in spot correspondence before downstream joint analysis.

## When to use

After performing spot_align_byknn to map SM spots to ST spots, validate that all SM spots have been successfully assigned and that the Euclidean distance distributions between SM spots and their assigned nearest ST neighbors are reasonable (no outliers or failed assignments that would compromise downstream multi-omics integration).

## When NOT to use

- ST and SM spot coordinates are already in identical resolution or on the same grid (unified resolution already achieved; alignment is unnecessary)
- Input data lack spatial coordinate information or coordinate systems are incompatible (alignment cannot be performed without valid coordinate mappings)
- Single-modality analysis that does not require multi-omics integration (validation of cross-modal spot correspondence is not applicable)

## Inputs

- Preprocessed ST AnnData object with spatial coordinates and filtered features
- Preprocessed SM AnnData object with spatial coordinates and filtered features
- KNN index built on ST spot coordinates
- SM spot coordinates (query points for KNN search)

## Outputs

- SM-to-ST spot correspondence index pairs (stored in joint AnnData metadata)
- Euclidean distance measurements for each SM-to-ST spot assignment
- Quality validation report (assignment coverage, distance statistics, anomaly flags)
- Joint AnnData object with validated spot alignment metadata

## How to apply

After the spot_align_byknn step completes, inspect the joint AnnData object metadata to confirm 100% assignment coverage (all SM spots have corresponding ST spot indices). Examine the distance distribution of SM-to-ST Euclidean distances: verify that distances fall within expected spatial resolution range and identify any spots with anomalously large distances that may indicate alignment failures. Calculate quality control metrics such as median distance, distance percentiles (e.g., 95th), and count of spots exceeding a reasonable distance threshold (typically determined by the average spot diameter or inter-spot spacing in the original coordinate systems). Flag any SM spots with distance > expected threshold for manual review or re-alignment; validate that distance distributions across the tissue are spatially homogeneous to detect regional alignment drift. These checks ensure that the spot correspondence stored in metadata is reliable before proceeding to joint feature normalization and cross-modal analysis.

## Related tools

- **spatialMETA** (Performs spot_align_byknn workflow step and stores spot correspondence metadata in joint AnnData; hosts quality assessment validation functions) — https://github.com/WanluLiuLab/SpatialMETA
- **scikit-learn NearestNeighbors** (Constructs KNN index on ST spot coordinates and queries it with SM coordinates to compute Euclidean distances for validation)

## Examples

```
# After spot_align_byknn completes, inspect joint AnnData metadata
import numpy as np
from spatialmeta.pp import spot_align_byknn
spot_align_byknn(st_adata, sm_adata, k=1)  # Align SM spots to nearest ST spots
print(f"SM-to-ST mappings: {sm_adata.obs['st_spot_index'].isna().sum()} missing assignments")
distances = sm_adata.obs['alignment_distance']
print(f"Distance stats: median={distances.median():.2f}, 95th={distances.quantile(0.95):.2f}")
outliers = (distances > distances.median() * 2).sum()
print(f"Outlier spots (>2× median): {outliers} ({100*outliers/len(sm_adata):.1f}%)")
```

## Evaluation signals

- Verify 100% assignment coverage: all SM spots have a corresponding ST spot index in the joint AnnData metadata with no null or missing assignments
- Inspect Euclidean distance distribution: median and 95th percentile distances should fall within the expected range given the average spot diameter and inter-spot spacing of the modalities
- Check for spatial homogeneity: distance distributions should not vary significantly across different tissue regions (no systematic drift or alignment failure zones)
- Identify and flag outlier spots: count of SM spots with distance > threshold (e.g., > 2× median distance) should be minimal (< 5% of total); high outlier counts indicate alignment failure
- Validate metadata schema: confirm that SM-to-ST index pairs are correctly stored and accessible in the joint AnnData object before proceeding to normalization

## Limitations

- KNN-based alignment assumes that the nearest ST neighbor is the correct match for each SM spot; this may fail when spot distributions are highly non-uniform or when SM and ST spot densities differ substantially across the tissue
- Alignment quality depends on spatial coordinate accuracy; if ST or SM coordinates contain systematic errors or artifacts, validation metrics may not detect downstream integration failures
- Distance thresholds for quality assessment must be manually determined based on expected spot sizes and modality resolutions; no universal threshold is provided, requiring domain expertise or pilot tuning
- Validation does not account for biological confounding; spots may align spatially but represent different biological regions due to tissue distortion, morphological variation, or cross-modal measurement inconsistencies

## Evidence

- [other] Assign each SM spot to its nearest ST spot based on minimum Euclidean distance.: "Assign each SM spot to its nearest ST spot based on minimum Euclidean distance."
- [other] Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata.: "Generate aligned coordinate mappings and store spot correspondence (SM-to-ST index pairs) in the joint AnnData object metadata."
- [other] Validate that all SM spots have been assigned and distance distributions are reasonable.: "Validate that all SM spots have been assigned and distance distributions are reasonable."
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [other] Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors.: "Build a KNN index on ST spot coordinates using scikit-learn's NearestNeighbors."
