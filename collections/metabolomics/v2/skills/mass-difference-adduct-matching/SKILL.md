---
name: mass-difference-adduct-matching
description: Use when after correlation-based feature pairing has identified feature
  groups with matching temporal intensity profiles through direct-injection or plasma
  ionization mass spectrometry experiments. You have a set of putative feature-pair
  candidates and need to assign specific chemical identities (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - mass-spectrometry
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

# Reconstruct the mass-difference open-search step to assign candidate adduct/fragment species

## Summary

This skill uses exact mass differences between correlated feature pairs to refine and disambiguate ion-species relationships in direct-injection mass spectrometry by matching observed m/z deltas against a user-defined reference table of in-source fragments and adducts. It serves as a second refinement layer after temporal correlation, annotating feature pairs with specific adduct or fragment identities and reporting mass accuracy.

## When to use

Apply this skill after correlation-based feature pairing has identified feature groups with matching temporal intensity profiles through direct-injection or plasma ionization mass spectrometry experiments. You have a set of putative feature-pair candidates and need to assign specific chemical identities (e.g., [M-H₂O+H]⁺, [M+nO+H]⁺) to each pair by comparing the observed m/z difference to reference adduct/fragment masses.

## When NOT to use

- Input already contains manual or database-curated adduct identities and no refinement is needed.
- Feature pairs lack significant temporal correlation (correlation coefficient below user threshold, e.g., < 0.9); mass-difference matching alone cannot establish chemical relationships without temporal evidence.
- Mass spectrometer resolution and mass calibration are poor (mass error >> user-specified ppm tolerance); exact mass differences cannot be reliably resolved.

## Inputs

- Feature-pair table from temporal correlation (columns: base_mz, base_index, match_mz, match_index, correlation coefficient)
- User-defined adduct/fragment reference DataFrame (columns: deltamz, motive/ion_formula)
- ppm tolerance parameter (float, typically 2–5 ppm depending on MS resolution)
- Extracted ion chromatogram (XIC) intensities or feature table (for optional validation)

## Outputs

- Refined candidate table with columns: base_mz, base_index, match_mz, match_index, observed_mzdiff, matched_adduct/fragment_label, mass_accuracy_ppm, correlation_coefficient
- Dictionary or nested structure indexed by adduct type, each entry containing annotated feature pairs

## How to apply

Load the correlation-identified feature pairs (output from temporal correlation step) alongside a user-supplied adduct/fragment mass-difference reference table. For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference list using exact mass matching within a user-specified ppm tolerance (e.g., 2 ppm for high-resolution instrumentation). Assign adduct or fragment labels to feature pairs where a match is found, recording the mass accuracy (observed − expected mass difference). Output a refined candidate table that lists feature pairs, observed mass differences, matched adduct/fragment annotations, and mass accuracy metrics. The rationale is that chemical adducts and in-source fragments have precise, predictable mass signatures; matching these signatures confirms the ion-species relationship and reduces false-positive correlations.

## Related tools

- **DBDIpy** (Primary library implementing the mass-difference refinement step via identify_adducts() function; handles mass matching, adduct lookup, and result annotation for DBDI-MS and plasma ionization datasets.) — https://github.com/leopold-weidner/DBDIpy
- **matchms** (Supporting library integrated into DBDIpy for spectral import/export and alignment; provides the ecosystem for preprocessing and comparing mass spectrometric data.)
- **Python** (Runtime environment for executing DBDIpy and performing DataFrame operations (pandas) for mass-difference calculation and matching.)

## Examples

```
adduct_rule = pd.DataFrame({'deltamz': [47.984744], 'motive': ['O3']}); search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- Mass accuracy of matched adduct/fragment pairs should be ≤ user-specified ppm tolerance (e.g., observed − expected Δm/z < 2 ppm for high-resolution FT-ICR-MS).
- Annotated feature pairs should show chemical plausibility: e.g., [M+O+H]⁺ pairs should have match_mz > base_mz by ~15.995 Da; [M-H₂O+H]⁺ pairs should have match_mz < base_mz by ~18.011 Da.
- Correlation coefficients of matched pairs should remain ≥ threshold used in prior temporal-correlation step (e.g., ≥ 0.9 for Pearson correlation); mass matching should not include low-correlation false positives.
- Output table should contain no duplicate feature-pair–adduct assignments (each pair matched to at most one adduct type, or multiple only if genuinely ambiguous within tolerance).
- Comparison of matched adduct counts across adduct types should align with known ionization chemistry: e.g., oxygen-addition adducts ([M+O+H]⁺, [M+2O+H]⁺) more prevalent in DBDI than in ESI, consistent with plasma oxidation.

## Limitations

- Mass-difference matching is ambiguous when multiple adducts or fragments have similar Δm/z values (e.g., [M+NH₄]⁺ vs. [M+H₂O+H]⁺); user must choose appropriate ppm tolerance and reference-table specificity to resolve.
- Skill assumes temporal correlation has already identified genuine feature pairs; poor correlation thresholds in the prior step will propagate false-positive pairs into mass-difference matching.
- User must define the reference adduct/fragment table; omitted or misspecified adduct masses will result in unmatched feature pairs, reducing coverage. Custom adducts must be user-supplied; the method does not enumerate novel or unexpected in-source modifications.
- Mass calibration errors and resolution limitations of the MS instrument directly limit achievable ppm accuracy; instruments with poor mass calibration (> 5–10 ppm drift) may yield unreliable matches even with relaxed tolerance settings.

## Evidence

- [other] DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+) to refine the nature of potential ion-species candidates identified by temporal correlation.: "DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+)"
- [other] For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified ppm tolerance).: "calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified"
- [readme] Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
- [readme] DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H<sub>2</sub>O+H]<sup>+</sup>) and in-source generated adducts (eg. [M+nO+H]<sup>+</sup>).: "DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H2O+H]+) and in-source generated adducts (eg. [M+nO+H]+)"
- [readme] (exact) mass differences are used to refine the nature of potential candidates: "(exact) mass differences are used to refine the nature of potential candidates"
- [readme] search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule, method = "pearson", threshold = 0.9, mass_error = 2): "identify_adducts(df = specs_imputed, masses = feature_mz, custom_adducts = adduct_rule, method = "pearson", threshold = 0.9, mass_error = 2)"
