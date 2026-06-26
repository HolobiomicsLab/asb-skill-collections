---
name: mass-spectrometry-qc-criteria-definition
description: 'Use when when setting up a new LC-MS QC workflow or modifying existing
  QC rules: you have access to internal standards and target analytes, know their
  expected retention times and m/z values, and need to establish pass/fail boundaries
  for sample acceptance before or concurrent with instrument runs.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS-DIAL
  - MSConvert
  - Rapid QC-MS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-qc-criteria-definition

## Summary

Define quantitative quality control criteria for LC-MS runs by specifying acceptance thresholds for internal standard detection, peak intensity, retention time windows, and mass accuracy. This skill enables automated and user-defined QC checks to flag failing samples during or after data acquisition.

## When to use

When setting up a new LC-MS QC workflow or modifying existing QC rules: you have access to internal standards and target analytes, know their expected retention times and m/z values, and need to establish pass/fail boundaries for sample acceptance before or concurrent with instrument runs.

## When NOT to use

- Input data are already QC-passed or curated; criteria definition is not needed for validation of known-good samples.
- No internal standards or reference compounds are available for the LC-MS method; criteria cannot be anchored to reliable calibration points.
- The analysis requires post-hoc statistical filtering (e.g., sample abundance filtering or outlier detection) rather than instrument-level acceptance thresholds.

## Inputs

- Processed LC-MS data (mzML or vendor format .raw files)
- Internal standard compound identifiers and expected m/z values
- Target analyte m/z values or compound lists
- QC configuration file specifying retention time windows, m/z tolerances, and intensity thresholds

## Outputs

- QC report with per-sample pass/fail status
- Flagged QC violations (retention time drift, mass accuracy deviation, intensity out of range)
- Diagnostic metrics (detected m/z, observed retention time, peak intensity per sample)
- Optional: Slack or email notifications for QC failures

## How to apply

Load processed LC-MS data (mzML or vendor format via MSConvert) and define QC criteria as configuration parameters: (1) specify retention time windows for internal standards and target analytes; (2) set m/z tolerances (ppm) for mass accuracy; (3) establish intensity thresholds for peak detection and internal standard presence; (4) optionally configure custom user-defined rules beyond automated checks. During QC execution, the system verifies each sample against these thresholds: internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance. Aggregate results assign binary pass/fail status per sample.

## Related tools

- **MSConvert** (Converts vendor-format LC-MS raw data (e.g., Thermo .raw) to standardized mzML format for QC criteria evaluation) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Performs data processing and peak identification prior to QC criteria application) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Orchestrates QC criteria definition, automated/user-defined checks, and real-time reporting against LC-MS runs) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Evaluation signals

- QC criteria are measurable and reproducible: retention time windows ±tolerance, m/z tolerance in ppm, intensity threshold in absolute or relative units.
- All samples in the QC report have binary pass/fail assignment; no samples lack a status.
- Flagged violations are traceable to specific criteria boundaries (e.g., 'internal standard m/z 447.2 not detected within ±5 ppm' or 'retention time 8.2 min outside window 7.9–8.1 min').
- Pass/fail status correlates with downstream data utility: samples marked fail show known problems (e.g., drift, contamination, instrument malfunction) and would benefit from re-analysis or exclusion.
- User-defined custom rules in configuration file are applied consistently across the sample batch without omission or conflict.

## Limitations

- Criteria definition requires a priori knowledge of internal standard m/z, retention time, and expected intensity range; criteria cannot be derived de novo from data alone.
- Rapid QC-MS has been tested extensively on Thermo Fisher mass spectrometers and Thermo .raw files; behavior on Agilent, Bruker, Sciex, or Waters formats may include bugs or unsupported workflows.
- Criteria are method-specific and instrument-specific; transfer between different LC-MS instruments, columns, or mobile phases requires re-validation and possible threshold adjustment.
- QC checks operate on peak-level and compound-level metrics; they do not detect all sources of run failure (e.g., gradient malfunction, detector saturation, or systematic bias in untargeted detection).

## Evidence

- [other] Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes.: "Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes."
- [other] Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance.: "Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance."
- [readme] Automated and user-defined quality control checks during instrument runs: "Automated and user-defined quality control checks during instrument runs"
- [readme] Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline: "Because MSConvert converts raw acquired data into open mzML format before routing it to the data processing pipeline"
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with processing data of other vendor formats.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with"
