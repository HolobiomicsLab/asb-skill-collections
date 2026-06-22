---
name: cnn-spectral-feature-extraction
description: Use when you have preprocessed 1D NMR spectra (¹H and/or ¹³C) and need to extract spectral features for molecular structure inference on molecules with up to 19 heavy atoms. The skill is necessary as the first stage before fragment assembly or connectivity prediction;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Convolutional Neural Network (CNN)
  - Transformer architecture
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- Integrating this capability with a convolutional neural network, we build an end-to-end model
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

# CNN-based spectral feature extraction

## Summary

Extract learned feature representations from 1D NMR spectra (¹H and/or ¹³C) using a convolutional neural network, transforming raw spectral intensity patterns into high-level encodings suitable for downstream molecular structure prediction. This skill is the foundational signal-processing stage in end-to-end NMR structure elucidation.

## When to use

Apply this skill when you have preprocessed 1D NMR spectra (¹H and/or ¹³C) and need to extract spectral features for molecular structure inference on molecules with up to 19 heavy atoms. The skill is necessary as the first stage before fragment assembly or connectivity prediction; use it whenever raw spectral data must be converted into a compact learned representation that captures resonance patterns and peak relationships.

## When NOT to use

- Input spectra are not preprocessed (contain baseline artifacts, uncalibrated chemical shift axes, or extreme outliers) — preprocessing must occur before CNN feature extraction.
- Molecules exceed 19 heavy atoms — the framework has not been validated beyond this scope and model capacity may be insufficient.
- The goal is to extract explicit peak lists or chemical shift assignments manually — use traditional peak-picking algorithms instead; CNN extraction is for end-to-end learned feature representation, not human-readable peak tables.

## Inputs

- Preprocessed 1D ¹H NMR spectrum (1D array: chemical shift bins × intensity values)
- Preprocessed 1D ¹³C NMR spectrum (1D array: chemical shift bins × intensity values)
- CNN model with pretrained weights (h5, .pt, or equivalent serialized format)

## Outputs

- CNN-encoded feature tensor (fixed-size multidimensional array representing learned spectral representation)
- Intermediate activation maps (optional; useful for interpretability)

## How to apply

Load the preprocessed NMR spectrum (1D array of chemical shift and intensity values for ¹H and/or ¹³C) and pass it through a convolutional neural network initialized with pretrained weights. The CNN learns local spectral patterns (peak shapes, multiplet structures, chemical shift clusters) through convolutional layers and progressively encodes them into fixed-size feature vectors. The output feature tensor becomes the input to a transformer architecture for subsequent molecular assembly. Validate extraction by confirming: (1) the output feature dimension matches the model's expected transformer input size, (2) feature activations are non-degenerate (not all zero or constant), and (3) the extracted features preserve discriminative information (verified indirectly through downstream structure prediction accuracy).

## Related tools

- **Convolutional Neural Network (CNN)** (Feature extraction backbone; encodes spectral intensity patterns into learned representations via learned convolutional filters and pooling layers)
- **Transformer architecture** (Downstream consumer of CNN-extracted features; receives encoded spectral representation and performs molecular fragment assembly and connectivity prediction)

## Evaluation signals

- CNN output feature shape matches transformer input expectation (e.g., batch_size × feature_dim); schema validation confirms non-null tensors.
- Feature activations across the batch show non-zero variance; statistical summary (mean, std, min, max per feature channel) indicates learned differentiation between spectra.
- End-to-end structure prediction accuracy on held-out test molecules is consistent with reported benchmarks (structure similarity scores or F1 on molecular formula and connectivity).
- Ablation: features extracted from CNN produce higher structure prediction accuracy than hand-crafted spectral descriptors (peak counts, intensity ratios, shift ranges), validating that learned representations capture nonlinear spectral patterns.
- Gradient analysis: backpropagation through CNN shows that convolutional filters learn interpretable local spectral patterns (peak shape kernels, chemical shift cluster detectors) rather than noise.

## Limitations

- Scope restricted to molecules with ≤19 heavy atoms; tradeoff between model capacity and feasible molecular structure space was not systematically explored for larger molecules.
- Requires preprocessed spectra (baseline correction, peak normalization, chemical shift calibration); CNN feature extraction quality is entirely dependent on input data quality and preprocessing fidelity.
- No explicit uncertainty quantification on features; confidence in extracted representations is inferred only through downstream structure prediction metrics, not directly from feature statistics.
- Pretrained weights are dataset-specific; transfer learning or fine-tuning to new spectral acquisition protocols, solvent conditions, or NMR instruments may require retraining or substantial hyperparameter adjustment.

## Evidence

- [intro] CNN-encoded spectral features as foundational stage: "Feed NMR spectra through the convolutional neural network feature extraction layer to encode spectral information."
- [intro] CNN-transformer integration for structure prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra that is fast and accurate"
- [intro] Scope limitation: ≤19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] CNN as feature extraction before transformer assembly: "Pass CNN-encoded features to the transformer architecture to assemble molecular fragments and predict connectivity and molecular formula."
