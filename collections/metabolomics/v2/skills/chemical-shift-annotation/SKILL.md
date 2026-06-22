---
name: chemical-shift-annotation
description: Use when when you have preprocessed 1H NMR spectral data with unidentified peaks and need to determine metabolite identity by exploiting the correlation structure of NMR signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Bioconductor
  - MWASTools
  - Statistical Total Correlation Spectroscopy (STOCSY)
  - TopSpin 3.2
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-shift-annotation

## Summary

Use Statistical Total Correlation Spectroscopy (STOCSY) to assign chemical identity to unknown NMR signals by analyzing their covariance and correlation patterns across a reference spectrum. This workflow converts ambiguous δ shifts into metabolite assignments by identifying characteristic multiplet patterns.

## When to use

When you have preprocessed 1H NMR spectral data with unidentified peaks and need to determine metabolite identity by exploiting the correlation structure of NMR signals. Specifically, when a driver signal (known or suspected metabolite at a specific ppm value) shows strong covariance with other peaks in the spectrum, STOCSY can reveal whether those peaks belong to the same metabolite based on their J-coupling and chemical shift relationships.

## When NOT to use

- Raw, unphased NMR spectra or data not baseline-corrected (preprocessing in TopSpin or equivalent is required before STOCSY)
- Metabolites lacking strong multiplet structure or J-coupling patterns (STOCSY relies on covariance across related spins)
- Highly overlapped spectral regions where multiple metabolites share the same chemical shift range and cannot be resolved by correlation alone

## Inputs

- Preprocessed 1H NMR spectral data (Bioconductor metabo_SE object or compatible matrix/data frame with ppm chemical shift columns and intensity rows)
- Driver signal chemical shift value (ppm, e.g., 1.04)
- Known or suspected metabolite reference library with expected multiplet patterns and chemical shifts

## Outputs

- STOCSY correlation profile (numeric vector of correlation coefficients indexed by ppm)
- Annotated STOCSY plot with highlighted covariant peaks and metabolite assignments
- Correlation data matrix linking driver signal to all other chemical shifts
- Metabolite identity assignment with confidence support from J-coupling pattern matching

## How to apply

Load preprocessed NMR spectral data (in the format accepted by Bioconductor's metabo_SE object) into R with Bioconductor installed. Apply the STOCSY function from MWASTools with the query ppm parameter set to the chemical shift of your driver signal (e.g., δ 1.04 for the BMI-associated valine signal). The function generates a correlation profile across all chemical shifts; extract and visualize correlation coefficients to identify peaks showing significant covariance. Cross-reference highlighted multiplets against known metabolite chemical shift signatures from NMR literature (e.g., valine doublets at δ 1.04 and δ 0.99). A successful assignment occurs when the STOCSY correlation pattern matches the expected J-coupling fine structure and chemical shift spacing of a known metabolite.

## Related tools

- **Statistical Total Correlation Spectroscopy (STOCSY)** (Core algorithm that computes correlation coefficients between driver signal intensity and all other chemical shifts to reveal covariant metabolite signatures)
- **MWASTools** (R/Bioconductor package providing STOCSY implementation, preprocessing infrastructure, and visualization for metabolite-phenotype association workflows) — https://github.com/AndreaRMICL/MWASTools
- **R** (Programming environment for loading, manipulating, and running STOCSY analysis on NMR spectral objects)
- **Bioconductor** (Data structure (metabo_SE) and computational framework for managing high-dimensional NMR spectral matrices and annotation metadata)
- **TopSpin 3.2** (Upstream NMR data processing software for phasing and baseline correction required before STOCSY analysis)

## Evaluation signals

- Highlighted doublets or multiplets in the STOCSY output appear at expected chemical shifts for the assigned metabolite (e.g., valine at δ 1.04 and δ 0.99)
- Correlation coefficients at covariant peaks are statistically significant (high magnitude, consistent across independent samples or spectral replicates)
- J-coupling splitting patterns and chemical shift spacing match literature values for the proposed metabolite identity
- Cross-validation: driver signal and assigned peaks show consistent covariance when STOCSY is rerun with one of the highlighted peaks as an alternative driver
- No conflicting high-correlation peaks from unrelated metabolites appear in the STOCSY profile

## Limitations

- STOCSY requires strong J-coupling and covariance structure; highly isolated singlets or closely overlapped multiplets may not yield unambiguous assignments
- Assignment confidence depends on the quality and completeness of the reference chemical shift library; novel or rare metabolites may not be reliably identified
- Baseline distortions or residual phase errors in the preprocessed NMR data can reduce correlation signal and lead to missed or false assignments
- STOCSY identifies only correlations; it does not distinguish between structurally similar metabolites with nearly identical chemical shifts and J-coupling patterns without additional MS or 2D NMR data

## Evidence

- [other] STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine.: "STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine"
- [other] Can STOCSY analysis of NMR spectral data identify the chemical identity of unknown metabolic features by their covariance and correlation patterns with a driver signal?: "STOCSY analysis of NMR spectral data identify the chemical identity of unknown metabolic features by their covariance and correlation patterns with a driver signal"
- [other] Apply STOCSY (Statistical Total Correlation Spectroscopy) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts.: "Apply STOCSY (Statistical Total Correlation Spectroscopy) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts"
- [intro] metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY): "metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)"
- [intro] Following phasing and baseline correction in TopSpin 3.2 software: "Following phasing and baseline correction in TopSpin 3.2 software"
