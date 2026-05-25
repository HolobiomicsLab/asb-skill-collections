---
name: random-forest-model-training
description: Train a random-forest classifier on metabolomic feature data to identify features predictive of categorical phenotypes (e.g., industrialization group), with tree count iteratively increased until out-of-bag error stabilizes. This skill surfaces variable-importance scores for subsequent feature selection and filtering.
when_to_use_negative:
- Input feature table has already been dimensionally reduced to a small, curated set; random forests perform best with hundreds of candidate features, not dozens.
- Your outcome is continuous (e.g., abundance value, metabolite concentration); use random-forest regression instead of classification.
- You have only a handful of samples (<20); random-forest models require sufficient samples to estimate stable feature importances and OOB error.
edam_operation: http://edamontology.org/operation_2426
edam_topics:
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3673
tools:
- name: RandomForest
  role: R package used to train the random-forest classifier on the top 1,000 metabolite features, iterating tree count until OOB error plateaus
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: R programming language
  role: Environment for loading feature tables, training random-forest models, extracting importance scores, and filtering features by threshold
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: Jupyter Notebook
  role: Interactive notebook interface documenting the random-forest workflow and variable-importance filtering steps
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/random-forest-model-training@sha256:91835b06128e9f3793cda519d84f3761f76cca8a4a4581347cbf376968504dac
---

# random-forest-model-training

## Summary

Train a random-forest classifier on metabolomic feature data to identify features predictive of categorical phenotypes (e.g., industrialization group), with tree count iteratively increased until out-of-bag error stabilizes. This skill surfaces variable-importance scores for subsequent feature selection and filtering.

## When to use

You have preprocessed metabolomic feature tables (gap-filled and/or non-gap-filled) with a categorical outcome (e.g., industrialization group, disease status), and you want to rank features by their predictive utility and identify a subset of differential features that drive group separation. Apply this skill when univariate tests alone are insufficient and you need a multivariate, ensemble approach to capture feature interactions and nonlinearity.

## When NOT to use

- Input feature table has already been dimensionally reduced to a small, curated set; random forests perform best with hundreds of candidate features, not dozens.
- Your outcome is continuous (e.g., abundance value, metabolite concentration); use random-forest regression instead of classification.
- You have only a handful of samples (<20); random-forest models require sufficient samples to estimate stable feature importances and OOB error.

## Inputs

- metabolite feature table (numeric matrix, features × samples)
- top 1,000 most abundant features (pre-filtered)
- categorical phenotype vector (e.g., industrialization group labels)
- gap-filled and non-gap-filled variants (analyzed separately)

## Outputs

- trained random-forest model object
- variable-importance scores (one per feature)
- subset of differential features meeting importance threshold (e.g., 377 features at >1.3)
- feature list with importance rankings for downstream annotation

## How to apply

Load the top 1,000 most abundant metabolite features from your preprocessed feature table and format them as a numeric matrix with industrialization group (or equivalent categorical phenotype) as the target variable. Use the R RandomForest package to train a classifier, starting with 5 trees and gradually increasing the tree count (e.g., 5, 10, 20, 50, 100, 150, 200) until the out-of-bag (OOB) error plateaus, indicating further trees add no new information. Extract variable-importance scores for all features from the final trained model. Apply a variable-importance threshold (e.g., >1.3) to subset features with the strongest predictive signal. The rationale is that iterating tree count to OOB plateau avoids overfitting while maximizing stability of importance estimates, and the threshold cutoff reduces the feature space to annotation-friendly size (the study reduced 1,000 features to 377 at threshold >1.3).

## Related tools

- **RandomForest** (R package used to train the random-forest classifier on the top 1,000 metabolite features, iterating tree count until OOB error plateaus) — https://github.com/jhaffner09/core_metabolome_2021
- **R programming language** (Environment for loading feature tables, training random-forest models, extracting importance scores, and filtering features by threshold) — https://github.com/jhaffner09/core_metabolome_2021
- **Jupyter Notebook** (Interactive notebook interface documenting the random-forest workflow and variable-importance filtering steps) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# In R: Load top 1,000 features and train random forest
library(randomForest)
rf_model <- randomForest(industrialization_group ~ ., data=feature_data[,1:1000], ntree=200, importance=TRUE)
importances <- importance(rf_model)
thresholded_features <- rownames(importances)[importances[,'MeanDecreaseGini'] > 1.3]
```

## Evaluation signals

- Out-of-bag (OOB) error reaches a plateau (no substantial decrease) as tree count increases from 5 to 200, indicating model stability and absence of overfitting.
- Variable-importance scores are non-negative, ranked, and the top features show biological plausibility (e.g., metabolites known to vary with industrialization or health state).
- After thresholding at >1.3, the number of retained features (e.g., 377) falls within an annotation-feasible range and reflects meaningful dimensionality reduction from the input 1,000.
- Gap-filled and non-gap-filled variants yield consistent ranking of top features, confirming robustness to preprocessing artifacts.
- Downstream univariate tests (e.g., Kruskal-Wallis) on the thresholded feature set confirm that most features show significant association with the outcome (e.g., p < 0.05 after multiple-testing correction).

## Limitations

- Random forests require sufficient sample size to reliably estimate feature importances; studies with <20 samples per group will yield unstable rankings.
- Importance scores are biased toward high-cardinality features and features with high variance; normalization or scaling of input features may be necessary.
- The variable-importance threshold (e.g., >1.3) is chosen empirically and may not be optimal for all datasets; the study does not provide a formal justification for this cutoff, and thresholds should be validated against external cohorts or cross-validation.
- Random forests do not provide p-values or confidence intervals on importances; downstream statistical tests (e.g., Kruskal-Wallis) are needed to confirm biological significance of selected features.
- The 'top 1,000 most abundant features' input constraint discards rare but potentially informative features; preprocessing and feature-selection criteria may bias the final result.

## Evidence

- [results] we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features: "we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features"
- [results] After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
- [other] Train a random-forest classifier using the R package RandomForest with tree count gradually increased from 5 to 200 until out-of-bag error plateaus: "Train a random-forest classifier using the R package RandomForest with tree count gradually increased from 5 to 200 until out-of-bag error plateaus"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021"
