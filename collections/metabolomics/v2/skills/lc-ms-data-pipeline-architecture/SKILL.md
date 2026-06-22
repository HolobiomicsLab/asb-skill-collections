---
name: lc-ms-data-pipeline-architecture
description: Use when you have vendor-format LC-MS acquisition files (.raw, .d, .ms) from instrument runs and need to set up an end-to-end data quality control system that converts proprietary formats into open mzML, processes spectral data, and surfaces QC failures in real time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MSConvert
  - MS-DIAL
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS data pipeline architecture

## Summary

Design and implement a modular LC-MS data processing pipeline that chains vendor format conversion (via MSConvert), data processing and identification (via MS-DIAL), and real-time quality control checks into a unified workflow. This skill is essential for automating vendor-agnostic acquisition data into open formats and routing it through downstream analytical tools.

## When to use

You have vendor-format LC-MS acquisition files (.raw, .d, .ms) from instrument runs and need to set up an end-to-end data quality control system that converts proprietary formats into open mzML, processes spectral data, and surfaces QC failures in real time. This is particularly relevant during active instrument runs where early detection of acquisition drift, internal standard degradation, or retention time shifts can prevent data loss.

## When NOT to use

- Input data is already in open mzML or other non-proprietary mass spectrometry formats — skip MSConvert conversion and route directly to MS-DIAL.
- You are running on MacOS and need to perform automated data processing; Rapid QC-MS on MacOS is limited to monitoring and viewing only, not conversion or processing.
- Your workflow requires support for vendor formats other than Thermo Fisher, which have not been extensively tested; expect potential bugs with Agilent, Bruker, Sciex, or Waters data.

## Inputs

- Vendor-format LC-MS acquisition files (.raw, .d, .ms from Thermo Fisher, Agilent, Bruker, Sciex, or Waters)
- MSConvert executable or module reference
- MS-DIAL executable or module reference
- QC parameter configuration (retention time ranges, m/z tolerance, intensity thresholds, internal standard identities)

## Outputs

- mzML-formatted spectral data files (open format, vendor-agnostic)
- Processed and identified data output from MS-DIAL
- QC result reports (pass/fail status per sample)
- Real-time notifications (Slack messages, email alerts) on QC failures
- Interactive visualization dashboard of internal standard retention time, m/z, and intensity trends across samples

## How to apply

First, confirm MSConvert and MS-DIAL are installed and available in the system PATH or as standalone modules on your Windows platform (MacOS can monitor but not process). Second, design a wrapper architecture that invokes MSConvert as the input-preparation step, accepting vendor acquisition files and outputting mzML files compatible with downstream tools. Third, chain the mzML output into MS-DIAL for data processing and identification. Fourth, integrate automated and user-defined QC checks (e.g., internal standard retention time, m/z, intensity thresholds) that execute after each conversion and processing step. Fifth, route QC results and failures to external notification systems (Slack, email) and interactive visualization dashboards (Plotly Dash) for real-time monitoring. Validate that the output mzML files are well-formed and contain expected spectral metadata (scan count, retention times, m/z values, intensities) before marking conversion successful.

## Related tools

- **MSConvert** (Converts vendor-format LC-MS acquisition files into open mzML format as the first step of the pipeline) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Processes mzML spectral data and performs data identification downstream of MSConvert conversion) — http://prime.psc.riken.jp/compms/msdial/main.html

## Examples

```
rapidqcms
```

## Evaluation signals

- Output mzML files are well-formed and pass schema validation; confirm presence of expected spectral metadata: scan count, retention times, m/z values, and intensities match the vendor acquisition file.
- MSConvert conversion completes without errors and mzML file size is proportional to the input vendor file (no truncation or data loss).
- MS-DIAL successfully processes the output mzML files without crashing; identified compounds and peak lists are generated.
- QC thresholds are evaluated correctly: internal standard retention time drift, m/z deviation, and intensity drop-off are detected and flagged according to configured parameters.
- Real-time notifications are triggered and delivered to Slack/email when QC fails; notifications contain sample ID, failed QC metric, and observed vs. expected values.

## Limitations

- Rapid QC-MS is designed for and extensively tested only on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files; other vendor formats (Agilent, Bruker, Sciex, Waters) are expected to have bugs and issues.
- Windows platform is required for automated data conversion and processing due to MSConvert and MS-DIAL dependencies; MacOS users can only monitor and view results.
- Python 3.8 to 3.11 is required; compatibility with newer Python versions is not guaranteed.
- Installation of MSConvert and MS-DIAL must be performed manually; they are not installed automatically during Rapid QC-MS setup.

## Evidence

- [intro] its dependency on MSConvert for vendor format data conversion: "its dependency on MSConvert for vendor format data conversion"
- [readme] Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification.: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification."
- [readme] MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline: "MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline"
- [other] Validate that the output mzML file is well-formed and contains expected spectral metadata (scan count, retention times, m/z values, intensities).: "Validate that the output mzML file is well-formed and contains expected spectral metadata (scan count, retention times, m/z values, intensities)."
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files"
- [intro] Automated and user-defined quality control checks during instrument runs: "Automated and user-defined quality control checks during instrument runs"
