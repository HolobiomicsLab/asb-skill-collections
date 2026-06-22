---
name: metabolite-annotation-confidence-assignment
description: Use when you have a feature intensity table with feature metadata (m/z, retention time) extracted from XCMS or MS-Dial, and you want to cross-reference each feature against a known-compound database to assign standardized confidence levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R
  - XCMS
  - MS-Dial
  - GetFeatistics
  - patRoon
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

# metabolite-annotation-confidence-assignment

## Summary

Assigns annotation confidence levels (e.g., AnnoLevel 1 for confirmed identity) to metabolite features based on two-dimensional matching of m/z and retention time against a reference compound database. This skill distinguishes confirmed identifications from candidates with lower confidence, enabling prioritization of reliable annotations in non-targeted metabolomics workflows.

## When to use

Apply this skill when you have a feature intensity table with feature metadata (m/z, retention time) extracted from XCMS or MS-Dial, and you want to cross-reference each feature against a known-compound database to assign standardized confidence levels. Use when instrument calibration parameters (m/z tolerance in ppm or Da, retention-time window) are established and you need to distinguish single confirmed matches from zero, multiple, or partial matches.

## When NOT to use

- Input feature table lacks retention time or accurate m/z values (e.g., low-resolution MS or non-chromatographic data).
- Reference compound database is incomplete, uncalibrated, or missing retention time values for the same method.
- Instrument calibration parameters (m/z tolerance, RT window) are unknown or cannot be reliably estimated from quality control samples.

## Inputs

- Feature intensity table (samples × features)
- Feature info table (with m/z and retention time per feature)
- Reference compound database (m/z, retention time, compound name, and metadata)

## Outputs

- Annotated featINFO table with confidence levels (AnnoLevel column)
- Feature ID to compound name mapping
- Match statistics (number of features with AnnoLevel 1, multiple matches, or no matches)

## How to apply

Load the feature intensity table and feature info table (with m/z and retention time per feature) alongside a reference compound database containing m/z, retention time, and compound names. For each feature, calculate both mass difference (Δm/z in ppm or Da) and retention-time difference (ΔRT in minutes) against each reference compound. Apply user-defined tolerance windows (e.g., ±5 ppm for m/z, ±0.5 min for retention time, adjusted per instrument calibration) to identify candidate matches. Assign AnnoLevel '1' (confirmed identity) only to features with exactly one match within both tolerance windows; transfer the matched compound name and metadata to the output featINFO table. Mark features with zero or multiple matches as NA or lower confidence levels, preserving feature IDs. Export the annotated featINFO table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and reference metadata.

## Related tools

- **GetFeatistics** (R package providing checkmolecules_in_feat_table function to perform two-dimensional m/z and retention-time matching and assign AnnoLevel annotations) — https://github.com/FrigerioGianfranco/GetFeatistics
- **XCMS** (Feature extraction and grouping from raw MS data; output feature tables and m/z–RT coordinates as input to annotation confidence assignment)
- **MS-Dial** (Alternative feature extraction platform; outputs feature info and intensity tables compatible with annotation confidence workflow)
- **patRoon** (Comprehensive non-target analysis framework that integrates XCMS and other tools; supports componentization, adduct annotation, and confidence estimation) — https://github.com/rickhelmus/patRoon

## Examples

```
library(GetFeatistics); annotated_table <- checkmolecules_in_feat_table(feat_intensity, feat_info, known_molecules, mz_tolerance = 5, mz_unit = 'ppm', rt_tolerance = 0.5, return_as_featinfo_lev1 = TRUE)
```

## Evaluation signals

- Verify output featINFO table contains no missing values in feature ID, m/z, retention time, and annotation level columns.
- Check that features assigned AnnoLevel '1' have exactly one reference match and zero matches outside both tolerance windows.
- Confirm that the number of AnnoLevel '1' assignments is consistent with reference database coverage (typically 5–50% of features in non-targeted analyses).
- Inspect flagged features (AnnoLevel NA or lower levels) to ensure they are genuinely unmatched or ambiguous, not annotation errors.
- Validate that matched compound names and m/z values in output correspond to reference database entries within specified tolerance.

## Limitations

- Confidence assignment depends critically on instrument calibration; inaccurate or drifting m/z or RT calibration will increase false negatives (features marked as unmatched) and false positives (incorrect matches).
- Reference database must be updated and validated for the specific analytical method (LC-MS gradient, column, ionization mode); using outdated or mismatched retention times leads to systematic annotation failures.
- Features with exactly one match are marked as confirmed (AnnoLevel 1), but structural isomers or isobars with identical m/z and similar retention times cannot be disambiguated without MS/MS fragmentation data.
- No changelog provided for GetFeatistics; users should verify function behavior and parameter defaults with package documentation or vignette.

## Evidence

- [other] checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified error tolerances (in ppm or Da) and retention time windows.: "checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified"
- [other] For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply m/z tolerance and retention-time tolerance windows (specific tolerances to be set by the user based on instrument calibration and method) to identify candidate matches.: "For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply m/z"
- [other] For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table. For features with zero or multiple matches, mark annotation level as NA or lower confidence level and retain feature ID in the featINFO table.: "For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table. For features with zero or"
- [intro] This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
- [readme] patRoon combines established software tools with novel functionality in order to provide comprehensive NTA workflows: "patRoon combines established software tools with novel functionality in order to provide comprehensive NTA workflows"
