---
name: stocsy-metabolite-assignment
description: Use when use STOCSY when you have preprocessed 1H NMR spectral data with an unidentified peak of interest (driver signal at a specific δ ppm value) and need to determine its metabolite identity by finding correlated signals across the spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Statistical Total Correlation Spectroscopy (STOCSY)
  - R
  - Bioconductor
  - MWASTools
  - TopSpin 3.2
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)
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

# stocsy-metabolite-assignment

## Summary

STOCSY (Statistical Total Correlation Spectroscopy) is a multivariate NMR analysis technique that identifies the chemical identity of unknown metabolic features by correlating their spectral patterns with a driver signal across all chemical shifts. It enables rapid metabolite assignment without prior structural knowledge by detecting covariance signatures characteristic of specific compounds.

## When to use

Use STOCSY when you have preprocessed 1H NMR spectral data with an unidentified peak of interest (driver signal at a specific δ ppm value) and need to determine its metabolite identity by finding correlated signals across the spectrum. This is particularly valuable when the unknown signal's doublet or multiplet structure suggests a known metabolite family (e.g., amino acids, fatty acids) but direct library matching is inconclusive or unavailable.

## When NOT to use

- Input spectra have not been phased and baseline-corrected; STOCSY assumes high-quality preprocessed data and will produce artifacts or false correlations on poorly processed spectra.
- The driver signal represents an overlapping multiplet from multiple metabolites; STOCSY will produce ambiguous correlations confounding rather than clarifying metabolite identity.
- Prior metabolite annotation is already complete or confident from other orthogonal methods (e.g., 2D NMR, high-resolution MS/MS); STOCSY adds confirmatory value but is not necessary for confirmed assignments.

## Inputs

- Preprocessed 1H NMR spectral data matrix (e.g., R data.frame or Bioconductor ExpressionSet with rows = chemical shifts, columns = samples)
- Query chemical shift value (δ ppm) for the driver signal of unknown identity
- Phased and baseline-corrected NMR spectra (pre-processed in TopSpin or equivalent)

## Outputs

- STOCSY correlation coefficient vector across all chemical shifts
- Annotated STOCSY plot showing correlation intensities and highlighted metabolite-specific peaks
- Metabolite assignment with chemical shift annotations (δ values and multiplicity)
- Correlation data table with ppm values, correlation coefficients, and significance metrics

## How to apply

Load preprocessed NMR spectral data (e.g., metabo_SE object in R/Bioconductor) and invoke the STOCSY function with the driver signal's chemical shift (query ppm parameter) set to the δ value of the unknown peak. The function generates correlation coefficients across all chemical shifts in the spectrum, highlighting peaks that co-vary with the driver signal. Extract and visualize the resulting correlation profile to identify significant peaks (typically doublets or multiplets appearing at characteristic δ intervals for the suspected metabolite class). Cross-reference the pattern of highlighted peaks against literature chemical shift signatures and known metabolite standards (e.g., valine shows doublets at δ 1.04 and δ 0.99). Validate the assignment by confirming that the identified peaks match the expected multiplicity and spacing for the candidate metabolite's proton splitting patterns.

## Related tools

- **MWASTools** (R/Bioconductor package that wraps STOCSY as an integrated function for metabolite assignment within a broader MWAS workflow; provides quality control, association modeling, and visualization alongside STOCSY metabolite annotation) — github.com/AndreaRMICL/MWASTools
- **TopSpin 3.2** (Pre-processing platform for phasing and baseline correction of raw Bruker NMR spectra prior to STOCSY analysis)
- **R** (Programming environment (≥3.3) in which MWASTools and STOCSY functions execute)
- **Bioconductor** (Bioinformatics framework providing data structures and statistical methods integrated with MWASTools for NMR spectral analysis)

## Examples

```
# Load MWASTools and preprocessed NMR data in R; apply STOCSY with driver signal at δ 1.04:
# stocsy_result <- STOCSY(metabo_SE, query_ppm = 1.04)
# Visualize correlation plot and extract metabolite assignments from significant peaks.
```

## Evaluation signals

- Identified correlated peaks in the STOCSY plot appear at chemical shifts matching literature values for the proposed metabolite (e.g., doublets at δ 1.04 and δ 0.99 for valine with expected coupling constant ~7 Hz).
- Correlation coefficients for metabolite-specific peaks are statistically significant and substantially higher than background noise or uncorrelated chemical shifts; visual inspection shows clear clustering of correlated signals.
- Cross-validation: predicted metabolite identity is consistent with the multiplicity and splitting pattern of the driver signal and satellite peaks (e.g., doublet for amino acid methyl groups).
- Annotated STOCSY plot is interpretable and reproducible; rerunning the analysis with the same driver δ and preprocessed data yields identical correlation vectors and metabolite assignments.
- Independent confirmation from orthogonal NMR techniques (e.g., 1D 13C NMR, HMQC, or COSY) or literature standards corroborates the STOCSY-assigned metabolite identity.

## Limitations

- STOCSY performance depends critically on NMR spectrum quality and preprocessing (phasing, baseline correction); poor preprocessing in TopSpin will degrade correlation profiles and lead to false or missed assignments.
- Overlapping or co-eluting signals from multiple metabolites sharing the same chemical shift region will produce ambiguous or misleading correlations that do not uniquely identify any single metabolite.
- STOCSY assigns identity based on covariance patterns, not absolute chemical shifts; if a metabolite's abundance varies independently of the driver signal across samples (e.g., no biological covariance in the cohort), its true peaks may not appear in the correlation profile despite metabolite presence.
- No built-in mechanism to resolve stereoisomers or distinguish between metabolites with identical or near-identical 1H NMR fingerprints; manual inspection or 2D NMR confirmation is required for ambiguous cases.
- The method assumes a single primary driver signal; when the chosen δ corresponds to an overlapping multiplet or contaminant, downstream correlation assignments become unreliable.

## Evidence

- [other] STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine.: "STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine."
- [intro] metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY): "metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)"
- [other] Apply STOCSY (Statistical Total Correlation Spectroscopy) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts.: "Apply STOCSY (Statistical Total Correlation Spectroscopy) function with query ppm parameter set to 1.04 to generate a correlation profile across all chemical shifts."
- [intro] Following phasing and baseline correction in TopSpin 3.2 software: "Following phasing and baseline correction in TopSpin 3.2 software"
- [abstract] Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation: "metabolite assignment using statistical total correlation"
- [other] Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor.: "Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor."
- [other] Cross-reference the doublet peaks at δ 1.04 and δ 0.99 against known valine chemical shift signatures and literature references.: "Cross-reference the doublet peaks at δ 1.04 and δ 0.99 against known valine chemical shift signatures and literature references."
