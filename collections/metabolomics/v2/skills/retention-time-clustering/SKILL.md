---
name: retention-time-clustering
description: Use when you have an XCMS CentWave feature extraction output table containing multiple features with near-identical m/z values and retention times (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - XCMS CentWave
  - Paramounter
derived_from:
- doi: 10.1021/acs.analchem.1c04758
  title: Paramounter
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_paramounter_cq
schema_version: 0.2.0
---

# retention-time-clustering

## Summary

Cluster and deduplicate XCMS CentWave-extracted metabolic features by grouping those with similar m/z values and retention times within a user-defined mass tolerance threshold, then collapse each cluster to a single representative feature. This skill prevents inflation of feature counts from redundant detections of the same metabolite.

## When to use

Apply this skill when you have an XCMS CentWave feature extraction output table containing multiple features with near-identical m/z values and retention times (e.g., due to peak shoulder detection or isotopologue splitting), and you need to reduce false feature inflation while preserving true distinct metabolites. Use it when your analytical goal is to produce a deduplicated, non-redundant feature list suitable for downstream statistical or annotation analyses.

## When NOT to use

- Input is already a deduplicated or manually curated feature table — re-clustering may introduce unnecessary aggregation.
- Your experimental design or biological question requires retention of isotopologues or adduct variants as separate features — dereplication would be counterproductive.
- Mass tolerance threshold (mzdiff) is unknown or poorly characterized for your instrument — without validation, clustering may merge true distinct metabolites or miss duplicates.

## Inputs

- XCMS CentWave feature extraction output table (with columns: feature ID, m/z, retention time, intensity)
- Mass tolerance threshold (mzdiff parameter, numeric in m/z units or negative to disable)

## Outputs

- Deduplicated feature table (rows = unique features, duplicates collapsed to representatives)
- Feature count reduction report (original vs. deduplicated feature count)

## How to apply

Load the XCMS CentWave feature table with m/z values, retention times, and feature identifiers. Set a mass tolerance threshold (mzdiff parameter; suggested default 0.001–0.01 m/z units) that reflects your instrument's mass accuracy and the smallest meaningful m/z difference between distinct metabolites in your experiment. Group features where both m/z difference and retention time are within tolerance windows, then collapse each group to a single representative feature (e.g., the highest intensity or earliest retention time member). If you suspect true metabolites with mass differences smaller than mzdiff exist in your dataset, disable dereplication by setting mzdiff to a negative value to retain all features for manual inspection. Output the deduplicated feature table with reduced feature count and verified absence of near-duplicate m/z–RT pairs.

## Related tools

- **XCMS CentWave** (Peak detection and feature extraction from raw mass spectrometry data; produces m/z and retention time coordinates that serve as input to dereplication clustering)
- **Paramounter** (Post-extraction dereplication implementation; applies mzdiff mass tolerance threshold and retention time similarity to cluster and collapse XCMS CentWave features) — github.com/HuanLab/Paramounter

## Evaluation signals

- Feature count is reduced from the raw XCMS output (duplicates removed); verify reduction is proportional to expected redundancy level.
- No m/z–retention time pair in the output table has a near-duplicate within the mzdiff mass tolerance threshold (invariant check for deduplication completeness).
- Representative features retained per cluster have expected properties (e.g., highest intensity or earliest RT within each group).
- When mzdiff is set to a negative value, feature count remains unchanged from raw XCMS output (dereplication disabled correctly).
- Downstream analysis (e.g., metabolite annotation, statistical association) shows no inflation of false hits due to redundant features.

## Limitations

- True positive metabolic features with mass differences smaller than the mzdiff threshold may be removed by mistake during dereplication, leading to loss of distinct metabolites.
- Dereplication outcome depends critically on accurate mzdiff parameterization; incorrect threshold can merge true distinct features or fail to collapse redundant ones.
- Peak height optimization (used by Paramounter to maximize true positives) increases false positive rate and software crash likelihood; users may need to apply a secondary filter (e.g., 2× optimized peak height threshold) to manage false positives after dereplication.
- No changelog available for Paramounter, making version-to-version reproducibility and parameter stability unclear.

## Evidence

- [readme] mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave"
- [readme] some true positive metabolic features with mass differences smaller than that value may be removed by mistake: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
- [readme] if a user wants to disable the dereplication function, set the mzdiff to be any negative value: "if a user wants to disable the dereplication function, set the mzdiff to be any negative value"
- [readme] Suggested default value: 0.001 or 0.01: "Suggested default value: 0.001 or 0.01"
- [other] Apply dereplication by grouping features within the mzdiff mass tolerance threshold and retention time similarity window, then collapse each group to a single representative feature: "Apply dereplication by grouping features within the mzdiff mass tolerance threshold and retention time similarity window, then collapse each group to a single representative feature"
