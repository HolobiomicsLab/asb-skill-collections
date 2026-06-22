---
name: m-z-based-feature-grouping
description: Use when after retention-time clustering has grouped features from multiple LC-MS samples, when you need to refine feature assignments by enforcing m/z consistency and eliminate duplicate or near-duplicate features with the same mass but potentially misaligned retention times.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - JPA
  - R
  - XCMS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
---

# m/z-based-feature-grouping

## Summary

Refine and merge putative metabolic features across multiple samples by clustering on mass-to-charge ratio (m/z) after retention-time-based clustering. This step consolidates features with matching m/z values into unified entries for a multi-sample aligned feature table.

## When to use

Apply this skill after retention-time clustering has grouped features from multiple LC-MS samples, when you need to refine feature assignments by enforcing m/z consistency and eliminate duplicate or near-duplicate features with the same mass but potentially misaligned retention times.

## When NOT to use

- Do not use this skill on already-aligned multi-sample feature tables; m/z clustering is meant to refine per-sample or RT-pre-clustered data, not re-cluster aligned output.
- Do not apply m/z clustering in isolation without prior retention-time-based clustering; the two-stage approach is designed to work sequentially for robust alignment.
- Do not use this skill on single-sample feature extracts; m/z-based grouping is only meaningful when consolidating features across multiple samples.

## Inputs

- retention-time-clustered feature groups (intermediate output from RT clustering)
- extracted feature tables from individual samples (MS1 peak picking, MS2 recognition, or targeted list output)

## Outputs

- unified aligned feature table with merged entries
- alignment statistics (number of aligned features, sample-to-feature coverage matrix, quality metrics)

## How to apply

Following retention-time-based clustering, apply m/z-based clustering to refine the grouping and merge features with matching mass-to-charge ratios within the specified m/z tolerance (e.g., 10 ppm, controlled by the mz.tol or similar parameter). The JPA alignment workflow performs this as a secondary refinement step: features already grouped by retention time are re-examined for m/z consistency, and features falling within the m/z tolerance window are merged into single aligned features. This two-stage approach (RT-first, then m/z) reduces false positives from retention-time drift while ensuring mass accuracy. Generate alignment statistics post-clustering to report the number of aligned features and sample-to-feature coverage metrics, which serve as validation that the procedure produced a coherent feature table.

## Related tools

- **JPA** (Performs the m/z-based clustering refinement step as Part 5 of its alignment workflow after RT clustering) — https://github.com/HuanLab/JPA.git
- **XCMS** (Embedded within JPA to provide underlying peak picking and feature extraction prior to alignment and clustering)

## Evaluation signals

- Verify that all features within the specified m/z tolerance window have been merged into single aligned entries in the output table.
- Check the sample-to-feature coverage matrix to confirm each aligned feature is present across expected samples with no spurious duplicates.
- Confirm that the number of aligned features is less than or equal to the sum of per-sample feature counts, indicating successful consolidation.
- Validate that m/z values of merged features fall within the specified tolerance (e.g., max pairwise m/z difference ≤ 10 ppm) and are representative of cluster centers.
- Review alignment quality metrics (e.g., number of features aligned across all samples vs. singletons) to assess the robustness of the clustering.

## Limitations

- M/z tolerance must be set appropriately for the instrument's mass accuracy; overly tight tolerances may prevent valid feature merging, while loose tolerances may incorrectly merge distinct metabolites.
- The two-stage clustering approach (RT then m/z) assumes that retention-time pre-clustering is robust; poor RT clustering will propagate errors into the m/z refinement step.
- High m/z features or isobaric compounds within the tolerance window may be incorrectly merged, leading to loss of information about distinct metabolites with similar mass.
- The procedure does not account for adduct variants or in-source fragmentation; those must be handled by downstream annotation modules (e.g., CAMERA).

## Evidence

- [other] Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. Apply m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios.: "Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. 3. Apply m/z-based clustering to refine grouping and merge features"
- [other] Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics.: "Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics."
- [other] JPA alignment workflow step (Part 5: Alignment) operates after feature extraction and before annotation.: "JPA includes an alignment workflow step (Part 5: Alignment) as part of its comprehensive metabolomics data processing pipeline that operates after feature extraction and before annotation."
- [readme] for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5."
