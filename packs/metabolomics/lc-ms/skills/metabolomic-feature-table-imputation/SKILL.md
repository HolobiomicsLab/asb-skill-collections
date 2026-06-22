---
name: metabolomic-feature-table-imputation
description: Use when after feature detection and peak alignment have produced a feature table with zero or missing values across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - Python
  - pycombat
  - Asari
  - PCPFM (PythonCentricPipelineForMetabolomics)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- Batch correction is performed using pycombat.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-feature-table-imputation

## Summary

Replace zero and missing values in LC-MS metabolomics feature tables using a minimum-value-based interpolation strategy, where each missing/zero entry is filled with a feature-specific imputation value calculated as the interpolation_ratio parameter multiplied by that feature's minimum non-zero intensity. This is a critical preprocessing step that prevents loss of samples and features while stabilizing downstream statistical analyses.

## When to use

Apply this skill after feature detection and peak alignment have produced a feature table with zero or missing values across samples. The skill is necessary when (1) the feature table contains non-detects or intentional zero-filling, (2) you intend to retain all samples and features for downstream analysis rather than filter them out, and (3) you need to avoid inflated variance from zero values while preserving feature-wise intensity relationships.

## When NOT to use

- Input is already a feature table with no zero or missing values (imputation is unnecessary and will artificially inflate all feature intensities by the interpolation_ratio).
- All non-zero values for a feature are identical or there is no measurable minimum; imputation by ratio becomes meaningless or produces values identical to the observed minimum.
- The research goal explicitly requires filtering out samples or features with missingness rather than imputing them (e.g., strict completeness criterion).

## Inputs

- feature table (TSV or matrix format) with samples as rows and metabolomic features (m/z–RT pairs or identifiers) as columns
- table_moniker (string identifier for input table location within experiment directory)
- interpolation_ratio parameter (float, default 0.5)
- sample metadata (optional, if batch-specific imputation is desired)

## Outputs

- imputed feature table (TSV or matrix format, same dimensions as input)
- new_moniker (string identifier for output table saved to feature_tables subdirectory)
- imputation summary or log (feature-wise minimum values and imputation thresholds applied)

## How to apply

Load the input feature table (identified by table_moniker) from the experiment's feature_tables subdirectory. For each feature in the table, identify its minimum non-zero (strictly positive) intensity value across all samples. Calculate the imputation value for that feature as interpolation_ratio × minimum_non_zero_value; the default interpolation_ratio is 0.5, yielding a conservative imputation at 50% of the minimum observed intensity. Replace all zero and missing (NaN/null) entries in that feature's column with the computed imputation value. This ratio-based strategy is grounded in the principle that non-detects likely fall below the quantitative limit but remain chemically present at trace levels. Save the imputed feature table to a new moniker in the experiment's feature_tables subdirectory for downstream use (e.g., normalization, batch correction, or statistical testing).

## Related tools

- **Python** (Implement imputation algorithm: load feature table, compute per-feature minima, apply interpolation_ratio multiplication, and replace zeros/NaNs)
- **ThermoRawFileParser** (Upstream raw-file conversion (produces mzML input for feature detection; not directly involved in imputation))
- **Asari** (Upstream feature detection and table generation; produces the raw feature table that is input to imputation) — https://github.com/shuzhao-li/asari
- **PCPFM (PythonCentricPipelineForMetabolomics)** (Pipeline orchestration; integrates imputation as a standard preprocessing step within the full workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- Output feature table has identical sample count and feature count as input table (no rows or columns removed).
- All zero and missing (NaN) entries in input are replaced; verify no zeros/NaNs remain in output.
- Imputed values for each feature are exactly equal to (interpolation_ratio × min_nonzero_value) for that feature; spot-check 5–10 features by manual calculation.
- Imputed values are strictly less than the minimum non-zero value observed for each feature (lower bound check).
- Distribution of imputed intensities is unimodal and concentrated near the lower end of the feature's intensity range, confirming conservative filling rather than artificial inflation.

## Limitations

- If a feature is entirely zero or missing across all samples, no minimum non-zero value exists; imputation cannot proceed for that feature without a fallback strategy (e.g., use a global minimum or exclude the feature).
- The choice of interpolation_ratio (default 0.5) is heuristic and data-dependent; it may be too high for features with very low detection rates or too low for robust features, potentially affecting downstream statistical power or false-discovery rates.
- Imputation assumes that zero/missing values are non-detects and not true biological absences; if some zeros represent genuine absence, imputation introduces false positives.
- The method does not account for instrumental sensitivity differences or normalization; imputation should typically be followed by normalization or batch correction to avoid systematic bias.

## Evidence

- [other] The impute command fills missing values by calculating an imputation value as the interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default interpolation ratio of 0.5.: "impute command fills missing values by calculating an imputation value as the interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default"
- [other] For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. Replace all zero and missing values in the feature table with the corresponding imputation values.: "For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. Replace all zero and missing values in the feature table with the corresponding imputation values."
- [other] Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory.: "Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory."
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.): "Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.)"
- [readme] data normalization and batch correction: "The pipeline can perform quality control, data normalization and batch correction"
