---
name: cross-validation-performance-evaluation
description: Use when when you have paired microbiome and metabolome count data and need to estimate how well a neural network or regression model can predict metabolite abundances from microbial features without overfitting to a single held-out test set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0654
  tools:
  - MiMeNet
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - scikit-learn MLPRegressor
  - SciPy Spearman correlation
  - MelonnPan
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- Canonical correlation analysis models were implemented using Python's scikit-learn package.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- In MiMeNet, φ is set as the rectified linear unit (ReLU). We selected this activation function since previous studies have shown that it is resilient to the problems of exploding and vanishing
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
---

# cross-validation-performance-evaluation

## Summary

Systematically partition paired microbiome-metabolome datasets into multiple train/validation/test folds across multiple iterations to measure prediction accuracy using Spearman correlation coefficients, producing a distribution of per-metabolite performance metrics that distinguishes signal from chance.

## When to use

When you have paired microbiome and metabolome count data and need to estimate how well a neural network or regression model can predict metabolite abundances from microbial features without overfitting to a single held-out test set. Use this skill when you need robust, reproducible performance estimates across diverse datasets (e.g., IBD, cystic fibrosis, soil) with different sample sizes, feature counts, and metabolite-microbe association strengths.

## When NOT to use

- Input microbiome or metabolome data has not been preprocessed (features present in <10% of samples should be removed; features should be transformed to CLR or relative abundance unless already normalized).
- Sample size is very small (<20 samples) — cross-validation may produce unstable fold partitions; consider leave-one-out CV or pooling with external cohorts.
- Metabolites or microbes are already filtered to only those with known associations — this skill is designed to discover which metabolites are predictable genome-wide, not to validate pre-selected features.

## Inputs

- paired microbiome count matrix (samples × microbial features, e.g., 201 microbes × 121 samples for IBD PRISM)
- paired metabolome count matrix (samples × metabolite features, e.g., 8848 metabolites × 121 samples for IBD PRISM)
- network hyperparameters (layer size, number of layers, L2 penalty λ, dropout rate) as JSON or dict
- optional: external validation microbiome and metabolome matrices

## Outputs

- mean Spearman correlation coefficient (SCC) per metabolite, averaged over all iterations and test folds
- SCC distribution across all metabolites (e.g., range -0.272 to 0.309 for IBD PRISM)
- per-fold and per-iteration SCC values for downstream statistical analysis
- trained neural network models from each CV iteration (used for feature attribution scoring in downstream modules)

## How to apply

Execute multiple iterations (e.g., 10) of k-fold cross-validation (e.g., 10 folds), where each fold splits the data into training (80% of fold), validation (20% of fold), and held-out test (10% of full data). Train a neural network (e.g., MLPNN with dataset-specific hyperparameters: layer size, number of layers, L2 regularization λ, dropout rate) on the training set using mean squared error loss with early stopping (e.g., 40 iterations without validation loss improvement). Evaluate on the held-out test set and compute the Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances for each metabolite. Average SCCs across all test folds and iterations to obtain mean SCC per metabolite. This produces a distribution of performance scores that captures metabolite-level variability in predictability.

## Related tools

