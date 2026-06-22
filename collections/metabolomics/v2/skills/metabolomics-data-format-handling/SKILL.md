---
name: metabolomics-data-format-handling
description: Use when you have raw LC-MS data in mzML or equivalent binary format from a public repository (MetaboLights, MassIVE) or instrument vendor output, and need to ingest it into MetaboAnalystR 4.0 for unified LC-MS1 feature detection and MS/MS spectra processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-48009-6
  all_source_dois:
  - 10.1038/s41467-024-48009-6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-format-handling

## Summary

Loading and preparing raw LC-MS metabolomics data in standard open formats (mzML, NetCDF) for downstream feature detection and quantification. This skill ensures data integrity and compatibility across the MetaboAnalystR 4.0 processing pipeline.

## When to use

You have raw LC-MS data in mzML or equivalent binary format from a public repository (MetaboLights, MassIVE) or instrument vendor output, and need to ingest it into MetaboAnalystR 4.0 for unified LC-MS1 feature detection and MS/MS spectra processing. Use this skill as the entry point before executing the auto-optimized feature detection module.

## When NOT to use

- Input data is already a processed feature table (CSV, TSV with rows=features, columns=samples); skip directly to statistical analysis or functional interpretation modules.
- Data is in proprietary vendor binary format and no mzML/NetCDF conversion tool is available; conversion must be completed externally first (e.g., using ProteoWizard msConvert).
- Input is already quality-controlled and feature-detected by an external pipeline; load the feature table instead of raw scans.

## Inputs

- raw LC-MS data file in mzML format
- raw LC-MS data file in NetCDF format
- vendor-proprietary LC-MS raw data (requires prior conversion to mzML/NetCDF)

## Outputs

- loaded LC-MS data object (MetaboAnalystR internal format)
- parsed scan metadata (retention time, m/z, intensity arrays)
- ready-to-process data structure for feature detection module

## How to apply

Load raw LC-MS data (mzML or equivalent format) into MetaboAnalystR 4.0 using the package's data import functions. Verify that the input file contains both LC-MS1 scans (for quantification) and, optionally, MS/MS spectra (for compound annotation via DDA or DIA acquisition modes). The loaded data will be parsed into an internal object representation that the unified LC-MS workflow can consume. MetaboAnalystR 4.0 will handle vendor-specific format conversion and normalization transparently. No manual format conversion or external tools are required if input is already in mzML; for other formats, ensure conversion to mzML before import.

## Related tools

- **MetaboAnalystR** (Data import and unified LC-MS workflow execution environment for loading and processing mzML/NetCDF files) — https://github.com/xia-lab/MetaboAnalystR

## Evaluation signals

- Data object successfully instantiated in R environment without parsing errors or warnings
- Scan count and sample count are consistent with experiment design (≥1 sample, ≥10 scans per sample typical for LC-MS)
- m/z values span expected mass range (50–1500 m/z common for metabolomics; no negative or zero m/z)
- Intensity arrays are numeric, non-negative, and contain variability across scans (not all zeros or constants)
- Retention time values are monotonically increasing or form realistic scan order (no future-dated or negative times)

## Limitations

- Metadata (instrument type, acquisition parameters, sample annotations) embedded in mzML headers may be incomplete or non-standard; manual curation of experimental design files is often required.
- Large files (>10 GB raw mzML) may cause memory pressure during import; consider splitting into separate batches or using the MetaboAnalyst web server API for large-scale processing.
- Vendor-specific m/z calibration or lock-mass corrections are not automatically applied; users must verify calibration accuracy before peak detection.
- Data from unconventional acquisition modes (e.g., targeted monitoring, ion mobility spectrometry) may not be fully supported by the unified LC-MS workflow; DDA and DIA are the primary supported acquisition modes.

## Evidence

- [other] Load raw LC-MS data (mzML or equivalent format) from a public repository (MetaboLights or MassIVE) into MetaboAnalystR 4.0.: "Load raw LC-MS data (mzML or equivalent format) from a public repository (MetaboLights or MassIVE) into MetaboAnalystR 4.0."
- [readme] MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation.: "MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] a streamlined MS/MS spectra deconvolution and compound annotation module for both data-dependent acquisition (DDA) or data-independent acquisition (DIA): "a streamlined MS/MS spectra deconvolution and compound annotation module for both data-dependent acquisition (DDA) or data-independent acquisition (DIA)"
