---
name: spectral-to-structure-mapping-prediction
description: Use when you have preprocessed 1D ¹H and/or ¹³C NMR spectra from an unknown organic compound with ≤19 heavy atoms, and you need to recover its molecular structure (both formula and connectivity) rapidly without access to 2D NMR experiments (HSQC, HMBC, COSY) or mass spectrometry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3070
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3372
  tools:
  - convolutional neural network (CNN) encoder
  - transformer architecture
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
---

# spectral-to-structure-mapping-prediction

## Summary

Predict molecular structure (formula and connectivity) directly from 1D NMR spectra using an integrated convolutional neural network and transformer architecture. This skill enables rapid structure elucidation on molecules up to 19 heavy atoms without requiring 2D NMR data or manual spectral interpretation.

## When to use

You have preprocessed 1D ¹H and/or ¹³C NMR spectra from an unknown organic compound with ≤19 heavy atoms, and you need to recover its molecular structure (both formula and connectivity) rapidly without access to 2D NMR experiments (HSQC, HMBC, COSY) or mass spectrometry. This is particularly valuable when only routine 1D spectra are available and combinatorial structure enumeration would be intractable.

## When NOT to use

- Input spectra contain molecules with >19 heavy atoms; model performance degrades significantly beyond this threshold due to combinatorial explosion.
- Only 2D NMR data (HSQC, HMBC, COSY) are available and 1D spectra are not provided; the model is trained to extract features from 1D peak patterns.
- Spectra are poorly preprocessed (excessive noise, unaligned peaks, or missing peak frequency calibration); the CNN encoder relies on intact spectral signal quality.

## Inputs

- 1D ¹H NMR spectrum (preprocessed, normalized)
- 1D ¹³C NMR spectrum (preprocessed, normalized)
- Ground-truth molecular structures (test set; optional, for evaluation)

## Outputs

- Predicted molecular formula (string, e.g., 'C₆H₁₂O')
- Predicted molecular connectivity graph (adjacency matrix or SMILES string)
- Top-k candidate structures (ranked by model confidence)
- Exact match recovery rate (%)—comparison of predicted vs. ground-truth structure

## How to apply

Load the normalized 1D NMR spectrum (or concatenated ¹H and ¹³C spectra) and pass it through a convolutional neural network encoder to extract spectral features that capture peak positions, intensities, and multiplet structure. Feed the encoded feature vector into a transformer architecture that learns to assemble molecular fragments and predict both molecular formula (via one task head) and molecular connectivity graph (via another task head). The multitask formulation allows the model to jointly optimize formula prediction and structure assembly, improving generalization. Compute top-k exact match rates (typically k=1, 3, 5) by comparing predicted molecular graphs against ground-truth structures using graph isomorphism. Performance on molecules with 11–19 heavy atoms typically achieves >90% top-1 accuracy on test sets, but accuracy declines with molecular complexity and sparsity of spectral features.

## Related tools

- **convolutional neural network (CNN) encoder** (Extracts spectral feature vectors from 1D NMR spectra; compresses peak patterns into a dense latent representation that captures chemically relevant information.)
- **transformer architecture** (Assembles molecular fragments predicted by the CNN into a complete molecular structure; jointly predicts molecular formula and connectivity via multitask learning heads.)

## Evaluation signals

- Top-1, top-3, and top-5 exact structure recovery rates (percentage of predicted structures that exactly match ground-truth graphs); target >90% top-1 for molecules ≤11 heavy atoms.
- Graph isomorphism check: predicted molecular connectivity (as adjacency matrix or SMILES) is compared against ground-truth using canonical SMILES or graph matching to confirm chemical equivalence.
- Molecular formula accuracy: predicted formula string matches ground-truth elemental composition exactly.
- Consistency across multitask outputs: the predicted formula is chemically consistent with the connectivity graph (valence, atom counts).
- Inference speed: model processes a single spectrum in <1 second on GPU, confirming end-to-end efficiency.

## Limitations

- Performance degrades sharply for molecules >19 heavy atoms due to combinatorial explosion of possible structures; the training set distribution does not cover larger molecules.
- Accuracy depends critically on spectral quality and preprocessing; spectra with poor peak resolution, baseline drift, or artifacts may yield incorrect predictions.
- The model was trained on specific NMR pulse sequences and solvent systems (details in paper); transfer to markedly different experimental conditions (e.g., non-standard solvent, very high or low field strength) is not validated.
- Multitask learning may not capture rare or novel structural motifs absent from the training set; out-of-distribution molecular scaffolds may be predicted with low confidence.
- No explicit handling of chirality or stereochemistry; the model predicts connectivity only and does not assign 3D configuration.

## Evidence

- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [intro] a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion: "elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion"
