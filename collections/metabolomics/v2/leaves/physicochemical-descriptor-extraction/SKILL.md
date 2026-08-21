---
name: physicochemical-descriptor-extraction
description: Use when when you have validated RDKit molecule objects derived from
  PubChem or HMDB molecule IDs and need to generate quantitative chemical property
  representations as one modality in a multimodal feature tensor for neural network
  training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3318
  - http://edamontology.org/topic_0091
  tools:
  - RDKit 2020.03.4
  - RDKit
  - numpy
  - pandas
  - scikit-learn
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s10489-022-04351-0
  title: Mass Spectrum Transformer
evidence_spans:
- RDKit == 2020.03.4
- numpy == 1.19.1
- implicit in data.csv loading requirement
- scikit-learn == 0.23.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass_spectrum_transformer_cq
    doi: 10.1007/s10489-022-04351-0
    title: Mass Spectrum Transformer
  dedup_kept_from: coll_mass_spectrum_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s10489-022-04351-0
  all_source_dois:
  - 10.1007/s10489-022-04351-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# physicochemical-descriptor-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings) from molecular structures using RDKit to generate quantitative chemical property vectors for multimodal machine learning models. This skill bridges structural chemistry and feature engineering for molecular property prediction.

## When to use

When you have validated RDKit molecule objects derived from PubChem or HMDB molecule IDs and need to generate quantitative chemical property representations as one modality in a multimodal feature tensor for neural network training. Use this skill when graph-based and fingerprint-based representations alone are insufficient to capture interpretable chemical properties.

## When NOT to use

- Input molecules have invalid or incomplete structural information (e.g., partial SMILES, missing bonds); descriptors will be NaN or semantically meaningless.
- Your model architecture does not support concatenated multimodal inputs; graph-only or fingerprint-only models will not benefit from additional descriptor tensors.
- Descriptor values are already precomputed and aligned in your feature table; re-extraction is redundant.

## Inputs

- RDKit molecule objects (converted from PubChem/HMDB IDs)
- Validated molecular structures (SMILES or molecular graphs)

## Outputs

- Physicochemical descriptor vectors (6-dimensional per molecule: MW, logP, HBA, HBD, rotatable bonds, aromatic rings)
- Stacked multimodal descriptor tensors (numpy array or serialized HDF5/pickle)

## How to apply

For each RDKit molecule object in your dataset, compute six descriptor values: molecular weight, logP (partition coefficient), hydrogen bond acceptors (HBA), hydrogen bond donors (HBD), rotatable bonds, and aromatic rings. Extract these using RDKit's descriptor module, which provides standardized calculations based on SMILES or 2D structure. Stack the resulting descriptor vectors (6-dimensional per molecule) into a numpy array aligned with your graph tensors and Morgan fingerprints. Serialize the stacked descriptor tensors alongside graph and fingerprint modalities into a structured output file (HDF5 or pickle format) for downstream model training. Validate that no descriptor values are NaN or out-of-range before serialization.

## Related tools

- **RDKit** (Compute molecular descriptors (MW, logP, HBA, HBD, rotatable bonds, aromatic rings) from validated molecule objects) — https://www.rdkit.org/
- **numpy** (Stack descriptor vectors into aligned multimodal feature tensors alongside graph and fingerprint modalities) — https://numpy.org/
- **pandas** (Load and organize molecule metadata and IDs for descriptor computation workflow) — https://pandas.pydata.org/

## Examples

```
from rdkit import Chem; from rdkit.Chem import Descriptors; mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O'); descriptors = [Descriptors.MolWt(mol), Descriptors.MolLogP(mol), Descriptors.NumHAcceptors(mol), Descriptors.NumHDonors(mol), Descriptors.NumRotatableBonds(mol), Descriptors.NumAromaticRings(mol)]
```

## Evaluation signals

- All six descriptor values (MW, logP, HBA, HBD, rotatable bonds, aromatic rings) are numeric and contain no NaN or inf entries.
- Descriptor tensor shape matches the number of molecules and contains exactly 6 columns per molecule.
- Descriptor values fall within chemically plausible ranges (e.g., MW > 0, logP typically -5 to 5 for drug-like molecules, HBA/HBD ≥ 0).
- Descriptor tensor is serialized and colocated with corresponding graph tensors and Morgan fingerprints in the output HDF5 or pickle file.
- Descriptor computation completes without RDKit errors or warnings indicating invalid molecular structures.

## Limitations

- RDKit descriptor calculations assume valid 2D or 3D molecular structures; invalid or incomplete SMILES/structures will produce NaN or raise exceptions.
- Descriptor values are computed in isolation and do not capture 3D spatial or conformational properties; only 2D graph-based properties are extracted.
- The fixed six-descriptor set (MW, logP, HBA, HBD, rotatable bonds, aromatic rings) may not capture domain-specific chemical properties relevant to your prediction task (e.g., polar surface area, lipophilicity indices); consider extending the descriptor set if required.
- RDKit 2020.03.4 is an older version; compatibility with newer PyTorch or CUDA versions may require upgrading to a current RDKit release.

## Evidence

- [other] Calculate physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings) using RDKit.: "Calculate physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings) using RDKit."
- [other] Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy.: "Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy."
- [other] Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training.: "Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training."
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
