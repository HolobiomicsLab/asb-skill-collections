---
name: batch-prediction-comparison
description: Use when when you have a trained molecular classifier (like BitterPredict)
  that accepts structured descriptor input, and you need to understand which chemical
  descriptor subgroups drive prediction outcomes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3407
  tools:
  - BitterPredict
  - BitterPredict.m
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not,
  based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-prediction-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare predictions across multiple ablated feature sets by systematically removing descriptor subgroups from a classifier input and measuring prediction stability. This skill quantifies which molecular descriptor families are most influential on bitter/not-bitter classification outcomes.

## When to use

When you have a trained molecular classifier (like BitterPredict) that accepts structured descriptor input, and you need to understand which chemical descriptor subgroups drive prediction outcomes. Apply this skill when feature importance cannot be directly extracted from the model and you want empirical evidence of descriptor impact through prediction perturbation.

## When NOT to use

- Input data is already a feature-importance report or has been pre-reduced to a single feature set (no ablation possible)
- Descriptor subgroups are not semantically meaningful or cannot be independently zeroed without breaking chemical validity
- Classifier requires descriptor normalization or interaction effects that would be destroyed by zeroing subgroups

## Inputs

- CSV or EXCEL file with molecular descriptors and bitter/not-bitter labels
- Descriptor subgroup definitions (mapping of descriptors to functional categories)
- Trained BitterPredict.m classifier

## Outputs

- Ablated prediction datasets (one per descriptor subgroup)
- Per-molecule prediction change indicator (binary: changed or unchanged)
- Summary table with descriptor subgroups as rows, prediction-change rates and molecule counts as columns
- Ranked descriptor subgroups by predictive importance

## How to apply

Load the descriptor CSV or EXCEL file containing molecular descriptors and bitter/not-bitter labels. Partition descriptors into functionally coherent subgroups (e.g., molecular weight, lipophilicity, topological, pharmacophoric descriptors). For each subgroup, create a modified dataset by setting all descriptors in that subgroup to zero while retaining others unchanged. Run BitterPredict.m on each ablated dataset to generate predictions. Compare ablated predictions against baseline (full-descriptor) predictions molecule-by-molecule, recording which predictions changed. Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose bitter label changed when that subgroup was zeroed. Compile results into a summary table with descriptor subgroups as rows and metrics (e.g., count of molecules with changed predictions, change rate percentage) as columns. Subgroups with high change rates indicate greater predictive importance.

## Related tools

- **BitterPredict.m** (Executes batch predictions on descriptor-ablated datasets and returns bitter/not-bitter classifications for each molecule) — https://github.com/Niv-Lab/BitterPredict1

## Examples

```
% Load descriptor CSV, define descriptor_subgroups = {'MW', 'Lipophilicity', 'Topological', 'Pharmacophoric'}; for each subgroup, create modified_data by setting subgroup descriptors to zero, run BitterPredict(modified_data), compare predictions to baseline, record change rates, compile summary table.
```

## Evaluation signals

- All ablated datasets contain the same number of molecules as the original input, with only descriptor subgroup values modified
- Prediction change rates are monotonic and reasonable (e.g., removing a highly important descriptor causes >50% changes; removing a minor descriptor causes <5% changes)
- Summary table is complete with no missing values for any descriptor subgroup row
- The sum of molecules with changed predictions for all subgroups does not exceed the total number of molecules (accounting for overlaps)
- Baseline predictions (full descriptor set) match the original BitterPredict.m output on the unmodified input file

## Limitations

- Zeroing descriptor subgroups may produce out-of-distribution or chemically implausible descriptor combinations that the classifier did not encounter during training, potentially biasing importance estimates
- Descriptor importance is measured only by prediction change frequency, not by magnitude of confidence shift or consistency across chemical scaffolds
- The method assumes descriptor subgroups are independent; if descriptors within subgroups are highly correlated with descriptors in other subgroups, ablation may conflate their contributions

## Evidence

- [other] descriptor-ablation-workflow: "For each descriptor subgroup, create a modified dataset where all descriptors in that subgroup are set to zero while retaining other descriptors unchanged."
- [readme] bitterpredict-input-format: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
- [other] prediction-change-metric: "Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed."
- [other] descriptor-subgrouping-rationale: "Organize descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors)."
- [other] summary-table-output: "Compile results into a summary table with descriptor subgroups as rows and metrics (e.g., number of molecules with changed predictions, change rate percentage) as columns."
