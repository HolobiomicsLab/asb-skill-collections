---
name: reproducibility-signal-detection-nonparametric
description: Use when when you have high-dimensional replicate experimental data (e.g.,
  metabolomics, proteomics, genomics assays) where technical or biological variability
  threatens reproducibility, and you need to distinguish genuine reproducible signals
  from noise without assuming normality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Bioconductor
  - marr
  - devtools
  - BiocManager
  - SummarizedExperiment
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

# reproducibility-signal-detection-nonparametric

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess reproducibility of high-dimensional biological signals across replicate experiments using rank-based nonparametric methods, identifying reproducible features and sample pairs without distributional assumptions. This skill detects which metabolites, genes, or other features show consistent ranking patterns across biological or technical replicates, and which sample pairs exhibit reproducible signals across the feature space.

## When to use

When you have high-dimensional replicate experimental data (e.g., metabolomics, proteomics, genomics assays) where technical or biological variability threatens reproducibility, and you need to distinguish genuine reproducible signals from noise without assuming normality. Apply this skill when your research question requires quantifying reproducibility at both the feature level (which metabolites rank consistently?) and sample-pair level (which replicate comparisons are trustworthy?), rather than testing a single global hypothesis.

## When NOT to use

- Input data lacks replicate measurements; reproducibility assessment requires multiple independent replicates across which rank order can be compared.
- Data is already normalized or preprocessed such that rank structure is destroyed or made artificially uniform.
- Your primary goal is hypothesis testing on a single global mean or variance, rather than identifying reproducible subsets of features or sample pairs.

## Inputs

- SummarizedExperiment object or matrix/data frame with features (rows) × samples (columns)
- Replicate experimental data (biological or technical replicates required)
- Threshold parameter: pFeatures (numeric, 0–1; default 0.75)
- Threshold parameter: pSamplepairs (numeric, 0–1; default 0.75)
- FDR control parameter: alpha (numeric, default 0.05)

## Outputs

- Marr output object containing reproducibility statistics per feature and per sample pair
- Distribution of percent reproducible features per sample pair (column-wise)
- Distribution of percent reproducible sample pairs per feature (row-wise)
- Binary/filtered reproducibility calls for features and sample pairs
- Visualization plots (MarrPlotFeatures(), MarrPlotSamplepairs())

## How to apply

Load your high-dimensional data (features as rows, samples as columns) into a SummarizedExperiment or matrix object and pass it to the Marr() function, which computes pairwise rank correlations between all replicate sample pairs for each feature. The function outputs two distributions: (1) the percentage of reproducible pairwise signals per feature (row-wise), and (2) the percentage of reproducible features per sample pair (column-wise). Set thresholds pFeatures (default 0.75) and pSamplepairs (default 0.75) to define what percentage of signals must be reproducible to classify a feature or sample pair as reproducible. The nonparametric rank-based approach is robust to outliers and does not require normality assumptions, making it suitable for count data, heteroscedastic measurements, and non-Gaussian distributions common in metabolomics and mass spectrometry. Extract reproducibility metrics using accessor functions (MarrFeatures(), MarrSamplepairs()) and visualize distributions with MarrPlotFeatures() and MarrPlotSamplepairs() to identify reproducible signal subsets.

## Related tools

- **marr** (Core R/Bioconductor package implementing the Maximum Rank Reproducibility method; primary function Marr() computes reproducibility statistics; accessor and plotting functions extract and visualize results) — https://github.com/Ghoshlab/marr
- **devtools** (Package installation and development utility; used to install marr from GitHub via devtools::install_github()) — https://github.com/r-lib/devtools
- **BiocManager** (Bioconductor package manager; alternative installation method for marr from Bioconductor)
- **SummarizedExperiment** (Data container class accepted as input to Marr(); supports assay matrices with feature and sample metadata)

## Examples

```
library(marr)
MarrOutput <- Marr(object = dataSE, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05)
MarrPlotFeatures(MarrOutput)
MarrPlotSamplepairs(MarrOutput)
```

## Evaluation signals

- Reproducibility distributions (percent reproducible signals per feature/sample pair) should show clear separation between reproducible and non-reproducible subsets; bimodal or right-skewed histograms indicate signal stratification.
- MarrPlotFeatures() and MarrPlotSamplepairs() output should reveal distinct peaks or inflection points at or above threshold values (default 0.75), confirming meaningful reproducibility calls.
- Filtered data subsets (via MarrFilterData with by='features', by='samplePairs', or by='both') should have reduced dimensionality (fewer features or sample pairs retained) while preserving rank structure and pairwise consistency.
- Accessor functions (MarrFeaturesfiltered(), MarrSamplepairsfiltered()) should return numeric vectors of length ≤ input dimensions, with values in [0,1] representing percent reproducibility.
- Reproducibility statistics should be robust across replication: repeated runs on the same data with identical parameters should yield identical rank orderings and reproducibility thresholds.

## Limitations

- Method requires at least 2 replicate samples (preferably ≥3) to compute pairwise rank correlations; single-replicate or unreplicated designs are not supported.
- Reproducibility assessment is sensitive to choice of thresholds (pFeatures, pSamplepairs); values must be calibrated per study and may require pilot data or sensitivity analysis to avoid over- or under-filtering.
- Rank-based approach discards magnitude information; features with reproducible rank order but vastly different scales or absolute levels may pass reproducibility filters despite biological unreliability.
- High-dimensional datasets with very large feature counts may exhibit conservative reproducibility calls due to multiple testing burden; FDR control (alpha parameter) should be adjusted accordingly.
- Method does not account for confounding batch effects or systematic technical drift across replicates; pre-processing (normalization, batch correction) should precede Marr() analysis.

## Evidence

- [readme] marr: An R/Bioconductor package for Maximum Rank Reproducibility (marr) for high-dimensional biological data.: "marr: An R/Bioconductor package for Maximum Rank Reproducibility (marr) for high-dimensional biological data."
- [readme] marr measures the reproducibility of features per sample pair and sample pairs per feature in high-dimensional biological replicate experiments.: "marr measures the reproducibility of features per sample pair and sample pairs per feature in high-dimensional biological replicate experiments."
- [intro] We assign feature m to be reproducible if a certain percentage signals (100c_s%) are reproducible for pairwise combinations of replicate experiments: "We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments"
- [intro] we assign a sample pair (i,i') to be reproducible if a certain percentage signals (100c_m%) are reproducible across all features: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [other] MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering criteria simultaneously.: "MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering"
- [readme] The main function in the marr package is Marr(). The Marr() function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns: "The main function in the marr package is Marr(). The Marr() function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with one"
- [readme] pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75.: "pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75."
- [readme] pFeatures (Optional) a threshold value that lies between 0 and 1, used to assign a sample pair to be reproducible based on the reproducibility output of the features per sample pair. Default is 0.75.: "pFeatures (Optional) a threshold value that lies between 0 and 1, used to assign a sample pair to be reproducible based on the reproducibility output of the features per sample pair. Default is 0.75."
- [intro] Reproducibility is an on-going challenge with high-throughput technologies that have been developed in the last two decades for quantifying a wide range of biological processes.: "Reproducibility is an on-going challenge with high-throughput technologies that have been developed in the last two decades for quantifying a wide range of biological processes."
