---
name: molecular-structure-prediction-evaluation
description: Use when you have trained a multitask NMR-to-structure model and need
  to quantify its predictive accuracy on held-out test molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3315
  tools:
  - convolutional neural network encoder
  - transformer architecture
  - NMR2Struct model
  techniques:
  - NMR
  license_tier: restricted
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

# molecular-structure-prediction-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate the accuracy and performance of machine learning models predicting molecular structures from NMR spectra by computing exact-match and graph-based metrics across different spectroscopic modalities and complexity ranges. This skill validates whether the multitask learning framework correctly infers molecular formula and connectivity from 1D ¹H NMR, ¹³C NMR, or combined spectral inputs.

## When to use

Apply this skill when you have trained a multitask NMR-to-structure model and need to quantify its predictive accuracy on held-out test molecules. Use it specifically when you want to isolate the individual contributions of ¹H NMR vs. ¹³C NMR vs. combined inputs, or when assessing whether performance scales appropriately across molecules of different sizes (up to ~19 heavy atoms). Trigger this skill after model inference has produced candidate molecular formulas and connectivity predictions.

## When NOT to use

- Model has not yet been trained or checkpoint does not exist; use model training or hyperparameter optimization first.
- Input spectra are 2D (COSY, HSQC, HMBC) rather than 1D (¹H, ¹³C); this skill is designed exclusively for 1D modalities.
- Test set molecules contain more than ~19 heavy atoms; the framework was demonstrated only up to this size and extrapolation accuracy is not established.

## Inputs

- trained NMR2Struct model checkpoint (PyTorch or equivalent)
- test set molecular structures with canonical SMILES or graph representations
- ¹H NMR spectra (1D arrays or CNN-compatible spectral format)
- ¹³C NMR spectra (1D arrays or CNN-compatible spectral format)
- ground truth molecular formulas (e.g., C₁₀H₁₂O₂)
- ground truth molecular connectivity (adjacency matrices or bond lists)

## Outputs

- exact-match accuracy scores for molecular formula (per modality and combined)
- graph edit distance or connectivity F1-score (per modality and combined)
- synergy metric: (combined accuracy) − max(¹H accuracy, ¹³C accuracy)
- error distribution and misclassification counts (per modality)
- performance stratification by molecular complexity (atom count bins, ring count, branching)
- tabulated results showing accuracy, error type, and performance gaps

## How to apply

Load the trained NMR2Struct model checkpoint and a test set containing molecular structures paired with their ¹H and ¹³C NMR spectra. Prepare three separate inference batches: one using only ¹H NMR inputs, one using only ¹³C NMR inputs, and one using both modalities combined with identical ground truth labels. Run the convolutional neural network encoder followed by the transformer architecture on each modality condition to generate structure predictions (molecular formula and connectivity). Compute accuracy metrics for each: exact-match accuracy for molecular formula and graph edit distance or connectivity F1-score for structure topology. Compare accuracies across the three conditions and calculate synergy by subtracting single-modality baselines from the combined (¹H+¹³C) accuracy. Stratify results by molecular complexity (atom count, branching, ring systems) to identify performance gaps and error patterns.

## Related tools

- **convolutional neural network encoder** (processes raw 1D NMR spectral inputs into learned feature representations)
- **transformer architecture** (assembles molecular fragments (decoded from CNN features) into candidate molecular structures using attention mechanisms)
- **NMR2Struct model** (end-to-end multitask framework combining CNN encoder and transformer fragment assembler for structure prediction from 1D NMR)

## Evaluation signals

- Exact-match accuracy for molecular formula should be reported separately for ¹H-only, ¹³C-only, and combined conditions; combined condition should meet or exceed single-modality baseline.
- Graph edit distance or F1-score for connectivity should show measurable improvement (synergy > 0) when both modalities are used together, quantifying the joint contribution beyond linear combination.
- Error distributions (false negatives, incorrect formula, incorrect connectivity) should be stratified by molecular complexity; accuracy should not degrade sharply for molecules near the 19 heavy-atom limit.
- Modality-specific failure patterns (e.g., ¹³C-only worse on branched structures, ¹H-only worse on aromatic compounds) should be documented to justify the fusion strategy.
- Metrics must be computed on held-out test pairs with no data leakage from training set; test set size and composition should be reported.

## Limitations

- Evaluation is restricted to molecules with up to 19 heavy atoms; performance and failure modes on larger or more complex structures (polycyclic, highly substituted) are not characterized.
- The skill assumes ground truth connectivity and formula are unambiguous and correctly assigned; evaluation cannot distinguish between prediction errors and incorrect labels.
- Graph edit distance and F1-score are coarse proxies for chemical utility; predictions with minor topological errors (e.g., one bond misplaced in a long chain) may be acceptable in practice but count as failures.
- Synergy calculation assumes independent processing in single-modality baselines; actual fusion may involve learned cross-modality interactions that are not captured by simple subtraction.
- Evaluation does not assess whether the predicted structures are synthetically accessible, chemically stable, or consistent with other spectroscopic data (MS, IR, UV–Vis).

## Evidence

- [other] Run inference on the convolutional neural network encoder followed by transformer architecture on each modality condition to generate structure predictions (molecular formula and connectivity).: "Run inference on the convolutional neural network encoder followed by transformer architecture on each modality condition to generate structure predictions (molecular formula and connectivity)."
- [other] Compute accuracy metrics (e.g., exact-match accuracy for formula and graph edit distance or connectivity F1 for structure) for each modality independently.: "Compute accuracy metrics (e.g., exact-match accuracy for formula and graph edit distance or connectivity F1 for structure) for each modality independently."
- [other] Compare accuracies across the three conditions and compute the joint contribution (1H+13C accuracy minus single-modality baseline) to quantify synergy.: "Compare accuracies across the three conditions and compute the joint contribution (1H+13C accuracy minus single-modality baseline) to quantify synergy."
- [intro] a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
