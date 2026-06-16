---
name: neural-network-transfer-learning-for-spectral-models
description: Use when your input is a corpus of MS/MS spectra with annotated molecular formulas and adduct types that represent a new ionisation mode, instrument type, or adduct chemistry not well-represented in the pre-trained model's training data. You have access to a trained formula transformer (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3678
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
---

# neural-network-transfer-learning-for-spectral-models

## Summary

Adapt a pre-trained formula transformer neural network (MIST-CF) to new ionisation modes or mass spectrometry platforms by fine-tuning on a held-out dataset of annotated MS/MS spectra, preserving learned sinusoidal formula embeddings while retraining the adduct tokenization and ranking layers. This skill is critical when extending spectral interpretation models to conditions (e.g., negative ionisation mode) not covered by the original training distribution.

## When to use

Your input is a corpus of MS/MS spectra with annotated molecular formulas and adduct types that represent a new ionisation mode, instrument type, or adduct chemistry not well-represented in the pre-trained model's training data. You have access to a trained formula transformer (e.g., MIST-CF checkpoint) and want to maintain its learned representations while adapting its adduct and ranking decisions to the new condition without retraining from scratch.

## When NOT to use

- You have no access to annotated MS/MS spectra for the new condition; zero-shot application of the original pre-trained model is more appropriate.
- The new condition is so different (e.g., drastically different mass range, resolution, or fragmentation chemistry) that the pre-trained sinusoidal formula embeddings are likely misleading; retraining from scratch may be more robust.
- Your goal is to improve fingerprint prediction for molecular structure rather than formula assignment; the article notes that MIST-CF improvements are planned to be added back into MIST for fingerprint prediction in future work, suggesting the current transfer learning workflow is formula-specific.

## Inputs

- Pre-trained MIST-CF model checkpoint (PyTorch .pt or .pth file)
- MS/MS spectra in MGF or mzML format with annotated molecular formulas and adduct annotations
- Train/validation/test split metadata (e.g., spectrum IDs assigned to each split)
- Configuration YAML file specifying adduct types, preprocessing thresholds, learning rates, and epoch count

## Outputs

- Fine-tuned MIST-CF model checkpoint with updated adduct tokenization and ranking layers
- Top-k formula ranking accuracy metrics table (top-1, top-5, top-10) stratified by adduct type
- Per-spectrum predictions with ranked formula candidates and confidence scores
- Training/validation loss curves and convergence plots

## How to apply

Load the pre-trained MIST-CF model checkpoint, which includes sinusoidal formula embeddings learned via SCARF. Extend the adduct tokenization layer to include new adduct types (e.g., [M-H]−, [M+Cl]−, [M+FA]− for negative mode) that were not in the original positive-mode vocabulary. Preprocess the new-condition spectra by normalizing intensity and removing noise below a defined threshold. Fine-tune the formula transformer neural network on the new spectra dataset using the same loss function and training schedule as the original work, allowing the adduct embedding and ranking layers to adapt while keeping early-layer formula embeddings frozen or lightly regularized. Evaluate the fine-tuned model on a held-out test set from the new condition by computing top-1, top-5, and top-10 formula ranking accuracy. Compile results in a metrics table stratified by adduct type and compare against the original pre-trained model's zero-shot performance on the same test spectra to quantify the gain from transfer learning.

## Related tools

- **MIST-CF** (Pre-trained formula transformer model to be fine-tuned; handles de novo chemical formula and adduct ranking from MS/MS spectra) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Source of sinusoidal formula embeddings that are preserved and reused during transfer learning) — https://arxiv.org/abs/2303.06470
- **SIRIUS** (Dependency used to enumerate potential chemical formulas for observed MS1 masses via dynamic programming (SIRIUS decomp)) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. run_scripts/public_data_train/train_mist_cf.sh
```

## Evaluation signals

- Top-k formula ranking accuracy (top-1, top-5, top-10) on held-out test set is statistically significantly higher than the pre-trained baseline's zero-shot performance on the same spectra.
- Per-adduct type accuracy shows consistent improvement, indicating the model is not overfitting to one dominant adduct species.
- Training loss monotonically decreases and validation loss plateaus without diverging, indicating stable fine-tuning without catastrophic forgetting.
- Model predictions recover correct formulas for spectra whose precursor mass had not been observed during pre-training, confirming generalization of the transferred embeddings.
- Confusion analysis shows the fine-tuned model makes systematic improvements on adducts that were rare or absent in the original training set (e.g., [M+Cl]− in negative mode).

## Limitations

- Fine-tuning requires a substantial corpus of annotated MS/MS spectra for the new condition; performance degrades if the new-condition dataset is very small (<100 spectra).
- The sinusoidal formula embeddings from SCARF are frozen or lightly regularized to preserve pre-trained knowledge, which may constrain adaptation if the new condition exhibits drastically different fragmentation patterns.
- MIST-CF currently supports positive-mode adducts only in the pre-trained checkpoint; extending to negative mode requires explicit adduct tokenization changes and retraining, not zero-shot transfer.
- The model's performance is evaluated on top-k formula ranking accuracy; it does not jointly optimize for adduct classification, so an incorrect adduct prediction can cause a correct formula to be ranked lower.
- Transfer learning assumes the pre-trained model was trained on a distribution sufficiently similar to the new condition; very exotic adducts or ionisation regimes may require more extensive adaptation or retraining.

## Evidence

- [other] Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−): "Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−)."
- [other] Fine-tune the formula transformer neural network using negative-mode spectra, maintaining the existing sinusoidal formula embeddings from SCARF: "Fine-tune the formula transformer neural network using negative-mode spectra, maintaining the existing sinusoidal formula embeddings from SCARF."
- [other] Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy: "Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy."
- [intro] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
