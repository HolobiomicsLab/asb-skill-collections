---
name: descriptor-subgroup-partitioning
description: Use when when you have a trained BitterPredict classifier, a dataset of molecules with computed descriptors and known bitter/not-bitter labels, and want to understand which descriptor categories (e.g., molecular weight, lipophilicity, topological, pharmacophoric) drive prediction decisions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_0209
  tools:
  - BitterPredict
  - BitterPredict.m
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# descriptor-subgroup-partitioning

## Summary

Partition molecular descriptors into functionally coherent subgroups and systematically ablate each subgroup to quantify its impact on bitter/not-bitter prediction accuracy. This skill enables feature importance analysis through controlled descriptor removal and comparison of prediction changes.

## When to use

When you have a trained BitterPredict classifier, a dataset of molecules with computed descriptors and known bitter/not-bitter labels, and want to understand which descriptor categories (e.g., molecular weight, lipophilicity, topological, pharmacophoric) drive prediction decisions. Use this skill to prioritize descriptor collection effort or identify redundant descriptor subsets.

## When NOT to use

- Your input data already lacks raw descriptors (e.g., you have only pre-selected features or a feature matrix with no descriptor metadata)
- You lack a validated, trained BitterPredict model or cannot run BitterPredict.m on modified input files
- Your descriptors are not organized or documented well enough to group them into functionally coherent subsets with scientific justification

## Inputs

- CSV or EXCEL file containing molecular descriptors and bitter/not-bitter labels
- Functionally organized descriptor subgroup definitions (list or schema mapping descriptors to subgroups)
- Trained BitterPredict.m classifier

## Outputs

- Set of ablated descriptor datasets (one per subgroup, with target subgroup zeroed)
- Predictions for each molecule from each ablated dataset
- Summary table with descriptor subgroups as rows and metrics including number of molecules with changed predictions and change rate percentage as columns
- Per-descriptor-group prediction-change rate (fraction of molecules with changed predictions)

## How to apply

First, organize all descriptors in your input CSV/EXCEL file into functionally coherent subgroups based on their chemical meaning (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors). For each subgroup, create a modified dataset where descriptors in that subgroup are set to zero while all other descriptors remain unchanged. Run BitterPredict.m independently on each ablated dataset to generate predictions for every molecule. Compare the predictions from each ablated dataset against baseline (full-descriptor) predictions, recording which molecules' bitter labels changed. Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed. Finally, compile results into a summary table with descriptor subgroups as rows and metrics such as number of molecules with changed predictions and change rate percentage as columns.

## Related tools

- **BitterPredict.m** (Classifier that accepts CSV/EXCEL files with molecular descriptors and produces bitter/not-bitter predictions; run independently on each ablated dataset to quantify descriptor subgroup impact) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- All ablated datasets have the same number of molecules and rows as the baseline input file
- Each ablated dataset contains exactly one descriptor subgroup set to zero; all other descriptors match the baseline
- Predictions from BitterPredict.m run on each ablated dataset are obtained for every molecule in the input
- Per-descriptor-group prediction-change rates are between 0.0 and 1.0 (inclusive) and sum to a plausible total
- Summary table is complete with all descriptor subgroups as rows and both molecule-count and percentage-change metrics populated

## Limitations

- The method assumes descriptors can be meaningfully grouped; descriptors that are highly interdependent or co-linear may not show clear subgroup effects
- Zeroing a descriptor subgroup is a blunt ablation strategy; it does not preserve the natural distribution or correlation structure of withheld descriptors
- Results are sensitive to how subgroups are defined; different grouping schemes may yield different importance rankings
- The skill requires a working BitterPredict.m implementation and the ability to modify and re-run the classifier on multiple datasets; availability and computational cost depend on the model size and dataset size

## Evidence

- [other] Organize descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors).: "Organize descriptors into functionally coherent subgroups (e.g., molecular weight descriptors, lipophilicity descriptors, topological descriptors, pharmacophoric descriptors)."
- [other] For each descriptor subgroup, create a modified dataset where all descriptors in that subgroup are set to zero while retaining other descriptors unchanged.: "For each descriptor subgroup, create a modified dataset where all descriptors in that subgroup are set to zero while retaining other descriptors unchanged."
- [other] Run BitterPredict.m on each ablated dataset to obtain predictions for every molecule.: "Run BitterPredict.m on each ablated dataset to obtain predictions for every molecule."
- [other] Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed.: "Calculate the per-descriptor-group prediction-change rate as the fraction of molecules whose prediction changed when that subgroup was zeroed."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
