---
name: metabolite-rank-performance-evaluation
description: Use when after training an ensemble model (MLP, GNN, or ESP) on spectral data, use this skill to measure performance on test spectra where ground-truth metabolite identities are known. Essential for comparing model variants (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - LDA (Latent Dirichlet Allocation)
  - PyTorch
  - DGL (Deep Graph Library)
  - scikit-learn
  techniques:
  - LC-MS
  - GC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae490
  all_source_dois:
  - 10.1093/bioinformatics/btae490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-rank-performance-evaluation

## Summary

Evaluate ensemble spectral prediction models for metabolite annotation by computing average rank and Rank@K metrics on held-out test spectra. This skill quantifies how well predicted metabolite candidates rank the true chemical identity relative to the full NIST candidate set.

## When to use

After training an ensemble model (MLP, GNN, or ESP) on spectral data, use this skill to measure performance on test spectra where ground-truth metabolite identities are known. Essential for comparing model variants (e.g., MLP vs. GNN vs. ESP) and validating that ensemble weighting improves ranking performance over baseline approaches.

## When NOT to use

- Test set contains spectra without known ground-truth metabolite identity (unsupervised or unknown metabolites).
- Candidate list contains <5 candidates per spectrum; ranking metrics become uninformative when candidate pool is too small.
- Model has not been trained on a ranking task (e.g., purely regression or classification models without ranking loss) — use classification accuracy or MSE instead.

## Inputs

- Pre-trained model checkpoint (.pt file)
- Test candidate dataset (torch_tecand_*.pkl with spectral features and candidate metadata)
- Ground-truth metabolite identity labels for test spectra

## Outputs

- Average rank metric (mean rank position of true metabolite in candidate list)
- Rank@K metrics (fraction of spectra with true metabolite in top K, for K=1–20)
- Standard deviation of average rank across test set

## How to apply

Load pre-trained model weights (e.g., best_model_mlp_can.pt, best_model_gnn_can.pt, or ESP_can.pt) and a prepared test dataset containing spectra and their true metabolite identities. Run the model in inference mode on the test candidate dataset to generate ranked predictions for each spectrum. For each spectrum, compute the rank position of the true metabolite in the model's scored candidate list, then aggregate across all test spectra to compute average rank and Rank@K (the fraction of spectra where the true metabolite ranks in the top K positions, typically K=1,2,...,20). Report mean ± standard deviation for average rank and Rank@K curves to quantify annotation accuracy and compare to baseline models.

## Related tools

- **PyTorch** (Model loading and inference on test tensors; gradient-free evaluation loop)
- **DGL (Deep Graph Library)** (Graph neural network model instantiation and forward pass for GNN-based predictions)
- **scikit-learn** (Ranking metrics computation and statistical aggregation)

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Average rank value is lower for ensemble (ESP) than for individual baseline models (MLP, GNN); ESP should achieve ~23.7% improvement over MLP baseline (test set average rank ~339 for MLP, ~280 for ESP on NPLIB1).
- Rank@K curves are monotonically increasing (Rank@1 ≤ Rank@2 ≤ ... ≤ Rank@20) and asymptote toward 1.0 at large K.
- Standard deviation is reported alongside mean; values are typically large (e.g., ±1000+ on NPLIB1) due to wide range of spectrum difficulty.
- Evaluation script runs without NaN or infinity values; all predicted ranks are positive integers within [1, candidate_pool_size].
- When model is run on the same test set multiple times (deterministic inference), average rank and Rank@K metrics are identical (reproducibility check).

## Limitations

- Average rank is highly sensitive to candidate pool size and dataset composition; direct comparison across datasets with different candidate counts (e.g., NPLIB1 vs. NIST-20) requires normalization or separate reporting.
- Rank@K metrics may be dominated by easy-to-annotate spectra; median rank or percentile statistics can better reflect performance on hard spectra.
- Performance on EI/GC-MS data not validated in the ESP paper; results reported here are for ESI/LC-MS only.
- Ground-truth labels must be clean and unambiguous; if true metabolite is absent from the candidate list or duplicated, rank computation will fail or be misleading.

## Evidence

- [readme] average_rank_and_rank_at_k: "Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain over existing neural network approaches."
- [readme] esp_improvement_over_mlp: "23.7% increase in average rank performance on the full NIST candidate set"
- [readme] example_metrics_output: "Average rank 279.557 +- 1170.300
Rank at 1 0.187
Rank at 2 0.277
Rank at 3 0.328"
- [intro] ranking_task_training_context: "Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions"
- [other] evaluation_on_held_out_set: "Evaluate ensemble performance on held-out validation set and report ranking metrics (average rank, rank improvement over baseline MLP)."
