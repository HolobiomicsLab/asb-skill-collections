---
name: molecular-formula-prediction
description: Use when you have 1D ¹H or ¹³C NMR spectra from an unknown organic compound
  and need to predict its molecular formula (e.g., C₆H₁₂O₂). The compound must contain
  ≤19 heavy (non-hydrogen) atoms. Use this as the first stage of a structure elucidation
  pipeline before predicting molecular connectivity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Transformer (encoder-decoder architecture)
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- transformer architecture
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct_cq
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct_cq
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

# Molecular Formula Prediction from NMR Spectra

## Summary

Predict the molecular formula (elemental composition) of an unknown compound from 1D ¹H and/or ¹³C NMR spectra using a multitask transformer-based machine learning model. This skill enables rapid structure elucidation traditionally performed by manual spectroscopic interpretation.

## When to use

Apply this skill when you have 1D ¹H or ¹³C NMR spectra from an unknown organic compound and need to predict its molecular formula (e.g., C₆H₁₂O₂). The compound must contain ≤19 heavy (non-hydrogen) atoms. Use this as the first stage of a structure elucidation pipeline before predicting molecular connectivity.

## When NOT to use

- Input compound contains >19 heavy atoms — model was only validated on molecules up to C/H/N/O/S/halide with ≤19 non-hydrogen atoms.
- Input is a 2D NMR spectrum (HSQC, HMBC, COSY) — this skill is trained exclusively on 1D spectra.
- The spectrum is from a mixture or unknown impurities — the model assumes a single pure compound.

## Inputs

- 1D ¹H NMR spectrum (token-encoded spectral features or raw peak list)
- 1D ¹³C NMR spectrum (token-encoded spectral features or raw peak list)
- Ground-truth molecular formulas (for training/validation)

## Outputs

- Predicted molecular formula (element count vector or SMILES-like formula string)
- Prediction confidence scores (softmax probabilities per element)
- Accuracy metric on held-out test set

## How to apply

Encode the input 1D NMR spectrum as a token sequence representing spectroscopic features (chemical shifts, intensities, multiplicities). Feed this sequence through a transformer encoder that learns to map spectral embeddings to a chemical formula space. The model is trained end-to-end using supervised classification loss on ground-truth molecular formulas. At inference, the transformer decoder outputs a predicted molecular formula as a vector encoding element counts (e.g., [C_count, H_count, O_count, N_count, ...]). Validate predictions by comparing predicted formula to ground truth using exact-match accuracy or elemental composition metrics. The model integrates multi-head self-attention to capture long-range spectral correlations and learns which NMR peaks are most diagnostic for formula prediction.

## Related tools

- **PyTorch** (Neural network framework for implementing transformer encoder-decoder architecture, training supervised loss on formula classification, and inference) — https://pytorch.org
- **Transformer (encoder-decoder architecture)** (Core neural architecture with multi-head self-attention and cross-attention layers to map NMR spectral embeddings to molecular formula space)

## Evaluation signals

- Exact-match accuracy: predicted formula matches ground-truth formula (e.g., C₆H₁₂O₂)
- Element-wise accuracy: each predicted element count (C, H, O, N, etc.) matches ground truth
- Schema invariant: output vector has fixed length equal to number of tracked elements and sums to expected molecular weight range
- Held-out test set accuracy reported separately for ¹H-only, ¹³C-only, and combined spectra inputs
- No negative element counts or implausible formulas (e.g., H₀ or C₀)

## Limitations

- Validated only on molecules with ≤19 heavy atoms; performance unknown for larger molecules.
- Requires high-quality, well-resolved 1D NMR spectra; noisy, overlapped, or sparse spectra may degrade predictions.
- Model is trained on a specific dataset; generalization to novel chemical scaffolds not in training set is not characterized.
- Does not handle isotope information (e.g., ¹³C labeling) — treats all carbons uniformly.

## Evidence

- [intro] A multitask machine learning framework can predict molecular structure (formula and connectivity) from 1D ¹H and/or ¹³C NMR spectra: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [methods] Training uses supervised loss on formula prediction as classification task: "Train the transformer end-to-end using supervised loss on formula prediction (classification) and bond connectivity prediction (link prediction on molecular graph)"
- [methods] Validation involves comparing predicted formula to ground truth: "Validate the trained model on held-out test molecules by comparing predicted formula and connectivity to ground truth, computing accuracy metrics for both outputs"
- [intro] Framework is effective for molecules with up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
