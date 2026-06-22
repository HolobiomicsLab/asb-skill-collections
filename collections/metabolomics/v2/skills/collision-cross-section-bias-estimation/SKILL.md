---
name: collision-cross-section-bias-estimation
description: Use when when you have IM-MS lipidomics data spiked with U13C labeled lipid internal standards (e.g., fully labeled yeast extract) and want to assess whether measured CCS values deviate systematically from expected values in the DTCCS_N2 reference library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0008
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

# collision-cross-section-bias-estimation

## Summary

Quantify systematic bias in measured collision cross section (CCS) values from ion mobility-mass spectrometry by comparing them against a reference DTCCS_N2 library for U13C labeled lipid standards, stratified by lipid class and adduct type. This enables detection and correction of instrument-specific CCS measurement drift without requiring external calibrants beyond vendor specifications.

## When to use

When you have IM-MS lipidomics data spiked with U13C labeled lipid internal standards (e.g., fully labeled yeast extract) and want to assess whether measured CCS values deviate systematically from expected values in the DTCCS_N2 reference library. Apply this skill if you need to quantify per-lipid-class bias before deciding whether CCS correction is necessary.

## When NOT to use

- Sample does not contain U13C labeled lipid internal standards — internal standardization requires detected labeled lipids in each lipid class to compute class-specific bias.
- Only a single U13C lipid (or fewer than 3 for class-adduct combination) is detected — bias estimation requires multiple reference points per class to be statistically meaningful.
- Measured CCS values are already bias-corrected or post-correction; this skill estimates uncorrected bias.
- Non-lipidomics IM-MS data (e.g., proteins, metabolites) — the DTCCS_N2 library is lipid-specific.

## Inputs

- IM-MS measurement data as CSV file with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), CCS
- U13C DTCCS_N2 reference library CSV file (provided with MobiLipid)
- Sample must contain detected U13C labeled lipids across lipid classes of interest

## Outputs

- CCS bias table (CSV): percent deviation of measured vs. DTCCS_N2 values per lipid
- CCS bias distribution plots (per lipid class): visualization of bias before correction
- Summary statistics: mean bias, standard deviation, and count of U13C lipids per class-adduct combination
- Diagnostic HTML/PDF report with tables and figures

## How to apply

Load measured IM-MS CCS values and the DTCCS_N2 library for U13C labeled lipids into R, then stratify all measured CCS values by lipid class and adduct combination. For each lipid class, compute the bias (in %) as the relative deviation of observed CCS from corresponding DTCCS_N2 library values for detected U13C labeled lipids within that class. The bias is calculated using internal standardization: only U13C labeled lipids detected in your sample are used as calibration references, eliminating the need for separate external calibrants. Generate diagnostic plots showing bias distribution per lipid class, including statistics such as mean bias and standard deviation before any correction. Evaluate whether the observed bias is within acceptable tolerance (typically vendor calibration specification) or if correction is warranted.

## Related tools

- **MobiLipid** (R Markdown workflow that automates CCS bias calculation and optional correction; integrates DTCCS_N2 library lookup and per-class bias computation) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Execution environment for statistical computation, linear regression, and visualization of CCS bias)
- **ggplot2** (R package for generating diagnostic bias distribution plots)
- **data.table** (R package for efficient stratification and aggregation of measured CCS by lipid class and adduct)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', params = list(data_file = 'measured_ims_data.csv', library_file = 'U13C_DT_CCS_library.csv'), output_format = c('html_document', 'pdf_document'))
```

## Evaluation signals

- Bias values are computed separately for each lipid class–adduct combination and are expressed as percentages (typically within ±5% for well-calibrated instruments).
- Number of U13C lipids used per class-adduct combination is reported; combinations with fewer than 3 lipids should be flagged as insufficiently supported.
- Bias distribution plots show non-systematic residuals (roughly centered near zero) if the instrument is well-calibrated; persistent positive or negative skew suggests systematic drift.
- All U13C lipids in the sample that match lipid class entries in the DTCCS_N2 library are included in bias calculation; none are omitted due to missing library entries.
- Output CSV tables contain complete mappings of measured CCS, library CCS, computed bias (%), lipid class, and adduct — no missing values in bias column for lipids with library entries.

## Limitations

- Requires detection of U13C labeled lipids in each lipid class; classes with no detected labeled standards cannot have bias estimated. Minimum of 1 lipid per class for bias calculation, though 3+ are recommended for robust estimates.
- Bias estimation is restricted to lipid classes present in the DTCCS_N2 library (Cer, Co, DG, HexCer, LPC, LPE, PA, PC, PE, PG, PI, PS, SPH, TG, AcCa). Other lipid classes will not have library reference values.
- Requires spiking samples with fully labeled U13C yeast extract or equivalent; endogenous U13C signal (from natural isotope abundance or prior labeling) is not a suitable substitute.
- CCS bias is measured relative to DTCCS_N2 values for N2 drift gas specifically; application to other drift gases (e.g., He) requires separate calibration data.
- Linear bias model assumes systematic offset and does not model non-linear drift or mass-dependent curvature in CCS measurement error.

## Evidence

- [other] MobiLipid employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization, eliminating the need for additional external calibration beyond vendor-specific requirements.: "employs a newly established DTCCS_N2 library for U13C labeled lipids to enable CCS bias assessment and correction through internal standardization, eliminating the need for additional external"
- [other] For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each class).: "compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each class)"
- [readme] Stratify measured CCS values by lipid class and adduct combination; requires a low number of lipids detected per lipid class for effective implementation of CCS bias calculation.: "requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction"
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract).: "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract"
- [readme] Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value.: "Input values for linear regression using the equation y = m * x + b are measured CCS values of U13C labeled lipids as x value and DTCCS_N2 library values as y value"
- [readme] To monitor the result of CCS correction, the bias between corrected CCS values and DTCCS_N2 library values of U13C labeled lipids is calculated.: "To monitor the result of CCS correction, the bias between corrected CCS values and DTCCS_N2 library values of U13C labeled lipids is calculated"
