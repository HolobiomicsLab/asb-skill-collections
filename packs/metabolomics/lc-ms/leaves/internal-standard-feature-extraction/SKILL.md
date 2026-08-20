---
name: internal-standard-feature-extraction
description: Use when you have processed LC-MS run data (feature table or peak detection output) containing internal standard identifications and need to monitor internal standard retention time, m/z, and intensity variation across samples as part of automated or user-defined QC checks during instrument runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - MSConvert
  - MS-DIAL
  - Pandas
  techniques:
  - LC-MS
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

# internal-standard-feature-extraction

## Summary

Extract and isolate internal standard peaks from processed LC-MS feature tables by matching known m/z and retention time windows, enabling quality control assessment of instrument performance across samples. This skill is essential for verifying consistency of internal standard signals in untargeted metabolomics workflows.

## When to use

Apply this skill when you have processed LC-MS run data (feature table or peak detection output) containing internal standard identifications and need to monitor internal standard retention time, m/z, and intensity variation across samples as part of automated or user-defined QC checks during instrument runs.

## When NOT to use

- Input data is raw vendor format (.raw, .d, .yep files)—convert to mzML using MSConvert first.
- No internal standards were spiked into the samples or their m/z and retention time windows are not known.
- Goal is to identify unknown metabolites; internal standard extraction is a QC-specific task.

## Inputs

- processed LC-MS feature table or peak detection output (tabular format with columns: m/z, retention time, intensity, sample identifier)
- internal standard reference list (known m/z values, retention time ranges, and identifiers for each internal standard compound)

## Outputs

- filtered feature table containing only internal standard peaks across all samples
- internal standard intensity matrix (samples × internal standards) with retention times and m/z values

## How to apply

Load processed LC-MS data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements. Define or retrieve known m/z and retention time windows for your internal standards (these are typically experiment-specific reference values established during method validation). Filter or subset the feature table to isolate peaks matching these m/z and retention time windows—this reduces false matches by excluding off-target peaks. Retain all sample identities and their associated intensity measurements for the matched internal standard peaks. The rationale is that internal standards should appear at consistent retention times and m/z values across all samples; deviations indicate instrument drift, column degradation, or data acquisition problems that warrant investigation or automated alerts.

## Related tools

- **MSConvert** (vendor format data conversion prior to feature extraction; enables uniform mzML input) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (data processing and peak detection to generate feature table input) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Pandas** (tabular data filtering and subsetting to isolate internal standard peaks)

## Evaluation signals

- All internal standard peaks appear at retention times within ±0.5–1.0 min of expected windows across samples (exact tolerance depends on method).
- Extracted internal standard m/z values match reference list within instrument mass accuracy (typically <5 ppm for high-resolution MS).
- Intensity coefficient of variation (CV) for each internal standard across samples is <20% (or experiment-specific threshold); high CV flags potential QC issues.
- No features outside the defined m/z and retention time windows are included in the filtered output (verify by spot-checking edge cases).
- Feature table row count after filtering equals (number of samples × number of internal standards), or fewer if some samples lack certain internal standards.

## Limitations

- Extraction accuracy depends on accurate reference m/z and retention time windows; misalignment (e.g., due to column degradation or method drift) can cause internal standard peaks to fall outside windows and be missed.
- Does not account for isobaric or co-eluting compounds; if another metabolite has identical m/z and similar retention time to an internal standard, it may be incorrectly included.
- Requires prior knowledge of internal standard identities and their expected chromatographic properties; cannot be used for exploratory internal standard discovery.
- Rapid QC-MS has been tested extensively on Thermo Fisher mass spectrometers; results may vary with other vendor instruments.

## Evidence

- [other] Load processed LC-MS run data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements across samples.: "Load processed LC-MS run data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements across samples."
- [other] Filter or subset data to isolate internal standard peaks by matching known m/z and retention time windows.: "Filter or subset data to isolate internal standard peaks by matching known m/z and retention time windows."
- [other] Rapid QC-MS provides interactive data visualization of internal standard retention time, m/z, and intensity across samples as a key feature for streamlining untargeted metabolomics research.: "Rapid QC-MS provides interactive data visualization of internal standard retention time, m/z, and intensity across samples"
- [readme] Automated and user-defined quality control checks during instrument runs.: "Automated and user-defined quality control checks during instrument runs"
- [readme] its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification.: "its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification"
