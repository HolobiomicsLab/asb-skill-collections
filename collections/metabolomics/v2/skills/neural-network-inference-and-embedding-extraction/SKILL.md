---
name: neural-network-inference-and-embedding-extraction
description: Use when when you have paired or unpaired MS/MS spectra and need to compute structural similarity scores without explicit molecular fingerprint computation, or when you want to generate low-dimensional embeddings for spectral visualization, clustering, or retrieval tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - Spec2Vec
  - RDKit
  - Python
  - scikit-learn
  - matchms
  - PyTorch
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- recently introduced unsupervised Spec2V
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-inference-and-embedding-extraction

## Summary

Extract fixed-dimensional vector embeddings and compute pairwise structural similarity predictions from tandem mass spectra using a trained Siamese neural network. This skill produces both continuous similarity scores (Tanimoto predictions) and intermediate spectrum representations suitable for dimensionality reduction and clustering.

## When to use

When you have paired or unpaired MS/MS spectra and need to compute structural similarity scores without explicit molecular fingerprint computation, or when you want to generate low-dimensional embeddings for spectral visualization, clustering, or retrieval tasks. Use this when you have a trained Siamese model and want to move from raw spectra to either similarity matrices or embedding arrays.

## When NOT to use

- Spectra have not been cleaned and preprocessed (no peak filtering, no binning, no intensity normalization applied yet).
- You need interpretable molecular fingerprints or explicit structural annotations; MS2DeepScore predicts similarity without generating fingerprints.
- Spectra are from ionization modes or compound classes not represented in the training data (model trained on >500,000 spectra from GNPS, Mona, MassBank, MSnLib in positive/negative modes); cross-ionization predictions available in MS2DeepScore 2.0+ but not in the original 2021 model.

## Inputs

- Cleaned tandem mass spectra (MS/MS) in matchms Spectrum objects or formats supporting msp, mzml, mgf, mzxml, json, usi
- Trained Siamese neural network model (PyTorch .pt file)
- Spectrum pairs (tuples of two Spectrum objects) or individual Spectrum objects

## Outputs

- Tanimoto similarity score predictions (continuous values 0–1) for spectrum pairs
- Embedding array: 2D numpy array where each row is a fixed-dimensional vector representation of a spectrum
- Uncertainty estimates (IQR values) for each prediction when using Monte-Carlo Dropout

## How to apply

Load a trained MS2DeepScore Siamese neural network model and pass cleaned, binned spectrum pairs (or individual spectra for embedding extraction) through the base network. For similarity scoring: compute cosine similarity between embeddings of spectrum pairs to produce Tanimoto score predictions (range 0–1). For embedding extraction: call the embedding layer directly to obtain fixed-dimensional vectors for each spectrum, optionally applying Monte-Carlo Dropout at inference time to estimate prediction uncertainty via interquartile range (IQR) filtering. Spectrum preprocessing must include peak intensity normalization (square root transform), removal of low-intensity peaks (<0.1% of max), and binning into 10,000 equally-sized bins across the 10–1000 m/z range. Filter predictions by IQR threshold if uncertainty quantification is required for higher accuracy.

## Related tools

- **MS2DeepScore** (Siamese neural network model for predicting structural similarity scores and generating spectrum embeddings from MS/MS spectra) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data structure and pipeline management; handles spectrum loading, cleaning, and filtering) — https://github.com/matchms/matchms
- **PyTorch** (Deep learning framework for loading trained model and executing forward passes during inference)
- **scikit-learn** (t-SNE dimensionality reduction for visualizing embeddings in 2D chemical space)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
similarity_scores = ms2ds.pair_predict(spectrum_pairs)
```

## Evaluation signals

- Similarity scores lie in valid range [0, 1] representing predicted Tanimoto overlap; check for NaN or out-of-range values.
- Embedding array dimensions match expected size: number of spectra × model embedding dimension (e.g., if model outputs 256-dim vectors, array shape is N × 256).
- Root mean squared error (RMSE) between predicted Tanimoto scores and ground-truth Tanimoto scores (computed on molecular fingerprints) is ~0.15 without uncertainty filtering, improving to ~0.10 with IQR-based filtering; check reproducibility against published Figure 4.
- Precision-recall curves for high structural similarity pairs (Tanimoto > 0.6) show MS2DeepScore outperforming modified Cosine and Spec2Vec baselines across full threshold range (0–1.0).
- Embeddings from the same compound cluster together in dimensionality-reduced visualization (UMAP/t-SNE) with visually distinct separation from unrelated compounds.

## Limitations

- Spectrum metadata (parent mass, elemental formula, adduct information) are not used in the Siamese network training, so predictions rely only on fragment peaks.
- Model was trained on spectra binned to 10,000 m/z bins (10–1000 range); spectra outside this range or with different binning strategies may degrade performance.
- Uncertainty quantification via Monte-Carlo Dropout sampling and IQR filtering adds computational overhead; trade-off between accuracy gain and inference time must be evaluated per use case.
- Cross-ionization mode predictions (negative to positive or vice versa) are not supported in the original 2021 MS2DeepScore model; available only in MS2DeepScore 2.0+.
- Training on >500,000 spectra with strong bias toward common lipids, metabolites, and natural products; performance on rare compound classes or non-standard ionization conditions is not characterized.

## Evidence

- [intro] MS2DeepScore, a deep learning approach that is trained to predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra: "predict structural similarities (Tanimoto or Dice scores based on molecular fingerprints) directly from pairs of MS/MS spectra without first"
- [intro] achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [intro] can create mass spectral embeddings that can be used for additional spectral clustering: "can create mass spectral embeddings that can be used for additional spectral clustering"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [full_text] MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds: "MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical space' by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical"
- [readme] The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model.: "The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model."
