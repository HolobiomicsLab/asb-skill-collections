---
name: variable-importance-ranking-and-interpretation
description: Use when after fitting a random forest classifier to metabolomics count
  data with a binary or multiclass grouping variable (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2939
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3314
  tools:
  - R
  - randomForest
  - ggplot2
  - Omu
  license_tier: restricted
  provenance_tier: literature
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

# variable-importance-ranking-and-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Ranks and visualizes metabolite importance in random forest classification models to identify which compounds discriminate between experimental groups. This skill extracts feature importance scores from a fitted random forest model and generates publication-ready plots, enabling interpretation of which metabolites drive group separation in metabolomics datasets.

## When to use

After fitting a random forest classifier to metabolomics count data with a binary or multiclass grouping variable (e.g., treatment, genotype, disease status), use this skill to identify which metabolites are most predictive of group membership and to communicate their relative importance in a figure.

## When NOT to use

- Input random forest model was not fitted to metabolomics count data or was trained on pre-aggregated/collapsed features rather than individual metabolites.
- Grouping variable is continuous (e.g., pH, age in years) rather than categorical; random forest importance is designed for classification tasks, not regression.
- Dataset has extreme class imbalance or very few samples per group, making importance scores unreliable due to instability in tree construction.

## Inputs

- randomForest model object (output from Omu's random_forest wrapper function)
- Metabolomics count data (c57_nos2KO_mouse_countDF or equivalent count matrix)
- Metadata with grouping factor (e.g., Treatment, Grouped column from c57_nos2KO_mouse_metadata)

## Outputs

- ggplot2 object showing ranked metabolite importance scores
- Variable importance ranking (metabolite names and scores)
- Publication-ready visualization customizable with ggplot2 themes

## How to apply

Call the plot_variable_importance function on the random forest model object returned by the Omu random_forest wrapper. This function extracts variable importance scores (which measure the decrease in impurity, typically Gini importance, across all splits in the forest) and produces a ggplot2 object ranking metabolites by importance. The resulting plot can be customized with standard ggplot2 themes (e.g., theme_bw) to remove gridlines or adjust aesthetics. Importance scores reflect the average discriminative power of each metabolite across all trees; metabolites with higher scores contributed more to correct classification. Inspect the top-ranked metabolites to identify which compounds or metabolite classes best separate your experimental groups.

## Related tools

- **randomForest** (Underlying R package that implements the random forest algorithm; Omu's random_forest wrapper calls randomForest with default hyperparameters and returns a model object containing importance scores.) — https://cran.r-project.org/web/packages/randomForest/
- **ggplot2** (Produces the variable importance plot as a ggplot2 object, allowing customization with themes, coordinate flips, and geom modifications.) — https://ggplot2.tidyverse.org/
- **Omu** (R package containing the random_forest wrapper function and plot_variable_importance function that extract and visualize variable importance from randomForest models applied to metabolomics data.) — https://github.com/connor-reid-tiffany/Omu

## Examples

```
model <- random_forest(count_data=c57_nos2KO_mouse_countDF, metadata=c57_nos2KO_mouse_metadata, response='Metabolite', grouping='Treatment'); plot_variable_importance(model) + theme_bw() + theme(panel.grid=element_blank())
```

## Evaluation signals

- Variable importance plot displays all metabolites ranked by importance score in descending order; top metabolites should correspond to compounds known to differ between experimental groups.
- Importance scores are non-negative and sum to a total reflecting the model's discriminative power; verify no scores are NaN or Inf.
- Plot is a ggplot2 object that responds to ggplot2 theme functions (e.g., theme_bw); custom themes can be applied without error.
- Random forest model accuracy or out-of-bag error rate is reasonable (better than random guessing) on the grouping variable; poor model performance indicates importance scores may be uninformative.
- Top-ranked metabolites, when manually inspected in the original count data, show visibly different distributions or mean abundance across groups.

## Limitations

- Variable importance scores depend on default randomForest hyperparameters (mtry, ntree, etc.) documented in the randomForest package; changing these parameters may alter rankings.
- Importance is biased toward high-cardinality features in some implementations; metabolites with many unique values may receive inflated importance scores.
- Importance does not measure effect size or biological significance; a metabolite can rank high while having a small log-fold-change between groups.
- No built-in statistical significance test for importance scores; practitioners should consider permutation testing or cross-validation to assess ranking stability.
- Omu's documentation does not specify the exact importance metric (Gini, permutation, etc.) used by the random_forest wrapper, making it difficult to reproduce or compare with other implementations.

## Evidence

- [other] Extract variable importance: "Generate a variable importance plot using plot_variable_importance on the random forest model object, which produces a ggplot2 object"
- [other] Customize with ggplot2: "customize with ggplot2 themes as desired (e.g., theme_bw, remove gridlines)"
- [other] Random forest wrapper in Omu: "Omu has a function, ```random_forest```, which is a wrapper built around the function ```randomForest``` from the R package randomForest"
- [other] ggplot2 compatibility: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] Model output structure: "Extract the returned random forest model object and associated metadata from the wrapper output"