- **MiMeNet** (Neural network architecture (multi-layer perceptron) that maps microbiome features to metabolome features during cross-validated training and evaluation) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn MLPRegressor** (Trains multi-layer perceptron neural network with specified hyperparameters (layer size, activation, regularization, dropout) on training folds)
- **SciPy Spearman correlation** (Computes rank correlation coefficient between predicted and observed metabolite abundances on held-out test folds)
- **ADAM optimizer** (Gradient descent optimization algorithm used to train neural network weights during each cross-validation fold)
- **MelonnPan** (Baseline linear regression (Elastic Net) model used for comparative benchmarking of cross-validation performance against MiMeNet) — https://github.com/biobakery/melonnpan

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -output IBD_results
```

## Evaluation signals

- Mean SCC per metabolite falls within the reported range for the dataset (e.g., 0.108–0.309 for IBD PRISM across all 8,848 metabolites before well-predicted filtering). Ranges that deviate substantially indicate preprocessing or hyperparameter errors.
- SCC distribution is continuous and approximately bell-shaped around dataset-specific mean. Extreme outliers (e.g., all metabolites at SCC = 1.0 or SCC < −0.5 for soil) suggest data leakage, incorrect normalization, or overfitting.
- Number of well-predicted metabolites (SCC > 95th percentile of background shuffled distribution) matches reported counts: IBD PRISM 198–366, cystic fibrosis 104–143, soil 4–29. Counts far below or above indicate incorrect background generation or threshold setting.
- External validation cohort (if provided) shows consistent SCC range and well-predicted metabolite count as internal folds, confirming model generalization. Substantial decline in external performance suggests overfitting.
- Verification that cross-validation fold assignments, training/validation/test splits, and early stopping callback are applied consistently across all 10 iterations without data leakage (e.g., metabolite normalization computed per-fold, not globally).

## Limitations

- Lower SCC threshold for soil dataset (0.410 vs. 0.129–0.136 for others) may reflect longitudinal sampling structure (repeated measurements per location), which violates CV fold independence assumptions. When data has temporal or spatial structure, stratified CV is recommended.
- Not all metabolites are microbiome-associated; metabolites with no causal relationship to microbiome composition will have low predicted SCC regardless of model quality, reducing overall mean correlation across all metabolites.
- Mean SCC is averaged across all metabolites including both well-predicted and poorly predicted, which can mask strong signal in a subset. Report both mean SCC and count/proportion of well-predicted metabolites.
- Cross-validation performance on a single cohort may not reflect out-of-distribution generalization. External validation on independent cohorts (e.g., LifeLines-DEEP for IBD) is critical for reproducibility claims.
- Early stopping threshold (e.g., 40 iterations without validation loss improvement) is dataset- and hyperparameter-dependent; inappropriate thresholds can lead to underfitting or overfitting. Validate early stopping against a held-out validation fold.

## Evidence

- [methods] Execute 10 iterations of 10-fold cross-validation using MiMeNet MLPNN with optimal hyperparameters, training on 80% of each fold, validating on 20%, and testing on held-out 10%: "Execute 10 iterations of 10-fold cross-validation using MiMeNet MLPNN with optimal hyperparameters (IBD PRISM: layer size 512, 1 layer, λ=0.001, dropout=0.5; CF: layer size 128, 1 layer, λ=0.0001,"
- [methods] Calculate Spearman correlation coefficient between predicted and observed metabolite abundances for each metabolite across all test folds and iterations, averaging to obtain mean SCC per metabolite: "Calculate Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances for each metabolite across all test folds and iterations, averaging to obtain mean SCC per"
- [methods] Generate background distribution by shuffling microbiome and metabolome samples independently, performing 100 models of 10-fold cross-validation on shuffled data, collecting SCC values for all metabolites: "Generate background distribution by shuffling microbiome and metabolome samples independently, performing 100 models of 10-fold cross-validation on shuffled data, collecting SCC values for all"
- [methods] Define well-predicted metabolites as those with SCC above 95th percentile of background correlations, identifying cutoffs of 0.136 (IBD PRISM), 0.129 (cystic fibrosis), and 0.410 (soil): "Define well-predicted metabolites as those with SCC above 95th percentile of background correlations, identifying cutoffs of 0.136 (IBD PRISM), 0.129 (cystic fibrosis), and 0.410 (soil)"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [abstract] Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets: "Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets"
- [readme] MiMeNet uses microbial features to predict metabolite output features. To do so, neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in Spearman correlation coefficients (SCC) for each metabolite representing how well they could be predicted.: "MiMeNet uses microbial features to predict metabolite output features. To do so, neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in"
- [methods] mean squared error loss with L2 regularization, ReLU activation, ADAM optimizer, and early stopping at 40 iterations without validation loss improvement: "mean squared error loss with L2 regularization, ReLU activation, ADAM optimizer, and early stopping at 40 iterations without validation loss improvement"
