---
name: dense-neural-network-layer-construction
description: Use when when you have a binned MS/MS spectrum vector (e.g., 9948-dimensional
  input from 10,000 equally-spaced m/z bins in the 10–1000 Da range) and need to compress
  it into a learned latent representation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3379
  tools:
  - matchms
  - Python
  - TensorFlow / Keras
  - Adam optimizer
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dense-neural-network-layer-construction

## Summary

Construct sequential dense layers with regularization, batch normalization, and dropout to build a neural network base encoder that transforms high-dimensional binned MS/MS spectra into lower-dimensional embeddings. This skill is essential for building the embedding pipeline of Siamese networks in spectral similarity learning.

## When to use

When you have a binned MS/MS spectrum vector (e.g., 9948-dimensional input from 10,000 equally-spaced m/z bins in the 10–1000 Da range) and need to compress it into a learned latent representation (e.g., 200-dimensional embedding) while controlling overfitting on a moderately-sized training set (>100,000 spectra). Apply this skill before pairing the base network with a Siamese loss function or when you need intermediate spectral embeddings for clustering or visualization.

## When NOT to use

- Input spectrum is already a pre-computed molecular fingerprint or explicit feature vector (use this skill only on raw binned spectra or augmented variants thereof).
- Embedding dimension is smaller than 50 or larger than input dimensionality; the 200-node embedding size is tuned for this specific 9948 → 200 compression ratio.
- Dataset is smaller than ~50,000 annotated spectra; dropout(0.2) and L1/L2(10⁻⁶) may be insufficient regularization or introduce excessive bias on tiny datasets.

## Inputs

- binned MS/MS spectrum vector (9948-dimensional, square-root-transformed intensities, m/z range 10–1000 Da binned into 10,000 equally-sized bins)

## Outputs

- 200-dimensional spectral embedding vector
- trained dense network base model (component for Siamese architecture)

## How to apply

Construct a sequential dense network by stacking layers with the following pattern: input layer → dense(500 nodes) + L1/L2 regularization (10⁻⁶ each) → batch normalization → dropout(0.2) → dense(500 nodes) + batch normalization → dropout(0.2) → dense(200 nodes, no normalization/dropout). The first two hidden layers use 500 nodes with identical regularization and dropout to prevent overfitting on the large but finite GNPS training corpus; the final layer has 200 nodes without post-activation regularization because embeddings require interpretable magnitude variance. Use batch normalization after dense layers (except the final embedding layer) to stabilize training and accelerate convergence. Apply dropout(0.2) after each intermediate hidden layer to reduce co-adaptation of neurons. The L1/L2 regularization strength (10⁻⁶) is a conservative choice that penalizes large weights without inducing sparsity, suitable for dense layers. Return the 200-dimensional output as the final spectral embedding.

## Related tools

- **TensorFlow / Keras** (Deep learning framework for implementing dense layers, batch normalization, dropout, and L1/L2 regularization)
- **matchms** (MS/MS spectrum loading, cleaning, and binning into the 10,000 m/z bins required as input to the dense network) — https://github.com/matchms/matchms
- **Adam optimizer** (Gradient descent optimizer for training the dense layer weights to minimize MSE loss on structural similarity labels)

## Examples

```
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout; from tensorflow.keras import Sequential; model = Sequential([Dense(500, activation='relu', kernel_regularizer=L1L2(l1=1e-6, l2=1e-6), input_shape=(9948,)), BatchNormalization(), Dropout(0.2), Dense(500, activation='relu', kernel_regularizer=L1L2(l1=1e-6, l2=1e-6)), BatchNormalization(), Dropout(0.2), Dense(200)]); embedding = model(binned_spectrum_vector)
```

## Evaluation signals

- Output embedding has exactly 200 dimensions and dtype float32/float64; check shape(embedding) == (batch_size, 200).
- Training loss (MSE on Tanimoto score prediction) converges smoothly without divergence; expect RMSE ≈ 0.13–0.2 on validation set for Tanimoto scores in range [0.1, 0.9].
- Batch normalization statistics (running mean/variance) are tracked and updated during training; verify that per-layer batch norm has non-zero learnable scale/shift parameters.
- Dropout is disabled during inference; embeddings from the same spectrum should be deterministic (not stochastic), unlike embeddings during training.
- Regularization penalty (L1 + L2 loss term) decreases weight magnitudes in the first two dense layers without collapsing them to zero; inspect weight histograms to confirm no dead neurons.

## Limitations

- The 200-dimensional embedding size was optimized for the MS2DeepScore Siamese architecture and may not be optimal for other downstream tasks (e.g., direct clustering may perform better with 50–100 dimensions).
- Dropout(0.2) assumes batch size is sufficiently large (≥32); smaller batches may cause poor batch norm statistics and instability.
- The network is sensitive to input peak intensity preprocessing (square-root transformation); if raw intensities or other transformations are used, the learned weights will not transfer.
- No internal mechanism to detect or handle sparse spectra (very few non-zero m/z bins); very sparse inputs may result in near-zero embeddings and poor gradient flow.
- L1/L2 regularization at 10⁻⁶ is weak and assumes large training datasets (>100,000 spectra); on smaller datasets, stronger regularization (10⁻⁴ to 10⁻³) may be necessary to avoid overfitting.

## Evidence

- [other] The base network accepts a binned spectrum (peaks binned into 10,000 equally-sized m/z bins from 10 to 1000) as input and produces a 200-dimensional spectral embedding vector through dense neural network layers.: "The base network accepts a binned spectrum (peaks binned into 10,000 equally-sized m/z bins from 10 to 1000) as input and produces a 200-dimensional spectral embedding vector through dense neural"
- [other] Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities). Pass the input vector through the first dense layer (500 nodes) with L1 (10⁻⁶) and L2 (10⁻⁶) regularization applied. Apply batch normalization after the first dense layer. Apply dropout with rate 0.2 to regularize the layer. Pass through the second dense layer (500 nodes) followed by batch normalization and dropout (0.2). Pass through the final dense layer (200 nodes) to produce the spectral embedding without batch normalization or dropout.: "Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities). Pass the input vector through the"
- [methods] Models were trained with the Adam optimizer [44, 45] that optimized the mean squared error (MSE) loss: "Models were trained with the Adam optimizer that optimized the mean squared error (MSE) loss"
- [other] Data augmentation is applied during training, including low-intensity peak removal (0–20% of bins below 0.4 intensity), peak intensity jitter (0–40% changes), and new peak addition (0–10 random bins with values 0–0.01).: "Data augmentation is applied during training, including low-intensity peak removal (0–20% of bins below 0.4 intensity), peak intensity jitter (0–40% changes), and new peak addition (0–10 random bins"
- [results] MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2: "MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2"
- [readme] the MS2deepscore_model.pt is needed. The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model.: "The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model."
