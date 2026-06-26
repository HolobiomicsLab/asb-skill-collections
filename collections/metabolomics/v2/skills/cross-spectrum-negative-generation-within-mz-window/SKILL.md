---
name: cross-spectrum-negative-generation-within-mz-window
description: Use when when preparing augmented training data for a Siamese rescore
  model that must learn to rank correct molecular formulas above incorrect ones;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0611
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-spectrum-negative-generation-within-mz-window

## Summary

Generate negative training examples for MS/MS rescore models by pairing spectra within a defined precursor m/z window, creating hard negatives that improve model discrimination between correct and incorrect molecular formula candidates.

## When to use

When preparing augmented training data for a Siamese rescore model that must learn to rank correct molecular formulas above incorrect ones; specifically when you have TCN-predicted candidate formulas and need to create negative pairs that are confusable (similar precursor m/z) but incorrect, to prevent the model from over-fitting to trivial negative examples.

## When NOT to use

- When negative examples are already available from an external reference library or pre-computed candidate set — use those instead to avoid redundant pairing.
- When the goal is spectrum similarity or clustering rather than formula ranking; cross-spectrum negatives are tuned for discriminative rescore tasks, not exploratory analysis.
- When precursor m/z window is unknown or the spectrum set is too small to yield meaningful cross-spectrum pairs within a tight m/z tolerance.

## Inputs

- TCN train and test set spectra (m/z arrays, intensity arrays, metadata)
- TCN-predicted candidate formulas and their precursor m/z values
- Precursor m/z tolerance window definition (Da or ppm)
- Molecular formula annotations for each spectrum

## Outputs

- Augmented training set with positive and hard-negative spectrum pairs
- Augmented test set with positive and hard-negative spectrum pairs
- Class-balanced dataset (positive:negative ratio specified, e.g., 1:1)
- Output files in format compatible with Siamese rescore model ingestion

## How to apply

After loading TCN train and test set spectra and filtering positive examples (capping per molecular formula to enforce class balance), systematically pair each spectrum with other spectra whose precursor m/z falls within a defined window (e.g., ±tolerance in Da or ppm) but whose molecular formulas differ from the true formula. These cross-spectrum pairings create negative training instances that are harder than random negatives because they are chemically and mass-wise similar. The rationale is that such 'hard negatives' force the rescore model to learn fine-grained discrimination based on fragment patterns rather than gross mass differences. After generating negatives, downsample the combined positive and negative pool to achieve a target ratio (e.g., 1:1 positive:negative) to prevent class imbalance from biasing the rescore model's loss landscape.

## Related tools

- **msfiddle** (Python API and CLI for FIDDLE formula prediction; encapsulates TCN and rescore model inference; used to load spectra, compute initial formula candidates, and invoke rescore ranking.) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase for model training, evaluation, and data augmentation including the prepare_augment_rescore.py script that orchestrates cross-spectrum negative generation and class-balanced downsampling.) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Verify that all generated negative pairs have precursor m/z within the defined tolerance window of the query spectrum.
- Confirm that no negative pair uses a spectrum whose true molecular formula matches the query spectrum's true formula (no false negatives in the negative set).
- Check that the final augmented dataset achieves the target positive:negative ratio (e.g., 1:1) by counting pair types in the output file.
- Validate that the output format matches the expected schema for Siamese rescore model ingestion (e.g., paired (query, candidate) records with binary labels).
- Ensure that the downsampling step does not remove all spectra from any molecular formula class or precursor m/z bin, preserving diversity in the training set.

## Limitations

- Hard negatives are only available within the defined m/z tolerance window; spectra far outside that window will not contribute negative examples, potentially under-representing very different formulas.
- The quality of negatives depends on the density of spectra in the dataset; sparse datasets may not yield enough cross-spectrum pairs within a tight m/z window, leading to underfitting.
- Downsampling to achieve class balance discards potentially valuable examples; the choice of target ratio (e.g., 1:1) is heuristic and may not be optimal for all datasets.
- The approach assumes that precursor m/z similarity correlates with formula confusion; datasets with severe isotope labeling, adduct variation, or in-source fragmentation may violate this assumption.

## Evidence

- [other] Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window.: "Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window."
- [other] Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio.: "Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio."
- [readme] The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md: "The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md."
- [other] Load TCN train and test set spectra and annotations. Cap positive examples per molecular formula to enforce class balance constraints.: "Load TCN train and test set spectra and annotations. Cap positive examples per molecular formula to enforce class balance constraints."
