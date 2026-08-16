---
name: collision-cross-section-bias-quantification
description: Use when you have ion mobility-mass spectrometry lipidomics data from samples spiked with U¹³C-labeled lipid internal standards (fully labeled yeast extract) and want to assess whether measured CCS values systematically deviate from a validated DT CCS N₂ reference library, indicating bias that may.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MobiLipid
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

# collision-cross-section-bias-quantification

## Summary

Quantify systematic bias in measured collision cross section (CCS) values relative to a reference library by comparing ion mobility-mass spectrometry measurements of U¹³C-labeled internal standard lipids against their known theoretical CCS values. This enables detection of instrument drift or calibration error before applying correction.

## When to use

Apply this skill when you have ion mobility-mass spectrometry lipidomics data from samples spiked with U¹³C-labeled lipid internal standards (fully labeled yeast extract) and want to assess whether measured CCS values systematically deviate from a validated DT CCS N₂ reference library, indicating bias that may affect downstream lipid quantification or identification.

## When NOT to use

- Input data lacks U¹³C-labeled internal standards or does not include heavy-labeled lipids marked in the Label column — bias cannot be calculated without reference standards
- Reference library values are unavailable or do not cover the lipid classes detected in your sample
- CCS values have already been corrected by the instrument vendor — bias quantification is most meaningful on raw, uncorrected measured data

## Inputs

- CSV file with measured IM-MS data (columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DT CCS N₂ reference library for U¹³C-labeled lipids (CSV format)
- Requirement: Data must include U¹³C-labeled lipids marked as 'heavy' in Label column

## Outputs

- CCS bias table (%) per lipid-adduct combination
- Mean and standard deviation of bias per lipid class-adduct pair
- Bias visualization figures (scatter plots, violin plots by lipid class)
- HTML and PDF reports summarizing bias statistics and distribution
- RData file storing all bias calculation results as an R list

## How to apply

Load measured CCS values for U¹³C-labeled lipids from your analysis output as a CSV file (with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS), and pair each measured value with its corresponding theoretical CCS from the DT CCS N₂ library for U¹³C labeled lipids. Calculate bias as percentage deviation: [(measured CCS − library CCS) / library CCS] × 100 for each lipid-adduct pair, then stratify bias statistics by lipid class-adduct combination. The MobiLipid R Markdown automates this calculation and produces visualizations (bias distributions, mean bias per class) to identify systematic shifts. Bias values near zero indicate good agreement; systematic positive or negative shifts suggest instrument calibration drift requiring correction or recalibration.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias calculation, generates correction functions, and produces HTML/PDF reports with bias statistics and visualizations) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical computing environment in which the MobiLipid markdown executes bias calculations and rendering)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_mydata.html', 'MobiLipid_CCS-bias-calculation_mydata.pdf'))
```

## Evaluation signals

- Bias values for U¹³C-labeled lipids should cluster tightly around zero (or a small systematic offset); wide or asymmetric distributions suggest instrument instability or miscalibration
- Bias statistics should be stratified by lipid class-adduct combination and show consistency within each class (homogeneous bias suggests class-specific systematic error rather than random noise)
- Minimum of 3 U¹³C-labeled lipids per lipid class-adduct combination should be present; classes with fewer lipids will show larger confidence intervals
- Cross-check: bias values calculated from raw measured CCS and library CCS should match those output in the CCS_bias_no_correction CSV file
- Visual inspection of bias plots (scatter or violin) should reveal whether bias is random (scatter around zero) or systematic (consistent positive or negative shift)

## Limitations

- CCS bias calculation and correction requires a minimum of 3 U¹³C-labeled lipids per lipid class-adduct combination; lipid classes with fewer detections cannot be corrected and will show large statistical uncertainty
- The DT CCS N₂ reference library is specific to U¹³C-labeled yeast extract; bias quantification applies only to those internal standards; correction of unlabeled analytes is indirect and depends on linear regression quality
- Linear regression-based correction functions assume a linear relationship between measured and true CCS; non-linear drift or adduct-specific calibration issues may not be fully captured
- Bias quantification is most reliable for lipid classes well-represented in the reference library; lipid classes with sparse or missing library entries will yield unreliable bias estimates

## Evidence

- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization.: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [other] Bias assessment results (bias factors and statistics per lipid class) are loaded from the upstream bias assessment step and quantify CCS deviation.: "Load bias assessment results (bias factors and statistics per lipid class) from the upstream bias assessment step"
- [readme] Bias is calculated between measured CCS values and library values of U¹³C labeled lipids using linear regression.: "to first calculate CCS bias between measured CCS values and library values of U<sup>13</sup>C labeled lipids"
- [readme] Minimum of 3 lipids per lipid class-adduct combination is required for effective CCS bias calculation.: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
- [readme] Bias calculation output includes CCS bias before correction, and visualizations stratified by lipid class.: "CCS bias calculation without CCS correction [with] CCS bias table [and] CCS bias figure"
