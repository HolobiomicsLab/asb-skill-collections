---
name: ion-mobility-mass-spectrometry-data-processing
description: Use when you have IM-MS lipidomics samples spiked with U13C-labeled internal
  standards (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0673
  tools:
  - R
  - MobiLipid
  - RStudio
  - ggplot2
  - rmarkdown
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates
  into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated
  solution for assessing and correcting collision cross section (CCS) bias
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  - build: coll_mobilipid_cq
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01253
  all_source_dois:
  - 10.1021/acs.analchem.4c01253
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-mass-spectrometry-data-processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess and correct collision cross section (CCS) bias in ion mobility-mass spectrometry (IM-MS) lipidomics data by internal standardization using U13C-labeled lipid standards and a reference DTCCS_N2 library. This skill eliminates the need for additional external calibration beyond vendor-specific requirements.

## When to use

Apply this skill when you have IM-MS lipidomics samples spiked with U13C-labeled internal standards (e.g., fully labeled yeast extract), measured CCS values stratified by lipid class and adduct, and seek to quantify systematic bias in observed CCS relative to reference values and apply per-lipid-class correction functions.

## When NOT to use

- Samples are not spiked with U13C-labeled internal standards; the skill depends on detecting and comparing U13C lipids to derive bias corrections.
- Lipid class–adduct combinations have fewer than 3 U13C-labeled lipids detected; linear regression correction functions require a minimum of 3 points and MobiLipid restricts correction to classes with ≥3 detected standards.
- Input CCS values are already externally calibrated or corrected by the instrument vendor and no evidence of systematic bias is suspected; internal standardization is most valuable when bias variation across lipid classes is observed.

## Inputs

- Measured IM-MS CCS data (CSV format with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DTCCS_N2 reference library for U13C-labeled lipids (CSV format with lipid class, species identifier, and CCS reference values)
- R Markdown workflow file (MobiLipid_CCS-bias-calculation.Rmd or MobiLipid_CCS-bias-calculation_CCS-correction.Rmd)

## Outputs

- CCS bias table before correction (CSV: CCS_bias_no_correction.csv)
- CCS correction function coefficients table (CSV: Correction_functions.csv)
- Mean CCS bias by correction function (CSV: CCS_bias_mean_by_function.csv)
- Mean CCS bias aggregated across functions by lipid count (CSV: CCS_bias_mean_all_functions.csv)
- Corrected CCS values and residual bias (CSV: Corrected_CCS_values.csv)
- Mean corrected CCS values aggregated by lipid count (CSV: Corrected_CCS_values_mean.csv)
- HTML and PDF reports with tables and diagnostic figures (bias distributions, violin plots, resampling summary)
- RData file storing all results as a list (readRDS-compatible)

## How to apply

Load measured IM-MS CCS values (as CSV with headers: File, LipidClass, LipidSpecies, Adduct, Label, CCS) and the DTCCS_N2 library for U13C labeled lipids into R. Stratify measurements by lipid class and compute bias as the deviation of observed CCS from library reference values using U13C labeled standards detected within each class. For lipid class–adduct combinations with ≥3 U13C lipids, generate linear regression correction functions (y = m*x + b, where x = measured CCS, y = library CCS). Apply the computed per-class correction function to all measured CCS values in that class, then recalculate bias post-correction. Output bias tables (before and after correction), correction function coefficients, and diagnostic plots (bias distribution, violin plots by correction function, per-function bias summaries) to both HTML and PDF formats.

## Related tools

- **R** (Execution environment and statistical computing for CCS bias calculation, linear regression, and diagnostic visualization) — https://cran.r-project.org/
- **MobiLipid** (R Markdown workflow that automates CCS bias assessment, correction function generation via linear regression, and report generation) — https://github.com/FelinaHildebrand/MobiLipid
- **RStudio** (IDE for executing R Markdown files and interactive parameter input via dialog boxes) — https://www.rstudio.com/products/rstudio/download/
- **ggplot2** (R package for generating diagnostic plots (bias distributions, violin plots, beeswarm plots))
- **rmarkdown** (R package for rendering R Markdown to HTML and PDF outputs with embedded tables and figures)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_analysis.html', 'MobiLipid_analysis.pdf'))
```

## Evaluation signals

- CCS bias values before correction cluster around a class-specific mean (e.g., +5% for PC, −2% for PE), with residual SD < 3% after correction, indicating effective per-class bias removal.
- Linear regression correction functions exhibit R² > 0.90 for each lipid class–adduct combination, confirming high fidelity of the fitted correction model.
- Corrected CCS values of U13C lipids converge toward library reference values; mean absolute bias after correction is <1.5% per lipid class–adduct combination.
- Diagnostic violin plots show a visually marked reduction in bias spread (variance) after correction is applied, with outliers (>3 SD from mean) reduced or absent.
- Resampling summary table confirms generation of expected number of correction functions (up to 100 distinct functions) with 3–6 lipids per function, and no lipid class–adduct combinations are missing from output due to insufficient sample size.

## Limitations

- CCS correction is restricted to lipid class–adduct combinations with ≥3 U13C-labeled lipids detected; classes with fewer standards (e.g., AcCa, Co, LPE, PG, SPH) are excluded from correction and only bias is calculated.
- Correction functions are linear (y = m*x + b); non-linear bias patterns across the CCS range will not be captured.
- MobiLipid requires samples to be spiked with fully labeled yeast extract; other U13C labeling schemes or external standards are not validated.
- Supported lipid class–adduct combinations are predefined (13 lipid classes × up to 3 adducts each); custom adducts or lipid classes must be manually integrated into the workflow.
- The DTCCS_N2 library provided with MobiLipid is specific to yeast-derived U13C lipids; applicability to other organism-derived or synthetic U13C standards is not documented.

## Evidence

- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [other] Stratify measured CCS values by lipid class. For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization: "For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value"
- [readme] The .csv file has to have the following headers: File, LipidClass, LipidSpecies, Adduct, Label, CCS: "The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS""
- [readme] Additionally, a .RData file is saved storing all results as a list which can be opened within R studio (readRDS()): "Additionally, a .RData file is saved storing all results as a list which can be opened within R studio"
