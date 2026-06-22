---
name: performance-degradation-quantification-and-analysis
description: Use when you have a pretrained model with documented performance on a bounded input domain (e.g., molecules ≤19 heavy atoms, sequences <1000 bp) and you need to establish whether and how much accuracy drops on held-out test cases outside that domain boundary.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - NMR2Struct model (pretrained checkpoint)
  - PubChem or equivalent chemical database
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
---

# performance-degradation-quantification-and-analysis

## Summary

Quantifies and characterizes how a trained machine learning model's accuracy degrades when applied to data beyond its original training scope. This skill measures the gap between in-scope and out-of-scope performance, documents failure modes, and establishes known performance boundaries.

## When to use

Apply this skill when you have a pretrained model with documented performance on a bounded input domain (e.g., molecules ≤19 heavy atoms, sequences <1000 bp) and you need to establish whether and how much accuracy drops on held-out test cases outside that domain boundary. Use it to quantify the generalization failure rather than assume graceful degradation or complete failure.

## When NOT to use

- Input molecules or samples are already within the documented training scope (≤19 heavy atoms); use standard validation metrics instead.
- No ground-truth annotations or test set exists for out-of-scope samples; degradation quantification requires known structure labels.
- Model is being applied to a completely different domain or task (e.g., using NMR2Struct on protein folding); this skill measures scope boundary effects, not domain transfer.

## Inputs

- Pretrained model checkpoint (transformer + CNN architecture weights)
- Held-out test set of molecules exceeding the training scope boundary (>19 heavy atoms)
- 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules (simulated, experimental, or database-sourced)
- Ground-truth molecular connectivity graphs or structure annotations for each test molecule

## Outputs

- Top-1, top-3, and top-5 structure recovery accuracy metrics for out-of-scope molecules
- Absolute and relative accuracy degradation compared to in-scope baseline
- Error distribution histogram or summary (e.g., counts of correct fragments vs. misassembled fragments)
- Failure mode analysis report documenting systematic error patterns
- Performance degradation summary report with conclusions about generalization limits

## How to apply

Load the pretrained model checkpoint and construct or retrieve a held-out test set of samples that exceed the documented training scope boundary. Generate or obtain input data (e.g., NMR spectra, sequence reads) for each out-of-scope sample, then run inference to produce ranked predictions with confidence scores. Compute top-1, top-3, and top-5 accuracy metrics on the out-of-scope set, and directly compare against the reported in-scope baseline (e.g., molecules ≤19 heavy atoms). Calculate absolute and relative accuracy loss (e.g., baseline 95% minus out-of-scope 78% = 17 percentage point loss). Document the error distribution and identify recurring failure modes (e.g., misassembled fragments, low confidence predictions) in a summary report to characterize which types of out-of-scope samples fail predictably.

## Related tools

- **NMR2Struct model (pretrained checkpoint)** (The transformer + CNN model used to generate predicted molecular structures from NMR spectra; inference is run on out-of-scope test molecules to measure accuracy drop.)
- **PubChem or equivalent chemical database** (Source for retrieving or constructing held-out test molecules exceeding the training scope boundary (>19 heavy atoms) and their ground-truth structures.)

## Evaluation signals

- Absolute accuracy loss is quantifiable and reported (e.g., baseline 95% vs. out-of-scope 78% = 17 pp loss).
- Top-1, top-3, and top-5 accuracy metrics are all computed for the out-of-scope set and compared directly to in-scope baseline values.
- Error distribution is documented and reviewed for systematic failure modes (e.g., consistent misassembly of heavy-atom fragments above a threshold).
- All out-of-scope test samples have ground-truth structure annotations and are ranked by model confidence; predictions are matched against ground-truth connectivity.
- Summary report explicitly quantifies the performance boundary (e.g., 'accuracy remains >90% up to X heavy atoms, then drops sharply beyond Y atoms').

## Limitations

- The framework's effectiveness is bounded to molecules with up to 19 heavy atoms; generalization performance beyond this training scope is uncharacterized and expected to degrade.
- Accuracy degradation depends on the quality and representativeness of the out-of-scope test set; sparse or skewed sampling of out-of-scope molecules may not reveal all failure modes.
- NMR spectrum quality (simulation fidelity, experimental noise, spectral resolution) directly affects measured accuracy on out-of-scope molecules and may conflate model degradation with data quality issues.

## Evidence

- [other] The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.: "The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized."
- [other] Compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity) and compare against in-scope baseline.: "Rank predictions by confidence score and compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity). Compare out-of-scope accuracy"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
