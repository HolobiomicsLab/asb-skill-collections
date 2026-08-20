---
name: structure-similarity-evaluation
description: Use when after an NMR-based structure prediction model has generated predicted molecular structures (formula and connectivity) for a test set of molecules with up to 19 heavy atoms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_3047
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structure-similarity-evaluation

## Summary

Evaluate predicted molecular structures against ground-truth structures using graph-based or chemical similarity metrics to quantify model accuracy. This skill applies structure matching metrics to assess whether an end-to-end spectroscopy-to-structure model has correctly recovered molecular formula, connectivity, and stereochemistry.

## When to use

After an NMR-based structure prediction model has generated predicted molecular structures (formula and connectivity) for a test set of molecules with up to 19 heavy atoms. Use this skill when you need to measure how closely the predicted structures match experimentally validated or known ground-truth structures, particularly in high-dimensional chemical space where simple string matching is insufficient.

## When NOT to use

- When only raw spectral data (1D ¹H or ¹³C NMR peaks) are available and no structure prediction has been performed yet—use the full CNN+transformer pipeline first.
- When molecules exceed 19 heavy atoms—the framework was validated only up to this threshold; larger molecules enter unexplored chemical space with exponentially more possible structures.
- When ground-truth structures are unavailable or ambiguous—structure similarity evaluation requires a reliable reference to compare against.

## Inputs

- predicted molecular structures (formula and connectivity as graph or SMILES)
- ground-truth molecular structures (formula and connectivity as graph or SMILES)
- model confidence scores per prediction
- evaluation dataset metadata (molecule identifiers, atom counts)

## Outputs

- structure similarity scores per molecule
- aggregate accuracy (exact match rate, %)
- F1-score
- per-prediction comparison report (predicted vs. ground-truth structure, similarity, confidence)
- evaluation metrics log

## How to apply

Load both predicted structures and ground-truth molecular structures from the evaluation dataset. Apply structure matching metrics (e.g., graph isomorphism, Tanimoto similarity on molecular fingerprints, or canonical SMILES comparison) to quantify structural similarity. Compute aggregate evaluation metrics—accuracy (exact match rate), F1-score, or structure similarity scores—across the entire test set. Log predictions with associated confidence scores alongside similarity scores to identify cases where the model is uncertain. Rationale: structure matching accounts for the fact that multiple canonical representations of the same molecule exist; direct string comparison would incorrectly penalize valid alternative notations. Comparing both formula and connectivity separately reveals whether errors stem from incorrect atom composition or incorrect assembly of fragments.

## Related tools

- **Convolutional Neural Network (CNN)** (feature extraction layer that encodes 1D NMR spectral information prior to structure assembly; outputs are fed to transformer)
- **Transformer architecture** (assembles CNN-encoded spectral features into predicted molecular fragments and predicts connectivity and molecular formula)

## Evaluation signals

- Exact structure match rate (accuracy): predicted and ground-truth structures are graph-isomorphic or have identical canonical SMILES representations.
- F1-score on per-molecule predictions balances precision (fraction of predicted structures that are correct) and recall (fraction of ground-truth structures that are recovered).
- Structure similarity scores follow expected distribution: high scores (>0.9) for correct predictions, low scores (<0.5) for incorrect ones, with minimal overlap in the intermediate range.
- Confidence score correlation: model's reported confidence scores should correlate positively with achieved structure similarity (Spearman or Pearson ρ > 0.5).
- No structure prediction exceeds the 19 heavy-atom molecular weight limit; all test molecules conform to the validated scope.

## Limitations

- Effectiveness demonstrated only on molecules with up to 19 heavy (non-hydrogen) atoms; efficacy on larger, more complex molecules is unknown.
- Structure similarity depends on the quality and completeness of ground-truth reference data; ambiguous or incorrect reference structures will bias evaluation metrics.
- Metrics such as graph isomorphism can be computationally expensive for large molecular graphs; throughput may degrade for high-volume test sets.
- The framework predicts formula and connectivity but does not address three-dimensional stereochemistry or conformational ensembles; similarity scores ignore spatial orientation.

## Evidence

- [intro] framework validation on molecular size: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [other] output structure prediction and comparison: "Generate predicted structures for all test molecules and compare against ground truth using structure matching metrics"
- [other] evaluation metric computation: "Compute and log evaluation metrics (accuracy, F1-score, or structure similarity scores) and save predictions with confidence scores"
- [intro] integrated model for fast and accurate prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra that is fast and accurate"
