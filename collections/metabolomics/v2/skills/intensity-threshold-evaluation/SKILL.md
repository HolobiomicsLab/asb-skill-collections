---
name: intensity-threshold-evaluation
description: Use when you have processed LC-MS data (mzML or vendor format) and need
  to validate that internal standards and target analytes produce peak intensities
  within expected operational ranges.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
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

# intensity-threshold-evaluation

## Summary

Automated assessment of LC-MS peak intensity against user-defined or instrument-specific acceptable ranges to flag samples with weak or anomalous signals. This skill is essential for detecting failed or compromised LC-MS runs before downstream analysis, ensuring only high-quality metabolomics data proceeds.

## When to use

Apply this skill when you have processed LC-MS data (mzML or vendor format) and need to validate that internal standards and target analytes produce peak intensities within expected operational ranges. Use it during or immediately after LC-MS data acquisition to catch instrument drift, sample degradation, or detector malfunction before committing time to downstream analysis.

## When NOT to use

- Input is raw, unprocessed instrument data without peak detection or peak intensity extraction — apply peak detection first (e.g., MS-DIAL).
- You lack a priori knowledge of expected intensity ranges for your analytes and instrument — establish reference baselines from known-good runs before deploying intensity thresholds.
- The analysis goal is identification or quantification and intensity is already been quality-controlled upstream — do not re-apply this skill redundantly.

## Inputs

- Processed LC-MS data in mzML or vendor format (.raw, .d, etc.)
- QC criteria configuration (JSON or CSV) specifying intensity thresholds for internal standards and target analytes
- Extracted peak intensity values per sample (from MS-DIAL or equivalent peak detection)

## Outputs

- Per-sample QC pass/fail status based on intensity validation
- Flagged violations report listing samples with out-of-range intensities
- Diagnostic metrics (observed intensity, threshold bounds, violation magnitude)
- Interactive visualization of internal standard intensity across samples

## How to apply

Load processed LC-MS data and define intensity thresholds as part of QC criteria configuration, specifying acceptable minimum and maximum intensity bounds for internal standards and target analytes. Execute automated checks that compare observed peak intensity for each sample against these thresholds. Aggregate results per sample and flag those with intensities outside the defined range as QC violations. The rationale is that intensity deviations signal instrumental problems or sample preparation failures; by catching these early, you avoid wasting resources on analysis of degraded or compromised data.

## Related tools

- **MS-DIAL** (Peak detection and intensity extraction from LC-MS data prior to threshold evaluation) — http://prime.psc.riken.jp/compms/msdial/main.html
- **MSConvert** (Vendor format data conversion to standardized mzML format for platform-agnostic processing) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **Rapid QC-MS** (End-to-end framework for defining, executing, and visualizing intensity-based QC checks during LC-MS runs) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Examples

```
rapidqcms
```

## Evaluation signals

- Verify that all samples receive a binary pass/fail status with no missing or ambiguous assignments.
- Check that intensity violations are correctly identified: samples with observed intensity < minimum threshold or > maximum threshold are flagged; those within range pass.
- Confirm that flagged violations include the observed intensity value, threshold bounds, and sample identifier so violations are traceable.
- Validate that the interactive visualization plots internal standard intensity across all samples and matches the per-sample pass/fail decisions.
- Compare QC results to known instrument performance history or reference standards; samples flagged as failing intensity checks should correlate with periods of instrument drift or known sample degradation.

## Limitations

- Intensity thresholds must be manually defined or derived from baseline runs; no universal thresholds exist across instrument models, vendors, or metabolite classes. Misspecified thresholds lead to false positives or false negatives.
- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers and Thermo RAW files; intensity evaluation on Agilent, Bruker, Sciex, or Waters data may encounter untested edge cases or bugs.
- Intensity thresholds are static per QC job; they do not adapt to gradual instrument drift or seasonal variation. Periodic review and recalibration of thresholds is necessary.
- The skill operates post-acquisition; it cannot prevent collection of out-of-threshold data, only flag it after the fact for review or exclusion.

## Evidence

- [other] Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes.: "Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes."
- [other] Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance.: "Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance."
- [readme] Interactive data visualization of internal standard retention time, m/z, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [other] Rapid QC-MS provides automated and user-defined quality control checks during LC-MS instrument runs, both during and after data acquisition, to evaluate run quality.: "Rapid QC-MS performs automated and user-defined quality control checks during LC-MS instrument runs, both during and after data acquisition, to evaluate run quality."
- [readme] Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with processing data of other vendor formats.: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with"
