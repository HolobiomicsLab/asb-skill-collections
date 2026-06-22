---
name: missing-pattern-generation-validation
description: Use when you have a complete metabolomics data matrix (simulated or real abundance table) and need to create reproducible, controlled MNAR scenarios for evaluating imputation algorithm performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GSimp_evaluation.R
  - impute::impute.QRILC
  - R package imputeLCMD
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
evidence_spans:
- '**GSimp.R** contains the core functions for GSimp'
- GSimp.R contains the core functions for GSimp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gsimp_cq
    doi: 10.1371/journal.pcbi.1005973
    title: GSimp
  dedup_kept_from: coll_gsimp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1005973
  all_source_dois:
  - 10.1371/journal.pcbi.1005973
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# missing-pattern-generation-validation

## Summary

Generate synthetic missing-not-at-random (MNAR) patterns in metabolomics abundance matrices by applying left-censoring thresholds and feature-dependent missingness mechanisms, then validate the resulting data against expected missingness distributions and coverage statistics. This skill enables benchmarking of imputation methods on realistic missing-data scenarios.

## When to use

Use this skill when you have a complete metabolomics data matrix (simulated or real abundance table) and need to create reproducible, controlled MNAR scenarios for evaluating imputation algorithm performance. Specifically, apply it when you want to simulate left-censored observations due to detection limits (LOD/LOQ), and must test whether imputation methods recover true values before deploying them on real incomplete datasets.

## When NOT to use

- Input data already contains real missing values—pre-process or separate real from synthetic missingness first to avoid confounding
- No known ground truth exists for the data; MNAR validation requires comparison to original complete values, so use only on simulated or artificially censored data
- Missingness mechanism is known to be MCAR or MAR with no left-censoring component; apply MCAR/MAR generation instead

## Inputs

- complete metabolomics abundance matrix (data.frame or matrix in R)
- detection limit specification (percentile value, absolute threshold, or vector of feature-specific thresholds)
- missing-data mechanism definition (MCAR, feature-dependent missingness rates, or custom specification)
- optional: seed value for reproducible random selection

## Outputs

- censored data matrix with NA values replacing sub-threshold observations
- metadata object documenting: total missing count, per-feature missingness rates, per-sample missingness rates, features affected, samples affected, threshold used, mechanism applied
- missingness position matrix (row/column indices of all NA entries)

## How to apply

Load a complete metabolomics abundance table into R and define left-censoring threshold parameters (detection limit as a percentile, e.g., minimum observed value, or an absolute value). Randomly select features and samples according to a specified missing-data mechanism—either completely-at-random or feature-dependent (where missingness rates vary by metabolite). Replace all values below the detection threshold with NA to simulate left-censored observations. Return both the censored data matrix and metadata documenting the missingness pattern (total count, per-feature and per-sample rates), the threshold used, and which features/samples were affected. Validate by comparing the observed missingness distribution against the target mechanism and checking that all censored values fall below the specified threshold.

## Related tools

- **GSimp_evaluation.R** (R module containing MNAR generation and evaluation functions that implement the missing-pattern generation and validation workflow) — https://github.com/WandeRum/GSimp
- **impute::impute.QRILC** (Quantile Regression Imputation of Left-Censored data; used for initialization and baseline comparison after MNAR generation)
- **R package imputeLCMD** (Provides QRILC imputation wrapper for post-generation evaluation)

## Examples

```
source('GSimp_evaluation.R'); NA_pos <- which(is.na(untargeted_data), arr.ind = T); mnar_data <- untargeted_data; mnar_data[sample(nrow(mnar_data), size=nrow(mnar_data)*0.2), ] <- NA; missmap(mnar_data, col=c('black', 'grey'), legend=FALSE)
```

## Evaluation signals

- Missingness count matches expected value: total NAs = (number_of_selected_samples × number_of_selected_features) when applied uniformly, or sum of per-feature rates when feature-dependent
- All censored positions fall below threshold: verify max(censored_values_before_NA) ≤ detection_limit for each feature
- Metadata missingness rates match observed rates: count NAs per feature and per sample; compare to reported rates ±0.5%
- Reproducibility: same seed + parameters produce identical NA positions and censored values across runs
- No loss of intact data: non-missing observations remain unchanged; only values below threshold are replaced with NA

## Limitations

- Assumes detection limits are uniform per feature or can be specified independently; real LOD/LOQ variation within assay batches not modeled
- Left-censoring mechanism only; does not simulate right-censoring or mixed censoring mechanisms
- Threshold specification as percentile may yield different absolute limits when applied to metabolites with different dynamic ranges; verify threshold values post-generation
- MNAR generation assumes missingness depends only on unobserved (true) values and feature identity; does not model sample-level effects or time-dependent missingness
- Evaluation relies on availability of ground-truth complete data; not applicable to real-world datasets with genuine missing values

## Evidence

- [other] GSimp_evaluation.R contains MNAR generation and evaluation functions that form part of the missing value imputation evaluation pipeline, enabling the creation of missing-not-at-random data for benchmarking imputation methods.: "GSimp_evaluation.R contains MNAR generation and evaluation functions that form part of the missing value imputation evaluation pipeline, enabling the creation of missing-not-at-random data for"
- [other] Load a complete metabolomics data matrix and define left-censoring threshold parameters, randomly select features and samples according to a specified missing-data mechanism, replace values below the detection threshold with NA to simulate left-censored observations.: "Load a complete metabolomics data matrix (e.g., simulated or real abundance table) into R. 2. Define left-censoring threshold parameters (detection limit as a percentile or absolute value). 3."
- [other] Return the censored data matrix and metadata (missingness pattern, threshold used, features/samples affected) for downstream imputation and evaluation.: "Return the censored data matrix and metadata (missingness pattern, threshold used, features/samples affected) for downstream imputation and evaluation."
- [readme] GSimp provides data pre-processing, simulated data generation, MNAR generation, wrapper functions for different imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods: "GSimp provides data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and"
- [readme] The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD.: "The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD."
