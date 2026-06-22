---
name: u13c-labeled-standard-reference-matching
description: Use when you have IM-MS measurements of samples spiked with U13C-labeled internal standards (e.g., fully labeled yeast extract) and need to assess whether measured CCS values systematically deviate from their true reference values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - R
  - MobiLipid
  - DTCCS_N2 library for U13C labeled lipids
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# u13c-labeled-standard-reference-matching

## Summary

Match measured collision cross section (CCS) values from isotope-labeled lipid internal standards to a reference DTCCS_N2 library to quantify per-lipid-class bias, enabling systematic CCS correction in IM-MS lipidomics without external calibration.

## When to use

Apply this skill when you have IM-MS measurements of samples spiked with U13C-labeled internal standards (e.g., fully labeled yeast extract) and need to assess whether measured CCS values systematically deviate from their true reference values. Use it before correcting CCS measurements across an entire dataset when you want to avoid the cost and complexity of additional external calibration beyond vendor-specific requirements.

## When NOT to use

- Your samples lack U13C-labeled internal standards or contain fewer than 3 lipids per lipid class–adduct combination, since bias estimation requires sufficient labeled lipid coverage.
- Your measured lipid nomenclature or adduct notation does not match the DTCCS_N2 library scheme, and you have no way to harmonize them.
- You are working with lipid classes not present in the DTCCS_N2 library (e.g., novel or rare lipid classes with no U13C reference data).

## Inputs

- Measured IM-MS CCS values (CSV with headers: File, LipidClass, LipidSpecies, Adduct, Label, CCS)
- DTCCS_N2 reference library for U13C-labeled lipids (CSV)
- Sample metadata indicating which measurements correspond to U13C-labeled internal standards

## Outputs

- CCS bias table (%) per lipid, lipid class, and adduct
- Mean and median CCS bias per lipid class
- Diagnostic plots: bias distribution before correction (box plots, violin plots, or histograms by lipid class)
- List of matched lipid identities (measured vs. library) used for bias calculation
- Bias summary statistics (e.g., mean bias, standard deviation, range per class)

## How to apply

Load measured IM-MS CCS values and the DTCCS_N2 reference library for U13C-labeled lipids into R. Stratify measured CCS by lipid class and adduct type (e.g., PC [M+H], PE [M-H]). For each lipid class–adduct combination, identify detected U13C-labeled lipids that exist in both the measured data and the reference library. Calculate bias as the percent deviation of observed CCS from DTCCS_N2 reference values for each matched lipid. Compute mean and distribution statistics of bias per lipid class. Output include bias tables, diagnostic plots showing bias distribution before correction, and lists of matched lipid identities to verify the matching succeeded.

## Related tools

- **MobiLipid** (R Markdown tool that automates CCS bias calculation by internally matching U13C-labeled lipid CCS values to the DTCCS_N2 library and generates diagnostic reports) — https://github.com/FelinaHildebrand/MobiLipid
- **R** (Statistical programming environment used to load data, stratify by lipid class, compute bias metrics, and generate plots)
- **DTCCS_N2 library for U13C labeled lipids** (Reference dataset of theoretical CCS values for U13C-labeled lipids; provided with MobiLipid code) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
rmarkdown::render('MobiLipid_CCS-bias-calculation.Rmd', output_format = c('html_document', 'pdf_document'), output_file = c('MobiLipid_measured_data.html', 'MobiLipid_measured_data.pdf'))
```

## Evaluation signals

- All U13C-labeled lipids detected in the measured data are successfully matched to entries in the DTCCS_N2 library by lipid species and adduct.
- Bias values are computed as percent deviation and fall within expected ranges (typically ±5–10% for well-calibrated instruments); extreme outliers should be flagged.
- Per-lipid-class bias distribution shows coherent patterns (e.g., one class may show consistent positive bias while another shows negative bias), not random scatter.
- At least 3 lipids per lipid class–adduct combination are matched; if fewer, the skill should not proceed to correction.
- Diagnostic plots visually confirm that bias distributions are reduced or eliminated after correction (if using the correction step downstream).

## Limitations

- Requires a minimum of 3 U13C-labeled lipids detected per lipid class–adduct combination for valid bias estimation and subsequent correction; low detection of labeled standards reduces reliability.
- The DTCCS_N2 library is specific to U13C-labeled yeast lipid extract; bias values may not generalize to other labeled lipid sources or non-biological matrices.
- Bias calculation depends on exact nomenclature matches between measured lipid species names and the library; mismatches prevent pairing and bias calculation.
- Internal standardization via U13C labeling assumes that labeled and unlabeled lipids co-elute and behave similarly in IM-MS; violations can introduce systematic errors in bias estimation.
- Linear regression-based correction (downstream step) assumes the bias is linear across the CCS range; non-linear drift is not captured.

## Evidence

- [other] For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each class).: "For each lipid class, compute the bias as the deviation of observed CCS from reference DTCCS_N2 values using internal standardization (leveraging U13C labeled lipid standards detected within each"
- [readme] Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code, MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization.: "Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code, MobiLipid eliminates the need to measure additional external calibration besides"
- [readme] For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract (Neubauer et al. 2012)).: "For utilizing the MobiLipid workflow samples measured with (LC-)IM-MS have to be spiked with U13C labeled internal standards (fully labeled yeast extract (Neubauer et al. 2012))."
- [readme] To monitor the result of CCS correction, the bias between corrected CCS values and DTCCS_N2 library values of U13C labeled lipids is calculated.: "To monitor the result of CCS correction, the bias between corrected CCS values and DTCCS_N2 library values of U13C labeled lipids is calculated."
- [readme] CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination: "CCS correction functions are based on linear regression functions which require a minimum of 3 lipids within a lipid class-adduct combination"
