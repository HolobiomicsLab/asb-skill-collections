---
name: sample-replicate-pair-assessment
description: Use when you have high-throughput replicate measurements (e.g., mass
  spectrometry metabolomics) on biological replicates and need to identify which sample
  pairs exhibit reproducible feature signals across a threshold (typically 75% reproducibility).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - devtools
  - Bioconductor
  - marr
  - MarrPlotSamplepairs()
  techniques:
  - mass-spectrometry
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

# sample-replicate-pair-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess reproducibility of sample pairs in high-dimensional replicate experiments by computing the percentage of reproducible features per sample pair and ranking sample pairs by reproducibility rank. This skill measures technical and biological consistency across replicate measurements using the Maximum Rank Reproducibility (marr) approach.

## When to use

Apply this skill when you have high-throughput replicate measurements (e.g., mass spectrometry metabolomics) on biological replicates and need to identify which sample pairs exhibit reproducible feature signals across a threshold (typically 75% reproducibility). Use it to validate technical consistency before downstream analysis, to flag problematic replicate pairs, or to filter data for robust downstream modeling.

## When NOT to use

- Input data lacks technical or biological replicates—marr requires pairwise comparisons across replicate experiments.
- Feature counts are very low (< 10 features)—reproducibility ranking becomes unstable with sparse observations.
- Data is already quality-filtered or pre-processed for reproducibility—applying marr twice risks circular filtering.

## Inputs

- SummarizedExperiment object with assay of metabolite/feature abundances (rows) × biological replicates (columns)
- matrix or data frame with observations on rows, samples on columns
- pSamplepairs threshold (0–1; default 0.75)
- pFeatures threshold (0–1; default 0.75)
- alpha significance level for FDR control (default 0.05)

## Outputs

- MarrSamplepairs table: percent of reproducible features per sample pair (unfiltered)
- MarrSamplepairsfiltered table: sample pairs with reproducible feature percentage ≥ pFeatures threshold
- ranked sample pairs by reproducibility reproducibility metric
- MarrFeatures table: percent of reproducible sample pairs per feature (complementary output)

## How to apply

Execute the Marr() function on a SummarizedExperiment or matrix with observations (metabolites/genes) as rows and samples as columns, specifying pSamplepairs and pFeatures thresholds (default 0.75 each) and an alpha level for FDR control (default 0.05). The function computes the percentage of reproducible features (signals) for each pairwise combination of replicate experiments. Extract the MarrSamplepairs output table, which reports the percent-reproducible features per sample pair ranked by reproducibility. Apply the pFeatures threshold to filter sample pairs: retain only pairs where the percentage of reproducible features across all measured metabolites exceeds the threshold. Validate that filtered output (MarrSamplepairsfiltered) is non-empty and contains expected columns for reproducibility metrics and rankings.

## Related tools

- **marr** (Computes reproducibility rankings and filters sample pairs and features via the Marr() function and accessor methods MarrSamplepairs(), MarrSamplepairsfiltered().) — https://github.com/Ghoshlab/marr
- **devtools** (Installs marr package from GitHub using devtools::install_github().) — https://github.com/r-lib/devtools
- **R** (Execution environment for marr and data manipulation.)
- **Bioconductor** (Provides SummarizedExperiment class and alternative installation route for marr.)
- **MarrPlotSamplepairs()** (Visualization function to plot percent reproducible features per sample pair.) — https://github.com/Ghoshlab/marr

## Examples

```
library(marr); MarrOutput <- Marr(object = dataSE, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); samplePairReproducibility <- MarrSamplepairs(MarrOutput); filteredPairs <- MarrSamplepairsfiltered(MarrOutput); MarrPlotSamplepairs(MarrOutput)
```

## Evaluation signals

- MarrSamplepairsfiltered table is non-empty and contains ≥ 1 sample pair meeting the pFeatures ≥ 0.75 threshold.
- All rows in MarrSamplepairs correspond to unique pairwise combinations of the input biological replicates (expected count = n choose 2 for n samples).
- Percent-reproducible-features column contains values in range [0, 100] or [0, 1]; verify no NaN or Inf values.
- MarrSamplepairs and MarrSamplepairsfiltered are sorted or rankable by reproducibility metric in descending order (highest reproducibility first).
- MarrPlotSamplepairs() visualization renders without error and shows monotonic or expected distribution of reproducibility percentages across sample pairs.

## Limitations

- Reproducibility assessment is sensitive to missing data; pre-processing with imputation (e.g., Bayesian PCA) and filtering (e.g., removal of metabolites missing >80% of samples) is recommended prior to Marr().
- Thresholds pSamplepairs, pFeatures, and alpha are user-specified; results are sensitive to threshold choice and no automatic selection criterion is provided by the method.
- marr assesses reproducibility of ranks, not absolute abundance values; it does not account for systematic batch effects or drift in instrument calibration across runs.
- Method assumes pairwise independence and may not capture complex replicate dependencies (e.g., temporal autocorrelation across runs).

## Evidence

- [intro] assign a sample pair (i,i′) to be reproducible if percentage of reproducible signals (100c_m%) across all features exceeds threshold: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [intro] pFeatures threshold used to assign sample pair reproducibility based on feature reproducibility output: "pFeatures (Optional) a threshold value that lies between 0 and 1, used to assign a sample pair to be reproducible based on the reproducibility output of the features per sample pair. Default is 0.75."
- [readme] Accessor method to extract percent reproducible features per sample pair: "MarrSamplepairs(MarrOutput) # extract the distribution of percent reproducible features (column-wise) per sample pair"
- [readme] Filtered sample pairs meeting reproducibility threshold: "MarrSamplepairsfiltered(MarrOutput) # extract the percent of reproducible features based on a threshold value"
- [readme] Visualization of sample pair reproducibility: "The percent reproducible features per sample pair can be directly plotted using the `MarrPlotSamplepairs()` function."
