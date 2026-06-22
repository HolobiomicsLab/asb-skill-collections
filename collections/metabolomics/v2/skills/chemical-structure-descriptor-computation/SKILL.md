---
name: chemical-structure-descriptor-computation
description: Use when when you have a set of molecular structures (N-Me derived unsaturated sterol lipids or structurally similar organic molecules with C=C bonds) represented as SMILES or molecular geometry files, and you need to train or apply a machine-learning model to predict an instrument-dependent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_2814
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - scikit-learn
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- collection of Python scripts
- All functions are implemented in jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_na_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_na_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Chemical Structure Descriptor Computation

## Summary

Compute quantum chemistry-derived structural descriptors (3D conformations, electronic properties) for organic molecules to serve as features for machine-learning models such as collision cross section (CCS) prediction. This skill bridges ab initio or semi-empirical quantum calculations with downstream supervised learning for physicochemical property estimation.

## When to use

When you have a set of molecular structures (N-Me derived unsaturated sterol lipids or structurally similar organic molecules with C=C bonds) represented as SMILES or molecular geometry files, and you need to train or apply a machine-learning model to predict an instrument-dependent property (e.g., CCS in ion mobility spectrometry) that requires 3D conformational and electronic information not easily captured by 2D fingerprints alone.

## When NOT to use

- Input molecules are already represented in a pre-computed feature matrix or fingerprint space (e.g., ECFP6 or Morgan fingerprints) — use feature selection or model training directly instead.
- The target property is independent of 3D structure or electronic properties (e.g., predicting molecular weight from a name) — simpler 2D descriptors or lookup tables suffice.
- Computational budget is severely constrained and quantum chemistry runtime is prohibitive for the dataset size; consider empirical or machine-learning-only descriptor alternatives.

## Inputs

- SMILES strings or molecular geometry files for N-Me derived unsaturated sterol lipids
- Specification of structural variants (e.g., double-bond positions for isomers)
- Quantum chemistry method parameters (basis set, functional, convergence thresholds)

## Outputs

- 3D conformational structures (coordinate files or in-memory representations)
- Electronic structure data (orbital energies, electron densities, dipole moments)
- Feature matrix: rows = molecules, columns = computed descriptors (numeric array or DataFrame indexed by lipid identifier and isomer class)

## How to apply

Prepare structural input data as SMILES strings or 3D molecular geometry files for each lipid or variant. Execute quantum chemistry calculations (e.g., geometry optimization, electronic structure analysis) to generate 3D conformations and compute electronic descriptors for each structure. Extract features (bond lengths, angles, electronic densities, polarizability tensors, etc.) from the quantum outputs. Normalize or standardize these features and assemble into a feature matrix indexed by molecular identifier. Validate that descriptors capture expected chemical variation (e.g., distinct features for isomers with different double-bond positions) before passing to the machine-learning model. The workflow is typically executed in Python using RDKit (for structure manipulation) and quantum chemistry packages, with feature extraction and ML training handled via scikit-learn.

## Related tools

- **RDKit** (Parses SMILES, recognizes double-bond positions, generates 3D coordinates, and manipulates molecular structures for quantum chemistry input preparation)
- **Python** (Host language for orchestrating quantum chemistry calculations, feature extraction, and data compilation into tabular datasets)
- **Jupyter Notebook** (Interactive development and execution environment for the full descriptor computation and validation workflow)
- **scikit-learn** (Feature normalization, model training (SVR with LASSO feature selection), and cross-validation for downstream CCS prediction)

## Evaluation signals

- Quantum chemistry calculations converge for all input structures; geometry optimization achieves target energy gradient or SCF convergence criterion.
- Computed descriptors are numeric, finite, and free of NaN or Inf values; descriptor ranges and distributions are sensible for the chemical class (e.g., lipid dipole moments and polarizabilities fall within expected literature ranges).
- Structural isomers (e.g., different double-bond positions) produce distinct descriptor vectors; principal-component analysis or t-SNE visualization shows clear separation by isomer class.
- Descriptor values correlate meaningfully with the downstream property (CCS): Pearson or Spearman correlation with experimental or benchmark CCS values is non-trivial (|r| > 0.5–0.7 depending on data quality).
- Feature matrix dimensions match expectations: n_samples = number of lipid variants, n_features = number of computed descriptors; no row or column is constant or all-zero.

## Limitations

- Quantum chemistry calculations are computationally expensive and scale poorly with molecular size; for very large datasets or large lipids, approximations (semi-empirical methods, machine-learning geometry prediction) or pre-screening may be necessary.
- The article tests the MS/MS fragmentation script 'only [on] sterol lipids' despite theoretical applicability to all C=C-containing molecules; generalization to other functional groups or stereochemistry patterns is not empirically validated.
- Descriptor quality depends critically on quantum method choice (basis set, functional), which is not fully specified in the README; poor choice can lead to non-transferable or physically unrealistic features.
- Predicted CCS values must be validated against reference standards or experimental benchmarks; the skill outputs feature matrices, not validated predictions — downstream model training is required.

## Evidence

- [other] Prepare structural input data for N-Me derived unsaturated sterol lipids (SMILES or molecular geometry files). Execute quantum chemistry calculations to generate 3D conformational and electronic structure data for each lipid variant.: "Prepare structural input data for N-Me derived unsaturated sterol lipids (SMILES or molecular geometry files). 2. Execute quantum chemistry calculations to generate 3D conformational and electronic"
- [other] Apply machine-learning CCS prediction model trained on quantum chemistry features to estimate CCS values for the full lipid dataset. Compile predicted CCS values into a tabular dataset indexed by lipid identifier and structural isomer class.: "Apply machine-learning CCS prediction model trained on quantum chemistry features to estimate CCS values for the full lipid dataset. 4. Compile predicted CCS values into a tabular dataset indexed by"
- [readme] The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [readme] The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR model.: "The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR"
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
