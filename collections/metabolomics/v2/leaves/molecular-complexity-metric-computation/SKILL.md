---
name: molecular-complexity-metric-computation
description: Use when you have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited
  table with molecular formulas and mass values) and need to quantify the structural
  diversity, elemental stoichiometry patterns, or complexity landscape of the organic
  mixture.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3172
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

# molecular-complexity-metric-computation

## Summary

Compute molecular complexity metrics and chemodiversity descriptors from formula-assigned FT-ICR MS datasets to quantify the structural and compositional diversity of environmental organic complex mixtures. This enables systematic characterization of molecular transformations and reactivity patterns across environmental samples.

## When to use

Apply this skill when you have a formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) and need to quantify the structural diversity, elemental stoichiometry patterns, or complexity landscape of the organic mixture. Typical triggers include: exploring chemodiversity across treatment conditions, comparing DOM reactivity in anaerobic systems, or screening for molecular transformation patterns in environmental samples.

## When NOT to use

- Input dataset lacks molecular formula assignments or contains only m/z values without elemental composition—use formula assignment/annotation tools first.
- Data are already pre-aggregated into a feature or descriptor table—this skill is for raw formula-to-metric transformation, not re-computation.
- Sample size is <2 or dataset is a single chromatographic peak—complexity metrics are most meaningful at the mixture level, not individual compound level.

## Inputs

- Formula-assigned FT-ICR MS dataset in CSV or tab-delimited format with columns: molecular formula, mass (m/z), sample identifier
- Elemental composition counts extracted from parsed molecular formulas

## Outputs

- Structured descriptor table with rows = samples, columns = computed complexity and chemodiversity metrics (mass-based statistics, elemental ratios, diversity indices, molecular complexity scores)
- Sample-level summary report with descriptor values and sample identifiers

## How to apply

Load the formula-assigned FT-ICR MS dataset into the MoleTrans post-analysis module. Parse molecular formula assignments to extract elemental composition counts (C, H, O, N, S, P). Compute mass-based statistics (e.g., mean mass, mass range), elemental stoichiometry diversity indices (e.g., H/C, O/C ratios), and molecular complexity metrics (e.g., degree of unsaturation, aromaticity indices) across the sample. Generate and export a structured output table containing computed descriptors indexed by sample identifier. Evaluate correctness by verifying that descriptor ranges are chemically plausible (e.g., H/C 0–2.5, O/C 0–1.2 for natural organic matter) and that sample-level statistics are consistent with the input formula cardinality.

## Related tools

- **MoleTrans** (Webtool for post-analysis and data mining on formula-assigned FT-ICR MS datasets; computes molecular chemodiversity descriptors and complexity metrics.) — https://github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Elemental composition counts (C, H, O, N, S, P) are non-negative integers consistent with parsed molecular formulas.
- Computed descriptors fall within chemically plausible ranges for environmental organic matter (H/C 0–2.5, O/C 0–1.2, mass typically 200–1000 Da).
- Sample-level descriptor values are consistent with the cardinality and composition of the input formula set (no NaN or infinite values for valid inputs).
- Output table schema matches the declared format (sample ID, descriptor name, descriptor value, units) with no missing values for complete input records.
- Descriptor variance across samples is non-zero and correlates with known treatment or transformation conditions (e.g., higher O/C in oxidized samples, higher aromaticity in aged DOM).

## Limitations

- MoleTrans partially supports formula-assigned datasets from FT-ICR MS; combined analysis on compound-annotated results from other mass spectrometry approaches has reduced coverage.
- Molecular complexity metrics are aggregate descriptors and do not resolve individual compound-level reactivity or transformation pathways.
- Accuracy of computed metrics depends on quality and completeness of upstream formula assignment; systematic mass calibration or formula assignment errors will propagate to descriptor values.
- The skill does not provide statistical significance testing or hypothesis-driven filtering; practitioner must post-process descriptor output for comparative or correlation analysis.

## Evidence

- [other] MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations to enable molecular chemodiversity exploration and transformation analysis of environmental organic complex mixtures.: "MoleTrans ingests formula-assigned datasets from FT-ICR MS and performs post-analysis and data mining operations to enable molecular chemodiversity exploration and transformation analysis of"
- [other] Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module from the published source code repository.: "Load the formula-assigned FT-ICR MS dataset (CSV or tab-delimited table with molecular formulas and mass values) into the MoleTrans post-analysis module from the published source code repository"
- [other] Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts). Compute molecular chemodiversity descriptors including mass-based statistics, elemental stoichiometry diversity indices, and molecular complexity metrics across the sample.: "Parse the molecular formula assignments and extract elemental composition (C, H, O, N, S, P counts). Compute molecular chemodiversity descriptors including mass-based statistics, elemental"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated"
