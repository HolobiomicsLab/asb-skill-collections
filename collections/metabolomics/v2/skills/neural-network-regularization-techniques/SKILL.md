---
name: neural-network-regularization-techniques
description: Use when when training a deep neural network on paired MS/MS spectra
  to predict structural similarity scores, especially when the training dataset is
  moderate-sized (109,734 spectra across 15,062 molecules) and overfitting risk is
  high.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - Python
  - TensorFlow / Keras
  - Adam optimizer
  - ms2deepscore
  techniques:
  - LC-MS
  license_tier: restricted
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

# Neural Network Regularization Techniques

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Application of L1/L2 regularization, batch normalization, and dropout to constrain neural network learning and reduce overfitting when training deep embeddings on spectral data. These techniques improve generalization by penalizing large weights, normalizing activations, and stochastically masking units during training.

## When to use

When training a deep neural network on paired MS/MS spectra to predict structural similarity scores, especially when the training dataset is moderate-sized (109,734 spectra across 15,062 molecules) and overfitting risk is high. Apply these techniques to the base network layers that convert binned spectra into low-dimensional embeddings.

## When NOT to use

- Input spectra are not binned into fixed m/z bins; use spectrum-specific preprocessing first.
- Training dataset is very small (<10,000 spectra); regularization strength may need tuning to avoid underfitting.
- Final output layer requires probabilistic uncertainty estimates; do not apply dropout to the embedding layer itself, only to earlier dense layers.

## Inputs

- Binned MS/MS spectrum vector (9948-dimensional, m/z range 10–1000, square-root-transformed intensities)
- Training dataset of spectrum pairs with structural similarity labels (Tanimoto scores)

## Outputs

- 200-dimensional spectral embedding vector
- Trained base network weights and biases
- Model prediction errors (RMSE) on validation/test sets

## How to apply

Implement three complementary regularization strategies in sequence on the dense layers of the base network: (1) Apply L1 (10⁻⁶) and L2 (10⁻⁶) regularization coefficients to the first and second dense layers (500 nodes each) to penalize large weight magnitudes; (2) Insert batch normalization immediately after each regularized dense layer to normalize activations and stabilize training; (3) Apply dropout with rate 0.2 after batch normalization on intermediate layers (but not the final 200-dimensional embedding layer) to randomly deactivate 20% of units during training, forcing the network to learn redundant representations. The rationale is that L1/L2 control weight magnitude, batch norm reduces internal covariate shift, and dropout creates an implicit ensemble that improves generalization on held-out test spectra.

## Related tools

- **TensorFlow / Keras** (Neural network framework for implementing dense layers, batch normalization, and dropout regularization)
- **Adam optimizer** (Gradient-based optimizer for training the regularized network to minimize mean squared error loss)
- **matchms** (Preprocessing and cleaning MS/MS spectra before binning and input to regularized network) — https://github.com/matchms/matchms
- **ms2deepscore** (Complete implementation of the Siamese network with all regularization techniques applied) — https://github.com/matchms/ms2deepscore

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Root mean squared error (RMSE) on validation and test sets should be ≤0.15 when predicting Tanimoto scores in the 0.1–0.9 range (indicates effective regularization prevents overfitting).
- Training loss should decrease smoothly without divergence; validation loss should remain stable or improve, not degrade (batch norm and dropout stabilize convergence).
- Dropout and L1/L2 coefficients should reduce model uncertainty (interquartile range of Monte-Carlo Dropout predictions) to acceptable thresholds without sacrificing predictive accuracy.
- Inspect final embedding layer outputs: they should cluster spectra of similar structure (same InChIKey) close together in 200-dimensional space when visualized with t-SNE.
- Ablation test: removing any one regularization component (e.g., dropout) should increase test RMSE or validation loss, confirming each component contributes to generalization.

## Limitations

- Regularization strength (L1/L2 coefficients 10⁻⁶, dropout rate 0.2) were tuned on one dataset (GNPS) and may require retuning for spectra from other sources or instrument types.
- Batch normalization assumes mini-batches are representative of the data distribution; very small batch sizes may degrade its effectiveness.
- Dropout introduces stochasticity during training but requires multiple forward passes (N=10) at inference time for uncertainty estimation, increasing computational cost.
- Final embedding layer (200 nodes) has no regularization; if overfitting occurs specifically in the embedding space, additional constraints may be needed.
- Article does not report sensitivity analysis on regularization hyperparameters (e.g., effect of varying L1/L2 or dropout rate), limiting guidance for practitioners on different datasets.

## Evidence

- [other] L1 (10⁻⁶) and L2 (10⁻⁶) regularization applied: "Pass the input vector through the first dense layer (500 nodes) with L1 (10⁻⁶) and L2 (10⁻⁶) regularization applied."
- [other] Batch normalization after dense layers: "Apply batch normalization after the first dense layer. Apply dropout with rate 0.2 to regularize the layer."
- [other] Dropout rate 0.2 on intermediate layers: "Apply dropout with rate 0.2 to regularize the layer. Pass through the second dense layer (500 nodes) followed by batch normalization and dropout (0.2)."
- [other] No regularization on final embedding layer: "Pass through the final dense layer (200 nodes) to produce the spectral embedding without batch normalization or dropout."
- [methods] Data augmentation applied during training: "we applied three forms of data augmentation on the binned spectra. (1) low-intensity peak removal, (2) peak intensity jitter, (3) new peak addition. Data augmentation was applied for every training"
- [results] RMSE achievement on test set: "MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2"
- [methods] Training with Adam optimizer and MSE loss: "Models were trained with the Adam optimizer [44, 45] that optimized the mean squared error (MSE) loss"
- [intro] Siamese network architecture with base network: "we present MS2DeepScore, a deep learning approach that is trained to predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra"
- [methods] Monte-Carlo Dropout for uncertainty: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [results] Training set size and molecule diversity: "training data set contains chemical structure annotations for 109,734 spectra... The dataset contains 15,062 different molecules"
- [other] Binning specification for spectral preprocessing: "Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities)."
- [readme] Architecture overview and regularization strategy: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum."
