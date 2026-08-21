---
name: mass-spectrometry-dataset-post-processing
description: Use when you have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited
  table with molecular formulas and mass values) and need to quantify molecular chemodiversity,
  characterize elemental stoichiometry patterns, or explore transformation pathways
  across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# mass-spectrometry-dataset-post-processing

## Summary

Post-analysis and data mining of formula-assigned FT-ICR MS datasets to compute molecular chemodiversity descriptors and extract elemental composition statistics from environmental organic complex mixtures. Transforms raw mass spectrometry assignments into structured, interpretable molecular complexity metrics suitable for transformation and reactivity analysis.

## When to use

You have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify molecular chemodiversity, characterize elemental stoichiometry patterns, or explore transformation pathways across samples. Use this skill when the input is already formula-resolved (not raw m/z spectra) and your goal is to extract bulk chemical diversity statistics rather than compound-level identification.

## When NOT to use

- Input is raw, unassigned FT-ICR MS spectra (m/z peaks without formula assignments) — use mass calibration and formula assignment first
- You need to identify specific compounds or assign structures — this skill produces bulk molecular descriptors, not individual compound annotations
- Input contains only peak intensities without molecular formula or elemental composition metadata

## Inputs

- Formula-assigned FT-ICR MS dataset (CSV or tab-delimited table)
- Molecular formula strings (e.g., C₁₂H₂₀O₁₀)
- Mass values (m/z or exact mass)
- Sample identifiers or run metadata

## Outputs

- Structured descriptor table with sample identifiers and computed chemodiversity metrics
- Mass-based statistics (average mass, mass range per sample)
- Elemental stoichiometry diversity indices
- Molecular complexity metrics (e.g., DBE, H/C, O/C ratios)
- Exported report (CSV or formatted table)

## How to apply

Load the formula-assigned dataset (CSV or tab-delimited format containing molecular formulas, mass values, and sample identifiers) into MoleTrans. Parse the molecular formula strings to extract elemental composition counts (C, H, O, N, S, P). Compute mass-based statistics (e.g., average nominal mass, mass range), elemental stoichiometry diversity indices, and molecular complexity metrics (e.g., degree of unsaturation, aromaticity indices) on a per-sample basis. Aggregate results into a structured output table indexed by sample identifier, with one row per descriptor and columns for descriptor name, value, and metadata. Validate that all formula strings parse successfully and that computed descriptors fall within expected chemical ranges (e.g., H/C and O/C ratios typical for environmental DOM).

## Related tools

- **MoleTrans** (Webtool for post-analysis and data mining on formula-assigned FT-ICR MS datasets; computes molecular chemodiversity descriptors and enables transformation analysis of environmental organic complex mixtures) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- All molecular formula strings in the input parse successfully without errors; elemental counts (C, H, O, N, S, P) are non-negative integers
- Computed H/C and O/C ratios fall within literature ranges for environmental DOM (typically H/C ∈ [0.5, 2.5], O/C ∈ [0, 1.2])
- Output descriptor table has exactly one row per computed metric per sample; no missing or NaN values in required descriptor columns
- Descriptor values are reproducible across re-runs with identical input; output schema matches specification (sample_id, descriptor_name, value columns)
- Mass-based statistics (mean, min, max) are consistent with input m/z distribution; elemental diversity indices decrease monotonically as the number of unique formulas decreases

## Limitations

- MoleTrans partially supports compound-annotated results from other mass spectrometry approaches but is optimized for FT-ICR MS formula assignments; generalization to other MS platforms requires validation
- Descriptor computation assumes correct formula assignment; errors or ambiguities in input formula strings will propagate to output metrics
- The webtool (www.moletrans.cn) requires user registration for stable operation; source code is provided but full reproduction may require reverse-engineering of web algorithms

## Evidence

- [other] MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations to enable molecular chemodiversity exploration and transformation analysis of environmental organic complex mixtures.: "MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations to enable molecular chemodiversity exploration and transformation analysis"
- [other] Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module: "Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module"
- [other] Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts). Compute molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics across the sample.: "Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts). Compute molecular chemodiversity descriptors including mass-based statistics, elemental"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated"
