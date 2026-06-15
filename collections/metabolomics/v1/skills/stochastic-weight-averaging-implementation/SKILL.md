---
name: stochastic-weight-averaging-implementation
description: Use when training a deeply regularized deep neural network on a large molecular feature dataset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - alvaDesc
  - PyTorch or TensorFlow
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# stochastic-weight-averaging-implementation

## Summary

Stochastic weight averaging (SWA) is a post-training technique that improves neural network generalization by averaging model weights collected at intervals during training, particularly effective when combined with cyclic learning rate schedules. In retention time prediction, SWA reduces test-set mean and median absolute errors by stabilizing learned representations across multiple training epochs.

## When to use

Apply this skill when training a deeply regularized deep neural network on a large molecular feature dataset (e.g., >80,000 molecules with >5,000 descriptors and fingerprints) where you have already adopted a cyclic learning rate schedule (cosine annealing with warm restarts) and aim to improve generalization performance on held-out regression targets such as retention time or other continuous molecular properties.

## When NOT to use

- Input data has fewer than ~1,000 training samples or very low-dimensional features; SWA benefits scale with dataset and model size and may add negligible improvement on small problems.
- The learning rate schedule is not cyclic (e.g., monotone decay or fixed learning rate); SWA is most effective when the optimizer visits diverse points in weight space, which cyclic schedules facilitate.
- The model is already converged to a sharp minimum; SWA works best when the training trajectory explores a relatively broad region, typical of regularized networks with cyclic schedules.

## Inputs

- trained deep neural network (PyTorch or TensorFlow model) mid-training or at epoch checkpoints
- feature matrix combining molecular descriptors and fingerprints (e.g., 5,666 descriptors + 2,214 MACCS166/Extended Connectivity/Path fingerprints)
- regression targets (e.g., experimental retention times in seconds)
- learning rate schedule configuration (cosine annealing with warm restarts)

## Outputs

- averaged model weights (parameter tensor)
- retrained neural network with SWA-updated weights
- evaluation metrics (mean absolute error and median absolute error on test set with uncertainty estimates)

## How to apply

After configuring the DNN with heavy L1/L2 regularization and cosine annealing warm restarts as the learning rate scheduler, enable weight averaging by collecting and averaging model weights at regular intervals during training—typically after each warm restart cycle or at the end of the final training epoch. The averaging operates by maintaining a running mean of all model parameter tensors encountered during the latter portion of training (often the final 10–20% of epochs). Once training completes, replace the final trained weights with the averaged weight tensor before final evaluation. The rationale is that cyclic learning rates cause the optimizer to explore a local region of the loss landscape; averaging weights from these diverse exploration points finds a solution with lower generalization error. Evaluate improvement by comparing mean absolute error and median absolute error on a held-out test set against the unaveraged model.

## Related tools

- **alvaDesc** (generates the 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) that serve as input features to the DNN before SWA is applied) — https://www.alvascience.com/alvadesc/
- **PyTorch or TensorFlow** (framework for implementing the DNN architecture, cosine annealing scheduler, and SWA weight averaging logic)

## Evaluation signals

- Mean absolute error (MAE) on held-out test set decreases and uncertainty (±σ) is within reported range (e.g., 39.2±1.2 s for SMRT dataset).
- Median absolute error (MdAE) on held-out test set is lower than model without SWA (e.g., 17.2 ± 0.9 s achieved vs. unaveraged baseline).
- Weight tensor statistics (e.g., mean, variance, norm) stabilize across averaged checkpoints, indicating convergence to a consistent solution.
- Cross-validation or nested cross-validation results show consistent improvement across multiple train–test splits, not just a single test fold.
- Averaged weights lie in a region of lower gradient magnitude, consistent with finding a flatter minimum in the loss landscape.

## Limitations

- SWA requires storing multiple checkpoint states during training, increasing memory overhead; this can be prohibitive for very large models or datasets.
- The method assumes the cyclic learning rate schedule (e.g., cosine annealing with warm restarts) is already tuned; poor schedule hyperparameters reduce SWA's benefit.
- SWA averaging assumes that weights collected from different epochs lie in the same local mode; if the optimizer jumps between disconnected regions, averaging may degrade performance.
- No guidance is provided in the article or README on the optimal number of weight snapshots to average, frequency of collection (per epoch, per cycle, etc.), or whether batch normalization layers require re-calibration after averaging.
- Improvement magnitude varies with dataset, model architecture, and regularization strength; transferability to other molecular property prediction tasks is not validated in the source work.

## Evidence

- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [other] Apply stochastic weight averaging during training to improve generalization.: "Apply stochastic weight averaging during training to improve generalization."
