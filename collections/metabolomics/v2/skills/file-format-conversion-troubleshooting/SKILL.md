---
name: file-format-conversion-troubleshooting
description: Use when when integrating MSConvert into an automated LC-MS QC workflow
  and you need to confirm that vendor acquisition files are properly converted to
  mzML format with intact spectral metadata. Apply this skill after each MSConvert
  invocation or when QC results appear incomplete or anomalous (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSConvert
  - Rapid QC-MS
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_rapid_qc_ms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c00786
  all_source_dois:
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-conversion-troubleshooting

## Summary

Validate and troubleshoot vendor-format-to-mzML conversion using MSConvert within LC-MS QC pipelines. This skill ensures proprietary acquisition files (e.g., .raw, .d, .ms) are correctly transformed into open mzML format before downstream quality control analysis.

## When to use

When integrating MSConvert into an automated LC-MS QC workflow and you need to confirm that vendor acquisition files are properly converted to mzML format with intact spectral metadata. Apply this skill after each MSConvert invocation or when QC results appear incomplete or anomalous (e.g., missing scan counts, abnormal retention time ranges, zero-intensity peaks).

## When NOT to use

- Input is already in open mzML or NetCDF format — skip conversion entirely.
- MSConvert is unavailable on your platform (e.g., MacOS instrument computers can only monitor/view data, not process via MSConvert).
- You are using a non-Thermo vendor format and have not tested MSConvert output on your specific instrument — prioritize pilot testing before integrating into production QC workflows.

## Inputs

- vendor-format LC-MS acquisition file (.raw, .d, .ms, or other MSConvert-supported format)
- system PATH or standalone MSConvert executable

## Outputs

- validated mzML file with intact spectral metadata
- conversion validation report (scan count, RT range, m/z range, intensity statistics)

## How to apply

Locate or confirm MSConvert availability in the system PATH or as a standalone module. Design a wrapper function that invokes MSConvert with the vendor acquisition file as input and mzML as the output format specification. Execute the conversion on a representative vendor-format LC-MS file, then validate the output mzML by parsing and inspecting key spectral metadata: scan count, retention time range, m/z value distribution, and intensity values. Cross-check that spectral counts and time ranges match expectations from the original vendor file metadata. Document the MSConvert version, supported vendor formats (Thermo .raw files are extensively tested; Agilent, Bruker, Sciex, and Waters support is less mature), and the specific integration point within your QC pipeline.

## Related tools

- **MSConvert** (converts vendor-format LC-MS acquisition files into open mzML format for downstream QC processing) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **Rapid QC-MS** (provides automated quality control checks and interactive data visualization; depends on MSConvert for vendor format data conversion) — https://github.com/czbiohub-sf/Rapid-QC-MS
- **MS-DIAL** (downstream data processing and identification following MSConvert conversion) — http://prime.psc.riken.jp/compms/msdial/main.html

## Evaluation signals

- Output mzML file is well-formed and parseable by standard mzML readers (no truncation or corruption).
- Spectral metadata invariants are preserved: total scan count, retention time range, and m/z value ranges match known characteristics of the input vendor file.
- Intensity values are non-zero and follow a realistic distribution (not all identical or all zero).
- MSConvert exit code is 0 and no warnings or errors are logged for the conversion step.
- Downstream QC pipeline (e.g., MS-DIAL) successfully ingests the mzML file without format errors or anomalies in identified features.

## Limitations

- Rapid QC-MS was designed for Windows platforms due to MSConvert dependency; MacOS users can monitor instrument runs but cannot process data via MSConvert.
- Extensive testing has been conducted only on Thermo Fisher mass spectrometers and Thermo RAW files; Agilent, Bruker, Sciex, and Waters vendor formats may have undiscovered bugs or integration issues.
- MSConvert must be installed manually; it is not automatically included in the Rapid QC-MS Python package installation.
- Conversion performance and metadata fidelity depend on MSConvert version and vendor API support; older or discontinued vendor formats may not convert reliably.

## Evidence

- [intro] its dependency on MSConvert for vendor format data conversion: "its dependency on MSConvert for vendor format data conversion"
- [other] Validate that the output mzML file is well-formed and contains expected spectral metadata (scan count, retention times, m/z values, intensities).: "Validate that the output mzML file is well-formed and contains expected spectral metadata (scan count, retention times, m/z values, intensities)."
- [readme] Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion"
- [readme] Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline, the package will work seamlessly with data of all vendor formats.: "Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline"
- [readme] However, Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files."
- [readme] Python dependencies are installed automatically, but dependencies such as MSConvert and MS-DIAL will need to be installed manually.: "Python dependencies are installed automatically, but dependencies such as MSConvert and MS-DIAL will need to be installed manually."
