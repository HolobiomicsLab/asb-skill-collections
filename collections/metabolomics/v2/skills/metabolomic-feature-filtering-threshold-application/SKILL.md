---
name: metabolomic-feature-filtering-threshold-application
description: Use when after running the Marr() function on preprocessed metabolomic data (with missing value imputation and normalization already complete) when you need to distinguish reproducible from non-reproducible features and sample pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# metabolomic-feature-filtering-threshold-application

## Summary

Apply reproducibility-based thresholds to filter metabolomic features and sample pairs in high-dimensional replicate experiments, identifying which features and sample pairs meet minimum reproducibility standards. This skill uses the marr (Maximum Rank Reproducibility) method to assign reproducibility status based on the percentage of reproducible signals across pairwise replicate combinations.

## When to use

Apply this skill after running the Marr() function on preprocessed metabolomic data (with missing value imputation and normalization already complete) when you need to distinguish reproducible from non-reproducible features and sample pairs. Specifically use it when you have pairwise replicate measurements (e.g., biological or technical replicates from the same samples) and want to assess which metabolites maintain consistent signals across those replicates at a specified confidence level (alpha threshold).

## When NOT to use

- Input metabolomic data has not been preprocessed (missing values imputed, normalized) — apply MSPrep or equivalent preprocessing first.
- You have only single replicates per sample with no pairwise comparisons available — marr requires replicate measurements to compute reproducibility.
- Your experimental design does not include technical or biological replicates — the method cannot assess reproducibility without variation across replicates to measure consistency.

## Inputs

- SummarizedExperiment object with metabolite features as rows and biological/technical replicate samples as columns
- Pre-processed metabolomic matrix (missing values imputed, normalized via median normalization or equivalent)
- Three threshold parameters: pSamplepairs (0–1), pFeatures (0–1), alpha (0–1 for FDR control)

## Outputs

- MarrFeatures table: percent of reproducible sample pairs per metabolite (row-wise)
- MarrSamplepairs table: percent of reproducible features per sample pair (column-wise)
- MarrFeaturesfiltered table: subset of features where percent reproducible sample pairs exceeds pFeatures threshold
- MarrSamplepairsfiltered table: subset of sample pairs where percent reproducible features exceeds pSamplepairs threshold

## How to apply

Execute the Marr() function on your SummarizedExperiment object containing metabolite rows and sample columns, specifying three filtering parameters: pSamplepairs (threshold for percent reproducible features per sample pair, typically 0.75), pFeatures (threshold for percent reproducible sample pairs per feature, typically 0.75), and alpha (FDR control level, typically 0.05). The function assigns a feature m as reproducible if the percentage of reproducible signals (100*c_s%) for pairwise combinations of replicate experiments exceeds the pFeatures threshold; conversely, it assigns a sample pair (i, i') as reproducible if the percentage of reproducible signals (100*c_m%) across all features exceeds the pSamplepairs threshold. Extract the four output tables (MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered) and validate that all contain non-empty results with expected columns for reproducibility metrics and rankings.

## Related tools

- **marr** (Executes the Marr() function and outputs four reproducibility tables for filtered and unfiltered feature and sample pair reproducibility metrics) — https://github.com/Ghoshlab/marr
- **devtools** (Installs the marr R package from GitHub repository using devtools::install_github()) — https://github.com/r-lib/devtools
- **Bioconductor** (Alternative installation pathway for marr via BiocManager::install())
- **R** (Host environment for loading SummarizedExperiment objects, executing Marr() function, and extracting/validating output tables)
- **MSPrep** (Upstream preprocessing tool for metabolomic data; msprepCOPD dataset in marr package was pre-processed using MSPrep)

## Examples

```
library(marr); data(msprepCOPD); MarrOutput <- Marr(object = msprepCOPD, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); features_filtered <- MarrFeaturesfiltered(MarrOutput); samplepairs_filtered <- MarrSamplepairsfiltered(MarrOutput)
```

## Evaluation signals

- All four output tables (MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered) are non-empty and contain expected columns for reproducibility percentages and feature/sample pair identifiers.
- Filtered tables (MarrFeaturesfiltered, MarrSamplepairsfiltered) are proper subsets of unfiltered tables (MarrFeatures, MarrSamplepairs), with row counts reduced according to applied thresholds.
- Reproducibility percentages in all tables fall within the 0–100 range and exhibit expected distribution patterns (e.g., filtered tables skewed toward higher percentages than unfiltered tables).
- No missing or NaN values in the reproducibility percentage columns; all features and sample pairs in output tables have valid metric values.
- Threshold parameters (pSamplepairs, pFeatures, alpha) used in the Marr() call match the analysis goal and are documented in the output metadata or processing log.

## Limitations

- The method requires replicate experiments (biological or technical) — it cannot assess reproducibility in single-measurement-per-sample designs.
- Reproducibility assessment depends on the quality of upstream preprocessing; missing value imputation errors or inadequate normalization will propagate into marr reproducibility rankings.
- Alpha threshold for FDR control is applied globally; features or sample pairs with borderline reproducibility near the threshold boundary may be sensitive to small changes in parameter values.
- The method ranks reproducibility but does not account for feature-specific variability (e.g., inherently noisy metabolites or sample-specific batch effects) — filtering by percentage alone may remove truly variable but biologically meaningful features.

## Evidence

- [intro] We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments: "We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments"
- [intro] we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [other] The Marr() function produces four outputs: reproducible sample pairs per metabolite (MarrFeatures), reproducible metabolites per sample pair (MarrSamplepairs), percent of reproducible sample pairs per metabolite greater than 75% (MarrFeaturesfiltered), and percent of reproducible metabolites per sample pair greater than 75% (MarrSamplepairsfiltered).: "The Marr() function produces four outputs: reproducible sample pairs per metabolite (MarrFeatures), reproducible metabolites per sample pair (MarrSamplepairs), percent of reproducible sample pairs"
- [readme] MarrSamplepairs(MarrOutput) # extract the distribution of percent reproducible features (column-wise) per sample pair: "MarrSamplepairs(MarrOutput) # extract the distribution of percent reproducible features (column-wise) per sample pair"
- [readme] MarrFeatures(MarrOutput) # extract the distribution of percent reproducible sample pairs (row-wise) per feature: "MarrFeatures(MarrOutput) # extract the distribution of percent reproducible sample pairs (row-wise) per feature"
- [readme] object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns: "object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns"
- [readme] pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75.: "pSamplepairs (Optional) a threshold value that lies between 0 and 1, used to assign a feature to be reproducible based on the reproducibility output of the sample pairs per feature. Default is 0.75."
- [readme] alpha (Optional) level of significance to control the False Discovery Rate (FDR). Default is 0.05.: "alpha (Optional) level of significance to control the False Discovery Rate (FDR). Default is 0.05."
