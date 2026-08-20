---
name: data-normalization-in-mass-spectrometry
description: Use when you have raw or partially processed metabolomics data (mzML/mzXML
  format) from LC-MS or GC-MS runs and need to apply standardized feature detection,
  alignment, and intensity normalization as part of a reproducible workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MZmine
  techniques:
  - LC-MS
  - GC-MS
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.05.13.593988v1
  title: plantMASST
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_plantmasst_2_cq
    doi: 10.1101/2024.05.13.593988v1
    title: plantMASST
  dedup_kept_from: coll_plantmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.05.13.593988v1
  all_source_dois:
  - 10.1101/2024.05.13.593988v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-normalization-in-mass-spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize and align metabolomics feature tables produced by mass spectrometry acquisition using batch processing parameters embedded in MZmine configuration files. This skill ensures consistent peak intensity scaling and retention time alignment across multiple samples before statistical or taxonomic analysis.

## When to use

You have raw or partially processed metabolomics data (mzML/mzXML format) from LC-MS or GC-MS runs and need to apply standardized feature detection, alignment, and intensity normalization as part of a reproducible workflow. Use this skill when a repository or study provides pre-configured MZmine batch files that encode the normalization parameters validated for a specific biological context (e.g., plant metabolomics as in plantMASST).

## When NOT to use

- Input is already a processed feature table (CSV or mzTab); use this skill only on raw instrumental data.
- MZmine batch files are unavailable or not validated for your instrument/sample type; use this skill only when pre-configured parameters are provided or peer-reviewed.
- Data are from a different analytical platform (e.g., GC-FID, NMR, or non-MS proteomics); MZmine is MS-specific.

## Inputs

- raw mass spectrometry data files (mzML or mzXML format)
- MZmine batch processing configuration file (.xml or equivalent)
- MZmine input parameter set (feature detection and alignment settings)

## Outputs

- processed feature table (CSV or mzTab format)
- normalized peak intensity matrix (samples × features)
- retention time-aligned feature annotations

## How to apply

Retrieve the MZmine batch processing configuration and input parameter files from the repository (typically found in a dedicated MZmine/ subdirectory). Load raw mass spectrometry data in mzML or mzXML format into MZmine and execute the batch workflow, which performs feature detection (peak picking), retention time alignment across samples, and intensity normalization according to the embedded parameters. The batch process outputs a standardized feature table in CSV or mzTab tabular format. Validate the output table dimensions (number of features × samples) and verify that intensity values are scaled consistently (e.g., no extreme outliers or zero-variance features within sample groups) against repository documentation or the original manuscript's expected schema.

## Related tools

- **MZmine** (Batch feature detection, retention time alignment, and intensity normalization of raw mass spectrometry data)

## Evaluation signals

- Output feature table has expected dimensions (number of samples and number of detected features) matching or exceeding repository documentation.
- Intensity values are numeric, non-negative, and show no systematic biases across samples (e.g., no sample exhibits zero or near-zero median intensity).
- Retention time values are aligned across samples; features from the same compound should cluster within expected retention time windows (typically ±0.5 min after alignment).
- Missing values or data quality flags in the feature table are documented and consistent with the batch processing parameters (e.g., features missing in >50% of samples are flagged or excluded).
- Output schema (column names, data types, row/column order) matches the repository's stated format or the manuscript's supplementary table specifications.

## Limitations

- MZmine batch parameters are often instrument- and sample-type-specific; parameters validated for plant tissues may not work for other matrices (e.g., serum, soil) without re-optimization.
- The skill assumes the raw data are in supported formats (mzML/mzXML); proprietary vendor formats may require prior conversion.
- Normalization effectiveness depends on the quality of the raw data; severely compromised runs or samples with extreme outlier peaks may distort alignment and normalization.
- No changelog is available in the plantMASST repository to document parameter updates; reproducibility depends on version control of the batch files themselves.

## Evidence

- [intro] MZmine inputs used for metabolomics processing: "the MZmine inputs used for metabolomics processing"
- [intro] Repository organization around metabolomics workflow materials: "It is organized around the main tables used in the study, the notebooks that generate figure panels, the MZmine inputs used for metabolomics processing, and the supplementary HTML outputs"
- [readme] MZmine directory contains batch processing files: "`MZmine/`: input files and batch files for the metabolomics datasets used in as use cases in this project."
- [other] Workflow tasks include feature detection, alignment, and normalization: "Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration."
- [other] Output validation against expected schema: "Validate the output feature table dimensions and content against repository documentation or expected schema."
