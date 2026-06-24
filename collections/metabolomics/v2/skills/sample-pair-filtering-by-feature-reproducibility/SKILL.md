---
name: sample-pair-filtering-by-feature-reproducibility
description: Use when when you have a Marr() output object containing reproducibility
  statistics from replicate experiments, and your goal is to retain only those sample
  pairs (i,i') where reproducibility is robust across the majority of features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Bioconductor
  - marr
  - devtools
  license_tier: restricted
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-pair-filtering-by-feature-reproducibility

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter high-dimensional biological replicate data to retain only sample pairs where the percentage of reproducible signals across all features exceeds a user-defined threshold. This skill applies the MarrFilterData() function with by='samplePairs' mode to subset reproducible experimental pairs based on feature-level reproducibility consensus.

## When to use

When you have a Marr() output object containing reproducibility statistics from replicate experiments, and your goal is to retain only those sample pairs (i,i') where reproducibility is robust across the majority of features. Use this when you want to identify biologically or technically reliable pairwise replicates before downstream analysis, particularly when feature-level variability makes individual feature filtering insufficient.

## When NOT to use

- Input is already a single-replicate experiment or lacks replicate structure — sample pairs cannot be defined without replicates.
- Goal is to filter features (reproducible metabolites or genes) rather than sample pairs — use by='features' mode instead.
- Marr() object has not yet been computed; raw data matrix alone is insufficient without reproducibility statistics.

## Inputs

- Marr() output object (S4 class containing reproducibility statistics)
- SummarizedExperiment or matrix with observations (rows) × samples (columns)
- numeric threshold pSamplepairs (0–1; default 0.75) defining minimum reproducible signal fraction per sample pair

## Outputs

- Filtered SummarizedExperiment or matrix retaining only reproducible sample pairs
- Accessor MarrSamplepairsfiltered(MarrOutput) extracting percent reproducible features per retained sample pair
- Reduced high-dimensional dataset suitable for downstream statistical or biological analysis

## How to apply

First, compute reproducibility statistics on your high-dimensional dataset (rows = features, columns = samples across replicates) using Marr(object = dataSE, pSamplepairs=c_m, pFeatures=..., alpha=0.05), which generates a distribution of the percentage of reproducible signals across all features for each sample pair. Then apply MarrFilterData(MarrOutput, by='samplePairs') to retain only sample pairs where the percentage of reproducible signals (100*c_m%) meets or exceeds your sample-pair-level threshold (default pSamplepairs=0.75, meaning ≥75% of features must show reproducible signals for that pair). The filtering logic assigns a sample pair (i,i') as reproducible if a certain percentage of signals (100*c_m%) are reproducible across all features. Export the filtered subset for subsequent analysis, ensuring you document the c_m threshold used to enable reproducibility traceability.

## Related tools

- **marr** (Computes reproducibility statistics and provides MarrFilterData() function for sample-pair filtering by feature-level reproducibility) — https://github.com/Ghoshlab/marr
- **R** (Language and environment for executing Marr() and MarrFilterData() workflows)
- **Bioconductor** (Provides SummarizedExperiment container class for input/output high-dimensional data)
- **devtools** (R package manager for installing marr from GitHub) — https://github.com/r-lib/devtools

## Examples

```
MarrOutput <- Marr(object = dataSE, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); filtered_data <- MarrFilterData(MarrOutput, by='samplePairs')
```

## Evaluation signals

- Verify that the filtered dataset contains fewer sample pairs than the input Marr() object, with exactly those pairs meeting the 100*c_m% reproducibility threshold across all features.
- Check MarrPlotSamplepairs(filtered_output) visualizes only retained sample pairs with reproducible signal percentages ≥ threshold; excluded pairs should not appear.
- Confirm the number of features (rows) remains unchanged; only columns (sample pairs) are reduced.
- Validate that accessor MarrSamplepairsfiltered(filtered_output) returns a numeric vector with length equal to the count of retained sample pairs, all values ≥ threshold.
- Cross-check reproducibility percentages against the original Marr() output to ensure no pairs below threshold are retained and no above-threshold pairs are excluded.

## Limitations

- Sample-pair filtering depends critically on the pSamplepairs threshold (c_m); misaligned thresholds may discard valid replicates or retain noisy pairs. Threshold selection should align with downstream analysis sensitivity requirements.
- Filtering requires sufficient feature coverage per sample pair; if most features have missing values or low reproducibility signals, few or no sample pairs may survive filtering.
- The method is nonparametric and rank-based; it may not detect subtle biological differences that parametric tests would capture, particularly in small replicate experiments.
- Does not account for feature-specific biology; a globally reproducible sample pair (high signal across many features) may still contain outlier features unsuitable for specific biological questions.

## Evidence

- [intro] we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features: "we assign a sample pair (i,i') to be reproducible if a certain percentage signals (100*c_m%) are reproducible across all features"
- [other] MarrFilterData() accepts three filtering modes: by='samplePairs' to retain only reproducible sample pairs: "MarrFilterData() accepts three filtering modes: by='samplePairs' to retain only reproducible sample pairs"
- [other] Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing a sample-pair-filtered subset.: "Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing"
- [readme] pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75.: "pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75."
- [readme] MarrSamplepairsfiltered(MarrOutput) extract the percent of reproducible features based on a threshold value: "MarrSamplepairsfiltered(MarrOutput) extract the percent of reproducible features based on a threshold value"
