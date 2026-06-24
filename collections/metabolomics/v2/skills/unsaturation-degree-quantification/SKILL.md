---
name: unsaturation-degree-quantification
description: Use when you have FT-ICR MS peak data with assigned molecular formulas
  (C, H, O, N, S, P elemental counts) and want to characterize the structural saturation
  and aromaticity of metabolites to assess their biochemical degradation potential,
  compare chemodiversity across samples, or stratify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - NumPy
  - pandas
  - MetaboDirect
  techniques:
  - mass-spectrometry
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

# unsaturation-degree-quantification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify the degree of unsaturation and aromaticity in metabolites by calculating double-bond equivalents (DBE) and modified aromaticity index (AImod) from elemental composition of assigned molecular formulas. This enables characterization of molecular saturation state and aromatic structure prevalence, key properties for understanding metabolite lability and biochemical reactivity in FT-ICR MS datasets.

## When to use

You have FT-ICR MS peak data with assigned molecular formulas (C, H, O, N, S, P elemental counts) and want to characterize the structural saturation and aromaticity of metabolites to assess their biochemical degradation potential, compare chemodiversity across samples, or stratify compounds by oxidation state and reactivity in natural organic matter or microbial metabolomes.

## When NOT to use

- Input lacks assigned molecular formulas or elemental composition counts — DBE and AImod require complete C, H, O, N, S, P composition.
- Peaks have unvalidated or low-confidence formula assignments (e.g., ppm error > 0.5, isotopic ambiguity) — unreliable elemental counts yield meaningless indices.
- Goal is to separate chemical isomers or identify stereoisomers — DBE and AImod depend only on molecular formula, not 3D structure or connectivity, so they cannot distinguish isomeric forms.

## Inputs

- CSV table with filtered peaks and assigned molecular formulas
- Elemental composition data (C, H, O, N, S, P counts per peak)
- Peak m/z and intensity values

## Outputs

- CSV table with columns: m/z, molecular formula, DBE, AImod, NOSC, GFE, peak intensity
- Unsaturation and aromaticity metrics per peak for downstream statistical and visualization analysis

## How to apply

For each peak with a valid molecular formula, extract the elemental composition (C, H, O, N, S, P counts) from the pre-processed assignment data. Calculate DBE using the standard formula from Supplementary Table 2: DBE = (2C + 2 + N − H − X) / 2, which quantifies total degree of unsaturation (including aromatic rings and double bonds). Separately compute AImod (modified aromaticity index) using the equation in Supplementary Table 2 to reflect carbon-to-carbon double bond density normalized by molecular formula. Both indices should fall within expected biological ranges for organic matter (DBE typically 0–15 for metabolites; AImod 0–1 for saturation spectrum). Export results alongside m/z, molecular formula, peak intensity, and companion indices (NOSC, GFE) to enable joint interpretation of oxidation state and molecular structure.

## Related tools

- **NumPy** (Vectorized arithmetic for elemental composition-based calculations of DBE and AImod across peak datasets)
- **pandas** (Data frame I/O and aggregation of computed indices with peak metadata (m/z, formula, intensity))
- **MetaboDirect** (End-to-end pipeline that implements DBE and AImod calculation as part of the pre-processing and data diagnostics workflow steps) — https://github.com/Coayala/MetaboDirect

## Evaluation signals

- All peaks with valid molecular formulas receive both DBE and AImod values; no missing or NaN entries in output.
- DBE values are non-negative integers or half-integers (e.g., 0, 0.5, 1, 1.5) and fall within 0–15 range typical for metabolites.
- AImod values range from 0 (fully aliphatic) to 1 (highly aromatic) and correlate inversely with H/C ratio as expected for organic matter spectra.
- Indices are exportable alongside NOSC and GFE in a single CSV; indices from the same peak are mutually consistent (e.g., high DBE often co-occurs with higher AImod).
- Computed values match reference calculations from Supplementary Table 2 equations on a validation subset of test formulas.

## Limitations

- DBE and AImod are computed from molecular formula alone and cannot distinguish chemical isomers or stereoisomers — peaks with identical C, H, O, N, S, P composition receive identical indices even if they represent different 3D structures or connectivity arrangements.
- Uncertain elemental assignments (e.g., from ion suppression, isotopic ambiguity, or relaxed mass tolerance) propagate directly into indices; validation relies on upstream formula assignment quality (e.g., < 0.5 ppm error threshold).
- DBE interpretation assumes standard valency (C=4, H=1, N=3/5, S=2/4); novel or exotic oxidation states or radicals may yield non-intuitive or negative values not discussed in the article.

## Evidence

- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas to characterize metabolite properties such as saturation, lability, and degree of oxidation.: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [other] For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2. Calculate Gibbs free energy (ΔG°C-ox or GFE) for each peak from NOSC to determine degradation likelihood using the equation in Supplementary Table 2. Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation. Calculate double bond equivalent (DBE) representing molecular unsaturation and aromatic structure presence from elemental composition using Supplementary Table 2 equation.: "Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation. Calculate double bond equivalent (DBE)"
- [other] Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. Validation: all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. Validation: all peaks with valid molecular formulas receive four index"
- [methods] calculating several thermodynamic and molecular indices based on each peak's elemental composition: "calculating several thermodynamic and molecular indices based on each peak's elemental composition"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: Python: argparse, numpy, pandas, seaborn, more-itertools, py4cytoscape, statsmodels: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: Python: argparse, numpy, pandas, seaborn, more-itertools,"
