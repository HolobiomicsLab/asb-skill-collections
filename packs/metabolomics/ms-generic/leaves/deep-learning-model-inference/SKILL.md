---
name: deep-learning-model-inference
description: Use when you have preprocessed mass spectrometry spectra (tokenized m/z
  and intensity pairs or feature matrices) and a trained deep learning model checkpoint,
  and you need to classify unknown compounds or generate prediction confidence scores
  for structural novelty analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3379
  tools:
  - PS2MS
  - Python deep learning framework (PyTorch or TensorFlow)
  - Matplotlib or Seaborn for visualization
  - NEIMS
  - DeepEI
  - PyTorch or TensorFlow
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
- Deep Learning-Based Prediction System
- prediction confidence scores vary across
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  - build: coll_ms2mp_cq
    doi: 10.1021/acs.analchem.4c06875
    title: MS2MP
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  - build: coll_ps2ms_cq
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-inference

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute forward inference pass on preprocessed mass spectrometry data using a pre-trained deep learning model to generate predictions with confidence scores. This skill applies learned model weights to new inputs to produce classification results and per-class probability distributions without retraining.

## When to use

You have preprocessed mass spectrometry spectra (tokenized m/z and intensity pairs or feature matrices) and a trained deep learning model checkpoint, and you need to classify unknown compounds or generate prediction confidence scores for structural novelty analysis. Use this skill when the input data schema matches the model's training format and you require ranked predictions with per-class probabilities rather than model parameter updates.

## When NOT to use

- Input spectra have not been preprocessed or normalized according to the model's training requirements — preprocess first before inference.
- You have raw, untokenized mass spectrometry data (e.g., raw vendor instrument files) — execute feature extraction and normalization workflow before inference.
- The goal is to retrain, fine-tune, or evaluate model parameters — use model training/evaluation workflows instead of inference.

## Inputs

- Preprocessed mass spectrometry feature matrices or tokenized m/z–intensity pair vectors
- Pre-trained deep learning model weights (e.g., PyTorch .pt or TensorFlow .h5 checkpoint)
- Model architecture definition and input schema specification
- Spectrum identifiers or sample metadata (for result annotation)

## Outputs

- Structured prediction table with spectrum identifiers, predicted NPS class labels, and per-class probabilities
- Confidence scores or softmax probability distributions for each prediction
- Optionally: prediction uncertainties or model uncertainty estimates for filtering

## How to apply

Load the pre-trained deep learning model weights from the repository (e.g., jhhung/PS2MS). Ensure input spectra conform to the model's expected preprocessing format (normalization, tokenization/vectorization of m/z–intensity pairs). Execute the forward pass on the entire batch of preprocessed spectra. Extract raw model outputs (e.g., softmax probabilities, prediction uncertainties) and apply a confidence threshold to filter low-confidence predictions. Post-process by assigning class labels and generating structured output tables mapping spectrum identifiers to predicted NPS classes and per-class probabilities. Validate output schema consistency and probability distributions (softmax probabilities must sum to 1.0 per spectrum).

## Related tools

- **PS2MS** (Pre-trained deep learning system for NPS classification from mass spectrometry; executes inference to generate predictions and confidence scores) — https://github.com/jhhung/PS2MS
- **NEIMS** (Predicts mass spectrum features for synthetic database compounds used in PS2MS comparison pipeline)
- **DeepEI** (Predicts chemical fingerprints for unknown analytes and synthetic database compounds for similarity scoring)
- **PyTorch or TensorFlow** (Deep learning framework for loading model checkpoints and executing forward inference passes)

## Evaluation signals

- All output probabilities per spectrum sum to 1.0 (softmax constraint satisfied)
- Prediction confidence scores fall within the expected range (e.g., [0.0, 1.0] for probability-based scores)
- Output table schema matches specification: each row has spectrum ID, predicted class label, and per-class probability columns with no missing values
- Predictions for positive control compounds (if available) match expected NPS classes or known structural analogues
- Confidence scores are lower for structurally novel compounds than for training-distribution-similar compounds (when validated against structural novelty stratification)

## Limitations

- Model predictions are limited to NPS classes present in the training dataset; compounds with core structures absent from training may receive low confidence scores
- Inference accuracy depends critically on input preprocessing conformance to the training normalization and tokenization scheme; any deviation will degrade predictions
- The system is designed for novel psychoactive substance detection and may not generalize to other chemical classification tasks or non-spectrometry modalities
- Confidence scores do not directly measure chemical novelty; they measure similarity to training-set prediction distributions — novel structural analogues may receive low confidence even if correctly classified

## Evidence

- [other] Load the pre-trained PS2MS deep learning model from the jhhung/PS2MS repository. Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence scores.: "Load the pre-trained PS2MS deep learning model from the jhhung/PS2MS repository. Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence"
- [other] Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs).: "Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs)."
- [other] Post-process predictions to assign NPS class labels and filter by model confidence threshold. Export results as a structured prediction table with spectrum identifiers, predicted NPS classes, and per-class probabilities.: "Post-process predictions to assign NPS class labels and filter by model confidence threshold. Export results as a structured prediction table with spectrum identifiers, predicted NPS classes, and"
- [other] Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model.: "Extract or compute prediction confidence scores (e.g., softmax probabilities, prediction uncertainties) for each compound in the evaluation set using the PS2MS model."
- [readme] The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score.: "The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score."
