---
name: cosine-annealing-learning-rate-scheduling
description: Use when when training a heavily regularized deep neural network on large
  molecular datasets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - PyTorch / TensorFlow
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cosine-annealing-learning-rate-scheduling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Cosine annealing with warm restarts is a learning rate scheduling strategy that cyclically reduces the learning rate following a cosine curve and periodically restarts to higher values, enabling exploration of multiple local minima and improved generalization in deep neural networks for regression tasks.

## When to use

When training a heavily regularized deep neural network on large molecular datasets (e.g., >80,000 samples) for continuous prediction tasks like retention time estimation, and you need to balance overfitting control with exploration of the loss landscape to achieve low generalization error on held-out test data.

## When NOT to use

- Input features are already low-dimensional (< 10 dimensions) or problems exhibit simple, unimodal loss landscapes where restarts are unnecessary.
- Training data is very small (< 1,000 samples) where regularization may be sufficient without annealing cycles.
- Real-time or online learning scenarios where periodic restarts introduce unacceptable computational overhead.

## Inputs

- training data with molecular fingerprint features (MACCS166, Extended Connectivity, Path Fingerprints)
- validation dataset for monitoring performance across restart cycles
- initialized deep neural network with L1/L2 regularization
- initial learning rate and restart period hyperparameters

## Outputs

- trained DNN model with learned weights after cosine annealing + SWA
- mean absolute error (MAE) and median absolute error metrics on test set
- learning rate schedule trajectory across training epochs

## How to apply

Initialize the cosine annealing warm restarts scheduler during DNN training alongside L1/L2 regularization. The scheduler reduces the learning rate following a cosine curve within each restart cycle, then periodically resets to a higher initial value to enable escape from local minima. Combine with stochastic weight averaging (SWA), which accumulates model weights across cycles to further reduce overfitting. Monitor validation performance (mean absolute error and median absolute error) across restart cycles; the periodic resets allow the optimizer to explore different regions of parameter space while regularization prevents divergence. This combination is particularly effective for fingerprint-based molecular feature inputs (e.g., MACCS166, Extended Connectivity, Path Fingerprints) where the loss landscape is complex and high variance in predictions can occur.

## Related tools

- **alvaDesc** (generates molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) that serve as input features for DNN training with cosine annealing scheduling) — https://www.alvascience.com/alvadesc/
- **PyTorch / TensorFlow** (deep learning framework providing cosine annealing warm restarts scheduler (torch.optim.lr_scheduler.CosineAnnealingWarmRestarts) and stochastic weight averaging utilities)

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models
```

## Evaluation signals

- Mean absolute error (MAE) converges to target value of 39.2±1.2 s on held-out test data from METLIN SMRT dataset.
- Median absolute error stabilizes around 17.2±0.9 s, indicating reduced outlier impact from annealing cycles.
- Validation loss exhibits periodic dips coinciding with cosine annealing restart cycles, confirming scheduler is active.
- Stochastic weight-averaged model outperforms individual models from any single restart cycle, demonstrating benefit of multi-cycle exploration.
- Generalization gap (validation error − training error) remains small despite large feature dimensionality (2,214 fingerprints), confirming regularization + annealing effectiveness.

## Limitations

- Performance depends critically on choice of restart period (Tcycle) and number of restarts; no principled method provided in the article for tuning these hyperparameters.
- Cosine annealing assumes smooth, continuous loss landscape; may not perform well on highly irregular or discontinuous optimization surfaces.
- Computational cost increases with number of restart cycles; trade-off between exploration and wall-clock training time not quantified.
- Method is demonstrated only on fingerprint-based features (MACCS166, Extended Connectivity, Path Fingerprints); transferability to other molecular representations or domains not established.

## Evidence

- [other] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2±0.9 s on retention time prediction.: "A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT); both retained and unretained molecules were considered.: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
