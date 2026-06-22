---
name: chemodiversity-descriptor-calculation
description: Use when you have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify the molecular chemodiversity, elemental composition diversity, or complexity of environmental organic samples for cross-sample comparison or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
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

# chemodiversity-descriptor-calculation

## Summary

Compute molecular chemodiversity descriptors (mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics) from formula-assigned FT-ICR MS datasets to characterize the molecular diversity and transformation patterns of environmental organic complex mixtures.

## When to use

Apply this skill when you have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify the molecular chemodiversity, elemental composition diversity, or complexity of environmental organic samples for cross-sample comparison or transformation analysis.

## When NOT to use

- Input is not formula-assigned: MoleTrans requires parsed molecular formulas; raw m/z values without formula assignment cannot be processed.
- Data source is not FT-ICR MS or supported mass spectrometry: while MoleTrans can partially support compound-annotated results from other MS approaches, it is optimized for FT-ICR formula assignments.
- Sample lacks sufficient molecular diversity: descriptor computation assumes a heterogeneous molecular population; homogeneous or single-compound samples may not benefit from chemodiversity metrics.

## Inputs

- formula-assigned FT-ICR MS dataset (CSV or tab-delimited table)
- columns: molecular formulas, mass values, sample identifiers

## Outputs

- structured descriptor table with sample identifiers and chemodiversity metrics
- mass-based statistics per sample
- elemental stoichiometry diversity indices per sample
- molecular complexity metrics per sample

## How to apply

Load the formula-assigned FT-ICR MS dataset into MoleTrans post-analysis module. Parse the molecular formula assignments to extract elemental composition (C, H, O, N, S, P counts) for each formula. Compute a suite of chemodiversity descriptors including mass-based statistics (e.g., mean, median, standard deviation of molecular masses), elemental stoichiometry diversity indices (ratios and proportional distributions of elements), and molecular complexity metrics across the sample. Export a structured output table or report mapping sample identifiers to descriptor values. Validate that computed indices capture expected trends in molecular complexity and that elemental counts match the input formulas.

## Related tools

- **MoleTrans** (post-analysis and data-mining platform for computing chemodiversity descriptors from formula-assigned FT-ICR MS datasets) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Output descriptor table contains one row per sample with all expected chemodiversity metrics (mass statistics, elemental diversity indices, complexity scores) populated and non-null.
- Elemental composition counts (C, H, O, N, S, P) in parsed formulas match the elemental tallies reflected in stoichiometry diversity indices.
- Molecular complexity metrics show expected correlation with formula mass and elemental richness (e.g., higher complexity for larger, more heteroatom-rich molecules).
- Sample identifiers in output table map one-to-one to input dataset rows; no duplicates or drops.
- Descriptor values fall within chemically plausible ranges (e.g., mass > 0, diversity indices 0–1 or within documented scale).

## Limitations

- MoleTrans can only partially support combined analysis on compound-annotated results from non-FT-ICR MS approaches; full optimization is for FT-ICR formula-assigned data.
- Requires user registration (or demo account) to access the live webtool; source code from the repository provides only the main calculation functions and algorithms, not the complete web interface.
- Descriptor computation assumes adequate sample size and molecular diversity; very small or homogeneous datasets may yield uninformative or unreliable indices.
- Post-analysis is limited to elemental composition (C, H, O, N, S, P); other elements present in formulas may not be represented in standard diversity metrics.

## Evidence

- [other] formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values): "Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module"
- [other] chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics: "Compute molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics across the sample."
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS."
- [readme] it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry: "Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry."
- [other] Extract elemental composition (C, H, O, N, S, P counts): "Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts)."
