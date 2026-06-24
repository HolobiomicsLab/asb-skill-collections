---
name: multi-regime-model-performance-comparison-visualization
description: Use when you have paired microbiome-metabolome (or similar multivariate)
  datasets and want to quantify whether training on a superset of features (e.g.,
  both annotated and unannotated metabolites) improves prediction accuracy for a well-defined
  target subset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0769
  tools:
  - MiMeNet
  - ADAM optimizer
  - Python (scikit-learn, seaborn, or matplotlib for visualization)
  - TensorFlow
  - scikit-learn
  - SciPy
  - matplotlib / seaborn
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
- using Seaborn's clustermap function in Python
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
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

# multi-regime-model-performance-comparison-visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare predictive performance of machine learning models trained under different data regimes (e.g., all features vs. subset-only) by computing correlation coefficients across independent cross-validation folds and visualizing per-outcome effect sizes. This reveals whether incorporating broader feature sets improves predictions for a target output class.

## When to use

You have paired microbiome-metabolome (or similar multivariate) datasets and want to quantify whether training on a superset of features (e.g., both annotated and unannotated metabolites) improves prediction accuracy for a well-defined target subset (e.g., annotated metabolites only), compared to training on the target subset alone. Use this skill when you suspect latent information in unannotated features can inform prediction of annotated ones.

## When NOT to use

- Input datasets are unpaired (microbiome and metabolome from different cohorts or timepoints) — cross-regime comparison assumes the same samples and ecosystem context.
- Target subset (e.g., annotated metabolites) has no natural partitioning — the skill requires a biologically or operationally meaningful distinction between features used for training.
- Sample size is very small (n < 20) or cross-validation fold count is < 5 — the statistical power to detect regime differences may be insufficient, and correlation estimates become unstable.

## Inputs

- paired microbiome-metabolome count matrices (samples × features)
- feature annotation file identifying target subset (e.g., annotated metabolites)
- neural network hyperparameter specification (layer sizes, L2 penalty, dropout, activation function)
- cross-validation split parameters (train fraction, number of folds, number of iterations)

## Outputs

- scatterplot comparing SCC values for target outputs across both training regimes
- per-output delta scores (SCC_all − SCC_annotated_only)
- mean SCC table per regime (rows=outputs, columns=regime)
- count of well-predicted outputs per regime (e.g., outputs with SCC > threshold)
- summary statistics (overall mean delta, confidence interval, p-value from paired test)

## How to apply

Train two identically configured neural network models in parallel: one on the complete feature set (all metabolites) and one on the target subset (annotated-only), using the same hyperparameters (layer size, L2 penalty, dropout, optimizer), split strategy (80/20 train-test), and cross-validation scheme (e.g., 10 iterations of 10-fold CV). For each held-out test fold across all CV iterations, calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each target output (annotated metabolite). Compute mean SCC per output for each training regime, then generate a scatterplot with one regime on each axis and overlay the diagonal (y=x line); calculate per-output delta (SCC_all − SCC_annotated_only) and overall mean delta. Statistical significance can be assessed via paired t-tests across the 100 cross-validation runs. This design isolates the effect of training data composition while holding architecture and evaluation constant.

## Related tools

- **MiMeNet** (Multi-layer perceptron neural network framework for training and evaluating dual-regime metabolome prediction models with configurable hyperparameters and cross-validation) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow** (Deep learning backend for constructing and training MLPNN models in dual regimes)
- **scikit-learn** (Preprocessing, train-test splitting, and cross-validation orchestration)
- **SciPy** (Spearman correlation coefficient computation and statistical significance testing)
- **matplotlib / seaborn** (Scatterplot visualization of per-output SCC comparisons and effect size distributions)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -annotation data/IBD/metabolome_annotation.csv -num_run_cv 10 -num_cv 10 -output results_all_metabolites && python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -annotation data/IBD/metabolome_annotation.csv -num_run_cv 10 -num_cv 10 -output results_annotated_only
```

## Evaluation signals

- Scatterplot shows systematic deviation from the diagonal (y=x line): if all-metabolite training consistently predicts annotated metabolites better, points should cluster above the diagonal, and mean delta should be positive and statistically significant (p < 0.05 from paired t-test across 100 CV runs).
- Count of well-predicted annotated metabolites increases in the all-metabolite regime (e.g., from 333 to 366 out of 466 in the article's example), and this gain is robust across CV folds (low variance in per-fold counts).
- Per-metabolite delta scores are consistent in sign across CV iterations (e.g., if delta > 0 for metabolite X in fold 1, similar ordering holds in folds 2–10), indicating the regime effect is not an artifact of fold-specific sampling.
- Mean SCC values for both regimes fall within the expected range given the background distribution (generated via shuffling); absence of obviously out-of-range predictions suggests proper model convergence and hyperparameter tuning.
- Hyperparameter specifications (layer size, L2 penalty, dropout, activation) are identical between regimes; deviations in performance are attributable to feature set composition, not architecture differences.

## Limitations

- Not all metabolites may be associated with microbes, resulting in lower prediction correlations and lower overall mean correlation across all metabolites, which may obscure the regime effect for truly microbe-independent metabolites.
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge, so improved SCC in the all-metabolite regime does not prove causal relationships or biological mechanisms.
- External validation datasets may have different sample distributions, feature sparsity, or measurement error profiles than the training cohort, potentially affecting the magnitude and sign of regime effects; generalizability should be verified on independent cohorts.
- The approach assumes that unannotated features are conditionally informative given annotated features; if unannotated features are purely noise or highly correlated with annotated features, the all-metabolite regime may suffer from overfitting or redundancy.
- Cross-validation sample size and fold count affect the precision of SCC estimates and the power to detect regime differences; very small datasets or few folds may yield unstable or non-reproducible comparisons.

## Evidence

- [other] Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to 366 out of 466 annotated metabolites: "Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to"
- [other] Split data into training (80%) and validation (20%) sets, then perform 10 iterations of 10-fold cross-validation.: "Split data into training (80%) and validation (20%) sets, then perform 10 iterations of 10-fold cross-validation."
- [other] Train a separate MiMeNet MLPNN model (using optimal hyperparameters: 512-node single hidden layer, L2 penalty λ=0.001, dropout=0.5, ReLU activation) on the complete feature set (all metabolites), using ADAM optimizer and mean squared error loss: "train a separate MiMeNet MLPNN model (using optimal hyperparameters: 512-node single hidden layer, L2 penalty λ=0.001, dropout=0.5, ReLU activation) on the complete feature set (all metabolites),"
- [other] In parallel, train an identically configured MiMeNet model using only annotated metabolites as outputs.: "In parallel, train an identically configured MiMeNet model using only annotated metabolites as outputs."
- [other] Calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite across all 100 model runs (10 iterations × 10 folds).: "calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite across all 100 model runs (10 iterations × 10 folds)."
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances"
- [methods] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
