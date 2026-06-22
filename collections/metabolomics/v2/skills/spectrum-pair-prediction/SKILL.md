---
name: spectrum-pair-prediction
description: Use when you have pairs of MS/MS spectra and need to estimate their structural similarity (Tanimoto score based on molecular fingerprints) as a proxy for compound relatedness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - matchms
  - PyTorch
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- mean squared error (MSE) loss
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
---

# Spectrum-Pair Prediction

## Summary

Predict structural similarity scores (Tanimoto) between pairs of tandem mass spectra using a Siamese neural network trained on MS/MS data. This skill generates high-dimensional spectral embeddings and compares them to estimate molecular structural relationships without computing fingerprints directly.

## When to use

Use this skill when you have pairs of MS/MS spectra and need to estimate their structural similarity (Tanimoto score based on molecular fingerprints) as a proxy for compound relatedness. Apply it when fingerprint computation is unavailable or when you want to leverage spectral features learned by a deep model trained on >100,000 annotated spectra. Trigger conditions: (1) input is binned MS/MS spectrum pairs (52+ bins per spectrum after filtering); (2) reference structural labels (InChIKey or SMILES) exist for validation; (3) you need predictions across test sets of 3,000+ spectrum pairs to achieve stable RMSE estimates.

## When NOT to use

- Spectra have not been preprocessed: remove peaks <0.1% of maximum intensity, limit to 1000 highest peaks, and bin to 52 dimensions first.
- Reference structural labels (InChIKey, SMILES, InChI) are unavailable for validation; model predictions cannot be evaluated without ground truth.
- Spectrum metadata such as parent mass or elemental formula is required for prediction; MS2DeepScore was not trained on metadata features.

## Inputs

- Pre-trained MS2DeepScore Siamese neural network model (PyTorch .pt file)
- Test set of binned MS/MS spectra (52 bins per spectrum after filtering unused bins)
- Reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for validation
- Spectrum pair indices or iterator for all unique pairs (e.g., 6.5M pairs from 3,601 spectra)

## Outputs

- Predicted Tanimoto similarity scores for all spectrum pairs (float values 0–1)
- 200-dimensional spectral embeddings for each spectrum
- Root mean squared error (RMSE) metric between predictions and reference scores
- Optional: uncertainty estimates per prediction (from Monte-Carlo Dropout sampling)

## How to apply

Load a pre-trained MS2DeepScore Siamese network and the test set of binned spectra (52 bins per spectrum, with low-intensity peaks already filtered <0.1% of max). Generate all unique spectrum pairs from the test set. Compute 200-dimensional spectral embeddings for each spectrum using the trained base network's feature extraction layers. Calculate cosine similarity between paired embeddings and convert the result to predicted Tanimoto scores using the learned scoring head. Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for ground-truth comparison. Compute root mean squared error (RMSE) between predicted and reference scores. Optionally, apply uncertainty filtering using Monte-Carlo Dropout interquartile range (IQR) thresholds to improve accuracy on high-confidence predictions (RMSE improves from ~0.15 to ~0.10 with filtering).

## Related tools

- **MS2DeepScore** (Siamese neural network model for predicting Tanimoto scores from spectrum pairs; provides base network for embedding generation and scoring) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data preparation, metadata cleaning, adduct extraction, and spectrum pair generation) — https://github.com/matchms/matchms
- **RDKit** (Compute reference Tanimoto scores from Daylight fingerprints (2048 bits) for ground-truth validation)
- **NumPy** (Compute cosine similarity between embeddings and RMSE metrics)
- **PyTorch** (Load pre-trained model and execute forward passes for embedding generation)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; import numpy as np; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); embeddings = ms2ds.get_embedding_array(cleaned_spectra); similarity_scores = np.dot(embeddings, embeddings.T); rmse = np.sqrt(np.mean((similarity_scores - reference_tanimoto)**2))
```

## Evaluation signals

- RMSE on test set is approximately 0.15 without uncertainty filtering; improves to ~0.10 with IQR-based uncertainty thresholds applied.
- Predicted Tanimoto scores fall in the valid range [0, 1] with no NaN or infinity values.
- Cosine similarity values between embeddings convert monotonically to Tanimoto scores; verify no sign flips or anomalous jumps.
- On 3,601 spectra from 500 unseen compounds, predictions maintain stable RMSE across random train–test splits (no systematic bias).
- High-confidence predictions (low uncertainty via Monte-Carlo Dropout ensemble) show lower RMSE than low-confidence predictions, indicating model calibration.

## Limitations

- Model generalizes to spectra from unseen compounds but was trained on GNPS, MoNA, MassBank, and MSnLib data; performance on novel ionization modes or untrained compound classes is unknown.
- Spectrum metadata (parent mass, elemental formula, instrument type) was not used in training; predictions rely solely on peak patterns and intensities.
- Computational cost scales quadratically with number of spectra: 6.5M unique pairs from 3,601 spectra requires significant memory for embedding storage.
- Predictions require pre-binning spectra to consistent dimensions (52 bins after filtering); incompatible with raw, unbinned peak lists.
- Model uncertainty estimates depend on Monte-Carlo Dropout sampling; very small or very large IQR thresholds may filter out valid predictions or retain unreliable ones.

## Evidence

- [other] MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions.: "MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions"
- [methods] Generate 200-dimensional spectral embeddings for each spectrum using trained base network, compute cosine similarity, convert to Tanimoto scores, and calculate RMSE vs. reference.: "compute 200-dimensional spectral embeddings for each spectrum using the trained base network. 3. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores"
- [methods] Spectrum peaks were binned into 10,000 equally-sized bins (resulting in 52 bins after filtering unused bins from training data).: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) used for structural similarity ground truth.: "we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities"
- [intro] Monte-Carlo Dropout ensembles estimate uncertainty; filtering predictions by interquartile range thresholds improves accuracy from RMSE ~0.15 to ~0.10.: "achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [intro] Siamese network trained on MS/MS spectrum pairs to predict structural similarity labels without first computing molecular fingerprints.: "a deep learning approach that is trained to predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra"
- [results] Spectrum metadata such as parent mass and elemental formula were not used during training.: "the neural network was not trained on any spectrum metadata such as parent mass and elemental formula"
- [readme] Load pre-trained model, generate all spectrum pairs, compute embeddings, calculate cosine similarity and convert to Tanimoto scores, compare against reference fingerprint scores.: "load in the ms2deepscore model ... cleaned_spectra = pipeline.spectra_queries ... ms2ds_model = MS2DeepScore(model) ... ms2ds_embeddings = ms2ds_model.get_embedding_array(cleaned_spectra)"
