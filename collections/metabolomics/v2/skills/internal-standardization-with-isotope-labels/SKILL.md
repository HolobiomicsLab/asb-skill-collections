---
name: internal-standardization-with-isotope-labels
description: Use when your IM-MS lipidomics samples have been spiked with fully labeled isotopic internal standards (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MobiLipid
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

# internal-standardization-with-isotope-labels

## Summary

Use fully labeled isotopic standards (e.g., U13C-labeled lipids) spiked into samples to calculate and correct systematic bias in ion mobility-derived collisional cross section (CCS) measurements without requiring additional external calibration. This approach enables accurate quality control of IM-MS lipidomics data by leveraging a reference library of isotope CCS values.

## When to use

Your IM-MS lipidomics samples have been spiked with fully labeled isotopic internal standards (e.g., U13C yeast lipid extract), and you want to quantify and correct bias in measured CCS values by comparing them to literature or newly established reference CCS values for those same isotope-labeled species. This is particularly useful when vendor-supplied CCS calibration alone is insufficient or when you have limited numbers of detected lipids per class (≥3 lipids per lipid class–adduct combination) and want to avoid measuring additional external calibration standards.

## When NOT to use

- Your samples lack isotopic internal standards or those standards are not fully labeled; this skill requires labeled lipids to serve as ground truth.
- You have fewer than 3 labeled lipids detected per lipid class–adduct combination; linear regression correction cannot be robustly fit, though bias calculation without correction is still possible.
- Your reference CCS library does not cover the isotopic form (e.g., U13C) or adduct type measured in your samples; comparison and correction cannot proceed.

## Inputs

- IM-MS lipidomics data table (CSV format) with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), measured CCS
- Reference DTCCSN2 library (CSV) for U13C-labeled lipids with columns: LipidClass, LipidSpecies, Adduct, library CCS
- Sample must contain detectable U13C-labeled internal standards across ≥3 lipids per lipid class–adduct combination (where correction is desired)

## Outputs

- CCS bias table (%) before correction for each lipid and lipid class–adduct combination
- Correction functions (linear regression slope and intercept) for each lipid class–adduct pair (if ≥3 labeled lipids available)
- Corrected CCS values for all lipids (labeled and unlabeled) after function application
- CCS bias table (%) after correction, summarized by number of lipids used to generate each correction function
- HTML and PDF reports with tabular and visual summaries (violin plots, bias scatter plots, correction function summaries)
- RData object storing all results as a list for downstream R analysis

## How to apply

Spike your sample with fully labeled isotopic internal standards (e.g., U13C-labeled yeast lipids). Load both the experimental IM-MS lipidomics data (with measured CCS values for both light and heavy labeled species) and a reference library of DTCCSN2 values for the isotope-labeled standards into your analysis workflow. For each lipid class–adduct combination detected in your sample, calculate bias by computing the residual error (measured CCS minus library CCS) across all available labeled lipids in that class. If you have ≥3 labeled lipids per class–adduct combination, optionally generate linear regression correction functions using measured CCS as the independent variable and library CCS as the dependent variable. Apply these correction functions to all measured CCS values (both labeled and unlabeled) to yield corrected CCS and recalculate bias post-correction to confirm improvement. Monitor correction quality via residual error, deviation metrics, or absolute CCS bias (%) before and after.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias calculation and correction using internal standardization with U13C-labeled lipids) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical computing environment for loading data, performing linear regression, calculating bias metrics, and generating reports)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_experiment.html', 'MobiLipid_experiment.pdf'))
```

## Evaluation signals

- Bias residuals (measured CCS − library CCS) for labeled lipids decrease in magnitude and variance after correction; visual inspection via violin plots or scatter plots should show tightening of the distribution around zero.
- Mean absolute CCS bias (%) for each lipid class–adduct pair decreases after correction; quantitative metrics should improve by ≥10–20% where correction functions are applied.
- Correction functions are generated only for lipid class–adduct combinations with ≥3 labeled lipids, and those combinations should have valid linear regression fits (check R² and residual distributions).
- Corrected CCS values for unlabeled lipids lie within the confidence interval or residual bounds established by the correction function, indicating physically plausible estimates.
- Output CSV and HTML files contain complete tables (all lipids and all lipid class–adduct combinations), with no missing values where correction was performed; R-generated report renders without errors.

## Limitations

- Correction functions require a minimum of 3 labeled lipids per lipid class–adduct combination; lipid classes or adducts with <3 detections cannot be corrected, only bias-calculated.
- Linear regression correction assumes a linear relationship between measured and true CCS; significant non-linearity or instrumental artifacts may not be fully captured.
- The approach depends on the accuracy and completeness of the reference DTCCSN2 library for the isotopic form used; systematic errors in the library will propagate to corrected CCS values.
- Resampling or Monte Carlo approaches may generate multiple correction functions per class–adduct pair (up to 100), introducing model uncertainty; reported metrics should reflect this variability.

## Evidence

- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [readme] Requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction: "requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid"
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards: "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract)"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCSN2 library values as y value: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCSN2 library values as y value"
- [readme] After generation of all CCS correction functions, all measured CCS values are corrected, irrespective of their labeling status: "After generation of all CCS correction functions, all measured CCS values are corrected, irrespective of their labeling status"
