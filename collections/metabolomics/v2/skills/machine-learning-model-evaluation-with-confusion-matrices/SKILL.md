---
name: machine-learning-model-evaluation-with-confusion-matrices
description: Use when after fitting a random forest model to metabolomics count data with a categorical response variable (e.g., wild-type vs. knockout treatment groups), you need to quantify how accurately the model predicts group membership and identify which metabolites drive the classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - randomForest
  - ggplot2
  - Omu
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# machine-learning-model-evaluation-with-confusion-matrices

## Summary

Evaluate a trained random forest classifier on metabolomics data by computing and visualizing a confusion matrix to assess prediction accuracy across treatment groups. This skill generates variable importance plots and model diagnostics essential for validating whether the classifier correctly distinguishes metabolite profiles between experimental conditions.

## When to use

After fitting a random forest model to metabolomics count data with a categorical response variable (e.g., wild-type vs. knockout treatment groups), you need to quantify how accurately the model predicts group membership and identify which metabolites drive the classification. Use this when the goal is to validate classifier performance on the example c57_nos2KO_mouse_countDF dataset or similar two-factor metabolomics experiments.

## When NOT to use

- Input metadata lacks a clear categorical response variable or grouping factor (random_forest requires a factor-level target for supervised classification).
- Count data is severely sparse or underdispersed; log transformation may not adequately stabilize variance for random forest splits.
- Sample size is very small (n < 10 per group); random forest ensemble may overfit or produce unreliable variable importance estimates.

## Inputs

- metabolomics count data (e.g., c57_nos2KO_mouse_countDF loaded via read.metabo)
- sample metadata with categorical grouping factor (e.g., Treatment, Grouped)
- optionally log-transformed count data (via transform_samples with natural log)

## Outputs

- random forest model object from Omu random_forest wrapper
- variable importance plot (ggplot2 object) ranking metabolites by classification contribution
- confusion matrix diagnostics (accuracy, precision, recall per treatment group)

## How to apply

Fit the random_forest wrapper function from Omu on log-transformed count data and metadata, specifying a grouping factor (e.g., Treatment or Grouped) as the response variable; the wrapper internally calls randomForest with default hyperparameters. Extract the returned model object and pass it to plot_variable_importance to generate a ggplot2 object showing metabolite rankings by importance (typically mean decrease in accuracy or Gini). Interpret the plot by identifying top-ranked metabolites as the strongest classifiers; customize visualization with ggplot2 themes (e.g., theme_bw, remove gridlines) for publication clarity. Verify model fit by checking that variable importance scores are non-negative and sorted in descending order, and that the number of metabolites in the plot equals the number of features in the original count data.

## Related tools

- **randomForest** (underlying R package that fits the ensemble classifier; called by Omu's random_forest wrapper with default hyperparameters (number of trees, mtry, node size))
- **ggplot2** (produces and customizes the variable importance plot returned by plot_variable_importance; enables theme modification (e.g., theme_bw, gridline removal))
- **Omu** (R package providing random_forest wrapper function and plot_variable_importance visualization; manages metadata integration and model object extraction) — https://github.com/connor-reid-tiffany/Omu
- **R** (runtime environment for Omu, randomForest, and ggplot2 functions)

## Examples

```
rf_model <- random_forest(count_data = c57_nos2KO_mouse_countDF, metadata = c57_nos2KO_mouse_metadata, response_var = 'Treatment'); plot_variable_importance(rf_model) + theme_bw() + theme(panel.grid = element_blank())
```

## Evaluation signals

- Variable importance plot displays all metabolite features ranked by importance score in descending order with no missing or negative values.
- Model predictions on held-out or in-bag samples yield a confusion matrix with >50% accuracy (typical threshold for two-class metabolomics discrimination); check diagonal sum / total predictions.
- Top-ranked metabolites in the importance plot align with known biological differences between treatment groups (e.g., wild-type vs. nos2 knockout), validating that the classifier learns meaningful patterns.
- Plot is a valid ggplot2 object compatible with additional ggplot2 themes; verifiable by printing structure and checking for ggplot class attribute.
- The number of metabolites plotted equals the number of rows in the input count data, indicating no features were dropped during model fitting.

## Limitations

- Omu documentation does not specify exact default hyperparameters for randomForest (number of trees, mtry, node size, split criterion); users cannot directly tune these within the wrapper.
- Variable importance metric (mean decrease in accuracy vs. Gini) is not documented; relative rather than absolute ranking should be emphasized when interpreting results.
- random_forest wrapper output structure and metadata handling are not fully detailed; users must infer model object composition from example code.
- Applies only to count-based metabolomics data; continuous spectral or intensity data may require different preprocessing or alternative classifiers not covered by Omu.

## Evidence

- [other] random_forest wrapper from Omu generates variable importance plots: "Omu has a function, ```random_forest```, which is a wrapper built around the function ```randomForest``` from the R package randomForest"
- [other] log transformation addresses overdispersion in metabolomics counts: "```transform_samples``` will perform column-wise transformations across the data using the supplied function. This is useful for operations such as log transformation"
- [other] plot_variable_importance produces ggplot2 object customizable with themes: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] c57_nos2KO_mouse dataset is a two-factor experiment with wild-type and knockout mice: "Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene"
- [other] Metadata must include Sample column and grouping factor columns: "The meta data file should have a Sample column, with row values being sample names, and then a column for each Factor in your dataset"
