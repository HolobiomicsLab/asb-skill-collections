---
name: molecular-fingerprint-generation-rdk
description: Use when you have a set of chemical compounds represented as InChI or
  SMILES strings and need to extract molecular features for input into a neural network
  or traditional ML model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0166
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - rdkit-pypi
  - Python 3.9
  - pandas
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-generation-rdk

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate fixed-length binary or count-based molecular fingerprints from chemical structures (InChI or SMILES) using RDKit, suitable as input features for machine learning models predicting molecular properties such as retention time. This skill encodes chemical structure topology and atom properties into a dense vector representation.

## When to use

You have a set of chemical compounds represented as InChI or SMILES strings and need to extract molecular features for input into a neural network or traditional ML model. Use this skill when your downstream model expects a fixed-length numeric vector representation of molecular structure (as opposed to or in addition to graph-based representations). This is especially relevant when building dual-branch architectures that combine fingerprint and graph inputs, as in retention time prediction pipelines.

## When NOT to use

- You already have pre-computed fingerprints or feature vectors in your data; fingerprint generation is redundant.
- Your model architecture is graph-only (e.g., pure graph neural networks without a fingerprint branch); graph representations alone may be more appropriate.
- Input chemical identifiers are malformed, unparseable, or contain mixtures of SMILES and InChI with inconsistent formatting; pre-cleaning is required.

## Inputs

- CSV file with 'InChI' column (or 'SMILES' column) containing chemical structure identifiers
- List of InChI or SMILES strings
- RDKit Mol objects (optional intermediate)

## Outputs

- NumPy array or PyTorch tensor of shape [num_molecules, fingerprint_length] with numeric dtype (int or float)
- Fingerprint features suitable for concatenation or fusion with other molecular representations

## How to apply

Load molecular structures from a CSV file containing an 'InChI' column (or SMILES column). Use RDKit's Python API to convert each InChI/SMILES string into a Mol object, then generate a standard fingerprint (e.g., Morgan/circular fingerprint, RDKit bit-vector fingerprint, or atom-pair fingerprint) by calling RDKit's fingerprinting functions. Specify the fingerprint bit length (typically 1024 or 2048 bits) and any radius/diameter parameters relevant to the fingerprint type. Stack all fingerprints into a tensor of shape [num_molecules, fingerprint_length] and validate that (1) no molecules failed to parse (check for None Mol objects), (2) all fingerprints have the same length, and (3) the tensor contains only numeric values (0/1 for bit vectors, or counts for count-based fingerprints). This tensor then serves as one branch input to architectures like RT-Transformer.

## Related tools

- **rdkit-pypi** (Core library for molecular structure parsing (InChI/SMILES to Mol) and fingerprint generation (Morgan, RDKit bit-vector, atom-pair fingerprints)) — https://www.rdkit.org/
- **Python 3.9** (Programming language for executing RDKit API calls and tensor construction)
- **torch** (Convert NumPy fingerprint arrays to PyTorch tensors for downstream model training) — https://pytorch.org/
- **pandas** (Load and manipulate CSV files containing InChI/SMILES and metadata) — https://pandas.pydata.org/

## Examples

```
from rdkit import Chem; import pandas as pd; data = pd.read_csv('data.csv'); mols = [Chem.MolFromInchi(inchi) for inchi in data['InChI']]; fps = [Chem.AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024) for mol in mols if mol]; fingerprints = np.array([np.array(fp) for fp in fps])
```

## Evaluation signals

- Fingerprint tensor shape is [num_molecules, fixed_fingerprint_length] with no missing or NaN values.
- All molecules in input CSV successfully parse to RDKit Mol objects; no None objects in the batch.
- Fingerprint values are numeric (dtype int32/int64 for bit vectors, float32/float64 for counts); no strings or object types.
- Fingerprint tensor can be concatenated or fused without shape mismatch when combined with other feature branches (e.g., graph embeddings in dual-branch RT-Transformer).
- Fingerprint bit length matches the model's expected input dimension (e.g., 1024 or 2048 bits).

## Limitations

- Fingerprints lose 3D conformational and stereochemical detail; they encode only 2D topology and atom types, which may limit predictive power for properties sensitive to 3D geometry.
- InChI and SMILES parsing can fail for malformed or non-standard chemical identifiers; error handling and validation are required.
- Different fingerprint types (Morgan, RDKit bit-vector, atom-pair) encode different chemical information; choice of fingerprint must be justified for the target property (e.g., retention time prediction).
- Fixed fingerprint length may not capture variable-sized or large molecules optimally; fingerprints are lossy representations.
- Requires RDKit installation and dependency resolution (rdkit-pypi); environment setup can be complex on some systems.

## Evidence

- [other] Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects.: "Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects."
- [other] The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch.: "The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch"
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [readme] Prepare your dataset as a csv file which has 'InChI' and 'RT' columns.: "Prepare your dataset as a csv file which has "InChI" and "RT" columns."
