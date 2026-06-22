---
name: metabolite-annotation-ensemble-ranking
description: Use when you have ESI/LC-MS test spectra requiring candidate metabolite ranking, pre-trained MLP (NEIMS) and GNN baseline models are available or can be trained, you seek quantified improvement over single-model average rank performance (baseline MLP shows ~339 average rank), and your evaluation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3577
  tools:
  - github.com/HassounLab/ESP
  - MLP (Multi-Layer Perceptron) baseline model
  - GNN (Graph Neural Network) baseline model
  - LDA (Latent Dirichlet Allocation)
  - PyTorch & DGL
  - ens_train_canopus.py
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1093/bioinformatics/btae490
  title: ESP
evidence_spans:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-ensemble-ranking

## Summary

Combines MLP and GNN neural network models enhanced with multi-tasking on LDA spectral topic labels and attention mechanisms into an ensemble trained on ranking tasks to improve metabolite annotation performance on mass spectra. Apply this skill when you need to rank candidate metabolites from ESI/LC-MS spectra and want to exceed single-model baseline performance.

## When to use

You have ESI/LC-MS test spectra requiring candidate metabolite ranking, pre-trained MLP (NEIMS) and GNN baseline models are available or can be trained, you seek quantified improvement over single-model average rank performance (baseline MLP shows ~339 average rank), and your evaluation metric is average rank or Rank@K on a full candidate set (e.g., NIST).

## When NOT to use

- Input spectra are EI/GC-MS (ESP shows improvements only on ESI/LC-MS; README states 'in terms of a 23.7% increase in average rank performance on the full NIST candidate set' and compares to NEIMS which uses EI/GC-MS).
- Pre-trained MLP or GNN models are unavailable and retraining on your dataset is infeasible (ensemble training requires convergent baseline models).
- Your evaluation metric is not average rank or Rank@K (e.g., if precision/recall on top-1 or molecular fingerprint similarity is the goal, ensemble ranking may not be the right choice).

## Inputs

- pre-trained MLP baseline model (.pt file, implementation of NEIMS on ESI/LC-MS data)
- pre-trained GNN baseline model (.pt file)
- ESI/LC-MS test spectral dataset (torch tensor format or .pkl)
- test candidate set (full NIST or similar, with InChiKey mappings)

## Outputs

- trained ESP ensemble model (.pt file)
- average rank metric for ESP predictions (lower is better)
- Rank@K curves (Rank@1 through Rank@20 or higher)
- percentage performance gain relative to MLP baseline
- comparison table with baseline and ensemble metrics

## How to apply

First, ensure MLP and GNN baseline models are pre-trained or train them using the repository's train.py script with multi-tasking disabled (--disable_mt_lda, --disable_mt_fingerprint, --disable_mt_ontology flags). Load the test spectral dataset and generate predictions from both baseline models independently. Train an ESP ensemble model using ens_train_canopus.py with the pre-trained MLP and GNN models, which learns weighted averaging of predictions through ranking task optimization. Compute average rank and Rank@K metrics for both baseline and ensemble predictions on the test set. Calculate percentage improvement as ((ESP_rank − MLP_rank) / MLP_rank) × 100, targeting at least 23.7% gain for ESI/LC-MS data. The ensemble learns to weight model outputs via a ranking loss rather than equal averaging, leveraging complementary strengths of MLP sequence processing and GNN graph-based molecular structure reasoning.

## Related tools

- **MLP (Multi-Layer Perceptron) baseline model** (Base neural network for spectral peak sequence prediction; enhanced with LDA multi-tasking and attention; one of two inputs to ensemble) — github.com/HassounLab/ESP
- **GNN (Graph Neural Network) baseline model** (Base neural network for molecular structure graph prediction; enhanced with LDA multi-tasking and attention; one of two inputs to ensemble) — github.com/HassounLab/ESP
- **LDA (Latent Dirichlet Allocation)** (Generates spectral topic labels for multi-task learning auxiliary task on both MLP and GNN)
- **PyTorch & DGL** (Deep learning framework for model training, inference, and tensor operations) — github.com/HassounLab/ESP
- **ens_train_canopus.py** (Training script for ESP ensemble model; orchestrates loading of pre-trained MLP/GNN, ranking task optimization, and evaluation) — github.com/HassounLab/ESP

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- Ensemble average rank is lower (better) than both MLP and GNN baselines by at least 23.7% relative to MLP (e.g., if MLP = 339.350, ESP ≤ 258.5).
- Rank@K curve for ESP is monotonically non-decreasing and lies above (better than) baseline curves across all K values from 1 to 20.
- ESP model file is successfully saved and loads without errors using PyTorch; model architecture reflects weighted ensemble of MLP and GNN outputs.
- Standard deviation of average rank is reported and shows ensemble variance is reasonable (not inflated relative to baselines).
- Training converges within expected epoch count (README example shows convergence within 100 epochs for ESP); loss curves show monotonic or smooth improvement.

## Limitations

- Performance gains are demonstrated only on ESI/LC-MS data with NPLIB1 and NIST-20 candidate sets; EI/GC-MS improvement not validated (README: 'Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data').
- NIST-20 pre-trained models cannot be published due to NIST license restrictions; users must either use NPLIB1 models or retrain on their own data (README: 'In accordance with NIST license regulations, we are unable to publish the NIST-20 data alongside our models').
- Ensemble performance depends on quality and diversity of baseline MLP and GNN models; if baselines are poorly trained or highly correlated, ensemble gains diminish.
- Requires sufficient GPU/CPU memory (8 GB RAM minimum) and computational time for training (README example: 819 test spectra processed in ~15 seconds on GPU for inference).

## Evidence

- [readme] 23.7% increase in average rank performance: "We have shown improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS), in terms of a 23.7%"
- [readme] Ensemble trained on ranking tasks: "Next, we create an Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions."
- [readme] Multi-tasking on LDA spectral topic labels and attention mechanisms: "First, the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies"
- [other] ESI/LC-MS test spectra workflow: "Load the pre-trained ESP ensemble model and MLP baseline model from the github.com/HassounLab/ESP repository. 2. Load the ESI/LC-MS test spectral dataset. 3. Generate predictions on test spectra"
- [other] Average rank metric computation: "Compute average rank performance metric for MLP baseline predictions. 6. Compute average rank performance metric for ESP ensemble predictions. 7. Calculate the percentage performance gain: ((ESP_rank"
- [readme] Pre-trained model files location: "The pretrained MLP, GNN, and ESP models on the NPLIB1 dataset are `/pretrained_models/best_model_mlp_can.pt`, `/pretrained_models/best_model_gnn_can.pt`, and `/pretrained_models/ESP_can.pt`,"
- [readme] Baseline MLP average rank benchmark: "Average rank 339.350 +- 1264.715"
- [readme] ESP average rank result: "Average rank 279.557 +- 1170.300"
