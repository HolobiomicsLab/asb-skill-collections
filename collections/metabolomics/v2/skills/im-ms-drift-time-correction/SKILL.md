---
name: im-ms-drift-time-correction
description: Use when when you have IM-MS lipidomics data acquired on samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and need to quantify systematic CCS bias and apply lipid class-specific bias correction to all measured CCS values, particularly when multiple lipids per lipid.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
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

# IM-MS Drift Time Correction

## Summary

Automated assessment and correction of collision cross section (CCS) bias in ion mobility–mass spectrometry analyses using internal U13C-labeled lipid standards and linear regression-based correction functions. This skill eliminates the need for external calibration beyond vendor-specific requirements by leveraging a DT CCS N2 library.

## When to use

When you have IM-MS lipidomics data acquired on samples spiked with U13C-labeled internal standards (fully labeled yeast extract) and need to quantify systematic CCS bias and apply lipid class-specific bias correction to all measured CCS values, particularly when multiple lipids per lipid class-adduct combination are detected (minimum 3 required for correction).

## When NOT to use

- Samples were not spiked with U13C-labeled lipid internal standards; the correction function relies on measured U13C lipids as anchors.
- Lipid class-adduct combinations have fewer than 3 detected U13C labeled lipids; linear regression cannot be reliably estimated and correction will be skipped for that combination.
- Input CCS data do not follow the required CSV schema (File, LipidClass, LipidSpecies, Adduct, Label, CCS columns) or use non-standard lipid nomenclature or adduct notation incompatible with the DT CCS N2 library.

## Inputs

- Measured data CSV file with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS
- DT CCS N2 library CSV file for U13C labeled lipids
- R Markdown template (MobiLipid_CCS-bias-calculation_CCS-correction.Rmd)

## Outputs

- HTML and PDF reports with CCS bias and correction visualizations
- RData file containing results as a list for downstream R analysis
- CSV: CCS_bias_no_correction (bias % before correction)
- CSV: Correction_functions (all generated linear regression models)
- CSV: CCS_bias_mean_by_function (mean bias per lipid class-adduct per function)
- CSV: CCS_bias_mean_all_functions (aggregated bias across functions by lipid count)
- CSV: Corrected_CCS_values (corrected CCS and residual bias per lipid per function)
- CSV: Corrected_CCS_values_mean (mean corrected CCS per lipid across functions by lipid count)

## How to apply

Load measured CCS data (with File, LipidClass, LipidSpecies, Adduct, Label, and CCS columns) and the DT CCS N2 library for U13C labeled lipids. First, calculate CCS bias by comparing measured values of U13C labeled lipids against library reference values. For lipid class-adduct combinations with ≥3 labeled lipids, generate correction functions via linear regression (y = m*x + b, where x = measured CCS of U13C lipids, y = library CCS values). MobiLipid computes up to 100 distinct correction functions using random resampling of 3–6 lipids per combination. Apply the resulting correction functions to all measured CCS values (labeled and unlabeled). Finally, recalculate bias between corrected CCS and library values to verify correction efficacy. The workflow restricts correction to lipid classes with sufficient standards: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG.

## Related tools

- **MobiLipid** (R Markdown workflow for automated CCS bias calculation and correction; implements linear regression correction functions and generates multi-format reports) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Execution environment for the R Markdown workflow; required packages: htmltools, rmarkdown, data.table, ggplot2, DT, webshot, tcltk, knitr, ggbeeswarm) — https://cran.r-project.org/

## Examples

```
rmarkdown::render("MobiLipid_CCS-bias-calculation_CCS-correction.Rmd", output_format = c("html_document", "pdf_document"), output_file = c("MobiLipid_output.html", "MobiLipid_output.pdf"))
```

## Evaluation signals

- Mean CCS bias (%) after correction is substantially lower than before correction for each lipid class-adduct combination, as shown in violin plots and summary tables.
- Corrected CCS values are closer to DT CCS N2 library reference values for U13C labeled lipids; residual bias is minimized across all correction functions.
- All output CSV files contain expected columns and row counts matching the input lipid detections; no missing values in corrected CCS or bias calculations.
- Number of generated correction functions per lipid class-adduct matches expected resampling: up to 100 functions with 3–6 lipids per function.
- Correction is applied uniformly to all measured CCS values (both labeled and unlabeled); Corrected_CCS_values and Corrected_CCS_values_mean tables include all input lipids.

## Limitations

- CCS correction is restricted to 10 lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG) because they require a minimum of 3 U13C labeled lipids for linear regression; other classes are only assessed for bias without correction.
- Correction relies on linear regression and assumes a linear relationship between measured and true CCS across the m/z range; non-linear bias patterns or instrument-specific deviations may not be fully captured.
- Accuracy depends on the quality and relevance of the DT CCS N2 library for U13C yeast lipids; if lipid species in the sample are absent from the library or have atypical CCS behavior, bias estimation will be imprecise.
- Resampling-based correction function generation introduces variability; results must be interpreted as an ensemble mean across up to 100 functions rather than a single deterministic model.

## Evidence

- [intro] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DT CCS N2 library values as y value: "Input values for linear regression using the equation *y* = *m* \* *x* + *b* are measured CCS values of U<sup>13</sup>C labeled lipids as x value and <sup>DT</sup>CCS<sub>N2</sub> library values as y"
- [readme] After generation of all CCS correction functions, all measured CCS values are corrected, irrespective of their labeling status: "After generation of all CCS correction functions, all measured CCS values are corrected, irrespective of their labeling status"
- [readme] MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression: "MobiLipid computes up to 100 distinct correction functions employing 3 to 6 lipids of a lipid class-adduct combination for linear regression"
