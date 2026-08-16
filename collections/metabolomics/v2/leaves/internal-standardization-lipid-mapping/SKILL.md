---
name: internal-standardization-lipid-mapping
description: Use when you have (LC-)IM-MS lipidomics data from samples spiked with
  U13C-labeled yeast extract, measured CCS values for both labeled and unlabeled lipids,
  and need to quantify systematic CCS bias between your instrument and a reference
  library before applying bias correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0153
  tools:
  - R
  - MobiLipid R Markdown (MobiLipid_CCS-bias-calculation.Rmd)
  - ggplot2
  - data.table
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates
  into IM-MS lipidomics workflows
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

# internal-standardization-lipid-mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Map measured ion mobility-mass spectrometry lipid signals to a deuterated CCS library using U13C-labeled internal standards to establish bias correction factors for each lipid class–adduct combination. This skill enables quality control and systematic bias quantification without requiring external calibration beyond vendor-specific requirements.

## When to use

You have (LC-)IM-MS lipidomics data from samples spiked with U13C-labeled yeast extract, measured CCS values for both labeled and unlabeled lipids, and need to quantify systematic CCS bias between your instrument and a reference library before applying bias correction.

## When NOT to use

- Samples lack U13C-labeled internal standards or yeast extract spike-in — the skill fundamentally depends on labeled lipids to establish library mapping.
- Reference library nomenclature does not match your measured lipid naming convention — lipid class and species must align with DT CCS N2 library entries.
- Input CCS values are already corrected or transformed — the skill assumes raw, uncorrected measured CCS as input.

## Inputs

- Measured data table (.csv) with columns: File, LipidClass, LipidSpecies, Adduct (one of: [M+H], [M+NH4], [M+Na], [M-H], [M+HCOO]), Label (light or heavy), CCS
- DT CCS N2 reference library for U13C labeled lipids (.csv)
- Sample preparation metadata indicating U13C labeling status

## Outputs

- CCS bias calculation table (.csv) with measured CCS, library CCS, bias (%), and bias statistics per lipid class–adduct combination
- Bias assessment results organized by lipid class, species, and adduct
- Summary statistics (mean bias, standard deviation) per lipid class–adduct combination
- .RData file containing all bias metrics as R list object

## How to apply

Load your measured data (in .csv format with columns: File, LipidClass, LipidSpecies, Adduct, Label, CCS) and the provided DT CCS N2 library for U13C labeled lipids. Match measured lipid signals to library entries by lipid class, species nomenclature, and adduct type. Calculate CCS bias as the difference between measured CCS values and library values for U13C-labeled lipids within each lipid class–adduct combination. Organize results by lipid class and adduct to prepare for downstream linear regression-based correction (requires minimum 3 lipids per class–adduct combination for correction functions). This internal standardization approach avoids the need for additional external calibration measurements beyond vendor-specific instrument calibration.

## Related tools

- **R** (Runtime and implementation language for MobiLipid R Markdown workflow that automates lipid mapping and bias calculation)
- **MobiLipid R Markdown (MobiLipid_CCS-bias-calculation.Rmd)** (Automated workflow that loads measured data, maps to U13C library, calculates CCS bias, and generates HTML/PDF reports with bias tables and visualizations) — https://github.com/FelinaHildebrand/MobiLipid
- **ggplot2** (Visualization of CCS bias distributions and bias statistics across lipid class–adduct combinations)
- **data.table** (Efficient manipulation and aggregation of large measured lipid datasets and library matching)

## Examples

```
# In R Studio console:
rmarkdown::render("MobiLipid_CCS-bias-calculation.Rmd", output_format = c("html_document", "pdf_document"), output_file = c("MobiLipid_CCS-bias-calculation_results.html", "MobiLipid_CCS-bias-calculation_results.pdf"))
```

## Evaluation signals

- All measured U13C-labeled lipids successfully match to corresponding DT CCS N2 library entries by lipid class, species, and adduct type with no unmapped signals.
- Bias calculation produces numeric bias percentages for each matched lipid; check for data type consistency and absence of NaN or missing values in bias columns.
- Each lipid class–adduct combination with ≥3 U13C-labeled lipids shows bias statistics (mean, SD, min, max); combinations with <3 lipids are flagged as unable to support later correction functions.
- Bias values fall within expected ranges for IM-MS (typically ±5–10% before correction); outliers should be investigated for data quality or nomenclature mismatches.
- Output .csv files match input row counts for measured lipids; join operations with library preserve data integrity and traceability (e.g., original CCS, library CCS, and calculated bias all present).

## Limitations

- Requires U13C labeled lipid internal standards (fully labeled yeast extract) spiked into samples — not applicable to samples without this preparation step.
- Linear regression-based correction functions require a minimum of 3 lipids per lipid class–adduct combination; this restricts correction to classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG. Other classes (AcCa, Co, LPE, PG, SPH) can be assessed for bias but not corrected.
- Nomenclature must exactly match the DT CCS N2 library; inconsistencies in lipid class or species names will cause mapping failures and exclusion from bias calculation.
- Bias calculation is instrument-specific and reflects only the systematic offset between your measured CCS and the reference library; bias factors are not transferable between different IM-MS instruments or ion sources without validation.

## Evidence

- [other] MobiLipid employs an R Markdown integrated into IM-MS lipidomics workflows that automates CCS bias correction, utilizing a DT CCS N2 library for U13C labeled lipids as internal standards to adjust CCS measurements without requiring additional external calibration.: "employs an R Markdown integrated into IM-MS lipidomics workflows that automates CCS bias correction, utilizing a DT CCS N2 library for U13C labeled lipids as internal standards"
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract). Subsequently, it is possible to utilize the DT CCS N2 library for U13C labeled lipids to first calculate CCS bias between measured CCS values and library values of U13C labeled lipids.: "samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract) ... to calculate CCS bias between measured CCS values and library values"
- [readme] This needs to be a .csv file containing the measured data. The .csv file has to have the following headers: 'File', 'LipidClass', 'LipidSpecies', 'Adduct', 'Label', 'CCS': ".csv file has to have the following headers: 'File', 'LipidClass', 'LipidSpecies', 'Adduct', 'Label', 'CCS'"
- [intro] Internal standardization using U13C labeled lipids eliminates the need for additional external calibration beyond vendor-specific requirements: "Internal standardization using U13C labeled lipids eliminates the need for additional external calibration beyond vendor-specific requirements"
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, and TG.: "linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination which restricts the CCS correction to the following lipid classes: Cer, DG, HexCer, LPC, PA,"
