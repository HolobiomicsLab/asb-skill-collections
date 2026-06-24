---
name: nmr-spectrum-preprocessing
description: Use when you have raw or semi-processed 1D NMR spectra (¹H and/or ¹³C)
  from routine laboratory instruments and need to feed them into a CNN–transformer
  architecture for end-to-end structure elucidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Convolutional Neural Network (CNN)
  - Transformer Architecture
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- Integrating this capability with a convolutional neural network, we build an end-to-end
  model
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

# nmr-spectrum-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and normalize 1D ¹H and/or ¹³C NMR spectra for machine learning-based molecular structure prediction by loading, validating, and encoding spectral data into a standardized format compatible with CNN feature extraction.

## When to use

You have raw or semi-processed 1D NMR spectra (¹H and/or ¹³C) from routine laboratory instruments and need to feed them into a CNN–transformer architecture for end-to-end structure elucidation. Use this skill when your spectra lack the standardized numeric encoding required by convolutional layers, or when you need to pair spectra with ground-truth molecular structure annotations for model evaluation.

## When NOT to use

- Spectra are already encoded as pretrained CNN embeddings or latent features; skip directly to transformer assembly.
- Input is 2D NMR data (COSY, HSQC, HMBC); this skill is designed for 1D ¹H and/or ¹³C spectra only.
- Molecules exceed 19 heavy atoms; the framework's effectiveness scope does not extend beyond this threshold.

## Inputs

- 1D ¹H NMR spectrum (numeric array, ppm vs. intensity)
- 1D ¹³C NMR spectrum (numeric array, ppm vs. intensity)
- Molecular structure ground truth (molecular formula, connectivity/SMILES)
- Evaluation dataset (spectra–structure pairs)

## Outputs

- Preprocessed NMR spectra tensor (normalized, aligned, CNN-compatible)
- CNN-encoded spectral features (latent representation for transformer input)
- Validation metadata (shape, range, alignment success indicators)

## How to apply

Load preprocessed NMR spectra and their corresponding molecular structure ground truth from an evaluation dataset into aligned tensors. Validate that spectral data are encoded as numeric arrays with consistent shape and range (suitable for CNN input). Normalize or standardize spectral intensities across the dataset to account for instrument variation. Align chemical shift axes (ppm scale) and peak intensity distributions if multiple spectra are combined. Pass the preprocessed spectra through the CNN feature extraction layer, which encodes spectral patterns into latent representations. Verify that the output feature tensors have expected dimensionality before passing to the transformer assembly module.

## Related tools

- **Convolutional Neural Network (CNN)** (Feature extraction layer that encodes preprocessed NMR spectral information into latent representations for downstream transformer assembly)
- **Transformer Architecture** (Downstream module that receives CNN-encoded spectral features and assembles molecular fragments to predict connectivity and formula)

## Evaluation signals

- Preprocessed spectral tensors have consistent shape across the entire evaluation dataset (no ragged arrays).
- Normalized spectral intensities fall within the expected range (e.g., [0, 1] or z-score ~ 0 ± 3σ) with no NaN or inf values.
- Chemical shift axes (ppm scale) are aligned correctly across all spectra; peak positions do not shift unexpectedly after preprocessing.
- CNN feature extraction produces output tensors with the expected latent dimensionality, matching transformer input specification.
- Downstream structure prediction accuracy (using ground-truth comparisons) is consistent with reported performance on molecules with up to 19 heavy atoms.

## Limitations

- Framework is validated only for molecules with up to 19 heavy (non-hydrogen) atoms; preprocessing and prediction reliability are unverified beyond this scope.
- Preprocessing assumes 1D ¹H and/or ¹³C spectra acquired on routine instruments; non-standard acquisition parameters or artifacts may degrade model performance.
- No explicit handling of solvent peaks, impurities, or baseline distortions is described; these must be addressed upstream in the data collection or cleaning pipeline.

## Evidence

- [other] Load preprocessed NMR spectra (¹H and/or ¹³C) and corresponding molecular structure ground truth from the evaluation dataset.: "Load preprocessed NMR spectra (¹H and/or ¹³C) and corresponding molecular structure ground truth from the evaluation dataset."
- [other] Feed NMR spectra through the convolutional neural network feature extraction layer to encode spectral information.: "Feed NMR spectra through the convolutional neural network feature extraction layer to encode spectral information."
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra: "framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
