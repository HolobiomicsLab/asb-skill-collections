---
name: elemental-composition-extraction
description: Use when you have formula-assigned FT-ICR MS data (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify elemental stoichiometry, compute diversity indices, or assess molecular complexity across environmental organic mixtures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3094
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - MoleTrans
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moletrans_cq
    doi: 10.1021/acs.estlett.5c00284
    title: MoleTrans
  dedup_kept_from: coll_moletrans_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.estlett.5c00284
  all_source_dois:
  - 10.1021/acs.estlett.5c00284
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# elemental-composition-extraction

## Summary

Extract and parse elemental composition (C, H, O, N, S, P counts) from molecular formula assignments in FT-ICR MS datasets to enable downstream chemodiversity descriptor computation and molecular transformation analysis.

## When to use

You have formula-assigned FT-ICR MS data (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify elemental stoichiometry, compute diversity indices, or assess molecular complexity across environmental organic mixtures. This skill is the entry point for post-analysis workflows that require standardized elemental accounting before descriptor generation.

## When NOT to use

- Input dataset lacks molecular formula assignments or contains only mass-to-charge ratios without structural information
- Formula annotations are from non-FT-ICR MS sources without prior validation or harmonization to FT-ICR mass accuracy standards
- Downstream analysis requires compound-level structural features (e.g., DBE, aromaticity indices) beyond elemental stoichiometry

## Inputs

- formula-assigned FT-ICR MS dataset (CSV or tab-delimited table)
- molecular formula strings (e.g., 'C₁₂H₂₀O₅')
- sample identifiers

## Outputs

- structured elemental composition table (C, H, O, N, S, P counts per formula)
- validated formula-to-element mapping
- elemental composition vectors for downstream descriptor calculation

## How to apply

Load the formula-assigned FT-ICR MS dataset into MoleTrans and parse the molecular formula assignments to extract individual elemental counts (C, H, O, N, S, P). The parser should validate formula syntax and standardize elemental notation. These extracted counts serve as the foundation for computing molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics. Verify extraction accuracy by spot-checking formula-to-count mappings and confirming that all detected elements are captured in the output table.

## Related tools

- **MoleTrans** (Post-analysis and data mining platform that ingests formula-assigned FT-ICR MS datasets and performs elemental composition parsing and chemodiversity descriptor computation) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Elemental counts (C, H, O, N, S, P) are non-negative integers and consistent with input formula strings
- All molecular formulas in the input dataset are successfully parsed with no unhandled exceptions or missing element counts
- Output table preserves sample identifiers and mass values alongside extracted elemental composition; row count matches input dataset
- Spot-check: manually verify 5–10 formula-to-element mappings by hand calculation; counts must match exactly
- Downstream chemodiversity descriptors (e.g., diversity indices, complexity metrics) are computable from the extracted elemental table with no missing or anomalous values

## Limitations

- MoleTrans can only partially support combined analysis on compound-annotated results from non-FT-ICR MS approaches; elemental extraction assumes FT-ICR-standard formula quality
- Extraction depends on formula assignment accuracy upstream; incorrect or ambiguous formula assignments will propagate into elemental counts
- Rare or unusual elements (e.g., halogens, metals) may not be captured if the parser is tuned only for C, H, O, N, S, P

## Evidence

- [other] Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts).: "Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts)."
- [other] MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations: "MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations"
- [other] Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values): "Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values)"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS"
