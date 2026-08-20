---
name: spectral-prediction-model-fusion
description: Use when you have pre-trained MLP and GNN spectral prediction models
  evaluated on the same ESI/LC-MS test dataset, and you seek to improve average rank
  performance beyond either baseline model alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - LDA (Latent Dirichlet Allocation)
  - github.com/HassounLab/ESP
  - PyTorch
  - DGL (Deep Graph Library)
  - PyTorch Geometric
  - ESP repository (HassounLab/ESP)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
- spectral topic labels obtained using LDA (Latent Dirichlet Allocation)
- github.com/HassounLab/ESP
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-prediction-model-fusion

## Summary

Combine heterogeneous spectral prediction models (MLP and GNN) into a single ensemble through ranking-task-based training to generate weighted average predictions for improved metabolite annotation. This skill is applied when independent models with complementary strengths (sequential feature processing vs. graph-based dependency capture) need to be unified into a ranking-optimized prediction system.

## When to use

You have pre-trained MLP and GNN spectral prediction models evaluated on the same ESI/LC-MS test dataset, and you seek to improve average rank performance beyond either baseline model alone. Apply this skill when you need to quantify and operationalize the contribution of each model to a final ranked candidate list for metabolite annotation.

## When NOT to use

- Input MLP and GNN models are not pre-trained or have not been enhanced with multi-task learning on spectral topic labels and attention mechanisms—the ensemble assumes both models leverage these complementary enhancements.
- True ranking labels for the ensemble training task are unavailable or the ranking task is not well-defined (e.g., only binary correct/incorrect labels are available).
- Test spectral data differ fundamentally from ESI/LC-MS (e.g., EI/GC-MS data)—the ESP model is trained and validated on ESI/LC-MS and may not generalize to other ionization modes or chromatographic methods.

## Inputs

- pre-trained MLP spectral prediction model (PyTorch .pt file)
- pre-trained GNN spectral prediction model (PyTorch .pt file)
- ranking task dataset with true metabolite rank labels (CSV or pickle format)
- ESI/LC-MS test spectral data (torch tensor format)

## Outputs

- trained ESP ensemble model with learned weights (.pt file)
- weighted-average spectral predictions for test spectra
- average rank and Rank@K performance metrics on validation/test set
- comparison table of baseline MLP, GNN, and ESP metrics

## How to apply

Load pre-trained MLP and GNN spectral prediction models that have been enhanced with multi-task learning on LDA-derived spectral topic labels and attention mechanisms to capture peak dependencies. Prepare a ranking task dataset with true metabolite rank labels (e.g., ordering candidate metabolites by correctness). Initialize an ensemble weighting layer and define a ranking loss function (listwise or pairwise ranking objective). Train the ensemble on ranking tasks using gradient descent to learn optimal scalar weights for each model's predictions. During inference, apply these learned weights to compute weighted-average predictions from both models. Evaluate on held-out validation spectra using average rank and Rank@K metrics to confirm the ensemble outperforms baseline MLP performance by the target margin (e.g., 23.7% improvement).

## Related tools

- **LDA (Latent Dirichlet Allocation)** (Generates spectral topic labels used as auxiliary multi-task learning targets to enhance both MLP and GNN base models before ensemble training)
- **PyTorch** (Deep learning framework used for implementing ensemble weighting layer, ranking loss computation, and gradient-based optimization of ensemble weights)
- **DGL (Deep Graph Library)** (Graph neural network library used to implement and load the pre-trained GNN spectral prediction model)
- **PyTorch Geometric** (Alternative graph representation library for constructing and processing molecular graph structures in GNN model)
- **ESP repository (HassounLab/ESP)** (Contains pre-trained MLP, GNN, and ESP ensemble models, training scripts (ens_train_canopus.py), and evaluation harness) — https://github.com/HassounLab/ESP

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Ensemble average rank metric on held-out test set must be lower (better) than both baseline MLP and GNN average ranks, with target improvement of ≥23.7% over MLP baseline.
- Rank@K curves (reported for K=1–20) for ESP must dominate (lie above) both baseline MLP and GNN curves across the full K range, confirming improved ranking across all cutoff depths.
- Learned ensemble weights must be positive and sum to 1.0 (or are properly normalized); weights should reflect model complementarity (neither weight should be close to 0 or 1).
- Training loss (ranking objective) must monotonically decrease or plateau over ensemble training epochs; validation average rank should improve or stabilize, indicating convergence.
- Predictions on the full NIST candidate set (not just top K) should show statistically significant improvement in average rank with reduced variance, confirming ensemble robustness across the full metabolite search space.

## Limitations

- ESP model is trained and validated on NPLIB1 and ESI/LC-MS data; generalization to EI/GC-MS spectra or other ionization modes is not demonstrated in the article and may fail.
- Ensemble weights are learned on a specific ranking task and dataset; retraining is required if switching datasets (e.g., from NPLIB1 to NIST-20) or if the ranking task definition changes.
- The approach assumes that MLP and GNN models capture sufficiently different aspects of spectral information to warrant ensembling; if models are highly correlated or one dominates, ensemble gains may be minimal.
- NIST-20 data cannot be published alongside pre-trained models due to license restrictions; users must obtain and preprocess NIST-20 independently if they wish to reproduce results on that dataset.

## Evidence

- [intro] Ensemble model combining MLP and GNN approaches improves metabolite annotation performance: "We propose a novel ensemble model to take advantage of both MLP and GNN models."
- [readme] 23.7% improvement on ESI/LC-MS test data: "We have shown improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS), in terms of a 23.7%"
- [readme] Multi-task learning and attention mechanisms enhance base models: "First, the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies"
- [readme] Training procedure uses ranking tasks for ensemble weighting: "Next, we create an Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions."
- [readme] Evaluation uses average rank and Rank@K metrics: "Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain over existing neural network approaches."
- [readme] Data and license restrictions: "In accordance with NIST license regulations, we are unable to publish the NIST-20 data alongside our models trained on NIST-20."
