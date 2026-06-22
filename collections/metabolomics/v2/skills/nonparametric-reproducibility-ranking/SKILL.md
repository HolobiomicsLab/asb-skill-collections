---
name: nonparametric-reproducibility-ranking
description: Use when you have high-dimensional replicate experiment data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - Bioconductor
  - marr
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

# Nonparametric Reproducibility Ranking

## Summary

Apply the Maximum Rank Reproducibility (marr) method to quantify reproducibility of features (metabolites/genes) across replicate biological or technical samples, and of sample pairs across features. This nonparametric approach produces ranked reproducibility metrics and binary classifications (reproducible/non-reproducible) based on user-defined thresholds, without assuming a distributional form.

## When to use

Use this skill when you have high-dimensional replicate experiment data (e.g., mass spectrometry metabolomics, RNA-seq) with multiple biological or technical replicates per sample, and you need to assess which features are reproducible across replicates and which sample pairs show reproducible feature rankings. Apply it when traditional parametric assumptions are unreliable or when you require a non-parametric ranking-based measure of concordance rather than correlation or statistical significance alone.

## When NOT to use

- Input data has not been preprocessed (missing value imputation and normalization must be completed first); marr expects a clean, imputed matrix.
- You have no replicate structure or only single replicates per sample; marr requires pairwise comparisons across replicates to rank and measure concordance.
- Your goal is differential abundance testing or statistical hypothesis testing rather than reproducibility profiling; use marr to filter reproducible features, then apply differential testing downstream.

## Inputs

- SummarizedExperiment object with feature (metabolite/gene) abundance matrix (rows=observations, columns=samples)
- Preprocessed data: filtered for >80% missingness, BPCA-imputed, median-normalized
- Numeric replicate design indicating which samples are biological or technical replicates

## Outputs

- MarrFeatures: percent reproducible sample pairs per feature (unfiltered)
- MarrSamplepairs: percent reproducible features per sample pair (unfiltered)
- MarrFeaturesfiltered: binary classification of reproducible features meeting pFeatures threshold
- MarrSamplepairsfiltered: binary classification of reproducible sample pairs meeting pSamplepairs threshold

## How to apply

First, load or construct a SummarizedExperiment object with observations (metabolites or genes) on rows and samples on columns; data should be pre-processed (filtered for >80% missingness, imputed with BPCA, and median-normalized). Install the marr package via devtools::install_github("Ghoshlab/marr") and call the Marr() function with three key parameters: pSamplepairs (threshold, default 0.75) to classify features as reproducible if the percentage of reproducible sample pairs exceeds this fraction; pFeatures (threshold, default 0.75) to classify sample pairs as reproducible if the percentage of reproducible features exceeds this fraction; and alpha (FDR control level, default 0.05). The method ranks feature values within each sample pair, counts concordant rankings across replicates, and produces four output tables: unfiltered and filtered reproducibility metrics for both features (per sample pair) and sample pairs (per feature). Interpret the filtered tables as the binary reproducibility classifications, and use the unfiltered tables to assess the degree of reproducibility on a continuum.

## Related tools

- **marr** (R/Bioconductor package implementing the Maximum Rank Reproducibility method; provides Marr() function and accessor methods (MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered) to compute and extract reproducibility tables) — https://github.com/Ghoshlab/marr
- **devtools** (R package development tool used to install marr from GitHub via devtools::install_github()) — https://github.com/r-lib/devtools
- **BiocManager** (Alternative installation route for marr from Bioconductor repository)
- **SummarizedExperiment** (Bioconductor class for storing high-dimensional biological data with rows (features) and columns (samples); required input container for marr)

## Examples

```
library(marr); data(msprepCOPD); MarrOutput <- Marr(object=msprepCOPD, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); MarrFeat <- MarrFeatures(MarrOutput); MarrSP <- MarrSamplepairs(MarrOutput)
```

## Evaluation signals

- All four output tables (MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered) are non-empty and contain expected columns for reproducibility metrics and feature/sample pair identifiers.
- Unfiltered tables contain numeric percent reproducibility values in the range [0, 100]; filtered tables contain binary (0/1 or TRUE/FALSE) classifications matching the threshold criteria (pSamplepairs=0.75, pFeatures=0.75).
- Reproducibility percentages in unfiltered tables are monotonically consistent with binary assignments in filtered tables (e.g., features/sample pairs with >75% reproducibility are marked as reproducible in filtered output).
- Reproducibility metrics respect the ranking structure: sample pairs with more concordant feature rank orderings should show higher percent reproducibility values.
- FDR control at alpha=0.05 is applied; verify by comparing filtered classifications against a null model or checking that false positive rate among filtered reproducible entities remains below expected level.

## Limitations

- The method is most reliable when the number of replicate pairs is sufficient (typically ≥3 biological or technical replicates); small sample sizes reduce the stability of rank-based reproducibility estimates.
- Threshold parameters (pSamplepairs, pFeatures, alpha) are user-configurable but no formal guidance for dataset-specific optimization is provided; choice of thresholds is data-dependent and may require validation or sensitivity analysis.
- marr assumes that replicate structure is well-defined and that samples are correctly annotated as replicates; mislabeled or ambiguous replicate assignments will produce misleading reproducibility rankings.
- The nonparametric rank-based approach does not account for magnitude of feature abundance; a small true signal with perfect rank concordance across replicates will score equally reproducible as a large signal with the same rank concordance, which may not reflect biological relevance.

## Evidence

- [intro] marr procedure can be adapted to high-throughput MS-Metabolomics experiments across biological or technical replicate samples: "the (ma)ximum (r)ank (r)eproducibility (marr) procedure can be adapted to high-throughput MS-Metabolomics experiments across (biological or technical) replicate samples"
- [intro] The Marr() function produces four outputs: MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, and MarrSamplepairsfiltered: "The Marr() function produces four outputs: reproducible sample pairs per metabolite (MarrFeatures), reproducible metabolites per sample pair (MarrSamplepairs), percent of reproducible sample pairs"
- [intro] Feature filtering assigns a feature to be reproducible if percentage of reproducible signals exceeds threshold: "We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments"
- [intro] Sample pair filtering assigns a sample pair to be reproducible if percentage of reproducible signals across features exceeds threshold: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [intro] Preprocessing requires filtering >80% missingness, BPCA imputation, and median normalization: "Filtering: Metabolites are removed if they are missing more than 80% of the samples. Missing value imputation technique: We apply Bayesian Principal Component Analysis (BPCA) to impute missing"
- [readme] marr installed from GitHub using devtools::install_github(): "The R-package **marr** can be installed from GitHub using the R package [devtools]: devtools::install_github("Ghoshlab/marr")"
- [readme] Marr() function requires SummarizedExperiment object with rows as observations and columns as samples: "object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns"
- [readme] Default threshold parameters: pSamplepairs=0.75, pFeatures=0.75, alpha=0.05: "pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75."
