---
name: ms-ms-spectral-preprocessing-normalization
description: Use when you have paired MS/MS spectra from unknown and known metabolites with raw intensity values and need to prepare them as input for a deep-learning model that will predict structural similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DeepMASS
  - RDKit
  - Keras
derived_from:
- doi: 10.1021/acs.analchem.8b05405
  title: Deep MS/MS similarity
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  dedup_kept_from: coll_deep_ms_ms_similarity_cq
schema_version: 0.2.0
---

# MS/MS spectral preprocessing and normalization

## Summary

Normalize and extract m/z features from raw MS/MS spectra to prepare paired unknown–known metabolite spectral datasets for deep-learning model training. This preprocessing step standardizes intensity values across spectra, enabling consistent feature encoding and downstream structural similarity prediction.

## When to use

You have paired MS/MS spectra from unknown and known metabolites with raw intensity values and need to prepare them as input for a deep-learning model that will predict structural similarity. Apply this skill when spectral intensities are uncalibrated across different runs or instruments and m/z features must be extracted in a uniform manner before model training.

## When NOT to use

- Spectra are already normalized and feature-extracted by your instrument vendor or prior pipeline step.
- You are performing peak picking or deconvolution (a distinct upstream step; preprocessing assumes you already have resolved m/z–intensity pairs).
- Your workflow does not involve paired spectra or supervised learning (e.g., if you only need to identify individual spectra against a single reference database without training a model).

## Inputs

- Raw MS/MS spectral data (paired unknown and known metabolite spectra)
- Spectral metadata (acquisition parameters, metabolite identifiers)
- m/z and intensity arrays per spectrum

## Outputs

- Normalized intensity values (0–1 or z-score scaled)
- Extracted m/z feature vectors
- Preprocessed spectrum pairs with metadata labels
- Feature-ready dataset for model training

## How to apply

Load paired MS/MS spectra datasets (unknown and known metabolite spectra) with their metadata. Normalize intensity values across all spectra using a standardization method (e.g., vector normalization or peak-relative scaling) to ensure consistent magnitude ranges. Extract relevant m/z features from each spectrum—typically the mass-to-charge ratio values and their associated normalized intensities. The rationale is that deep-learning models are sensitive to input magnitude and feature scaling; unnormalized spectra with widely varying intensity ranges can bias gradient-based optimization. Store preprocessed spectra in a structured format (e.g., paired feature arrays) ready for supervised learning with annotated structural similarity labels.

## Related tools

- **DeepMASS** (End-to-end framework that incorporates spectral preprocessing, deep-learning model training, and structural similarity ranking for known-to-unknown metabolite identification) — https://github.com/hcji/DeepMASS
- **RDKit** (Used for molecular structure manipulation and feature extraction in the DeepMASS pipeline)
- **Keras** (Deep-learning framework for building and training the spectral encoder model)

## Evaluation signals

- Intensity values fall within expected normalized range (e.g., [0, 1] or mean ≈ 0, std ≈ 1 for z-score scaling).
- No NaN or infinite values remain after normalization; all m/z features are numeric.
- Preprocessed spectrum pairs maintain consistent dimensionality (same number of m/z features per spectrum).
- Normalized spectra preserve relative peak patterns—visual inspection or cosine similarity to raw spectrum should show high correlation (>0.95).
- Model training converges on the normalized data without numerical instability (loss decreases monotonically; no NaN gradients).

## Limitations

- Preprocessing assumes MS/MS spectra are already peak-detected and mass-calibrated; does not perform deconvolution or mass recalibration.
- Normalization method choice (e.g., peak-relative vs. vector norm) can affect downstream model performance; the article does not specify which method is optimal.
- The DeepMASS dataset (MetDNA) has been removed from the public repository; preprocessing must be demonstrated on your own in-house spectral database or public alternatives.
- No ablation study is provided on the sensitivity of the deep-learning model to different normalization schemes, so practitioners should validate on their own data.

## Evidence

- [other] Load paired MS/MS spectra datasets (unknown and known metabolite spectra) with metadata: "Load paired MS/MS spectra datasets (unknown and known metabolite spectra) with metadata."
- [other] Preprocess spectra by normalizing intensity values and extracting relevant m/z features: "Preprocess spectra by normalizing intensity values and extracting relevant m/z features."
- [readme] Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites: "Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites"
- [other] Train the model on annotated spectrum pairs with structural similarity labels using supervised learning: "Train the model on annotated spectrum pairs with structural similarity labels using supervised learning."
