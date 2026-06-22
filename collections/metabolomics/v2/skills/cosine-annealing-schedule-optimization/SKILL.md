---
name: cosine-annealing-schedule-optimization
description: Use when when training a regularized deep neural network for molecular property regression (e.g., retention time prediction on the METLIN SMRT dataset with 80,038+ samples), use cosine annealing warm restarts to escape plateaus and improve convergence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - alvaDesc
  - PyTorch / TensorFlow
  - cmmrt
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
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

# Cosine-Annealing Schedule Optimization

## Summary

Cosine annealing with warm restarts is a learning rate scheduling strategy that cyclically reduces the learning rate following a cosine curve, periodically restarting to higher values to escape local minima. In retention time prediction for small molecules, this scheduling approach combined with stochastic weight averaging significantly improves deep neural network generalization.

## When to use

When training a regularized deep neural network for molecular property regression (e.g., retention time prediction on the METLIN SMRT dataset with 80,038+ samples), use cosine annealing warm restarts to escape plateaus and improve convergence. This is particularly valuable when your validation loss plateaus or when you need to balance exploration of the loss landscape against computational efficiency.

## When NOT to use

- When using simple linear regression or tree-based models that do not benefit from gradient-based learning rate schedules
- When training data is very small (<1,000 samples), where restart cycles may be too frequent relative to data size
- When prior hyperparameter tuning has already identified a fixed learning rate that works well; cosine annealing adds complexity that may not improve overfitting-prone small models

## Inputs

- Molecular descriptor matrix (5,666 features per molecule)
- Molecular fingerprint matrix (2,214 features: MACCS166, Extended Connectivity, Path Fingerprints)
- Retention time target vector (experimental ground truth in seconds)
- Training set from METLIN SMRT dataset (80,038 molecules minimum recommended)

## Outputs

- Trained DNN model with optimized learning rate trajectory
- Mean absolute error on test set (e.g., 39.2±1.2 s)
- Median absolute error on test set (e.g., 17.2±0.9 s)
- Learning rate schedule artifact (cosine annealing trajectory log)

## How to apply

Configure the learning rate scheduler to follow a cosine decay curve within each restart cycle, with periodic warm restarts that reset the learning rate to a higher value. During training on molecular descriptor and fingerprint feature matrices (5,666 descriptors + 2,214 fingerprints), apply this scheduler in conjunction with heavy L1/L2 regularization and stochastic weight averaging (SWA) to average model weights across cycles. The cosine schedule reduces the learning rate from initial value to near-zero following a cosine function, then jumps back up at restart points; this helps escape shallow local minima while allowing fine-tuning phases. Monitor mean absolute error (MAE) and median absolute error (MdAE) on held-out test sets to confirm improvements in both center and tail of the error distribution.

## Related tools

- **alvaDesc** (Generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) that serve as feature inputs to the DNN before cosine annealing is applied) — https://www.alvascience.com/alvadesc/
- **PyTorch / TensorFlow** (Deep learning framework implementing the DNN model and cosine annealing warm restarts scheduler (lr_scheduler.CosineAnnealingWarmRestarts))
- **cmmrt** (Reference implementation of cosine annealing warm restarts with stochastic weight averaging for retention time prediction on METLIN SMRT) — https://github.com/constantino-garcia/cmmrt

## Evaluation signals

- Mean absolute error converges to 39.2±1.2 s on held-out SMRT test set, confirming the schedule improves prediction accuracy
- Median absolute error achieves 17.2±0.9 s, indicating the method reduces tail errors and outlier sensitivity
- Validation loss exhibits periodic dips at restart points (evidence of escape from local minima) followed by smooth cosine decay
- Comparison with fixed learning rate or other schedules (step decay, exponential) shows lower final MAE and MdAE with cosine annealing
- Stochastic weight averaging checkpoint (averaged weights across restart cycles) outperforms final-epoch weights alone

## Limitations

- Requires careful tuning of restart period (T_0) and initial learning rate; suboptimal values can lead to oscillation or insufficient exploration
- Performance gains are most pronounced on large datasets (80,000+ molecules); benefit diminishes on smaller datasets where computational cost of restarts becomes prohibitive
- Must be combined with heavy regularization (L1/L2 penalties) and stochastic weight averaging to achieve reported error margins; cosine annealing alone does not guarantee 39.2 s MAE
- Not applicable to unretained molecules without special handling; the METLIN SMRT dataset includes both retained and unretained molecules, requiring class-aware loss weighting or separate models

## Evidence

- [intro] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s and median absolute error of 17.2 ± 0.9 s on retention time prediction.: "A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s and median absolute error of 17.2 ± 0.9 s"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT); both retained and unretained molecules were considered.: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) were generated with the alvaDesc software.: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) were generated with the alvaDesc software"
- [other] Apply stochastic weight averaging during training to improve generalization.: "Apply stochastic weight averaging during training to improve generalization"
