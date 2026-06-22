---
name: fragment-assembly-transformer-architecture
description: Use when when you have 1D NMR spectra (1H and/or 13C) of an unknown compound with up to ~19 heavy atoms and need to predict both molecular formula and connectivity without manual structure hypothesis generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3324
  - http://edamontology.org/topic_0154
  tools:
  - transformer architecture
  - convolutional neural network
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- a transformer architecture can be constructed to efficiently solve the task
- we show how a transformer architecture can be constructed to efficiently solve the task
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

# fragment-assembly-transformer-architecture

## Summary

A transformer-based approach that assembles ordered or unordered sets of molecular fragments into candidate molecular structures using attention mechanisms to model fragment relationships. This skill automates the manual chemist task of structure elucidation from spectroscopic data by learning to predict connectivity and molecular topology from fragment-structure training pairs.

## When to use

When you have 1D NMR spectra (1H and/or 13C) of an unknown compound with up to ~19 heavy atoms and need to predict both molecular formula and connectivity without manual structure hypothesis generation. Specifically, use this skill when the combinatorial explosion of possible structures makes exhaustive enumeration infeasible and you have access to training data of fragment-structure ground truth pairs extracted from deposited molecular datasets.

## When NOT to use

- When input NMR data is from molecules with >19 heavy atoms (model was demonstrated only up to this limit)
- When 2D NMR spectra (HSQC, HMBC, COSY) are available; use those for more direct connectivity information
- When you lack training data of fragment-structure pairs; the transformer requires supervised ground truth to learn assembly patterns

## Inputs

- 1D NMR spectra (1H and/or 13C format)
- Molecular fragment-structure ground truth pairs (SMILES strings or molecular graphs)
- Molecular formula or constraint information

## Outputs

- Predicted molecular structures (canonical SMILES or molecular graphs)
- Structure match accuracy metrics (exact match rate, partial correctness)
- Assembly success/failure patterns indexed by molecular complexity

## How to apply

First, extract or prepare fragment-structure ground truth pairs from a molecular dataset, identifying molecular fragments (substructures or building blocks) and their corresponding assembled target structures in canonical SMILES or graph representation. Build a transformer module that takes an ordered or unordered set of fragments as input tokens and uses self-attention mechanisms to model pairwise fragment relationships, outputting logits over candidate assembled structures. Train the transformer on fragment-structure pairs using a structure prediction loss such as graph matching accuracy or canonical SMILES string matching. Evaluate assembly accuracy on held-out test pairs using metrics such as exact structure match rate and partial assembly correctness. Document failure patterns across molecular complexity ranges (atom count, branching degree, ring system topology) to identify model limitations.

## Related tools

- **transformer architecture** (Core neural network module that encodes fragment relationships via self-attention and decodes candidate molecular structures)
- **convolutional neural network** (Integrated with transformer for end-to-end feature extraction from raw NMR spectral input before fragment assembly)

## Evaluation signals

- Exact structure match rate: percentage of test molecules where predicted canonical SMILES matches ground truth
- Partial assembly correctness: degree of overlap in predicted vs. true molecular subgraphs (e.g., correct connectivity for branching/ring cores even if side chains differ)
- Assembly accuracy stratified by molecular complexity: report success rate separately for molecules binned by heavy atom count, ring count, and branching factor
- Canonical SMILES agreement: verify outputs are valid SMILES strings that canonicalize to single unique representation
- Fragment coverage: confirm all input fragments appear in the assembled structure (no fragments dropped or duplicated)

## Limitations

- Model was demonstrated only on molecules with up to 19 heavy (non-hydrogen) atoms; performance on larger molecules unknown
- Combinatorial explosion of possible structures remains a challenge; effectiveness depends on size of training fragment-structure corpus and diversity of molecular scaffolds
- Assembly failures and success patterns vary across molecular complexity ranges; model may be biased toward certain ring systems or branching patterns seen frequently in training data
- Requires high-quality ground truth fragment-structure pairs; noisy or incorrectly labeled training data will degrade assembly accuracy

## Evidence

- [intro] a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [other] Build a transformer architecture that takes an ordered or unordered set of molecular fragments as input and outputs candidate assembled molecular structures using attention mechanisms for fragment relationship modeling.: "Build a transformer architecture that takes an ordered or unordered set of molecular fragments as input and outputs candidate assembled molecular structures using attention mechanisms"
- [other] Train the transformer module on the fragment-structure pairs using a structure prediction loss (e.g., graph matching or canonical SMILES accuracy).: "Train the transformer module on the fragment-structure pairs using a structure prediction loss (e.g., graph matching or canonical SMILES accuracy)"
- [other] Evaluate fragment assembly accuracy on held-out test pairs, computing metrics such as exact structure match rate and partial assembly correctness.: "Evaluate fragment assembly accuracy on held-out test pairs, computing metrics such as exact structure match rate and partial assembly correctness"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion: "elucidating structure using only one-dimensional (1D) NMR spectra remains an extremely challenging problem because of the combinatorial explosion"
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra: "a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
