---
name: compound-standard-ratio-normalization
description: Use when you have raw peak area or intensity measurements for both compounds and their corresponding internal standards across all study samples (including QC and calibration samples), and you need to normalize for instrument variability and injection efficiency before batch correction or quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-standard-ratio-normalization

## Summary

Normalize metabolomics compound abundances by calculating ratios between each compound and its assigned internal standard to account for instrument response variation and sample preparation differences. This foundational preprocessing step enables downstream batch correction and quality control assessment in mass spectrometry-based metabolomics.

## When to use

Apply this skill when you have raw peak area or intensity measurements for both compounds and their corresponding internal standards across all study samples (including QC and calibration samples), and you need to normalize for instrument variability and injection efficiency before batch correction or quality assessment. Use this as the first normalization step in mzQuality's analysis pipeline.

## When NOT to use

- If internal standard assignments have not been validated or are missing for compounds of interest
- If internal standard peak areas are below detection limit or show excessive variability (these should be flagged before ratio calculation)
- If you are analyzing data where compounds and internal standards were measured in separate injection methods or incompatible ionization modes

## Inputs

- SummarizedExperiment object with assay slots containing peak areas or intensities for compounds and internal standards
- Mandatory columns: compound identifier, internal standard assignment per compound, sample identifiers, sample type (study/QC/calibration)
- Tab-delimited text file or Sciex OS export with compound areas and internal standard areas

## Outputs

- SummarizedExperiment object with new 'ratio' assay containing compound/internal standard ratios for all samples
- rowData and colData slots preserved with metadata intact for downstream filtering and visualization

## How to apply

For each compound in your SummarizedExperiment object, divide the peak area (or intensity) of that compound by the peak area of its assigned internal standard across all samples and aliquots. This produces compound/internal standard ratios that normalize out instrument response drift and sample handling variation. The ratios are then stored as a new assay in the SummarizedExperiment and serve as input for downstream batch correction using pooled study quality control (SQC) samples, background signal quantification, matrix effect assessment, and internal standard recommendation. The assignment of internal standards to compounds should be done prior to ratio calculation, typically based on chemical similarity or retention time proximity.

## Related tools

- **mzQuality** (Primary R package that automates compound/internal standard ratio calculation, batch correction, and quality metrics within the SummarizedExperiment framework) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor data container used by mzQuality to store compound areas, internal standard areas, calculated ratios, and analysis metadata in a unified object structure)
- **mzQualityDashboard** (Interactive Shiny application that wraps mzQuality's ratio calculation and subsequent analyses with a user-friendly GUI for non-programmers) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
library(mzQuality); path <- system.file('extdata', 'example.tsv', package = 'mzQuality'); exp <- buildExperiment(readData(path)); exp <- doAnalysis(exp = exp)
```

## Evaluation signals

- Ratio assay is present in the SummarizedExperiment and contains numeric values (no NaN or Inf unless from genuine missing internal standard peaks)
- Ratio values are reasonable in magnitude (typically 0.01–100 depending on compound and ionization efficiency) and show expected batch structure before batch correction
- QC sample ratios have lower variance than study sample ratios (this is verified after batch correction by calculating RSDQC for candidate internal standards)
- No samples or compounds are lost during ratio calculation; dimensions of the output SummarizedExperiment match the input
- Ratio distributions are approximately log-normal when plotted; severe outliers or bimodal distributions suggest incorrect internal standard assignment

## Limitations

- If an internal standard is absent or below detection in a sample, the ratio becomes undefined (NA or Inf); these samples may need to be flagged or excluded depending on prevalence.
- The skill assumes internal standards were co-measured with compounds in the same analysis; it cannot correct for systematic differences between separate measurement batches or ionization modes.
- Currently mzQuality enforces a one-to-many internal standard assignment (one internal standard per compound) and does not support multiple internal standards per compound or compound groups.
- Ratio calculation alone does not account for matrix effects or ionization suppression; these require additional assessment after batch correction.

## Evidence

- [readme] Calculate the ratio between the compounds and assigned internal standards: "Calculate the ratio between the compounds and assigned internal standards,"
- [other] For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios.: "For each compound, iterate over all internal standard candidates and compute the relative standard deviation (RSD) of the batch-corrected QC sample ratios."
- [intro] The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio.: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio."
- [other] Load the batch-corrected SummarizedExperiment object containing QC sample ratios (compound / internal standard): "Load the batch-corrected SummarizedExperiment object containing QC sample ratios (compound / internal standard)"
- [intro] Internally, mzQuality uses Bioconductors' SummarizedExperiment object to store the data.: "Internally, mzQuality uses Bioconductors' SummarizedExperiment object to store the data."
