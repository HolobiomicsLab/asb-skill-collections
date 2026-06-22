---
name: internal-standardization-correction-lipidomes
description: Use when you have IM-MS lipidomics data from samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and measured CCS values need bias assessment or correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - MobiLipid
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# internal-standardization-correction-lipidomes

## Summary

Assess and correct collision cross section (CCS) bias in ion mobility-mass spectrometry (IM-MS) lipidomics data using U13C-labeled internal standards and a reference DTCCS_N2 library. This skill eliminates the need for external calibration beyond vendor-specific requirements by leveraging lipid class-stratified bias calculation and per-class linear correction functions.

## When to use

Apply this skill when you have IM-MS lipidomics data from samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and measured CCS values need bias assessment or correction. Use it specifically when your goal is to improve CCS accuracy across multiple lipid classes within a single analytical run, without adding external calibration standards beyond instrument vendor requirements.

## When NOT to use

- Samples lacking U13C-labeled internal standard lipids; internal standardization requires detected U13C lipids within each class.
- Lipid class-adduct combinations with <3 U13C-labeled lipids detected; linear regression correction requires minimum 3 standards and is restricted to: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG.
- Data already corrected by vendor-supplied CCS calibration where no additional bias correction is acceptable or desired.

## Inputs

- Measured IM-MS CCS data as .csv file with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), CCS
- DTCCS_N2 library for U13C-labeled lipids as .csv file
- Sample requirement: ≥3 U13C-labeled lipids per lipid class-adduct combination for correction to be possible

## Outputs

- CCS bias table (%) before correction for all U13C-labeled lipids
- Corrected CCS values table with post-correction bias for each lipid and correction function
- Correction functions table with regression coefficients (slope, intercept) for each lipid class-adduct combination
- Mean CCS bias summaries by lipid class-adduct combination and by number of lipids used to generate each function
- Diagnostic plots: bias distributions before/after correction, violin plots by correction function, resampling summaries
- .html and .pdf reports with full results and tables
- .RData file storing all results as R list for downstream analysis

## How to apply

Load measured IM-MS CCS values and the DTCCS_N2 library for U13C-labeled lipids into R. Stratify measured CCS by lipid class and adduct type. For each lipid class-adduct combination with ≥3 U13C-labeled lipid standards detected, compute bias as the percent deviation between observed and library DTCCS_N2 values. Generate up to 100 linear regression correction functions (y = m*x + b, where x is measured CCS of U13C lipids and y is library CCS) by resampling 3–6 lipids per class-adduct pair. Apply the resulting correction functions to all measured CCS values (both labeled and unlabeled lipids) in each class. Evaluate correction success by computing post-correction bias and visualizing bias distributions before and after correction using diagnostic plots stratified by lipid class-adduct combination.

## Related tools

- **MobiLipid** (R Markdown implementation that automates CCS bias calculation and linear correction function generation stratified by lipid class-adduct combination) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Execution environment for statistical computing, linear regression, and data visualization within MobiLipid workflow) — https://cran.r-project.org/
- **ggplot2** (R package for generating diagnostic violin plots and bias distribution visualizations before and after correction)
- **data.table** (R package for efficient stratification and aggregation of measured CCS values by lipid class and adduct)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_CCS-correction_Example_data_import.html', 'MobiLipid_CCS-bias-calculation_CCS-correction_Example_data_import.pdf'))
```

## Evaluation signals

- Bias distribution plots show reduced spread and mean closer to zero post-correction compared to pre-correction; residual bias should be substantially smaller across all lipid class-adduct combinations.
- Linear regression correction functions are successfully generated for all lipid class-adduct combinations meeting the ≥3 U13C-lipid threshold; resampling summary confirms expected number of functions (up to 100 per combination).
- Post-correction CCS values for U13C-labeled lipids converge toward DTCCS_N2 library reference values; mean absolute bias per class should decrease by ≥50% when adequate standards are present.
- Output .csv files contain no NaN or missing values in corrected CCS columns for lipids where correction functions were applicable; all rows retain original lipid identifiers and metadata.
- Diagnostic plots and summary tables match the expected output structure documented in README (e.g., number of lipids detected table, correction function summary, violin plots stratified by lipid class-adduct).

## Limitations

- CCS correction is restricted to lipid class-adduct combinations with ≥3 U13C-labeled standards detected; classes with fewer standards can be assessed for bias but not corrected.
- Linear correction functions are generated only for lipid classes with sufficient standards (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG); other classes (e.g., AcCa, Co, LPE, PG, SPH) can be assessed but not corrected.
- Resampling approach generates up to 100 distinct correction functions per lipid class-adduct combination, increasing computational overhead and potential for overfitting if lipid diversity within a class is low.
- Method assumes U13C labeling is complete and that bias is linear within each lipid class-adduct combination; non-linear or adduct-dependent CCS behavior may not be fully captured.
- Requires samples specifically spiked with U13C-labeled internal standards (fully labeled yeast extract); cannot be applied retroactively to existing datasets lacking labeled lipid spikes.

## Evidence

- [other] MobiLipid employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization: "MobiLipid employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization, eliminating the need for additional"
- [other] For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each class): "For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value."
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract): "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract)."
