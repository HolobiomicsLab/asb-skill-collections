---
name: zero-value-handling-in-mass-spectrometry-data
description: Use when after feature detection has produced a feature table with zero
  and missing values (sparse abundance matrix) but before multivariate statistical
  analysis or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ThermoRawFileParser
  - Python
  - Asari
  - metDataModel
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# zero-value-handling-in-mass-spectrometry-data

## Summary

Replace zero and missing values in LC-MS metabolomics feature tables using minimum-value-based interpolation, where each feature's missing values are filled with a scaled fraction of that feature's minimum non-zero abundance. This addresses data sparsity introduced during feature detection and quantification without discarding features with sporadic low-abundance observations.

## When to use

After feature detection has produced a feature table with zero and missing values (sparse abundance matrix) but before multivariate statistical analysis or annotation. Apply this skill when you need to handle absence-of-signal entries while preserving feature variance structure and avoiding artificial feature loss from complete-case deletion.

## When NOT to use

- Input feature table is already fully imputed or contains no zero/missing values.
- Analysis goal requires explicit handling of absence-of-signal as a biological distinction (e.g., presence/absence in specific sample types where zeros are informative).
- Downstream workflow requires unimputed data for comparative purposes or validation against raw abundance distributions.

## Inputs

- feature table (TSV format) with monikers identifying table identity
- interpolation_ratio parameter (float, default 0.5)
- table_moniker (string identifier for the input feature table)

## Outputs

- imputed feature table (TSV format) with zeros and missing values replaced
- new_moniker (string identifier for the output table in feature_tables subdirectory)

## How to apply

Load the feature table identified by its table_moniker from the experiment's feature_tables subdirectory. For each feature independently, compute the minimum non-zero (non-missing) abundance value across all samples. Multiply that minimum by the interpolation_ratio parameter (default 0.5) to derive the imputation value. Replace all zero and missing entries in that feature's column with this imputation value. Save the resulting imputed table to a new moniker in the same feature_tables directory. The default ratio of 0.5 produces values equal to half the lowest observed signal for each feature, balancing between zero and measured values.

## Related tools

- **Python** (Language for implementing the imputation logic and feature table I/O operations) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Upstream tool that produces the initial feature table requiring imputation) — https://github.com/shuzhao-li/asari
- **metDataModel** (Data model library for standardized metabolomics feature table representation and I/O) — https://github.com/shuzhao-li-lab/metDataModel

## Evaluation signals

- Output table has no zero or missing values in any cell (except sample/feature identifiers).
- For each feature, all imputed values equal interpolation_ratio × (minimum non-zero value for that feature).
- Imputed values are smaller than the minimum observed non-zero abundance for each feature (i.e., they fill the gap between zero and real signal).
- Output table retains identical shape (rows, columns) as input; no features or samples are dropped.
- Output file is written to the feature_tables subdirectory with the specified new_moniker and standard TSV format.

## Limitations

- Assumes minimum non-zero value is a defensible proxy for instrumental detection limit; may perform poorly for features with extreme outliers or systematic platform-specific background noise.
- Fixed interpolation_ratio applies uniformly across all features; may not account for feature-specific or sample-type-specific differences in missingness mechanism.
- Does not account for zero-inflated or compositional constraints in metabolomics data; imputation may artificially increase total abundance per sample.
- Default ratio of 0.5 is a heuristic choice; optimal ratio depends on the prevalence and pattern of missing data in the original feature table.

## Evidence

- [other] The impute command fills missing values by calculating an imputation value as the interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default interpolation ratio of 0.5.: "The impute command fills missing values by calculating an imputation value as the interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default"
- [other] For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. Replace all zero and missing values in the feature table with the corresponding imputation values.: "For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. Replace all zero and missing values in the feature table with the corresponding imputation values."
- [other] Load the input feature table (identified by table_moniker) from the experiment directory. Identify the minimum non-zero value for each feature across all samples.: "Load the input feature table (identified by table_moniker) from the experiment directory. Identify the minimum non-zero value for each feature across all samples."
- [other] Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory.: "Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory."
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked,"
