---
name: molecular-formula-validation
description: Use when when you have a feature list from HRMS with tentatively assigned
  molecular formulas (from in silico tools or databases) and need to assess formula
  plausibility before applying downstream PFAS-specific filters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - PFΔScreen
  - OpenMS / pyOpenMS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Formula Validation via Mass Defect Calculation

## Summary

Validate assigned molecular formulas in high-resolution mass spectrometry (HRMS) features by calculating exact mass from elemental composition and comparing it to observed m/z to derive mass defect metrics. This skill underpins prioritization of potential PFAS in non-target screening workflows.

## When to use

When you have a feature list from HRMS with tentatively assigned molecular formulas (from in silico tools or databases) and need to assess formula plausibility before applying downstream PFAS-specific filters. Use this skill to flag or rank features whose mass defects deviate significantly from expected patterns, especially when combined with carbon-count normalization to isolate PFAS-like mass signatures.

## When NOT to use

- Input is already a curated PFAS suspect list with verified structures — use this skill for primary screening of unknowns, not re-validation of confirmed identities.
- Feature list lacks assigned molecular formulas — the skill requires formula input; de novo formula assignment is a separate (and prior) step.
- Data source is low-resolution MS (e.g., unit m/z resolution) — mass defect calculations require HRMS accuracy (ppm-level mass error); low-resolution data will yield uninformative defects.

## Inputs

- Feature list (CSV, Excel, or tabular format) with columns: m/z (observed mass-to-charge ratio), retention time (RT), intensity, assigned molecular formula (e.g., C8H4F17O2)
- Standard atomic masses (typically hardcoded or imported from a reference library)
- Optional: MS2 spectral data (mzML format) linked to features for cross-validation

## Outputs

- Validated/ranked feature list with appended columns: exact mass, calculated mass defect (Da), MD/C value (mDa/C), PFAS prioritization flag (binary or rank score)
- MD/C vs. m/z scatter plot (interactive HTML or static image) highlighting PFAS-candidate region
- Summary statistics: count of features flagged as PFAS candidates, distribution of MD/C values

## How to apply

Load a feature list containing m/z values and molecular formulas assigned to each feature. For each formula, calculate the exact mass using standard atomic weights (C: 12.0000, H: 1.00783, O: 15.99491, N: 14.00307, F: 18.99840, S: 31.97207, P: 30.97376, Cl: 34.96885, Br: 78.91834, etc.). Compute mass defect as (observed m/z − exact mass). Divide the mass defect by the number of carbon atoms in the molecular formula to obtain the MD/C (mass defect per carbon) value. Apply a threshold criterion on MD/C (typical range: −50 to +100 mDa/C for organic compounds, with PFAS candidates often occupying a narrower band) to flag features as potential PFAS candidates. The rationale is that PFAS compounds, characterized by extensive C–F bonds, occupy a distinct region of mass-defect space; normalizing by carbon count corrects for formula size and enhances discrimination. Output the filtered or ranked feature list with MD/C scores and PFAS prioritization flags for downstream validation.

## Related tools

- **PFΔScreen** (Integrates molecular-formula-validation as part of the MD/C-m/C prioritization pipeline; implements exact-mass calculation, mass-defect computation, and MD/C thresholding within the PFAS-prioritization workflow) — https://github.com/JonZwe/PFAScreen
- **Python** (Language for implementing exact-mass calculation loops, mass-defect arithmetic, and threshold filtering on feature tables)
- **OpenMS / pyOpenMS** (Provides feature detection and MS data access; molecular-formula-validation operates on the feature list output by OpenMS)

## Evaluation signals

- Exact mass values match published elemental-composition databases (e.g., NIST, ChemSpider) to within measurement precision (typically ±5 ppm for HRMS).
- Mass defect distribution is unimodal or multimodal with expected skew; outlier formulas (e.g., extreme positive or negative defects) are flagged for manual review or re-assignment.
- MD/C values for confirmed PFAS standards (perfluorooctanoic acid, perfluorooctane sulfonate, etc.) cluster in a narrow, reproducible range; unknown features with MD/C in that range score high for PFAS candidacy.
- Feature ranking by MD/C correlates with subsequent MS2 fragment confirmation (e.g., CF2 loss, CF3 groups) — top-ranked MD/C features should show diagnostic PFAS fragmentation patterns.
- Blank-subtracted sample features retain higher MD/C ranks than corresponding blank features, indicating true signal enrichment rather than formula artifacts.

## Limitations

- Exact mass calculation assumes correct elemental composition; errors in formula assignment (e.g., misassignment of isotopologue, charge state, or adduct) propagate directly into mass defect. Cross-validation with isotope patterns and adduct detection is essential.
- MD/C thresholds are empirically derived from training datasets of known PFAS; thresholds may not generalize to novel PFAS classes or non-PFAS contaminants with similar mass-defect signatures.
- Mass-defect approach assumes linear relationship between defect and carbon count, which holds well for organic molecules but may break down for extremely large molecules or those with unusual elemental compositions (e.g., many heteroatoms, unusual isotopes).
- High-resolution MS data quality (ppm-level mass accuracy, minimal spectral noise) is required; systematic mass calibration drift or poor spectral centering introduces bias in defect calculations.

## Evidence

- [other] Calculate exact mass for each molecular formula using standard atomic masses.: "Calculate exact mass for each molecular formula using standard atomic masses."
- [other] Compute mass defect (observed m/z minus exact mass) for each feature.: "Compute mass defect (observed m/z minus exact mass) for each feature."
- [other] Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value.: "Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value."
- [other] The MD/C-m/C approach is one of several prioritization techniques implemented in PFΔScreen for identifying potential PFAS features from non-target HRMS data: "The MD/C-m/C approach is one of several prioritization techniques implemented in PFΔScreen for identifying potential PFAS features from non-target HRMS data"
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences"
- [readme] To perform the PFASPrioritization, appropriate input parameters can be set, and then PFAS-specific data evaluation is performed with the "Run PFASPrioritization" button.: "To perform the PFASPrioritization, appropriate input parameters can be set, and then PFAS-specific data evaluation is performed"
