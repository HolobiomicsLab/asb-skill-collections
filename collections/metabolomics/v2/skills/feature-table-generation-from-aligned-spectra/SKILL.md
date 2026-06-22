---
name: feature-table-generation-from-aligned-spectra
description: Use when after retention-time and m/z-based peak alignment has been completed across a cohort of LC-MS samples, and you need to create a unified quantitative matrix for statistical testing, multivariate analysis, or annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
---

# feature-table-generation-from-aligned-spectra

## Summary

Consolidates aligned LC-MS peaks across all samples into a quantitative feature matrix by organizing m/z, retention time, and intensity values into a single table format suitable for downstream statistical analysis. This step bridges raw spectral alignment to metabolomics data analysis by creating the canonical input for quality assessment and biological interpretation.

## When to use

After retention-time and m/z-based peak alignment has been completed across a cohort of LC-MS samples, and you need to create a unified quantitative matrix for statistical testing, multivariate analysis, or annotation workflows. Use this skill when aligned peak lists exist but have not yet been organized into a sample-by-feature intensity table.

## When NOT to use

- Input is already a complete, validated feature table from a prior analysis—skip directly to downstream statistical or annotation steps.
- Peaks have not yet been aligned across samples—perform alignment (RT and m/z-based) before consolidation.
- Raw spectral data have not undergone peak detection—execute peak detection on raw spectra before alignment.

## Inputs

- aligned peak lists (with m/z, retention time, intensity values per sample)
- peak alignment parameters (m/z tolerance, retention time tolerance)
- raw LC-MS spectral data in mzML or mzXML format

## Outputs

- quantitative feature table (sample × feature matrix with intensity values)
- feature metadata (m/z, retention time, feature identifiers)
- quality assessment report (missing value patterns, completeness metrics)

## How to apply

Take the output of peak alignment (aligned peaks with m/z, retention time, and intensity values for each sample) and consolidate them into a single quantitative feature table where rows represent unique m/z–retention-time pairs (features) and columns represent samples. Assign unique feature identifiers (e.g., based on rounded m/z and RT) to group peaks across samples that share the same mass and retention time within specified tolerances. Populate intensity values for each sample–feature pair; missing values arise when a feature is detected in some samples but not others. Validate the resulting table for completeness, missing value patterns, and quality metrics (e.g., total ion current per sample, number of features detected per sample, and reproducibility of retention time and m/z within expected instrumental precision).

## Related tools

- **MetaboAnalystR** (provides the unified LC-MS workflow module that consolidates aligned peaks into a quantitative feature table and validates it for completeness and quality metrics) — https://github.com/xia-lab/MetaboAnalystR

## Evaluation signals

- Feature table dimensions match expected number of unique m/z–RT pairs across samples
- No negative or unrealistic intensity values; intensity distribution reflects expected biological and technical variation
- Missing value pattern is sparse and random rather than systematic per sample or feature (indicating technical rather than biological dropout)
- Feature metadata (m/z, retention time) match input parameters and remain consistent across samples within instrumental precision
- Quality metrics (total ion current per sample, detection rate per feature) are within expected ranges for the instrument and biological system

## Limitations

- Feature consolidation relies on accurate prior alignment; misaligned peaks will create spurious features or merge distinct features, degrading downstream analysis.
- Missing value handling is non-trivial: features present in some samples but absent in others complicate imputation and statistical testing strategies.
- High-dimensional feature tables (>10,000 features) from untargeted LC-MS can introduce multiple-testing burden in downstream analysis.
- Intensity normalization is not addressed at this step; batch effects, instrumental drift, and sample-to-sample variation in ionization efficiency require separate correction before statistical testing.

## Evidence

- [other] Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples.: "Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples."
- [other] Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module.: "Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] MetaboAnalystR 4.0 can significantly improve the quantification accuracy and identification coverage of the metabolome: "MetaboAnalystR 4.0 can significantly improve the quantification accuracy and identification coverage of the metabolome"
