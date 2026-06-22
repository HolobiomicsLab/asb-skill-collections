---
name: python-class-interface-design-for-ml-libraries
description: 'Use when when building a machine learning library for scientific workflows where users need to: (1) prepare domain-specific data (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - ms2deepscore
  - Python
  - matchms
  - PyTorch
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
- make sure the existing tests still work by running ``python setup.py test``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_2_0_cq
    doi: 10.1101/2024.03.25.586580v5
    title: MS2DeepScore 2.0
  dedup_kept_from: coll_ms2deepscore_2_0_cq
schema_version: 0.2.0
---

# python-class-interface-design-for-ml-libraries

## Summary

Design intuitive Python class interfaces for machine learning libraries that expose data preparation, model training, and inference operations as high-level, composable abstractions. This skill ensures that complex workflows (spectrum pair sampling, Siamese network training, similarity scoring) become accessible through clear method signatures and shared weight semantics.

## When to use

When building a machine learning library for scientific workflows where users need to: (1) prepare domain-specific data (e.g., mass spectrometry spectra pairs), (2) train models with hyperparameter control, and (3) compute predictions on new data—all without exposing low-level tensor operations. Use this skill when your library will serve both practitioners unfamiliar with deep learning and researchers who need to customize training.

## When NOT to use

- Input spectra are already vectorized as fixed-length feature tables; the library expects raw spectral peaks (m/z, intensity) that require preprocessing and pair sampling.
- You need real-time streaming inference with sub-millisecond latency; the class interface assumes batch processing and model loading once per session.
- Training dataset is <100,000 spectra; the Siamese architecture and pair sampling strategy are optimized for large, diverse public libraries (>500,000 spectra from GNPS, MoNA, MassBank).

## Inputs

- Settings object specifying spectrum file path, metadata fields, hyperparameters, and ionization mode
- Mass spectrometry spectrum pairs in MGF, MSP, MzML, MzXML, JSON, or USI format
- Trained model checkpoint file (PyTorch .pt format)
- Cleaned spectrum objects (matchms Spectrum instances)

## Outputs

- Trained Siamese neural network model (PyTorch checkpoint)
- Embedding array (NumPy array of latent vectors per spectrum)
- Similarity matrix (NumPy array of pairwise Tanimoto scores in range [0, 1])
- Trained embedding evaluator model (optional, for per-spectrum prediction accuracy)

## How to apply

Structure the library around three core class tiers: a Settings class that bundles hyperparameters and data paths (e.g., SettingsMS2Deepscore for ionization mode, precursor m/z scaling, pair sampling strategy), a Model class that encapsulates the neural network architecture and shared weight logic (e.g., Siamese twin branches processing spectra identically), and a high-level wrapper function that orchestrates data loading, training loops, and validation (e.g., train_ms2deepscore_wrapper). Use metadata transformers (CategoricalToBinary, StandardScaler) as composable mixin classes to handle domain-specific feature engineering. For similarity prediction, design a separate class (e.g., MS2DeepScore) that loads trained model checkpoints and exposes methods for computing pairwise scores and extracting embeddings. Validate that class methods accept standardized input containers (lists of spectrum objects from matchms) and return NumPy arrays or scalar predictions in expected ranges (e.g., [0, 1] for Tanimoto scores).

## Related tools

- **ms2deepscore** (Core library exposing Settings, Model, and MS2DeepScore classes for Siamese training and similarity scoring on mass spectrometry spectral pairs) — https://github.com/matchms/ms2deepscore
- **matchms** (Provides Spectrum class, DEFAULT_FILTERS pipeline, and Pipeline orchestration for data loading and spectrum preprocessing) — https://github.com/matchms/matchms
- **PyTorch** (Underlying deep learning framework for Siamese network implementation and checkpoint serialization (.pt files))

## Examples

```
from ms2deepscore.SettingsMS2Deepscore import SettingsMS2Deepscore, SettingsEmbeddingEvaluator
from ms2deepscore.wrapper_functions.training_wrapper_functions import train_ms2deepscore_wrapper
settings = SettingsMS2Deepscore(spectrum_file_path="./combined_libraries.mgf", additional_metadata=[("CategoricalToBinary", {"metadata_field": "ionmode", "entries_becoming_one": "positive", "entries_becoming_zero": "negative"})])
train_ms2deepscore_wrapper(settings, SettingsEmbeddingEvaluator())
```

## Evaluation signals

- Settings object successfully bundles all hyperparameters (ionization mode, precursor m/z scaling, metadata transformers) without requiring user to manipulate raw tensor configs
- Siamese model accepts pairs of Spectrum objects and outputs scalar Tanimoto scores in range [0.0, 1.0]
- Trained checkpoint loads without errors and produces identical similarity matrices across multiple inference runs
- Embedding array has shape (n_spectra, embedding_dim) and can be reduced to 2D via UMAP for visualization without requiring user intervention in model forward pass
- Wrapper function completes training in <5 minutes on laptop hardware with <100,000 test spectra; logs convergence and validation metrics

## Limitations

- Pair sampling quality must be manually verified and re-optimized for new datasets, particularly for training sets <100,000 spectra, as suboptimal pair distributions degrade model learning
- Model requires spectra to be cleaned using matchms DEFAULT_FILTERS before training; raw, uncurated spectral data may introduce noise that undermines Siamese similarity learning
- Cross-ionization mode predictions are supported by the default model (trained on >500,000 combined spectra) but custom-trained models may not generalize across ionization modes unless explicitly trained on balanced positive/negative pairs
- Embedding evaluator is optional and incurs additional training cost; its accuracy estimates are model-specific and may not transfer to re-trained or fine-tuned variants

## Evidence

- [readme] The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra.: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra."
- [other] Siamese neural network designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto scores.: "MS2DeepScore implements a Siamese neural network architecture designed to take pairs of mass spectrometry spectra as input and output predicted molecular structural similarities expressed as Tanimoto"
- [readme] SettingsMS2Deepscore bundles spectrum file path, metadata field transformers (CategoricalToBinary, StandardScaler), and ionization mode as configuration.: "settings = SettingsMS2Deepscore(
    spectrum_file_path=spectrum_file,
    additional_metadata=[...],
    ionisation_mode="both")"
- [readme] Pair sampling quality must be checked and potentially re-optimized for new datasets, particularly for smaller training sets where pair sampling can be suboptimal if not checked.: "Particularly for smaller training sets, the pair sampling can be suboptimal if not checked."
- [readme] Model training should use >100,000 spectra of sufficiently diverse types for effective feature learning.: "should contain a substantial amount of spectra to learn relevant features, say > 100,000 spectra of sufficiently diverse types."
