---
name: differential-feature-identification
description: Use when metabolomics involves LC-MS or GC-MS untargeted lipidomics to identify metabolite features associated with a categorical experimental variable by training a random-forest classifier on high-abundance features and filtering by variable-importance score.
when_to_use_negative:
- Input feature table is already heavily pre-filtered to a small set (e.g., <100 features); random-forest variable importance may be unstable or overfitting due to small feature count relative to sample count.
- Categorical grouping variable has very imbalanced class sizes (e.g., 95% samples in one group, 5% in another); random-forest importance can be biased toward the majority class, and the selected features may not generalize to minority populations.
- You require per-feature p-values, confidence intervals, or effect sizes; random-forest variable importance is a relative ranking without formal statistical inference—use univariate tests (e.g., Kruskal-Wallis, ANOVA) if statistical significance and direction are critical.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0625
tools:
- name: RandomForest R package
  role: Train random-forest classifier on top abundant features to compute variable-importance scores for feature ranking and selection.
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: R programming language
  role: Environment for random-forest model training, feature filtering by population presence, and threshold application.
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: Jupyter Notebook
  role: Interactive interface for executing and documenting the random-forest feature selection workflow in R and Python.
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/differential-feature-identification@sha256:8da47ac0cae03088a6410a175d36396879a693f9ec26ba2b5fb3f36ad9ddd9a9
---

# differential-feature-identification

## Summary

Identify metabolite features most strongly associated with a categorical experimental variable (e.g., industrialization group) by training a random-forest classifier on high-abundance features and filtering results by variable-importance score. This skill ranks features by their predictive power and retains only those exceeding a statistical threshold, yielding a curated set of candidate differential features for downstream annotation and validation.

## When to use

You have a preprocessed feature table (gap-filled or non-gap-filled metabolite intensities) stratified by a categorical grouping variable (e.g., industrialization level, disease status, treatment), and you need to discover which individual features are most informative for discriminating between groups. Use this skill after filtering features by prevalence/abundance (e.g., top 1,000 most abundant) but before detailed annotation or mechanistic interpretation.

## When NOT to use

- Input feature table is already heavily pre-filtered to a small set (e.g., <100 features); random-forest variable importance may be unstable or overfitting due to small feature count relative to sample count.
- Categorical grouping variable has very imbalanced class sizes (e.g., 95% samples in one group, 5% in another); random-forest importance can be biased toward the majority class, and the selected features may not generalize to minority populations.
- You require per-feature p-values, confidence intervals, or effect sizes; random-forest variable importance is a relative ranking without formal statistical inference—use univariate tests (e.g., Kruskal-Wallis, ANOVA) if statistical significance and direction are critical.

## Inputs

- preprocessed metabolite feature table (gap-filled or non-gap-filled, rows=samples, columns=m/z-RT or feature IDs, values=peak intensities)
- categorical grouping variable (e.g., industrialization group, population, treatment assignment)
- top N most abundant features subset (e.g., top 1,000 ranked by median or mean intensity)

## Outputs

- ranked feature list with variable-importance scores (all input features scored)
- filtered differential feature set (subset meeting importance cutoff, e.g., 377 features for importance >1.3)
- random-forest model object (for inspection of out-of-bag error, feature rankings, tree structure)

## How to apply

Load the top 1,000 most abundant metabolite features from your preprocessed feature table. Train a random-forest classifier (e.g., R package RandomForest) on these features, using your categorical grouping variable as the target; incrementally increase tree count from 5 to 200 until out-of-bag error plateaus, ensuring stable variable importance estimates. Extract variable-importance scores for all features from the fitted model. Apply a variable-importance threshold (e.g., >1.3, tuned by domain knowledge or cross-validation) to subset features. Retain only features meeting the threshold as your differential feature set. This two-stage filter (abundance-based pre-filter followed by importance-based selection) balances statistical power with computational efficiency and reduces multiple-testing burden.

## Related tools

- **RandomForest R package** (Train random-forest classifier on top abundant features to compute variable-importance scores for feature ranking and selection.) — https://github.com/jhaffner09/core_metabolome_2021
- **R programming language** (Environment for random-forest model training, feature filtering by population presence, and threshold application.) — https://github.com/jhaffner09/core_metabolome_2021
- **Jupyter Notebook** (Interactive interface for executing and documenting the random-forest feature selection workflow in R and Python.) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Load top 1,000 features; train RF with increasing trees until OOB stabilizes; extract & filter importance scores
library(randomForest)
rf_model <- randomForest(industrialization_group ~ ., data=top_1000_features, ntree=200, importance=TRUE)
vi_scores <- importance(rf_model)[,1]
differential_features <- names(vi_scores[vi_scores > 1.3])
# Result: 377 features meeting cutoff for annotation
```

## Evaluation signals

- Out-of-bag (OOB) error from the random-forest model should plateau and stabilize as tree count increases from 5 to 200, confirming convergence and reliable variable-importance estimates.
- Variable-importance scores should be non-negative and sum to a stable total; compare distributions before and after threshold to ensure cutoff is neither too stringent (retaining <50 features) nor too lenient (retaining >50% of input features).
- Differential features should show statistically significant univariate association with the grouping variable (e.g., Kruskal-Wallis p < 0.001 for top features), validating that random-forest selection agrees with single-feature tests.
- Retained differential features should exhibit biological plausibility: enrichment in expected metabolite classes (e.g., bile acids in industrialized populations), consistency across gap-filled and non-gap-filled variants, and enrichment in public reference databases (e.g., HFMDB, GNPS) for later annotation.
- Feature presence/absence patterns should be balanced across grouping categories—if all top features are missing in one group, this signals data imbalance or preprocessing artifacts rather than true differential abundance.

## Limitations

- Random-forest variable importance is a relative ranking without formal p-values; features below the threshold are not statistically insignificant, only lower-ranked predictors. Multiple-testing correction is not applied to importance scores.
- Choice of importance cutoff (e.g., >1.3) is heuristic and data-dependent; no universal threshold exists. Cross-validation or permutation testing can validate stability, but final cutoff should be tuned for the specific metabolome and biological question.
- Random-forest importance can be inflated for rare features or those with high variance; pre-filtering to the top 1,000 most abundant features helps mitigate this but may exclude rare biomarkers of biological interest.
- Results assume the categorical grouping variable is well-defined and non-overlapping; confounding variables (e.g., age, sex, storage delay) may inflate importance scores for features correlated with confounders rather than the primary variable of interest.
- Out-of-bag error plateau may not be reached within 200 trees for very high-dimensional data or weak class separation; in such cases, importance estimates remain noisy and feature selection may be unreliable.

## Evidence

- [results] we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features: "we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features"
- [results] After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
- [other] Train a random-forest classifier using the R package RandomForest with tree count gradually increased from 5 to 200 until out-of-bag error plateaus: "Train a random-forest classifier using the R package RandomForest with tree count gradually increased from 5 to 200 until out-of-bag error plateaus"
- [other] Extract variable importance scores for all features from the trained random-forest model: "Extract variable importance scores for all features from the trained random-forest model"
- [other] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook links at: https://github.com/jhaffner09/core_metabolome_2021: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook"
