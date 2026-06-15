---
name: spectral-similarity-prediction-neural-networks
description: Use when when you have paired MS/MS spectra with known structural similarity labels (Tanimoto scores from molecular fingerprints) and need to predict structural similarity for new spectrum pairs faster than fingerprint-based methods, or when you want to assess model prediction confidence per.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  - Adam optimizer
  - scikit-learn
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
---

# spectral-similarity-prediction-neural-networks

## Summary

Train and apply a Siamese neural network to predict structural similarity scores (Tanimoto or Dice) directly from pairs of tandem mass spectra without computing molecular fingerprints. This skill enables rapid similarity assessment and uncertainty quantification via Monte-Carlo Dropout on MS/MS spectral pairs.

## When to use

When you have paired MS/MS spectra with known structural similarity labels (Tanimoto scores from molecular fingerprints) and need to predict structural similarity for new spectrum pairs faster than fingerprint-based methods, or when you want to assess model prediction confidence per spectrum pair using uncertainty estimates.

## When NOT to use

- Input spectra are from a single ionization mode and you require cross-ionization predictions (use MS2DeepScore 2.0+ trained on multi-ionization data instead).
- You have fewer than ~100,000 spectra in your training set; the model may not learn robust features without sufficient diversity.
- Structural similarity labels are not available or are computed using methods fundamentally different from RDKit Daylight fingerprints (e.g., substructure matching); the model is trained specifically on Tanimoto scores from Daylight fingerprints.

## Inputs

- MS/MS spectrum pairs (as binned intensity vectors, 10,000 bins, 10–1000 m/z)
- Ground-truth Tanimoto scores or Dice scores from molecular fingerprints (for training)
- Metadata: InChIKey, precursor m/z, ionization mode (optional for extended models)

## Outputs

- Predicted structural similarity scores (continuous, 0–1 range)
- Per-pair uncertainty estimates (interquartile range from Monte-Carlo Dropout ensemble)
- 200-dimensional spectral embeddings (for visualization, clustering, or downstream analysis)

## How to apply

Preprocess spectra by removing peaks with intensity < 0.1% of maximum, retaining the top 1,000 peaks, applying square-root transformation to intensities, and binning into 10,000 equally-sized bins (10–1000 m/z range). Train a Siamese network with a 200-dimensional embedding base network (2×500-node hidden layers, L1/L2 regularization, batch normalization, dropout 0.2) using the Adam optimizer on balanced pairs of spectra sampled across Tanimoto score bins. At inference, compute cosine similarity between paired 200-dimensional embeddings to yield predicted scores. To quantify uncertainty and filter low-confidence predictions, apply Monte-Carlo Dropout (N=10 forward passes with dropout enabled) and compute the interquartile range (IQR) of predictions; retain only pairs with IQR < 0.025 to reduce outliers and improve RMSE from ~0.15 to ~0.10.

## Related tools

- **MS2DeepScore** (Siamese neural network library implementing spectral embedding, similarity prediction, and Monte-Carlo Dropout uncertainty quantification) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum metadata cleaning, filtering (peak intensity thresholding, peak limiting), and data preparation pipeline) — https://github.com/matchms/matchms
- **RDKit** (Compute Daylight molecular fingerprints (2048 bits) and Tanimoto similarity scores for ground-truth labels)
- **Adam optimizer** (Stochastic optimization algorithm for training Siamese network weights)
- **scikit-learn** (t-SNE dimensionality reduction for visualizing 200-dimensional spectral embeddings)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
similarities = ms2ds.pair(spectrum1, spectrum2)
embeddings = ms2ds.get_embedding_array(spectra_list)
```

## Evaluation signals

- RMSE on held-out test set matches reported values: ~0.15 without uncertainty filtering, ~0.10 with IQR < 0.025 threshold, for Tanimoto scores in range 0.1–0.9.
- Distribution of predicted Tanimoto scores aligns with ground-truth distribution (no systematic bias toward 0 or 1).
- Monte-Carlo Dropout ensemble (N=10 passes) produces stable predictions: interquartile ranges are narrow (<0.025) for high-confidence pairs and wide for ambiguous pairs.
- Precision/recall curves show model retrieving high-similarity pairs (Tanimoto > threshold) at expected rates across threshold sweeps.
- t-SNE visualization of 200-dimensional embeddings shows tight clustering of spectra from the same molecule, separation of structurally different compounds.

## Limitations

- Model trained on GNPS spectra; generalization to spectra from other libraries (Mona, MassBank) not characterized in original 2021 paper (extended to 2026 paper cited in README).
- Performance is best for Tanimoto scores between 0.1 and 0.9; boundary cases (very low or very high similarity) have higher RMSE.
- Monte-Carlo Dropout uncertainty estimates may be miscalibrated if the Siamese network has learned to exploit regularization patterns rather than true prediction disagreement.
- Requires substantial training data (≥100,000 diverse spectra); smaller datasets may not yield robust feature learning.
- Runtime and memory scale quadratically with number of spectra for all-pairs similarity computation (6.5M+ unique pairs for 3,601-spectrum test set).

## Evidence

- [other] root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds to remove high-uncertainty predictions: "root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds"
- [other] remove peaks with intensity < 0.1% of maximum, keep top 1,000 peaks, apply square-root transformation to intensities, and bin into 10,000 equally-sized bins: "remove peaks with intensity < 0.1% of maximum, keep top 1,000 peaks, apply square-root transformation to intensities, and bin into 10,000 equally-sized bins (10–1000 m/z)"
- [other] Siamese network with 200-dimensional embedding layer, 2×500-node hidden layers, L1/L2 regularization, batch normalization, dropout rate 0.2: "200-dimensional embedding layer, 2×500-node hidden layers, L1/L2 regularization, batch normalization, dropout rate 0.2"
- [other] Monte-Carlo Dropout uncertainty quantification (N=10 forward passes with dropout enabled, compute interquartile range on predictions): "Monte-Carlo Dropout uncertainty quantification (N=10 forward passes with dropout enabled, compute interquartile range on predictions)"
- [methods] we use annotated MS/MS spectra from GNPS, which underwent basic metadata cleaning as described in [6, 18]. The dataset was retrieved from GNPS (25/01/2021) and contains a total of 210,407 MS/MS: "annotated MS/MS spectra from GNPS, which underwent basic metadata cleaning. The dataset was retrieved from GNPS (25/01/2021) and contains a total of 210,407 MS/MS"
- [methods] For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated: "For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder ./tests/resources/pesticides_processed.mgf: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder ./tests/resources/pesticides_processed.mgf"
- [readme] Training your own model is only recommended if you have some familiarity with machine learning. You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra: "You can train a new model on a dataset of your choice. That, however, should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra"
