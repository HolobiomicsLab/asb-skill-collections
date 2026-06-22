---
name: background-distribution-threshold-calibration
description: Use when when you have trained a predictive model (e.g., neural network or regression model) that outputs continuous scores (such as Spearman correlation coefficients) for individual features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3673
  tools:
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - TensorFlow
  - scikit-learn
  - SciPy
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- these models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate Elastic Net, and Canonical
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
---

# background-distribution-threshold-calibration

## Summary

A method to establish empirically-grounded significance thresholds for predictive model outputs by generating a null distribution from shuffled data, then using percentile cutoffs to classify well-predicted features. This skill ensures that feature predictions are statistically validated against random baseline correlations rather than relying on arbitrary fixed cutoffs.

## When to use

When you have trained a predictive model (e.g., neural network or regression model) that outputs continuous scores (such as Spearman correlation coefficients) for individual features (e.g., metabolites), and you need to distinguish which features are genuinely well-predicted versus indistinguishable from chance. This is especially critical when prediction correlations are low or variable across features, and when you plan to perform downstream module discovery or biological interpretation on the predicted features.

## When NOT to use

- When prediction scores are known to follow a standard statistical distribution (normal, log-normal) for which parametric thresholds (e.g., z-score cutoffs) are more efficient and well-calibrated.
- When features are independent and identically distributed and your analysis goal is only to rank features by prediction quality, not to claim statistical significance.
- When the computational cost of running 10+ complete cross-validation iterations on shuffled data is prohibitive (e.g., very large feature sets or slow models).

## Inputs

- Paired microbiome and metabolomic abundance tables (samples × features, non-negative counts or relative abundances)
- Trained neural network or regression model (weights and architecture)
- Cross-validation fold assignments (train/validation/test splits)

## Outputs

- Background distribution of prediction scores (vector of Spearman correlations from shuffled runs)
- Empirically-derived percentile threshold (e.g., 95th percentile value)
- Well-predicted feature binary classification (boolean per feature: above or below threshold)
- Feature prediction scores with significance status

## How to apply

First, train your primary model using cross-validation on the original data and record the prediction score (e.g., mean Spearman correlation coefficient) for each output feature. Second, generate a background distribution by performing the same cross-validation protocol multiple times (at least 10 iterations recommended) on shuffled versions of the data—specifically, randomly reorder sample labels while keeping feature values intact—and collect the prediction scores from each shuffled run. Third, compute a percentile threshold from the background distribution (e.g., the 95th percentile) that represents the score at which observed predictions exceed 95% of random predictions. Fourth, classify each feature as 'well-predicted' if its observed score exceeds this empirically-derived threshold. This approach accounts for dataset-specific noise, feature correlation structure, and sample size, making the threshold adaptive rather than fixed across studies.

## Related tools

- **MiMeNet** (Primary neural network framework for microbe-metabolite prediction; generates correlation scores that are validated against background distribution) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow** (Deep learning backend for training the MLPNN models whose outputs are calibrated by background shuffling)
- **scikit-learn** (Provides cross-validation utilities (KFold), correlation metrics (Spearman), and baseline models (Random Forest, Elastic Net) for comparison)
- **SciPy** (Computes Spearman correlation coefficients and percentile functions for threshold derivation)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -num_run_cv 10 -num_cv 10 -num_background 10 -threshold 0.95 -output IBD_results
```

## Evaluation signals

- Background distribution has >100 data points (from 10+ iterations of 10-fold CV) and shows a roughly smooth distribution centered near zero or the null expectation, not bimodal or heavily skewed.
- Observed feature prediction scores are visibly separated from the background distribution (e.g., well-predicted metabolites > 95th percentile) with no leakage of 'well-predicted' features below the threshold.
- The well-predicted feature count differs substantially between observed and shuffled runs (e.g., 366 observed vs. implied ~5–10% of total in background for the IBD dataset), confirming the threshold is non-trivial.
- Threshold value is adaptive across datasets (e.g., different for IBD, Cystic Fibrosis, and Soil data) reflecting dataset-specific noise and feature correlations, rather than fixed to a single hardcoded value.
- Downstream modules inferred from well-predicted features contain coherent biological annotations or known metabolite–microbe functional relationships, validating that the threshold is biologically meaningful.

## Limitations

- The threshold is sensitive to the number of background iterations; fewer iterations (< 5) may lead to unstable or overly permissive cutoffs, while more iterations (> 100) incur substantial computational cost with diminishing improvement.
- The method assumes that random sample shuffling produces a valid null distribution; if sample-level confounders (e.g., batch, time point, disease state) are strong, shuffling may not truly represent chanceable predictions and can inflate or deflate the threshold.
- Performance depends on adequate sample size and feature diversity; datasets with very few samples (< 50) or highly sparse metabolomic profiles may have unreliable background distributions and unstable percentile estimates.
- The choice of percentile (e.g., 95th vs. 90th) is somewhat arbitrary; the article does not provide a principled way to select it beyond convention, and different choices can substantially alter the number of well-predicted features and downstream interpretations.
- In some datasets (e.g., Soil with longitudinal structure), the background threshold may be higher than expected due to implicit temporal or spatial structure in the samples, but the article does not provide guidance for detecting or correcting such biases.

## Evidence

- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [other] Train MiMeNet using ADAM optimizer with mean squared error loss function and L2 regularization, applying ReLU activation and dropout at each hidden layer, with early stopping when validation loss does not improve within 40 iterations.: "Train MiMeNet using ADAM optimizer with mean squared error loss function and L2 regularization, applying ReLU activation and dropout at each hidden layer, with early stopping when validation loss"
- [results] Generate background distribution by shuffling dataset and cross-validation: "Generate background distribution by shuffling dataset and cross-validation"
- [readme] Identifying Well-Predicted Metabolties: MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration"
- [readme] Number of iterations for cross-validation to perform. num_cv: Number of partitions to divide the data into during cross-validation (Recommend at least 5).: "Number of iterations for cross-validation to perform. num_cv: Number of partitions to divide the data into during cross-validation (Recommend at least 5)."
