---
name: dropout-regularization-application
description: Use when when training a deep neural network on mass spectrometry spectral
  data where overfitting is a risk (especially with data augmentation applied), and
  when you need both regularization during training AND uncertainty quantification
  at inference time via multiple forward passes with dropout.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2426
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - matchms
  - Python
  - TensorFlow / Keras
  - ms2deepscore
  - scikit-learn
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

# dropout-regularization-application

## Summary

Apply dropout regularization during training of a Siamese neural network to prevent overfitting and improve generalization when predicting structural similarities from MS/MS spectral pairs. Dropout probabilistically removes activations during training and is selectively applied at inference time to quantify prediction uncertainty via Monte-Carlo ensembles.

## When to use

When training a deep neural network on mass spectrometry spectral data where overfitting is a risk (especially with data augmentation applied), and when you need both regularization during training AND uncertainty quantification at inference time via multiple forward passes with dropout enabled.

## When NOT to use

- When the training dataset is very small (<10,000 spectra) and regularization would excessively discard learned signal; use L1/L2 regularization alone instead.
- When computational cost of N=10 forward passes at inference is prohibitive (e.g., real-time single-prediction scenarios); use standard deterministic inference without dropout.
- When uncertainty quantification is not needed and a single point prediction suffices; standard dropout during training is still beneficial, but Monte-Carlo inference adds overhead.

## Inputs

- Binned MS/MS spectrum vectors (9948-dimensional, square-root-transformed intensities, m/z range 10–1000 in 10,000 equally-spaced bins)
- Pairs of spectra with corresponding Tanimoto structural similarity labels (0.0–1.0)
- Training configuration: dropout rate, number of Monte-Carlo samples, IQR threshold for filtering

## Outputs

- Trained base network with dropout layers regularizing the hidden dense layers
- 200-dimensional spectral embeddings for each spectrum
- Prediction uncertainty estimates (interquartile range of Monte-Carlo ensemble predictions)
- Filtered similarity scores with outliers removed above specified IQR threshold

## How to apply

Apply dropout with rate 0.2 after each hidden dense layer (500 nodes) in the base network, but NOT after the final output layer (200-dimensional embedding). During training, dropout probabilistically sets activations to zero to prevent co-adaptation of neurons. At inference time, enable dropout on all but the first layer and perform N=10 forward passes (Monte-Carlo Dropout) to generate an ensemble of embeddings, computing the interquartile range (IQR) as an uncertainty estimate. Filter predictions with IQR values above task-specific thresholds to reduce outlier predictions. This dual use—regularization during training and uncertainty quantification during inference—enables both better generalization and calibrated confidence scores.

## Related tools

- **TensorFlow / Keras** (Neural network framework providing Dropout layer implementation and training loop)
- **matchms** (Spectrum preprocessing, metadata cleaning, and data pipeline management for MS/MS spectra) — https://github.com/matchms/matchms
- **ms2deepscore** (Reference implementation of Siamese network with dropout and Monte-Carlo Dropout for MS/MS similarity prediction) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (Dimensionality reduction (t-SNE) for visualizing regularized spectral embeddings)

## Examples

```
from ms2deepscore.models import MS2DeepScore; from ms2deepscore import MS2DeepScore; ms2ds_model = MS2DeepScore(model); embeddings = ms2ds_model.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Training loss decreases monotonically and validation loss converges without sharp divergence, indicating dropout is reducing overfitting without suppressing learning.
- Root mean squared error (RMSE) on held-out test set for Tanimoto score predictions is ≤ 0.15 without uncertainty filtering and ≤ 0.10 with IQR-based filtering, matching reported performance.
- Monte-Carlo ensemble predictions show reasonable IQR values (e.g., median IQR < 0.1) for high-confidence predictions and elevated IQR for low-confidence or borderline similarity predictions.
- After filtering predictions with IQR above threshold, precision and recall curves show improved ranking of true high-similarity pairs (Tanimoto > 0.7) without massive reduction in dataset size.
- Spectral embeddings visualized via t-SNE show distinct clustering by structural similarity class, with intra-class variance minimized and inter-class separation maximized.

## Limitations

- Dropout rate (0.2) and Monte-Carlo sample size (N=10) are fixed hyperparameters; optimal values may vary for datasets with different spectrum counts, diversity, or augmentation intensity.
- IQR-based uncertainty filtering requires manual threshold selection per task; no principled method for choosing the threshold is provided, and overly stringent filtering discards valid predictions.
- Monte-Carlo Dropout assumes dropout distribution is representative of posterior uncertainty, which may not hold for highly imbalanced similarity labels or out-of-distribution spectra.
- Computational cost of N=10 forward passes during inference scales linearly with spectrum count; inference is not real-time for very large spectral libraries.
- No explicit guidance on when dropout should be disabled (e.g., for inference on highly similar spectra to existing training data where uncertainty is low).

## Evidence

- [methods] Apply dropout with rate 0.2 after each hidden layer during training; omit dropout after final embedding layer.: "Apply dropout with rate 0.2 to regularize the layer. 5. Pass through the second dense layer (500 nodes) followed by batch normalization and dropout (0.2). 6. Pass through the final dense layer (200"
- [methods] Enable dropout at inference time for uncertainty quantification via multiple forward passes.: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [results] Filter predictions using interquartile range thresholds to remove uncertain predictions and improve performance.: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [intro] Dropout achieves root mean squared error of about 0.15 without filtering and down to 0.1 with stricter uncertainty restrictions.: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [abstract] Dropout enables both regularization during training and Monte-Carlo uncertainty quantification.: "different model varieties through Monte-Carlo Dropout is u"
- [readme] README implementation example showing dropout applied during model training in the default configuration.: "The settings below use default training settings and use precursor mz and ionmode as additional metadata input."
