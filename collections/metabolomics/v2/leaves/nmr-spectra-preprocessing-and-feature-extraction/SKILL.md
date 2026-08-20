---
name: nmr-spectra-preprocessing-and-feature-extraction
description: Use when when you have raw or lightly processed 1D NMR spectra (¹H and/or
  ¹³C) from unknown organic compounds and need to extract latent spectral features
  prior to structure elucidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - convolutional neural network
  - transformer architecture
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectra-preprocessing-and-feature-extraction

## Summary

Preprocess raw 1D NMR spectra (¹H and/or ¹³C) and extract spectral features using a convolutional neural network encoder to prepare inputs for downstream molecular structure prediction. This skill bridges raw spectroscopic data and learned feature representations suitable for transformer-based structure assembly.

## When to use

When you have raw or lightly processed 1D NMR spectra (¹H and/or ¹³C) from unknown organic compounds and need to extract latent spectral features prior to structure elucidation. Apply this skill when the downstream task requires dense, learned feature vectors rather than raw peak lists or chemical shift values, and when molecules are expected to contain up to 19 heavy atoms.

## When NOT to use

- Input is already a hand-curated list of chemical shift values and multiplicities — the CNN encoder is designed to learn features directly from raw or minimally processed spectra, not from manually extracted peak annotations.
- Molecules contain more than 19 heavy atoms — the model was demonstrated on molecules with ≤19 heavy atoms and may not generalize reliably beyond this scope.
- You require direct interpretability of individual peaks or coupling constants — CNN feature extraction produces opaque, distributed representations unsuitable for chemist-level peak assignment.

## Inputs

- Preprocessed 1D ¹H NMR spectra (tensor, shape [batch, frequency_bins] or [batch, channels, frequency_bins])
- Preprocessed 1D ¹³C NMR spectra (tensor, shape [batch, frequency_bins] or [batch, channels, frequency_bins])
- Trained convolutional neural network encoder weights/checkpoint

## Outputs

- Spectral feature vectors (tensor, shape [batch, feature_dim]) — learned dense representations of NMR spectra
- Intermediate activation maps (optional, for interpretability)

## How to apply

Load preprocessed 1D ¹H and/or ¹³C NMR spectra from your test or query set into a standardized tensor format (typically [batch, frequency_bins] or [batch, channels, frequency_bins]). Pass the spectra batch through a trained convolutional neural network encoder that extracts hierarchical spectral features (e.g., peak patterns, multiplet structure, relative intensities) across multiple convolutional layers. The CNN encoder output is a fixed-dimensional feature vector per spectrum that captures the essential information content of the spectral profile. These encoded features are then fed into downstream models (e.g., a transformer) that perform higher-level tasks such as molecular formula prediction or connectivity assembly. The CNN encoder should be pretrained on a large, diverse dataset of NMR spectra paired with known molecular structures to ensure robust feature learning.

## Related tools

- **convolutional neural network** (Encoder that extracts learned spectral features from raw 1D NMR spectra; the first stage of the end-to-end pipeline)
- **transformer architecture** (Downstream module that consumes CNN-encoded spectral features to predict molecular formula and connectivity)

## Evaluation signals

- Feature vector shape and dimensionality match the expected feature_dim from the trained encoder (e.g., [batch, 256] if the CNN outputs 256 features per spectrum).
- Feature values are continuous and bounded (not NaN, inf, or trivially zero-valued), indicating successful forward pass without numerical failures.
- When the same spectrum is encoded multiple times with the same model in inference mode (no dropout), the output feature vectors are identical (deterministic), confirming reproducibility.
- Top-k exact structure recovery accuracy on a held-out test set matches or approaches the reported metrics from the paper (e.g., >70% top-1 accuracy on molecules with ≤19 heavy atoms), when features are passed to the full pipeline.
- Feature entropy and variance across a batch of diverse spectra are non-trivial (not constant or highly skewed), suggesting the encoder is learning to differentiate between structurally diverse molecules.

## Limitations

- The model was evaluated only on molecules with up to 19 heavy atoms; performance on larger molecules is unknown.
- Preprocessing requirements (normalization, frequency alignment, noise filtering) for input spectra are not explicitly specified in the article and may significantly impact feature quality.
- The CNN encoder is task-specific and requires retraining if applied to NMR spectra from a substantially different chemical domain, acquisition protocol, or instrument type.
- The skill assumes ¹H and/or ¹³C spectra; applicability to other nuclei (e.g., ¹⁹F, ³¹P) is not demonstrated.

## Evidence

- [intro] CNN encodes spectra, transformer assembles fragments: "Pass spectra through the convolutional neural network encoder to extract spectral features. Feed encoded features into the transformer architecture to assemble molecular fragments"
- [intro] End-to-end integration for structure prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] Demonstrated scope: up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] Multitask prediction from 1D NMR: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
