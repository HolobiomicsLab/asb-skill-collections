---
name: model-artifact-persistence
description: Use when after a deep neural network model has completed training on
  LC-MS spectral peak classification data and you need to preserve the learned weights
  and architecture for downstream inference, validation on held-out test sets, or
  sharing with collaborators.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - TensorFlow
  - Keras
  - EDML_deep_learning2.py
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b02983
  title: DNN peak classifier
- doi: 10.25345/C5FD2F
  title: ''
evidence_spans:
- Deep Neural Networks for Classification of LC-MS Spectral Peaks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dnn_peak_classifier_cq
    doi: 10.1021/acs.analchem.9b02983
    title: DNN peak classifier
  dedup_kept_from: coll_dnn_peak_classifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02983
  all_source_dois:
  - 10.1021/acs.analchem.9b02983
  - 10.25345/C5FD2F
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-artifact-persistence

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Save trained deep neural network model weights and architecture to disk after training completion, ensuring reproducibility and enabling future inference without retraining. This skill is essential for capturing the learned state of a DNN classifier so it can be retrieved and applied to new LC-MS spectral peak data.

## When to use

After a deep neural network model has completed training on LC-MS spectral peak classification data and you need to preserve the learned weights and architecture for downstream inference, validation on held-out test sets, or sharing with collaborators. Apply this skill immediately upon successful training completion to avoid loss of the learned model state.

## When NOT to use

- When the model is still undergoing active training or hyperparameter tuning—save only after convergence or final validation.
- When model artifacts are already stored in a version control system or artifact repository with automated backup (redundant persistence may be inefficient).
- When the training run is exploratory and the model is discarded; only apply this skill to models intended for reuse or publication.

## Inputs

- trained TensorFlow/Keras model object (in-memory after EDML_deep_learning2.py execution)
- model architecture definition
- optimized model weights from training

## Outputs

- model artifact file (serialized weights and architecture)
- persisted neural network model suitable for inference or transfer learning

## How to apply

Upon completion of EDML_deep_learning2.py training, use the training script's built-in model serialization functionality to write both the trained model weights and the neural network architecture definition to a model artifact file. The artifact should contain sufficient information to reconstruct the network topology and load the learned parameters without requiring access to the original training data or retraining. Verify that the artifact file has been written to disk and can be loaded back into memory to confirm persistence was successful. Store the artifact in a version-controlled or well-documented location alongside metadata documenting the training dataset version, hyperparameters, and training date.

## Related tools

- **TensorFlow** (deep learning framework providing model serialization methods (e.g., SavedModel, HDF5) for persisting trained DNN weights and architecture)
- **Keras** (high-level API within TensorFlow used to define and train the neural network model; provides save() method for artifact persistence)
- **EDML_deep_learning2.py** (training script that produces the trained model object; should include or be augmented with serialization code to save weights and architecture upon completion) — https://github.com/JainLab/Manuscript-DNNs-for-Classification-of-LCMS-Peaks

## Examples

```
model.save('trained_lcms_peak_classifier.h5')
```

## Evaluation signals

- Model artifact file exists on disk at the specified path and has a file size consistent with the number of trainable parameters in the network.
- Artifact can be successfully deserialized and loaded back into memory without errors; model object properties (layer counts, parameter counts, input/output shapes) match the original trained model.
- Inference on a held-out test set using the loaded model produces identical predictions to inference on the original trained model before persistence, confirming no data loss during serialization.
- Metadata or version information accompanying the artifact clearly documents the training dataset version (DOI 10.25345/C5FD2F), training script version, and timestamp of training completion.
- Artifact is reproducible: training the model again from the same dataset and hyperparameters (with fixed random seed) and persisting yields an artifact that passes inference equivalence checks.

## Limitations

- Serialized model artifacts may not be forward-compatible if TensorFlow or Keras versions are significantly upgraded; document the framework version used during training.
- Artifact file size can be substantial for large DNNs (gigabytes), requiring adequate storage and backup infrastructure.
- No explicit workflow metadata (e.g., training hyperparameters, learning curves, validation metrics) is captured by standard model serialization; practitioners should separately log training configuration and evaluation results.
- The README and article do not specify the exact model artifact format (e.g., SavedModel, .h5, .pb); implementation details must be inferred from EDML_deep_learning2.py source code.

## Evidence

- [other] Save the trained model weights and architecture to a model artifact file upon completion of training.: "Save the trained model weights and architecture to a model artifact file upon completion of training."
- [readme] Then use the script EDML_deep_learning2.py to train the deep neural network model from scratch on peak classification.: "Then use the script EDML_deep_learning2.py"
- [other] Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets.: "then executing the EDML_deep_learning2.py script on those datasets"
