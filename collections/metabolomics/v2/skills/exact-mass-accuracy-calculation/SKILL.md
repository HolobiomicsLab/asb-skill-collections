---
name: exact-mass-accuracy-calculation
description: Use when you have feature pairs identified by temporal correlation in
  direct-injection MS data and need to confirm their relationship is consistent with
  known adduct/fragment mass shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DBDIpy
  - Python
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# Exact Mass Accuracy Calculation

## Summary

Calculate and evaluate mass accuracy of observed m/z differences against reference adduct and fragment masses to refine ion-species candidate assignments in direct-injection mass spectrometry. This refinement step disambiguates correlations by matching measured mass differences to expected adduct/fragment patterns within user-specified ppm tolerance.

## When to use

You have feature pairs identified by temporal correlation in direct-injection MS data and need to confirm their relationship is consistent with known adduct/fragment mass shifts. Apply this skill when you possess an observed m/z difference between two features and a reference table of expected adduct or in-source fragment mass deltas (e.g., [M-H₂O+H]⁺, [M+nO+H]⁺), and want to assign biochemical meaning and validate mass accuracy before accepting the correlation.

## When NOT to use

- Input features are already separated by liquid chromatography (retention time dimension removes ambiguity about fragment/adduct identity).
- You do not have a curated reference table of expected adduct/fragment masses for your analyte class and ionization method.
- Feature m/z values have low mass accuracy (>>5 ppm error) or low mass resolution (>0.1 Da at m/z 200), making exact mass matching unreliable.

## Inputs

- Correlation-identified feature pairs (m/z_A, m/z_B, correlation coefficient)
- User-supplied adduct/fragment reference table with mass differences (Δm/z, adduct label)
- Mass spectrometric feature table (m/z values with intensity profiles)

## Outputs

- Refined candidate table with feature pairs, observed mass differences, matched adduct/fragment labels, and mass accuracy metrics
- Mass accuracy report (observed vs. theoretical mass differences)
- Unassigned or ambiguous feature pairs (failed to match reference list within tolerance)

## How to apply

Load correlation-identified feature pairs (from the temporal correlation step) and a user-defined reference table listing adduct/fragment types with their exact mass differences. For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match this observed difference against the reference adduct/fragment list using exact mass matching, allowing for a user-specified ppm tolerance window (typical values are 2–5 ppm depending on instrument resolution). When a match is found, assign the adduct or fragment label to that feature pair and record the mass accuracy (difference between observed and theoretical mass shift). Features failing to match any reference adduct/fragment within tolerance are flagged as unassigned or ambiguous. Output a refined candidate table listing feature pairs, observed mass differences, matched adduct/fragment annotations, and calculated mass accuracy metrics.

## Related tools

- **DBDIpy** (Implements the second refinement step via identify_adducts() function; handles exact mass difference matching against user-definable adduct/fragment reference tables and reports mass accuracy) — https://github.com/leopold-weidner/DBDIpy
- **Python** (Programming language for implementing mass difference calculations, ppm tolerance filtering, and reference table matching logic)

## Examples

```
search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- All matched feature pairs have observed mass differences within the specified ppm tolerance of theoretical values (e.g., ±2 ppm).
- Mass accuracy values reported for each match are consistent with the mass resolution of the instrument used (e.g., <5 ppm for high-resolution FT-ICR-MS).
- Number and distribution of assigned adducts/fragments are chemically plausible for the ionization method (e.g., [M+O+H]⁺ and [M+2O+H]⁺ are common for plasma ionization).
- Feature pairs assigned to the same adduct type show similar mass accuracy distributions, suggesting systematic calibration quality.
- Unassigned feature pairs are examined for potential false correlations (high correlation but no biochemical basis in the adduct/fragment reference).

## Limitations

- Mass accuracy matching is sensitive to instrument calibration; poor calibration (>5 ppm systematic error) can cause valid adducts to be rejected or false matches to be accepted.
- Reference table completeness is critical; if expected adducts/fragments for a given ionization method are not listed, valid feature relationships will be missed.
- The method does not distinguish isomers or constitutional isomers; multiple adduct types may have overlapping or identical mass differences, requiring MS/MS or additional orthogonal data.
- Performance depends on user-selected ppm tolerance; excessively loose tolerance (>10 ppm) risks false positives; excessively tight tolerance (<1 ppm) risks false negatives on lower-resolution instruments.

## Evidence

- [other] For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). 3. Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified ppm tolerance).: "For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching"
- [other] DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+) to refine the nature of potential ion-species candidates identified by temporal correlation.: "DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+)"
- [other] Assign adduct or fragment labels to feature pairs where a match is found, and record the mass accuracy.: "Assign adduct or fragment labels to feature pairs where a match is found, and record the mass accuracy."
- [other] Output a refined candidate table listing feature pairs, observed mass differences, matched adduct/fragment annotations, and mass accuracy metrics.: "Output a refined candidate table listing feature pairs, observed mass differences, matched adduct/fragment annotations, and mass accuracy metrics."
- [readme] By default, identify_adducts() searches for [M-H<sub>2</sub>O+H]<sup>+</sup>, [M+1O+H]<sup>+</sup> and [M+2O+H]<sup>+</sup>. For demonstrational purposes we also want to search for [M+3O+H]<sup>+</sup> in this example.: "By default, identify_adducts() searches for [M-H₂O+H]⁺, [M+1O+H]⁺ and [M+2O+H]⁺"
- [readme] (exact) mass differences are used to refine the nature of potential candidates.: "(exact) mass differences are used to refine the nature of potential candidates."
