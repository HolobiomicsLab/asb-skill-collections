---
name: negative-adduct-tokenization-in-mass-spectrometry
description: Use when you have negative-mode MS/MS spectra with annotated molecular formulas and negative adducts (from repositories like MassIVE or MetaboLights), and your current formula inference model is restricted to positive mode only.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3648
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# negative-adduct-tokenization-in-mass-spectrometry

## Summary

Extend formula transformer neural networks to recognize and tokenize negative ionization mode adducts ([M-H]−, [M+Cl]−, [M+FA]−) in tandem mass spectra, enabling chemical formula ranking for negative-mode MS/MS data. This skill adapts the MIST-CF architecture from positive-mode-only operation to support dual-polarity metabolite identification.

## When to use

You have negative-mode MS/MS spectra with annotated molecular formulas and negative adducts (from repositories like MassIVE or MetaboLights), and your current formula inference model is restricted to positive mode only. Use this skill when you need to extend an existing formula transformer to handle [M-H]−, [M+Cl]−, or [M+FA]− ions and rank candidate formulas by top-k accuracy on held-out negative-mode test spectra.

## When NOT to use

- Your input spectra are exclusively positive ionization mode or contain no adduct annotations—use the original positive-mode MIST-CF instead.
- Your negative-mode dataset is too small (<1000 spectra) to support fine-tuning without overfitting; consider data augmentation or transfer learning from positive mode first.
- You require real-time inference on new spectra without a labeled negative-mode test set for validation; train and evaluate on the same dataset will not yield reliable accuracy estimates.

## Inputs

- negative-mode MS/MS spectra (MGF or raw format)
- precursor m/z values with annotated molecular formulas
- negative adduct type annotations ([M-H]−, [M+Cl]−, [M+FA]−)
- pre-trained MIST-CF model weights (positive mode)
- sinusoidal formula embeddings from SCARF

## Outputs

- extended MIST-CF model with negative-mode adduct tokenization layer
- fine-tuned formula transformer weights for negative ionization
- top-1, top-5, top-10 formula ranking accuracy metrics per negative adduct type
- comparative metrics table across negative adducts

## How to apply

First, acquire negative-mode MS/MS spectra from public metabolomics repositories with annotated molecular formulas and negative adducts. Preprocess spectra by normalizing intensity and removing noise below a defined threshold. Extend the adduct tokenization layer in the MIST-CF architecture to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−), treating each adduct type as a discrete token similar to the existing positive-mode tokens. Fine-tune the formula transformer neural network using negative-mode spectra while maintaining the existing sinusoidal formula embeddings from SCARF to preserve learned chemical space structure. Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy across each negative adduct type, and compile results in a metrics table to identify any performance asymmetries across adduct classes.

## Related tools

- **MIST-CF** (formula transformer architecture extended with negative-mode adduct tokenization and fine-tuned on negative-mode spectra) — https://github.com/samgoldman97/mist-cf
- **SCARF** (source of sinusoidal formula embeddings maintained during fine-tuning to preserve chemical structure knowledge) — https://arxiv.org/abs/2303.06470
- **SIRIUS** (decomposition engine for enumerating candidate formulas from precursor m/z (used upstream for candidate generation)) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. run_scripts/public_data_train/train_mist_cf.sh
```

## Evaluation signals

- Top-1, top-5, and top-10 formula ranking accuracy on held-out negative-mode test set all improve relative to positive-mode baseline
- Performance is consistent across the three main negative adduct types ([M-H]−, [M+Cl]−, [M+FA]−); large variance between adducts suggests incomplete tokenization or insufficient training data for rare adducts
- Sinusoidal formula embeddings remain stable (L2 norm difference < 1% from SCARF pre-training) after fine-tuning, confirming knowledge preservation
- Adduct token logits in the output layer show clear separation between negative and positive adduct classes (e.g., via t-SNE or cosine similarity clustering)
- No significant overfitting: test accuracy gap relative to training accuracy is < 5 percentage points across all top-k metrics

## Limitations

- MIST-CF currently supports only positive ionization mode; extension to negative mode has not yet been benchmarked against competing tools like SIRIUS on negative-mode datasets.
- Fine-tuning may suffer from data scarcity if negative-mode spectra are underrepresented in available public repositories (e.g., MassIVE, MetaboLights).
- Sinusoidal formula embeddings from SCARF were learned on positive-mode chemical space; transfer to negative mode may introduce bias toward positive-mode ion fragmentation patterns.
- Adduct tokenization assumes discrete adduct types; complex or instrument-specific adducts not in the predefined set ([M-H]−, [M+Cl]−, [M+FA]−) will not be recognized.
- Evaluation is limited to top-k accuracy metrics; other desiderata (e.g., calibration, false positive rate on out-of-database formulas) are not addressed in the task specification.

## Evidence

- [other] MIST-CF currently considers multiple adduct types beyond [M+H]+ but is still restricted to positive mode only.: "MIST-CF currently considers multiple adduct types beyond [M+H]+ but is still restricted to positive mode only."
- [other] Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−).: "Extend the adduct tokenization layer in MIST-CF to include common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−)."
- [other] Fine-tune the formula transformer neural network using negative-mode spectra, maintaining the existing sinusoidal formula embeddings from SCARF.: "Fine-tune the formula transformer neural network using negative-mode spectra, maintaining the existing sinusoidal formula embeddings from SCARF."
- [other] Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy.: "Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy."
- [intro] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [intro] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
