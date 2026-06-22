---
name: internal-standard-peak-detection-and-validation
description: Use when you have loaded processed LC-MS data (mzML or vendor format) and need to establish baseline instrument performance before evaluating sample analytes. Use it at the start of each LC-MS batch or run to ensure that internal standard detection passes predefined thresholds;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS-DIAL
  - MSConvert
  - Rapid QC-MS
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans:
- and MS-DIAL
- '[MS-DIAL](http://prime.psc.riken'
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

# internal-standard-peak-detection-and-validation

## Summary

Automated detection and validation of internal standard peaks in LC-MS runs to confirm instrument performance and data quality. This skill verifies that internal standards are present, detected within expected retention time windows, possess sufficient intensity, and meet mass accuracy tolerances—critical prerequisites for trusting downstream QC decisions on sample data.

## When to use

Apply this skill when you have loaded processed LC-MS data (mzML or vendor format) and need to establish baseline instrument performance before evaluating sample analytes. Use it at the start of each LC-MS batch or run to ensure that internal standard detection passes predefined thresholds; failure here indicates instrument malfunction or data acquisition problems that should halt downstream analysis.

## When NOT to use

- Input data does not include internal standards (e.g., discovery metabolomics without spiked standards).
- You are performing targeted analysis where internal standard validation is already handled upstream by the instrument's built-in QC.
- Retention time windows and m/z tolerances have not been experimentally established or calibrated for your instrument and method.

## Inputs

- Processed LC-MS data in mzML format or vendor raw format (e.g., Thermo .raw)
- Internal standard definition file (m/z values, expected retention times, compound names)
- QC configuration (retention time windows, m/z tolerance in ppm, intensity thresholds)

## Outputs

- Per-sample internal standard detection status (detected/not detected)
- Per-sample internal standard peak metrics (observed m/z, retention time, intensity)
- Per-sample pass/fail status for internal standard validation
- Diagnostic report flagging retention time drift, mass accuracy failures, or intensity anomalies

## How to apply

After converting vendor format data to standardized mzML using MSConvert if necessary, define QC criteria specific to your internal standards: retention time windows (e.g., ±0.5 min around expected RT), m/z tolerance (e.g., ±5 ppm mass accuracy), and acceptable intensity thresholds. Execute automated checks that verify internal standard detection, peak intensity within the acceptable range, retention time within the defined window, and mass accuracy within tolerance for each sample. Aggregate results across the batch and flag any samples where one or more internal standards fail these checks. Use these pass/fail results to gate downstream sample analyte evaluation—samples with failed internal standards should not proceed to user-defined QC checks or be marked as valid.

## Related tools

- **MSConvert** (Converts vendor-specific LC-MS raw data formats (e.g., Thermo .raw) to standardized mzML format before internal standard peak detection) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Processes and identifies LC-MS data peaks, enabling extraction of internal standard m/z, retention time, and intensity values for validation) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Automated QC orchestration platform that executes internal standard detection and validation checks during and after LC-MS instrument runs, aggregates results, and triggers alerts) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Evaluation signals

- All internal standards are detected in each sample (binary presence check passes)
- Observed m/z for each internal standard falls within the specified tolerance (e.g., ±5 ppm of theoretical m/z)
- Detected retention time for each internal standard falls within the predefined window (e.g., expected RT ± tolerance window)
- Peak intensity for each internal standard exceeds the minimum threshold and remains stable across the batch (low run-to-run variation)
- No samples are marked as passed without successful detection of all required internal standards

## Limitations

- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers and Thermo RAW files; bugs and issues may occur with other vendor formats (Agilent, Bruker, Sciex, Waters), though MSConvert conversion provides theoretical universal support.
- Internal standard validation requires experimentally determined and instrument-specific retention time windows and m/z tolerances; incorrect thresholds will produce false positives or false negatives.
- The skill assumes internal standards are present in the sample preparation; it cannot detect issues upstream of data acquisition (e.g., internal standard not added to the sample).
- Mass accuracy and retention time drift over long instrument runs may require periodic recalibration of QC criteria thresholds.

## Evidence

- [other] Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes.: "Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes."
- [other] Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance.: "Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance."
- [readme] Automated and user-defined quality control checks during instrument runs: "Automated and user-defined quality control checks during instrument runs"
- [readme] its dependency on MSConvert for vendor format data conversion: "its dependency on MSConvert for vendor format data conversion"
- [readme] However, Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files.: "However, Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files."
