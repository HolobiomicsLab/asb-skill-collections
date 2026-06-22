---
name: data-quality-control-report-generation
description: Use when after applying biomolecule filtering criteria (minimum non-missing values and coefficient of variation thresholds) to an omics expression dataset, generate a report to document filtering impact and justify data retention decisions to stakeholders or for reproducibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - PMart_ShinyApp
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-quality-control-report-generation

## Summary

Generate a summary report documenting the number of biomolecules retained and removed at each filtering step during omics data quality control. This skill produces a transparent, auditable record of filtering decisions applied to expression datasets.

## When to use

After applying biomolecule filtering criteria (minimum non-missing values and coefficient of variation thresholds) to an omics expression dataset, generate a report to document filtering impact and justify data retention decisions to stakeholders or for reproducibility.

## When NOT to use

- No filtering has been applied to the dataset — a report on unfiltered data would be misleading.
- Filtering criteria have not been formally defined or applied (e.g., only exploratory EDA has been performed).
- The dataset is too small or the filtering has removed most biomolecules — a report may expose inadequate sample size or overly stringent thresholds before downstream analysis.

## Inputs

- expression data matrix (with initial biomolecule count)
- non-missing value counts per biomolecule
- coefficient of variation (CV) values per biomolecule
- minimum non-missing value threshold (numeric)
- maximum CV threshold (numeric)
- filtering step execution log (pass/fail counts)

## Outputs

- filtering summary report (tabular or text format)
- filtered expression matrix with metadata
- per-step biomolecule retention counts and percentages

## How to apply

Following filtering operations in pmartR, construct a summary report that tabulates: (1) the initial count of biomolecules before filtering; (2) the count retained after applying the minimum non-missing value threshold; (3) the count retained after applying the coefficient-of-variation threshold; and (4) the total count of biomolecules removed and the cumulative removal percentage. The report should be exportable as a human-readable document (e.g., text or tabular format) alongside the filtered expression matrix, providing traceability of which filtering step caused the greatest data loss and whether the filtering strategy is defensible given the dataset size.

## Related tools

- **pmartR** (R package providing filtering, data transformation, and reporting functions for omics data quality control) — https://github.com/pmartR/pmartR
- **PMart_ShinyApp** (Shiny GUI wrapper around pmartR that automates filtering workflows and generates filtering reports within the web interface) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Statistical programming language in which pmartR and reporting functions are implemented)

## Evaluation signals

- Report tabulates at least four metrics: initial biomolecule count, count after non-missing-value filtering, count after CV filtering, and total removed count.
- Sum of retained biomolecules after all steps plus removed biomolecules equals the initial count (arithmetic consistency check).
- Removal percentages are calculated correctly and sum to ≤100% at each cumulative step.
- Report is exportable and machine-readable (e.g., CSV, TSV, or structured text) alongside the filtered expression matrix.
- Filtering thresholds used (minimum non-missing values, maximum CV) are explicitly stated in the report for reproducibility.

## Limitations

- The report documents only the biomolecule filtering steps; sample-level filtering based on statistical metrics is not addressed in this skill.
- No guidance is provided on how to select optimal non-missing value or CV thresholds; the report assumes thresholds have been chosen a priori.
- The README and article do not detail validation protocols or performance metrics for the reporting functionality itself.
- If filtering is applied iteratively or conditionally, the report structure may need to be adapted; the workflow assumes sequential, non-overlapping filtering steps.

## Evidence

- [other] The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a filtered result.: "The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds"
- [other] Export the filtered expression matrix and a summary report detailing the number of biomolecules retained and removed at each filtering step.: "Export the filtered expression matrix and a summary report detailing the number of biomolecules retained and removed at each filtering step."
- [readme] Filtering. Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds.: "Filtering.  Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds."
- [readme] Shiny GUI implementation of the pmartR R package with the aim for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself.: "Shiny GUI implementation of the pmartR R package...The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package"
