---
name: model-generalization-assessment-across-molecular-size-regimes
description: Use when a deep learning model for molecular structure prediction (e.g., NMR2Struct) has been trained and evaluated on a limited molecular size range (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - NMR2Struct
  - PubChem or equivalent chemical database
  - NMR spectrum simulator or experimental database
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
---

# model-generalization-assessment-across-molecular-size-regimes

## Summary

This skill assesses whether a trained structure-prediction model maintains accuracy when applied to molecules outside its training scope, specifically testing generalization across molecular size regimes. It quantifies performance degradation and failure modes when the model encounters out-of-scope inputs, establishing empirical boundaries on model applicability.

## When to use

Apply this skill when a deep learning model for molecular structure prediction (e.g., NMR2Struct) has been trained and evaluated on a limited molecular size range (e.g., up to 19 heavy atoms), and you need to determine whether predictions remain reliable for larger or smaller molecules, or when deploying the model on real-world samples of unknown size distribution.

## When NOT to use

- The model has not yet been trained or validated on any in-scope molecules—use this skill only after establishing a baseline on the design training scope.
- Input molecules are already within the characterized scope (≤19 heavy atoms for NMR2Struct)—apply standard validation metrics instead.
- Ground-truth connectivity labels are unavailable for out-of-scope test molecules—accuracy cannot be computed without reference structures.

## Inputs

- pretrained NMR2Struct checkpoint (transformer + CNN architecture)
- held-out test set of molecules exceeding training scope (molecular graphs with connectivity labels)
- 1D ¹H NMR spectra (simulated or experimental)
- 1D ¹³C NMR spectra (simulated or experimental)

## Outputs

- top-1, top-3, and top-5 structure recovery accuracy metrics for out-of-scope molecules
- predicted molecular formulas and connectivity graphs ranked by model confidence score
- absolute and relative accuracy degradation versus in-scope baseline
- error distribution and failure mode analysis report
- summary document establishing empirical performance boundaries

## How to apply

Load the pretrained checkpoint and construct a held-out test set of molecules exceeding the known training scope (e.g., >19 heavy atoms for NMR2Struct), with ground-truth connectivity labels from PubChem or equivalent databases. Generate or retrieve 1D ¹H and/or ¹³C NMR spectra for each out-of-scope molecule via simulation or experimental sources. Feed each spectrum through the model's end-to-end pipeline (CNN preprocessor + transformer fragment assembler) and capture predicted molecular formulas and connectivity graphs ranked by confidence score. Compute top-1, top-3, and top-5 structure recovery accuracy (the fraction of predictions with correct connectivity) for the out-of-scope set. Directly compare these metrics against the reported in-scope baseline using absolute difference and relative degradation percentages. Document the accuracy loss distribution, identify systematic failure modes (e.g., connectivity errors in specific functional groups), and produce a summary report quantifying the performance cliff.

## Related tools

- **NMR2Struct** (end-to-end transformer + CNN model for predicting molecular structure (formula and connectivity) from 1D NMR spectra; checkpoint must be loaded to generate predictions on out-of-scope molecules)
- **PubChem or equivalent chemical database** (source of ground-truth molecular structures and connectivity graphs for out-of-scope test molecules)
- **NMR spectrum simulator or experimental database** (generates or retrieves 1D ¹H and ¹³C NMR spectra for molecules in the out-of-scope test set)

## Evaluation signals

- Top-1, top-3, and top-5 accuracy metrics for out-of-scope molecules are computed and reported with clear numerators and denominators (e.g., 45/100 correct for top-1).
- Absolute difference in accuracy between out-of-scope and in-scope baseline is quantified (e.g., 'in-scope baseline: 92%, out-of-scope: 68%, degradation: 24 percentage points').
- Relative degradation is expressed as a percentage loss from baseline (e.g., '26% relative accuracy loss beyond 19 heavy atoms').
- Error distribution is analyzed by failure category (e.g., molecular formula errors vs. connectivity errors, errors stratified by number of heavy atoms).
- Confidence score distributions are compared between correct and incorrect predictions to identify whether the model's internal confidence correlates with actual accuracy on out-of-scope inputs.

## Limitations

- The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms; generalization beyond this scope is uncharacterized and likely to degrade significantly.
- Accuracy is only measurable for out-of-scope molecules with available ground-truth connectivity labels; real-world deployment may lack reference structures.
- The transformer architecture's ability to assemble molecular fragments into correct connectivity may be fundamentally limited by the compositional complexity of larger molecules, which were underrepresented or absent from training.
- NMR spectrum quality (resolution, signal-to-noise ratio) varies by acquisition method (simulation vs. experimental); degradation may partly reflect spectrum quality rather than pure model generalization limits.

## Evidence

- [intro] Framework performance boundary: "The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized."
- [intro] Top-K accuracy metric definition: "compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity)"
- [intro] Transformer architecture role: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] Multitask learning framework scope: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] End-to-end prediction pipeline: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
