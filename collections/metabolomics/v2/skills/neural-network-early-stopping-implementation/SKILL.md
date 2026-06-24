---
name: neural-network-early-stopping-implementation
description: Use when when training a multilayer perceptron neural network on paired
  microbiome-metabolome datasets where you have a held-out validation fold (20% of
  each cross-validation fold) and wish to prevent overfitting without manual epoch
  selection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0084
  - http://edamontology.org/topic_3407
  tools:
  - MiMeNet
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - TensorFlow
  - scikit-learn MLPRegressor
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome
  abundance features (green) are used to train a neural network to predict metabolite
  abundance features (blue).
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- Canonical correlation analysis models were implemented using Python's scikit-learn
  package.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- In MiMeNet, φ is set as the rectified linear unit (ReLU). We selected this activation
  function since previous studies have shown that it is resilient to the problems
  of exploding and vanishing
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

# neural-network-early-stopping-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Early stopping terminates neural network training when validation loss stops improving over a fixed number of iterations, preventing overfitting while preserving generalization performance. This is essential for multivariate metabolite prediction from microbiome data, where the optimization landscape is high-dimensional and validation performance diverges from training performance.

## When to use

When training a multilayer perceptron neural network on paired microbiome-metabolome datasets where you have a held-out validation fold (20% of each cross-validation fold) and wish to prevent overfitting without manual epoch selection. Apply this when training multiple cross-validated models in succession and you need a consistent, data-driven stopping criterion across all folds and iterations.

## When NOT to use

- When validation data is not available or validation fold is <10% of training data; early stopping requires a statistically powered validation signal.
- When training only a single model without cross-validation; early stopping is most effective in cross-validated pipelines where multiple folds provide stable estimates of the best stopping point.
- When the validation loss is extremely noisy (high variance per iteration) due to small batch sizes or low-signal validation sets; the patience threshold may trigger prematurely on random fluctuations rather than genuine overfitting.

## Inputs

- Paired microbiome feature matrix (samples × microbes, CLR-transformed or relative abundance)
- Paired metabolome feature matrix (samples × metabolites, CLR-transformed)
- Cross-validation fold split (80% training, 20% validation per fold)
- Initialized multilayer perceptron with specified hyperparameters (layer size, dropout, L2 penalty)
- Training data batch and validation data batch

## Outputs

- Trained neural network model checkpoint (weights at best validation loss iteration)
- Validation loss trajectory across iterations
- Iteration at which early stopping occurred (stopping iteration)
- Best validation loss value achieved
- Predicted metabolite abundances on held-out test set from the stopped model

## How to apply

Monitor the validation loss (mean squared error computed on the held-out 20% validation subset of each cross-validation fold) at each training iteration. Define a patience threshold — the maximum number of iterations without improvement in validation loss before halting. In the MiMeNet workflow, a patience of 40 iterations was used: if validation loss does not decrease for 40 consecutive iterations, training stops immediately, and the model at the best validation loss checkpoint is retained. This prevents training on noisy validation curves while maintaining the model state that best generalized to unseen data. Apply this uniformly across all hyperparameter configurations (layer sizes, L2 regularization, dropout rates) to ensure reproducible, automated termination across the entire 10×10-fold cross-validation regime.

## Related tools

- **TensorFlow** (Deep learning framework used to implement multilayer perceptron and manage gradient descent training with early stopping callbacks)
- **scikit-learn MLPRegressor** (Alternative implementation of multilayer perceptron regression; supports early stopping via warm_start and validation_fraction parameters)
- **ADAM optimizer** (Adaptive learning rate optimizer used during training iterations to minimize mean squared error loss before early stopping criterion is evaluated)
- **ReLU activation** (Non-linear activation function applied in hidden layers; early stopping monitors validation loss of the complete activated network)
- **MiMeNet** (End-to-end pipeline that applies early stopping during cross-validated neural network training on microbiome-metabolome data) — https://github.com/YDaiLab/MiMeNet

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -output IBD
```

## Evaluation signals

- Validation loss decreased monotonically or with manageable noise up to the stopping iteration, then would have continued to oscillate without improvement thereafter (inspect loss trajectory plot).
- Stopping iteration is consistent across multiple cross-validation folds (e.g., all 10 folds stop between iterations 35–45 when patience=40), indicating stable convergence behavior.
- Test set Spearman correlation coefficient (SCC) on the held-out 10% test fold is stable and does not degrade compared to models stopped at earlier iterations; confirms that early stopping checkpoint generalizes well.
- Reported mean SCC and well-predicted metabolite counts match published validation ranges (e.g., IBD PRISM: SCC range 0.108→0.309, well-predicted metabolites 198→366) when early stopping is applied uniformly across all 10 iterations of 10-fold cross-validation.
- Early stopping iteration is less than the total training budget (e.g., <1000 iterations if max_iter=10000); confirms training terminated before reaching iteration limit, indicating effective regularization.

## Limitations

- Early stopping requires a held-out validation set; reducing the training set size from 90% to 80% per fold may slow convergence or increase variance in final model performance, especially on smaller datasets (e.g., soil dataset with 85 metabolites).
- The patience threshold (40 iterations in MiMeNet) is a hyperparameter that must be tuned per dataset; a fixed value may be suboptimal for datasets with different noise characteristics or optimization landscapes.
- Noisy or small validation sets can cause spurious early stops; validation loss must be smoothed or evaluated over multiple iterations to distinguish signal from noise.
- Early stopping only detects overfitting with respect to mean squared error on the validation fold; it does not guarantee that the selected model will perform well on downstream tasks (e.g., module enrichment, biomarker discovery) that depend on biological relevance rather than prediction accuracy alone.

## Evidence

- [other] training on 80% of each fold, validating on 20%, and testing on held-out 10% using mean squared error loss with L2 regularization, ReLU activation, ADAM optimizer, and early stopping at 40 iterations without validation loss improvement: "early stopping at 40 iterations without validation loss improvement"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [other] Execute 10 iterations of 10-fold cross-validation using MiMeNet MLPNN with optimal hyperparameters (IBD PRISM: layer size 512, 1 layer, λ=0.001, dropout=0.5; CF: layer size 128, 1 layer, λ=0.0001, dropout=0.5; soil: layer size 128, 2 layers, λ=0.005, dropout=0.3): "Execute 10 iterations of 10-fold cross-validation using MiMeNet MLPNN with optimal hyperparameters"
- [intro] MiMeNet uses multilayer perceptron neural networks to model metagenomic taxonomic or functional features to predict metabolomic features while learning underlying metabolite relationships: "MiMeNet uses multilayer perceptron neural networks to model metagenomic taxonomic or functional features to predict metabolomic features"
- [readme] MiMeNet will then take any metabolite with a SCC evaluation value above the 95th percentile to be well-predicted.: "MiMeNet will then take any metabolite with a SCC evaluation value above the 95th percentile to be well-predicted."
