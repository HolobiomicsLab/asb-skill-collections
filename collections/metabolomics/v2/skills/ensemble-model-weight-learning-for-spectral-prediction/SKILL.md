---
name: ensemble-model-weight-learning-for-spectral-prediction
description: Use when you have pre-trained MLP and GNN models that generate different spectral predictions for the same metabolite candidates, and you want to combine them to improve ranking performance (average rank, Rank@K metrics) without retraining the base models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LDA (Latent Dirichlet Allocation)
  - PyTorch
  - DGL (Deep Graph Library)
  - PyTorch Geometric
  - ESP
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
- spectral topic labels obtained using LDA (Latent Dirichlet Allocation)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_esp_cq
    doi: 10.1093/bioinformatics/btae490
    title: ESP
  dedup_kept_from: coll_esp_cq
schema_version: 0.2.0
---

# Ensemble Model Weight Learning for Spectral Prediction

## Summary

Train an ensemble weighting layer on ranking tasks to learn optimal weights for combining MLP and GNN spectral predictions into a single weighted-average prediction for metabolite annotation. This approach improves annotation accuracy by leveraging complementary strengths of both neural network architectures through task-specific optimization.

## When to use

You have pre-trained MLP and GNN models that generate different spectral predictions for the same metabolite candidates, and you want to combine them to improve ranking performance (average rank, Rank@K metrics) without retraining the base models. Use this skill when you have a ranking task dataset with true metabolite rank labels and aim to learn adaptive weights for each model's contribution.

## When NOT to use

- Base MLP and GNN models are not yet trained or enhanced with multi-task LDA and attention mechanisms—train them first using task_id=task_001 and task_id=task_002.
- You lack a ranking task dataset with true metabolite rank labels; ensemble training requires supervised ranking objectives.
- Your goal is only to predict spectral properties (e.g., fragment intensities) rather than to rank metabolite candidates—use individual MLP or GNN models directly.

## Inputs

- Pre-trained MLP model (PyTorch .pt file with multi-task LDA and attention enhancements)
- Pre-trained GNN model (PyTorch .pt file with multi-task LDA and attention enhancements)
- Ranking task dataset with spectra and ground-truth metabolite rank labels (e.g., pos_train.csv formatted data)
- Test candidate set with candidate size and resolution parameters (e.g., 100 candidates per spectrum, 1000 bins)

## Outputs

- Trained ensemble weighting parameters (PyTorch .pt model file, e.g., ESP_can.pt)
- Weighted-average spectral predictions for test spectra
- Ranking metrics on test set (average rank ± std dev, Rank@1 through Rank@20)

## How to apply

Load the pre-trained MLP and GNN models enhanced with multi-task learning on LDA spectral topic labels and attention mechanisms. Prepare a ranking task dataset containing spectra with ground-truth metabolite rank labels. Initialize an ensemble weighting layer and define a ranking loss function (listwise or pairwise ranking objective). Train the ensemble on the ranking dataset using gradient descent to learn optimal weights that combine MLP and GNN outputs as: weighted_prediction = w_mlp * mlp_output + w_gnn * gnn_output. Evaluate the ensemble on a held-out validation set using ranking metrics (average rank, Rank@K) to verify that the learned weights improve upon individual model baselines.

## Related tools

- **PyTorch** (Deep learning framework for defining, training, and saving ensemble weighting layers and ranking loss functions)
- **DGL (Deep Graph Library)** (Framework for managing GNN models and graph-based spectral data processing)
- **PyTorch Geometric** (Geometric deep learning library for loading and handling GNN candidate ranking datasets)
- **LDA (Latent Dirichlet Allocation)** (Generates spectral topic labels used as multi-task learning targets to enhance base MLP and GNN models)
- **ESP** (Full implementation of ensemble model, training loop, and ranking evaluation metrics) — https://github.com/HassounLab/ESP

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Ensemble average rank on test set is lower (better) than both baseline MLP and baseline GNN average ranks—expected improvement ≥23.7% over MLP baseline (e.g., MLP: 339.35 → ESP: 184.8 or better).
- Rank@K metrics (Rank@1–Rank@20) for the ensemble are monotonically increasing and exceed both individual model curves across all K.
- Learned ensemble weights (w_mlp, w_gnn) are non-negative and sum approximately to 1.0, indicating a valid weighted combination.
- Training loss (ranking objective) on the training set decreases monotonically and plateaus; validation ranking metrics do not show consistent degradation (no severe overfitting).
- Ensemble predictions on held-out test set are reproducible: same model file and hyperparameters yield identical average rank and Rank@K values.

## Limitations

- Ensemble weight learning depends critically on the quality and diversity of base MLP and GNN models; if both models are poorly trained or highly correlated, ensemble improvement is limited.
- Ranking task dataset must have sufficient size and representative metabolite rank distribution; small or biased ranking datasets may lead to overfitted or poorly generalized weights.
- The method is evaluated on ESI/LC-MS data and NPLIB1 dataset; performance on EI/GC-MS data or other spectral databases is not reported and may differ.
- Pre-trained models are published only for NPLIB1 data; NIST-20 models cannot be published due to license restrictions, limiting reproducibility on proprietary datasets.

## Evidence

- [intro] Ensemble model trained on ranking tasks to generate weighted average MLP and GNN predictions: "Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions"
- [intro] Multi-task learning on spectral topic labels and attention mechanisms enhance base models: "the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among"
- [intro] ESP ensemble shows 23.7% average rank improvement over MLP baseline: "23.7% increase in average rank performance over MLP model on ESI/LC-MS data"
- [readme] Training procedure for ensemble on ranking tasks using pre-trained models: "Before you train a new ESP model, you must have pretrained MLP and GNN models. To train a new ESP model, set `--te_cand_dataset_suffix` to an empty string or don't call this argument."
- [readme] Example ranking metric evaluation (Average rank ± std dev and Rank@K): "Average rank 279.557 +- 1170.300
Rank at 1 0.187
Rank at 2 0.277
Rank at 3 0.328"
