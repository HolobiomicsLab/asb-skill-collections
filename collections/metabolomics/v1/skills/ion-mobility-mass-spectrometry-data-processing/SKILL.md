---
name: ion-mobility-mass-spectrometry-data-processing
description: Use when you have (LC-)IM-MS lipidomics data from samples spiked with U13C labeled internal standards (e.g., fully labeled yeast extract) and need to quantify and correct systematic CCS bias before downstream lipid identification or quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - R
  - MobiLipid
  - RStudio
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
---

# Ion Mobility–Mass Spectrometry Data Processing

## Summary

Processing and quality control of IM-MS lipidomics data by calculating and correcting collision cross section (CCS) bias using internal standardization with U13C labeled lipid standards. This skill enables automated assessment of systematic CCS deviation and generation of lipid class–adduct-specific correction functions without requiring additional external calibration.

## When to use

You have (LC-)IM-MS lipidomics data from samples spiked with U13C labeled internal standards (e.g., fully labeled yeast extract) and need to quantify and correct systematic CCS bias before downstream lipid identification or quantification. This is appropriate when vendor-specific calibration alone does not account for class-dependent CCS deviations.

## When NOT to use

- Samples were not spiked with U13C labeled internal standards; internal standardization is the foundation of this workflow.
- Your goal is to identify unknown lipids de novo without reference data; this skill assumes a populated reference library for bias quantification.
- CCS values are already pre-corrected by instrument vendor software and no further bias assessment is required.

## Inputs

- CSV file with measured IM-MS lipidomics data (columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DTCCSN2 reference library CSV for U13C labeled lipids
- Samples spiked with U13C labeled internal standards

## Outputs

- CCS bias values (%) by lipid class–adduct combination before and after correction
- Linear regression correction functions (up to 100 distinct functions) with coefficients m and b per lipid class–adduct pair
- Corrected CCS values for all detected lipids
- HTML and PDF reports with bias assessment tables and visualizations (violin plots, scatter plots, summary statistics)
- RData file and CSV files documenting bias metrics, correction functions, and corrected CCS values

## How to apply

Load measured IM-MS lipidomics data (in CSV format with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS) and the DTCCSN2 reference library for U13C labeled lipids into R. Map detected U13C labeled lipid features to library entries by lipid class and species nomenclature, then calculate experimental-to-theoretical CCS bias as the difference between measured and reference CCS values. Aggregate bias metrics by lipid class–adduct combination and compute summary statistics (mean bias, standard deviation, range). If correction is desired, generate linear regression correction functions for each lipid class–adduct pair using a minimum of 3 U13C lipids per combination (derived from resampling), then apply the fitted correction functions to all measured CCS values (labeled and unlabeled). Assess correction quality by recalculating bias after application and visualizing before/after distributions.

## Related tools

- **MobiLipid** (R Markdown workflow that integrates DTCCSN2 library, performs CCS bias calculation and linear regression–based correction, and generates automated reports) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical computing environment for executing MobiLipid Markdown, data manipulation (data.table), visualization (ggplot2, ggbeeswarm), and linear regression)
- **RStudio** (IDE for editing, rendering, and executing MobiLipid R Markdown files)

## Examples

```
# Open MobiLipid workflow in R:
Rmd <- tcltk::tk_choose.files(caption = "Select R markdown (.Rmd file) which should be used for data processing:", filters = matrix(c("Rmd files", "Rmd"), 1, 2), multi = FALSE)
data_import <- tcltk::tk_choose.files(caption = "Data import (measured data as CSV file):", filters = matrix(c("csv files", "csv"), 1, 2), multi = FALSE)
rmarkdown::render(Rmd, output_format = c("html_document", "pdf_document"))
```

## Evaluation signals

- CCS bias values (mean and range per lipid class–adduct combination) are numeric, fall within ±10% for well-calibrated systems, and show systematic patterns consistent with known ion mobility behavior
- Corrected CCS values reduce bias by ≥30% on average when compared to uncorrected values, with residual error between corrected and reference CCS values smaller than before correction
- Correction functions are generated only for lipid class–adduct pairs with ≥3 detected U13C labeled lipids; pairs with <3 lipids are flagged and excluded from correction
- Violin plots and scatter plots show tighter clustering and reduced systematic offset after correction relative to reference library values
- Output CSV files (CCS_bias_no_correction, Corrected_CCS_values, Correction_functions) are populated with valid numeric values and match expected lipid class nomenclature

## Limitations

- CCS correction is restricted to lipid classes with ≥3 U13C labeled lipids in the same adduct form; classes below this threshold (e.g., Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG with fewer than 3 lipids) cannot be corrected, only assessed for bias
- Linear regression correction assumes a linear relationship between measured and reference CCS; non-linear bias patterns may not be adequately modeled
- The DTCCSN2 library is specific to fully labeled yeast extract U13C lipids under specified ion mobility conditions (N2 drift gas); applicability to other labeling schemes or buffer gases is not validated
- Up to 100 distinct correction functions are generated through resampling (3–6 lipids per function); performance depends on the number and diversity of available U13C standards per class–adduct pair

## Evidence

- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract): "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract"
- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [other] Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values: "Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [readme] MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression: "MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression"
- [intro] requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction: "requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction"
