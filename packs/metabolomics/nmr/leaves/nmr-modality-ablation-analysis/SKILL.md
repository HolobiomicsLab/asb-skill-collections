---
name: nmr-modality-ablation-analysis
description: Use when you have a trained multitask machine learning model for structure prediction, test set molecules with paired ¹H and ¹³C NMR spectra, and need to understand the marginal contribution of each NMR modality or justify multimodal input design.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Convolutional Neural Network (CNN) encoder
  - Transformer architecture
  - NMR2Struct multitask framework
  techniques:
  - NMR
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

# nmr-modality-ablation-analysis

## Summary

Systematically evaluate the individual and joint contributions of ¹H NMR, ¹³C NMR, and combined 1D NMR inputs to molecular structure prediction accuracy by running inference under each modality condition independently and comparing performance metrics. This skill isolates which spectroscopic modalities drive structure elucidation performance and quantifies synergy between them.

## When to use

Apply this skill when you have a trained multitask machine learning model for structure prediction, test set molecules with paired ¹H and ¹³C NMR spectra, and need to understand the marginal contribution of each NMR modality or justify multimodal input design. Use it when stakeholders ask 'which NMR experiment is actually necessary?' or when you suspect one modality is redundant with the other.

## When NOT to use

- Input lacks paired ¹H and ¹³C NMR spectra for the same molecules (modality ablation requires both modalities present to be meaningful).
- The model is not yet trained or checkpoint is not available; ablation analysis requires a frozen, fixed model.
- Goal is to optimize model architecture or hyperparameters; this skill measures performance, not tunes the model.

## Inputs

- Trained NMR2Struct model checkpoint (weights and architecture)
- Test set molecular structures (SMILES or graph representation)
- ¹H NMR spectra (CNN-compatible tensor, e.g., shape [batch, channels, frequency_bins])
- ¹³C NMR spectra (CNN-compatible tensor, same shape as ¹H)
- Ground truth molecular formula and connectivity labels

## Outputs

- Per-modality accuracy metrics (exact-match formula accuracy, structure connectivity F1 or graph edit distance)
- Modality-specific error distribution (confusion matrix by atom type, bond type, molecular weight bins)
- Synergy quantification (combined accuracy minus single-modality baseline)
- Tabulated results by modality showing accuracy, error gaps, and per-molecule predictions
- Comparison summary (which modality(s) dominate for different structural classes)

## How to apply

Load the trained NMR2Struct model checkpoint and prepare the test set with aligned molecular ground truth labels and corresponding ¹H and ¹³C NMR spectra. Create three separate inference batches: (1) ¹H-only spectra masked to zeros in ¹³C channels, (2) ¹³C-only spectra masked to zeros in ¹H channels, and (3) both modalities combined. Run the convolutional neural network encoder and transformer decoder on each batch independently, generating molecular formula and connectivity predictions for each condition. Compute accuracy metrics (exact-match accuracy for formula, graph edit distance or connectivity F1 for structure) separately for each modality. Quantify synergy by subtracting the maximum single-modality accuracy from the combined accuracy; compare error distributions across conditions to identify which structural features (connectivity, functional groups, molecular weight) each modality resolves best. Tabulate results by modality with accuracy, confidence intervals, and per-molecule error analysis.

## Related tools

- **Convolutional Neural Network (CNN) encoder** (Encodes raw 1D NMR spectra (¹H and/or ¹³C) into learned feature representations for transformer input)
- **Transformer architecture** (Decodes CNN feature representations and assembled molecular fragments into predicted structure (formula and connectivity))
- **NMR2Struct multitask framework** (End-to-end model combining CNN encoder and transformer decoder for structure prediction from 1D NMR)

## Evaluation signals

- Exact-match accuracy for predicted molecular formula matches ground truth for ≥80% of test molecules in single-modality and combined conditions.
- Synergy value (combined minus best single-modality accuracy) is non-negative and quantifies the benefit of multimodal input; if synergy ≈ 0, modalities are redundant.
- Error distribution differs qualitatively across modalities (e.g., ¹H alone fails on isomers with identical ¹H shifts but different ¹³C shifts, while ¹³C alone struggles with quaternary carbons); this confirms complementarity.
- Graph edit distance or connectivity F1 score for structure prediction increases monotonically from single modalities to combined input across molecule classes.
- Per-molecule predictions show same connectivity for all three conditions on molecules where the model achieves high confidence; large disagreements flag ambiguous spectra or modality-specific artifacts.

## Limitations

- Ablation measures marginal contribution but does not explain which spectroscopic features (e.g., splitting patterns, chemical shift ranges) drive predictions; interpretation requires additional feature attribution analysis.
- Performance reported on molecules with up to 19 heavy atoms; ablation results may not generalize to larger structures or rare functional groups outside the training distribution.
- Masking one modality to zeros assumes independence; in a real multitask model, the two modalities may share learned representations in early layers, so true single-modality performance may differ from zero-masking.
- Exact-match accuracy is a strict metric; two predictions differing by a single atom or bond will be marked as failure, potentially underestimating practical utility of lower-accuracy modality combinations.

## Evidence

- [intro] multitask machine learning framework capable of predicting molecular structure using 1D ¹H NMR, ¹³C NMR, or both modalities combined as input: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [intro] transformer architecture assembles molecular fragments into structures; CNN encodes spectra: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] CNN and transformer integrated for end-to-end prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] 1D NMR structure elucidation is challenging due to combinatorial explosion: "elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion"
- [intro] Framework tested on molecules up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
