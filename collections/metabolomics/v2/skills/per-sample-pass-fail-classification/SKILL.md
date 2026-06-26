---
name: per-sample-pass-fail-classification
description: Use when after LC-MS data acquisition is complete (or during real-time
  monitoring) and you have loaded processed LC-MS data in mzML or vendor format and
  defined QC criteria (retention time windows, m/z tolerances, intensity thresholds)
  for your internal standards and target analytes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# per-sample-pass-fail-classification

## Summary

Assign binary pass/fail status to individual LC-MS samples by aggregating automated and user-defined quality control checks against defined thresholds for internal standard detection, peak intensity, retention time, and mass accuracy. This skill ensures only high-quality runs proceed to downstream analysis.

## When to use

After LC-MS data acquisition is complete (or during real-time monitoring) and you have loaded processed LC-MS data in mzML or vendor format and defined QC criteria (retention time windows, m/z tolerances, intensity thresholds) for your internal standards and target analytes. Use this skill when you need a per-sample binary decision to flag failing runs before committing computational or experimental resources to downstream analysis.

## When NOT to use

- Input LC-MS data has not been converted to standardized format (mzML) and you lack MSConvert for vendor format conversion.
- QC criteria (retention time windows, m/z tolerances, intensity thresholds) have not been defined or validated against your instrument and analyte panel.
- You need detailed peak shape or isotope pattern quality assessment beyond retention time, m/z accuracy, and intensity thresholds.

## Inputs

- processed LC-MS data in mzML format or vendor raw format
- QC criteria configuration (retention time windows, m/z tolerances, intensity thresholds for internal standards and target analytes)
- user-defined QC rules and custom thresholds

## Outputs

- per-sample binary pass/fail status
- QC report with flagged violations and diagnostic metrics
- internal standard retention time, m/z, and intensity values per sample

## How to apply

Execute automated QC checks against each sample by verifying: (1) internal standard detection and presence, (2) peak intensity within acceptable range, (3) retention time within defined window, and (4) mass accuracy within tolerance. Then execute user-defined QC checks based on custom thresholds and rules supplied as configuration. Aggregate all check results and assign binary pass/fail status to each sample based on whether all checks pass or any violation is flagged. Export a QC report with per-sample pass/fail status, flagged violations, and diagnostic metrics (retention time, m/z, intensity values) to enable triage and investigation of failures.

## Related tools

- **MSConvert** (Convert vendor format raw mass spectrometry data to standardized mzML format before QC check execution) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Process and identify LC-MS data prior to QC classification workflow) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Automated and user-defined quality control checks during LC-MS instrument runs with real-time Slack/email notifications and interactive visualization) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Examples

```
rapidqcms
```

## Evaluation signals

- All samples with internal standard intensity above the defined threshold receive pass status; those below receive fail status.
- Samples with internal standard retention time within the defined window pass; those outside the window are flagged as failures.
- Mass accuracy of detected internal standard m/z is within the defined tolerance for pass samples; violations are recorded in the QC report.
- Each sample in the output report has exactly one binary status (pass or fail) and a list of specific violated QC criteria (if any).
- QC report diagnostic metrics (retention time, m/z, intensity per sample) are traceable back to the raw LC-MS data and match exported values from MSConvert or MS-DIAL output.

## Limitations

- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files; other vendor formats may have undetected bugs and compatibility issues.
- Pass/fail classification is binary and does not account for subtle data quality issues such as peak shape distortion, isotope ratio abnormalities, or chromatographic interference that do not cross defined intensity or retention time thresholds.
- Windows platform is required for full functionality including MSConvert and MS-DIAL integration; macOS users can only monitor and view results, not execute the full QC pipeline.
- QC criteria (retention time windows, m/z tolerances, intensity thresholds) must be manually defined and validated; inappropriate thresholds will produce misleading pass/fail assignments.

## Evidence

- [other] Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance.: "Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance."
- [other] Aggregate results and assign binary pass/fail status to each sample.: "Aggregate results and assign binary pass/fail status to each sample."
- [other] Export QC report with per-sample pass/fail status, flagged violations, and diagnostic metrics.: "Export QC report with per-sample pass/fail status, flagged violations, and diagnostic metrics."
- [readme] Automated and user-defined quality control checks during instrument runs: "Automated and user-defined quality control checks during instrument runs"
- [other] Execute user-defined QC checks based on custom thresholds and rules supplied as configuration.: "Execute user-defined QC checks based on custom thresholds and rules supplied as configuration."
- [readme] Interactive data visualization of internal standard retention time, m/z, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with processing data of other vendor formats.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with"
