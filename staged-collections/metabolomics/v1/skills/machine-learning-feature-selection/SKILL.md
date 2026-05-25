---
name: machine-learning-feature-selection
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to apply random-forest variable importance scoring on a preprocessed feature table to identify and rank discriminative metabolite features, followed by a quantitative threshold to subset differential features for annotation and validation.
when_to_use_negative:
- Input feature table is already a curated, low-dimensional feature set (e.g., <50 features); random-forest selection adds unnecessary complexity.
- Outcome variable is continuous (e.g., age, metabolite concentration); use regression-based feature selection (e.g., elastic net, recursive feature elimination) instead.
- You need global feature rankings across multiple studies or platforms without retraining; random-forest importance is specific to your training set and outcome.
edam_operation: http://edamontology.org/operation_2409
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: RandomForest (R package)
  role: Train ensemble classifier to compute variable importance scores for metabolite feature ranking and selection
- name: R programming language
  role: Environment for implementing random-forest training, threshold filtering, and feature table manipulation
- name: Jupyter Notebook
  role: Reproducible notebook environment for documenting and executing the feature selection workflow
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
derived_from:
- doi: 10.1128/msystems.00710-22
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/machine-learning-feature-selection@sha256:cf969729ae5f745ee7bbccb5bd4cffc2688fae52d17a262126b3c5527792bfd4
---

# machine-learning-feature-selection

## Summary

Use random-forest variable importance scoring to identify and rank the most discriminative metabolite features from a preprocessed feature table, then apply a quantitative threshold to subset a tractable set of differential features for downstream annotation and validation. This approach reduces dimensionality while preserving biological signal by letting the ensemble model weight features by their predictive power.

## When to use

When you have a large, preprocessed metabolomic feature table (e.g., >1,000 features) and a categorical outcome variable (e.g., industrialization status), and you need to reduce the feature space to a manageable subset for manual annotation or validation. Specifically applicable when you have already removed noise, aligned peaks, and gap-filled your data, and you want to rank features by their ability to discriminate between groups without imposing arbitrary abundance thresholds.

## When NOT to use

- Input feature table is already a curated, low-dimensional feature set (e.g., <50 features); random-forest selection adds unnecessary complexity.
- Outcome variable is continuous (e.g., age, metabolite concentration); use regression-based feature selection (e.g., elastic net, recursive feature elimination) instead.
- You need global feature rankings across multiple studies or platforms without retraining; random-forest importance is specific to your training set and outcome.

## Inputs

- Preprocessed metabolomic feature table (gap-filled and non-gap-filled variants), with features as rows and samples as columns
- Categorical outcome variable (e.g., industrialization group, disease status)
- Top N most abundant features (e.g., top 1,000 by mean intensity or prevalence)

## Outputs

- Ranked list of variable importance scores for all input features
- Subset of differential metabolite features passing the importance threshold (e.g., 377 features with importance >1.3)
- Feature rankings and importance metrics for downstream annotation

## How to apply

Load the top 1,000 most abundant metabolite features from gap-filled and non-gap-filled preprocessed feature tables separately. Train a random-forest classifier (using the R RandomForest package or equivalent) with the industrialization group (or your categorical outcome) as the target variable, incrementally increasing tree count from 5 to 200 until the out-of-bag error plateaus—this convergence ensures the model is stable and not overfitting. Extract variable importance scores from the trained model for all features. Apply a quantitative threshold (e.g., >1.3, or your domain-specific cutoff based on pilot runs or prior studies) to subset features, retaining only those exceeding the threshold. Validate by comparing results across gap-filled and non-gap-filled variants; consistency strengthens confidence in the selected features. Export the final feature set (e.g., 377 features in the reference study) as a ranked list for annotation.

## Related tools

- **RandomForest (R package)** (Train ensemble classifier to compute variable importance scores for metabolite feature ranking and selection)
- **R programming language** (Environment for implementing random-forest training, threshold filtering, and feature table manipulation)
- **Jupyter Notebook** (Reproducible notebook environment for documenting and executing the feature selection workflow) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Train random forest on top 1,000 abundant features; extract importance and filter to >1.3
library(randomForest)
rf_model <- randomForest(industrialization_group ~ ., data=top_1000_features, ntree=200, importance=TRUE)
importance_scores <- importance(rf_model)
selected_features <- names(importance_scores[importance_scores[,1] > 1.3])
write.csv(selected_features, 'differential_features_377.csv')
```

## Evaluation signals

- Out-of-bag error converges (plateaus) as tree count increases from 5 to 200, indicating model stability and adequate ensemble size.
- Variable importance scores exhibit a clear separation between top-ranked and low-ranked features; sharp elbows in the sorted importance curve suggest a natural threshold region.
- Results are consistent across gap-filled and non-gap-filled data variants; large discrepancies suggest data preprocessing or model instability issues.
- Selected features are enriched for known biological signals (e.g., amino acid–conjugated bile acids, differential metabolites in literature) or can be annotated to known metabolites at high rate (e.g., >40% compound-level annotation).
- Downstream statistical validation (e.g., Kruskal-Wallis or ANOVA on selected features) confirms that retained features show significant group differences (p < 0.05 or lower, depending on multiple-testing correction).

## Limitations

- Variable importance scores are specific to the training set and outcome variable; retraining is required for different cohorts or outcomes, limiting cross-study generalizability.
- The threshold cutoff (e.g., >1.3) must be manually chosen and validated; no consensus heuristic exists for setting it, and performance is sensitive to this choice.
- Random-forest selection does not account for feature correlation or multicollinearity; highly correlated metabolites may appear redundantly in the selected set.
- Computational cost scales with the number of input features and samples; training on very large feature tables (>10,000 features) or cohorts (>1,000 samples) may be slow.
- The method does not explicitly control for batch effects, storage delays, or other technical covariates; these must be addressed in preprocessing or incorporated as nuisance variables in the model.

## Evidence

- [results] we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features: "we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features"
- [results] After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
- [other] tree count gradually increased from 5 to 200 until out-of-bag error plateaus, using industrialization group as the target variable: "tree count gradually increased from 5 to 200 until out-of-bag error plateaus, using industrialization group as the target variable"
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook links at: https://github.com/jhaffner09/core_metabolome_2021: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook links at: https://github.com/jhaffner09/core_metabolome_2021"
