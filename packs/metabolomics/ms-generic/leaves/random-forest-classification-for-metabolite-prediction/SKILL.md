---
name: random-forest-classification-for-metabolite-prediction
description: Use when you have a metabolomics count table (rows=metabolites, columns=samples) with associated metadata containing a categorical grouping factor (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - R
  - randomForest
  - ggplot2
  - Omu
  - read.metabo
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# random-forest-classification-for-metabolite-prediction

## Summary

Apply the Omu random_forest wrapper to classify metabolites or samples in metabolomics count data and generate variable importance plots that rank metabolites by their predictive strength for a specified grouping factor. This skill is useful when you need to identify which metabolites are most discriminative between experimental groups in a two-factor design.

## When to use

You have a metabolomics count table (rows=metabolites, columns=samples) with associated metadata containing a categorical grouping factor (e.g., Treatment, Genotype) and you want to: (1) build a predictive model to classify samples into groups, (2) rank metabolites by their contribution to that classification, or (3) visualize variable importance to identify candidate biomarkers. Apply this skill when univariate tests alone are insufficient and you need multivariate, ensemble-based feature ranking.

## When NOT to use

- Your data are already processed into a feature importance table or pre-ranked list; re-running random forest on derived data will not improve ranking.
- You have fewer than ~10–20 samples total; random forests require sufficient samples to avoid overfitting and to partition reliably into trees.
- Your metabolomics data are continuous measurements (e.g., quantitative m/z intensities from direct injection) rather than count or abundance data; the Omu random_forest wrapper is designed for count-like data (e.g., spectral counts, relative abundance).

## Inputs

- metabolomics count data frame (rows=metabolites, columns=samples with numeric abundance values)
- metadata table with Sample column and at least one categorical grouping factor (e.g., Treatment, Genotype, Grouped)
- grouping factor name (string specifying which metadata column to use as the response variable for classification)

## Outputs

- random forest model object (from randomForest package)
- variable importance scores (numeric vector ranking metabolites)
- ggplot2 plot object showing variable importance rankings

## How to apply

Load the metabolomics count data using read.metabo and metadata using read.csv, ensuring the metadata includes a Sample column and a grouping factor column (e.g., Treatment). Optionally, address overdispersion by applying transform_samples with the natural log function to log-transform the count data column-wise. Call the random_forest wrapper function from the Omu package, specifying the count data, metadata, the response variable (typically 'Metabolite'), and a grouping factor from the metadata; the wrapper internally invokes randomForest from the randomForest R package with default hyperparameters. Extract the returned random forest model object, then pass it to plot_variable_importance to generate a ggplot2-compatible visualization that ranks metabolites by their importance scores. Customize the plot using ggplot2 themes (e.g., theme_bw, gridline removal) as desired. The importance scores reflect how much each metabolite decreases impurity (Gini or mean-squared error) when used as a split in the forest.

## Related tools

- **randomForest** (underlying R package that implements the random forest algorithm; Omu wraps its randomForest() function to handle metabolomics data and metadata)
- **ggplot2** (graphics package used to render the variable importance plot returned by plot_variable_importance; allows customization via themes)
- **Omu** (metabolomics analysis R package providing the random_forest wrapper function and plot_variable_importance visualization) — https://github.com/connor-reid-tiffany/Omu
- **read.metabo** (Omu function for loading metabolomics count data into R with proper class assignment) — https://github.com/connor-reid-tiffany/Omu

## Examples

```
rf_model <- random_forest(count_data = c57_nos2KO_mouse_countDF, metadata = c57_nos2KO_mouse_metadata, response = 'Metabolite', grouping_factor = 'Treatment'); plot_variable_importance(rf_model) + theme_bw()
```

## Evaluation signals

- The returned random forest model object is non-null and contains ntree, mtry, and other expected slots from the randomForest S3 class.
- Variable importance scores are non-negative numeric values, sorted in descending order, with length equal to the number of metabolites in the input count table.
- The ggplot2 plot object renders without error and displays metabolites on one axis and importance values (scaled to 0–100 or raw scale) on the other; the plot is customizable with ggplot2 themes.
- Spot-check: metabolites ranked as high-importance should show visual or statistical differences across the grouping factor when examined in univariate tests (e.g., t-test, ANOVA) or in boxplots stratified by group.
- The model achieves reasonable out-of-bag (OOB) error rate (typically available via model$err.rate); if OOB error is very high (>0.4) or the model overfits, consider reducing ntree or increasing mtry, or re-evaluating the input data quality.

## Limitations

- Default hyperparameters (number of trees, mtry, node size) are applied automatically by the wrapper; the article does not document these values, so users cannot easily tune the model for their specific dataset.
- The random forest model assumes independence between metabolites and may not capture complex interactions; results are ensemble-averaged and importance scores can be sensitive to correlated metabolites.
- Variable importance is computed on training data only; the article does not mention cross-validation or separate test sets, so importance estimates may be biased or overoptimistic.
- The skill is demonstrated only on a two-factor experimental design (wild-type vs. knockout); applicability to higher-order designs, continuous outcomes, or survival endpoints is not discussed.
- No guidance is provided on sample size requirements, class imbalance handling, or how to interpret importance scores in the biological context (e.g., whether a high-importance metabolite is differentially abundant or a predictive proxy).

## Evidence

- [other] Omu has a function, `random_forest`, which is a wrapper built around the function `randomForest` from the R package randomForest: "Omu has a function, `random_forest`, which is a wrapper built around the function `randomForest` from the R package randomForest"
- [other] Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene: "Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene"
- [other] For end users metabolomics data, it is recommended to use the `read.metabo` function to load it into R: "For end users metabolomics data, it is recommended to use the `read.metabo` function to load it into R"
- [other] `transform_samples` will perform column-wise transformations across the data using the supplied function. This is useful for operations such as log transformation, or transforming by the square: "`transform_samples` will perform column-wise transformations across the data using the supplied function. This is useful for operations such as log transformation, or transforming by the square"
- [other] The figure is a ggplot2 object, so it is compatible with any ggplot2 themes: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] The meta data file should have a Sample column, with row values being sample names, and then a column for each Factor in your dataset: "The meta data file should have a Sample column, with row values being sample names, and then a column for each Factor in your dataset"
