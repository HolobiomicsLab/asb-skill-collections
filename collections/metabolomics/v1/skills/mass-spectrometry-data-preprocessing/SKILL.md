---
name: mass-spectrometry-data-preprocessing
description: Use when you have raw mass spectra or processed feature matrices from liquid chromatography–mass spectrometry (LC-MS) or direct infusion MS that must be ingested by a deep learning model for substance identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PS2MS
  - PS²MS
  - NEIMS
  - DeepEI
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
---

# mass-spectrometry-data-preprocessing

## Summary

Prepare raw or processed mass spectrometry spectra for deep learning inference by normalizing intensities and converting m/z–intensity pairs into vectorized feature representations. This skill bridges raw instrumental output and neural network input schemas, ensuring compatibility with downstream prediction systems like PS²MS.

## When to use

You have raw mass spectra or processed feature matrices from liquid chromatography–mass spectrometry (LC-MS) or direct infusion MS that must be ingested by a deep learning model for substance identification. The input spectra are in a format native to MS instruments or databases but do not yet conform to the tokenization and normalization rules required by PS²MS or similar neural architectures.

## When NOT to use

- Input is already a tokenized and normalized feature tensor matching the target model's input shape and value range.
- You are performing exploratory mass spectrometry data visualization or statistical summaries that do not require neural network inference.

## Inputs

- raw mass spectra (m/z and intensity pairs)
- processed feature matrices from MS data
- mass spectrometry data in format compatible with PS²MS input schema

## Outputs

- normalized and tokenized spectra tensors
- vectorized m/z–intensity feature matrices
- preprocessed data conforming to deep learning model input schema

## How to apply

Load mass spectrometry input data as raw spectra (m/z–intensity pairs) or processed feature matrices. Apply PS²MS normalization and feature extraction by tokenizing and vectorizing m/z and intensity pairs according to the model's input schema. Ensure all spectra conform to identical feature dimensions and value ranges (e.g., intensity normalization to 0–1 or log-scale) before batching. Validate that preprocessed spectra match the expected input tensor shape and data type. Execute this preprocessing step immediately before invoking the pre-trained deep learning model's forward inference pass, as the model's performance depends critically on consistent input formatting.

## Related tools

- **PS²MS** (Target deep learning prediction system that consumes preprocessed spectra to infer NPS class labels and confidence scores) — https://github.com/jhhung/PS2MS
- **NEIMS** (Generates predicted mass spectra for synthetic NPS database compounds; output spectra may require equivalent preprocessing)
- **DeepEI** (Predicts chemical fingerprints from mass spectra; interacts with preprocessed spectrum representations)

## Evaluation signals

- Preprocessed spectra match the exact input tensor shape and data type required by PS²MS (confirm by inspecting tensor.shape and tensor.dtype).
- All intensity values fall within the normalized range (e.g., 0–1 or verified log-scale bounds) with no NaN or inf entries.
- m/z and intensity pairs are consistently tokenized across all spectra in the batch; verify by spot-checking multiple samples for uniform feature dimensionality.
- Forward inference on a small test batch completes without shape mismatch or dtype errors.
- Prediction confidence scores and class probability distributions are valid (sum to 1.0, no negative values).

## Limitations

- Preprocessing rules are specific to the PS²MS model architecture; preprocessing for other deep learning MS systems (e.g., NEIMS or DeepEI) may differ in tokenization and normalization strategies.
- No publicly documented changelog or version history for preprocessing parameter changes; reproducibility across PS²MS versions may be affected.
- Preprocessing does not handle missing or corrupted spectra; input data quality assurance (e.g., intensity range validation, m/z monotonicity checks) must be performed upstream.

## Evidence

- [other] Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs).: "Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs)."
- [other] Load mass spectrometry input data (raw spectra or processed feature matrices) compatible with PS2MS input schema.: "Load mass spectrometry input data (raw spectra or processed feature matrices) compatible with PS2MS input schema."
- [other] Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence scores.: "Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence scores."
