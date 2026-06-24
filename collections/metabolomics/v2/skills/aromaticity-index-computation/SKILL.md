---
name: aromaticity-index-computation
description: Use when after molecular formula assignment from FT-ICR MS peaks and
  elemental composition tabulation (C, H, O, N, S, P counts), when you need to quantify
  the degree of aromaticity and carbon-skeleton unsaturation for each detected compound
  to support Van Krevelen classification, chemodiversity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - NumPy
  - pandas
  - MetaboDirect
  techniques:
  - direct-infusion-MS
  license_tier: restricted
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

# aromaticity-index-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Computation of the modified Aromaticity Index (AImod) from elemental composition of assigned molecular formulas to characterize the density of carbon-to-carbon double bonds and aromatic structure in metabolites. This index is a key thermodynamic descriptor for evaluating metabolite lability and degree of structural condensation in complex organic mixtures analyzed by FT-ICR MS.

## When to use

After molecular formula assignment from FT-ICR MS peaks and elemental composition tabulation (C, H, O, N, S, P counts), when you need to quantify the degree of aromaticity and carbon-skeleton unsaturation for each detected compound to support Van Krevelen classification, chemodiversity analysis, or mechanistic interpretation of metabolite reactivity and persistence in natural organic matter.

## When NOT to use

- Input peaks lack valid molecular formula assignments or elemental composition counts; AImod requires complete C, H, O, N, S, P data.
- Molecular formulas were assigned using very loose mass error tolerances (>1 ppm); unreliable formula assignments will produce meaningless AImod values.
- The goal is to separate chemical isomers or distinguish regioisomers; FT-ICR MS cannot resolve isomers and AImod, based only on elemental composition, cannot discriminate structural isomers.

## Inputs

- CSV file containing filtered peak data with m/z values, assigned molecular formulas, and elemental composition (C, H, O, N, S, P atom counts) from pre-processing step output

## Outputs

- CSV table with columns for m/z, molecular formula, AImod (modified Aromaticity Index), and optionally peak intensity and other thermodynamic indices (NOSC, GFE, DBE)

## How to apply

For each peak with a valid assigned molecular formula and its elemental composition counts, apply the modified Aromaticity Index (AImod) equation from the article's Supplementary Table 2 using the carbon (C), hydrogen (H), oxygen (O), nitrogen (N), sulfur (S), and phosphorus (P) atom counts. The equation reflects the density of C=C double bonds normalized by total carbon; compute it on vectorized elemental composition data using NumPy or pandas for efficiency across all peaks. Validate that computed AImod values fall within expected ranges (typically 0–1 for natural organic matter); peaks with incomplete or ambiguous formula assignments should be excluded before computation to ensure data quality.

## Related tools

- **NumPy** (Vectorized computation of AImod values across all elemental composition arrays)
- **pandas** (Loading, organizing, and exporting filtered peak data with elemental composition and computed AImod indices as CSV DataFrames)
- **MetaboDirect** (Command-line pipeline that orchestrates aromaticity index computation as part of the data exploration and characterization workflow) — https://github.com/Coayala/MetaboDirect

## Evaluation signals

- All peaks with valid molecular formulas receive a single AImod value; no missing or NaN values in the output column.
- Computed AImod values fall within expected biological ranges for natural organic matter (typically 0–1 for lipids, carbohydrates, proteins, and lignins).
- AImod values are consistent with chemical logic: highly condensed aromatic structures (e.g., polycyclic aromatics) yield higher AImod; aliphatic and saturated compounds yield lower AImod.
- The output CSV contains no duplicate rows and preserves the original m/z and molecular formula columns for traceability and cross-referencing.
- Spot-check: manually calculate AImod for a subset of peaks using the Supplementary Table 2 equation and verify agreement with the computed column to within machine precision (< 1e-10).

## Limitations

- AImod is computed solely from elemental composition and does not distinguish chemical isomers or regioisomers; FT-ICR MS lacks separation capacity and cannot provide structural isomer information.
- The modified Aromaticity Index assumes all heteroatoms (N, S, P, O) are accounted for in the assigned formula; unrecognized or misassigned heteroatoms will bias AImod computation.
- AImod values are relative indices; absolute comparison between datasets requires normalization to the same formula assignment stringency and mass error tolerance (≤0.5 ppm recommended per methods).
- Peaks detected below the ion suppression threshold or obscured by matrix effects may be underrepresented; AImod is only meaningful for confidently assigned and detected peaks.

## Evidence

- [other] Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation.: "Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation."
- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas to characterize metabolite properties such as saturation, lability, and degree of oxidation.: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [other] all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter."
- [intro] FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures: "FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures"
- [intro] Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers, lack of: "Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers"
