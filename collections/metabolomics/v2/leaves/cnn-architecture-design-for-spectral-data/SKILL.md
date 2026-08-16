---
name: cnn-architecture-design-for-spectral-data
description: Use when when you have mass-spectrometry data (m/z and intensity pairs
  or spectral matrices) paired with ground-truth molecular fingerprints or InChIKeys,
  and you need to learn a non-linear mapping from spectral patterns to structural
  fingerprints for downstream metabolite ranking or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - TensorFlow
  - PyTorch
  - scikit-learn
  - PyFingerprint
  - PubChemPy
  - Open Babel
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-020-01726-7
  title: MetFID
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfid_cq
    doi: 10.1007/s11306-020-01726-7
    title: MetFID
  dedup_kept_from: coll_metfid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01726-7
  all_source_dois:
  - 10.1007/s11306-020-01726-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CNN Architecture Design for Spectral Data

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and implement a convolutional neural network (CNN) to map mass-spectrometry spectral features (m/z and intensity arrays) to molecular fingerprint vector outputs for metabolite annotation. This skill bridges raw MS data preprocessing and learned compound prediction by architecting convolutional, pooling, and dense layers tailored to spectral input dimensionality and fingerprint prediction tasks.

## When to use

When you have mass-spectrometry data (m/z and intensity pairs or spectral matrices) paired with ground-truth molecular fingerprints or InChIKeys, and you need to learn a non-linear mapping from spectral patterns to structural fingerprints for downstream metabolite ranking or annotation. This is appropriate when fingerprint prediction scores will directly rank candidate compounds by Tanimoto similarity.

## When NOT to use

- Input spectra lack paired ground-truth fingerprints or molecular identities; use unsupervised or semi-supervised methods instead.
- Spectral data are already encoded as high-level statistical features (e.g., principal components or manually extracted fragment counts); CNN requires raw or minimally preprocessed m/z–intensity pairs to learn hierarchical patterns.
- Inference speed or model size is critical and a CNN would be prohibitively expensive; consider lightweight linear models or lookup tables instead.

## Inputs

- Mass-spectrometry spectral data: m/z and intensity pairs (precursor mass, ionization mode, fragment m/z and normalized intensity values)
- Molecular fingerprints or InChIKeys paired with spectra for supervised training
- Training/validation/test split metadata

## Outputs

- Trained CNN model weights and architecture (e.g., .h5 format)
- Fingerprint vector predictions (continuous or binary) for query spectra
- Model performance metrics (validation loss, test-set accuracy or Tanimoto similarity distribution)

## How to apply

Load MS input data as m/z and intensity arrays or spectral matrices compatible with CNN input layers. Design the CNN architecture with sequential convolutional blocks (extracting local spectral motifs), pooling layers (downsampling and aggregating), and dense layers to map learned features to fingerprint vector outputs—typically binary or continuous bits per dimension. Split labeled data into training, validation, and held-out test sets. Train using a loss function suited to fingerprint representation (binary cross-entropy for bit-level predictions or Tanimoto-based loss for similarity-optimized learning) with TensorFlow or PyTorch. Monitor validation performance across epochs to detect overfitting. Evaluate the trained model on the test set and save trained weights and architecture for reuse.

## Related tools

- **TensorFlow** (Deep learning framework for building, training, and saving CNN architectures and weights) — https://www.tensorflow.org/
- **PyTorch** (Alternative deep learning framework for CNN design and training with dynamic computation graphs)
- **PyFingerprint** (Generates molecular fingerprint representations from chemical structures or InChIKeys for training labels) — https://github.com/hcji/PyFingerprint
- **PubChemPy** (Retrieves molecular and fingerprint data from PubChem to augment or validate training labels) — https://pubchempy.readthedocs.io/en/latest/guide/install.html
- **scikit-learn** (Provides data splitting (train/test), preprocessing utilities, and evaluation metrics)
- **Open Babel** (Converts between chemical file formats (InChI, SMILES, etc.) and generates fingerprints) — https://openbabel.org/wiki/Python

## Examples

```
# Load and train CNN on MS–fingerprint pairs; evaluate on test set
import tensorflow as tf; from tensorflow.keras import layers; X_train, X_test = load_spectral_data(); model = tf.keras.Sequential([layers.Conv1D(64, 3, activation='relu', input_shape=(None, 1)), layers.MaxPooling1D(2), layers.Dense(128, activation='relu'), layers.Dense(2048, activation='sigmoid')]); model.compile(loss='binary_crossentropy', optimizer='adam'); model.fit(X_train, y_train, validation_split=0.2, epochs=50); test_loss, test_acc = model.evaluate(X_test, y_test); model.save('metfid_cnn.h5')
```

## Evaluation signals

- Validation loss converges and test-set Tanimoto similarity scores exceed a minimum threshold (e.g., > 0.5) for known compounds, indicating the CNN has learned spectral-to-fingerprint mappings.
- Model predictions rank the true compound (ground-truth InChIKey) first or in the top-k candidates (k = 1, 3, or 5) when scored against candidate InChIKey lists with known fingerprints.
- Output fingerprint vectors have the expected dimensionality (bit-length) and value range (binary {0, 1} or continuous [0, 1]) matching training labels.
- Model reproducibility: saved weights and architecture can be reloaded and produce identical predictions on held-out test spectra.
- No systematic bias in Tanimoto scores across precursor mass ranges or ionization modes; score distributions are stable within expected bounds.

## Limitations

- CNN performance depends on training data size and diversity; limited labeled MS–fingerprint pairs may lead to overfitting or poor generalization to novel spectra.
- The choice of loss function (binary cross-entropy vs. Tanimoto-based loss) and architecture hyperparameters (layer counts, kernel sizes, pooling strategy) is not automatically determined; careful validation and ablation are needed.
- Fingerprint predictions are probabilistic estimates and may not reflect all structural isomers or stereochemistry; ranking by Tanimoto similarity alone cannot distinguish compounds with highly similar fingerprints.
- Input MS data must be normalized (intensity scaling, spectral alignment) and formatted consistently (m/z precision, missing fragment handling) before training; preprocessing mismatches between training and inference can degrade performance.

## Evidence

- [other] MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation.: "MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation."
- [other] Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer. Design a CNN architecture with appropriate convolutional, pooling, and dense layers to map spectral features to fingerprint vector outputs.: "Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer. Design a CNN architecture with appropriate"
- [other] Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance.: "Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance."
- [readme] The first column represents the `InChIKeys`, and the second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score.: "The second column represents the `Tanimoto similarity score`. Each table will be ranked in a descending order by score."
- [readme] The first row represents the precursor mass and ionization mode, followed by intensity pairs.: "The first row represents the precursor mass and ionization mode, followed by intensity pairs."
