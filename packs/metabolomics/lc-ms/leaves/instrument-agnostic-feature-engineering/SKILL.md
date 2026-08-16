---
name: instrument-agnostic-feature-engineering
description: Use when you have DIA raw mass spectrometry files from multiple instrument types (timsTOF, TripleTOF, Orbitrap) and need to build a single machine learning model to predict data quality across all platforms, or when you need to compare quality characteristics of files produced by different.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msConvert
  - Python
  - DIA-NN
  - iDIA-QC
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1038/s41467-024-54871-1
  title: iDIA-QC
evidence_spans:
- uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)
- iDIA-QC is a Python Graphical User Interface (GUI)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idia_qc_cq
    doi: 10.1038/s41467-024-54871-1
    title: iDIA-QC
  dedup_kept_from: coll_idia_qc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-54871-1
  all_source_dois:
  - 10.1038/s41467-024-54871-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# instrument-agnostic-feature-engineering

## Summary

Extract a standardized set of 15 quality metrics from DIA mass spectrometry files across heterogeneous instrument platforms (timsTOF, TripleTOF, Orbitrap) to enable machine learning-based quality prediction independent of instrument vendor or acquisition mode. This skill transforms raw instrument-specific DIA data into a unified feature space suitable for downstream ML model training and cross-platform quality assessment.

## When to use

Apply this skill when you have DIA raw mass spectrometry files from multiple instrument types (timsTOF, TripleTOF, Orbitrap) and need to build a single machine learning model to predict data quality across all platforms, or when you need to compare quality characteristics of files produced by different instruments in a standardized way.

## When NOT to use

- Input data are already in pre-computed feature or aggregated form (e.g., already a feature table or quality score matrix).
- Raw files are from targeted MS/MS or untargeted LC-MS/MS acquisition modes rather than DIA.
- You need instrument-specific tuning parameters or vendor-specific performance diagnostics rather than a unified quality assessment.

## Inputs

- DIA raw mass spectrometry files (.raw, .d, .wiff formats from timsTOF, TripleTOF, or Orbitrap instruments)
- Extracted precursor ion chromatogram (PIC) data (post-msConvert conversion)

## Outputs

- Structured metrics table (CSV format, one row per file, 15 columns representing quality metrics)
- Feature vectors suitable for machine learning model input

## How to apply

Convert raw DIA files (.raw, .d, .wiff formats) to extracted precursor ion chromatogram (PIC) format using msConvert. Load the converted PIC data into a Python environment and compute 15 quality-characterizing metrics from each file, including measures of precursor intensity distribution, chromatographic peak characteristics, and instrument-specific features. Aggregate the computed metrics into a structured table with one row per file and one column per metric. The metrics are instrument-agnostic—derived from common precursor ion intensity and chromatographic properties rather than vendor-specific parameters—enabling direct comparison across timsTOF, TripleTOF, and Orbitrap instruments. Save the resulting metrics table as CSV for use as input features to machine learning models that predict overall file quality.

## Related tools

- **msConvert** (Converts raw DIA files to extracted precursor ion chromatogram (PIC) format as the first step in metric computation)
- **Python** (Core environment for loading PIC data and computing the 15 quality metrics from each file)
- **DIA-NN** (Provides protein qualitative and quantitative algorithms incorporated into iDIA-QC for quality assessment)
- **iDIA-QC** (Python GUI that implements this skill, automating metric extraction and ML-based quality prediction across multiple DIA files) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- Metrics table has exactly 15 columns and one row per input file, with no missing values.
- Metrics are numeric and fall within expected ranges for precursor intensity distribution (e.g., non-negative, bounded by instrument dynamic range) and chromatographic properties (e.g., peak width in seconds, retention time in minutes).
- The same 15 metrics are computed and reported consistently across files from timsTOF, TripleTOF, and Orbitrap instruments, confirming instrument-agnostic derivation.
- Downstream machine learning model trained on the metrics table achieves expected predictive performance on held-out DIA files from multiple instruments, validating that the feature representation is generalizable.
- Manual inspection of chromatographic metrics (e.g., precursor intensity distribution statistics) align with visual assessment of the original PIC data.

## Limitations

- Metric extraction requires successful conversion to PIC format using msConvert; files that fail conversion or produce malformed PIC data will not yield valid metrics.
- The 15 metrics are derived from precursor ion properties and chromatographic characteristics; instrument-specific hardware failures or acquisition anomalies may not be captured if they do not perturb these properties.
- Metric ranges and expected distributions may differ across instrument platforms (timsTOF, TripleTOF, Orbitrap) due to differences in mass resolution, dynamic range, and ion optics, which could affect model generalization across platforms.
- Analysis time per file is under 5 minutes, but processing large batches of hundreds or thousands of files may require distributed or parallelized execution.

## Evidence

- [readme] Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments"
- [readme] uses msConvert for file conversion to extracted precursor ion chromatogram (PIC): "uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)"
- [other] Compute 15 quality-characterizing metrics from each DIA file (including measures of precursor intensity distribution, chromatographic peak characteristics, and instrument-specific features): "Compute 15 quality-characterizing metrics from each DIA file (including measures of precursor intensity distribution, chromatographic peak characteristics, and instrument-specific features)"
- [other] Aggregate metrics into a structured table with one row per file and one column per metric. 5. Save metrics table as CSV.: "Aggregate metrics into a structured table with one row per file and one column per metric. 5. Save metrics table as CSV"
- [readme] we utilize machine learning models to predict the quality of the DIA files: "we utilize machine learning models to predict the quality of the DIA files"
