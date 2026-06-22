---
name: reproducibility-statistic-computation-rank-based
description: Use when you have high-dimensional replicate experiment data (metabolomics, proteomics, or genomics) with multiple biological or technical replicates per sample, and you need to assess which features are reproducible across replicates and which sample pairs show consistent reproducibility patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - Bioconductor
  - marr
  - MSPrep
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compute rank-based reproducibility statistics for replicate experiments

## Summary

Apply the Maximum Rank Reproducibility (marr) procedure to quantify reproducibility of features (metabolites/genes) across technical or biological replicate samples, producing percent-reproducible rankings and filtered reproducibility tables stratified by feature-wise and sample-pair-wise thresholds.

## When to use

You have high-dimensional replicate experiment data (metabolomics, proteomics, or genomics) with multiple biological or technical replicates per sample, and you need to assess which features are reproducible across replicates and which sample pairs show consistent reproducibility patterns. Use this when replicate variability is a primary concern and you want a nonparametric, threshold-agnostic ranking before applying cutoffs.

## When NOT to use

- Input data contain >80% missing values per feature without imputation; preprocessing (BPCA imputation, median normalization) must precede marr.
- Samples are not true replicates (biological or technical); marr requires pairwise replicate structure to compute rank reproducibility.
- You seek fold-change or differential abundance comparisons rather than reproducibility assessment; marr is orthogonal to effect size.

## Inputs

- SummarizedExperiment object or matrix with observations (metabolites, genes, proteins) as rows and replicate samples as columns
- Preprocessed assay data with missing values imputed (e.g., via BPCA) and normalized (e.g., median normalization)
- Metadata defining replicate sample groupings

## Outputs

- MarrFeatures table: percent reproducible sample pairs per feature, unfiltered
- MarrSamplepairs table: percent reproducible features per sample pair, unfiltered
- MarrFeaturesfiltered table: features with percent reproducible sample pairs exceeding pFeatures threshold
- MarrSamplepairsfiltered table: sample pairs with percent reproducible features exceeding pSamplepairs threshold

## How to apply

Load your preprocessed, imputed, and normalized assay data (rows=features, columns=samples) as a SummarizedExperiment object or matrix. Execute the Marr() function with three key parameters: pSamplepairs (threshold for reproducible features per sample pair; default 0.75), pFeatures (threshold for reproducible sample pairs per feature; default 0.75), and alpha (FDR control level; default 0.05). The function computes reproducibility ranks for all pairwise replicate combinations, then filters features and sample pairs by the specified thresholds. Extract the four output tables using accessor methods: MarrFeatures (unfiltered feature-wise reproducibility), MarrSamplepairs (unfiltered sample-pair-wise reproducibility), MarrFeaturesfiltered (features meeting pFeatures threshold), and MarrSamplepairsfiltered (sample pairs meeting pSamplepairs threshold). Validate that all tables are non-empty and contain expected reproducibility metrics and rank columns.

## Related tools

- **marr** (Implements the Marr() function to compute rank-based reproducibility statistics and produce filtered reproducibility tables) — https://github.com/Ghoshlab/marr
- **devtools** (Enables installation of marr package from GitHub repository) — https://github.com/r-lib/devtools
- **Bioconductor** (Provides SummarizedExperiment data structure and ecosystem for handling high-dimensional biological assay data)
- **MSPrep** (Pre-processes and normalizes mass spectrometry metabolomics data prior to marr analysis)

## Examples

```
library(marr); data(msprepCOPD); MarrOutput <- Marr(object = msprepCOPD, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); features_filt <- MarrFeaturesfiltered(MarrOutput); samplepairs_filt <- MarrSamplepairsfiltered(MarrOutput)
```

## Evaluation signals

- All four output tables (MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered) are non-empty and contain at least one row with valid reproducibility metrics.
- Percent reproducible values in unfiltered tables range from 0 to 1 (or 0–100% depending on scale); filtered tables contain only rows meeting the specified pSamplepairs or pFeatures threshold.
- Feature and sample pair rank orderings are consistent between unfiltered and filtered outputs (filtered is a strict subset ranked by reproducibility).
- Number of features in MarrFeaturesfiltered ≤ total features in MarrFeatures; number of sample pairs in MarrSamplepairsfiltered ≤ total pairwise comparisons in MarrSamplepairs.
- marr output integrates with downstream visualization (MarrPlotFeatures, MarrPlotSamplepairs) without errors; plots show distribution of percent reproducibility across ranked features or sample pairs.

## Limitations

- marr requires replicate structure (biological or technical replicates per sample); cannot be applied to single-run or non-replicated assays.
- Performance and interpretability depend on quality of preprocessing (missing value imputation via BPCA, median normalization); systematic biases in preprocessing propagate into reproducibility rankings.
- Threshold parameters (pSamplepairs, pFeatures, alpha) are user-specified; no automatic threshold selection is provided; results are sensitive to choice of cutoff values.
- marr is nonparametric and does not estimate effect size, fold-change, or statistical significance of differential abundance; it ranks reproducibility only.

## Evidence

- [intro] marr procedure can be adapted to high-throughput MS-Metabolomics experiments across biological or technical replicate samples: "the (ma)ximum (r)ank (r)eproducibility (marr) procedure can be adapted to high-throughput MS-Metabolomics experiments across (biological or technical) replicate samples"
- [intro] Four reproducibility output tables produced by Marr(): MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered: "The Marr() function produces four outputs: reproducible sample pairs per metabolite (MarrFeatures), reproducible metabolites per sample pair (MarrSamplepairs), percent of reproducible sample pairs"
- [intro] Feature filtering: reproducible if percentage of reproducible signals across pairwise replicates exceeds threshold: "We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments"
- [intro] Sample pair filtering: reproducible if percentage of reproducible signals across all features exceeds threshold: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [readme] Marr() function parameters and accessor methods described in README: "The main function in the **marr** package is `Marr()`. The `Marr()` function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with"
- [readme] Accessor methods to extract individual marr output slots: "Individual slots can be extracted using accessor methods: MarrSamplepairs(MarrOutput) # extract the distribution of percent #reproducible features (column-wise) per sample pair"
- [intro] Missing value imputation and normalization preprocessing steps: "Missing value imputation technique: We apply Bayesian Principal Component Analysis (BPCA) to impute missing values; Normalization: Median normalization are performed"
