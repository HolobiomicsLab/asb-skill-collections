---
name: neural-network-hyperparameter-tuning
description: Use when when training a neural network to predict metabolite abundances from microbiome data (or similar paired multivariate omics prediction tasks) and you need to avoid overfitting while maximizing predictive accuracy on held-out test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - neural networks
  - neural networks (MLPNN with ReLU activation)
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - WGCNA
  - TensorFlow
  - scikit-learn
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers
- we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships
- In MiMeNet, φ is set as the rectified linear unit (ReLU).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- these models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate Elastic Net, and Canonical
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
schema_version: 0.2.0
---

# neural-network-hyperparameter-tuning

## Summary

Systematic tuning of multilayer perceptron neural network architecture and regularization parameters to optimize prediction of metabolite abundances from microbiome features. This skill uses nested cross-validation to select optimal layer size, number of layers, L2 regularization penalty, and dropout rates before final model evaluation.

## When to use

When training a neural network to predict metabolite abundances from microbiome data (or similar paired multivariate omics prediction tasks) and you need to avoid overfitting while maximizing predictive accuracy on held-out test data. Apply this skill before the main cross-validated evaluation workflow to prevent data leakage and ensure hyperparameters are selected independently of the test folds.

## When NOT to use

- Input data has already been split into train and test sets with hyperparameters tuned on the test set (data leakage will invalidate results)
- Sample size is <50 (nested cross-validation may be unstable; consider single-level tuning or Bayesian optimization instead)
- Hyperparameters are fixed by prior knowledge or external guidance; tuning is redundant

## Inputs

- Paired microbiome (microbial feature abundance table) and metabolome (metabolite abundance table) CSV files with samples in rows and features in columns
- Preprocessed and normalized data (centered log-ratio or relative abundance transformed, features present in <10% of samples removed)
- Training set indices or fold assignments for outer cross-validation

## Outputs

- Optimal hyperparameter set: layer size (integer), number of layers (integer), L2 regularization penalty λ (float), dropout rate (float)
- Validation loss trajectory for each hyperparameter combination
- Selected MLPNN architecture specification ready for main model training

## How to apply

Execute nested cross-validation on the training data: within each fold of an outer 10-fold cross-validation, use an inner 5-fold cross-validation to grid-search over the hyperparameter space (layer size ∈ {32, 128, 512}, number of layers ∈ {1, 2, 3}, L2 penalty λ evenly spaced on log scale from 0.0001–0.1, dropout rate ∈ {0.1, 0.3, 0.5}). For each hyperparameter combination, train the MLPNN with ReLU activation, ADAM optimizer, and mean squared error loss, applying early stopping when validation loss does not improve within 40 iterations. Select the combination that minimizes validation loss on the inner fold. Record these optimal hyperparameters for reuse across the outer cross-validation folds (or re-tune per fold if you have sufficient data and compute). The rationale is that nested validation isolates the tuning process from the test set, preventing optimistic bias in final performance metrics.

## Related tools

- **TensorFlow** (Deep learning framework used to construct and train the MLPNN with specified architecture, ReLU activation, ADAM optimizer, and early stopping)
- **scikit-learn** (Used for cross-validation splitting (KFold) and hyperparameter grid search infrastructure)
- **MiMeNet** (Reference implementation that applies this skill; see YDaiLab/MiMeNet repository for concrete code and parameter ranges) — https://github.com/YDaiLab/MiMeNet

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -output IBD
```

## Evaluation signals

- Nested cross-validation structure is enforced: inner grid search results (e.g., best λ and dropout per outer fold) are logged and differ across outer folds, confirming independence from test data
- Validation loss improves monotonically during inner fold training until early stopping criterion (40 iterations without improvement) is triggered
- Selected hyperparameters fall within the specified grid bounds: layer size ∈ {32, 128, 512}, λ ∈ [0.0001, 0.1] on log scale, dropout ∈ {0.1, 0.3, 0.5}
- When hyperparameters are fixed (shared) across all outer folds, final mean Spearman correlation coefficient on the full 10-fold cross-validation should remain competitive with per-fold tuning (within ~5% difference, as observed in task_005 on IBD PRISM dataset)
- Validation loss on inner folds is lower than the corresponding training loss on the same fold, indicating appropriate regularization and early stopping

## Limitations

- Nested cross-validation is computationally expensive: O(K_outer × K_inner × |hyperparameter_grid|) model trains required. For large datasets or many hyperparameters, consider Bayesian optimization or random search instead.
- Grid search does not adapt to data characteristics; optimal hyperparameters may vary by dataset (as noted in task_005: CF showed slight decrease with per-partition tuning despite IBD improvement), suggesting that once-tuned hyperparameters may not generalize across cohorts
- Early stopping patience (40 iterations) is fixed; no guidance provided on how to adjust this for different dataset sizes or convergence rates
- L2 regularization penalty is tuned on a log scale with 0.0001–0.1 range; outside this range (very weak or very strong regularization) is not explored
- No integration with external validation datasets during tuning; hyperparameters selected on internal cross-validation may not be optimal when evaluated on held-out external cohorts

## Evidence

- [methods] The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters for the number and size of the hidden layers, the L2 regularization penalty parameter, and the dropout rate using nested 5-fold cross-validation: "The network architecture in MiMeNet is first determined for each paired dataset by tuning the hyperparameters for the number and size of the hidden layers, the L2 regularization penalty parameter,"
- [other] Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each dataset.: "Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each"
- [other] Train MLPNN models with ReLU activation, L2 regularization, dropout, ADAM optimizer, and MSE loss; apply early stopping when validation loss does not improve within 40 iterations.: "Train MLPNN models with ReLU activation, L2 regularization, dropout, ADAM optimizer, and MSE loss; apply early stopping when validation loss does not improve within 40 iterations."
- [other] hyperparameters (layer size, number of layers, L2 penalty λ, dropout rate) are tuned once on the first training partition using nested 5-fold cross-validation over a grid (layer size ∈ {32, 128, 512}, λ evenly spaced on log scale 0.0001–0.1, dropout ∈ {0.1, 0.3, 0.5}): "hyperparameters (layer size, number of layers, L2 penalty λ, dropout rate) are tuned once on the first training partition using nested 5-fold cross-validation over a grid (layer size ∈ {32, 128,"
- [other] per-partition tuning increased mean SCC while cystic fibrosis showed a slight decrease, yet 141 of 143 significantly correlated metabolites were still identified with shared hyperparameters: "per-partition tuning increased mean SCC while cystic fibrosis showed a slight decrease, yet 141 of 143 significantly correlated metabolites were still identified with shared hyperparameters"
- [readme] net_params: JSON file containing neural network number of layers, layer size, L2 penalty, and dropout rate: "net_params: JSON file containing neural network number of layers, layer size, L2 penalty, and dropout rate"
