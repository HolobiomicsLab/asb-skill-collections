---
name: m-z-retention-time-feature-matching
description: Use when after extracting a feature table from XCMS, MS-Dial, or similar
  tools, when you possess a reference compound database with known m/z, retention
  time, and metadata, and you need to assign high-confidence (AnnoLevel 1) compound
  identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0097
  - http://edamontology.org/topic_3520
  tools:
  - R
  - XCMS
  - MS-Dial
  - GetFeatistics
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-retention-time-feature-matching

## Summary

Annotate metabolomics features by matching observed m/z and retention time against a reference compound database within user-specified error tolerances, assigning AnnoLevel 1 (confirmed identity) to features with exactly one match. This two-dimensional matching step bridges raw feature detection and confirmed compound annotation in non-targeted and targeted metabolomics workflows.

## When to use

After extracting a feature table from XCMS, MS-Dial, or similar tools, when you possess a reference compound database with known m/z, retention time, and metadata, and you need to assign high-confidence (AnnoLevel 1) compound identities. Apply this skill when your instrument calibration and method parameters support explicit m/z (ppm or Da) and retention-time (RT window) tolerance definitions.

## When NOT to use

- Input feature table has not been extracted or processed by a feature-finding algorithm (e.g., raw spectra or EICs only).
- Reference compound database lacks m/z and/or retention time values, or tolerances cannot be defined based on instrument calibration.
- You require lower-confidence annotations (e.g., formula-only or structural similarity matches) rather than confirmed compound identity.

## Inputs

- Feature intensity table (samples × features matrix, typically from XCMS or MS-Dial)
- Feature info table (feature ID, observed m/z, observed retention time, and other metadata)
- Reference compound database (compound name, known m/z, known retention time, annotation metadata)

## Outputs

- Annotated feature info table with AnnoLevel 1 assignments for confirmed matches
- Matched compound names and reference metadata merged into feature annotations
- Feature subset with annotation confidence levels (AnnoLevel 1, NA, or lower levels for unconfirmed features)

## How to apply

Load the feature intensity table (samples × features), feature info table (feature metadata), and a reference compound list with m/z, retention time, and annotation fields. For each feature, calculate mass difference (Δm/z) and retention-time difference (ΔRT) against all reference compounds. Apply user-specified tolerance windows (e.g., ppm or Da for m/z; seconds or minutes for RT) to identify candidate matches. Assign AnnoLevel 1 and transfer compound name and reference metadata to the feature info table only when exactly one reference compound falls within both tolerance windows simultaneously. For features with zero or multiple matches, mark annotation level as NA or a lower confidence tier. Export the annotated feature info table with columns for feature ID, matched compound name, m/z, retention time, annotation level, and reference metadata.

## Related tools

- **XCMS** (Feature extraction and grouping from raw MS data; source of feature intensity and info tables for matching)
- **MS-Dial** (Alternative feature extraction and annotation tool; produces feature tables compatible with matching workflow)
- **GetFeatistics** (R package implementing checkmolecules_in_feat_table function for m/z-RT matching and AnnoLevel 1 assignment) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Programming environment for executing feature matching and annotation workflows)

## Evaluation signals

- Each feature in the output featINFO table has exactly one AnnoLevel 1 annotation, or AnnoLevel 1 is absent if zero or multiple reference matches were found within both tolerance windows.
- All AnnoLevel 1 features have both Δm/z and ΔRT values within user-specified tolerance thresholds (e.g., ppm/Da and RT window).
- Reference compound metadata (name, m/z, RT, and additional fields) are correctly transferred and populated for AnnoLevel 1 features; unmatched features retain feature ID and show NA or lower annotation levels.
- Feature count and sample intensity values remain unchanged; matching does not alter the feature intensity table, only enriches feature metadata.
- Tolerance parameters (m/z cutoff in ppm/Da, RT window width) are recorded in the output or workflow log for reproducibility and audit.

## Limitations

- Matching accuracy is directly dependent on instrument calibration; poorly calibrated m/z or RT drifts can cause true matches to exceed tolerance windows.
- Features with multiple reference compounds within both tolerance windows are marked NA or lower confidence, not AnnoLevel 1; this ambiguity is intentional but may reduce annotation yield in complex mixtures or when tolerance windows are too wide.
- Retention time matching assumes the same chromatographic method and comparable instruments; reference RT values from different methods or instruments require re-calibration or adjustment.
- No automatic tolerance determination; users must define m/z (ppm or Da) and RT (time units) cutoffs based on instrument specifications and method validation, which can be dataset-specific.

## Evidence

- [other] The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using user-specified error tolerances (in ppm or Da) and retention time windows.: "The checkmolecules_in_feat_table function accepts a feature intensity table, feature info table, and known molecules list, then performs mass-to-charge and retention time matching using"
- [other] For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound. Apply m/z tolerance and retention-time tolerance windows (specific tolerances to be set by the user based on instrument calibration and method) to identify candidate matches.: "For each feature in the table, perform two-dimensional matching: calculate mass difference (Δm/z) and retention-time difference (ΔRT) between the feature and each reference compound"
- [other] For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table.: "For features with exactly one match within both tolerance windows, assign AnnoLevel 1 (confirmed identity) and transfer the compound name and metadata to the featINFO table"
- [other] For features with zero or multiple matches, mark annotation level as NA or lower confidence level and retain feature ID in the featINFO table.: "For features with zero or multiple matches, mark annotation level as NA or lower confidence level and retain feature ID in the featINFO table"
- [readme] This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
