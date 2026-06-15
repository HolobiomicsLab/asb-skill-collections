---
name: quality-control-metric-evaluation
description: Use when you have measured IM-MS lipidomics data spiked with U13C labeled internal standards and need to assess whether CCS bias remains within acceptable limits for each lipid class-adduct combination.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid
schema_version: 0.2.0
---

# Quality-Control Metric Evaluation

## Summary

Systematically evaluate and visualize collision cross section (CCS) bias metrics across lipid classes and adduct combinations to assess the quality of ion mobility-mass spectrometry lipidomics measurements. This skill determines whether CCS bias estimation remains acceptable across varying numbers of internal standards and quantifies the trade-off between analytical coverage and correction accuracy.

## When to use

Apply this skill when you have measured IM-MS lipidomics data spiked with U13C labeled internal standards and need to assess whether CCS bias remains within acceptable limits for each lipid class-adduct combination. Use it to determine the minimum number of labeled lipids required per class for reliable CCS bias calculation, or to verify that CCS correction has improved measurement quality before reporting corrected CCS values.

## When NOT to use

- Your IM-MS data were not spiked with U13C labeled internal standards—internal standardization is required to calculate meaningful CCS bias without external calibration.
- You have fewer than 3 lipids in a lipid class-adduct combination—linear regression-based CCS correction functions require a minimum of 3 lipids, making bias metrics unreliable below this threshold.
- Your goal is to perform absolute CCS prediction on unknown lipids without reference standards in the same measurement—this skill assesses bias of known-standard CCS values, not predictive accuracy on unknowns.

## Inputs

- DTCCSN2 library (.csv) with U13C labeled lipid CCS reference values
- Ion mobility-mass spectrometry lipidomics data (.csv) with measured CCS values, lipid class, species, adduct, labeling status

## Outputs

- CCS bias metrics summary table (.csv) with bias (%), residual error, and lipid count per class-adduct combination
- CCS bias visualization (curve or heatmap) showing stabilization of bias estimation with increasing lipid counts
- Violin or scatter plots comparing bias before and after correction stratified by lipid class and number of standards used
- HTML and PDF quality control reports with tabulated results and diagnostic figures

## How to apply

Load the DTCCSN2 library for U13C labeled lipids and your experimental IM-MS lipidomics data (formatted as .csv with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS). Systematically subsample the detected lipids per lipid class-adduct combination at multiple levels (e.g., 1, 2, 3, 5, 10 lipids) and calculate CCS bias at each level by comparing measured CCS values of labeled standards against library reference values using internal standardization without external calibration. For each subsampling level, compute residual error or absolute bias (%) metrics. Visualize the relationship between lipid count and bias estimation quality as a curve or heatmap, monitoring for stabilization of bias estimates. Generate a summary table documenting performance metrics (e.g., mean bias %, standard deviation) at each sampling level, and verify that bias remains acceptable (typically <2%) for the minimum lipid count you plan to use in routine analysis.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias calculation, generates correction functions, and produces quality-control reports with bias metrics visualization and statistical summaries) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation_CCS-correction.Rmd', params = list(data_file = 'lipidomics_data.csv', library_file = 'U13C_DT_CCS_library.csv'), output_format = c('html_document', 'pdf_document'))
```

## Evaluation signals

- CCS bias metrics stabilize (plateau) as the number of detected lipids per lipid class increases, indicating sufficient sampling for reliable estimation.
- Mean absolute bias (%) after correction is reduced compared to before correction for each lipid class-adduct combination, and residual errors fall within expected tolerance (typically <2%).
- Summary tables report consistent bias estimates and correction function statistics across resampled subsets of the same lipid class, indicating reproducibility.
- Violin plots or distribution visualizations show narrower spread of bias values after correction versus before, and outliers are documented and traced to specific lipids or adducts.
- All lipid class-adduct combinations with ≥3 detected lipids generate valid linear regression correction functions with r² > 0.95 and reportable slopes and intercepts.

## Limitations

- CCS correction is restricted to lipid classes with ≥3 detected labeled lipids per adduct combination (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG); other classes (AcCa, Co, LPE, PG, SPH) can only be bias-assessed, not corrected.
- Linear regression-based correction assumes a monotonic relationship between measured and library CCS; nonlinear or adduct-specific artifacts may not be captured.
- The DTCCSN2 library is derived from U13C-labeled yeast extract; bias metrics and correction functions may not transfer reliably to lipids or organisms not represented in the training set.
- Resampling to simulate varying numbers of lipids per class is computationally intensive and may mask rare lipids or class-adduct combinations present in real data.

## Evidence

- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract): "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract"
- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [other] Assess bias estimation quality by computing residual error or deviation metrics between predicted and reference CCS values across lipid classes: "Assess bias estimation quality by computing residual error or deviation metrics between predicted and reference CCS values across lipid classes"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [other] Quantify the trade-off between lipid count per class and bias correction accuracy, generating a summary table of performance metrics at each sampling level: "Quantify the trade-off between lipid count per class and bias correction accuracy, generating a summary table of performance metrics at each sampling level"
