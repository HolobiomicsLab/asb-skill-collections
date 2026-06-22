---
name: mass-spectrometry-metric-engineering
description: Use when you have raw DIA mass spectrometry files (.raw, .d, .wiff formats) from timsTOF, TripleTOF, or Orbitrap instruments and need to quantify file quality for automated quality control, longitudinal instrument monitoring, or training a quality prediction classifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - msConvert
  - DIA-NN
  - iDIA-QC
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1038/s41467-024-54871-1
  title: iDIA-QC
evidence_spans:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metric-engineering

## Summary

Extract and engineer 15 quality-predictive metrics from DIA mass spectrometry raw files (timsTOF, TripleTOF, Orbitrap formats) to characterize instrument performance and file quality for downstream machine learning classification. This skill bridges raw data acquisition and quality prediction by systematizing the computation of interpretable, instrument-agnostic metrics.

## When to use

Apply this skill when you have raw DIA mass spectrometry files (.raw, .d, .wiff formats) from timsTOF, TripleTOF, or Orbitrap instruments and need to quantify file quality for automated quality control, longitudinal instrument monitoring, or training a quality prediction classifier. Use when manual per-file inspection is infeasible and you require standardized, comparable metrics across multiple instrument types and acquisition runs.

## When NOT to use

- Input is already a pre-computed feature matrix or quality label — skip directly to model training.
- Raw files are from untested instrument platforms not covered by the 15-metric specification (e.g., MALDI, ESI-FTICR, or other non-DIA ionization schemes).
- Analysis goal is exploratory data visualization without the need for downstream ML-based quality prediction.

## Inputs

- Raw DIA mass spectrometry files in .raw (Orbitrap), .d (timsTOF), or .wiff (TripleTOF) format
- Extracted precursor ion chromatogram (PIC) data (post-msConvert conversion)
- Instrument type identifier (timsTOF, TripleTOF, or Orbitrap)

## Outputs

- 15-dimensional metric vector per DIA file
- Structured metric matrix (rows=files, columns=15 metrics, values=metric scores)
- File identifier and metadata paired with corresponding metric row

## How to apply

After converting raw files to extracted precursor ion chromatogram (PIC) format using msConvert, systematically compute the 15 metrics that characterize DIA file quality. These metrics capture intensity, chromatographic, and spectral features specific to DIA acquisition. Ensure metrics are computed consistently across all three instrument platforms (timsTOF, TripleTOF, Orbitrap) using instrument-aware normalization or platform-specific extraction logic. Validate that each metric is calculable from the PIC data without requiring external reference spectra. Store computed metrics in a structured tabular format (row per file, column per metric) suitable for machine learning ingestion. Quality check for missing values or outliers before feature matrix construction.

## Related tools

- **msConvert** (Converts raw DIA files to extracted precursor ion chromatogram (PIC) format as input to metric extraction)
- **DIA-NN** (Provides protein qualitative and quantitative algorithms incorporated into iDIA-QC for DIA data analysis)
- **iDIA-QC** (Python GUI that orchestrates metric extraction, quality prediction, and longitudinal visualization) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- All 15 metrics are numerically computable and non-null for ≥95% of input files; missing values are documented and handled consistently.
- Metric values are comparable across the three instrument platforms (timsTOF, TripleTOF, Orbitrap) — no platform shows extreme skew or scale drift in distributions.
- Computed metrics correlate with known quality issues (e.g., files with known instrument malfunction show expected metric anomalies).
- Metric matrix dimensions match expected shape (N files × 15 metrics) and file identifiers are preserved and traceable to raw input files.
- Metrics exhibit sufficient variance (not constant or near-constant) to serve as discriminative features for ML classification of quality labels.

## Limitations

- The 15-metric specification is optimized for DIA data from timsTOF, TripleTOF, and Orbitrap instruments; application to other MS platforms or ionization modes is not validated.
- Metric computation requires successful file conversion to PIC format via msConvert; files that fail conversion cannot be metricated.
- No explicit guidance provided in the source material on handling instrument-specific calibration drift or systematic metric biases across time; longitudinal stability of metrics is assumed but not empirically characterized.
- Outlier detection and handling strategy for metric values is not specified; practitioners must define thresholds or use domain knowledge to flag anomalous metrics before model training.

## Evidence

- [intro] Metrics characterize DIA files and instrument types: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments"
- [intro] Workflow uses msConvert to produce PIC data: "uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)"
- [intro] ML models use these metrics to predict quality: "we utilize machine learning models to predict the quality of the DIA files"
- [readme] Supported input file formats: "This software supports the .raw, .d, and .wiff raw data formats."
- [readme] Analysis pipeline requirement: "Click Raw (in the Input pane), select your raw mass spectrometry data files. Choose the type of instrument that generated the file."
