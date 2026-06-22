---
name: neural-network-hyperparameter-tuning
description: Use when when training a multilayer perceptron to predict metabolomic features from microbiome abundances, you need dataset-specific hyperparameter configurations because prediction performance (Spearman correlation and well-predicted metabolite counts) varies substantially across microbiome.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3795
  edam_topics:
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_2815
  - http://edamontology.org/topic_0092
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - SciPy
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MelonnPan and NED models were obtained from their respective GitHub repositories and executed using default parameters as according to their tutorials. Random Forest, multivariate Elastic Net, and
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
---

# neural-network-hyperparameter-tuning

## Summary

Systematic selection of multilayer perceptron hyperparameters (layer size, number of layers, L2 regularization, dropout rate) optimized per dataset to maximize metabolite prediction accuracy. This skill involves empirical tuning via cross-validation to identify dataset-specific configurations that balance model complexity and generalization.

## When to use

When training a multilayer perceptron to predict metabolomic features from microbiome abundances, you need dataset-specific hyperparameter configurations because prediction performance (Spearman correlation and well-predicted metabolite counts) varies substantially across microbiome environments. Use this skill when you have paired microbiome-metabolome data and must select layer architecture, regularization strength, and dropout before initiating cross-validated model evaluation.

## When NOT to use

- Data has not yet been filtered to remove features present in <10% of samples; preprocessing must complete before tuning.
- You have only a single small dataset (n<50 samples) without external validation cohorts; overfitting risk is high and cross-validation estimates unreliable.
- Hyperparameters are already fixed by a prior study or pre-trained model transfer task; tuning is then redundant.

## Inputs

- Comma-delimited microbial abundance table (samples × features, CLR or RA normalized, features present in ≥10% of samples)
- Comma-delimited metabolite abundance table (samples × features, CLR or RA normalized, features present in ≥10% of samples)
- Candidate hyperparameter grid or JSON specification file (net_params)

## Outputs

- Optimal net_params JSON file encoding selected layer size, number of layers, L2 penalty (λ), and dropout rate
- Cross-validation performance metrics (mean Spearman correlation coefficients per metabolite, counts of well-predicted metabolites above 95th percentile threshold)

## How to apply

Conduct grid search or empirical exploration across candidate hyperparameter combinations (layer sizes: 128–512; number of layers: 1–2; L2 regularization λ: 0.00001–0.005; dropout rates: 0.3–0.5) using a representative subset or the full training data with internal cross-validation (e.g., 5-fold). For each configuration, train the MLPNN with ReLU activation, ADAM optimizer, and MSE loss with early stopping (40 epochs without validation loss improvement). Select the configuration that maximizes mean Spearman correlation coefficient across folds. Document the optimal configuration in a JSON file (net_params) for reproducibility. The rationale is that different microbiome environments (gut, lung, soil) exhibit different signal-to-noise ratios and feature dimensionality: the IBD (PRISM) dataset required layer_size=512 with 1 layer and λ=0.001, while cystic fibrosis and soil required layer_size=128 with 1–2 layers and λ=0.0001–0.005, reflecting reduced metabolite complexity in smaller cohorts.

## Related tools

- **TensorFlow or PyTorch** (Deep learning framework for implementing multilayer perceptron with ReLU activation, ADAM optimizer, MSE loss, and early stopping)
- **scikit-learn** (Cross-validation partitioning (KFold) and model evaluation utilities)
- **MiMeNet** (Reference implementation that encapsulates hyperparameter tuning via net_params JSON and -num_cv / -num_run_cv arguments) — https://github.com/YDaiLab/MiMeNet
- **SciPy** (Spearman correlation coefficient computation for cross-validation performance assessment)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -output IBD
```

## Evaluation signals

- Mean Spearman correlation coefficient on held-out test folds increases or plateaus (does not degrade) compared to default or naive hyperparameter choices
- Count of well-predicted metabolites (SCC > 95th percentile of background) is maximized; for IBD (PRISM) this should be ≥6857, for CF ≥143, for soil ≥29
- Early stopping triggers within ≤40 epochs on validation set, indicating learning curves have plateaued and overfitting is controlled
- Cross-validation performance is reproducible across multiple independent CV splits; low variance in SCC distributions across folds indicates stable hyperparameter choice
- Net_params JSON file is syntactically valid and contains all required keys (layer_size, num_layers, lambda, dropout) as JSON scalars or lists

## Limitations

- Hyperparameter tuning is dataset-specific; configurations optimal for IBD gut microbiota (layer_size=512, λ=0.001) are not optimal for cystic fibrosis lung (layer_size=128, λ=0.0001) or soil (layer_size=128, λ=0.005), requiring re-tuning for each new microbiome context.
- Small microbiome cohorts (n<50) may not reliably estimate performance via k-fold cross-validation; external validation on an independent cohort is necessary to confirm generalization.
- Tuning is computationally expensive; 10 iterations of 10-fold cross-validation with background shuffling (100 models per condition) can require hours to days depending on feature dimensionality and hardware.
- The skill does not incorporate mechanistic knowledge of microbe-metabolite biology; optimal hyperparameters are purely data-driven and may not reflect underlying biological structure.
- Early stopping threshold (40 epochs without validation improvement) is fixed in the reference implementation; sensitivity to this choice is not systematically explored.

## Evidence

- [other] MiMeNet (multi-layer perceptron (MLPNN) with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) using 10 iterations of 10-fold cross-validation: "MiMeNet (multi-layer perceptron with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer)"
- [other] IBD PRISM: layer size 512, 1 layer, λ=0.001, dropout=0.5; CF: layer size 128, 1 layer, λ=0.0001, dropout=0.5; soil: layer size 128, 2 layers, λ=0.005, dropout=0.3: "optimal hyperparameters (IBD PRISM: layer size 512, 1 layer, λ=0.001, dropout=0.5; CF: layer size 128, 1 layer, λ=0.0001, dropout=0.5; soil: layer size 128, 2 layers, λ=0.005, dropout=0.3)"
- [other] training on 80% of each fold, validating on 20%, and testing on held-out 10% using mean squared error loss with L2 regularization, ReLU activation, ADAM optimizer, and early stopping at 40 iterations without validation loss improvement: "training on 80% of each fold, validating on 20%, and testing on held-out 10% using mean squared error loss with L2 regularization, ReLU activation, ADAM optimizer, and early stopping at 40 iterations"
- [readme] net_params JSON file containing neural network number of layers, layer size, L2 penalty, and dropout rate: "JSON file containing neural network number of layers, layer size, L2 penalty, and dropout rate"
- [other] different dataset was taken from a study that collected 172 lung sputum samples from patients with cystic fibrosis exhibiting mean Spearman correlations of 0.457, and soil dataset exhibited 0.264, contrasting with IBD 0.309: "mean Spearman correlation coefficients of 0.309, 0.457, and 0.264 for IBD (PRISM), cystic fibrosis, and soil datasets respectively"
