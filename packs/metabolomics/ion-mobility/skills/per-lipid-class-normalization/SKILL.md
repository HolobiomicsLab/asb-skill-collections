---
name: per-lipid-class-normalization
description: Use when you have IM-MS lipidomic data from samples spiked with U13C-labeled internal standards (e.g., fully labeled yeast extract), measured CCS values stratified by lipid class and adduct type, and access to the DTCCS_N2 reference library for U13C lipids.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3370
  tools:
  - R
  - MobiLipid
  - RStudio
  - ggplot2
  - data.table
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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

# Per-Lipid-Class CCS Bias Calculation and Correction

## Summary

Compute and correct collision cross section (CCS) bias in ion mobility–mass spectrometry (IM-MS) lipidomics by stratifying measured CCS values by lipid class, deriving per-class bias from U13C-labeled internal standards against the DTCCS_N2 library, and applying linear regression–based correction functions to all lipids in each class.

## When to use

Apply this skill when you have IM-MS lipidomic data from samples spiked with U13C-labeled internal standards (e.g., fully labeled yeast extract), measured CCS values stratified by lipid class and adduct type, and access to the DTCCS_N2 reference library for U13C lipids. Use it to remove systematic CCS bias before reporting corrected CCS metrics for lipidomic annotation or cross-platform comparison, particularly when vendor-specific calibration alone is insufficient for the required accuracy.

## When NOT to use

- Lipid class–adduct combination contains fewer than 3 U13C-labeled lipids detected; CCS correction cannot be generated (bias calculation still possible).
- Measured CCS values are already corrected by vendor software or external calibration; applying additional per-class normalization may introduce overcorrection.
- Samples lack isotopic spike-in standards or U13C labeling; internal standardization approach is inapplicable and external calibration standards are required instead.

## Inputs

- Measured IM-MS CCS data table (CSV format with headers: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DTCCS_N2 library for U13C-labeled lipids (CSV file)
- Sample spiked with U13C-labeled internal standards (fully labeled yeast extract or equivalent)

## Outputs

- CCS_bias_no_correction table (CCS bias % before correction)
- Correction_functions table (all generated linear regression functions)
- Corrected_CCS_values table (bias-corrected CCS and residual bias for each lipid across all correction functions)
- Corrected_CCS_values_mean table (mean corrected CCS per lipid grouped by number of standards used)
- CCS_bias_mean_by_function and CCS_bias_mean_all_functions tables (mean bias per lipid class–adduct combination)
- Diagnostic HTML and PDF reports with bias distribution plots, violin plots, and tabular summaries
- RData file storing all results as structured list

## How to apply

Load measured IM-MS CCS data and the DTCCS_N2 library for U13C-labeled lipids into R. Stratify all measured CCS values by lipid class. For each lipid class–adduct combination containing ≥3 U13C-labeled lipids, compute the observed CCS bias as the deviation of measured CCS from reference DTCCS_N2 values; use linear regression (y = m·x + b, where x is measured CCS of labeled lipids and y is library CCS) to generate up to 100 distinct correction functions by resampling subsets of 3–6 labeled lipids. Apply each correction function to all measured CCS values (both light and heavy isotopologues) in that class–adduct combination. Output bias-corrected CCS tables and diagnostic plots showing bias distribution before and after correction; monitor success by computing residual bias between corrected CCS and DTCCS_N2 values for labeled lipids.

## Related tools

- **R** (Execution engine for CCS bias calculation, linear regression, resampling, and visualization) — https://cran.r-project.org/
- **RStudio** (IDE for running R Markdown workflows and interactive data exploration) — https://www.rstudio.com/products/rstudio/download/
- **MobiLipid** (R Markdown modules (MobiLipid_CCS-bias-calculation.Rmd and MobiLipid_CCS-bias-calculation_CCS-correction.Rmd) that automate per-class bias calculation and correction) — https://github.com/FelinaHildebrand/MobiLipid
- **ggplot2** (R package for generating diagnostic plots (violin plots, bias distributions, correction function summaries))
- **data.table** (R package for efficient stratification and summarization of CCS data by lipid class)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_CCS-correction_example.html', 'MobiLipid_CCS-bias-calculation_CCS-correction_example.pdf'))
```

## Evaluation signals

- Mean CCS bias after correction should be substantially lower (closer to zero) than before correction for each lipid class–adduct combination, with residual bias typically <2–3% for well-behaved classes.
- Violin plots and bias distribution plots show narrower spread and median shift toward zero after correction compared to uncorrected bias.
- All generated correction functions are linear (y = m·x + b) with R² values and sample sizes (3–6 lipids) documented in the Correction_functions table.
- Corrected_CCS_values table contains no NaN or infinite values; all corrected CCS entries correspond to a valid correction function for the lipid class–adduct combination.
- Output report includes resampling summary confirming that up to 100 distinct functions were generated per class–adduct combination with ≥3 lipids; lipid classes with <3 standards are explicitly flagged as non-correctable.

## Limitations

- CCS correction requires ≥3 U13C-labeled lipids detected in each lipid class–adduct combination; restricted to 10 supported classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG). Other classes (e.g., AcCa, Co, LPE, PG, SPH) undergo bias calculation only, without correction.
- Linear regression models assume a linear relationship between measured and reference CCS over the observed range; nonlinear instrument drift or adduct-specific effects outside the calibration range may not be captured.
- Requires samples spiked with U13C-labeled internal standards; methodology is not applicable to datasets lacking isotopic labeling or to external validation cohorts without matched spike-in.
- Resampling generates up to 100 correction functions per class–adduct combination; mean corrected CCS and residual bias are reported as aggregate statistics, and individual correction function performance may vary.
- DTCCS_N2 library is specific to U13C-labeled yeast lipid extract; applicability to other labeled sources or organisms not explicitly validated in the publication.

## Evidence

- [other] Load measured IM-MS CCS values and the DT CCS N2 library for U13C labeled lipids into R. Stratify measured CCS values by lipid class.: "Load measured IM-MS CCS values and the DT CCS N2 library for U13C labeled lipids into R. Stratify measured CCS values by lipid class."
- [other] For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each class).: "For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each"
- [other] Apply the computed per-class bias correction to all CCS measurements in that lipid class. Output bias-corrected CCS table and generate diagnostic plots showing bias distribution per lipid class before and after correction.: "Apply the computed per-class bias correction to all CCS measurements in that lipid class. Output bias-corrected CCS table and generate diagnostic plots showing bias distribution per lipid class"
- [other] MobiLipid employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization, eliminating the need for additional external calibration beyond vendor-specific requirements.: "MobiLipid employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization, eliminating the need for additional"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value. After generation of all CCS correction functions, all measured CCS values are corrected, irrespective of their labeling status.: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value. After generation of all CCS"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG.: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid"
- [readme] MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression.: "MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression."
