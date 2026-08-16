---
name: nmr-spectrum-to-structure-inference
description: Use when you have 1D NMR spectra (¹H or ¹³C or both) for an unknown organic
  compound with ≤19 heavy atoms and need to rapidly predict its molecular formula
  and connectivity graph without manual peak interpretation or exhaustive combinatorial
  search.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - Transformer architecture
  - Convolutional neural network
  techniques:
  - NMR
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectrum-to-structure-inference

## Summary

Use a multitask transformer–CNN architecture to predict molecular structure (formula and connectivity) directly from 1D ¹H and/or ¹³C NMR spectra. This skill automates the chemist's task of assembling molecular fragments into complete structures, applicable to molecules with up to 19 heavy atoms.

## When to use

You have 1D NMR spectra (¹H or ¹³C or both) for an unknown organic compound with ≤19 heavy atoms and need to rapidly predict its molecular formula and connectivity graph without manual peak interpretation or exhaustive combinatorial search.

## When NOT to use

- Molecule contains >19 heavy atoms: generalization beyond this scope is uncharacterized and accuracy degradation is expected.
- Only 2D or higher-dimensional NMR data (COSY, HSQC, HMBC) are available: the model is trained exclusively on 1D spectra.
- Spectrum is severely noisy, undecayed, or distorted: preprocessing must clean the spectrum before model input to avoid spurious predictions.

## Inputs

- 1D ¹H NMR spectrum (intensity vs. chemical shift, ppm scale)
- 1D ¹³C NMR spectrum (intensity vs. chemical shift, ppm scale)
- Pretrained transformer–CNN model checkpoint
- Ground-truth molecular structure (connectivity graph, molecular formula) for evaluation

## Outputs

- Predicted molecular formula (elemental composition)
- Predicted molecular connectivity graph (atoms and bonds)
- Top-k candidate structures (ranked by model confidence score)
- Top-1, top-3, top-5 structure recovery accuracy (fraction of correct predictions)

## How to apply

Load a pretrained NMR2Struct checkpoint (transformer encoder + CNN decoder). Preprocess the input 1D NMR spectrum into a standardized numerical representation (e.g., intensity array over chemical shift bins). Feed the spectrum through the CNN to extract spectral features, then pass features through the transformer to assemble molecular fragments into a candidate structure graph. Rank predictions by model confidence score and report top-k accuracy (top-1, top-3, top-5). Validate predictions by comparing predicted connectivity and molecular formula against ground-truth structures from reference databases (PubChem, ChemSpider). The framework's multitask design jointly learns formula prediction and connectivity inference, leveraging the combinatorial constraints between these tasks to reduce the search space from exponential to tractable.

## Related tools

- **Transformer architecture** (Encodes spectral features and assembles molecular fragments into connectivity graphs via multi-head attention over fragment embeddings)
- **Convolutional neural network** (Extracts local and global features from 1D NMR spectra for downstream transformer encoding)

## Evaluation signals

- Top-1 accuracy (fraction of test cases where the model's highest-confidence prediction exactly matches ground-truth connectivity and molecular formula) should match or exceed reported in-scope baseline (≤19 heavy atoms).
- Top-3 and top-5 accuracy should show a consistent ranking distribution, with ground-truth appearing in the top-k predictions for most test cases.
- Predicted molecular formula (element counts) must match ground-truth elemental composition for each test compound.
- Connectivity graph topology (bond order, atom connectivity) must be isomorphic to the ground-truth structure graph when accuracy is positive.
- Error analysis: inspect cases where predictions fail; track failure modes (e.g., incorrect valence, disconnected fragments, impossible stereochemistry) and report their prevalence relative to random baseline.

## Limitations

- Framework effectiveness is demonstrated only on molecules with up to 19 heavy atoms; performance on larger molecules is unknown and likely degraded.
- Combinatorial explosion of possible structures grows with molecule size; the model's capacity to handle molecules beyond training scope is not validated.
- Accuracy depends on spectrum quality: simulated, experimental, or database spectra must be aligned in preprocessing (chemical shift calibration, peak resolution) for reliable inference.
- Model is trained on ¹H and/or ¹³C NMR data; other nuclei (¹⁹F, ³¹P) or heteronuclear correlation spectra are out of scope.

## Evidence

- [intro] Demonstrates effectiveness on molecules ≤19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] Multitask learning predicts formula and connectivity from 1D NMR: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] Transformer solves fragment assembly task: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] CNN–transformer integration for end-to-end prediction: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] Combinatorial explosion is a fundamental challenge: "elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion"
