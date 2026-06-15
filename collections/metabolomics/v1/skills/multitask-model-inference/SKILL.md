---
name: multitask-model-inference
description: Use when you have a trained multitask model checkpoint and preprocessed spectral inputs (1D NMR spectra, 1H-only, 13C-only, or combined 1H+13C), and you need to generate simultaneous predictions of molecular formula and connectivity structure to quantify modality contributions, compare single vs..
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3379
  - http://edamontology.org/topic_0625
  tools:
  - convolutional neural network encoder
  - transformer architecture
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

# multitask-model-inference

## Summary

Run inference on a trained multitask machine learning model to predict multiple correlated outputs (e.g., molecular formula and connectivity) from a single input modality or multiple fused input modalities. This skill applies a pre-trained CNN–transformer pipeline to generate structured predictions suitable for comparative multimodal analysis.

## When to use

You have a trained multitask model checkpoint and preprocessed spectral inputs (1D NMR spectra, 1H-only, 13C-only, or combined 1H+13C), and you need to generate simultaneous predictions of molecular formula and connectivity structure to quantify modality contributions, compare single vs. combined input performance, or measure end-to-end recovery accuracy on a held-out test set.

## When NOT to use

- Input spectra have not been preprocessed or normalized to model input shape and spectral resolution.
- Test molecules contain >19 heavy atoms, which exceeds the demonstrated scope of the trained model.
- You need to train or fine-tune the model; this skill is for inference only on a fixed checkpoint.

## Inputs

- trained model checkpoint (NMR2Struct)
- preprocessed 1D 1H NMR spectra (test set, ≤19 heavy atoms)
- preprocessed 1D 13C NMR spectra (test set, ≤19 heavy atoms)
- ground-truth molecular structures (SMILES or molecular graph format)

## Outputs

- predicted molecular formula (per-sample)
- predicted molecular connectivity / graph structure (per-sample)
- exact-match accuracy metrics by modality
- error distribution and performance gap statistics
- graph edit distance or connectivity F1 scores

## How to apply

Load the trained NMR2Struct model checkpoint and organize test spectra into separate input batches according to your modality condition (1H-only, 13C-only, or combined 1H+13C). Pass each batch through the convolutional neural network encoder to extract spectral features, then feed the encoded representations into the transformer architecture to perform joint prediction of molecular formula and connectivity. Run inference on all test molecules (≤19 heavy atoms) and collect structure predictions for each modality. Compare exact-match accuracy for formula and graph-based metrics (e.g., graph edit distance or connectivity F1 score) across modality conditions. For multimodal studies, compute joint contribution by subtracting single-modality baseline accuracies from combined 1H+13C accuracy to quantify synergy or redundancy.

## Related tools

- **convolutional neural network encoder** (extracts spectral features from 1D NMR input prior to transformer assembly)
- **transformer architecture** (assembles molecular fragments and predicts connectivity and formula from encoded spectral features)

## Evaluation signals

- Exact-match accuracy for predicted molecular formula matches reported test-set performance (e.g., >90% on molecules ≤19 heavy atoms).
- Graph edit distance or connectivity F1 scores are consistent with or exceed baseline single-modality performance.
- Combined 1H+13C accuracy is ≥ max(1H-only accuracy, 13C-only accuracy), indicating non-negative synergy.
- Prediction outputs (formula + connectivity) are valid and correspond to chemically feasible molecules.
- Error distribution (false negatives, near-misses) is traceable to input spectral ambiguity rather than model failure.

## Limitations

- Model is trained on and evaluated for molecules with ≤19 heavy atoms; accuracy is not established for larger molecules.
- Combinatorial explosion of possible molecular structures makes error analysis and failure mode diagnosis challenging even with good accuracy metrics.
- Single-modality (1H-only or 13C-only) performance is inherently lower than combined input; synergy gain depends on spectral complementarity.
- Inference assumes identical preprocessing (normalization, windowing, feature extraction) as training; deviations may degrade performance unpredictably.

## Evidence

- [intro] transformer architecture and CNN for end-to-end NMR-to-structure prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] multitask prediction of formula and connectivity: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] scope limited to ≤19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] inference workflow: CNN encoder then transformer assembly: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] model accuracy and speed from end-to-end prediction: "An end-to-end multitask machine learning model integrating a convolutional neural network with a transformer architecture can predict molecular structure from 1D NMR spectra and is fast and accurate"
