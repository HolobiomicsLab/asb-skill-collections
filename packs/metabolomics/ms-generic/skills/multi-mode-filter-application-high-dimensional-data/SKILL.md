---
name: multi-mode-filter-application-high-dimensional-data
description: Use when you have high-dimensional biological data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Bioconductor
  - marr
  - devtools
  - BiocManager
  techniques:
  - mass-spectrometry
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

# Multi-mode filter application to high-dimensional biological data

## Summary

Apply the MarrFilterData() function in three complementary filtering modes—by features, by sample pairs, or by both simultaneously—to subset high-dimensional replicate experiment data based on reproducibility thresholds computed across pairwise signal ranks. This skill enables targeted retention of reproducible signals at either the feature level (100×c_s% threshold), the sample-pair level (100×c_m% threshold), or both, producing filtered subsets suitable for downstream statistical or biological interpretation.

## When to use

You have high-dimensional biological data (e.g., metabolomics, mass spectrometry) measured across replicate experiments, a Marr() output object containing reproducibility statistics (percent reproducible signals per feature and per sample pair), and a research question requiring you to isolate either reproducible features, reproducible sample pairs, or both. Use this skill when reproducibility heterogeneity across features or sample pairs is expected and you need to stratify your analysis rather than apply a single global filter.

## When NOT to use

- Input is already a feature table with no replicate structure or reproducibility pre-computed; MarrFilterData() requires a pre-computed Marr() object.
- All features or sample pairs exhibit uniformly high or uniformly low reproducibility; filtering modes are most informative when reproducibility varies substantially across features or pairs.
- You require a fixed absolute count of features or sample pairs rather than a threshold-driven approach; MarrFilterData() uses percentage thresholds (c_s, c_m) rather than rank-based cutoffs.

## Inputs

- Marr() output object (S4 object containing reproducibility statistics)
- High-dimensional biological data (SummarizedExperiment, data frame, or matrix; rows = features, columns = samples)

## Outputs

- Feature-filtered SummarizedExperiment (subset by='features')
- Sample-pair-filtered SummarizedExperiment (subset by='samplePairs')
- Doubly-filtered SummarizedExperiment (subset by='both')
- Associated reproducibility metadata (MarrFeaturesfiltered, MarrSamplepairsfiltered accessor outputs)

## How to apply

Load the Marr() output object containing reproducibility distributions (e.g., MarrOutput). Apply MarrFilterData(object=MarrOutput, by='features') to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level reproducibility threshold (100×c_s%), typically defaulting to 75%; this produces a feature-filtered SummarizedExperiment. Alternatively, apply MarrFilterData(object=MarrOutput, by='samplePairs') to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100×c_m%, default 75%), producing a sample-pair-filtered object. For dual filtering, apply MarrFilterData(object=MarrOutput, by='both') to apply both filters simultaneously. The choice of mode depends on whether your downstream analysis prioritizes feature robustness, sample-pair concordance, or both. Inspect the filtered object dimensions and accessor methods (e.g., MarrFeaturesfiltered(), MarrSamplepairsfiltered()) to confirm that the number of retained features or sample pairs aligns with your reproducibility criteria.

## Related tools

- **marr** (R/Bioconductor package providing MarrFilterData() function and Marr() reproducibility computation; used to compute reproducibility statistics and apply multi-mode filtering) — https://github.com/Ghoshlab/marr
- **devtools** (R package management tool for installing marr from GitHub repository) — https://github.com/r-lib/devtools
- **BiocManager** (Bioconductor package manager for installing marr from Bioconductor repository)

## Examples

```
MarrOutput <- Marr(object = dataSE, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); filtered_features <- MarrFilterData(object = MarrOutput, by='features'); filtered_pairs <- MarrFilterData(object = MarrOutput, by='samplePairs'); filtered_both <- MarrFilterData(object = MarrOutput, by='both')
```

## Evaluation signals

- Verify that the filtered object's feature/sample-pair count is less than or equal to the input object's corresponding count; confirm dimensionality reduction is in the expected direction.
- Cross-check filtered feature/sample-pair membership against the MarrFeaturesfiltered() and MarrSamplepairsfiltered() accessor outputs; retained entities should have reproducibility percentages ≥ 100×c_s% (features) or 100×c_m% (sample pairs).
- For by='both' mode, confirm that the doubly-filtered object is a subset of both the by='features' and by='samplePairs' objects (intersection property).
- Inspect distribution plots (MarrPlotFeatures(), MarrPlotSamplepairs()) on the filtered object; retained features/pairs should exhibit shifted distributions toward higher reproducibility compared to the original.
- Verify no missing values or NaN entries are introduced in the filtered assay data; SummarizedExperiment structure and metadata should remain intact.

## Limitations

- MarrFilterData() depends critically on the choice of thresholds (c_s, c_m); suboptimal thresholds may retain too few or too many entities and should be validated against downstream analysis stability.
- The method assumes independence between feature-level and sample-pair-level reproducibility assessments; by='both' filtering may be overly stringent if these measures are correlated.
- Filtering is performed on reproducibility ranks computed from pairwise comparisons; the method is nonparametric and does not account for absolute signal magnitude, potentially retaining low-abundance but reproducible features.
- Sample size and replicate design affect reproducibility estimation; experiments with very few replicates or highly imbalanced replicate groups may yield unstable reproducibility distributions.

## Evidence

- [other] MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering criteria simultaneously.: "MarrFilterData() accepts three filtering modes: by='features' to retain only reproducible features, by='samplePairs' to retain only reproducible sample pairs, and by='both' to apply both filtering"
- [other] Apply MarrFilterData() with by='features' to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level threshold (100*c_s%).: "Apply MarrFilterData() with by='features' to retain only features where the percentage of reproducible pairwise signals exceeds the feature-level threshold (100*c_s%), producing a feature-filtered"
- [other] Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%).: "Apply MarrFilterData() with by='samplePairs' to retain only sample pairs where the percentage of reproducible signals across all features exceeds the sample-pair-level threshold (100*c_m%), producing"
- [intro] We assign feature m to be reproducible if a certain percentage signals (100c_s%) are reproducible for pairwise combinations of replicate experiments.: "We assign feature $m$ to be reproducible if a certain percentage signals ($100c_s\%$) are reproducible for pairwise combinations of replicate experiments"
- [intro] we assign a sample pair (i,i') to be reproducible if a certain percentage signals (100c_m%) are reproducible across all features.: "we assign a sample pair $(i,~i')$ to be reproducible if a certain percentage signals ($100c_m\%$) are reproducible across all features"
- [readme] marr measures the reproducibility of features per sample pair and sample pairs per feature in high-dimensional biological replicate experiments.: "`marr` measures the reproducibility of features per sample pair and sample pairs per feature in high-dimensional biological replicate experiments."
- [readme] The Marr() function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns.: "The `Marr()` function needs one required object and three optional objects: (1) object: a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites"
