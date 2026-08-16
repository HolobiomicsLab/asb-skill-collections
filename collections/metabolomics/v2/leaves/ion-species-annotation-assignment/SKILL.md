---
name: ion-species-annotation-assignment
description: Use when after temporal correlation has identified feature pairs with
  matching intensity profiles across time-resolved MS scans, but before final candidate
  validation. Apply this skill when you need to distinguish between competing ion-species
  hypotheses (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - LC-MS
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

A refinement step that uses exact mass differences to disambiguate and annotate ion-species relationships identified through temporal correlation in direct-injection mass spectrometry. This skill applies precise mass matching against a reference library of known in-source fragments and adducts to assign chemical identities to feature pairs and quantify mass accuracy.

## When to use

After temporal correlation has identified feature pairs with matching intensity profiles across time-resolved MS scans, but before final candidate validation. Apply this skill when you need to distinguish between competing ion-species hypotheses (e.g., [M+O+H]+ vs. [M+H2O+H]+) and assign chemical structure labels to correlated feature pairs in datasets lacking chromatographic separation (e.g., direct-injection DBDI-MS or plasma ionization time-series).

## When NOT to use

- Input is already a chromatographically separated dataset (LC-MS/MS); temporal correlation is unnecessary and mass difference refinement may not improve specificity.
- Feature pairs have been identified by methods other than temporal correlation (e.g., isotope pattern matching or spectral similarity alone); this skill is designed specifically to refine correlation-based candidates.
- User-supplied adduct/fragment reference table is unavailable or incomplete; the skill cannot function without domain-specific modification definitions.

## Inputs

- Feature pair table (m/z values and indices from temporal correlation step)
- User-definable adduct/fragment reference table (mass-difference library with theoretical Δm/z values and chemical labels)
- Mass spectrometric resolution parameter (ppm tolerance, typically 2 ppm)
- Intensity profile data for the feature pair (optional, for validation)

## Outputs

- Refined candidate annotation table (feature pairs, observed Δm/z, matched adduct/fragment labels, mass accuracy in ppm)
- Mass accuracy metrics per annotation
- Filtered feature pairs meeting mass tolerance thresholds

## How to apply

Load the correlation-identified feature pairs (m/z values and intensity profiles from the preceding correlation step) and a user-supplied adduct/fragment mass-difference reference table listing known modifications (e.g., [M-H2O+H]+, [M+nO+H]+) with their exact theoretical mass differences. For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference list using exact mass matching within a user-specified ppm tolerance (typically 2 ppm for high-resolution systems). Assign adduct or fragment labels to feature pairs where a match is found; record the measured mass accuracy (observed Δm/z vs. theoretical value). Output a refined candidate table with feature pair identities, observed mass differences, matched adduct/fragment annotations, and mass accuracy metrics to enable downstream filtering by mass error thresholds.

## Related tools

- **DBDIpy** (Implements the mass-difference refinement step via identify_adducts() function; handles alignment, imputation, correlation, and mass-difference matching for DBDI-MS datasets) — https://github.com/leopold-weidner/DBDIpy
- **Python** (Core language for executing mass-difference calculations and exact mass matching against reference tables)
- **matchms** (Integrated spectral processing library used by DBDIpy for data import and preprocessing of .mgf, .mzML, .mzXML formats) — https://github.com/matchms/matchms

## Examples

```
adduct_rule = pd.DataFrame({'deltamz': [47.984744], 'motive': ['O3']}); search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- All observed mass differences fall within the user-specified ppm tolerance of their matched theoretical values; mass accuracy histogram should be centered near 0 ppm with width ≤ tolerance.
- Feature pairs assigned to different adduct/fragment labels show distinct observed Δm/z values consistent with chemical modification definitions (e.g., [M+O+H]+ pairs have Δm/z ≈ 16 Da, [M+H2O+H]+ pairs ≈ 18 Da).
- No ambiguous assignments: each observed mass difference matches at most one reference adduct/fragment within tolerance; features with mass differences matching multiple entries are flagged or rejected.
- Output table row count equals or is less than input feature pair count (no spurious duplicates introduced).
- Mass accuracy distribution does not show systematic bias (median ppm error close to zero); large positive or negative drift suggests miscalibration or reference table error.

## Limitations

- Skill assumes that the reference adduct/fragment library is complete and accurate; missing modification entries will result in false-negative assignments. Users must curate the reference table for their ionization method and analyte class.
- Mass accuracy of assignment is limited by the mass spectrometer resolution and calibration stability; instruments with poor mass accuracy (>5 ppm drift) may fail to match true adducts or accept false positives if ppm tolerance is set too broadly.
- Feature pairs with very small or very large mass differences (e.g., loss of <1 Da or gain of >100 Da) may fall outside typical adduct/fragment definitions and remain unassigned; the skill does not perform de novo discovery of novel modifications.
- This refinement step cannot distinguish between adduct ions that have identical or near-identical mass differences (e.g., [M+O+H]+ and [M+C2H4]+, both ~16 Da); downstream MS2 spectral similarity or chromatographic data is needed for disambiguation.

## Evidence

- [other] DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+) to refine the nature of potential ion-species candidates identified by temporal correlation.: "DBDIpy implements a second refinement step in which exact mass differences are compared against a user-definable list of in-source fragments (e.g., [M-H2O+H]+) and adducts (e.g., [M+nO+H]+)"
- [other] For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching (within user-specified ppm tolerance).: "For each feature pair, calculate the observed mass difference (m/z_feature_B − m/z_feature_A). Match the observed mass difference against the reference adduct/fragment list using exact mass matching"
- [readme] (exact) mass differences are used to refine the nature of potential candidates.: "(exact) mass differences are used to refine the nature of potential candidates"
- [readme] Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
- [other] Assign adduct or fragment labels to feature pairs where a match is found, and record the mass accuracy.: "Assign adduct or fragment labels to feature pairs where a match is found, and record the mass accuracy."
