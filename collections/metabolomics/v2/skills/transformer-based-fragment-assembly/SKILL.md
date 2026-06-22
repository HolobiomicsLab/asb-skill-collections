---
name: transformer-based-fragment-assembly
description: Use when when you have CNN-encoded spectral features (¹H and/or ¹³C NMR) and a set of predicted or candidate molecular fragments, and you need to determine which fragments are present and how they connect to form a valid molecular structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3382
  tools:
  - Convolutional Neural Network (CNN)
  - Transformer
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- Integrating this capability with a convolutional neural network, we build an end-to-end model
- a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular
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

# transformer-based-fragment-assembly

## Summary

Use a transformer architecture to assemble predicted molecular fragments into complete molecular structures (formula and connectivity) from spectral feature encodings. This skill is essential when the input space (trillions of possible structures up to 19 heavy atoms) requires efficient sequential reasoning over fragment dependencies rather than brute-force enumeration.

## When to use

When you have CNN-encoded spectral features (¹H and/or ¹³C NMR) and a set of predicted or candidate molecular fragments, and you need to determine which fragments are present and how they connect to form a valid molecular structure. Specifically: the molecules are small enough that fragment assembly is feasible (≤19 heavy atoms), you have a pretrained fragment vocabulary, and the connectivity graph is not known a priori.

## When NOT to use

- When molecules have >19 heavy atoms; the framework is only demonstrated to be effective up to 19 heavy atoms.
- When spectral preprocessing or feature extraction has not been completed; the transformer expects CNN-encoded features, not raw spectra.
- When no pretrained fragment vocabulary or transformer weights are available; training from scratch requires substantial paired NMR + structure data.

## Inputs

- CNN-encoded spectral feature tensor (output of convolutional layer processing 1H and/or 13C NMR spectra)
- Pretrained transformer model weights
- Molecular fragment vocabulary (list of valid fragments with attachment points)
- Validation rules (valence constraints, aromaticity rules)

## Outputs

- Predicted molecular structure (formula and connectivity graph)
- Confidence score for each predicted structure
- Top-k candidate structures with confidence rankings

## How to apply

Initialize the transformer with pretrained weights trained on the same NMR + structure dataset. Pass the CNN-encoded spectral features as the initial context to the transformer decoder. The transformer then autoregressively predicts a sequence of molecular fragments and their assembly rules (e.g., bond types, attachment points) by attending over both the spectral encoding and previously predicted fragments. Use beam search or greedy decoding to generate candidate structures. Validate each predicted structure for chemical feasibility (valence, aromaticity rules) and rank by transformer confidence scores. Select the top-ranked structure that passes validation, or return the top-k candidates with confidence estimates for manual review.

## Related tools

- **Convolutional Neural Network (CNN)** (Feature extraction layer that encodes spectral information into dense vectors passed to the transformer)
- **Transformer** (Sequence-to-sequence architecture that assembles molecular fragments into full structures by attending over spectral encodings and previously predicted fragments)

## Evaluation signals

- Structure matching metrics (e.g., Tanimoto similarity, exact graph isomorphism) between predicted and ground-truth structures should exceed a task-specific threshold (article does not specify exact threshold, but reports overall accuracy and F1-score).
- Predicted molecular formula matches the ground truth (atomic count and element composition are correct).
- Predicted connectivity graph is chemically valid: all atoms satisfy valence rules and formal charges sum to zero.
- Confidence scores are well-calibrated: high-confidence predictions have higher match rates than low-confidence predictions.
- Beam search or greedy decoding terminates successfully without diverging or generating incomplete structures.

## Limitations

- Framework is validated only on molecules with up to 19 heavy atoms; applicability to larger molecules is unknown.
- Performance depends critically on the quality and diversity of the training dataset; out-of-distribution molecules or spectra may yield poor predictions.
- Transformer requires large paired datasets of NMR spectra and ground-truth structures for pretraining; no transfer learning between different NMR instruments or solvent conditions is demonstrated.
- The method predicts structure from 1D spectra alone; 2D NMR (COSY, HSQC) and other complementary techniques are not incorporated.

## Evidence

- [intro] We show how a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra that is fast and accurate: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [other] Pass CNN-encoded features to the transformer architecture to assemble molecular fragments and predict connectivity and molecular formula: "Pass CNN-encoded features to the transformer architecture to assemble molecular fragments and predict connectivity and molecular formula"
