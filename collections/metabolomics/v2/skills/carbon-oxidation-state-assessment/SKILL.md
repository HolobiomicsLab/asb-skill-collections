---
name: carbon-oxidation-state-assessment
description: Use when after molecular formula assignment from FT-ICR MS peak data, when you need to classify metabolites by their redox state to predict bioavailability or lability, or when generating thermodynamic indices for chemodiversity analysis and environmental metabolomic interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - NumPy
  - pandas
  - MetaboDirect
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# carbon-oxidation-state-assessment

## Summary

Calculate the nominal oxidation state of carbon (NOSC) from elemental composition of assigned molecular formulas to characterize metabolite oxidation degree and predict degradation likelihood in FT-ICR MS metabolomic datasets.

## When to use

After molecular formula assignment from FT-ICR MS peak data, when you need to classify metabolites by their redox state to predict bioavailability or lability, or when generating thermodynamic indices for chemodiversity analysis and environmental metabolomic interpretation.

## When NOT to use

- Peaks without assigned molecular formulas or missing elemental composition counts cannot be processed.
- If only m/z values are available without formula assignment, NOSC cannot be calculated.
- Data from techniques other than direct-injection FT-ICR MS (e.g., GC-MS, LC-MS with chromatographic separation) require different oxidation state frameworks.

## Inputs

- Peak data table (CSV) with m/z, assigned molecular formula, and elemental composition counts (C, H, O, N, S, P)
- Supplementary Table 2 NOSC equation specification

## Outputs

- NOSC index column (numeric vector) for each peak
- Extended CSV table with columns: m/z, molecular formula, NOSC, peak intensity

## How to apply

For each peak with assigned molecular formula and elemental composition (C, H, O, N, S, P counts), apply the NOSC calculation equation from Supplementary Table 2 using the elemental composition vector. NOSC characterizes the average oxidation state of carbon atoms within the molecule and ranges typically from −1 (highly reduced, e.g., alkanes) to +1 (highly oxidized, e.g., carboxylic acids) for organic matter. The calculation is deterministic given valid elemental counts; validate by ensuring all peaks with valid formulas receive NOSC values within expected biological ranges (typically −0.5 to +0.5 for natural organic matter). NOSC is downstream of formula assignment but upstream of Gibbs free energy and aromaticity index calculations, which depend on it. No missing or NaN values should appear in the output column.

## Related tools

- **MetaboDirect** (Command-line pipeline that orchestrates NOSC calculation as part of thermodynamic index computation step following formula assignment) — https://github.com/Coayala/MetaboDirect
- **NumPy** (Vectorized computation of NOSC from elemental composition arrays)
- **pandas** (Data frame management for indexed storage and export of NOSC values alongside peak metadata)

## Evaluation signals

- All peaks with valid assigned molecular formulas receive exactly one NOSC value; no NaN or missing entries in output column.
- NOSC values fall within expected biological ranges for organic matter (typically −0.5 to +0.5 for natural organic matter; extremes −1 to +1 acceptable for synthetic or highly reduced/oxidized compounds).
- NOSC values correlate predictably with compound class (e.g., carbohydrates cluster near −0.3 to 0, lipids near −1, highly oxygenated acids near +0.5), reflecting known redox chemistry.
- NOSC computation is deterministic: identical elemental compositions produce identical NOSC values across runs.
- NOSC output integrates cleanly into downstream Gibbs free energy (ΔG°C-ox) and aromaticity index (AImod) calculations without data type mismatches.

## Limitations

- NOSC assumes all assigned molecular formulas are correct; errors in formula assignment directly propagate to incorrect NOSC values.
- NOSC is an average oxidation state per molecule and does not distinguish structural isomers with identical molecular formulas but different spatial arrangements or local oxidation states.
- FT-ICR MS cannot directly distinguish chemical isomers, so two signals with the same m/z and formula receive the same NOSC even if they represent different compounds with different true oxidation states.
- NOSC calculation is sensitive to detection of low-abundance elements (N, S, P); incomplete or misassigned minor element counts can introduce systematic bias.

## Evidence

- [other] For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2.: "For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2."
- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas to characterize metabolite properties such as saturation, lability, and degree of oxidation.: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [other] all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter."
- [other] Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV.: "Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV."
- [other] Calculate Gibbs free energy (ΔG°C-ox or GFE) for each peak from NOSC to determine degradation likelihood using the equation in Supplementary Table 2.: "Calculate Gibbs free energy (ΔG°C-ox or GFE) for each peak from NOSC to determine degradation likelihood using the equation in Supplementary Table 2."
