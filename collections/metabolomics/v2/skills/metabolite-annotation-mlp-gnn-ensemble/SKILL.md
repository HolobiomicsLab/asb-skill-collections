---
name: metabolite-annotation-mlp-gnn-ensemble
description: Use when you have ESI/LC-MS test spectra requiring metabolite annotation and need to compare ensemble-based neural network predictions (ESP) against a baseline MLP model to quantify performance gains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - github.com/HassounLab/ESP
  - ESP (Ensembled Spectral Prediction)
  - MLP baseline (NEIMS implementation)
  - GNN baseline model
  - LDA (Latent Dirichlet Allocation)
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

# metabolite-annotation-mlp-gnn-ensemble

## Summary

Ensemble spectral prediction (ESP) combines MLP and GNN models enhanced with multi-tasking on LDA spectral topic labels and attention mechanisms to improve metabolite annotation rank performance on ESI/LC-MS spectra. This skill reproduces the 23.7% average rank improvement of ESP over the MLP baseline and generates comparative performance metrics.

## When to use

Use this skill when you have ESI/LC-MS test spectra requiring metabolite annotation and need to compare ensemble-based neural network predictions (ESP) against a baseline MLP model to quantify performance gains. Specifically apply this skill when your goal is to measure and report average rank and Rank@K metrics to validate that the combined MLP–GNN ensemble with multi-tasking and attention outperforms single-model baselines by a known target margin (≥23.7% improvement).

## When NOT to use

- Input spectra are EI/GC-MS data (ESP shows improvements only on ESI/LC-MS; README states 'not EI/GC-MS data in NEIMS')
- Pre-trained models are unavailable and retraining is not feasible (ensemble models require prior MLP and GNN checkpoints)
- Spectral candidate set size differs substantially from the full NIST set (average rank metric is sensitive to candidate pool composition and generalization to smaller pools is not documented)

## Inputs

- Pre-trained ESP ensemble model (PyTorch .pt file, e.g., ESP_can.pt)
- Pre-trained MLP baseline model (PyTorch .pt file, e.g., best_model_mlp_can.pt)
- Pre-trained GNN model (PyTorch .pt file, e.g., best_model_gnn_can.pt)
- ESI/LC-MS test spectral dataset (PyTorch geometric .pkl file, e.g., torch_tecand_1000bin_te_cand100_torchgeometric.pkl)
- LDA spectral topic labels (derived from pos_train.csv or equivalent training data)

## Outputs

- Average rank metric for MLP baseline predictions (numerical value ± std dev)
- Average rank metric for ESP ensemble predictions (numerical value ± std dev)
- Rank@K curves for both models (K=1 to 20, cumulative fraction correct)
- Percentage performance improvement: ((ESP_rank − MLP_rank) / MLP_rank) × 100
- Comparison table with baseline vs. ensemble metrics and confidence intervals

## How to apply

Load pre-trained ESP, MLP, and GNN models from the HassounLab/ESP repository. Load the ESI/LC-MS test spectral dataset (e.g., NPLIB1 or NIST-20 preprocessed data). Generate predictions on test spectra using the MLP baseline model and the ESP ensemble model (which internally combines weighted predictions from MLP and GNN components enhanced with LDA-based multi-tasking on spectral topic labels and attention mechanisms to capture peak dependencies). Compute average rank and Rank@K metrics for both models on the full NIST candidate set. Calculate percentage performance gain using ((ESP_rank − MLP_rank) / MLP_rank) × 100. Verify that the ESP average rank improvement meets or exceeds the 23.7% threshold; report results in a comparison table with both baseline and ensemble metrics, including standard deviations.

## Related tools

- **ESP (Ensembled Spectral Prediction)** (Primary ensemble model that combines MLP and GNN predictions with multi-tasking on LDA spectral topics and attention mechanisms to generate ranked metabolite annotations) — https://github.com/HassounLab/ESP
- **MLP baseline (NEIMS implementation)** (Single-model baseline for comparison; generates spectral predictions via feed-forward neural network) — https://github.com/HassounLab/ESP
- **GNN baseline model** (Single-model baseline using graph neural networks to capture molecular graph structure; ensembled with MLP in ESP) — https://github.com/HassounLab/ESP
- **LDA (Latent Dirichlet Allocation)** (Generates spectral topic labels used as additional multi-tasking supervision to enhance MLP and GNN model representations)

## Examples

```
python ens_train_canopus.py --cuda 0 --disable_two_step_pred --disable_fingerprint --disable_mt_fingerprint --disable_mt_ontology --correlation_mat_rank 100 --full_dataset --mode 'canopus'
```

## Evaluation signals

- ESP average rank is lower (better) than MLP baseline average rank by ≥23.7% on the full NIST candidate set
- Rank@K curves for ESP are above (higher cumulative fraction) those of MLP across K=1 to 20
- Standard deviations reported for both metrics are non-zero and overlapping error bars confirm statistical stability
- Reported average rank ± std dev values match expected output ranges (MLP ~339 ± 1264, GNN ~241 ± 939, ESP ~279 ± 1170 on NPLIB1 test set)
- Output table includes both average rank and Rank@K metrics with consistent formatting and all 819 test spectra evaluated

## Limitations

- Models and reported metrics are trained and evaluated on NPLIB1 data only; NIST-20 models cannot be published due to NIST license restrictions, limiting reproducibility on industry-standard datasets
- Improvement margin (23.7% MLP over GNN shown; 37.2% GNN over baseline) varies by model pairing and dataset; generalization to other ESI/LC-MS datasets or alternative candidate sets is not documented
- Attention mechanism and LDA multi-tasking enhance the model but require careful hyperparameter tuning (e.g., mt_lda_weight=0.01, correlation_mix_residual_weight=0.7); sensitivity to these parameters is not explored in the README
- Computational cost of ensemble inference (combining MLP and GNN predictions with attention) is not reported; evaluation on large-scale real-world spectra may require GPU acceleration (optional but recommended)

## Evidence

- [other] ESP model achieves a 23.7% increase in average rank performance over the MLP model on ESI/LC-MS data: "We have shown improvements with ESP over the MLP model (implementation of NEIMS model (Wei et al., 2019) with a generalized dataset ESI/LC-MS but not EI/GC-MS data in NEIMS), in terms of a 23.7%"
- [readme] MLP and GNN models are enhanced by multi-tasking on LDA spectral topic labels and attention mechanisms: "First, the MLP and GNN are enhanced by: 1) multi-tasking on additional data (spectral topic labels obtained using LDA (Latent Dirichlet Allocation), and 2) attention mechanism to capture dependencies"
- [readme] Ensemble model trained on ranking tasks to generate weighted average of MLP and GNN predictions: "Next, we create an Ensembled Spectral Prediction (ESP) model that is trained on ranking tasks to generate the average weighted MLP and GNN spectral predictions"
- [readme] Performance metrics are average rank and Rank@K on test spectra: "Our results, measured in average rank and Rank@K for the test spectra, show remarkable performance gain over existing neural network approaches"
- [readme] Pre-trained models on NPLIB1 dataset are available; NIST-20 models cannot be published: "The pretrained MLP, GNN, and ESP models on the NPLIB1 dataset are `/pretrained_models/best_model_mlp_can.pt`, `/pretrained_models/best_model_gnn_can.pt`, and `/pretrained_models/ESP_can.pt`,"
