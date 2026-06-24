---
name: custom-data-schema-mapping
description: Use when a practitioner has pre-computed features from an external feature-finding
  procedure (e.g., vendor software, alternative open-source tools) and wishes to incorporate
  them into PFΔScreen's PFAS prioritization pipeline without re-detecting features
  from raw mzML data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - pyOpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Custom Data Schema Mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and validate user-supplied feature lists (CSV/TSV/XLSX format) into a standardized internal feature object representation compatible with downstream PFAS prioritization workflows. This skill enables PFΔScreen to accept features from external feature-finding tools or vendor software rather than relying solely on pyOpenMS-detected features.

## When to use

Use this skill when a practitioner has pre-computed features from an external feature-finding procedure (e.g., vendor software, alternative open-source tools) and wishes to incorporate them into PFΔScreen's PFAS prioritization pipeline without re-detecting features from raw mzML data. This is particularly useful when custom feature detection parameters or proprietary tools have already been applied upstream.

## When NOT to use

- Input is already a feature table that has been successfully detected and validated by PFΔScreen's internal pyOpenMS workflow; re-mapping is unnecessary overhead.
- Custom feature list lacks required columns (m/z, retention time, intensity) and cannot be validated; skip to manual feature list curation or use pyOpenMS detection instead.
- mzML file is not provided alongside the custom feature list; MS2 spectral data cannot be retrieved and downstream fragment analysis will fail.

## Inputs

- Custom feature list (CSV, TSV, or XLSX file with required columns: m/z, retention time, intensity)
- Sample mzML file (raw HRMS data in centroided, data-dependent acquisition format)
- Optional blank mzML file (for blank correction)
- Feature metadata (optional additional columns for feature ID, charge state, or annotation)

## Outputs

- Parsed and validated feature table in PFΔScreen internal format
- Feature-to-MS2-spectrum mapping index (linking m/z and RT to MS2 scans)
- Preprocessed feature objects ready for MD/C-m/C, KMD, and MS2 fragment analysis
- Validation report noting any missing or malformed fields

## How to apply

Load the custom feature list from a user-supplied CSV, TSV, or XLSX file and validate that required columns are present: m/z, retention time, and intensity. Parse feature metadata and convert each row into PFΔScreen's internal feature object format, ensuring type consistency (numeric m/z and RT, intensity as float). Cross-reference the feature table with the corresponding mzML file to retrieve MS2 spectral data, which is essential for downstream MS2 fragment analysis and diagnostic fragment matching. The mapping must preserve feature identity (m/z and RT) so that MS2 spectra can be correctly linked during prioritization. Validate that no critical fields are null or malformed before passing features to the MD/C-m/C filtering, KMD analysis, and MS2 fragment diagnostics modules.

## Related tools

- **pyOpenMS** (Feature detection from raw HRMS data; provides alternative automated feature generation when custom lists are not available) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Vendor-independent conversion of raw proprietary HRMS data to mzML format required for MS2 spectral lookup)
- **PFΔScreen** (Host application that accepts mapped custom feature lists and applies prioritization via MD/C-m/C, KMD, and MS2 fragment analysis) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- All required columns (m/z, retention time, intensity) are present in the parsed feature table with no null or NaN values in critical fields.
- Feature-to-MS2 mapping achieves >95% successful matches between feature m/z–RT pairs and corresponding MS2 scans in the mzML file (within user-defined m/z and retention time tolerance).
- Downstream MD/C-m/C filtering, KMD analysis, and MS2 fragment diagnostics execute without errors, indicating feature objects are compatible with prioritization modules.
- Output feature count matches input feature count before mapping; no features are silently dropped during schema conversion.
- Validation report explicitly lists any features with missing MS2 data or metadata inconsistencies, allowing manual review before prioritization.

## Limitations

- Custom feature lists must be accompanied by corresponding mzML files; MS2 spectral data cannot be reconstructed if the mzML file is missing, breaking downstream fragment analysis.
- Mapping relies on m/z and retention time matching to link features to MS2 spectra; features with ambiguous or duplicate m/z–RT pairs may be incorrectly assigned or cause collisions.
- No automated collision-energy optimization for MS2 spectra; if custom features were detected using collision energies different from those in the provided mzML, fragment patterns may not align with diagnostic thresholds.
- Schema validation does not check for biologically plausible intensity distributions or retention time ordering; malformed or nonsensical feature lists may pass validation and produce spurious prioritization results.

## Evidence

- [readme] Optionally, custom feature lists can be included: "Optionally, custom feature lists can be included"
- [other] Load custom feature list from user-supplied CSV/TSV file, validating required columns (m/z, retention time, intensity). 2. Parse feature metadata and convert to internal PFΔScreen feature object format compatible with downstream prioritization modules.: "Load custom feature list from user-supplied CSV/TSF file, validating required columns (m/z, retention time, intensity). 2. Parse feature metadata and convert to internal PFΔScreen feature object"
- [readme] In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be included in PFΔScreen.: "In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be"
- [readme] Note that data evaluation only works when the corresponding mzML files are also given; otherwise MS2 data would be missing.: "Note that data evaluation only works when the corresponding mzML files are also given; otherwise MS2 data would be missing."
- [readme] This is done by the 'Browse SampleFeatures.xlsx' and 'Browse BlankFeatures.xlsx' buttons, which are preprocessed by the 'Run ExternalFeatureTable' button.: "This is done by the 'Browse SampleFeatures.xlsx' and 'Browse BlankFeatures.xlsx' buttons, which are preprocessed by the 'Run ExternalFeatureTable' button."
