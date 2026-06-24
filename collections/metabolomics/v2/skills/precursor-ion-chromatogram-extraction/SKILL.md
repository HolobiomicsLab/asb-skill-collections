---
name: precursor-ion-chromatogram-extraction
description: Use when you have raw DIA mass spectrometry data files (.raw, .d, or
  .wiff formats) from timsTOF, TripleTOF, or Orbitrap instruments and need to extract
  precursor ion chromatograms for quality assessment or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msConvert
  - Python
  - iDIA-QC
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
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

# precursor-ion-chromatogram-extraction

## Summary

Convert raw DIA mass spectrometry files from timsTOF, TripleTOF, and Orbitrap instruments into extracted precursor ion chromatogram (PIC) format using msConvert. This conversion is a prerequisite step for downstream quality metric extraction and machine learning-based file quality prediction in the iDIA-QC pipeline.

## When to use

Apply this skill when you have raw DIA mass spectrometry data files (.raw, .d, or .wiff formats) from timsTOF, TripleTOF, or Orbitrap instruments and need to extract precursor ion chromatograms for quality assessment or downstream analysis. The conversion is essential before computing the 15 quality-characterizing metrics used in iDIA-QC.

## When NOT to use

- Input data is already in PIC or other chromatogram-derived format — direct conversion would be redundant
- Raw files are from instruments other than timsTOF, TripleTOF, or Orbitrap — msConvert support and metric compatibility are not guaranteed
- Analysis objective does not require precursor ion chromatogram data (e.g., if only peptide/protein identification is needed without quality metrics)

## Inputs

- raw DIA mass spectrometry files in native instrument formats (.raw for Orbitrap, .d for timsTOF, .wiff for TripleTOF)
- instrument type specification (timsTOF, TripleTOF, or Orbitrap)

## Outputs

- extracted precursor ion chromatogram (PIC) files in standardized format
- converted DIA data ready for 15-metric extraction

## How to apply

Load raw DIA mass spectrometry files in supported native formats (timsTOF, TripleTOF, or Orbitrap) into msConvert. Configure msConvert with PIC (extracted precursor ion chromatogram) extraction parameters appropriate for your instrument type. Process each raw file through msConvert to generate the corresponding PIC file. Validate the converted PIC files for format integrity and completeness (verify file size, data structure, and absence of truncation). Output the converted PIC files in standardized format for downstream metric extraction. This conversion typically completes within the iDIA-QC pipeline's 5-minute-per-file analysis target.

## Related tools

- **msConvert** (performs file format conversion from raw DIA instrument files to extracted precursor ion chromatogram (PIC) format with configurable extraction parameters)
- **Python** (environment for loading, validating, and processing converted PIC data for downstream metric extraction)
- **iDIA-QC** (orchestrates the full pipeline including msConvert-based conversion, metric extraction, and quality prediction) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- Converted PIC files are non-empty and match expected file size range for the input raw file size and instrument type
- PIC file structure conforms to expected chromatogram data format (e.g., parseable headers, consistent data arrays)
- No truncation or corruption detected in PIC files (e.g., complete data records, no partial or malformed entries)
- Downstream 15-metric extraction succeeds without errors or missing data on converted PIC files
- Conversion completes within the iDIA-QC pipeline's per-file time budget (under 5 minutes)

## Limitations

- msConvert PIC extraction parameters must be tuned per instrument type (timsTOF, TripleTOF, Orbitrap); parameter transfer across instruments may produce suboptimal chromatograms
- Conversion quality depends on raw file integrity; corrupted or incomplete raw files may produce invalid or degraded PIC output
- Supported raw file formats are limited to .raw (Orbitrap), .d (timsTOF), and .wiff (TripleTOF); other DIA data formats require alternative conversion tools

## Evidence

- [other] Load raw DIA mass spectrometry files (supported formats: timsTOF, TripleTOF, Orbitrap native formats). Apply msConvert with PIC extraction parameters to convert each raw file into extracted precursor ion chromatogram format.: "Load raw DIA mass spectrometry files (supported formats: timsTOF, TripleTOF, Orbitrap native formats). Apply msConvert with PIC extraction parameters to convert each raw file into extracted precursor"
- [readme] uses msConvert for file conversion to extracted precursor ion chromatogram (PIC): "uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)"
- [other] Validate converted PIC files for format integrity and completeness. Output converted PIC files in standardized format ready for downstream metric extraction.: "Validate converted PIC files for format integrity and completeness. Output converted PIC files in standardized format ready for downstream metric extraction."
- [readme] Click Raw (in the Input pane), select your raw mass spectrometry data files. This software supports the .raw, .d, and .wiff raw data formats.: "Click Raw (in the Input pane), select your raw mass spectrometry data files. This software supports the .raw, .d, and .wiff raw data formats."
- [readme] Scalability and speed: Analysis time per file is under 5 minutes.: "Scalability and speed: Analysis time per file is under 5 minutes."
