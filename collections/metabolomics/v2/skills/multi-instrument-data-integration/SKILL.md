---
name: multi-instrument-data-integration
description: Use when you have DIA mass spectrometry raw files from multiple instrument types (timsTOF, TripleTOF, Orbitrap) in their native formats (.raw, .d, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - msConvert
  - DIA-NN
derived_from:
- doi: 10.1038/s41467-024-54871-1
  title: iDIA-QC
evidence_spans:
- iDIA-QC is a Python Graphical User Interface (GUI)
- uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)
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
---

# multi-instrument-data-integration

## Summary

Integrate and standardize mass spectrometry DIA files from heterogeneous instrument platforms (timsTOF, TripleTOF, Orbitrap) into a unified analytical pipeline by converting raw formats to a common intermediate representation (PIC) and extracting instrument-agnostic quality metrics. This skill enables downstream quality prediction and longitudinal monitoring across a diverse instrument fleet.

## When to use

You have DIA mass spectrometry raw files from multiple instrument types (timsTOF, TripleTOF, Orbitrap) in their native formats (.raw, .d, .wiff) and need to apply a single machine learning quality classifier or generate comparative quality visualizations across instruments without re-training separate models per platform.

## When NOT to use

- Input files are already in PIC or mzML format — skip msConvert conversion and proceed directly to metric extraction.
- You need instrument-specific quality models — if instrument differences in quality drivers are significant, train separate classifiers per platform rather than forcing a unified model.
- Raw files are from a single instrument type — the integration overhead (instrument-agnostic feature engineering, format conversion validation) is unnecessary; use instrument-specific pipelines instead.

## Inputs

- Raw DIA mass spectrometry files in native formats (.raw for Orbitrap, .d for timsTOF, .wiff for TripleTOF)
- msConvert parameter configuration for PIC extraction
- Pre-trained machine learning model (fitted on 15-metric feature space)
- Instrument type identifier for each input file

## Outputs

- Extracted precursor ion chromatogram (PIC) files in standardized format
- 15-metric feature matrix with file identifiers and instrument labels
- Quality class predictions for each file (with confidence scores if applicable)
- Longitudinal summary visualizations aggregating quality across instruments

## How to apply

First, convert each raw DIA file to extracted precursor ion chromatogram (PIC) format using msConvert with instrument-specific parameters, validating output for format integrity. Second, extract the standardized 15-metric feature set from each PIC file, ensuring all metrics are computed identically regardless of source instrument. Third, normalize or scale the 15-metric matrix to account for instrument-specific signal ranges or mass calibration offsets. Fourth, apply the unified pre-trained machine learning model (trained on the pooled 15-metric feature space) to predict quality labels for each file. This approach relies on the principle that the 15 metrics capture instrument-independent characteristics of DIA quality (e.g., precursor intensity distribution, MS/MS spectral richness) rather than instrument-specific artifacts.

## Related tools

- **msConvert** (Converts raw DIA files from timsTOF, TripleTOF, and Orbitrap instruments into extracted precursor ion chromatogram (PIC) format, standardizing the intermediate file representation before metric extraction.)
- **DIA-NN** (Provides the protein qualitative and quantitative algorithms incorporated into iDIA-QC for downstream proteomics analysis following quality assessment.)
- **Python** (Environment for implementing the metric extraction, data normalization, machine learning model application, and output formatting steps within the iDIA-QC GUI framework.) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- All input raw files successfully converted to PIC format without errors; PIC files contain expected chromatogram peaks and retention time ranges.
- The 15-metric feature matrix has identical columns and units across all input files, with no missing values or NaN entries (after imputation if applied).
- Quality predictions are generated for 100% of input files; predicted class labels match the expected range (e.g., 'pass'/'fail' or 0–100 confidence score) with no null outputs.
- Longitudinal visualizations show consistent instrument representation (no instrument type missing from the aggregated summary) and temporal trends align with known instrument maintenance or calibration events.
- Cross-validation or held-out test accuracy of the unified model on files from all three instrument types is within expected bounds (reported in the article or compared to instrument-specific baseline models).

## Limitations

- The 15-metric feature set was derived from timsTOF, TripleTOF, and Orbitrap instruments; applicability to other DIA instruments or older instrument firmware versions is not validated.
- msConvert PIC extraction parameters may require tuning per instrument type (precursor m/z window, retention time binning); default parameters may not optimize quality metrics for all platforms.
- Machine learning model performance assumes the 15 metrics capture quality variation uniformly across instruments; systematic instrument biases in metric distributions could lead to instrument-specific prediction drift.
- The analysis time per file (~5 minutes) may scale non-linearly with large sample batches; computational resources (CPU, memory) are not specified.

## Evidence

- [readme] 15-metric extraction and multi-instrument support: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments"
- [readme] msConvert conversion to PIC: "uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)"
- [readme] Unified machine learning prediction across instruments: "we utilize machine learning models to predict the quality of the DIA files"
- [readme] Supported raw file formats by instrument: "This software supports the .raw, .d, and .wiff raw data formats"
- [readme] Longitudinal aggregation across instruments: "The outputs of iDIA-QC in a longitudinal summary, visually display the quality of the DIA files"
