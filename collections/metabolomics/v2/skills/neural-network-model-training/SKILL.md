---
name: neural-network-model-training
description: Use when you have downloaded LC-MS spectral peak data (DOI 10.25345/C5FD2F or equivalent) and need to build a supervised deep neural network classifier to distinguish peak classes in mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3315
  tools:
  - TensorFlow
  - Keras
  - EDML_deep_learning2.py
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-model-training

## Summary

Train a deep neural network from scratch on LC-MS spectral peak classification data using TensorFlow/Keras. This skill converts raw LC-MS peak datasets into a trained classifier model suitable for automated spectral annotation.

## When to use

You have downloaded LC-MS spectral peak data (DOI 10.25345/C5FD2F or equivalent) and need to build a supervised deep neural network classifier to distinguish peak classes in mass spectrometry data. Use this skill when you have raw LC-MS peak records and want to train a model end-to-end rather than using a pre-trained checkpoint.

## When NOT to use

- You already have a pre-trained model checkpoint and only need to apply it to new spectra (use inference instead)
- Your LC-MS data is not in the expected peak classification format or lacks ground-truth labels
- You need to understand model interpretability or extract feature importance; this skill produces a black-box classifier

## Inputs

- LC-MS peaks dataset (DOI 10.25345/C5FD2F format)
- EDML_deep_learning2.py script
- TensorFlow/Keras environment

## Outputs

- Trained deep neural network model weights
- Model architecture definition
- Model artifact file (saved model)

## How to apply

Begin by loading the LC-MS peak dataset from the repository using the data loading utilities provided in the EDML_deep_learning2.py script. Initialize and train the deep neural network model on the loaded peak classification task using TensorFlow and Keras, which handle automatic differentiation, gradient descent, and layer composition. During training, the model learns to map LC-MS spectral features to peak class labels. Upon convergence, serialize the trained model weights and architecture to a persistent artifact file (typically HDF5 or SavedModel format) for later inference. Monitor training loss and validation metrics to confirm the model is learning; save the best checkpoint based on validation performance to avoid overfitting.

## Related tools

- **TensorFlow** (Deep learning framework providing automatic differentiation, optimizers, and neural network layer abstractions for model training)
- **Keras** (High-level API for defining, compiling, and training sequential and functional neural network architectures)
- **EDML_deep_learning2.py** (Project-specific training script that orchestrates data loading, model initialization, and training loop execution) — https://github.com/JainLab/Manuscript-DNNs-for-Classification-of-LCMS-Peaks

## Examples

```
python EDML_deep_learning2.py --dataset /path/to/downloaded/peaks/10.25345/C5FD2F --epochs 100 --batch_size 32 --output_model ./trained_dnn_model.h5
```

## Evaluation signals

- Training loss decreases monotonically or exhibits expected convergence pattern over epochs
- Validation loss plateaus or improves, indicating the model generalizes to unseen peak data
- Model artifact file is created and is readable (can be loaded back into TensorFlow/Keras without errors)
- Trained model produces probability distributions over peak classes that sum to 1.0 and respect expected class balance in held-out test set
- Model weights show non-trivial variation (not all near zero or saturated), confirming learning has occurred

## Limitations

- Requires the specific LC-MS peak dataset from DOI 10.25345/C5FD2F; transfer learning to other MS platforms or ionization methods is not addressed in the source material
- No changelog or discussion of failure modes, hyperparameter sensitivity, or robustness to data drift is available in the README
- Training time and computational requirements (GPU/CPU, memory) are not specified; users must provision infrastructure independently
- The skill assumes the provided EDML_deep_learning2.py script is fully functional and correctly implements the model architecture described in the manuscript

## Evidence

- [readme] For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py.: "For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py."
- [other] Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets.: "Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on"
- [other] Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py. Execute EDML_deep_learning2.py to initialize and train the deep neural network model from scratch on the peak classification task.: "Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py. Execute EDML_deep_learning2.py to initialize and train the"
- [other] Save the trained model weights and architecture to a model artifact file upon completion of training.: "Save the trained model weights and architecture to a model artifact file upon completion of training."
- [intro] Deep neural networks can be applied to classification of LC-MS spectral peaks: "Deep neural networks can be applied to classification of LC-MS spectral peaks"
