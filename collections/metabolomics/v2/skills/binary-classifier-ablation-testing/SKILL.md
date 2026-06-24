---
name: binary-classifier-ablation-testing
description: Use when you have a trained binary molecular classifier (like BitterPredict)
  and want to understand which groups of chemical descriptors drive its predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0199
  tools:
  - BitterPredict
  - BitterPredict.m
  license_tier: restricted
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

# binary-classifier-ablation-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically remove descriptor subgroups from a molecular classifier's input data and measure prediction changes to identify which chemical structure descriptors have the greatest impact on bitter/not-bitter predictions. This reveals descriptor importance and enables interpretability of the classifier's decision logic.

## When to use

You have a trained binary molecular classifier (like BitterPredict) and want to understand which groups of chemical descriptors drive its predictions. Apply this skill when you need to rank descriptor subgroups by their contribution to prediction accuracy, or when you suspect certain molecular properties (e.g., lipophilicity, topological features) are disproportionately influential.

## When NOT to use

- The classifier is not yet trained or validated — ablation testing requires a working, stable model.
- Descriptor subgroups are not well-defined or functionally coherent — results depend on meaningful groupings.
- Input data lacks bitter/not-bitter labels — baseline predictions cannot be reliably compared.

## Inputs

- CSV or EXCEL file containing molecular descriptors and bitter/not-bitter class labels
- Descriptor subgroup definitions (mapping of descriptors to functionally coherent categories)
- Trained BitterPredict.m classifier

## Outputs

- Summary table with descriptor subgroups as rows, metrics (prediction-change count, change rate percentage) as columns
- Per-molecule prediction change records for each descriptor ablation
- Ranked descriptor subgroups by impact on prediction accuracy

## How to apply

Organize molecular descriptors into functionally coherent subgroups (e.g., molecular weight, lipophilicity, topological, pharmacophoric descriptors). For each subgroup, create a modified dataset by setting all descriptors in that subgroup to zero while preserving all other descriptors and the bitter/not-bitter labels. Run BitterPredict.m on each ablated dataset and compare predictions against the baseline (full-descriptor) predictions, recording whether each molecule's bitter label changed. Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed. Compile results into a summary table with descriptor subgroups as rows and metrics (number of changed predictions, change rate percentage) as columns. Higher change rates indicate greater descriptor importance.

## Related tools

- **BitterPredict.m** (Binary classifier that accepts CSV/EXCEL descriptor files and outputs bitter/not-bitter predictions for each molecule; ablation testing iteratively calls this tool on descriptor-ablated datasets) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Each ablated dataset retains the same molecule count and bitter/not-bitter label distribution as the original; only descriptor subgroups are zeroed.
- Prediction-change rates fall between 0 and 1 (or 0–100% as percentage); subgroups with zero change indicate negligible impact.
- Descriptor subgroups with higher change rates correspond to known chemical properties relevant to taste perception (e.g., lipophilicity, polar surface area).
- Summary table contains no missing values and row totals (or per-subgroup metrics) are consistent across repeated runs.
- Baseline predictions (using the full descriptor set) match the original trained model's predictions on the same input data.

## Limitations

- Results are sensitive to how descriptors are grouped; poor grouping choices may obscure true descriptor importance.
- Zeroing descriptor subgroups creates artificially modified input that may not reflect real chemical variation; descriptor interactions are tested indirectly.
- The method assumes the classifier is deterministic; stochastic models may yield variable results across repeated ablation runs.
- No statistical significance testing is applied by default; change rates alone do not indicate whether differences are due to chance or model noise.

## Evidence

- [other] descriptor_ablation_overview: "Which descriptor subgroups have the greatest impact on bitter/not-bitter prediction accuracy when systematically removed from the BitterPredict classifier?"
- [other] descriptor_ablation_workflow: "For each descriptor subgroup, create a modified dataset where all descriptors in that subgroup are set to zero while retaining other descriptors unchanged. Run BitterPredict.m on each ablated dataset"
- [other] descriptor_ablation_metrics: "Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed. Compile results into a summary table with descriptor"
- [readme] bitterpredict_input_format: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
