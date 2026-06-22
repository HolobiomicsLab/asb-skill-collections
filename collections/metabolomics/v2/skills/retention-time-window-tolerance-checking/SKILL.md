---
name: retention-time-window-tolerance-checking
description: 'Use when you have acquired LC-MS data and need to verify run quality before proceeding to metabolite identification or quantification. Retention time checking is essential when: (1) you have established expected retention time ranges for known internal standards or reference compounds;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-DIAL
  - MSConvert
  - Rapid QC-MS
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

# retention-time-window-tolerance-checking

## Summary

Automated verification that internal standards and target analytes elute within user-defined retention time windows during LC-MS analysis, as a core QC checkpoint for flagging runs with chromatographic drift or peak misidentification. This skill detects retention time violations that indicate instrument malfunction, column degradation, or sample preparation issues.

## When to use

Apply this skill when you have acquired LC-MS data and need to verify run quality before proceeding to metabolite identification or quantification. Retention time checking is essential when: (1) you have established expected retention time ranges for known internal standards or reference compounds; (2) you need to detect chromatographic drift across a sample batch; (3) you want to flag runs where peaks appear outside their expected elution windows, suggesting column problems or injection failures.

## When NOT to use

- Untargeted discovery experiments where no reference retention times are available for the analytes of interest.
- Data from instruments with known chromatographic instability that makes fixed retention time windows unreliable within a single batch.
- Already-processed feature tables or integrated peak lists where original retention time data has been discarded.

## Inputs

- Processed LC-MS data (mzML format or vendor-specific raw files)
- Retention time window definitions (compound name, expected retention time, tolerance bounds in minutes)
- Internal standard or target analyte list with assigned m/z and retention time expectations

## Outputs

- Per-sample retention time pass/fail status
- Flagged retention time violations (compound, expected window, observed retention time)
- QC report with retention time diagnostic metrics across sample batch

## How to apply

Load processed LC-MS data in mzML or vendor format (converting via MSConvert if necessary). Define retention time windows for each internal standard and target analyte—these windows typically reflect ±tolerance around a reference retention time established from prior calibration runs. During or after data acquisition, execute automated checks that extract the detected retention time for each compound from the processed data and compare it against the defined window bounds. Aggregate results per sample: a sample passes if all monitored compounds fall within their respective windows; flag violations when any compound's retention time falls outside its window. Export per-sample pass/fail status with flagged violations and actual retention times for diagnostic review.

## Related tools

- **MSConvert** (Vendor format data conversion to standardized mzML format prior to retention time checking) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Data processing and peak detection to extract retention time values for QC evaluation) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Complete QC orchestration platform that implements and automates retention time window checking with interactive visualization and real-time alerts) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Examples

```
rapidqcms
```

## Evaluation signals

- All internal standards in passing samples have retention times within their defined windows; violations are consistently flagged in failing samples.
- Retention time pass/fail decisions are reproducible across re-runs of the same raw data with identical window definitions.
- QC report retention time metrics (mean, min, max, standard deviation across batch) show expected clustering for samples from same instrument session; outliers correspond to flagged failures.
- Samples flagged for retention time violations can be manually inspected in raw chromatographic data to confirm peak position outside window bounds.
- Trend analysis of retention times across sequential samples reveals monotonic drift or sudden shifts that correlate with known maintenance events or column age.

## Limitations

- Retention time windows must be pre-established from calibration runs or prior knowledge; the method cannot auto-discover appropriate windows for novel compounds.
- Fixed retention time windows assume stable chromatographic conditions within a batch; significant column degradation or temperature drift can render windows too narrow, causing false failures.
- Thermo Fisher mass spectrometers and RAW file format have been extensively tested; other vendor formats (Agilent, Bruker, Sciex, Waters) may exhibit bugs or incompatibilities in retention time extraction.
- Requires manual installation of MSConvert and MS-DIAL dependencies; Windows platform is required for full functionality, though MacOS users can view results.
- Retention time checking alone cannot distinguish between true peak misidentification and legitimate chromatographic variance; integration with m/z accuracy and intensity checks is recommended for robust QC.

## Evidence

- [other] Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes.: "Define QC criteria (retention time windows, m/z tolerances, intensity thresholds) for internal standards and target analytes."
- [other] Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance.: "Execute automated QC checks against each sample: verify internal standard detection, peak intensity within acceptable range, retention time within defined window, and mass accuracy within tolerance."
- [readme] Rapid QC-MS provides automated and user-defined quality control checks during LC-MS instrument runs: "Automated and user-defined quality control checks during instrument runs"
- [readme] Interactive data visualization of internal standard retention time, m/z, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [readme] Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification.: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing"
