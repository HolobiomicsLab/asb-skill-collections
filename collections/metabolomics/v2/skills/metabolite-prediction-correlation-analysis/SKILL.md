---
name: metabolite-prediction-correlation-analysis
description: Use when after training a neural network or regression model to predict
  metabolomic profiles from microbiome data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0602
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
  - CCA (Canonical Correlation Analysis)
  - Scikit-learn
  - TensorFlow
  - SciPy
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
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed
  using the given instructions
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV
  using 5-fold internal cross-validation
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

# metabolite-prediction-correlation-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantifies prediction accuracy of machine learning models for metabolite abundance by computing Spearman correlation coefficients (SCC) between predicted and observed metabolite abundances, then stratifies results against an empirical background distribution generated from shuffled data to identify well-predicted metabolites.

## When to use

Apply this skill after training a neural network or regression model to predict metabolomic profiles from microbiome data. Use it to: (1) measure per-metabolite prediction quality across cross-validation folds, (2) distinguish signal from noise by comparing observed correlations to a permutation baseline, and (3) count metabolites above a statistical threshold to enable downstream functional module discovery or biomarker validation.

## When NOT to use

- Input metabolomic or microbiome data is not pre-filtered to ≥10% sample presence; apply feature filtering before correlation analysis.
- Model predictions have not been generated on held-out test data; use cross-validation or external validation sets, not training set predictions.
- Background distribution has not been generated; correlation thresholds cannot be interpreted without the empirical null from shuffled data.

## Inputs

- Microbiome abundance matrix (samples × microbial features, CLR- or relative abundance–normalized, pre-filtered to ≥10% sample presence)
- Metabolomic abundance matrix (samples × metabolite features, CLR- or relative abundance–normalized, pre-filtered to ≥10% sample presence)
- Trained neural network or regression model with learned weights
- Predicted metabolite abundance matrix (samples × metabolites) from model inference on test set
- Observed metabolite abundance matrix (samples × metabolites) for test set

## Outputs

- Per-metabolite Spearman correlation coefficient (SCC) array
- Mean SCC across all metabolites
- Count of well-predicted metabolites (SCC > 95th percentile of background)
- Empirical background SCC distribution (from 10–100 shuffled cross-validation iterations)
- Well-predicted metabolite list with SCC values
- Microbe-metabolite feature attribution score matrix (optional, for module discovery)

## How to apply

First, train your predictive model (e.g., MLPNN, Elastic Net, Random Forest) on microbiome features and compute predictions on held-out test folds. For each metabolite, calculate the Spearman correlation coefficient (SCC) between its predicted and observed abundances across all samples or folds. In parallel, generate an empirical background distribution by shuffling the microbiome and metabolomic data independently, then re-running the full cross-validation pipeline 10–100 times on shuffled pairs and computing SCCs. Define the significance threshold as the 95th percentile of the background SCC distribution. Classify metabolites with observed SCC > 95th percentile threshold as well-predicted. Report: mean SCC across all metabolites, count of well-predicted metabolites, and optionally construct feature attribution matrices from model weights to enable biclustering into functional modules.

## Related tools

- **MiMeNet** (Integrative multilayer perceptron neural network that predicts metabolomic profiles from microbiome data and computes correlation-based evaluation metrics) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Baseline linear regression model using Elastic Net that predicts metabolite abundances for benchmarking against neural network approaches) — https://github.com/biobakery/melonnpan
- **Scikit-learn** (Provides cross-validation utilities, neural network implementations, and general regression models (Random Forest, Elastic Net) used for prediction)
- **TensorFlow** (Deep learning framework used to train multilayer perceptron neural networks with dropout and L2 regularization)
- **SciPy** (Computes Spearman correlation coefficients between predicted and observed metabolite abundances)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -output IBD
```

## Evaluation signals

- Mean SCC increases relative to baseline shuffled correlations (e.g., from 0.108 to 0.309 for well-performing models on IBD data)
- Count of well-predicted metabolites (SCC > 95th percentile) is substantially higher than expected by chance; compare to number detected in shuffled background
- Background SCC distribution is centered near zero and shows expected tail behavior; 95th percentile threshold should be noticeably above mean background
- External validation: when trained model is evaluated on held-out external cohort, mean SCC and well-predicted metabolite count remain consistent with internal cross-validation
- Feature attribution scores derived from model weights exhibit interpretable clustering (via biclustering) into functional modules consistent with prior biological knowledge

## Limitations

- Not all metabolites may be associated with microbes; some metabolites will have low prediction correlations regardless of model quality, reducing overall mean SCC.
- Analysis is data-driven without incorporating mechanistic knowledge; correlations alone do not prove causal microbe-metabolite interactions.
- Hyperparameter tuning strategy (single vs. per-partition) can affect metabolite counts; shared hyperparameters may miss dataset-specific optimization but improve generalization.
- Background distribution threshold (95th percentile) is empirical; choice may vary across datasets with different noise structures or biological associations.
- Longitudinal or hierarchical study designs (e.g., time-series soil data) may exhibit higher correlation thresholds due to repeated measurements within samples, complicating cross-study comparisons.

## Evidence

- [methods] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances"
- [methods] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [abstract] MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264): "MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)"
- [abstract] identifies more well-predicted metabolites (increase in the number of well-predicted metabolites from 198 to 366, 104 to 143, and 4 to 29) compared to state-of-art linear models: "identifies more well-predicted metabolites (increase in the number of well-predicted metabolites from 198 to 366, 104 to 143, and 4 to 29) compared to state-of-art linear models"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [methods] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [results] MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites: "MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites"
