---
name: siamese-network-inference-spectrum-pairs
description: Use when you have a collection of preprocessed tandem mass spectra (binned into 10,000 equally-sized m/z bins, intensities square-root transformed, top 1,000 peaks retained), a trained MS2DeepScore Siamese model, and you need to predict structural similarity scores (Tanimoto or Dice) for all or a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Siamese Network Inference on Spectrum Pairs

## Summary

Apply a trained Siamese neural network to compute predicted structural similarity scores (Tanimoto or Dice) between pairs of preprocessed tandem mass spectra by computing cosine similarity between paired 200-dimensional embeddings. This skill enables rapid prediction of molecular structural resemblance directly from MS/MS data without explicit fingerprint computation.

## When to use

You have a collection of preprocessed tandem mass spectra (binned into 10,000 equally-sized m/z bins, intensities square-root transformed, top 1,000 peaks retained), a trained MS2DeepScore Siamese model, and you need to predict structural similarity scores (Tanimoto or Dice) for all or a subset of unique spectrum pairs. Use this skill when batch inference on thousands of spectrum pairs is required and you want predictions to be fast and scalable.

## When NOT to use

- Spectra have not been preprocessed (not binned into 10,000 m/z bins, intensities not square-root transformed, or more than 1,000 peaks retained) — preprocessing is a prerequisite.
- You need to train a new model on your own dataset rather than apply an existing trained model — use the training workflow instead.
- Input spectra are from ionization modes or m/z ranges substantially different from the model's training distribution (e.g., negative mode if model trained exclusively on positive mode), as prediction accuracy may degrade outside the model's learned chemical space.

## Inputs

- Preprocessed tandem mass spectra (10,000-bin vectors with square-root-transformed intensities, m/z range 10–1000)
- Trained Siamese neural network model weights and architecture
- Spectrum pair indices (unique pairs for which similarity scores are desired)
- Ground-truth structural similarity labels (optional, for validation): Tanimoto or Dice scores computed from RDKit Daylight fingerprints

## Outputs

- Predicted structural similarity scores (Tanimoto or Dice) for all spectrum pairs
- 200-dimensional spectral embeddings for each unique spectrum
- Prediction uncertainty estimates (IQR) when Monte-Carlo Dropout is applied
- Filtered similarity score matrix (optionally restricted to low-uncertainty predictions)
- Root mean squared error (RMSE) metric comparing predictions to ground-truth labels

## How to apply

Load the pre-trained Siamese network model (with base network architecture: 200-dimensional embedding layer, 2×500-node hidden layers, L1/L2 regularization, batch normalization, dropout rate 0.2) and pass preprocessed spectrum pairs through the model to compute 200-dimensional embeddings for each spectrum in the pair. Compute cosine similarity between paired embeddings to yield predicted structural similarity scores. For uncertainty quantification, optionally apply Monte-Carlo Dropout by running N=10 forward passes with dropout enabled on all but the first layer, compute the interquartile range (IQR) of predictions, and filter predictions to retain only pairs with IQR below a threshold (e.g., IQR < 0.025 to remove high-uncertainty predictions). Calculate root mean squared error (RMSE) between predicted and ground-truth scores on the full or filtered subset.

## Related tools

- **MS2DeepScore** (Provides the trained Siamese network model and inference engine for computing spectral embeddings and similarity scores) — https://github.com/matchms/ms2deepscore
- **matchms** (Provides spectrum data structures, preprocessing utilities, and pipeline infrastructure for loading and filtering spectra) — https://github.com/matchms/matchms
- **RDKit** (Used to compute ground-truth Tanimoto scores from Daylight fingerprints for model validation)
- **Python** (Runtime environment for executing Siamese network inference and Monte-Carlo Dropout uncertainty quantification)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
similarity_scores = ms2ds.pair(spectrum_1, spectrum_2)
```

## Evaluation signals

- RMSE between predicted and ground-truth Tanimoto scores falls within expected range (~0.15 without filtering, ~0.10 with IQR < 0.025 filtering) on a held-out test set
- Predicted similarity scores lie within the valid range [0, 1] for Tanimoto/Dice scores; no NaN or infinite values
- Cosine similarity computations are numerically stable; embedding vectors have expected L2 norms and dimensionality (200)
- Monte-Carlo Dropout IQR estimates show decreasing variance with increasing model confidence; low-IQR predictions cluster away from boundary scores (0 and 1)
- Spectrum pair ordering and batch processing produce identical results regardless of execution order (reproducibility check)

## Limitations

- Model accuracy (RMSE ~0.13–0.20) is limited to predicting Tanimoto scores between 0.1 and 0.9; predictions for very low or very high structural similarity may be less reliable.
- The model was trained on GNPS spectra (109,734 spectra, 15,062 unique molecules); generalization to spectra from other sources (e.g., proprietary databases, novel compound classes) is not guaranteed.
- Inference requires spectra to be preprocessed identically to training (10,000-bin vectors, square-root-transformed intensities, top 1,000 peaks); deviations in preprocessing can degrade prediction accuracy.
- Monte-Carlo Dropout uncertainty estimates (N=10 forward passes) may be unreliable for rare or out-of-distribution spectrum types; computational cost scales linearly with the number of forward passes.
- The skill does not detect or flag failure modes (e.g., spectra with missing metadata, anomalous m/z distributions, or ionization mode mismatches that could cause silently degraded predictions).

## Evidence

- [other] Perform Siamese network inference on all unique spectrum pairs (n=6,485,401), computing cosine similarity between paired 200-dimensional embeddings to yield predicted Tanimoto scores.: "Perform Siamese network inference on all unique spectrum pairs (n=6,485,401), computing cosine similarity between paired 200-dimensional embeddings to yield predicted Tanimoto scores."
- [other] MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds to remove high-uncertainty predictions.: "MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR <"
- [methods] a base network (Fig. 1) which generates 200-dimensional embeddings for each spectrum: "a base network (Fig. 1) which generates 200-dimensional embeddings for each spectrum"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [readme] To compute the similarities between spectra of your choice you can run the code below.: "To compute the similarities between spectra of your choice you can run the code below."
- [results] MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2: "MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2"
