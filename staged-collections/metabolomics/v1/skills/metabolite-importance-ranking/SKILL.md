---
name: metabolite-importance-ranking
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to rank metabolite features by variable importance scores from a random-forest classifier trained on industrialization group membership and apply a quantitative threshold to identify differential metabolites for downstream annotation.
when_to_use_negative:
- Input is already a curated, annotated feature list (e.g., from targeted metabolomics or pre-filtered databases) — ranking is designed for discovery in untargeted, high-dimensional data.
- Experimental variable is continuous (e.g., age, BMI) rather than categorical — random-forest variable importance is most interpretable for classification; regression importance may differ.
- Sample size is very small (<20 samples per group) — random-forest estimates of importance become unstable and out-of-bag error plateau may not be reliable.
edam_operation: http://edamontology.org/operation_2238
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: RandomForest (R package)
  role: Train random-forest classifier on top 1,000 most abundant features, with tree count incremented from 5 to 200 until out-of-bag error plateaus; extract variable importance scores for each feature.
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: R programming language
  role: Environment for running random-forest model training, importance extraction, and threshold filtering.
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: Jupyter Notebook
  role: Interactive code documentation and reproducible workflow execution for the ranking and filtering pipeline.
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/metabolite-importance-ranking/SKILL.md
    - outputs/audit_haffner_v2/skills/metabolite-importance-ranking/skill.md
    merged_at: '2026-05-25T06:57:01.481014+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-importance-ranking@sha256:760b35f66a60eeb9247863f97bee77209d095155ce7de359d48a948171b8b60c
derived_from:
- doi: 10.1128/msystems.00710-22
---

# metabolite-importance-ranking

## Summary

Rank metabolite features by variable importance scores from a random-forest classifier trained on industrialization group membership, then apply a quantitative threshold to identify differential metabolites for downstream annotation. This skill distills high-dimensional untargeted metabolomic data into a curated set of features most predictive of the experimental condition.

## When to use

When you have preprocessed, abundance-normalized metabolite feature tables (gap-filled and/or non-gap-filled variants) and a categorical experimental variable (e.g., industrialization level, disease status, treatment group), and you need to identify which of hundreds or thousands of features are most predictive of that variable for prioritization in annotation and mechanistic follow-up.

## When NOT to use

- Input is already a curated, annotated feature list (e.g., from targeted metabolomics or pre-filtered databases) — ranking is designed for discovery in untargeted, high-dimensional data.
- Experimental variable is continuous (e.g., age, BMI) rather than categorical — random-forest variable importance is most interpretable for classification; regression importance may differ.
- Sample size is very small (<20 samples per group) — random-forest estimates of importance become unstable and out-of-bag error plateau may not be reliable.

## Inputs

- preprocessed metabolite feature table (gap-filled variant)
- preprocessed metabolite feature table (non-gap-filled variant)
- categorical experimental group variable (e.g., industrialization level)

## Outputs

- ranked variable-importance scores for top 1,000 metabolite features
- subset of differential metabolite features (377 in the article example) passing importance threshold >1.3
- feature identifiers and importance values for downstream annotation

## How to apply

First, restrict the input to the top 1,000 most abundant metabolite features to reduce noise and computational cost. Train a random-forest classifier using industrialization group (or your target variable) as the outcome, incrementally increasing tree count from 5 to 200 until out-of-bag error plateaus, to ensure model stability. Extract variable importance scores for all 1,000 features from the trained model. Apply a variable-importance threshold of >1.3 (or a threshold calibrated to your dataset and biological context) to subset features; this threshold is data-specific and should be justified by effect-size, interpretability, or cross-validation studies. Retain only features exceeding the cutoff for annotation. Optionally, run this pipeline on both gap-filled and non-gap-filled data variants separately for transparency and robustness checking.

## Related tools

- **RandomForest (R package)** (Train random-forest classifier on top 1,000 most abundant features, with tree count incremented from 5 to 200 until out-of-bag error plateaus; extract variable importance scores for each feature.) — https://github.com/jhaffner09/core_metabolome_2021
- **R programming language** (Environment for running random-forest model training, importance extraction, and threshold filtering.) — https://github.com/jhaffner09/core_metabolome_2021
- **Jupyter Notebook** (Interactive code documentation and reproducible workflow execution for the ranking and filtering pipeline.) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Train random forest on top 1,000 features, extract importance, subset to >1.3
rf_model <- randomForest(industrialization_group ~ ., data = top_1000_features, ntree = 200, importance = TRUE); importance_scores <- importance(rf_model); differential_features <- names(importance_scores[importance_scores > 1.3])
```

## Evaluation signals

- Out-of-bag error from the random-forest model plateaus, indicating the model is stable and not overfitting with increased tree count.
- The variable-importance threshold (>1.3) yields a biologically interpretable number of features (e.g., 377 in this study, representing ~38% of the input 1,000 features).
- Gap-filled and non-gap-filled analyses produce consistent rankings and similar subsets of differential features, confirming robustness to imputation strategy.
- Annotated features in the differential set (e.g., leucyl-leucine, urobilin, bile acids) show independent statistical significance in univariate tests (Kruskal-Wallis or ANOVA) with biologically coherent patterns across industrialization levels.
- Cross-validation or holdout-test performance confirms that features with importance >1.3 maintain predictive power on independent data.

## Limitations

- Variable-importance threshold of >1.3 is empirical and article-specific; generalization to other datasets requires validation or recalibration to avoid arbitrary feature selection.
- Random-forest importance does not distinguish causality from correlation; high-importance features may be biomarkers rather than mechanistic drivers.
- Restriction to the top 1,000 most abundant features may exclude rare but biologically important metabolites; abundance-based filtering can introduce bias.
- Out-of-bag error plateau is a heuristic criterion; the optimal tree count depends on data dimensionality and may differ across datasets.
- The ranking is relative to the specific categorical variable used (e.g., industrialization); reordering or subset of samples can shift importances.

## Evidence

- [results] we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features: "we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features"
- [results] After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
- [other] tree count gradually increased from 5 to 200 until out-of-bag error plateaus: "Train a random-forest classifier using the R package RandomForest with tree count gradually increased from 5 to 200 until out-of-bag error plateaus, using industrialization group as the target"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook links at: https://github.com/jhaffner09/core_metabolome_2021: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
