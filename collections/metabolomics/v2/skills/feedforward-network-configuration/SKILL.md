---
name: feedforward-network-configuration
description: Use when when implementing multiple spectrum predictor baseline models (NEIMS, MassFormer, etc.) and you need to isolate the impact of encoder architecture on predictive performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2275
  tools:
  - NEIMS
  - coleygroup/ms-pred
  - PyTorch / TensorFlow
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
- doi: 10.1021/acscentsci.9b00085
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  dedup_kept_from: coll_iceberg_fragmentation_graph_generation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  - 10.1021/acscentsci.9b00085
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feedforward Network Configuration

## Summary

Configure and implement FFN encoder architectures for mass spectrum prediction with matched hyperparameters and covariates across baseline models to enable fair performance comparison. This skill ensures that encoder variants (FFN vs. GNN) are trained under equivalent conditions so that architectural differences—rather than hyperparameter mismatches—drive performance variation.

## When to use

When implementing multiple spectrum predictor baseline models (NEIMS, MassFormer, etc.) and you need to isolate the impact of encoder architecture on predictive performance. Use this skill when you have a fixed dataset, feature set, and hyperparameter sweep range, but want to compare FFN and GNN encoders under strictly controlled conditions to avoid confounding the comparison with tuning differences.

## When NOT to use

- If hyperparameter settings differ between the FFN and GNN variants (e.g., one uses learning rate 1e-3 and the other 1e-4)—hyperparameter mismatch invalidates fair comparison of architectural effects.
- If covariates or input feature sets differ between encoders; the comparison requires identical feature engineering upstream of the encoder.
- If you only have access to pretrained weights for one encoder type and cannot retrain both under matched conditions; fair comparison requires paired training.

## Inputs

- Molecular dataset with extracted features and covariates (e.g., NIST'20 or MassSpecGym in .SDF or HDF5 format)
- Hyperparameter sweep specification (learning rate ranges, batch sizes, regularization coefficients, random seeds)
- Training/validation/test split assignments for molecules
- Target spectrum labels and experimental metadata (collision energy, ionization mode)

## Outputs

- Trained FFN encoder model checkpoint
- Trained GNN encoder model checkpoint
- Performance comparison report with metrics (spectral prediction accuracy, retrieval rank-1 accuracy, intensity MAE) for each encoder
- Training curve plots (loss vs. epoch) for both encoders showing convergence behavior
- Architecture configuration log documenting layer sizes, activation functions, and hyperparameters used

## How to apply

First, establish a common set of molecular covariates (input features extracted from the spectrum dataset) and a single hyperparameter sweep specification (learning rates, batch sizes, regularization, random seeds). Implement the FFN encoder variant by stacking fully connected layers with the specified dimensions and activation functions, initialized with the same random seed. In parallel, implement the GNN encoder using the same input covariates, hyperparameter values, and random seed initialization. Train both encoders on the identical training split for the same number of epochs, logging loss and validation metrics at each step. After training, evaluate both on the held-out test set using the same metrics (e.g., spectral cosine similarity, retrieval accuracy). Document any divergence between the two encoders' training curves or final performance to identify whether differences stem from architectural expressiveness or optimization dynamics.

## Related tools

- **NEIMS** (Baseline spectrum prediction model providing both FFN and GNN encoder reference implementations for configuration comparison) — https://pubs.acs.org/doi/full/10.1021/acscentsci.9b00085
- **coleygroup/ms-pred** (Repository containing unified implementation of FFN and GNN encoders with hyperparameter sweep harness and evaluation scripts) — https://github.com/coleygroup/ms-pred
- **PyTorch / TensorFlow** (Deep learning framework for implementing and training the FFN and GNN encoder architectures)

## Examples

```
python src/ms_pred/dag_pred/train_gen.py --config configs/neims_ffn.yaml --hyperparams configs/sweep_baseline.yaml --seed 1 && python src/ms_pred/dag_pred/train_gen.py --config configs/neims_gnn.yaml --hyperparams configs/sweep_baseline.yaml --seed 1
```

## Evaluation signals

- Both encoders trained on identical splits and hyperparameters report consistent loss curves for the first few epochs before diverging; indicates training is properly initialized and matched.
- Test set performance metrics for both encoders fall within a reasonable range (e.g., within 5% relative difference in cosine similarity); large divergence suggests hyperparameter or implementation mismatch rather than architectural difference.
- Random seed reproducibility: re-training both encoders with the same seed produces identical loss values and weight initializations.
- Hyperparameter log file exactly matches across both encoder configurations (layer dimensions, learning rate, batch size, regularization term, optimizer state).
- Model checkpoint files contain architecture metadata confirming encoder type (FFN vs. GNN) and layer configuration for post-hoc audit.

## Limitations

- Equivalent hyperparameter settings may not be optimal for both encoder types; FFN and GNN may have different effective learning rate ranges or batch size sensitivities, so 'fair' tuning may underperform one architecture.
- Matched random seeds ensure reproducibility but do not account for architectural differences in gradient flow or parameter initialization variance; GNNs may converge to different local minima even with identical seed and loss landscape.
- Configuration of GNN encoder (message passing layers, graph pooling, neighbor aggregation) introduces additional design choices beyond FFN that are difficult to fully 'match'; reported findings should acknowledge this irreducible structural difference.

## Evidence

- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.)"
- [other] NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison of spectrum prediction approaches.: "NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps)"
- [other] Train both encoder variants on the same training set with matched hyperparameters and random seeds. Evaluate both trained models on held-out test data and record performance metrics for each encoder type.: "Train both encoder variants on the same training set with matched hyperparameters and random seeds. Evaluate both trained models on held-out test data and record performance metrics"
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
