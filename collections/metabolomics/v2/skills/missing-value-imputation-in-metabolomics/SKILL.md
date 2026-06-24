---
name: missing-value-imputation-in-metabolomics
description: Use when after feature extraction and quality control filtering (blank
  masking, sample dropping, normalization) have been applied, but before statistical
  analysis or machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- pre-annotation to group featues to empirical compounds (khipu)
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

# Missing-value imputation in metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Impute missing or zero-intensity feature values in LC-MS metabolomics feature tables by computing multiples of the per-feature minimum value, enabling complete feature matrices for downstream statistical analysis without artificial feature removal.

## When to use

After feature extraction and quality control filtering (blank masking, sample dropping, normalization) have been applied, but before statistical analysis or machine learning. The feature table contains sparse zeros or missing values that would otherwise bias downstream analysis or violate distributional assumptions. Use this skill when you need to retain features with incomplete coverage across samples rather than discarding them.

## When NOT to use

- Input feature table is already complete with no missing values or after features with insufficient coverage have been dropped.
- Downstream analysis explicitly requires original missing-data patterns (e.g., missingness mechanism analysis or data-quality audits).
- Features are categorical or non-intensity-based (e.g., binary presence/absence); imputation is designed for continuous intensity scales.

## Inputs

- Feature table (TSV or CSV format) with features as rows and samples as columns, containing intensity values or zero/NaN for missing data
- Feature-level metadata (minimum detected intensity per feature, optional)

## Outputs

- Imputed feature table (TSV or CSV) with all missing/zero values replaced by interpolated values, ready for statistical analysis

## How to apply

For each feature independently, compute the minimum detected intensity value across all samples where the feature is present. Replace zero or missing values with a fractional multiple (default 0.5×) of that per-feature minimum. This approach preserves the relative scale of low-abundance features, avoids unrealistic imputation to zero, and respects the feature-specific noise floor. The rationale is that missing values in LC-MS often reflect true near-zero intensity (i.e., below the limit of detection) rather than incomplete data capture, so a small positive value proportional to that feature's minimum observed intensity provides a defensible null model without introducing artificial signal.

## Related tools

- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Command-line orchestration tool that exposes the impute operation via 'pcpfm impute' subcommand with configurable interpolation ratio parameter) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Language and ecosystem for implementing feature-wise minimum computation and vectorized replacement operations)

## Examples

```
pcpfm impute --input_table feature_table.tsv --output_table imputed_table.tsv --ratio 0.5
```

## Evaluation signals

- All zero and NaN values in the input feature table are replaced with positive, non-zero values in the output.
- For each feature, imputed values are ≤ the observed minimum intensity for that feature (when using ratio < 1.0).
- The relative ordering and magnitude of non-missing values are preserved; no original intensities are modified.
- Output feature table has no NaN or missing entries and is suitable for downstream statistical analysis without further value-filling.
- Imputed values respect the per-feature scale: features with higher minimum intensities receive proportionally higher imputed values.

## Limitations

- Default interpolation ratio (0.5×) is a heuristic choice; sensitivity to this parameter and the impact on downstream statistical power are not formally evaluated in the paper.
- The method assumes missing values represent true absence or detection below the instrument limit; it cannot distinguish between true missing data and biological absence.
- For very sparse features (detected in only one or few samples), the per-feature minimum may be unrepresentatively low or high, leading to biased imputation.
- No explicit guidance is provided for handling features detected in zero samples (i.e., entirely absent from the matrix); the method requires at least one non-missing value per feature.

## Evidence

- [other] Impute missing values using pcpfm impute with interpolation ratio (default 0.5×) applied to minimum per-feature value.: "Impute missing values using pcpfm impute with interpolation ratio (default 0.5×) applied to minimum per-feature value."
- [other] missing value imputation as multiples of minimum feature values: "missing value imputation as multiples of minimum feature values"
