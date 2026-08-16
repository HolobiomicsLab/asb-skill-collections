---
name: collision-cross-section-measurement-quality-control
description: Use when you have IM-MS lipidomics data from samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and you need to quantify whether measured CCS values deviate systematically from theoretical values, or when you want to correct CCS measurements before downstream lipid.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# collision-cross-section-measurement-quality-control

## Summary

Assess and correct collision cross section (CCS) bias in ion mobility-mass spectrometry lipidomics data using internal standardization with U13C-labeled lipids and a reference DT CCS N2 library. This skill detects systematic CCS deviation patterns and applies class-specific linear correction functions to improve measurement accuracy.

## When to use

Apply this skill when you have IM-MS lipidomics data from samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and you need to quantify whether measured CCS values deviate systematically from theoretical values, or when you want to correct CCS measurements before downstream lipid identification and quantification.

## When NOT to use

- Samples were not spiked with U13C-labeled internal standards; internal standardization is required and external calibration alone is insufficient for reliable bias assessment.
- Lipid class-adduct combinations with fewer than 3 detected U13C-labeled lipids when CCS correction is needed; linear regression requires a minimum of 3 reference points per combination.
- Non-lipidomics IM-MS data (e.g., proteomics, small molecule analysis) where the DT CCS N2 lipid reference library is not applicable.

## Inputs

- IM-MS lipidomics measurement data (.csv file with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DT CCS N2 reference library for U13C-labeled lipids (.csv file)
- R Markdown template (MobiLipid_CCS-bias-calculation.Rmd or MobiLipid_CCS-bias-calculation_CCS-correction.Rmd)

## Outputs

- CCS bias table (.csv: CCS_bias_no_correction with percent bias before correction)
- CCS correction functions (.csv: Correction_functions with linear regression coefficients by lipid class-adduct combination)
- Mean CCS bias by function (.csv: CCS_bias_mean_by_function and CCS_bias_mean_all_functions)
- Corrected CCS values (.csv: Corrected_CCS_values and Corrected_CCS_values_mean with post-correction bias)
- HTML and PDF report with bias visualizations, violin plots, and summary statistics
- R data object (.RData file storing all results as a list for downstream use)

## How to apply

Load measured IM-MS data (as .csv with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS) and the provided DT CCS N2 reference library into R. Map detected lipid features to the library by matching lipid class, species, and adduct type. Calculate experimental-to-theoretical CCS bias as the percentage difference between measured and library CCS values for each U13C-labeled lipid. Aggregate bias metrics by lipid class-adduct combination and generate summary statistics (mean bias, standard deviation, range). If performing correction, fit linear regression functions (y = m*x + b, where x = measured CCS, y = library CCS) using U13C-labeled lipids within each class-adduct pair; a minimum of 3 lipids is required per combination. Apply the fitted correction functions to all measured CCS values regardless of labeling status. Recalculate bias post-correction to verify improvement.

## Related tools

- **MobiLipid** (R Markdown workflow for automated CCS bias assessment and correction via internal standardization) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical computing environment and data processing language for executing MobiLipid workflow)
- **ggplot2** (R package for generating CCS bias distribution visualizations and violin plots)
- **data.table** (R package for efficient aggregation and manipulation of large IM-MS feature tables)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_CCS-correction_results.html', 'MobiLipid_CCS-bias-calculation_CCS-correction_results.pdf'))
```

## Evaluation signals

- Mean CCS bias for U13C-labeled lipids decreases in magnitude after correction; post-correction bias should be substantially smaller than pre-correction bias for each lipid class-adduct combination.
- Corrected CCS values align more closely with DT CCS N2 library reference values; residuals from linear regression fit should be minimized and centered near zero.
- Summary statistics (mean bias, standard deviation, range) are computed and reported for each lipid class-adduct combination; bias metrics should be interpretable and comparable across classes.
- A minimum of 3 U13C-labeled lipids per lipid class-adduct combination are used for correction function generation; combinations with insufficient lipids are flagged as ineligible for correction.
- HTML report contains at least one bias visualization (bias table, violin plot, or class-level distribution chart) showing pre- and post-correction patterns; visual inspection confirms that correction functions were applied and bias was reduced.

## Limitations

- CCS correction is limited to lipid classes with ≥3 detected U13C-labeled lipids in a given adduct form (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG); other lipid classes (AcCa, Co, LPE, PG, SPH) can be assessed for bias but not corrected.
- Linear regression-based correction assumes a linear relationship between measured and theoretical CCS; non-linear CCS deviations may not be fully corrected.
- Internal standardization requires a priori spiking of samples with U13C-labeled yeast extract; retrospective analysis of unlabeled or differently labeled samples cannot use this workflow.
- Requires vendor-specific IM-MS calibration to be performed independently; MobiLipid supplements but does not replace calibration against external standards.
- No changelog is available; version tracking and reproducibility may be limited for published workflows using specific MobiLipid versions.

## Evidence

- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [other] MobiLipid performs CCS bias assessment through a R Markdown workflow that integrates a newly established DT CCS N2 library for U13C labeled lipids: "MobiLipid performs CCS bias assessment through a R Markdown workflow that integrates a newly established DT CCS N2 library for U13C labeled lipids, enabling internal standardization-based bias"
- [readme] CCS correction functions are based on linear regression which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [other] Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values: "Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DT CCS N2 library values as y value: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DT CCS N2 library values as y value"
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards: "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract)"
