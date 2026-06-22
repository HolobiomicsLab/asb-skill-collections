---
name: formula-annotation-capping-by-frequency
description: Use when when preparing multi-formula MS/MS training data for a rescore model, if the raw positive examples show extreme imbalance (some formulas represented by hundreds of spectra while others have only a few).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0097
  - http://edamontology.org/topic_3520
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-annotation-capping-by-frequency

## Summary

Cap the number of positive (correctly annotated) examples per molecular formula in training data to enforce class balance constraints before rescore model training. This prevents high-frequency formulas from dominating the training set and skewing model performance toward common analytes.

## When to use

When preparing multi-formula MS/MS training data for a rescore model, if the raw positive examples show extreme imbalance (some formulas represented by hundreds of spectra while others have only a few). Apply this when you need to ensure the model learns equally across rare and common molecular formulas, particularly before pairing with cross-spectrum negative generation and downstream class balancing.

## When NOT to use

- Input spectra are already heavily downsampled or represent rare metabolites only; capping may further starve model of training signal.
- Downstream task requires stratified representation of all original formula frequencies (e.g., prevalence-aware benchmarking); capping artificially homogenizes the distribution.
- Formula annotations are missing or unreliable; capping is only meaningful if grouping by formula is trustworthy.

## Inputs

- TCN train set spectra with molecular formula annotations (MGF or equivalent format)
- TCN test set spectra with molecular formula annotations
- Class balance constraint specification (e.g., maximum examples per formula)

## Outputs

- Capped positive examples per molecular formula (reduced or unchanged counts)
- Train set with balanced formula representation
- Test set with balanced formula representation
- Metadata log recording cap threshold and per-formula counts before and after

## How to apply

After loading TCN train and test set spectra with their molecular formula annotations, iterate through the positive examples grouped by formula and truncate each group to a fixed maximum count (e.g., cap at N spectra per formula). The choice of cap threshold depends on the least-represented formula in your dataset and the target positive example budget; a common heuristic is to set the cap such that the sum of capped counts equals or slightly exceeds the desired positive pool size. Document the cap threshold and the pre- and post-capping distribution of examples per formula to justify the balance trade-off. This step must precede cross-spectrum negative generation, since the capped positive set determines the pool from which negatives are sampled.

## Related tools

- **msfiddle** (Python API and CLI for rescore model training and inference; prepare_augment_rescore.py is invoked as part of the FIDDLE training pipeline after formula capping) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase including training scripts and data preparation; contains prepare_augment_rescore.py and related augmentation and balancing workflows) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Verify that no formula in the capped set exceeds the specified cap threshold; histogram of examples per formula should show a hard ceiling.
- Confirm that capping preserves at least one spectrum per formula (no formulas dropped entirely) unless explicitly intended.
- Compare per-formula distributions before and after capping to ensure rare formulas are not disproportionately filtered out.
- Validate that capped positive counts, when passed to cross-spectrum negative generation and downsampling, result in the target positive:negative ratio (e.g., 1:1).
- Check that test set formulas remain unchanged (test set should not be capped) or, if capped, that the cap is applied identically to enable fair rescore model evaluation.

## Limitations

- Capping is a lossy operation; excess examples are discarded and cannot be recovered. If the cap is too aggressive, the model may underfit on rare formulas.
- The choice of cap threshold is somewhat arbitrary and dataset-dependent. No principled method for determining the optimal cap is provided in the documentation; it is typically set empirically.
- Capping affects only the positive class; it does not directly address imbalance between positive and negative classes, which is handled separately by cross-spectrum negative generation and subsequent downsampling.
- If a formula appears in the test set but was capped below its true frequency in the train set, the rescore model may show inflated performance on that formula because the test distribution differs from the train distribution.

## Evidence

- [other] Cap positive examples per molecular formula to enforce class balance constraints.: "Cap positive examples per molecular formula to enforce class balance constraints."
- [readme] The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md.: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
- [other] Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio.: "Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio."
- [other] Load TCN train and test set spectra and annotations.: "Load TCN train and test set spectra and annotations."
