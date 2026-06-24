---
name: multivariate-regression-comparison
description: Use when you have paired microbiome and metabolomic (or similar compositional)
  data with a new regression model and want to rigorously demonstrate its predictive
  advantage over alternatives (Elastic Net, Random Forest, CCA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_2885
  - http://edamontology.org/topic_0091
  tools:
  - MelonnPan (Elastic Net linear regression)
  - Elastic Net regression
  - Random Forest regression
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - MelonnPan (Elastic Net)
  - Random Forest
  - Canonical Correlation Analysis (CCA)
  - scikit-learn
  - TensorFlow
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed
  using the given instructions.
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV
  using 5-fold internal cross-validation for hyper-parameter tuning where the hyper-parameter
  grid contained
- Random Forest models were implemented using RandomForestRegressor with the default
  parameter set-tings of 100 tree estimators.
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

# Multivariate Regression Comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically benchmark a novel multivariate regression model (e.g., neural network) against established linear and ensemble baselines using identical cross-validation protocols, computing effect sizes (Spearman correlation coefficients) and counts of well-predicted features to quantify improvement. This skill is essential when claiming superiority of a new predictive method over prior work.

## When to use

You have paired microbiome and metabolomic (or similar compositional) data with a new regression model and want to rigorously demonstrate its predictive advantage over state-of-the-art alternatives (Elastic Net, Random Forest, CCA). The comparison must be fair: same preprocessing, same cross-validation scheme, same evaluation metric, same feature filtering thresholds, and ideally multiple datasets to establish generalizability.

## When NOT to use

- Input is already a pre-computed feature importance or prediction score matrix; use direct ranking instead.
- Datasets are too small (n < 50) to support reliable 10-fold cross-validation; consider leave-one-out or smaller fold counts.
- Baseline methods (e.g., Elastic Net, Random Forest) are not installed or not available in the same computational environment; ensure all tools are installed and validated.
- Evaluation metric (Spearman correlation) is inappropriate for your outcome type (e.g., binary classification, survival times); select a metric aligned with your prediction task.

## Inputs

- Paired microbiome abundance table (samples × microbial features, CSV or count matrix)
- Paired metabolome abundance table (samples × metabolite features, CSV or count matrix)
- Optional: external validation microbiome and metabolome tables
- Optional: sample labels or annotations for stratified analysis

## Outputs

- Comparison table: mean SCC ± SD per model per dataset
- Well-predicted feature counts per model per dataset
- Background SCC distributions (shuffled model results)
- Visualization: box plots or violin plots of SCC distributions across CV folds
- Summary statistics: p-values or confidence intervals for pairwise model differences

## How to apply

First, apply identical data preprocessing to all models: remove features present in <10% of samples and apply centered log-ratio (CLR) transformation with pseudocount of 1 (or specify alternative normalization clearly). Second, perform hyperparameter tuning for each model using nested 5-fold cross-validation on training data only—for MiMeNet, tune layer size, number of layers, L2 regularization (λ), and dropout rates; for Elastic Net (MelonnPan), grid-search α and l1_ratio; for Random Forest, fix estimators at 100; for CCA, test 10, 20, 40 components. Third, evaluate all models using identical outer cross-validation (10 iterations of 10-fold with 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC) between predicted and observed feature abundances. Fourth, define well-predicted features as those with SCC above the 95th percentile of a background distribution generated by training 100 shuffled models (random sample reordering). Report mean ± standard deviation of SCC and total well-predicted feature counts for each model, aggregated across all datasets and iterations. Fifth, assess statistical significance and effect size, reporting absolute improvements (e.g., SCC delta from 0.108 to 0.309) alongside confidence intervals when possible.

## Related tools

- **MiMeNet** (Novel multivariate neural network baseline being evaluated for superiority in metabolite prediction) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan (Elastic Net)** (Established linear regression baseline trained independently on each metabolite) — https://github.com/biobakery/melonnpan
- **Random Forest** (Ensemble regression baseline (100 trees) for benchmarking against non-linear methods)
- **Canonical Correlation Analysis (CCA)** (Multivariate linear baseline capturing shared structure across metabolites and microbes)
- **scikit-learn** (Python library providing Elastic Net, Random Forest, and cross-validation utilities) — https://scikit-learn.org
- **ADAM optimizer** (Gradient descent optimizer for training neural network models)
- **TensorFlow** (Deep learning framework for implementing and training MiMeNet MLPNN)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -output IBD_comparison
```

## Evaluation signals

- All models use the same preprocessed input (features filtered at 10% presence; CLR transformation applied to microbiome and metabolomic tables).
- Cross-validation scheme is identical across models: 10 iterations of 10-fold with 80/20 train-validation split; nested hyperparameter tuning does not contaminate outer folds.
- Mean Spearman correlation coefficients are reported with standard deviation; effect sizes show consistent improvement of novel method across all three independent datasets (IBD PRISM, Cystic Fibrosis, Soil).
- Well-predicted metabolite counts (SCC > 95th percentile of background) are higher for the novel method; background distribution is empirically derived from ≥100 shuffled model iterations.
- Statistical tests or confidence intervals are provided for pairwise model differences (or effect size is sufficiently large that practical significance is clear: e.g., SCC improvement from 0.108 to 0.309 or well-predicted metabolite increase from 198 to 366).

## Limitations

- Not all metabolites are associated with microbes, resulting in lower prediction correlations for some features and lower overall mean SCC; this biases the comparison toward models that can exploit weak signals.
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge of metabolic pathways, limiting biological interpretability of the comparison.
- External validation datasets used for MiMeNet may not be independent if they originate from the same cohort or study design; true external validation requires data from different institutions or disease contexts.
- The 95th percentile threshold for well-predicted features is empirical and dataset-dependent; higher threshold values observed for soil data may reflect longitudinal observations rather than true method performance.
- Comparison does not include all state-of-the-art methods (e.g., mmvec is mentioned but not directly benchmarked); this may understate performance of alternative neural network approaches.

## Evidence

- [abstract] MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan, and identifies more well-predicted metabolites: 366 vs 198 (IBD), 143 vs 104 (CF), and 29 vs 4 (Soil).: "MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan, and"
- [methods] Any input or output feature that is present in less than 10% of samples was removed. MiMeNet then trains multiple network models using 10-fold cross-validation.: "Any input or output feature that is present in less than 10% of samples was removed"
- [results] Hyperparameter tuning for network architecture using nested 5-fold cross-validation, followed by evaluation over 10 iterations of 10-fold cross-validation.: "Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each"
- [methods] Train Elastic Net (via MelonnPan with α and l1_ratio grid search), Canonical Correlation Analysis (with 10, 20, 40 components), and Random Forest (100 tree estimators) baseline models using identical cross-validation protocol.: "Train Elastic Net (via MelonnPan with α and l1_ratio grid search), Canonical Correlation Analysis (with 10, 20, 40 components), and Random Forest (100 tree estimators) baseline models using identical"
- [methods] Well-predicted metabolites were defined as those with SCC above the 95th percentile of background correlations generated by 100 shuffled models.: "define well-predicted metabolites as those with SCC above the 95th percentile of the background correlations"
- [readme] MiMeNet uses microbial features to predict metabolite output features. Neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in Spearman correlation coefficients (SCC) for each metabolite.: "MiMeNet uses microbial features to predict metabolite output features. To do so, neural network hyper-parameters are first tuned. Then models are evaluated in a cross-validated fashion resulting in"
- [discussion] Not all metabolites may be associated with microbes, resulting in lower prediction correlations and lower overall mean correlation.: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
