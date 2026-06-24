---
name: molecular-formula-to-carbon-count-extraction
description: Use when when you have a feature list from HRMS data with molecular formula
  annotations (inferred or assigned) and need to compute per-carbon mass defect ratios
  (MD/C, m/C) as part of PFAS candidate prioritization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0157
  tools:
  - Python
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: restricted
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
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
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

# molecular-formula-to-carbon-count-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract or infer the number of carbon atoms from a molecular formula annotation associated with a mass spectrometry feature. This count is essential for computing normalized mass defect metrics (MD/C, m/C) used in PFAS prioritization workflows.

## When to use

When you have a feature list from HRMS data with molecular formula annotations (inferred or assigned) and need to compute per-carbon mass defect ratios (MD/C, m/C) as part of PFAS candidate prioritization. Apply this skill before calculating MD/C and m/C thresholds in the MD/C-m/C prioritization approach.

## When NOT to use

- Input feature list already contains pre-computed MD/C or m/C values; skip to threshold-application step.
- No molecular formulas are available and no reliable heuristic for carbon count estimation has been validated for your instrument/ionization mode.
- Feature list is from a vendor platform that does not report or export molecular formula annotations; consider alternative prioritization methods (e.g., diagnostic fragment matching without normalization).

## Inputs

- feature list (CSV or DataFrame with m/z, retention time, and optional molecular formula per feature)
- molecular formula strings (e.g., 'C8H4F17O2' extracted from feature annotations or external database)
- exact mass or neutral mass values (required as fallback if formula is unavailable)

## Outputs

- carbon count per feature (integer, scalar)
- annotated feature list with carbon_count column added
- flag or confidence score indicating extraction method (direct vs. heuristic)

## How to apply

For each feature in the input list, parse the molecular formula string (if present) to count carbon atoms; if no formula is available, apply a default heuristic (e.g., estimate from exact mass or m/z using common PFAS structural rules). The carbon count becomes the divisor in two subsequent normalizations: MD/C = mass_defect / carbon_count, and m/C = exact_mass / carbon_count. The choice between formula-based extraction and heuristic inference depends on data provenance; prefer direct extraction when formulas are reliable (e.g., from high-resolution MSn matching or database lookup), and fall back to heuristic when formulas are absent or uncertain. Document which method was used for each feature to enable downstream filtering or quality flagging.

## Related tools

- **PFΔScreen** (Host application that implements carbon extraction and MD/C-m/C computation as part of automated PFAS feature prioritization workflow) — https://github.com/JonZwe/PFAScreen
- **Python** (Programming language in which molecular formula parsing and carbon count extraction logic is implemented)

## Examples

```
# Parse feature list and extract carbon counts from molecular formula column
import pandas as pd
df = pd.read_csv('features.csv')
df['carbon_count'] = df['molecular_formula'].apply(lambda f: int(f.split('C')[1].split('H')[0]) if pd.notna(f) and 'C' in f else None)
df['MD_per_C'] = df['mass_defect'] / df['carbon_count']
df['m_per_C'] = df['exact_mass'] / df['carbon_count']
df.to_csv('features_annotated.csv', index=False)
```

## Evaluation signals

- Carbon count is a positive integer ≥ 1 for all features (no zero or negative values).
- If two features have the same molecular formula, their carbon counts are identical (deterministic).
- Downstream MD/C and m/C values fall within expected ranges for known PFAS (e.g., m/C typically 100–200 for perfluorinated compounds); anomalous ratios suggest miscounted carbons.
- Features with manually validated formulas (e.g., from reference standards) have carbon counts matching chemical databases (e.g., PubChem, ChemSpider).
- Heuristic-inferred carbon counts are flagged and can be selectively excluded or downweighted in priority scoring.

## Limitations

- Molecular formula annotations from non-target HRMS are often uncertain; incorrect or ambiguous formulas (e.g., isomers with identical mass) will propagate errors into MD/C and m/C calculations.
- Default heuristics for carbon count estimation are instrument and ionization-mode specific; generalization across ESI, APCI, or GC-HRMS platforms may introduce bias.
- The skill does not distinguish between confirmed molecular formulas (e.g., from MS/MS fragmentation patterns or isotope ratios) and tentative assignments; integration with orthogonal confirmation methods is recommended.

## Evidence

- [other] Extract or infer the number of carbons from the molecular formula (if available) or use a default heuristic.: "Extract or infer the number of carbons from the molecular formula (if available) or use a default heuristic."
- [other] Load the feature list (containing m/z, retention time, and molecular formula or neutral mass per feature) into Python.: "Load the feature list (containing m/z, retention time, and molecular formula or neutral mass per feature)"
- [other] Calculate MD/C as MD divided by carbon count, and m/C as exact mass divided by carbon count.: "Calculate MD/C as MD divided by carbon count, and m/C as exact mass divided by carbon count."
- [readme] Optionally, custom feature lists can be included.: "Optionally, custom feature lists can be included."
