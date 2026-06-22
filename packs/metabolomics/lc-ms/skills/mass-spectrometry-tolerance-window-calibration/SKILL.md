---
name: mass-spectrometry-tolerance-window-calibration
description: Use when after feature extraction from raw LC-MS or GC-MS data (using XCMS, MS-Dial, or similar), when you have a feature intensity table with m/z and RT metadata and a reference compound database (known molecules list with m/z, RT, and annotation metadata), and you need to assign confidence-ranked.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - R
  - XCMS
  - MS-Dial
  - GetFeatistics
  - patRoon
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- open source tools such as XCMS and MS-Dial
- after obtaining a feature table using open source tools such as XCMS and MS-Dial.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-tolerance-window-calibration

## Summary

Setting and applying mass-to-charge (m/z) and retention time (RT) tolerance windows to match detected features against known reference compounds in high-resolution mass spectrometry workflows. This calibration step is critical for achieving confident compound annotation (AnnoLevel 1) while minimizing false positives from spurious matches.

## When to use

After feature extraction from raw LC-MS or GC-MS data (using XCMS, MS-Dial, or similar), when you have a feature intensity table with m/z and RT metadata and a reference compound database (known molecules list with m/z, RT, and annotation metadata), and you need to assign confidence-ranked identifications to features. Tolerance window calibration is essential when instrument calibration performance varies or when method conditions (column chemistry, flow rate, ionization mode) differ from a reference library.

## When NOT to use

- Input is already a validated compound list with known identities (no matching needed).
- Reference database lacks m/z or retention time metadata, or lacks standardization to your instrument's mass accuracy regime.
- Retention time is unmeasured or unavailable in either the feature table or reference database (one-dimensional matching alone is unreliable for confident annotation).

## Inputs

- Feature intensity table (samples × features matrix)
- Feature information table with m/z and retention time per feature
- Known molecules reference database with m/z, retention time, and compound metadata
- m/z tolerance threshold (in ppm or Da)
- Retention time tolerance threshold (user-specified window)

## Outputs

- Annotated feature information (featINFO) table with matched compound names
- Annotation level assignments (AnnoLevel '1' for confirmed, NA or lower for unconfirmed)
- Feature ID, m/z, retention time, and reference metadata columns

## How to apply

First, establish m/z tolerance (in ppm or Da) and RT tolerance (in seconds or minutes) based on your instrument's mass accuracy specification and chromatographic method repeatability. For each feature in the table, calculate the mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply the tolerance windows as a two-dimensional filter: retain only candidate matches where both |Δm/z| ≤ m/z_tolerance AND |ΔRT| ≤ RT_tolerance. Features with exactly one match within both windows are marked as AnnoLevel '1' (confirmed identity) and receive the compound name and metadata; features with zero matches or multiple matches are assigned lower or missing annotation levels. Export the annotated feature info table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and reference metadata.

## Related tools

- **XCMS** (Feature extraction and preprocessing upstream of tolerance window matching)
- **MS-Dial** (Feature extraction and preprocessing upstream of tolerance window matching)
- **GetFeatistics** (R package providing checkmolecules_in_feat_table function for applying tolerance windows and generating annotated feature info tables) — https://github.com/FrigerioGianfranco/GetFeatistics
- **patRoon** (Comprehensive NTA workflow wrapper integrating XCMS, MS-Dial, and annotation algorithms; can orchestrate feature extraction and compound annotation with tolerance-based matching) — https://github.com/rickhelmus/patRoon
- **R** (Computing environment for tolerance window calculations and feature-to-compound matching logic)

## Examples

```
checkmolecules_in_feat_table(feat_table, feat_info, molecules_ref, mz_tol = 5, rt_tol = 30, tol_unit = 'ppm', return_as_featinfo_lev1 = TRUE)
```

## Evaluation signals

- Check that the number of features assigned AnnoLevel '1' is reasonable (not all features, not zero) and document the m/z and RT tolerances used.
- Verify that features with exactly one match within tolerance windows are marked AnnoLevel '1', and features with zero or multiple matches are marked as NA or lower confidence.
- Cross-check a sample of matched features: confirm Δm/z and ΔRT are both within specified tolerance windows for AnnoLevel '1' entries.
- Compare annotation counts before and after filtering by tolerance windows; a sharp drop in confirmed identities suggests tolerances may be too strict.
- Inspect outlier features (e.g., very high or very low m/z) to ensure they were not spuriously matched due to tolerance window asymmetry or calibration drift.

## Limitations

- Tolerance windows are instrument- and method-specific; transferring tolerances between different MS platforms, columns, or ionization modes risks false positives or false negatives.
- Features with identical m/z and RT within tolerance of multiple reference compounds cannot be disambiguated by this approach alone; requires additional MS/MS or orthogonal data.
- One-dimensional matching (m/z alone or RT alone) is not supported; two-dimensional matching is mandatory for AnnoLevel '1' confidence.
- Reference database must be representative of the chemical space in the sample; missing compounds cannot be matched regardless of tolerance window settings.
- Retention time drift during analysis or poor chromatographic reproducibility will inflate unmatched features if RT tolerance is set based on a single analytical run.

## Evidence

- [other] For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound.: "For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT)"
- [other] Apply m/z tolerance and retention-time tolerance windows (specific tolerances to be set by the user based on instrument calibration and method): "Apply m/z tolerance and retention-time tolerance windows (specific tolerances to be set by the user based on instrument calibration and method)"
- [other] For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table.: "For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity)"
- [other] The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified error tolerances (in ppm or Da) and retention time windows.: "The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using"
- [intro] This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
