---
name: prediction-sensitivity-analysis
description: Use when you have a trained predictor (like BitterPredict) that accepts structured descriptors and want to understand feature importance without retraining.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - BitterPredict
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.
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
---

# prediction-sensitivity-analysis

## Summary

Systematically ablate input descriptor subgroups to quantify their individual impact on bitter/not-bitter prediction accuracy in a trained classifier. This skill reveals which molecular descriptor categories (e.g., lipophilicity, topological features) drive predictions and which are redundant.

## When to use

You have a trained predictor (like BitterPredict) that accepts structured descriptors and want to understand feature importance without retraining. Specifically, when you need to know which descriptor subgroups, if removed or zeroed, would change predictions for individual molecules—useful for model interpretation, descriptor reduction, and identifying critical chemical features for the target property.

## When NOT to use

- Input is already a condensed feature importance ranking or coefficient table—descriptor ablation is redundant with model-intrinsic importance metrics.
- Descriptor subgroups are not well-defined or functionally incoherent; ablation results will not be interpretable.
- The trained predictor is a black box that does not support CSV/EXCEL input or does not allow inference-only use without retraining.

## Inputs

- CSV or EXCEL file containing molecular descriptors and bitter/not-bitter labels
- Descriptor subgroup definitions (mapping of descriptors to functional categories)

## Outputs

- Ablated datasets (one per descriptor subgroup, with that subgroup zeroed)
- Prediction outputs from BitterPredict.m for each ablated dataset
- Per-molecule prediction-change annotations (boolean: prediction changed or not)
- Summary table with descriptor subgroups as rows and prediction-change rates and counts as columns

## How to apply

Load a descriptor CSV or EXCEL file with molecular descriptors and ground-truth labels (bitter/not-bitter). Partition descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors). For each subgroup, create an ablated dataset by setting all descriptors in that subgroup to zero while preserving other descriptors. Run BitterPredict.m on each ablated dataset to obtain predictions for every molecule. Compare each ablated prediction against the baseline (full-descriptor) prediction, recording whether the bitter label changed per molecule. Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction flipped when that subgroup was zeroed. Compile results into a summary table with descriptor subgroups as rows and metrics (number of molecules with changed predictions, change rate percentage) as columns. Subgroups with high change rates indicate strong predictive influence; low rates suggest redundancy.

## Related tools

- **BitterPredict** (Trained classifier that accepts CSV/EXCEL descriptor files and produces bitter/not-bitter predictions for each molecule; invoked on each ablated dataset to quantify the impact of descriptor subgroup removal on prediction outputs) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- All ablated datasets are identical to the baseline except for exactly one descriptor subgroup (all set to zero); no accidental data loss or corruption.
- Predictions from BitterPredict.m are obtained for 100% of molecules in each ablated dataset; no molecules are dropped or cause errors.
- Per-molecule prediction-change annotations are boolean and consistent: a prediction either changed or did not; no missing or ambiguous labels.
- Prediction-change rates are valid fractions in [0, 1] or percentages in [0, 100]; subgroup with highest rate has the strongest impact, lowest rate has the weakest.
- Summary table is complete with all descriptor subgroups listed, no duplicates, and metrics are correctly calculated (e.g., change rate = molecules_with_changed_predictions / total_molecules).

## Limitations

- Ablation studies assume descriptor independence; zeroing one subgroup does not capture interaction effects between subgroups.
- Prediction-change rate is a coarse binary metric (changed / not changed); it does not measure magnitude of change or confidence score variation.
- Functional coherence of descriptor subgroups is user-defined; poor or arbitrary groupings will yield uninterpretable results.
- The method is specific to inference on a fixed trained model; it does not reveal whether the model would generalize differently if trained without a descriptor subgroup.

## Evidence

- [other] Which descriptor subgroups have the greatest impact on bitter/not-bitter prediction accuracy when systematically removed from the BitterPredict classifier?: "Which descriptor subgroups have the greatest impact on bitter/not-bitter prediction accuracy when systematically removed from the BitterPredict classifier?"
- [other] BitterPredict.m accepts CSV or EXCEL files containing molecular descriptors as input and produces bitter/not-bitter predictions for each molecule, enabling descriptor ablation studies through systematic manipulation of descriptor subgroups in the input data.: "BitterPredict.m accepts CSV or EXCEL files containing molecular descriptors as input and produces bitter/not-bitter predictions for each molecule, enabling descriptor ablation studies through"
- [other] Organize descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors). For each descriptor subgroup, create a modified dataset where all descriptors in that subgroup are set to zero while retaining other descriptors unchanged.: "Organize descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors). For each descriptor"
- [other] Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed.: "Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
