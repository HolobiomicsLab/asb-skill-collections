---
name: cross-validation-benchmark-evaluation
description: Use when you have developed a predictive model and need to compare its
  performance against established baselines (e.g., linear regression, Random Forest,
  Canonical Correlation Analysis) across multiple datasets with paired input-output
  features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3697
  tools:
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - MelonnPan
  - Elastic Net regression
  - Random Forest regression
  - Canonical Correlation Analysis (CCA)
  - scikit-learn
  - TensorFlow / Keras
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
- these models can predict the entire set of metabolites at once, and all models were
  evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate
  Elastic Net, and Canonical
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

# cross-validation-benchmark-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A systematic evaluation protocol that uses nested and repeated cross-validation to rigorously benchmark a novel predictive model (MiMeNet) against multiple baseline methods across diverse datasets, ensuring fair comparison and robust performance estimation. This skill is essential when claiming methodological improvements over existing approaches and when generalization performance must be validated across multiple biological contexts.

## When to use

Apply this skill when you have developed a predictive model and need to compare its performance against established baselines (e.g., linear regression, Random Forest, Canonical Correlation Analysis) across multiple datasets with paired input-output features. Use it specifically when you must account for both model selection bias (via nested cross-validation) and sampling variability (via multiple iterations), and when you want to identify not just mean performance but also which individual features are well-predicted above noise.

## When NOT to use

- You have only a single dataset or fewer than ~50 samples per dataset—nested cross-validation and multiple iterations require sufficient data to partition meaningfully without overfitting to fold structure.
- You are comparing models on entirely different train-test splits or cross-validation schemes—all models must use identical folds to ensure fair comparison and avoid confounding results with validation protocol differences.
- Your baseline methods cannot be retrained on the same folds (e.g., using only pre-trained external models)—the protocol requires all models to undergo identical cross-validation to isolate algorithmic differences from data sampling effects.

## Inputs

- Paired feature tables: microbiome abundance matrix (samples × microbial features) and metabolome abundance matrix (samples × metabolite features)
- Preprocessed and normalized input matrices (CLR-transformed with pseudocount, features filtered to ≥10% sample presence)
- Hyperparameter search space definition (layer sizes, regularization penalties, dropout rates)
- Multiple independent datasets (≥2) to establish generalization across biological contexts

## Outputs

- Mean and standard deviation of Spearman correlation coefficients for each model across all cross-validation iterations and datasets
- Count of well-predicted metabolites per model (features with SCC > 95th percentile of background)
- Comparison table ranking models by prediction performance metric
- Background SCC distribution (from shuffled models) used to define significance threshold
- Per-metabolite prediction scores enabling downstream feature importance analysis

## How to apply

Implement a three-phase evaluation: (1) **Hyperparameter tuning**: Use nested 5-fold cross-validation on your novel model to select optimal architecture parameters (layer count, layer size, L2 regularization λ, dropout rates) independently for each dataset. (2) **Main cross-validation benchmark**: Train your model and all baseline models (Elastic Net, Random Forest, CCA, etc.) using identical 10 iterations of 10-fold cross-validation splits (90% train, 10% test; 80/20 train-validation split within training folds), computing Spearman correlation coefficients (SCC) between predicted and observed outputs for each metabolite in each fold. (3) **Statistical significance thresholding**: Generate a background SCC distribution by training 100 shuffled versions of each model with random sample reordering across the same cross-validation splits, then define well-predicted features as those with SCC above the 95th percentile of their background distribution. Aggregate results across all iterations and datasets, reporting mean ± standard deviation of SCC and absolute counts of well-predicted features for each method. This protocol isolates true model performance gains from optimistic bias.

## Related tools

