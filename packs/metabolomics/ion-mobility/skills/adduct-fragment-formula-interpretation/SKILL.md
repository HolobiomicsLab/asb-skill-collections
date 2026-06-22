---
name: adduct-fragment-formula-interpretation
description: Use when after temporal correlation has identified candidate feature pairs with matching intensity profiles across time-resolved DBDI-MS experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric barrier discharge ionisation mass spectrometric datasets
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

This skill uses exact mass differences between correlated ion features to disambiguate and annotate in-source adducts and fragments (e.g., [M-H₂O+H]⁺, [M+nO+H]⁺) in direct-injection plasma mass spectrometry data. It refines temporal-correlation-identified candidate pairs by matching observed m/z deltas against a user-defined reference table within a specified mass accuracy tolerance.

## When to use

Apply this skill after temporal correlation has identified candidate feature pairs with matching intensity profiles across time-resolved DBDI-MS experiments. Use it when you need to discriminate between multiple possible adduct/fragment interpretations for the same analyte—particularly when chromatographic separation is absent and in-source ionization produces multiple ion species per compound.

## When NOT to use

- Data already include chromatographic retention time information—use orthogonal chromatographic dimension instead of temporal ionization correlation.
- Input feature table contains missing values (NaN)—impute intensities first to ensure uniform XIC length for mass difference calculation.
- No reference adduct/fragment table is available or cannot be defined for the ionization method—open-search mode may be used, but this skill requires a priori defined mass-difference motives.

## Inputs

- Feature correlation table (output from pointwise correlation step with base_mz, match_mz, correlation coefficients)
- Mean m/z values for all features
- User-defined adduct/fragment reference table (DataFrame with deltamz and motive columns)
- Mass spectrometric data parameters (ppm_window matching instrument resolution)

## Outputs

- Dictionary of refined candidate tables, one DataFrame per adduct type
- Each DataFrame contains: base_mz, base_index, match_mz, match_index, mzdiff, correlation coefficient, and adduct/fragment label

## How to apply

Load the correlation-identified feature pairs (output from the temporal correlation step) and a user-supplied reference table listing expected mass-difference motives (e.g., [M-H₂O+H]⁺ → Δm/z = 18.01057 Da) with their symbolic labels. For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Compare this observed difference against all entries in the reference table using exact mass matching within the user-specified ppm tolerance (e.g., 2 ppm for high-resolution FT-ICR-MS). Assign adduct or fragment labels to pairs where a match is found. Record the mass accuracy (observed − theoretical) for each match. Output a refined candidate table listing feature pairs, observed mass differences, matched adduct/fragment annotations, and mass accuracy metrics for downstream validation.

## Related tools

- **DBDIpy** (Python library implementing the mass-difference matching and adduct/fragment annotation workflow via the identify_adducts() function) — github.com/leopold-weidner/DBDIpy
- **matchms** (Ecosystem library integrated with DBDIpy for spectral data import, preprocessing, and MS2 spectral similarity scoring in subsequent refinement steps)

## Examples

```
search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- All matched mass differences fall within the user-specified ppm tolerance; mass accuracy (observed − theoretical) is reported for each match.
- Feature pairs matched to adducts/fragments exhibit high correlation coefficients (default threshold ≥ 0.9 Pearson correlation) indicating co-elution during ionization.
- Matched adduct/fragment labels conform to known chemical rules (e.g., [M+nO+H]⁺ only pairs features with positive charge and oxygen additions; [M-H₂O+H]⁺ only pairs features with losses).
- Output table contains no ambiguous matches (each feature pair assigned to ≤1 adduct/fragment motive); if ambiguity exists, report mass accuracy for tie-breaking.
- Cross-validation with MS2 spectral similarity or external reference standards shows that annotated adduct pairs correlate with known or predicted fragmentation patterns.

## Limitations

- Accuracy depends on the completeness and correctness of the user-supplied adduct/fragment reference table; missing or misspecified mass differences will result in false negatives.
- High-mass spectral noise or incomplete imputation can artificially inflate correlations, leading to spurious feature pairings before mass-difference filtering; noise reduction in preprocessing is critical.
- Mass accuracy tolerance (ppm_window) must be set appropriately for the instrument resolution; too-wide windows increase false-positive matches, too-narrow windows miss legitimate adducts.
- The skill does not distinguish between multiple ionization pathways producing the same theoretical mass difference (e.g., [M+H]⁺ vs. [M+NH₄]⁺ both produce m/z shifts that may overlap); MS2 spectral similarity or complementary ion-mobility data is needed for disambiguation.

## Evidence

- [other] exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+): "DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+)"
- [other] For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). 3. Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified ppm tolerance).: "For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). 3. Match the observed mass difference against the reference adduct/fragment list using exact mass"
- [readme] DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H<sub>2</sub>O+H]<sup>+</sup>) and in-source generated adducts (eg. [M+nO+H]<sup>+</sup>): "DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H<sub>2</sub>O+H]<sup>+</sup>) and in-source generated adducts (eg. [M+nO+H]<sup>+</sup>)"
- [readme] calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. (exact) mass differences are used to refine the nature of potential candidates.: "calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. (exact) mass differences are used to refine the nature of potential"
- [readme] Missing values in our feature table will be imputed by a two-stage imputation algorithm. First, missing values within the detected signal region are interpolated in between. Second, a noisy baseline is generated for all XIC to be of uniform length: "Missing values in our feature table will be imputed by a two-stage imputation algorithm. First, missing values within the detected signal region are interpolated in between."
