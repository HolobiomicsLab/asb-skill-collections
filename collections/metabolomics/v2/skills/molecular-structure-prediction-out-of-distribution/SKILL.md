---
name: molecular-structure-prediction-out-of-distribution
description: Use when your goal is to assess whether a pretrained NMR2Struct model trained on molecules ≤19 heavy atoms can generalize to larger, more complex molecules, or whether accuracy degrades significantly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3520
  tools:
  - NMR2Struct model (transformer + CNN)
  - PubChem or equivalent molecular database
  techniques:
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Structure Prediction Out-of-Distribution

## Summary

Extend and evaluate a trained NMR2Struct deep learning model (transformer + CNN) on molecules exceeding its training scope (>19 heavy atoms) to characterize accuracy degradation and failure modes in out-of-distribution settings. This skill identifies the limits of the model's generalization and quantifies performance loss as molecular complexity increases beyond the original training boundary.

## When to use

Your goal is to assess whether a pretrained NMR2Struct model trained on molecules ≤19 heavy atoms can generalize to larger, more complex molecules, or whether accuracy degrades significantly. Apply this skill when you have access to a pretrained checkpoint, 1D ¹H and/or ¹³C NMR spectra for molecules with >19 heavy atoms (from experiment, simulation, or database), and ground-truth molecular connectivity labels. This skill is essential for establishing the actual performance boundary of the model and identifying whether further training or architectural changes are needed for larger molecules.

## When NOT to use

- Your test molecules are already within the training scope (≤19 heavy atoms); use standard in-distribution validation instead.
- You do not have ground-truth connectivity labels or SMILES for the test set; the skill requires reference labels to compute recovery accuracy.
- Your NMR spectra are of poor quality (low signal-to-noise, artifacts, or incomplete peak assignments); preprocessing and quality filtering must precede this skill.

## Inputs

- Pretrained NMR2Struct model checkpoint (transformer + CNN architecture)
- 1D ¹H NMR spectra for molecules with >19 heavy atoms
- 1D ¹³C NMR spectra for molecules with >19 heavy atoms
- Ground-truth molecular connectivity graphs (SMILES, graphs, or adjacency matrices)
- Molecular formula labels for test molecules

## Outputs

- Top-1, top-3, and top-5 structure recovery accuracy metrics
- Predicted connectivity graphs and molecular formulas for each test molecule
- Comparison report of in-scope vs. out-of-scope accuracy (absolute and relative degradation)
- Error distribution analysis and failure mode documentation
- Confidence score distributions for correct vs. incorrect predictions

## How to apply

Load the pretrained NMR2Struct model (transformer + CNN checkpoint) and a held-out test set of molecules with >19 heavy atoms sourced from PubChem or equivalent public databases. For each out-of-scope molecule, obtain or generate 1D ¹H and/or ¹³C NMR spectra (via simulation, experimental measurement, or database retrieval). Feed each spectrum through the model to generate predicted molecular formula and connectivity graphs, ranked by confidence score. Compute top-1, top-3, and top-5 structure recovery accuracy metrics (fraction of predictions matching ground-truth connectivity) and compare these against the reported in-scope baseline (molecules ≤19 heavy atoms). Quantify both absolute and relative degradation in accuracy, and document the error distribution and failure modes (e.g., which types of bonds or functional groups are most often mispredicted). The rationale is that systematic evaluation beyond the training distribution reveals not only the hard limit of the model but also how gracefully or catastrophically performance degrades, informing decisions about model retraining, ensemble methods, or hybrid human-AI workflows.

## Related tools

- **NMR2Struct model (transformer + CNN)** (Pretrained deep learning model that ingests 1D NMR spectra and outputs predicted molecular formula and connectivity graphs; forms the core of this out-of-distribution evaluation.)
- **PubChem or equivalent molecular database** (Source for retrieving test molecules with >19 heavy atoms, their ground-truth structures (SMILES, SDF), and optionally pre-computed or experimental NMR spectra.)

## Evaluation signals

- Top-1, top-3, and top-5 accuracy values are computed and reported separately for out-of-scope molecules; compare to the reported baseline accuracy for in-scope molecules (≤19 heavy atoms).
- Absolute accuracy loss and relative percentage degradation are quantified (e.g., 'accuracy dropped from 85% to 62%, a 27% relative loss').
- Error distribution is analyzed by molecular property (e.g., accuracy vs. number of heavy atoms, functional group type) to identify which molecular features trigger failure.
- Confidence score distributions are examined for correct vs. incorrect predictions; poorly calibrated confidence (high scores on wrong predictions) indicates the model is not aware of its own out-of-distribution status.
- Failure mode documentation includes examples of common mispredictions (e.g., incorrect bond types, missed rings, wrong functional group assignments) to guide future model improvements.

## Limitations

- The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms; generalization beyond this scope is uncharacterized and expected to degrade.
- Out-of-distribution performance depends on the availability and quality of NMR spectra for larger molecules; simulated spectra may not capture experimental artifacts or peak broadening effects that occur in real high-molecular-weight compounds.
- The transformer + CNN architecture may not scale efficiently or accurately to the combinatorial complexity of larger molecules; architectural modifications or additional training may be required for molecules with 20–30+ heavy atoms.

## Evidence

- [other] The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.: "The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized."
- [intro] A multitask machine learning framework can predict molecular structure (formula and connectivity) from 1D 1H and/or 13C NMR spectra.: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] The transformer and convolutional neural network are integrated for end-to-end structure prediction from spectra.: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [other] Top-1, top-3, and top-5 structure recovery accuracy should be ranked by confidence score and compared against baseline.: "Rank predictions by confidence score and compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity)"
- [other] Accuracy metrics for out-of-scope molecules should be compared to in-scope baseline and degradation quantified.: "Compare out-of-scope accuracy metrics against the reported in-scope baseline (molecules ≤19 heavy atoms) and quantify the absolute and relative degradation."
