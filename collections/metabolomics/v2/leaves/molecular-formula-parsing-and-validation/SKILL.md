---
name: molecular-formula-parsing-and-validation
description: Use when you have received a formula-assigned FT-ICR MS dataset (CSV
  or tab-delimited table containing molecular formulas and mass values) and need to
  convert those formula strings into quantified elemental compositions before computing
  molecular descriptors, diversity indices, or transformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3727
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MoleTrans
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned
  datasets from FT-ICR MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-parsing-and-validation

## Summary

Parse and validate molecular formula assignments from FT-ICR MS datasets to extract elemental composition (C, H, O, N, S, P counts) for downstream chemodiversity analysis. This skill transforms raw formula strings into structured elemental inventories required for molecular complexity metrics and stoichiometric diversity calculations.

## When to use

Apply this skill when you have received a formula-assigned FT-ICR MS dataset (CSV or tab-delimited table containing molecular formulas and mass values) and need to convert those formula strings into quantified elemental compositions before computing molecular descriptors, diversity indices, or transformation patterns in complex environmental organic mixtures.

## When NOT to use

- Input formulas are already parsed into elemental composition vectors or feature tables; re-parsing would duplicate effort.
- Dataset contains only compound-annotated results from non-FT-ICR MS approaches where formula assignment confidence or elemental coverage differs significantly from FT-ICR conventions.
- Formula strings are unstructured or lack standardized notation; validation would fail or require substantial preprocessing outside MoleTrans scope.

## Inputs

- Formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values)
- Molecular formula strings (e.g., 'C8H12O3', 'C10H15NO2S')

## Outputs

- Parsed elemental composition table (indexed by sample identifier, mass, and formula; containing C, H, O, N, S, P counts)
- Validated molecular formula inventory (non-negative integer elemental counts per formula)

## How to apply

Load the formula-assigned FT-ICR MS dataset from the source (CSV or tab-delimited format) into the MoleTrans post-analysis module. Parse each molecular formula assignment by tokenizing the elemental symbols and extracting stoichiometric counts for C, H, O, N, S, and P. Validate that each parsed formula is chemically plausible (e.g., non-negative integer counts, ratios within known bounds for organic matter). Store the extracted elemental composition in a structured table indexed by sample identifier and mass value. This parsing step is essential because downstream chemodiversity descriptors (mass-based statistics, elemental stoichiometry diversity indices, molecular complexity metrics) depend on accurate, validated elemental counts.

## Related tools

- **MoleTrans** (Post-analysis and data mining webtool that ingests formula-assigned FT-ICR MS datasets; executes formula parsing, elemental extraction, and chemodiversity descriptor computation) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- All formula strings in the input dataset are successfully parsed without syntax errors or dropped rows.
- Elemental counts (C, H, O, N, S, P) for each formula are non-negative integers and fall within chemically plausible ranges for organic environmental samples.
- Parsed elemental composition table contains no missing values for any formula in the input dataset; row count matches input formula count.
- Downstream chemodiversity descriptors (mass-based statistics, elemental stoichiometry diversity indices, molecular complexity metrics) can be computed without errors from the parsed elemental inventory.
- Spot-check: manually verify 5–10 random formulas by comparing their parsed elemental counts against the original formula strings to confirm tokenization accuracy.

## Limitations

- MoleTrans can only partially support combined analysis on compound-annotated results from mass spectrometry approaches other than FT-ICR MS, so formula parsing may be incomplete or less reliable for mixed-source datasets.
- Parsing assumes standardized molecular formula notation (e.g., Hill system or alphabetical order); non-standard or malformed formula strings may fail to parse.
- Only C, H, O, N, S, P are extracted; other elements present in formulas may be ignored, potentially underrepresenting elemental diversity in some environmental samples.

## Evidence

- [other] Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts).: "Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts)."
- [other] Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module: "Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS."
- [other] Compute molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics across the sample.: "Compute molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics across the sample."
