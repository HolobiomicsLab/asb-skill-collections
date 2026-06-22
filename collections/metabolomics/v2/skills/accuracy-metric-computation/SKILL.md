---
name: accuracy-metric-computation
description: Use when after running inference on a trained structure prediction model with one or more input modalities (1H NMR, 13C NMR, or combined), you have generated predicted molecular formulas and connectivity graphs that need to be compared against known ground truth structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - transformer architecture
  - convolutional neural network
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# accuracy-metric-computation

## Summary

Compute quantitative accuracy metrics (exact-match, graph edit distance, connectivity F1) to evaluate molecular structure predictions from spectroscopic inputs against ground truth labels. This skill measures prediction correctness across multiple structural representations and identifies performance gaps between modalities.

## When to use

After running inference on a trained structure prediction model with one or more input modalities (1H NMR, 13C NMR, or combined), you have generated predicted molecular formulas and connectivity graphs that need to be compared against known ground truth structures. Use this skill to quantify how well the model recovered the correct structure across different spectroscopic conditions.

## When NOT to use

- Input predictions are not yet generated (model inference has not completed)
- Ground truth labels are missing or inconsistent with prediction format (e.g., SMILES vs. graphs incompatible)
- Evaluating performance on training or validation data without explicit train/test split (risk of overfitting signal)

## Inputs

- predicted molecular formulas (strings, canonical SMILES, or molecular graphs)
- predicted connectivity graphs or bond adjacency matrices
- ground truth molecular structures (canonical SMILES or molecular graphs)
- modality condition labels (e.g., '1H-only', '13C-only', '1H+13C')
- test set size and molecular complexity metadata (atom count, branching, ring systems)

## Outputs

- exact-match accuracy for molecular formula (0–1 or percentage)
- graph edit distance per molecule or aggregate distribution
- connectivity F1-score (precision and recall per molecule or macro-averaged)
- accuracy stratified by modality (table or plot)
- synergy metric: joint accuracy minus single-modality baseline
- error distribution and failure analysis (e.g., false structure classes, common atom/bond misassignments)

## How to apply

Load the model predictions and corresponding ground truth molecular structures for a held-out test set. For each prediction, compute multiple accuracy metrics: exact-match accuracy for molecular formula (binary: predicted formula equals ground truth), graph edit distance or connectivity F1-score for structure topology, and document error distributions. When evaluating multiple modalities (1H-only, 13C-only, 1H+13C combined), compute accuracy independently for each condition, then calculate synergy as the joint accuracy (1H+13C) minus the best single-modality baseline. Tabulate results by modality to enable direct comparison and identify which spectroscopic input contributes most to structure elucidation.

## Related tools

- **transformer architecture** (generates predicted molecular structures (graphs or SMILES) from spectroscopic input; outputs feed into metric computation)
- **convolutional neural network** (encodes 1D NMR spectra into feature representations; predictions are evaluated by this skill)

## Evaluation signals

- Accuracy values fall within expected range [0, 1] and sum of category counts equals test set size
- Graph edit distance or F1-scores are consistent with visual inspection of sample predictions (high metrics for chemically plausible structures, low metrics for obviously incorrect bonds/atoms)
- Synergy metric (1H+13C minus baseline) is non-negative and interpretable: positive values indicate complementary information, zero or negative values suggest one modality dominates
- Error distribution is documented per complexity class (e.g., molecules with ≤10 atoms achieve higher accuracy than those with 15–19 atoms), confirming known difficulty scaling
- Comparison table shows clear ordering of modalities (e.g., 1H+13C ≥ 13C-only ≥ 1H-only or similar pattern); any inversion suggests a data or metric bug

## Limitations

- Evaluation on molecules with up to 19 heavy atoms only; accuracy and synergy on larger or more complex molecules (polycyclic, heavily branched) are not characterized
- Exact-match and graph edit distance metrics are stringent and do not reward partial structure recovery (e.g., correct formula but wrong connectivity); connectivity F1 is more lenient but may mask significant topological errors
- Synergy calculation assumes independence of 1H and 13C features; actual contributions may be non-additive or confounded if spectra encode redundant or correlated information
- Performance may vary with spectroscopic data quality, resolution, and preprocessing; results are tied to the NMR acquisition and model training conditions in this work

## Evidence

- [other] compute accuracy metrics (e.g., exact-match accuracy for formula and graph edit distance or connectivity F1 for structure) for each modality independently: "Compute accuracy metrics (e.g., exact-match accuracy for formula and graph edit distance or connectivity F1 for structure) for each modality independently."
- [other] Compare accuracies across the three conditions and compute the joint contribution (1H+13C accuracy minus single-modality baseline) to quantify synergy: "Compare accuracies across the three conditions and compute the joint contribution (1H+13C accuracy minus single-modality baseline) to quantify synergy."
- [other] Tabulate results by modality showing accuracy, error distribution, and performance gaps: "Tabulate results by modality showing accuracy, error distribution, and performance gaps."
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [other] Evaluate fragment assembly accuracy on held-out test pairs, computing metrics such as exact structure match rate and partial assembly correctness: "Evaluate fragment assembly accuracy on held-out test pairs, computing metrics such as exact structure match rate and partial assembly correctness."
