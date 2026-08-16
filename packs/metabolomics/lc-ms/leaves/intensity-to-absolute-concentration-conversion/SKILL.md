---
name: intensity-to-absolute-concentration-conversion
description: Use when your lipidomics experiment includes spiked internal lipid standards of known concentration, and you have raw signal intensity matrices from LipidSearch or LIQUID output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - LipidSearch
  - LIQUID
  - ADViSELipidomics
  - LIPID MAPS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- outputs from LipidSearch and LIQUID for lipid identification and quantification
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# intensity-to-absolute-concentration-conversion

## Summary

Convert raw lipidomics signal intensities to absolute lipid concentration values by normalizing against internal lipid standards. This skill bridges quantitative mass spectrometry output with biologically interpretable absolute amounts per lipid species and sample.

## When to use

Your lipidomics experiment includes spiked internal lipid standards of known concentration, and you have raw signal intensity matrices from LipidSearch or LIQUID output. Use this skill when relative abundance or intensity ranks are insufficient and downstream analysis requires actual lipid concentrations (e.g., biomarker thresholds, flux modeling, or cross-study comparison).

## When NOT to use

- No internal lipid standards were spiked into the experiment or standard intensities are missing from the data matrix.
- Your analysis goal is only exploratory (e.g., PCA, correlation) and relative abundance is sufficient.
- Input is already a normalized feature table or pre-computed concentration matrix from another pipeline.

## Inputs

- Raw lipidomics data matrix (samples × lipids, intensity values) from LipidSearch or LIQUID
- Internal lipid standard reference table with expected absolute concentrations
- Lipid metadata with LIPID MAPS classification

## Outputs

- Normalized lipidomics concentration matrix (samples × lipids, concentration values)
- Normalization factor per lipid species
- QC metrics (e.g., standard recovery rates, concentration ranges)

## How to apply

Load the lipidomics data matrix (samples × lipids) and the internal standard reference table specifying expected absolute concentrations for each standard. Extract signal intensities for all internal lipid standards across all samples. For each lipid species, calculate a normalization factor as the ratio of expected absolute concentration (from the standard reference) to the observed intensity for the corresponding internal standard. Apply this normalization factor uniformly to all lipid measurements in the data matrix to convert raw intensities to absolute concentration values. Verify that the normalized matrix contains only positive, biologically plausible concentration ranges and that LIPID MAPS classification annotations are preserved.

## Related tools

- **LipidSearch** (Produces raw lipidomics intensity data and lipid identifications from MS/MS spectra)
- **LIQUID** (Produces raw lipidomics intensity data and lipid identifications from MS/MS spectra)
- **LIPID MAPS** (Provides lipid classification scheme for annotating normalized lipid species)
- **ADViSELipidomics** (Implements internal standard normalization workflow and produces absolute concentration matrix) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- Normalized concentration values are all positive and within expected biological ranges (typically μM to nM for plasma lipids).
- Internal standard recovery rates (observed intensity / expected concentration) are consistent across samples (low coefficient of variation < 20%).
- No negative or zero concentration values remain after normalization (except for lipids genuinely absent from a sample).
- Concentration matrix retains LIPID MAPS class annotations and sample metadata without data loss.
- Normalization factors show negligible variation between technical replicates of the same internal standard.

## Limitations

- Normalization accuracy is bounded by the quality and stability of internal standards; degraded or unevenly distributed standards will propagate systematic error across the entire data matrix.
- The method assumes that ionization efficiency and chromatographic behavior are similar for internal standards and analyte lipids; large structural differences (e.g., standard is a triglyceride but analyte is a phospholipid) may introduce bias.
- If internal standard intensities vary dramatically between samples (e.g., due to injection volume errors or matrix effects), the normalization factor may become unreliable.
- Missing or below-detection-limit intensities for internal standards in some samples will render normalization impossible for those samples.

## Evidence

- [other] ADViSELipidomics normalizes the data matrix using internal lipid standards to provide absolute values of concentration per lipid and sample.: "ADViSELipidomics normalizes the data matrix using internal lipid standards to provide absolute values of concentration per lipid and sample."
- [other] For each lipid species, compute a normalization factor as the ratio of expected absolute concentration (from standard reference) to observed intensity for the corresponding internal standard. Apply the normalization factor to all lipid measurements in the data matrix to convert intensities to absolute concentration values.: "For each lipid species, compute a normalization factor as the ratio of expected absolute concentration (from standard reference) to observed intensity for the corresponding internal standard. Apply"
- [readme] In the presence of internal lipid standards in the experiment, ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample.: "In the presence of internal lipid standards in the experiment, ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample."
- [readme] It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"
