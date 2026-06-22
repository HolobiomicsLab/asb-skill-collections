---
name: adduct-specific-model-fine-tuning
description: Use when when you have access to annotated MS/MS spectra from a specific ionization mode (e.g., negative ESI) or adduct class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-specific-model-fine-tuning

## Summary

Fine-tune a formula transformer neural network on MS/MS spectra grouped by ionization mode and adduct type to improve chemical formula ranking accuracy for molecules ionized under specific conditions. This skill adapts a pre-trained model (e.g., MIST-CF) by retraining its adduct tokenization and formula embedding layers on mode-specific data, enabling accurate formula inference for underrepresented ionization modes or novel adduct chemistries.

## When to use

When you have access to annotated MS/MS spectra from a specific ionization mode (e.g., negative ESI) or adduct class (e.g., [M-H]−, [M+Cl]−) that is either absent or underrepresented in the pre-training data, and you want to improve top-k formula ranking accuracy on that mode without retraining from scratch. This is particularly useful when extending a positive-mode-only model (like the current MIST-CF) to support negative-mode or multi-adduct workflows.

## When NOT to use

- Positive-mode ESI spectra already well-represented in the pre-training data; fine-tuning adds minimal benefit and risks overfitting.
- Fewer than ~100–200 annotated spectra in the target mode; insufficient training signal for stable fine-tuning of a transformer.
- Pre-training data already includes the target adduct type; use the base model directly rather than fine-tuning.

## Inputs

- Pre-trained MIST-CF model weights (formula transformer checkpoint)
- MS/MS spectra in .mgf or standardized format with m/z and intensity arrays
- Ground-truth molecular formula and adduct type annotations (e.g., CSV with [spec_id, formula, adduct])
- List of target adducts for tokenization extension (e.g., [M-H]−, [M+Cl]−, [M+FA]−)

## Outputs

- Fine-tuned MIST-CF model checkpoint (weights for adduct tokenization and formula transformer layers)
- Metrics table with top-1, top-5, and top-10 formula ranking accuracy per adduct type
- Validation and test loss curves confirming model convergence
- Ranked formula predictions for test spectra with energy-based scores

## How to apply

Acquire a curated set of negative-mode or mode-specific MS/MS spectra with ground-truth molecular formulas and adduct annotations from public repositories (e.g., MassIVE, MetaboLights). Preprocess spectra by normalizing intensity to [0, 1] and removing noise below a signal-to-noise threshold (e.g., SNR < 3). Extend the adduct tokenization layer in the pre-trained model to include the target adducts ([M-H]−, [M+Cl]−, [M+FA]−, etc.), preserving the sinusoidal formula embeddings learned by SCARF. Fine-tune the extended model using the mode-specific training set with a held-out validation split (e.g., 80/20), monitoring loss on a validation fold to prevent overfitting. Evaluate the fine-tuned model on a held-out test set by computing top-1, top-5, and top-10 formula ranking accuracy and compile results in a metrics table stratified by adduct type. Use energy-based scoring to rank formula candidates and ensure convergence by checking that validation loss plateaus.

## Related tools

- **MIST-CF** (Pre-trained formula transformer model to be extended and fine-tuned for negative-mode and multi-adduct support) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Source of sinusoidal formula embeddings that are preserved and reused during fine-tuning to maintain learned chemical space structure) — https://arxiv.org/abs/2303.06470
- **SIRIUS** (Used to enumerate candidate molecular formulas for a given precursor mass via dynamic programming (SIRIUS decomp)) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. run_scripts/public_data_train/train_mist_cf.sh
```

## Evaluation signals

- Top-1 formula ranking accuracy on held-out negative-mode test set is ≥ 5 percentage points higher than zero-shot base model, stratified by adduct type.
- Validation loss converges and does not increase over final 10–20 epochs, indicating stable fine-tuning without overfitting.
- Top-5 and top-10 accuracy improve proportionally with top-1 accuracy across adduct types, showing consistent model improvement.
- Energy-based scores (model outputs) are well-calibrated: higher-ranked correct formulas have lower energy (higher probability) than incorrect candidates in ≥ 80% of test spectra.
- Metrics table shows comparable or improved performance on rare adducts (e.g., [M+FA]−) compared to common adducts (e.g., [M-H]−), confirming that fine-tuning balances representation across adduct classes.

## Limitations

- MIST-CF is currently restricted to positive-mode only in the published version; extending to negative mode requires custom implementation of the adduct tokenization layer and retraining from a positive-mode checkpoint.
- Fine-tuning is only effective when the target ionization mode or adduct type is sufficiently distinct from pre-training distribution; modes with very similar fragmentation patterns may not benefit significantly.
- Model performance is data-dependent and may degrade on spectra from instruments or sample types not well-represented in the fine-tuning set (e.g., Orbitrap vs. Q-TOF).
- Energy-based scoring requires careful regularization and validation to avoid mode collapse or trivial solutions during fine-tuning; convergence is not guaranteed on small or imbalanced datasets.

## Evidence

- [other] Can the MIST-CF formula transformer architecture be extended to support negative-mode adducts, and what is the resulting top-k formula ranking accuracy on negative-mode MS/MS spectra?: "Can the MIST-CF formula transformer architecture be extended to support negative-mode adducts, and what is the resulting top-k formula ranking accuracy on negative-mode MS/MS spectra?"
- [other] Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−). Fine-tune the formula transformer neural network using negative-mode spectra, maintaining the existing sinusoidal formula embeddings from SCARF.: "Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−). Fine-tune the formula transformer neural network using negative-mode spectra,"
- [other] Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy. Compile results in a metrics table comparing performance across negative adduct types.: "Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy. Compile results in a metrics table comparing performance across"
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] MIST-CF considers multiple adduct types beyond [M+H]+ (still only positive mode): "MIST-CF considers multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF"
