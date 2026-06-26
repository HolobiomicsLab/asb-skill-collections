---
name: cross-validated-model-performance-evaluation-10fold
description: Use when when you have trained a neural network or regression model to
  predict metabolite abundances from microbiome features and need to measure how well
  the model generalizes to unseen samples. Apply this skill when you want to compare
  multiple competing models (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0625
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - SciPy
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome
  abundance features (green) are used to train a neural network to predict metabolite
  abundance features (blue).
- we first compared MiMeNet to MelonnPan, a recent model that uses Elastic Net linear
  regression
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest
  (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- The NED model was trained using code downloaded from https://github.com/vuongle2/BiomeNED
- MelonnPan and NED models were obtained from their respective GitHub repositories
  and executed using default parameters as according to their tutorials. Random Forest,
  multivariate Elastic Net, and
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-validated-model-performance-evaluation-10fold

## Summary

Evaluate predictive model performance on paired microbiome-metabolome data using repeated 10-fold cross-validation, computing mean Spearman correlation coefficients (SCCs) as the primary metric to assess generalization ability across held-out samples.

## When to use

When you have trained a neural network or regression model to predict metabolite abundances from microbiome features and need to measure how well the model generalizes to unseen samples. Apply this skill when you want to compare multiple competing models (e.g., MiMeNet vs. MelonnPan) on the same dataset using a consistent, replicable evaluation protocol.

## When NOT to use

- Input data contains fewer than ~50 samples — 10-fold CV may produce unstable folds and unreliable SCC estimates.
- Model was already evaluated on a separate external test set — do not re-apply 10-fold CV on the same training data to avoid optimistic bias.
- You are performing hyperparameter tuning — nested cross-validation (outer loop for evaluation, inner loop for tuning) is required; this skill documents the outer evaluation only.

## Inputs

- Paired microbiome feature table (samples × genera/taxa, centered log-ratio transformed)
- Paired metabolome feature table (samples × metabolites, centered log-ratio transformed)
- Trained model (neural network weights or fitted Elastic Net coefficients)
- Cross-validation fold assignments (or random seed for reproducible fold generation)

## Outputs

- Mean Spearman correlation coefficient (SCC) across all folds and iterations
- Per-fold SCC values for each metabolite (for filtering well-predicted metabolites)
- Count of well-predicted metabolites (SCC ≥ 95th percentile threshold)
- Summary statistics table (mean SCC, metabolite count, improvement ratio vs. baseline)

## How to apply

Perform 10 iterations of 10-fold cross-validation on your paired microbiome-metabolome dataset: in each iteration, partition samples into 10 folds, train the model on 9 folds, and evaluate on the held-out fold. For each fold, compute the Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances. Average the SCCs across all folds and all iterations to produce a mean SCC metric. Document the fold-level correlations to allow downstream identification of well-predicted metabolites (those with SCC above a significance threshold derived from a background distribution). Report mean SCC alongside the count of well-predicted metabolites as the primary performance summary.

## Related tools

- **MiMeNet** (Multi-layer perceptron neural network trained and evaluated via 10-fold cross-validation to predict metabolite abundances from microbiome features) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net linear regression baseline model evaluated using the same 10-fold cross-validation protocol for direct performance comparison) — https://github.com/biobakery/melonnpan
- **scikit-learn** (Python library providing cross-validation fold generation and Spearman correlation coefficient computation)
- **TensorFlow** (Deep learning framework used to train MiMeNet neural networks during cross-validation iterations)
- **SciPy** (Python library for computing Spearman rank correlation coefficients between predicted and observed metabolite abundances)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_cv 10 -output IBD_results
```

## Evaluation signals

- Mean SCC is substantially higher than the 95th percentile background SCC threshold (e.g., 0.309 vs. 0.136 on IBD PRISM data), confirming signal above random shuffling baseline.
- Per-fold SCC values show low variance across folds and iterations, indicating stable model generalization (not driven by a single lucky fold).
- Count of well-predicted metabolites (SCC ≥ 95th percentile) is large relative to total metabolites tested (e.g., >4% of metabolites), and consistent across cross-validation runs.
- Comparison to baseline models (e.g., MelonnPan, Random Forest) shows improvement in mean SCC and metabolite count that is directionally consistent across all three datasets (IBD, CF, soil).
- External validation cohort (if available) produces SCC values in the same range as cross-validated training SCC, not substantially lower, confirming absence of overfitting.

## Limitations

- 10-fold CV assumes samples are independent; longitudinal or paired samples (e.g., soil data collected at multiple timepoints) may inflate correlation estimates if timepoints are split across folds.
- Mean SCC aggregation masks per-metabolite performance variation: some metabolites may be well-predicted while others remain poor predictors, but this heterogeneity is not visible in the aggregate metric.
- Not all metabolites may be associated with microbes; true biological non-association appears as low SCC and reduces overall mean correlation, which can be misinterpreted as model failure rather than biological reality.
- Threshold for well-predicted metabolites (95th percentile of background) is arbitrary; results are sensitive to choice of percentile and to the background generation procedure (shuffling strategy).
- Results are dataset-specific: thresholds and mean SCC values differ across environments (IBD threshold 0.136, CF 0.129, soil 0.410), requiring re-calibration for new environments.

## Evidence

- [abstract] Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets: "Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [abstract] MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264): "mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264"
- [results] Train multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [readme] num_run_cv | Number of iterations for cross-validation: "Number of iterations for cross-validation"
- [readme] num_cv | Number of cross-validated folds: "Number of cross-validated folds"
