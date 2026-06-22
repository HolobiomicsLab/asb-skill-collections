---
name: elemental-composition-parsing
description: Use when when you have FT-ICR MS peak data with assigned molecular formulas (e.g., from CoreMS, Formularity, or similar formula assignment tools) and need to compute thermodynamic indices (DBE, GFE, AImod, NOSC) or classify peaks by elemental composition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3737
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - NumPy
  - pandas
  - CoreMS
  - Formularity
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

# elemental-composition-parsing

## Summary

Extract and structure elemental composition (C, H, O, N, S, P counts) from assigned molecular formulas in FT-ICR MS peak data. This is a prerequisite step that prepares composition data for downstream thermodynamic index calculation and molecular characterization.

## When to use

When you have FT-ICR MS peak data with assigned molecular formulas (e.g., from CoreMS, Formularity, or similar formula assignment tools) and need to compute thermodynamic indices (DBE, GFE, AImod, NOSC) or classify peaks by elemental composition. Apply this skill immediately after molecular formula assignment and filtering but before index calculation.

## When NOT to use

- Peak data lacks assigned molecular formulas or formula assignment confidence is below acceptable thresholds (e.g., mass error > 0.5 ppm tolerance)
- Input is already a pre-computed feature table with derived indices; parsing is redundant
- Elemental composition data is incomplete or partially missing for significant portions of peaks

## Inputs

- CSV file containing filtered FT-ICR MS peaks with assigned molecular formulas
- Elemental composition counts (C, H, O, N, S, P) per peak from formula assignment

## Outputs

- Structured table (CSV or DataFrame) with columns: m/z, molecular_formula, C_count, H_count, O_count, N_count, S_count, P_count, peak_intensity

## How to apply

Load the filtered peak data CSV output containing assigned molecular formulas and their elemental composition from the MetaboDirect pre-processing step. Parse each row's molecular formula string to extract or verify the count of C, H, O, N, S, and P atoms. Store these counts in a structured format (e.g., dictionary or DataFrame columns) alongside m/z and formula identifiers. Ensure all peaks with valid molecular formulas have complete elemental counts with no missing or NaN values. This parsed composition forms the input for subsequent thermodynamic index calculations using the equations in Supplementary Table 2.

## Related tools

- **pandas** (Load, parse, and structure CSV data containing molecular formulas and elemental counts into DataFrames for index calculation)
- **NumPy** (Vectorize elemental count extraction and validation across multiple peaks)
- **CoreMS** (Upstream tool: assigns molecular formulas and provides initial elemental composition data to this skill)
- **Formularity** (Upstream tool: alternative formula assignment software that provides the molecular formulas and elemental counts as input)

## Examples

```
import pandas as pd; peaks = pd.read_csv('filtered_peaks.csv'); peaks[['C','H','O','N','S','P']] = peaks['molecular_formula'].str.extract(r'C(\d+)H(\d+)O(\d+)N(\d+)S(\d+)P(\d+)', expand=True).fillna(0).astype(int); peaks.to_csv('elemental_composition.csv', index=False)
```

## Evaluation signals

- All peaks with valid molecular formulas contain non-null C, H, O, N, S, P counts in output table
- Elemental counts match the molecular formula string (e.g., C6H12O6 has C_count=6, H_count=12, O_count=6)
- No NaN or missing values in elemental composition columns for successfully assigned formulas
- Output row count equals input peak count (no unexpected filtering or loss of records)
- Elemental counts fall within expected biological ranges (e.g., C: 3–100, H: 4–200 for typical organic metabolites)

## Limitations

- Cannot parse or recover elemental counts from unassigned peaks or those with failed formula assignment
- Requires upstream mass error filtering (≤0.5 ppm recommended per article) to ensure formula assignments are reliable; elemental counts inherit errors from upstream formula assignment
- FT-ICR MS has inherent inability to separate chemical isomers; different structural arrangements yield identical elemental compositions, so parsed counts alone do not distinguish isomers
- Isotopic peaks (e.g., 13C) must be filtered out before parsing to avoid double-counting; MetaboDirect removes these during pre-processing

## Evidence

- [other] Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV.: "Load filtered peak data with assigned molecular formulas and elemental composition (C, H, O, N, S, P counts) from the pre-processing step output as CSV."
- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas to characterize metabolite properties such as saturation, lability, and degree of oxidation.: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [other] For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2.: "For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation"
- [other] all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "all peaks with valid molecular formulas receive four index values; no missing or NaN values in output"
- [methods] detected peaks are filtered by their m/z values (based on the user's input), isotopic presence (13C peaks), and error in formula assignment (0.5 ppm): "detected peaks are filtered by their m/z values (based on the user's input), isotopic presence (13C peaks), and error in formula assignment (0.5 ppm)"
