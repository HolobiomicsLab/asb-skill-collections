---
name: reference-library-alignment
description: Use when when you have IM-MS lipidomics data with measured CCS values from samples spiked with U13C labeled internal standards, and you need to assess systematic CCS bias or enable CCS correction by comparing measured lipids against known library entries with validated CCS values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3957
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MobiLipid
  - R (ggplot2, data.table, DT packages)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reference-library-alignment

## Summary

Align detected ion mobility-mass spectrometry lipid features to a curated reference library (DT CCS N2) by matching mass-to-charge and retention time identifiers, enabling quantitative bias assessment and correction of collision cross section (CCS) values against theoretical reference standards.

## When to use

When you have IM-MS lipidomics data with measured CCS values from samples spiked with U13C labeled internal standards, and you need to assess systematic CCS bias or enable CCS correction by comparing measured lipids against known library entries with validated CCS values.

## When NOT to use

- Your samples were not spiked with U13C labeled internal standards—the alignment requires heavy-labeled lipids as anchors for bias calculation.
- Your measured data uses lipid nomenclature or adduct notation not present in the DT CCS N2 library—alignment will fail or produce incomplete matches.
- You lack a validated CCS reference library with coverage of your analyte lipid classes and adducts—bias assessment becomes unreliable without trusted ground truth.

## Inputs

- Measured IM-MS lipidomics data table (.csv) with columns: File, LipidClass, LipidSpecies, Adduct, Label (light/heavy), CCS
- DT CCS N2 reference library for U13C labeled lipids (.csv) with library CCS values

## Outputs

- Matched lipid features with experimental CCS values aligned to library entries
- CCS bias table (% bias or absolute difference per lipid feature)
- Aggregated bias statistics by lipid class and adduct combination (mean, SD, range)
- Visualization of CCS bias distribution by lipid class

## How to apply

Load both your measured IM-MS lipid feature table (containing m/z, retention time, CCS, lipid class, lipid species, adduct, and labeling status) and the DT CCS N2 library for U13C labeled lipids into R. Match detected lipid features to library entries by aligning on lipid class, lipid species, and adduct type—ensuring nomenclature consistency between your data and the library. For each successfully matched feature, calculate the experimental-to-theoretical CCS bias as the absolute or percent difference between measured CCS and library CCS values. Aggregate bias metrics by lipid class and adduct combination, computing mean bias and standard deviation. This alignment enables subsequent linear regression-based CCS correction functions (requiring minimum 3 lipids per lipid class–adduct combination) and provides bias distribution visualizations for quality control assessment.

## Related tools

- **MobiLipid** (Automated R Markdown workflow that implements reference library alignment, CCS bias calculation, and optional CCS correction via linear regression for IM-MS lipidomics) — https://github.com/FelinaHildebrand/MobiLipid
- **R (ggplot2, data.table, DT packages)** (Core environment for data loading, matching, bias calculation, aggregation, and visualization)

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_CCS-bias-calculation_results.html', 'MobiLipid_CCS-bias-calculation_results.pdf'))
```

## Evaluation signals

- All detected U13C labeled lipids in your input are successfully matched to library entries (100% or near-100% matching rate for heavy-labeled features in covered lipid classes).
- CCS bias values fall within expected ranges (typically ±5–10% for well-calibrated instruments); extreme outliers suggest mismatches or data quality issues.
- Aggregated bias statistics (mean, SD) are computed for each lipid class–adduct combination with ≥3 matched features; combinations with <3 features are flagged or excluded.
- Generated bias visualization shows systematic deviation patterns (e.g., consistent positive or negative bias by class) consistent with instrument calibration state.
- Output .csv files (e.g., CCS_bias_no_correction) contain matched lipid identifiers, measured CCS, library CCS, and calculated bias—all values traceable to input rows.

## Limitations

- CCS bias calculation depends critically on nomenclature consistency between input data and the DT CCS N2 library; mismatches (e.g., alternate lipid class abbreviations) will reduce alignment completeness.
- Lipid class–adduct combinations with fewer than 3 matched features cannot support linear regression-based CCS correction, limiting correction applicability to PC, PE, PI, PS, PA, Cer, HexCer, DG, TG, and LPC with adequate internal standard coverage.
- The DT CCS N2 library is specific to U13C labeled yeast lipids; alignment and bias assessment are not validated for other isotope labeling schemes or synthetic standard sets.
- Bias calculation assumes accurate m/z and retention time alignment; co-eluting isomers or isobaric lipids may create spurious matches or aggregation artifacts if not resolved upstream.

## Evidence

- [other] Map detected lipid features to the DTCCSN2 reference library by matching mass-to-charge and retention time identifiers.: "Map detected lipid features to the DTCCSN2 reference library by matching mass-to-charge and retention time identifiers."
- [other] Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values.: "Calculate experimental-to-theoretical CCS bias for each matched lipid as the difference between measured and reference CCS values."
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards: "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract)"
- [readme] The .csv file has to have the following headers: 'File', 'LipidClass', 'LipidSpecies', 'Adduct', 'Label', 'CCS': "The .csv file has to have the following headers: "File", "LipidClass", "LipidSpecies", "Adduct", "Label", "CCS""
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
