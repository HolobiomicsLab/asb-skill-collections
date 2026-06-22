---
name: molecular-connectivity-inference
description: Use when you have 1D ¹H and/or ¹³C NMR spectra (as preprocessed numerical arrays or peak lists) from an unknown organic molecule with ≤19 heavy atoms, and you need to recover its molecular formula and connectivity graph.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
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

# molecular-connectivity-inference

## Summary

Predict molecular formula and bond connectivity from 1D ¹H and/or ¹³C NMR spectra using an integrated CNN–transformer model. This skill recovers the complete molecular structure (atoms and bonds) from routine spectroscopic data for molecules up to 19 heavy atoms, automating a task traditionally performed by manual spectral interpretation.

## When to use

You have 1D ¹H and/or ¹³C NMR spectra (as preprocessed numerical arrays or peak lists) from an unknown organic molecule with ≤19 heavy atoms, and you need to recover its molecular formula and connectivity graph. This skill is appropriate when spectral interpretation by hand is labor-intensive or when you require systematic, reproducible structure assignment at scale across a dataset of spectra.

## When NOT to use

- Input molecules have >19 heavy atoms; the model's training and evaluation scope does not extend beyond this regime, and extrapolation may be unreliable.
- Spectra are multidimensional (2D COSY, HSQC, HMBC); this skill addresses 1D spectra only.
- Input spectra are low-quality, poorly phased, or contain severe artifacts; preprocessing quality is assumed to be adequate before model input.

## Inputs

- preprocessed 1D ¹H NMR spectrum (numerical array or peak tensor)
- preprocessed 1D ¹³C NMR spectrum (numerical array or peak tensor)
- ground truth molecular structure (molecular formula and connectivity matrix, for evaluation)

## Outputs

- predicted molecular formula (element counts)
- predicted connectivity matrix or bond graph
- prediction confidence scores per structure
- evaluation metrics (accuracy, F1-score, structure similarity scores)

## How to apply

Load the preprocessed NMR spectra (¹H and/or ¹³C) as input tensors. Initialize a multitask CNN–transformer model with pretrained weights. Feed spectra through the convolutional neural network to extract and encode spectral features into a latent representation. Pass the CNN-encoded features to a transformer module that treats molecular structure prediction as a sequence assembly task: the transformer learns to iteratively predict molecular fragments and their connectivity to reconstruct the full structure. Generate predicted molecular formulas and connectivity matrices for all test molecules. Compare predictions against ground truth using structure matching metrics (e.g., exact structure match, substructure similarity). Compute accuracy, F1-score, and structure similarity scores to assess prediction quality. The rationale is that CNNs efficiently capture local spectral patterns (peak positions, multiplicities, coupling), while transformers excel at long-range reasoning over fragment assembly and connectivity constraints.

## Related tools

- **Convolutional Neural Network (CNN)** (Feature extraction module that encodes 1D NMR spectral signals into latent representations capturing local peak patterns and chemical shifts)
- **Transformer** (Sequence-to-structure decoder that assembles molecular fragments from CNN-encoded spectral features and predicts molecular connectivity and formula through attention-based fragment reasoning)

## Evaluation signals

- Exact structure match: predicted connectivity and formula match ground truth molecular structure.
- Structure similarity score (e.g., Tanimoto similarity on molecular fingerprints or graph edit distance) meets or exceeds a target threshold (>0.90 typical for near-duplicate structures).
- F1-score on atom and bond predictions is computed and reported; precision and recall should both be >0.85 for reliable predictions.
- Confidence scores exhibit appropriate calibration: high-confidence predictions (>0.9) have low error rates, low-confidence predictions (<0.5) are flagged for manual review.
- Predictions on held-out test molecules scale reproducibly; results are deterministic (seeded) and do not degrade with batch reprocessing.

## Limitations

- Model is evaluated and effective only on molecules with up to 19 heavy (non-hydrogen) atoms; performance on larger structures is unknown.
- Predictions depend critically on input spectra being preprocessed consistently (peak picking, phasing, baseline correction); poor-quality spectra will degrade predictions.
- Model assumes access to either ¹H or ¹³C spectra or both; predictions from incomplete or missing spectral data (e.g., only partial chemical shift information) have not been explicitly characterized.
- Trillions of possible structures exist in the search space for 19-atom molecules; the model is not guaranteed to enumerate or rank all isomers, only to predict the most likely structure given the spectral evidence.

## Evidence

- [intro] multitask machine learning framework predicts molecular structure: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D ¹H and/or ¹³C NMR spectra"
- [intro] transformer assembles molecular fragments: "we show how a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [intro] CNN–transformer integration for fast accurate prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra that is fast and accurate"
- [intro] effectiveness on molecules up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
