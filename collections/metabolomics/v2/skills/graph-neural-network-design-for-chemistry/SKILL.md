---
name: graph-neural-network-design-for-chemistry
description: Use when you have 1D or 2D NMR spectra (1H and/or 13C) and need to predict
  unknown molecular structure (formula and connectivity) up to ~19 heavy atoms; or
  you have a set of molecular fragment-structure pairs and need to model how fragments
  assemble into complete structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3894
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3314
  tools:
  - transformer architecture
  - convolutional neural network
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

# graph-neural-network-design-for-chemistry

## Summary

Design and train graph neural network architectures to predict molecular properties or structures from spectroscopic data by encoding molecular connectivity and atomic features as node-edge graphs. This skill is essential when molecular topology and atomic relationships are central to the prediction task, such as structure elucidation from NMR spectra or fragment assembly.

## When to use

You have 1D or 2D NMR spectra (1H and/or 13C) and need to predict unknown molecular structure (formula and connectivity) up to ~19 heavy atoms; or you have a set of molecular fragment-structure pairs and need to model how fragments assemble into complete structures. The input is spectroscopic or fragment data that must be mapped to graph-structured outputs where nodes represent atoms and edges represent bonds.

## When NOT to use

- Input spectra are already pre-processed into fixed-length feature vectors with no spatial or relational structure retained.
- The target molecule class is known a priori and you only need to predict a single scalar property (e.g., molecular weight or binding affinity)—use regression or classification instead.
- Molecular structures are simple linear chains or highly stereotyped compounds where graph-based reasoning adds unnecessary complexity.

## Inputs

- 1D NMR spectra (1H and/or 13C chemical shift and intensity arrays)
- Molecular fragment sets (ordered or unordered collection of sub-structures in SMILES or graph format)
- Fragment-structure ground-truth pairs (fragments paired with their assembled target molecular structure)
- Molecular structures in canonical SMILES or graph adjacency format

## Outputs

- Predicted molecular structures (formula and connectivity) in SMILES or graph format
- Assembled molecular structures from input fragments
- Exact structure match predictions (binary: match or no-match)
- Partial assembly correctness scores per molecule

## How to apply

First, extract or prepare ground-truth pairs pairing input spectra (or fragment sets) with target molecular structures in canonical SMILES or graph format. Represent each target structure as a graph where atoms are nodes (with features such as atomic number, hybridization) and bonds are edges (with bond-order labels). Design a graph neural network (or transformer adapted for graph inputs) that accepts spectroscopic features or fragment embeddings and uses attention or message-passing mechanisms to model inter-atomic relationships. Train the model end-to-end using a structure prediction loss (e.g., graph matching accuracy, canonical SMILES string match, or connectivity correctness). Evaluate on held-out test data using exact structure match rate and partial assembly metrics, and document failure patterns across molecular complexity ranges (atom count, branching, ring systems).

## Related tools

- **transformer architecture** (Core model component for assembling molecular fragments into structures via attention-based fragment relationship modeling and for end-to-end spectroscopic-to-structure prediction)
- **convolutional neural network** (Feature extraction from raw spectroscopic data (1D NMR spectra), integrated with transformer to form end-to-end structure prediction pipeline)

## Evaluation signals

- Exact structure match rate on held-out test set (percentage of predicted structures that perfectly match ground-truth SMILES or canonical graph representation)
- Partial assembly correctness: fraction of correctly predicted bonds or atoms in cases of incomplete assembly
- Performance breakdown by molecular complexity (separate metrics for molecules by atom count, branching degree, and presence/absence of ring systems)
- Invariant check: predicted structure must have valid valence and formally correct connectivity graph
- Canonical SMILES string equality (predicted SMILES normalizes to identical string as ground-truth target)

## Limitations

- Effectiveness demonstrated on molecules with up to 19 heavy (non-hydrogen) atoms; scaling to larger molecules is untested.
- Elucidating structure from 1D NMR spectra alone remains extremely challenging due to combinatorial explosion of possible isomers; performance may degrade for highly ambiguous spectra.
- Fragment assembly assumes access to high-quality fragment-structure ground-truth pairs; performance depends critically on training data quality and coverage of chemical space.
- Graph-based models are sensitive to correct bond-type and atom-feature encoding; errors in preprocessing or feature extraction can degrade predictions.

## Evidence

- [intro] transformer architecture for fragment assembly: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] end-to-end integration of CNN and transformer for NMR-to-structure: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] multitask learning framework for structure prediction from 1D NMR: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] evaluation on molecules up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] combinatorial challenge of 1D NMR structure elucidation: "elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion"
