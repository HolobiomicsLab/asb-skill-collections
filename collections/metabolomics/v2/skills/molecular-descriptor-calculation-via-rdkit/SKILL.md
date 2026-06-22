---
name: molecular-descriptor-calculation-via-rdkit
description: Use when when you have a set of SMILES strings representing small molecules and need to generate a unified descriptor feature matrix for downstream machine learning (e.g., retention time prediction, property regression).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3315
  tools:
  - RDKit
  - mordred
  - NumPy
  - pandas
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- from rdkit import Chem
- from rdkit import Chem from rdkit.Chem import Descriptors
- import mordred from mordred import Calculator, descriptors
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-descriptor-calculation-via-rdkit

## Summary

Compute molecular descriptors from SMILES strings using RDKit and mordred libraries, deduplicate descriptors across both libraries, and export unified feature matrices in compressed NumPy format. This skill enables rapid featurization of chemical structures for machine learning on retention times and other physicochemical properties.

## When to use

When you have a set of SMILES strings representing small molecules and need to generate a unified descriptor feature matrix for downstream machine learning (e.g., retention time prediction, property regression). Use this skill if you require both RDKit's fast, standard descriptors and mordred's extended descriptor set, without redundancy between libraries.

## When NOT to use

- Input is already a preprocessed feature table or descriptor matrix — skip to model training.
- Your molecules are too large or contain structures not well-supported by RDKit/mordred (e.g., metals, exotic scaffolds) — descriptor calculation may fail or produce NaN values.
- You require only a small, curated set of domain-specific descriptors; computing the full RDKit + mordred set will introduce unnecessary dimensionality and compute overhead.

## Inputs

- SMILES strings (text)
- RDKit molecule objects (converted from SMILES)
- List of RDKit descriptor names
- List of mordred descriptor names

## Outputs

- Unified descriptor feature matrix (NumPy array)
- Compressed NumPy file (.npz)
- Optional CSV, .npy, or .pkl serializations
- List of deduplicated descriptor names

## How to apply

Parse input SMILES strings into RDKit molecule objects; calculate RDKit descriptors using RDKit's descriptor module. In parallel, calculate mordred descriptors using the full descriptor set from the mordred Calculator. Remove mordred descriptors that duplicate RDKit descriptors using the remove_mordred_duplicates function (keeping RDKit versions to avoid redundancy). Optionally normalize numerical descriptor features by division (e.g., dividing by domain-specific scaling factors). Concatenate the deduplicated descriptor arrays into a single NumPy feature matrix. Save the resulting matrix in compressed .npz format for efficient storage and downstream model training.

## Related tools

- **RDKit** (Fast, standard molecular descriptor computation from SMILES and molecule objects)
- **mordred** (Extended molecular descriptor calculator; run in parallel with RDKit to populate additional descriptor features)
- **NumPy** (Array operations, concatenation, and compressed serialization (.npz) of descriptor matrices)
- **pandas** (Optional CSV export and tabular inspection of descriptor features)

## Examples

```
from rdkit import Chem; from mordred import Calculator, descriptors; import numpy as np; mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]; rdkit_descriptors = [Chem.Descriptors.CalcMolWt(m) for m in mols]; calc = Calculator(descriptors, ignore_3D=True); mordred_descriptors = [calc(m) for m in mols]; cleared_mordred_descriptors, _ = remove_mordred_duplicates(mordred_descriptors, rdkit_descriptors); features = np.concatenate([rdkit_descriptors, cleared_mordred_descriptors], axis=1); np.savez_compressed('descriptors.npz', features=features)
```

## Evaluation signals

- Verify that the output descriptor matrix has correct shape (n_molecules × n_unique_descriptors) with no NaN or inf values exceeding a pre-defined tolerance threshold.
- Confirm that duplicate descriptors have been removed by checking that descriptor names from mordred do not overlap with RDKit names after deduplication.
- Validate that all SMILES strings successfully converted to valid RDKit molecule objects and that descriptor calculation did not fail on any molecule.
- Compare .npz file size and descriptor count against a baseline calculation to ensure deduplication reduced redundancy as expected.
- Spot-check descriptor ranges and distributions (e.g., molecular weight, logP) against known chemical property ranges to detect outliers or calculation failures.

## Limitations

- Molecules with invalid SMILES strings or structures not recognizable by RDKit will fail to generate descriptors; incomplete SMILES or exotic atoms may produce NaN values.
- Descriptor calculation is compute-intensive for large datasets; processing time scales roughly linearly with molecule count.
- Some mordred descriptors may be computationally expensive or numerically unstable; optional tolerance thresholds should be applied to remove descriptors with excessive broken or missing values.
- The deduplication step assumes RDKit and mordred compute the same descriptor using identical formulas; minor numerical differences between implementations are not detected.
- No built-in handling of stereochemistry or isotopic labeling variants; SMILES canonicalization must be performed upstream if required.

## Evidence

- [other] The Calc_Descriptors routine retrieves descriptor names from both RDKit and mordred libraries, removes duplicate descriptors that exist in both libraries (keeping RDKit versions), and combines them with extra custom headers to create a unified descriptor feature set: "retrieves descriptor names from both RDKit and mordred libraries, removes duplicate descriptors that exist in both libraries (keeping RDKit versions), and combines them with extra custom headers to"
- [other] Parse input SMILES strings and convert to RDKit molecule objects. Calculate RDKit descriptors using RDKit's descriptor module. Calculate mordred descriptors using the mordred Calculator with the full descriptor set.: "Parse input SMILES strings and convert to RDKit molecule objects. 2. Calculate RDKit descriptors using RDKit's descriptor module. 3. Calculate mordred descriptors using the mordred Calculator with"
- [other] Remove mordred descriptors that duplicate RDKit descriptors using remove_mordred_duplicates function. Optionally normalize numerical descriptor features by division: "Remove mordred descriptors that duplicate RDKit descriptors using remove_mordred_duplicates function. 5. Optionally normalize numerical descriptor features by division"
- [other] Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix. Save the resulting descriptor matrix in compressed NumPy format (.npz): "Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix. 7. Save the resulting descriptor matrix in compressed NumPy format (.npz)"
- [results] cleared_mordred_descriptors, duplicate_indeces = remove_mordred_duplicates(cleared_mordred_descriptors, rdkit_descriptors): "cleared_mordred_descriptors, duplicate_indeces = remove_mordred_duplicates(cleared_mordred_descriptors, rdkit_descriptors)"
- [results] def save_features(path: str, features: List[np.ndarray]): np.savez_compressed(path, features=features): "def save_features(path: str, features: List[np.ndarray]): np.savez_compressed(path, features=features)"
