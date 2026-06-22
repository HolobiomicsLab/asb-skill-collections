---
name: ranking-task-loss-optimization
description: Use when you have multiple pre-trained neural network models (e.g., MLP and GNN) that produce overlapping predictions on the same set of candidates, and your evaluation metric is rank-based (average rank, Rank@K) rather than point-wise accuracy or RMSE.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - LDA (Latent Dirichlet Allocation)
  - PyTorch
  - DGL (Deep Graph Library)
  - PyTorch Geometric
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

# ranking-task-loss-optimization

## Summary

Train an ensemble model to learn optimal prediction weights by optimizing a ranking loss function (listwise or pairwise) on ranking task datasets. This approach enables the ensemble to generate weighted-average predictions that minimize ranking error rather than regression error alone.

## When to use

You have multiple pre-trained neural network models (e.g., MLP and GNN) that produce overlapping predictions on the same set of candidates, and your evaluation metric is rank-based (average rank, Rank@K) rather than point-wise accuracy or RMSE. Use this skill when you want to learn data-driven weights for combining these models to optimize ranking performance rather than using fixed or simple average weighting.

## When NOT to use

- Input datasets lack true rank labels or ground-truth compound identity; ranking loss requires supervisory signal.
- Base models (MLP, GNN) have not been pre-trained or are still in early training; ensemble training assumes stable, converged base models.
- Evaluation metric is point-wise accuracy or MSE rather than ranking-based; use regression or classification loss instead.

## Inputs

- Pre-trained MLP model checkpoint (.pt file)
- Pre-trained GNN model checkpoint (.pt file)
- Ranking task training dataset with true metabolite rank labels and candidate sets
- Ranking task validation dataset with same structure
- Ranking task test dataset with same structure

## Outputs

- Trained ensemble weighting layer checkpoint (.pt file)
- Weighted-average spectral predictions for test spectra
- Ranking metrics: average rank, rank standard deviation, Rank@K (K=1–20)

## How to apply

Load pre-trained MLP and GNN spectral prediction models enhanced with multi-task learning on spectral topic labels (via LDA) and attention mechanisms. Prepare a ranking task dataset with true metabolite rank labels (e.g., known correct compound ranked against full candidate set). Initialize an ensemble weighting layer (e.g., learnable scalar weights or a small neural network) and define a ranking loss function—either listwise (e.g., LambdaMART-style) or pairwise (e.g., margin-based)—that directly optimizes ranking metrics. Train the ensemble using gradient descent on the ranking loss, updating only the weighting layer while keeping base model parameters frozen. Generate weighted-average predictions by combining MLP and GNN outputs with the learned weights. Evaluate on held-out test data using ranking metrics (average rank, Rank@K) to confirm improvement over baseline MLP or GNN models.

## Related tools

- **LDA (Latent Dirichlet Allocation)** (Generate spectral topic labels used in multi-task learning to enhance MLP and GNN base models before ensemble training)
- **PyTorch** (Deep learning framework for defining, training, and checkpointing the ensemble weighting layer and ranking loss optimization)
- **DGL (Deep Graph Library)** (Graph neural network library used by the GNN base model for spectral peak dependency modeling)
- **PyTorch Geometric** (Graph neural network library variant used for candidate set representation in the ensemble pipeline)

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Ensemble average rank on test set is significantly lower (better) than baseline MLP model average rank (e.g., 23.7% improvement as reported for ESP on ESI/LC-MS data).
- Learned ensemble weights are non-uniform and stable across validation folds, indicating the optimization has discovered meaningful model contributions (not a trivial uniform average).
- Rank@K metrics (K=1–20) improve monotonically or consistently across the ensemble compared to baseline models, particularly at early ranks (Rank@1, Rank@5).
- Ranking loss converges smoothly during training without divergence, and validation loss follows a similar trend, indicating proper regularization and hyperparameter tuning.
- Ensemble predictions on held-out test spectra correctly rank the true metabolite identity higher than the baseline MLP or GNN alone on ≥80% of test cases.

## Limitations

- Ensemble training is sensitive to quality and scale of pre-trained base models; poorly trained or overfit base models will limit ensemble gains.
- Ranking loss optimization requires large, labeled ranking datasets; performance may degrade on metabolomics data types (e.g., EI/GC-MS) or library formats not represented in training, as noted for NEIMS-derived models.
- Learned weights are specific to the base model pair and training data distribution; retraining is needed when base models or candidate libraries change significantly.
- Computational cost of ranking loss (e.g., listwise objectives) scales with candidate set size; performance on datasets with >10,000 candidates per spectrum may require approximations or subsampling.

## Evidence

- [intro] Ensemble model trained on ranking tasks to generate weighted average MLP and GNN predictions: "Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions"
- [other] Ranking loss function used during ensemble training optimization: "define ranking loss function (e.g., listwise or pairwise ranking objective). 4. Train the ensemble loop on ranking tasks to learn optimal weights for MLP and GNN predictions, using gradient descent."
- [intro] Multi-task learning and attention mechanisms enhance base models before ensemble: "the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies among"
- [intro] Ensemble performance improvement over MLP baseline: "23.7% increase in average rank performance over MLP model on ESI/LC-MS data"
- [readme] Pre-trained model checkpoints and training script for ensemble: "To train a new ESP model, set `--te_cand_dataset_suffix` to an empty string or don't call this argument. `--ens_model_file_suffix` should start with `ESP`. This will generate a file with parameters"
