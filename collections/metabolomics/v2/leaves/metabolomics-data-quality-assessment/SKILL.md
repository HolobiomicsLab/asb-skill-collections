---
name: metabolomics-data-quality-assessment
description: Use when after consolidating aligned LC-MS peaks into a quantitative
  feature table (with m/z, retention time, and intensity values across all samples),
  and before proceeding to statistical analysis or functional interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnalystR
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-48009-6
  all_source_dois:
  - 10.1038/s41467-024-48009-6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-quality-assessment

## Summary

Validation of LC-MS feature tables for completeness, missing value patterns, and quality metrics to ensure reliable downstream metabolomics analysis. This skill detects data integrity issues and anomalies in peak-aligned quantitative features before biological interpretation.

## When to use

After consolidating aligned LC-MS peaks into a quantitative feature table (with m/z, retention time, and intensity values across all samples), and before proceeding to statistical analysis or functional interpretation. Apply this skill when you need to identify missing value patterns, assess feature detection sensitivity, verify sample reproducibility, and flag low-quality features that may bias downstream results.

## When NOT to use

- Input is already a pre-validated, published feature table with known high quality and documented QC
- Analysis goal is exploratory/hypothesis-free and explicitly tolerates missing data or noise
- Sample count is very small (N<3) such that replicate-based QC metrics are unreliable

## Inputs

- aligned feature table (m/z, retention time, intensity matrix with sample columns)
- sample metadata (replicates, batch, class assignments)
- instrument parameters and detection thresholds
- blank/negative control sample identifiers

## Outputs

- quality assessment report (missing value summary, feature statistics, sample-level metrics)
- filtered/validated feature table with low-quality features marked or removed
- quality metrics plot(s) (e.g., feature abundance distribution, sample completeness heatmap)
- list of flagged features and samples with justification for exclusion

## How to apply

Load the aligned feature table into MetaboAnalystR's quality assessment module. Execute validation checks that examine: (1) completeness of the feature matrix (proportion of missing values per feature and per sample); (2) missing value patterns (systematic absence vs. random dropout); (3) intensity distributions and dynamic range across samples; (4) feature abundance thresholds relative to blank/negative controls; and (5) reproducibility metrics (e.g., coefficient of variation within replicate samples). Flag and optionally remove features below user-defined thresholds (e.g., features present in <N% of samples, or with intensity indistinguishable from background noise). Document quality metrics for reporting and downstream filtering decisions.

## Related tools

- **MetaboAnalystR** (executes peak detection, alignment, and quality assessment module for LC-MS feature validation and missing value characterization) — https://github.com/xia-lab/MetaboAnalystR

## Evaluation signals

- Quality report accurately reflects sample-wise and feature-wise missing data counts and proportions
- Flagged low-quality features are confirmed absent or below noise floor in raw LC-MS spectra or raw intensity matrices
- Reproducibility metrics (e.g., CV of replicates) fall within expected ranges for the instrument/method used
- Filtered feature table shows improved correlation structure in downstream PCA/clustering vs. unfiltered table
- Number and identity of retained features align with prior publications on the same sample type or instrument platform

## Limitations

- Quality thresholds (e.g., missing value cutoffs, intensity minima) are context-dependent and must be tuned per instrument, ionization mode, and metabolite class; no universal standard exists
- Missing values may be non-random (e.g., systematic loss of low-abundance features in late injections due to signal drift), requiring retention-time and batch-effect correction before QC assessment
- Replicate-based QC metrics (e.g., CV thresholds) assume adequate within-group replication; sparse or unbalanced experimental designs may yield unreliable quality judgments
- The README notes no changelog is provided for version 4.0, limiting traceability of QC algorithm changes or improvements in recent releases

## Evidence

- [other] Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples.: "Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples."
- [other] Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module.: "Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module."
- [readme] MetaboAnalystR 4.0 can significantly improve the quantification accuracy and identification coverage of the metabolome.: "MetaboAnalystR 4.0 can significantly improve the quantification accuracy and identification coverage of the metabolome."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
