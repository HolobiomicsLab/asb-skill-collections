---
name: lipid-class-stratified-analysis
description: Use when you have IM-MS lipidomics data with measured CCS values, samples spiked with U13C-labeled lipid internal standards (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MobiLipid
  - ggplot2
  - data.table
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
---

# lipid-class-stratified-analysis

## Summary

Stratify ion mobility-mass spectrometry (IM-MS) lipidomics data by lipid class and adduct type to assess and correct collision cross section (CCS) bias using internal U13C-labeled lipid standards. This skill enables class-level bias quantification and correction function generation without requiring external calibration beyond vendor specifications.

## When to use

Apply this skill when you have IM-MS lipidomics data with measured CCS values, samples spiked with U13C-labeled lipid internal standards (e.g., fully labeled yeast extract), and need to evaluate whether systematic CCS bias varies by lipid class-adduct combination and whether you have sufficient lipids per class to estimate and correct that bias.

## When NOT to use

- Your samples do not contain U13C-labeled internal standards; MobiLipid requires internal standardization and cannot work with external calibration alone.
- You have fewer than 3 U13C-labeled lipids in a lipid class-adduct combination; CCS correction functions require a minimum of 3 lipids for linear regression.
- Your lipid class-adduct combinations are outside the supported set (Cer, Co, DG, HexCer, LPC, LPE, PA, PC, PE, PG, PI, PS, SPH, TG with specific allowed adducts); bias assessment may proceed but correction will not be generated.

## Inputs

- Measured IM-MS lipidomics data (.csv) with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), CCS
- DT CCS N2 library for U13C labeled lipids (.csv) with reference CCS values by lipid species, class, and adduct
- Ion mobility-mass spectrometry analysis results from samples spiked with U13C-labeled internal standards

## Outputs

- CCS bias values (%) stratified by lipid class-adduct combination (mean, SD, range)
- Bias assessment report with class-level visualizations (box plots, violin plots)
- CCS correction functions (linear regression coefficients) per lipid class-adduct combination
- Corrected CCS values with associated metadata (lipid ID, m/z, corrected CCS, original CCS, bias factor)
- Summary tables: CCS bias before/after correction, correction function parameters, mean bias by class-adduct and number of lipids used
- HTML and PDF reports with tables and figures
- RData file containing all results as an R list for downstream analysis

## How to apply

Load your measured IM-MS lipidomics data (as .csv with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS) and the DT CCS N2 reference library for U13C labeled lipids into R. Map detected U13C-labeled lipids to the library by lipid class and adduct type. For each class-adduct combination, calculate bias as the difference between measured and library CCS values, then aggregate bias statistics (mean, standard deviation, range) by class. Generate class-level visualizations (box plots, violin plots) showing bias distribution. If planning CCS correction, verify that each class-adduct combination has at least 3 U13C-labeled lipids available for linear regression; MobiLipid will then compute up to 100 distinct correction functions using 3–6 lipids per class-adduct pair, apply the correction to all detected lipids (labeled or unlabeled), and recalculate bias post-correction to assess improvement.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias assessment and correction by lipid class-adduct combination) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical computing environment for executing the MobiLipid R Markdown workflow)
- **ggplot2** (R package for generating class-stratified bias visualizations (violin plots, box plots))
- **data.table** (R package for efficient aggregation and stratification of bias metrics by class-adduct)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_example_data.html', 'MobiLipid_example_data.pdf'))
```

## Evaluation signals

- Bias statistics (mean, SD) are successfully computed and reported for each lipid class-adduct combination with at least one U13C-labeled lipid detected.
- Visualizations (violin plots, box plots) display CCS bias distribution stratified by lipid class-adduct, showing systematic patterns or class-specific offsets.
- If CCS correction is performed: correction functions are generated only for class-adduct combinations with ≥3 U13C-labeled lipids; all other combinations show 'correction not possible' status.
- Mean CCS bias after correction is reduced compared to before correction for class-adduct combinations where correction functions were applied; residual bias should be near zero or substantially smaller.
- Output .csv files (CCS_bias_no_correction, Correction_functions, Corrected_CCS_values) contain non-empty rows with valid numeric values for bias (%), correction coefficients (slope, intercept), and corrected CCS, with lipid identifiers matching input data.

## Limitations

- CCS correction is restricted to lipid classes with ≥3 U13C-labeled lipids per class-adduct combination; classes with fewer lipids will have bias assessed but not corrected.
- Linear regression correction functions are generated from only 3–6 U13C-labeled lipids per class-adduct pair, which may not capture non-linear drift or complex instrument behavior across the full m/z range.
- MobiLipid requires samples to be spiked with a specific U13C-labeled yeast extract (Neubauer et al. 2012) and is not compatible with other internal standard compositions; the reference library is specific to this labeling source.
- Supported lipid classes and adduct types are predefined (e.g., PC with [M+H], [M+Na], [M+HCOO]; TG only with [M+NH4], [M+Na]); analysis of unsupported class-adduct pairs will fail or be skipped.
- No changelog is documented; versioning and updates to the reference library or methodology are not explicitly tracked.

## Evidence

- [readme] CCS bias calculation and correction by lipid class-adduct: "compute correction function for each lipid class-adduct combinations (possible combinations are listed in the table below"
- [intro] Minimum lipid count for effective bias calculation: "requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction"
- [readme] Minimum lipids for correction function generation: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [intro] Internal standardization without external calibration: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [readme] Workflow input data format and stratification: "The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS""
- [readme] Output includes stratified bias and correction tables: "CCS_bias_mean_by_function: Table with the mean CCS bias for each lipid class-adduct combination for each correction function"
