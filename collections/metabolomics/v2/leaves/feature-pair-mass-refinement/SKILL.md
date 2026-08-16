---
name: feature-pair-mass-refinement
description: Use when after temporal correlation has identified feature pairs with
  matching intensity profiles across direct-injection MS experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric
  barrier discharge ionisation mass spectrometric datasets
- DBDIpy is an open-source Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbdipy_cq
    doi: 10.1093/bioinformatics/btad088/7036334
    title: DBDIpy
  dedup_kept_from: coll_dbdipy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad088/7036334
  all_source_dois:
  - 10.1093/bioinformatics/btad088/7036334
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the mass-difference open-search step to assign candidate adduct/fragment species

## Summary

A refinement step that uses exact mass differences to disambiguate ion-species relationships identified through temporal correlation in direct-injection mass spectrometry. It matches observed m/z differences against a user-defined reference table of in-source fragments and adducts to assign chemical labels and assess mass accuracy.

## When to use

Apply this skill after temporal correlation has identified feature pairs with matching intensity profiles across direct-injection MS experiments. Use it when you have a list of candidate ion-species pairs (from correlation step) and need to determine whether each pair represents a known adduct or in-source fragment relationship rather than unrelated species.

## When NOT to use

- Input feature pairs have not yet been temporally correlated or do not have high correlation coefficients (threshold typically ≥ 0.9); use correlation step first.
- No reference table of in-source fragments and adducts is available or defined for your ionization method and analyte class.
- Mass spectrometry data lacks sufficient resolution to distinguish exact mass differences within the specified ppm tolerance; use coarser mass-window matching instead.

## Inputs

- Feature pair table (output from correlation step, containing base_mz, match_mz, correlation coefficient)
- User-defined adduct/fragment reference DataFrame with columns: deltamz (exact mass difference), motive (chemical annotation, e.g. 'O', 'O2', 'H2O', 'O3')
- Mass spectrometry resolution parameter (ppm_window or mass_error tolerance)

## Outputs

- Refined candidate table with columns: base_mz, base_index, match_mz, match_index, observed_mzdiff, matched_adduct_label, mass_accuracy_ppm
- Dictionary of DataFrames (one per adduct/fragment type) containing validated feature pair assignments

## How to apply

Load the correlation-identified feature pairs and a user-supplied adduct/fragment reference table containing exact mass differences (e.g., [M-H2O+H]+ = 18.01057, [M+nO+H]+ = 15.99491 for each n). For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference list using exact mass matching within a user-specified ppm tolerance (typically 2 ppm for high-resolution FT-ICR-MS). Assign adduct or fragment labels only to feature pairs where the observed mass difference falls within tolerance of a reference entry. Record mass accuracy for each match. Filter out feature pairs with no valid reference match.

## Related tools

- **DBDIpy** (Open-source Python library implementing the mass-difference refinement step via identify_adducts() function with exact mass matching and custom_adducts parameter) — https://github.com/leopold-weidner/DBDIpy
- **Python** (Core language for DataFrame manipulation and exact mass difference calculations)
- **matchms** (Ecosystem library integrated with DBDIpy for spectral import/export and preprocessing)

## Examples

```
adduct_rule = pd.DataFrame({'deltamz': [47.984744], 'motive': ['O3']})
search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- All matched feature pairs have observed mass differences within user-specified ppm tolerance of at least one reference adduct/fragment entry
- Mass accuracy (calculated as abs(observed_mzdiff − reference_deltamz) / reference_deltamz * 1e6) is consistently <5 ppm for high-resolution instruments
- No feature pairs are assigned multiple conflicting adduct labels; each pair maps to at most one reference entry
- Refined table contains only feature pairs where correlation coefficient (from prior step) exceeds threshold (typically 0.9) AND mass difference matches reference list
- Output dictionary structure matches input adduct/fragment categories; each key corresponds to a 'motive' from the reference table

## Limitations

- Requires a priori definition of expected adduct and fragment species; cannot discover truly novel mass losses or gains not in the reference table
- Exact mass matching is sensitive to instrument calibration drift; systematic mass errors >specified ppm tolerance will cause valid assignments to be rejected
- High-abundance background ions or isobaric species may create spurious feature pairs with matching temporal profiles but non-biological mass differences
- The DBDIpy implementation (v2.0) is still under development; advanced plotting and runtime optimization are listed as ongoing work

## Evidence

- [other] exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+): "DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+)"
- [other] For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified ppm tolerance).: "For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). 3. Match the observed mass difference against the reference adduct/fragment list using exact mass"
- [readme] mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
- [readme] calculation of pointwise correlation identifies features with matching temporal intensity profiles; (exact) mass differences are used to refine the nature of potential candidates: "calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. - (exact) mass differences are used to refine the nature of potential"
- [readme] search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule, method = 'pearson', threshold = 0.9, mass_error = 2): "identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule, method = "pearson", threshold = 0.9, mass_error = 2)"
