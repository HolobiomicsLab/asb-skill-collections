---
name: model-checkpoint-serialization
description: Use when after successfully training a spectrum prediction model (FFN
  encoder, GNN encoder, intensity predictor, or fragment generator) to completion
  or at intermediate milestones, and before using that model for inference on test
  sets, structural elucidation queries, or transfer learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3518
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0634
  tools:
  - PyTorch
  - TensorFlow
  - PubChem
  - ms-pred
  - spatialMETA
  - AnnData
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
- doi: 10.1038/s41467-025-63915-z
  title: ''
evidence_spans:
- _No usage/docs found._
- By inputting the chemical formula and your experimental spectrum, the WebUI will
  rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
- spatialMETA is a method for integrating spatial multi-omics data
- spatialmeta.pp.calculate_qc_metrics_sm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  - build: coll_spatialmeta_cq
    doi: 10.1038/s41467-025-63915-z
    title: SpatialMETA
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  - 10.1038/s41467-025-63915-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-checkpoint-serialization

## Summary

Save and load trained neural network model weights and hyperparameters to enable reproducible evaluation, transfer learning, and long-term archival of spectrum prediction models. This skill preserves the full state of a trained encoder or intensity predictor, allowing downstream retrieval or intensity prediction tasks to begin from a known checkpoint rather than retraining.

## When to use

After successfully training a spectrum prediction model (FFN encoder, GNN encoder, intensity predictor, or fragment generator) to completion or at intermediate milestones, and before using that model for inference on test sets, structural elucidation queries, or transfer learning. Also when distributing pretrained weights to users who lack NIST licenses or computational resources.

## When NOT to use

- Model is still actively training or validation loss is still decreasing — save only after a predefined stopping criterion (e.g., plateau in validation metric for N epochs) to avoid stale intermediate checkpoints.
- You intend to modify model architecture or retraining hyperparameters — loading a checkpoint frozen to an incompatible architecture will fail; retrain from scratch or use transfer learning with matching input/output specs.
- Checkpoint storage is extremely constrained and inference-only deployment is needed — consider quantization or model distillation before serialization.

## Inputs

- Trained PyTorch or TensorFlow model object (unfrozen weights)
- Training state dictionary (optimizer, learning rate scheduler state)
- Configuration YAML with hyperparameters and data preprocessing settings
- Validation/test metrics computed during training

## Outputs

- Serialized model checkpoint file (.pt for PyTorch, .h5 or SavedModel for TensorFlow)
- Training metadata file (JSON or YAML with epoch, loss history, seed, split info)
- Model architecture summary (for verification on load)

## How to apply

At the end of each training loop (or after validation criteria are met), use the deep learning framework's built-in checkpoint API (e.g., PyTorch's `torch.save(model.state_dict(), path)` or TensorFlow's `model.save()`) to serialize the model's learned parameters, optimizer state, and training metadata (epoch, loss, hyperparameters) to a filesystem path or cloud storage. Record the configuration YAML (learning rate, batch size, hidden layer sizes, activation functions) alongside the checkpoint. When resuming or deploying, load the checkpoint using the corresponding framework restore function and verify that architecture and data preprocessing match the saved configuration. Store checkpoints in a versioned directory structure (e.g., `ckpt/model_name/seed_N/epoch_K/`) to enable ablation studies and comparison across random seeds and scaffold splits.

## Related tools

- **PyTorch** (Deep learning framework for saving and loading model state_dict and optimizer state; used for NEIMS FFN/GNN encoders and fragment generators in ms-pred.)
- **TensorFlow** (Alternative deep learning framework with model.save() and model.load_weights() for checkpoint serialization; compatible with MassFormer and other models in ms-pred.)
- **ms-pred** (Repository providing training scripts (e.g., src/ms_pred/dag_pred/train_gen.py, train_inten.py) that implement checkpoint saving; configs/iceberg/*.yaml files specify checkpoint paths and loading logic.) — https://github.com/coleygroup/ms-pred

## Examples

```
python src/ms_pred/dag_pred/train_gen.py --config configs/iceberg/iceberg_elucidation.yaml --gen_ckpt data/ckpts/iceberg_gen_epoch50.pt
```

## Evaluation signals

- Checkpoint file exists and is non-zero size (typically >50 MB for spectrum prediction models); filesystem write succeeds without I/O errors.
- Model loads without shape mismatch or dtype errors when config YAML is applied; forward pass on a small batch (e.g., 1 molecule) executes without NaN or OOM.
- Predictions on a held-out validation set are bit-identical (or within floating-point tolerance <1e-5) before and after checkpoint round-trip, indicating faithful serialization and deserialization.
- Training resumed from checkpoint recovers the same loss trajectory and validation metrics as continuous training, confirming optimizer and random state were correctly preserved.
- When using checkpoint for retrieval or structural elucidation downstream, top-1 accuracy and hit rate metrics match reported benchmarks (e.g., 40% top-1 retrieval on NIST'20 for ICEBERG).

## Limitations

- Checkpoints are not version-controlled and can become stale if code or data preprocessing changes; store alongside git commit hash and data split seed in metadata to enable reproducibility.
- Pretrained weights require licensing agreements (e.g., NIST'20 purchase proof) when distributing publicly; the ms-pred repository requires users to email maintainers with proof of NIST license to receive ICEBERG weights.
- Large checkpoint files (tens of GB for models with millions of parameters) require adequate storage and bandwidth; MassSpecGym weights are distributed via Dropbox rather than GitHub due to size constraints.
- Checkpoint format is framework-specific (.pt vs .h5 vs SavedModel); model architecture must exactly match the saved weights; cross-framework conversion is non-trivial and not automated.

## Evidence

- [other] Save the trained model checkpoint and generate predictions on benchmark compounds for comparison with ms-pred results.: "Save the trained model checkpoint and generate predictions on benchmark compounds for comparison with ms-pred results."
- [readme] Get pretrained ICEBERG model weights. You can either train the model by yourself (following instructions below); Or if you have an NSIT'20 license (or newer), you can email the maintainer with a proof of license: "Get pretrained ICEBERG model weights. You can either train the model by yourself (following instructions below); Or if you have an NSIT'20 license (or newer), you can email the maintainer with a"
- [readme] You can download the weights trained on the MassSpecGym dataset, publicly available via Dropbox: "You can download the weights trained on the MassSpecGym dataset, publicly available via Dropbox"
- [readme] Update the configuration file based your local setting. Change python_path to your Python excutiable, and update gen_ckpt and inten_ckpt to the path of your pretrained models.: "Update the configuration file based your local setting. Change python_path to your Python excutiable, and update gen_ckpt and inten_ckpt to the path of your pretrained models."
- [other] Train the FFN encoder on the spectrum prediction task using mean squared error loss and an optimization algorithm (e.g. Adam). Evaluate the model on a held-out test set, computing prediction accuracy metrics (e.g. cosine similarity, spectral match score).: "Evaluate the model on a held-out test set, computing prediction accuracy metrics (e.g. cosine similarity, spectral match score)."
