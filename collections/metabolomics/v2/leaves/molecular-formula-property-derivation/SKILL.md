---
name: molecular-formula-property-derivation
description: Use when you have filtered FT-ICR MS peak data with valid molecular formula
  assignments (C, H, O, N, S, P elemental counts) and need to quantify molecular properties
  that predict metabolite reactivity, bioavailability, and biochemical role.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - NumPy
  - pandas
  - MetaboDirect
  - CoreMS
  - Formularity
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and
  is available to install through the Python Package Index... It requires the Python
  dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas [41, 42]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-property-derivation

## Summary

Compute thermodynamic and molecular indices (DBE, GFE, AImod, NOSC) from elemental composition of assigned molecular formulas to characterize metabolite saturation, lability, oxidation state, and aromaticity. This skill transforms high-resolution FT-ICR MS formula assignments into interpretable biochemical properties for downstream metabolomic analysis.

## When to use

You have filtered FT-ICR MS peak data with valid molecular formula assignments (C, H, O, N, S, P elemental counts) and need to quantify molecular properties that predict metabolite reactivity, bioavailability, and biochemical role. Apply this skill when you want to move beyond mass-to-charge ratios to chemical characterization suitable for Van Krevelen diagrams, transformation network inference, or chemodiversity analysis.

## When NOT to use

- Peak data lacks assigned molecular formulas or elemental composition counts — index calculation requires complete chemical formula, not just m/z.
- Unfiltered raw FT-ICR MS data with isotopic duplicates, high mass error peaks, or low-intensity noise — apply pre-processing and filtering first to ensure formula assignment confidence.
- Analysis requires structural isomer separation or fine-grained functional group composition — these indices describe aggregate elemental oxidation state and saturation, not detailed structural features.

## Inputs

- CSV file with filtered FT-ICR MS peaks: columns m/z, molecular_formula, C_count, H_count, O_count, N_count, S_count, P_count, peak_intensity
- Elemental composition table (atom counts per formula)
- Biochemical index calculation equations (DBE, NOSC, GFE, AImod formulas from Supplementary Table 2)

## Outputs

- CSV table with rows = peaks, columns = m/z, molecular_formula, NOSC, GFE, AImod, DBE, peak_intensity
- Thermodynamic and molecular index values for each peak (numeric scalars per index per peak)
- Quality report confirming 100% of valid formula peaks received four index values with no NaN values

## How to apply

Load filtered peak data in CSV format containing m/z, molecular formula, and elemental composition (C, H, O, N, S, P counts) from the data pre-processing step. For each peak, apply the equations in Supplementary Table 2 of the source article to sequentially compute: (1) nominal oxidation state of carbon (NOSC) from elemental composition to quantify the average carbon oxidation state; (2) Gibbs free energy of carbon oxidation (ΔG°C-ox or GFE) from NOSC to predict degradation likelihood; (3) modified aromaticity index (AImod) from elemental composition to reflect carbon-to-carbon double bond density; and (4) double bond equivalent (DBE) from elemental composition to represent total molecular unsaturation and aromatic character. Export results as a CSV table with one row per peak, including columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. Use NumPy and pandas for vectorized computation across all peaks in a single pass.

## Related tools

- **MetaboDirect** (End-to-end FT-ICR MS pipeline that integrates this index-derivation skill within its data exploration and pre-processing workflow modules) — https://github.com/Coayala/MetaboDirect
- **NumPy** (Vectorized arithmetic computation of index equations over all peak elemental compositions simultaneously)
- **pandas** (Tabular data loading, element composition manipulation, and CSV export of computed indices)
- **CoreMS** (Upstream tool for signal processing and molecular formula assignment that produces elemental composition input for this skill)
- **Formularity** (Alternative upstream tool for molecular formula assignment from FT-ICR MS raw data)

## Evaluation signals

- All peaks with valid molecular formulas (non-null elemental composition) have exactly four index values (NOSC, GFE, AImod, DBE) with no NaN or null entries.
- Numeric indices fall within expected biological ranges: NOSC typically [-1, +1] for organic matter; AImod in [0, 1]; DBE ≥ 0; GFE in realistic kcal/mol bounds.
- Output CSV has same number of rows as input filtered peak list, with consistent m/z and formula columns carried through.
- Index values show expected correlations: peaks with high DBE and AImod should show elevated AImod; peaks with more reduced carbon (negative NOSC) should show more negative ΔG°C-ox (higher free energy of oxidation).
- Computation completes without runtime errors and produces reproducible results when re-run on the same input data.

## Limitations

- Index calculation assumes molecular formulas are correctly assigned; errors in formula assignment (> 0.5 ppm mass error) propagate directly to index errors.
- Indices characterize average bulk oxidation state and saturation per formula but cannot distinguish structural isomers or regioisomers with identical elemental composition.
- GFE prediction of degradation likelihood is based on thermodynamic favorability alone and does not account for kinetic barriers, enzyme availability, or environmental bioavailability.
- DBE calculation from elemental composition is sensitive to presence of heteroatoms (N, S, P); the formula assumes standard valencies and may miscount unsaturation in unusual bonding configurations.

## Evidence

- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas to characterize metabolite properties such as saturation, lability, and degree of oxidation.: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [methods] For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2. Calculate Gibbs free energy (ΔG°C-ox or GFE) for each peak from NOSC to determine degradation likelihood using the equation in Supplementary Table 2. Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation. Calculate double bond equivalent (DBE) representing molecular unsaturation and aromatic structure presence from elemental composition using Supplementary Table 2 equation.: "For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2. Calculate Gibbs free energy (ΔG°C-ox"
- [other] Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. Validation: all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. Validation: all peaks with valid molecular formulas receive four index"
- [other] Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV.: "Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV."
- [methods] calculating several thermodynamic and molecular indices based on each peak's elemental composition: "calculating several thermodynamic and molecular indices based on each peak's elemental composition"
