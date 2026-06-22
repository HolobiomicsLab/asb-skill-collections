---
name: marr-output-object-manipulation
description: Use when when you have a Marr() output object containing reproducibility statistics computed across replicate experiments and need to reduce dimensionality by retaining only features or sample pairs that meet reproducibility criteria (percentage of reproducible signals exceeding feature-level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - marr
  - Bioconductor
  - devtools
  - BiocManager
  - SummarizedExperiment
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- devtools::install_github("Ghoshlab/marr")
- marr (Maximum Rank Reproducibility) is a nonparametric approach that detects reproducible signals using a maximal rank statistic for high-dimensional biological data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# marr-output-object-manipulation

## Summary

Extract, filter, and subset high-dimensional biological replicate data using the MarrFilterData() function to isolate reproducible features, reproducible sample pairs, or both simultaneously based on reproducibility thresholds. This skill enables targeted downstream analysis by removing non-reproducible signals from Marr() output objects.

## When to use

When you have a Marr() output object containing reproducibility statistics computed across replicate experiments and need to reduce dimensionality by retaining only features or sample pairs that meet reproducibility criteria (percentage of reproducible signals exceeding feature-level threshold 100*c_s% or sample-pair-level threshold 100*c_m%), or when you need to apply both filters simultaneously to obtain a doubly-filtered high-confidence subset for visualization or publication.

## When NOT to use

- Input is a raw data matrix or SummarizedExperiment that has not been processed through Marr() — use Marr() first to compute reproducibility statistics.
- You require unfiltered reproducibility distributions for exploratory analysis or method validation — use accessor methods on the original Marr() object without calling MarrFilterData().
- Your experiment has only a single replicate or lacks sufficient pairwise replicates to compute meaningful reproducibility scores — Marr() requires multiple replicate experiments.

## Inputs

- Marr() output object (S4 object with reproducibility statistics slots)
- filtering mode parameter: 'features', 'samplePairs', or 'both'
- optional: feature-level reproducibility threshold (c_s, default 0.75)
- optional: sample-pair-level reproducibility threshold (c_m, default 0.75)

## Outputs

- Feature-filtered SummarizedExperiment (by='features')
- Sample-pair-filtered SummarizedExperiment (by='samplePairs')
- Doubly-filtered SummarizedExperiment (by='both')
- Extracted slot vectors via accessor methods (MarrSamplepairs, MarrFeatures, etc.)
- Serialized filtered data objects (.rds or equivalent format)

## How to apply

Load the Marr() output object containing reproducibility statistics. Apply MarrFilterData() with by='features' to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level reproducibility threshold (100*c_s%), producing a feature-filtered SummarizedExperiment. Alternatively, apply by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing a sample-pair-filtered subset. For maximum stringency, apply by='both' to apply both filtering criteria simultaneously. Extract individual slots from the filtered objects using accessor methods (MarrSamplepairs(), MarrFeatures(), MarrSamplepairsfiltered(), MarrFeaturesfiltered()) and serialize the resulting subsets for downstream analysis or visualization with MarrPlotFeatures() or MarrPlotSamplepairs().

## Related tools

- **marr** (R/Bioconductor package containing Marr() function to compute reproducibility statistics and MarrFilterData() to filter output; required for this skill) — https://github.com/Ghoshlab/marr
- **devtools** (R package utility used to install the latest development version of marr from GitHub repository) — https://github.com/r-lib/devtools
- **BiocManager** (R package for installing marr and other Bioconductor packages)
- **SummarizedExperiment** (Bioconductor class used to store filtered output data objects with assay, row, and column metadata)

## Examples

```
MarrOutput <- Marr(object = dataSE, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); filtered_features <- MarrFilterData(MarrOutput, by='features'); filtered_pairs <- MarrFilterData(MarrOutput, by='samplePairs'); doubly_filtered <- MarrFilterData(MarrOutput, by='both')
```

## Evaluation signals

- Verify output SummarizedExperiment has reduced dimensionality compared to input Marr() object (fewer features or sample pairs retained).
- Check that all retained features in by='features' output have percentage reproducible signals ≥ 100*c_s% when inspected via MarrFeaturesfiltered().
- Check that all retained sample pairs in by='samplePairs' output have percentage reproducible signals ≥ 100*c_m% when inspected via MarrSamplepairsfiltered().
- Verify by='both' output is a strict subset of both by='features' and by='samplePairs' outputs (intersection, not union).
- Confirm plots generated by MarrPlotFeatures() and MarrPlotSamplepairs() show only the filtered signals without missing data artifacts.

## Limitations

- MarrFilterData() thresholds (c_s, c_m) are user-specified with defaults of 0.75; no automated threshold selection method is provided in the article.
- Filtering may be too stringent if thresholds are set too high (c_s, c_m > 0.9), resulting in empty or near-empty outputs; conversely, low thresholds retain too much noise.
- The method assumes independence of reproducibility between features and sample pairs; strong feature-sample correlations may violate this assumption.
- Reproducibility assessment depends on experimental design and replicate structure; insufficient replicate samples or unbalanced designs may yield unstable reproducibility estimates.

## Evidence

- [other] MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering criteria simultaneously.: "MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering"
- [other] Apply MarrFilterData() with by='features' to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level threshold (100*c_s%), producing a feature-filtered subset.: "Apply MarrFilterData() with by='features' to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level threshold (100*c_s%), producing a feature-filtered"
- [other] Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing a sample-pair-filtered subset.: "Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing"
- [readme] Individual slots can be extracted using accessor methods: MarrSamplepairs() extract the distribution of percent reproducible features (column-wise) per sample pair; MarrFeatures() extract the distribution of percent reproducible sample pairs (row-wise) per feature.: "Individual slots can be extracted using accessor methods: MarrSamplepairs() extract the distribution of percent reproducible features (column-wise) per sample pair; MarrFeatures() extract the"
- [readme] The main function in the **marr** package is `Marr()`. The `Marr()` function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns.: "The main function in the **marr** package is `Marr()`. The `Marr()` function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with"
