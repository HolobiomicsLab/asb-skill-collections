---
name: spectral-scan-metadata-matching
description: Use when you have extracted MS1 and MS2 scans in mzML/mzXML format from
  raw chromatogram files and a structured metadata file (containing retention time,
  m/z, compound name, molecular weight, and annotation fields), and you need to pair
  each scan set with its corresponding chemical record to build.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - meRgeION2
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-scan-metadata-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match extracted MS1 and MS2 scans to user-provided metadata (retention time, m/z, compound name, molecular weight) within specified tolerance windows to construct standardized spectral library records. This skill bridges raw chromatographic data and curated spectral libraries by associating instrumental measurements with chemical metadata.

## When to use

You have extracted MS1 and MS2 scans in mzML/mzXML format from raw chromatogram files and a structured metadata file (containing retention time, m/z, compound name, molecular weight, and annotation fields), and you need to pair each scan set with its corresponding chemical record to build a GNPS-compatible spectral library without manual curation.

## When NOT to use

- Metadata is unstructured or lacks m/z and retention time fields — matching requires quantitative anchors.
- Scans are already in a proprietary spectral library format (not raw mzML/mzXML) — re-matching introduces redundancy.
- Data confidentiality is not a concern and public spectral databases (GNPS, MassBank) are acceptable — use shared repositories instead.

## Inputs

- Extracted MS1 scans (mzML/mzXML format)
- Extracted MS2 scans (mzML/mzXML format)
- User-provided metadata file (structured format with retention time, m/z, compound name, molecular weight, annotation fields)

## Outputs

- GNPS-style spectral library records
- Merged spectral library output (GNPS-compatible format)

## How to apply

Load the extracted MS1 and MS2 scans from the preceding extraction step and parse the user-provided metadata file using a structured format reader. Match each extracted scan pair to metadata records by comparing m/z and retention time values against user-specified tolerance windows (the article does not define exact thresholds, but tolerance windows are user-configurable). For each successful match within the tolerance boundaries, construct a GNPS-style library entry by combining the scan data, metadata fields, and standardized GNPS headers. Finally, serialize the merged records into a GNPS-compatible spectral library output format. The key decision point is setting appropriate tolerance windows: tighter windows reduce false matches but risk missing valid pairs if instrumental drift or metadata recording uncertainty is present.

## Related tools

- **meRgeION2** (Performs batch matching of extracted scans to metadata and constructs GNPS-style library entries) — https://github.com/daniellyz/meRgeION2
- **GNPS** (Defines the spectral library format and metadata schema that merged records must conform to)

## Evaluation signals

- All extracted scans have been assigned to exactly one metadata record or confirmed as unmatched (no orphaned scans).
- Each matched record contains non-null values for m/z, retention time, compound name, molecular weight, and MS/MS fragmentation data.
- Serialized output conforms to GNPS spectral library schema (headers, field order, data types).
- m/z and retention time differences between matched scans and metadata records fall within the user-specified tolerance windows.
- Comparison of pre- and post-matching record counts shows no data loss (or documents intentional filtering rationale).

## Limitations

- Matching quality depends on accuracy and completeness of user-provided metadata; missing or incorrect m/z or retention time values will cause failed matches.
- No automated validation of metadata schema — malformed input files may cause silent failures or partial matches.
- Tolerance window selection is user-defined; no automated guidance is provided for setting appropriate thresholds for different MS platforms or methods.
- mzML/mzXML conversion quality depends on upstream vendor software and conversion tools; format corruption will propagate into the merged library.
- The README does not specify handling of multiple scans matching the same metadata record or a single scan matching multiple records; edge case behavior is undocumented.

## Evidence

- [other] Parse user-provided metadata file (retention time, m/z, compound name, molecular weight, and annotation fields) using a structured format reader.: "Parse user-provided metadata file (retention time, m/z, compound name, molecular weight, and annotation fields) using a structured format reader."
- [other] Match each extracted scan pair to metadata records by m/z and retention time within user-specified tolerance windows.: "Match each extracted scan pair to metadata records by m/z and retention time within user-specified tolerance windows."
- [other] Construct GNPS-style library entries by combining scan data, metadata fields, and standardized headers.: "Construct GNPS-style library entries by combining scan data, metadata fields, and standardized headers."
- [readme] extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users: "extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users"
- [readme] They are then merged into a GNPS-style spectral library combining user-provided metadata: "They are then merged into a GNPS-style spectral library combining user-provided metadata"
- [readme] It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
