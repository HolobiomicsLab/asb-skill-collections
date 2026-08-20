---
name: quality-metric-computation-from-mass-spectrometry-data
description: Use when you have raw DIA mass spectrometry files (.raw, .d, or .wiff
  format) from timsTOF, TripleTOF, or Orbitrap instruments and need to assess their
  quality before downstream proteomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msConvert
  - Python
  - DIA-NN
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# quality-metric-computation-from-mass-spectrometry-data

## Summary

Compute 15 quantitative metrics from DIA mass spectrometry files that characterize raw data quality across timsTOF, TripleTOF, and Orbitrap instruments. These metrics serve as input features for machine learning models to predict whether a DIA file meets quality standards.

## When to use

You have raw DIA mass spectrometry files (.raw, .d, or .wiff format) from timsTOF, TripleTOF, or Orbitrap instruments and need to assess their quality before downstream proteomics analysis. Apply this skill when you require structured, quantitative descriptors of precursor ion intensity distribution, chromatographic peak characteristics, and instrument-specific features to feed into quality prediction models or longitudinal monitoring dashboards.

## When NOT to use

- Input is already a pre-computed feature table or metrics matrix — skip to ML model prediction or quality assessment.
- Raw files are from data-independent acquisition (DIA) instruments not in the supported set (timsTOF, TripleTOF, Orbitrap) — instrument-specific features may not be meaningful.
- You need only summary statistics or visual inspection of individual chromatograms without quantitative feature vectors for modeling.

## Inputs

- Raw mass spectrometry DIA files (.raw, .d, or .wiff format from timsTOF, TripleTOF, or Orbitrap instruments)
- Extracted precursor ion chromatogram (PIC) files (output from msConvert conversion)

## Outputs

- Metrics table (CSV) with one row per file and 15 columns representing quality metrics
- Structured feature matrix suitable for machine learning model input

## How to apply

First, convert raw DIA files to extracted precursor ion chromatogram (PIC) format using msConvert. Load the converted PIC data into a Python environment. Compute all 15 quality-characterizing metrics from each file; these metrics capture precursor intensity distribution properties, chromatographic peak shape and elution characteristics, and instrument-specific signal features. Aggregate the metrics into a structured table with one row per file and one column per metric, ensuring consistent column ordering and data types across all files. Save the aggregated metrics table as CSV for downstream machine learning model input or quality visualization. Verify that all 15 metrics are present, non-null, and within expected ranges for your instrument type.

## Related tools

- **msConvert** (Convert raw DIA files to extracted precursor ion chromatogram (PIC) format prior to metric computation)
- **Python** (Load PIC data and compute 15 quality metrics; aggregate into structured metrics table)
- **DIA-NN** (Provides protein qualitative and quantitative algorithms integrated into iDIA-QC for quality assessment context)

## Evaluation signals

- All 15 metrics are present in the output CSV with no missing or NaN values per file.
- Metrics table has exactly N rows (one per input file) and exactly 15 columns with consistent, interpretable names.
- Metric values fall within expected ranges for the instrument type (e.g., precursor intensity metrics are non-negative; chromatographic peak width metrics are positive).
- Metrics table is machine-readable CSV with proper encoding and can be loaded without error into Python/R machine learning pipelines.
- Row and column order are consistent across repeated runs on the same input files.

## Limitations

- Metric extraction assumes proper conversion to PIC format; malformed or incomplete PIC files will produce spurious or missing metric values.
- The 15 metrics are instrument-specific and tuned for timsTOF, TripleTOF, and Orbitrap; application to other MS platforms may not be valid.
- Analysis time is under 5 minutes per file; very large batch computations may require parallelization outside the standard iDIA-QC GUI.
- Metrics characterize raw file properties but do not account for sample preparation, biological variability, or downstream data processing effects.

## Evidence

- [intro] The 15 metrics extracted from the DIA files that characterize raw data quality: "The iDIA-QC system extracts 15 metrics from DIA files to describe characteristics of raw files from timsTOF, TripleTOF, and Orbitrap instruments"
- [other] Conversion to PIC format and metric computation workflow: "Convert raw DIA files to extracted precursor ion chromatogram (PIC) format using msConvert. Load converted PIC data into Python environment. Compute 15 quality-characterizing metrics from each DIA"
- [intro] Metrics serve as ML model input features: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments, we"
- [readme] Supported input file formats and instruments: "This software supports the .raw, .d, and .wiff raw data formats. Choose the type of instrument that generated the file."
- [readme] Performance and scalability: "Analysis time per file is under 5 minutes."
