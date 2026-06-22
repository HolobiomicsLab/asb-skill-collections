---
name: molecular-structure-prediction-from-spectra
description: Use when you have preprocessed 1D ¹H and/or ¹³C NMR spectra (as numerical arrays or feature tensors) from an unknown organic compound with ≤19 heavy atoms, and you need to predict both the molecular formula and the connectivity graph of the compound without prior structural hypotheses or reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-prediction-from-spectra

## Summary

Predict molecular structure (formula and connectivity) from routine 1D ¹H and/or ¹³C NMR spectra using an end-to-end CNN–transformer model. This skill is applicable to small organic molecules with up to 19 heavy atoms, where traditional manual interpretation becomes intractable.

## When to use

Apply this skill when you have preprocessed 1D ¹H and/or ¹³C NMR spectra (as numerical arrays or feature tensors) from an unknown organic compound with ≤19 heavy atoms, and you need to predict both the molecular formula and the connectivity graph of the compound without prior structural hypotheses or reference databases.

## When NOT to use

- Input molecules have >19 heavy atoms: the model was trained and evaluated only on molecules up to 19 heavy atoms; extrapolation to larger structures is not supported.
- Input is 2D NMR (COSY, HSQC, HMBC) or multi-dimensional spectra: this skill operates on 1D ¹H and/or ¹³C spectra only.
- Spectra are not preprocessed or are in raw instrumental format (e.g., unphased, uncalibrated, or contain systematic artifacts): the workflow assumes spectra are already normalized and formatted as numerical tensors suitable for CNN input.

## Inputs

- 1D ¹H NMR spectrum (preprocessed array or tensor)
- 1D ¹³C NMR spectrum (preprocessed array or tensor)
- Ground-truth molecular structure (connectivity graph and formula, optional for evaluation)
- Pretrained CNN–transformer model weights

## Outputs

- Predicted molecular formula (elemental composition)
- Predicted molecular connectivity graph (atoms and bonds)
- Structure similarity scores or match confidence per molecule
- Evaluation metrics (accuracy, F1-score, structure matching scores)

## How to apply

Load the NMR spectra (¹H and/or ¹³C) as preprocessed numerical arrays and initialize a pretrained multitask CNN–transformer model with weights. Pass spectra through the CNN feature extraction layer to encode spectral information into a latent representation. Feed the CNN-encoded features into the transformer decoder to iteratively assemble molecular fragments and predict molecular formula and connectivity. Generate predicted structures for all test molecules and compare against ground truth using structure matching metrics (e.g., exact match, substructure overlap, or graph edit distance). Log evaluation metrics (accuracy, F1-score, structure similarity scores) and confidence scores for each prediction. The rationale is that CNNs efficiently capture local spectral patterns (peaks, multiplicities, coupling constants) while transformers resolve the combinatorially hard problem of assembling fragments into valid structures given the spectral constraints.

## Related tools

- **Convolutional Neural Network (CNN)** (Feature extraction from 1D NMR spectra; encodes spectral information into latent representations for downstream fragment assembly)
- **Transformer architecture** (Assembles CNN-encoded spectral features into molecular fragments and predicts connectivity and molecular formula via sequence-to-graph decoding)

## Evaluation signals

- Predicted molecular formula matches ground truth (exact match on atomic composition).
- Predicted connectivity graph matches ground truth using graph isomorphism or edit distance metrics (0 edit distance = perfect match).
- Structure similarity score (e.g., Tanimoto or other graph-based metric) is ≥0.9 for valid predictions on held-out test molecules.
- Confidence scores are well-calibrated: high-confidence predictions (e.g., top 10%) have >90% accuracy; low-confidence predictions show lower accuracy proportionally.
- Evaluation on molecules with ≤19 heavy atoms shows accuracy and F1-score consistent with those reported in the article (no significant drop on out-of-distribution test sets).

## Limitations

- Scope limited to molecules with ≤19 heavy atoms; performance on larger molecules is not characterized.
- Model trained on 1D ¹H and/or ¹³C spectra; does not exploit 2D correlations (COSY, HSQC, HMBC) that may resolve structural ambiguities in complex molecules.
- Requires high-quality preprocessed spectra; sensitivity to phase errors, calibration drift, or baseline distortions is not quantified.
- Transformer decoder generates structures via fragment assembly; validity of predicted structures (e.g., valence, aromaticity, chemical feasibility) depends on training data distribution and decoder constraints.

## Evidence

- [intro] multitask_learning_framework_definition: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [intro] transformer_fragment_assembly: "we show how a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [intro] cnn_transformer_integration: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra that is fast and accurate"
- [intro] scope_heavy_atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [other] workflow_steps: "1. Load preprocessed NMR spectra (¹H and/or ¹³C) and corresponding molecular structure ground truth from the evaluation dataset. 2. Initialize the multitask CNN+transformer model with pretrained"
