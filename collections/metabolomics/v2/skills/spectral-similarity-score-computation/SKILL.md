---
name: spectral-similarity-score-computation
description: Use when when you have pairs of MS/MS spectra (in mgf, msp, mzml, mzxml,
  json, or usi format) and need to retrieve structurally related compounds or rank
  spectral similarity on a continuous scale (Tanimoto prediction).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS2DeepScore
  - Spec2Vec
  - RDKit
  - Python
  - scikit-learn
  - matchms
  - ms2deepscore
  - PyTorch
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- recently introduced unsupervised Spec2V
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
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

# spectral-similarity-score-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute pairwise structural similarity scores between tandem mass spectra by predicting Tanimoto coefficients from spectrum pairs using a deep learning Siamese network, enabling large-scale spectral library searching and compound retrieval. This skill predicts structural similarity without requiring explicit molecular fingerprint computation.

## When to use

When you have pairs of MS/MS spectra (in mgf, msp, mzml, mzxml, json, or usi format) and need to retrieve structurally related compounds or rank spectral similarity on a continuous scale (Tanimoto prediction). Use this instead of classical cosine similarity when you need improved precision-recall trade-offs for high structural similarity pairs (Tanimoto > 0.6) or when you want to avoid computing molecular fingerprints explicitly. Appropriate for large-scale comparisons (>100K spectra pairs) where speed and scalability matter.

## When NOT to use

- Input spectra have not been cleaned (peaks not filtered by intensity, metadata not standardized); use matchms cleaning pipeline first.
- You only have individual spectra, not pairs; this skill requires spectrum pairs as input.
- You need interpretable molecular structural information (e.g., which functional groups drive similarity); MS2DeepScore predictions are black-box and do not provide atom-level or fragment explanations.

## Inputs

- Pair of cleaned MS/MS spectra (spectrum objects with m/z and intensity arrays)
- Trained MS2DeepScore model checkpoint (PyTorch .pt file)
- Spectrum metadata (optional: parent mass, ionization mode, elemental formula)

## Outputs

- Predicted Tanimoto structural similarity score (continuous value, 0–1 per pair)
- Uncertainty estimate (interquartile range from Monte-Carlo Dropout ensemble)
- Spectrum embeddings (fixed-dimension vector per spectrum for clustering/visualization)

## How to apply

Load the trained MS2DeepScore Siamese network model (available from zenodo). Prepare input spectra by cleaning metadata using matchms, removing peaks with intensities < 0.1% of maximum, limiting to the 1000 highest-intensity peaks, and applying square-root transformation to peak intensities. For each spectrum pair, pass the binned spectrum data (10,000 equally-sized bins from 10 to 1000 m/z) through the base network to obtain embeddings, then compute cosine similarity between embedding pairs to yield Tanimoto score predictions. Optionally apply Monte-Carlo Dropout (sample predictions across 10+ model variations with dropout enabled) to quantify prediction uncertainty via interquartile range; filter predictions with IQR above a user-defined threshold to improve accuracy. Vary the similarity score threshold from 0 to 1.0 to generate precision-recall curves if ground-truth structural similarity labels (RDKit Daylight fingerprint Tanimoto ≥ 0.6) are available for validation.

## Related tools

- **ms2deepscore** (Core library providing the Siamese network model, embedding computation, and prediction API for spectral similarity scoring) — https://github.com/matchms/ms2deepscore
- **matchms** (Data preparation and spectrum cleaning (metadata standardization, peak filtering, adduct extraction) prior to similarity computation) — https://github.com/matchms/matchms
- **RDKit** (Molecular fingerprint generation (Daylight fingerprints, 2048 bits) for ground-truth Tanimoto labels during validation and model training)
- **scikit-learn** (Dimensionality reduction (t-SNE) for visualizing spectra in chemical space after embedding computation)
- **PyTorch** (Deep learning framework underlying the Siamese network model and Monte-Carlo Dropout uncertainty quantification)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model("ms2deepscore_model.pt")
ms2ds = MS2DeepScore(model)
similarity_score = ms2ds.pair_to_distance(spectrum_1, spectrum_2)
```

## Evaluation signals

- Predicted Tanimoto scores fall within the expected range [0, 1] with a distribution that matches the training set structural similarity label distribution.
- On a validation set of 3600+ spectra with known high structural similarity pairs (Tanimoto > 0.6), precision-recall curve of MS2DeepScore predictions lies above classical spectral similarity measures (modified cosine, Spec2Vec) across the full threshold range.
- Root mean squared error (RMSE) between predicted and actual Tanimoto scores on a held-out test set is ≤ 0.15 without uncertainty filtering, and ≤ 0.10 when filtering predictions with IQR below user-defined threshold.
- Monte-Carlo Dropout ensemble (10+ samples per pair) yields stable, low-variance uncertainty estimates; interquartile range correlates inversely with prediction error.
- Spectrum embeddings computed from the base network are suitable for clustering and UMAP visualization, with known structurally similar compounds (same InChIKey) appearing proximal in 2D reduced space.

## Limitations

- Model requires >100K spectra for effective training; smaller custom datasets may suffer from poor generalization. Pre-trained model on public libraries (GNPS, MoNA, MassBank, MSnLib) may not transfer well to highly specialized or proprietary mass spectrometry datasets.
- Predictions are trained to approximate Tanimoto on RDKit Daylight fingerprints (2048 bits); structural similarity is limited to molecular features captured by this fingerprint type and does not guarantee chemically meaningful similarity in all domains.
- Root mean squared error is approximately 0.15 without uncertainty restrictions; predictions for borderline structural similarity cases (Tanimoto ≈ 0.5–0.65) may be unreliable. Uncertainty filtering via IQR improves accuracy but at the cost of reduced coverage.
- Model does not use spectrum metadata (parent mass, elemental formula, ionization mode details) in the version described in the primary article; version 2.0+ supports cross-ionization mode predictions but requires different training and model checkpoint.
- Computational cost scales quadratically with the number of spectra (all unique pairs); comparison of >1M spectra requires efficient pairwise computation and GPU acceleration to remain practical.

## Evidence

- [intro] MS2DeepScore, a deep learning approach that is trained to predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra without first: "MS2DeepScore, a deep learning approach that is trained to predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra"
- [other] MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall combinations for retrieving high Tanimoto pairs (Tanimoto > 0.6).: "MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer"
- [intro] achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf". Alternatively you can of course use your own spectra, most common formats are supported, e.g. msp, mzml, mgf, mzxml, json, usi.: "most common formats are supported, e.g. msp, mzml, mgf, mzxml, json, usi"