- **MiMeNet** (Novel neural network model (MLPNN with ReLU activation, ADAM optimizer, L2 regularization, dropout) being benchmarked; trains during each cross-validation fold) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Baseline method using Elastic Net linear regression; retrained during cross-validation with identical folds for fair comparison) — https://github.com/biobakery/melonnpan
- **Elastic Net regression** (Baseline regression method; tuned via grid search over α and l1_ratio parameters within cross-validation)
- **Random Forest regression** (Baseline ensemble method with 100 tree estimators; retrained on same cross-validation splits)
- **Canonical Correlation Analysis (CCA)** (Baseline dimensionality reduction + correlation method; tuned with 10, 20, 40 component variants)
- **scikit-learn** (Python library providing Elastic Net, Random Forest, and cross-validation utilities)
- **TensorFlow / Keras** (Deep learning framework for MiMeNet MLPNN implementation with ADAM optimizer and early stopping)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_cv 10 -num_background 100 -output results/IBD
```

## Evaluation signals

- All models trained on identical cross-validation fold splits: verify train/test indices are shared across MiMeNet, MelonnPan, Random Forest, and CCA to confirm fair comparison.
- Nested cross-validation structure respected: hyperparameter tuning uses only the training fold (no test leakage), and final metrics computed on held-out test folds.
- Background SCC distribution generated from shuffled data: confirm that 100 shuffled models show substantially lower and broader SCC range than observed models, validating that observed well-predicted metabolites are genuine signal rather than noise.
- Well-predicted metabolite threshold (95th percentile) applied consistently: verify that the SCC cutoff is computed per model per dataset from its background distribution, and that metabolites designated 'well-predicted' for each method have SCC values above this quantile.
- Performance aggregation across iterations: check that reported mean ± SD metrics combine results from all 10 iterations × 10 folds = 100 test evaluations per model per dataset, and that counts of well-predicted metabolites are summed across all these evaluations.

## Limitations

- Not all metabolites may be associated with microbes, resulting in lower prediction correlations and lower overall mean correlation across all metabolites—some metabolites will have inherently unpredictable abundances, biasing mean performance downward.
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge—the neural network learns statistical associations without biological constraints, which may find spurious correlations or miss biologically meaningful but weak associations.
- Generalizability may vary by data type: higher threshold values were observed for soil data, which may be due to longitudinal observations, suggesting the protocol's significance thresholds are context-dependent and may not transfer uniformly across environments.
- External validation datasets using different cohorts were not included in the main nested cross-validation protocol—external validation (e.g., IBD External dataset) should be treated as held-out test data rather than folded into the benchmark, or separate evaluation protocols should be applied.

## Evidence

- [methods] Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each dataset.: "Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each"
- [methods] Evaluate MiMeNet over 10 iterations of 10-fold cross-validation (90% training, 10% test; 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances.: "Evaluate MiMeNet over 10 iterations of 10-fold cross-validation (90% training, 10% test; 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC)"
- [methods] Generate background SCC distribution by training 100 shuffled models with random sample reordering and define well-predicted metabolites as those with SCC above the 95th percentile of background correlations.: "Generate background SCC distribution by training 100 shuffled models with random sample reordering and define well-predicted metabolites as those with SCC above the 95th percentile of background"
- [methods] Train Elastic Net (via MelonnPan with α and l1_ratio grid search), Canonical Correlation Analysis (with 10, 20, 40 components), and Random Forest (100 tree estimators) baseline models using identical cross-validation protocol and calculate mean SCC and well-predicted metabolite counts.: "Train Elastic Net (via MelonnPan with α and l1_ratio grid search), Canonical Correlation Analysis (with 10, 20, 40 components), and Random Forest (100 tree estimators) baseline models using identical"
- [methods] Aggregate results across all three datasets and ten iterations, reporting mean ± standard deviation of SCC and total well-predicted metabolite counts for each model.: "Aggregate results across all three datasets and ten iterations, reporting mean ± standard deviation of SCC and total well-predicted metabolite counts for each model."
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
- [readme] Number of iterations of 10-fold cross-validated evaluation to perform.: "Number of iterations of 10-fold cross-validated evaluation to perform."
- [readme] MiMeNet uses microbial features to predict metabolite output features. To do so, neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in Spearman correlation coefficients (SCC) for each metabolite: "MiMeNet uses microbial features to predict metabolite output features. To do so, neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in"
- [readme] MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for"
