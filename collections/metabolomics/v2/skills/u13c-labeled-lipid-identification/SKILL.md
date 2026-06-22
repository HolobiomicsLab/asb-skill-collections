---
name: u13c-labeled-lipid-identification
description: Use when you have measured CCS values from (LC-)IM-MS samples spiked with U¹³C labeled internal standards (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0153
  tools:
  - R
  - MobiLipid R Markdown
  - R (ggplot2, data.table, DT packages)
  - MobiLipid
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- providing a R Markdown that integrates into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  - build: coll_mobilipid_cq
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

# u13c-labeled-lipid-identification

## Summary

Identify and validate U¹³C labeled lipids in ion mobility-mass spectrometry (IM-MS) lipidomics data by matching measured CCS values against a reference DTCCSN2 library and calculating bias to assess data quality. This skill enables internal standardization for CCS quality control without requiring external calibration.

## When to use

Apply this skill when you have measured CCS values from (LC-)IM-MS samples spiked with U¹³C labeled internal standards (e.g., fully labeled yeast extract) and need to: (1) identify which measured lipids correspond to U¹³C labeled reference compounds, (2) assess CCS measurement bias relative to library values, or (3) establish correction functions for downstream CCS bias correction. The input data must contain lipid class, lipid species, adduct type, and measured CCS value for each detected lipid.

## When NOT to use

- If your samples were not spiked with U¹³C labeled internal standards; this skill requires known U¹³C reference lipids to identify and match.
- If your measured data lacks CCS values or does not include explicit labeling status (light vs. heavy); the skill cannot match unlabeled lipids to a U¹³C reference library.
- If your lipid nomenclature (class, species, adduct annotation) does not match the DTCCSN2 library format; mismatched nomenclature will prevent correct matching and introduce false negatives.

## Inputs

- CSV file with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS (measured data from spiked IM-MS samples)
- DTCCSN2 library CSV file (U13C_DT_CCS_library.csv) containing reference CCS values for U¹³C labeled lipids
- Metadata: sample file names, lipid nomenclature (must match library), adduct types

## Outputs

- CCS bias calculation table (% bias for each U¹³C labeled lipid matched to library entry)
- CCS bias summary figures (e.g., boxplots or violin plots grouped by lipid class-adduct combination)
- HTML and PDF report with tables and visualizations of bias before correction
- RData file storing all matched lipids, library lookups, and bias values for downstream use
- CSV file (CCS_bias_no_correction) with bias (%) for each identified U¹³C labeled lipid

## How to apply

Prepare input as a .csv file with columns: File, LipidClass, LipidSpecies, Adduct, Label ('heavy' for U¹³C), and CCS. Load the provided DTCCSN2 library (U13C_DT_CCS_library.csv) which contains reference DTCCSN2 CCS values for U¹³C labeled lipids across lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, etc.) and supported adducts ([M+H], [M+NH₄], [M+Na], [M-H], [M+HCOO]). Match measured U¹³C labeled lipids to library entries by lipid class, species, and adduct. Calculate CCS bias as the percent difference between measured and library CCS values. Identify lipids where measurement quality is acceptable (CCS values are numeric and within physically plausible ranges for ion mobility). Use R markdown workflow (MobiLipid_CCS-bias-calculation.Rmd) to automate matching, bias calculation, and report generation. The skill succeeds when all expected U¹³C labeled lipids are correctly matched to library entries and bias is quantified.

## Related tools

- **MobiLipid R Markdown** (Automated workflow for U¹³C lipid identification, library matching, CCS bias calculation, and reporting) — https://github.com/FelinaHildebrand/MobiLipid
- **R (ggplot2, data.table, DT packages)** (Data manipulation, visualization, and interactive table generation for CCS bias reports)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', output_format=c('html_document','pdf_document'), output_file=c('MobiLipid_CCS-bias-calculation_results.html','MobiLipid_CCS-bias-calculation_results.pdf'))
```

## Evaluation signals

- All U¹³C labeled lipids in the input data are successfully matched to DTCCSN2 library entries (100% match rate for lipids present in both input and library)
- CCS bias values are numeric, finite, and fall within expected ranges (typically ±5–10% for high-quality IM-MS data); no NaN or infinite values
- Matched lipids show the correct adduct types for their lipid class (e.g., PC with [M+H], [M+Na], [M+HCOO]; no mismatches like PC with [M-H])
- Bias distribution is visualized by lipid class-adduct combination with summary statistics (mean, median, std dev); outliers or systematic shifts are apparent
- Report includes a summary table showing count of U¹³C lipids detected per lipid class-adduct combination; minimum of 3 lipids per combination indicates sufficient coverage for correction function generation in downstream steps

## Limitations

- The DTCCSN2 library covers only a subset of lipid classes (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, and others listed in README); lipid classes outside this set cannot be identified via library matching.
- CCS bias calculation is sensitive to nomenclature consistency; any deviation in lipid class, species, or adduct notation between input and library will result in failed matches.
- The skill requires a minimum of 3 U¹³C labeled lipids per lipid class-adduct combination to support downstream CCS correction function generation; samples with sparse labeling may not achieve sufficient coverage.
- Measured CCS values must be from the same IM-MS instrument platform and gas (N₂) as the reference library; values from other gases (He, Ar) or different instruments are not directly comparable.
- No changelog or version history is documented in the repository; users cannot track updates or compatibility changes to the DTCCSN2 library or R markdown workflows.

## Evidence

- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U¹³C labeled internal standards (fully labeled yeast extract): "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U¹³C labeled internal standards"
- [readme] The .csv file has to have the following headers: 'File', 'LipidClass', 'LipidSpecies', 'Adduct', 'Label', 'CCS': "The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS""
- [readme] Employing a newly established DTCCSN2 library for U¹³C labeled lipids, which is provided together with the code: "Employing a newly established DTCCSN2 library for U¹³C labeled lipids, which is provided together with the code"
- [readme] MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization: "MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization"
- [readme] to first calculate CCS bias between measured CCS values and library values of U¹³C labeled lipids: "to first calculate CCS bias between measured CCS values and library values of U¹³C labeled lipids"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
