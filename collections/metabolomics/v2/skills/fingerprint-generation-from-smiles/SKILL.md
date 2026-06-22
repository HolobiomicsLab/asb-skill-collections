---
name: fingerprint-generation-from-smiles
description: Use when you have molecule IDs from PubChem or HMDB that have been converted to RDKit molecule objects, and you need to create a standardized fingerprint modality to combine with graph-based and physicochemical descriptor features for multimodal deep learning on molecular property prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - RDKit 2020.03.4
  - RDKit
  - numpy
  - pandas
  - scikit-learn
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
---

# fingerprint-generation-from-smiles

## Summary

Generate fixed-length binary fingerprint vectors (Morgan fingerprints) from molecular structures to create compact, machine-learning-ready representations of chemical compounds. This skill converts SMILES or RDKit molecule objects into 2048-bit vectors capturing molecular topology and features for multimodal model training.

## When to use

You have molecule IDs from PubChem or HMDB that have been converted to RDKit molecule objects, and you need to create a standardized fingerprint modality to combine with graph-based and physicochemical descriptor features for multimodal deep learning on molecular property prediction.

## When NOT to use

- Molecule structures have not been validated or converted to RDKit objects — validate structure integrity first.
- You require 3D conformer-dependent fingerprints (e.g., shape-based) — Morgan fingerprints are 2D topology-only.
- Input is already a pre-computed feature table or embedding — fingerprint generation is redundant.

## Inputs

- RDKit molecule objects (validated molecular structures)
- Molecule IDs from PubChem/HMDB with associated metadata (data.csv)

## Outputs

- 2048-bit Morgan fingerprint vectors (numpy arrays)
- Aligned multimodal feature tensors (graph + fingerprint + descriptor stacks)
- Serialized preprocessed features in HDF5 or pickle format

## How to apply

After validating molecular structure integrity via RDKit, invoke RDKit's Morgan fingerprint algorithm on each RDKit molecule object to generate 2048-bit binary vectors. Stack the resulting fingerprint vectors into aligned numpy arrays alongside graph features and physicochemical descriptors. The 2048-bit radius captures local and global molecular topology; this fixed dimensionality ensures all molecules produce tensors of identical shape required for batch processing in PyTorch models. Serialize the aligned multimodal tensors (graph, fingerprint, descriptor stacks) into HDF5 or pickle format for downstream training.

## Related tools

- **RDKit** (Convert molecule IDs to RDKit molecule objects; compute Morgan fingerprints (2048-bit vectors) from molecular structures) — https://www.rdkit.org/
- **numpy** (Stack fingerprint vectors with graph and descriptor modalities into aligned multimodal feature tensors)
- **pandas** (Load and organize molecule IDs and metadata from data.csv)

## Evaluation signals

- Fingerprint tensor shape is (N, 2048) where N is number of molecules, with all entries binary (0 or 1)
- No NaN or null values in fingerprint vectors; all molecules produce valid fingerprints without exceptions
- Fingerprint vectors are identical for identical molecules when run repeatedly (deterministic output)
- Aligned multimodal tensor stacks have matching first dimension across graph, fingerprint, and descriptor modalities (no index misalignment)
- Serialized output file (HDF5 or pickle) loads without corruption and preserves fingerprint dtype and shape

## Limitations

- Morgan fingerprints capture 2D topology only; they do not encode 3D stereochemistry or conformational differences.
- Fixed 2048-bit vector size may be suboptimal for very large or very small molecules; no adaptive radius tuning is performed.
- RDKit version 2020.03.4 is specified; newer versions may produce slightly different fingerprints due to algorithm updates.
- No canonicalization or salting strategy is applied; different SMILES representations of the same molecule will produce identical fingerprints only if converted through the same RDKit canonicalization pipeline.

## Evidence

- [other] Compute Morgan fingerprints (2048-bit vectors) for each molecule using RDKit.: "Compute Morgan fingerprints (2048-bit vectors) for each molecule using RDKit."
- [other] Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy.: "Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy."
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [other] Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training.: "Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training."
