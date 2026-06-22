---
name: mass-spectrometry-raw-data-preprocessing
description: Use when when you have raw DIA mass spectrometry data files (.raw, .d, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msConvert
  - Python
  - iDIA-QC
  - DIA-NN
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-raw-data-preprocessing

## Summary

Convert raw DIA mass spectrometry files from timsTOF, TripleTOF, or Orbitrap instruments into extracted precursor ion chromatogram (PIC) format using msConvert, preparing them for downstream quality assessment and metric extraction. This preprocessing step standardizes heterogeneous instrument outputs into a uniform format suitable for automated quality control pipelines.

## When to use

When you have raw DIA mass spectrometry data files (.raw, .d, .wiff formats) from timsTOF, TripleTOF, or Orbitrap instruments that need to be converted to PIC format as input for iDIA-QC quality assessment, or when you need extracted precursor ion chromatograms for metric calculation and machine learning-based file quality prediction.

## When NOT to use

- Input files are already in PIC format or extracted ion chromatogram format—apply this skill only to raw, unconverted mass spectrometry data files.
- Raw data comes from instrument types not supported by the pipeline (timsTOF, TripleTOF, Orbitrap); msConvert may lack appropriate conversion filters for other MS platforms.
- File format validation fails or PIC files are incomplete after conversion; investigate instrument error logs before re-attempting preprocessing.

## Inputs

- Raw DIA mass spectrometry files (.raw format from Orbitrap instruments)
- Raw DIA mass spectrometry files (.d format from TripleTOF instruments)
- Raw DIA mass spectrometry files (.wiff format from timsTOF instruments)
- Instrument type identifier (timsTOF, TripleTOF, or Orbitrap)
- msConvert PIC extraction parameters

## Outputs

- Extracted precursor ion chromatogram (PIC) files in standardized format
- Format-validated PIC files ready for metric extraction
- PIC files suitable for input to downstream quality assessment pipeline

## How to apply

Load raw DIA mass spectrometry files in supported formats (.raw, .d, .wiff) from your instrument of interest. Apply msConvert with PIC extraction parameters to convert each raw file into extracted precursor ion chromatogram format. The conversion step is critical because downstream metric extraction (15 metrics characterizing file quality) and machine learning-based quality prediction depend on consistent PIC output. Validate converted PIC files for format integrity and completeness before downstream analysis. The workflow should be automated to minimize manual intervention—iDIA-QC implements this with a GUI requiring only a few mouse clicks to specify input files, instrument type, and output directory.

## Related tools

- **msConvert** (Converts raw DIA mass spectrometry files into extracted precursor ion chromatogram (PIC) format with configurable PIC extraction parameters)
- **iDIA-QC** (Python GUI that orchestrates msConvert-based file conversion, metric extraction, and machine learning-based quality prediction; automates the preprocessing and downstream quality assessment workflow) — https://github.com/guomics-lab/iDIA-QC
- **DIA-NN** (Provides protein qualitative and quantitative algorithms used within iDIA-QC after preprocessing for quality metric extraction)

## Evaluation signals

- All converted PIC files have consistent file format structure and completeness (no truncated or corrupted headers).
- PIC file size is proportional to original raw file size; extreme deviations suggest failed conversion.
- Downstream metric extraction succeeds on all converted PIC files without format errors; 15 metrics are computed without missing values.
- Analysis time per file is under 5 minutes as specified in the iDIA-QC design principles, indicating efficient preprocessing.
- Machine learning quality prediction model accepts converted PIC files without format validation errors in the pipeline.

## Limitations

- msConvert PIC extraction relies on vendor-supplied format specifications; timsTOF, TripleTOF, and Orbitrap file formats must be supported; other instrument vendors are not mentioned.
- PIC extraction may lose raw-level detail (e.g., isotope patterns, high-resolution fragment data) depending on msConvert filter configuration; users should verify that extracted precursor ion information is sufficient for their quality metrics.
- Preprocessing automation via iDIA-QC GUI requires correct assignment of instrument type and ID; incorrect instrument assignment may corrupt metric interpretation downstream.

## Evidence

- [intro] Instrument formats supported: "Load raw DIA mass spectrometry files (supported formats: timsTOF, TripleTOF, Orbitrap native formats)."
- [intro] PIC conversion step in workflow: "Apply msConvert with PIC extraction parameters to convert each raw file into extracted precursor ion chromatogram format."
- [readme] msConvert role in iDIA-QC: "The software incorporates the protein qualitative and quantitative algorithms from DIA-NN and uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)."
- [readme] Input file formats accepted: "This software supports the .raw, .d, and .wiff raw data formats."
- [intro] Validation step requirement: "Validate converted PIC files for format integrity and completeness."
- [readme] Performance specification: "Analysis time per file is under 5 minutes."
