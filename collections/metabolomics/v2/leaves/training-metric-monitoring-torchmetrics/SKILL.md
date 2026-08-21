---
name: training-metric-monitoring-torchmetrics
description: Use when during supervised model training loops when you need to log
  loss and validation metrics at each epoch to assess whether the model is learning
  properly and to determine when to stop training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - PyG
  - RDKit
  - NumPy
  - Pandas
  - TorchMetrics
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyTorch
  - PyG (PyTorch Geometric)
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
evidence_spans:
- '**Python**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
- '**NumPy**'
- '**Pandas**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_abcort_cq
    doi: 10.1021/acs.jcim.4c02179
    title: ABCoRT
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# training-metric-monitoring-torchmetrics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Monitor and track model training performance metrics (loss, validation accuracy) in real time during PyTorch training using TorchMetrics. This skill is essential for detecting convergence, overfitting, and training stability in graph neural network models like ABCoRT.

## When to use

Apply this skill during supervised model training loops when you need to log loss and validation metrics at each epoch to assess whether the model is learning properly and to determine when to stop training. Use it specifically when training ABCoRT or similar PyTorch + PyG models on retention-time prediction tasks where validation performance is a key stopping criterion.

## When NOT to use

- When you are running inference only and have no ground-truth labels to compare against.
- When using pre-trained fixed-weight models where no backpropagation or parameter updates occur.
- When computational resources are so limited that metric computation overhead is prohibitive and you can afford no visibility into training.

## Inputs

- PyTorch model (instantiated graph neural network)
- Training data loader (batched molecular graphs and retention-time targets)
- Validation data loader (hold-out graphs and targets)
- Loss function (e.g., MSE for regression)

## Outputs

- Training loss trajectory (per-epoch scalar values)
- Validation loss trajectory (per-epoch scalar values)
- Convergence status (plateauing, diverging, or improving)
- Model checkpoint at best validation performance

## How to apply

Instantiate TorchMetrics objects for the metrics you wish to track (e.g., loss, accuracy) within your training script. Call the appropriate metric update method in each training loop iteration, passing the model predictions and ground-truth labels. At the end of each epoch, compute and log the aggregated metric values to monitor training progress. The ABCoRT training workflow uses TorchMetrics to log loss and validation metrics over epochs, allowing the practitioner to observe when performance plateaus or diverges and to save model checkpoints at points of best validation performance. Rationale: real-time metric monitoring prevents wasted computation on diverging or overfitting models and provides empirical evidence of successful training convergence.

## Related tools

- **TorchMetrics** (Logging and aggregating loss and validation metrics across training epochs)
- **PyTorch** (Providing the training loop, backward pass, and optimizer steps that TorchMetrics tracks)
- **PyG (PyTorch Geometric)** (Providing graph neural network architecture and data loaders for molecular graph batches)

## Examples

```
python train_SMRT.py
```

## Evaluation signals

- Training loss decreases monotonically or shows steady downward trend over epochs (no divergence).
- Validation loss exhibits a U-shaped curve: initial decrease followed by potential plateau or slight increase (sign of overfitting), indicating the model has learned meaningful patterns.
- Metrics are computed and logged at the end of each epoch with no NaN or infinite values.
- Model checkpoint saved at epoch with lowest validation loss contains weights different from initialization.
- Training stops when validation loss plateaus (no improvement for N consecutive epochs), preventing wasted computation.

## Limitations

- TorchMetrics require ground-truth labels; cannot be applied during pure inference or unsupervised training.
- Metric computation adds overhead to each training iteration; on very small datasets or with very frequent logging, this overhead may be non-negligible.
- Validation metrics only reflect performance on the validation set; poor validation performance does not guarantee poor generalization to held-out test data, requiring a separate test evaluation.
- No automatic threshold or heuristic for 'good' validation performance is provided; practitioners must inspect trajectories visually or define domain-specific stopping criteria.

## Evidence

- [other] Monitor training via TorchMetrics for loss and validation metrics over epochs.: "Monitor training via TorchMetrics for loss and validation metrics over epochs."
- [other] The training entry point instantiates the graph neural network and trains on SMRT data.: "Execute the training entry point using Python with the command 'python train_SMRT.py', which will instantiate the graph neural network architecture (PyTorch + PyG) and train on the SMRT data."
