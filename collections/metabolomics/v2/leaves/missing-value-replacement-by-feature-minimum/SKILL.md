---
name: missing-value-replacement-by-feature-minimum
description: Use when after loading a feature table into memory when the table contains
  zero or missing values that represent true signal loss (not genuine absence), and
  you need to impute them before normalization, batch correction, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - ThermoRawFileParser
  - Python
  - PCPFM (PythonCentricPipelineForMetabolomics)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# missing-value-replacement-by-feature-minimum

## Summary

Replace zero and missing values in a metabolomics feature table by calculating an imputation value as the interpolation_ratio parameter (default 0.5) multiplied by the minimum non-zero value observed for each feature. This strategy preserves the relative magnitude of features while avoiding artificial zeros that can distort downstream statistical analysis.

## When to use

Apply this skill after loading a feature table into memory when the table contains zero or missing values that represent true signal loss (not genuine absence), and you need to impute them before normalization, batch correction, or statistical analysis. This is typical after feature detection from LC-MS data but before quality control and annotation steps in the PCPFM pipeline.

## When NOT to use

- Input is already imputed or has no zero/missing values to replace
- Zeros represent true biological absence (e.g., a metabolite genuinely not detected in certain samples); imputation would introduce false signal
- Feature table is in raw count format from untargeted metabolomics where minimum-value-based imputation is not appropriate; consider other strategies (e.g., limit of detection, half minimum detection limit)

## Inputs

- Feature table (TSV or CSV format) with features as columns and samples as rows
- interpolation_ratio parameter (float, default 0.5)
- table_moniker (identifier for input table within experiment directory)

## Outputs

- Imputed feature table (same format as input, saved with new_moniker)
- Metadata recording interpolation_ratio and imputation strategy applied

## How to apply

Load the input feature table identified by a table moniker from the experiment's feature_tables directory. Identify the minimum non-zero value for each feature across all samples independently. For each feature, calculate the imputation value as interpolation_ratio × (feature's minimum non-zero value); use the default interpolation_ratio of 0.5 unless domain knowledge or data characteristics warrant adjustment. Replace all zero and missing (NA/NaN) values in that feature's column with its calculated imputation value. Save the imputed feature table to a new moniker in the experiment's feature_tables subdirectory, recording the interpolation_ratio used for reproducibility.

## Related tools

- **Python** (Language used to implement imputation logic and manipulate feature tables) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **PCPFM (PythonCentricPipelineForMetabolomics)** (Orchestrates imputation as a preprocessing step in the metabolomics workflow after feature table generation) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- All zero and missing (NA/NaN) values in the output table are replaced; no zeros or NaNs remain (except by intentional masking)
- For each feature, verify that imputed values equal exactly interpolation_ratio × (feature's minimum non-zero value from input)
- Non-zero, non-missing input values are unchanged in the output table (imputation does not alter existing signal)
- Output feature table has the same dimensions (rows, columns) as the input; no samples or features are dropped
- Metadata file or log records the interpolation_ratio used and the new_moniker assigned to the imputed table for downstream traceability

## Limitations

- Minimum-value-based imputation may underestimate missing values if the minimum non-zero value is an outlier or measurement artifact, potentially introducing bias in downstream statistical tests
- The default interpolation_ratio of 0.5 is a convention; its appropriateness depends on instrumental noise, sample preparation, and the proportion of missing values—no universal threshold is provided
- This method treats all features identically and does not account for metabolite-specific detection limits, ionization efficiency, or matrix suppression effects that may vary across chemical classes
- Imputation creates synthetic data points that can artificially reduce variance and inflate statistical power; users should document imputation strategy in methods and consider sensitivity analyses

## Evidence

- [other] The impute command fills missing values by calculating an imputation value as the interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default interpolation ratio of 0.5.: "imputation value as interpolation_ratio parameter multiplied by the minimum non-zero value observed for each feature, with a default interpolation ratio of 0.5"
- [other] For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. 4. Replace all zero and missing values in the feature table with the corresponding imputation values.: "For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. Replace all zero and missing values in the feature table with the corresponding imputation values."
- [other] Load the input feature table (identified by table_moniker) from the experiment directory. 2. Identify the minimum non-zero value for each feature across all samples.: "Load the input feature table (identified by table_moniker) from the experiment directory. Identify the minimum non-zero value for each feature across all samples."
- [other] Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory.: "Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory."
- [readme] perform quality control
- Data normalization and batch correction: "perform quality control
- Data normalization and batch correction"
