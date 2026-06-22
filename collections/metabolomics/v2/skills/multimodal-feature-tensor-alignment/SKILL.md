---
name: multimodal-feature-tensor-alignment
description: Use when when you have molecule IDs converted to multiple independent feature modalities (graph-based node/edge tensors from RDKit, Morgan fingerprints, and computed physicochemical descriptors) and need to combine them into a single structured tensor representation for multimodal model training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3366
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3372
  tools:
  - RDKit 2020.03.4
  - RDKit
  - numpy
  - pandas
  - scikit-learn
  - torch
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multimodal-feature-tensor-alignment

## Summary

Aligns and stacks heterogeneous molecular feature representations (graph tensors, fingerprints, physicochemical descriptors) into coherent multimodal tensors for joint model training. This skill ensures that diverse structural and chemical modalities are combined into compatible array structures suitable for downstream neural network ingestion.

## When to use

When you have molecule IDs converted to multiple independent feature modalities (graph-based node/edge tensors from RDKit, Morgan fingerprints, and computed physicochemical descriptors) and need to combine them into a single structured tensor representation for multimodal model training, particularly when using graph neural networks or attention-based architectures that consume aligned feature stacks.

## When NOT to use

- Input molecules are already represented as a single pre-computed feature table (e.g., a fixed descriptor matrix); alignment is unnecessary.
- Modalities have fundamentally incompatible temporal or spatial scales that cannot be meaningfully normalized (e.g., time-series kinetics mixed with static molecular structure without explicit alignment protocol).
- Feature counts or shapes are inconsistent across molecules and the application cannot tolerate padding or imputation strategies.

## Inputs

- List of molecule IDs sourced from PubChem/HMDB
- data.csv file containing molecule IDs and metadata
- RDKit-validated molecule objects
- Graph-based feature tensors (node and edge tensors per molecule)
- Morgan fingerprint vectors (2048-bit)
- Physicochemical descriptor arrays (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings)

## Outputs

- Aligned multimodal feature tensors (numpy or torch arrays)
- Serialized preprocessed features (HDF5 or pickle format)
- Metadata index linking molecule IDs to feature rows
- Training/test split datasets ready for model ingestion

## How to apply

After generating graph features (node and edge tensors), 2048-bit Morgan fingerprints, and physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings count) for each molecule using RDKit, use numpy operations to stack these heterogeneous modalities into aligned feature tensors. Ensure all molecules have consistent tensor shapes across modalities (padding graphs if necessary, maintaining fixed fingerprint bit width, normalizing descriptor scales). Stack the aligned modalities using numpy.concatenate or numpy.stack along a modality dimension, then serialize the result into HDF5 or pickle format with accompanying metadata for reproducible downstream model training. Validation involves confirming that the output tensor shape matches (num_molecules, total_feature_dim) and that no NaN or inf values were introduced during stacking.

## Related tools

- **RDKit** (Generates graph-based features (node/edge tensors), Morgan fingerprints, and physicochemical descriptors from molecule objects prior to alignment)
- **numpy** (Stacks and aligns heterogeneous feature modalities into coherent tensor structures)
- **pandas** (Loads and manages molecule ID metadata from data.csv to map IDs to feature indices during alignment)
- **torch** (Optional downstream consumer of aligned tensors for neural network model training)
- **scikit-learn** (Normalization and scaling of physicochemical descriptors prior to stacking to ensure modality balance)

## Evaluation signals

- Output tensor shape is (num_molecules, aligned_feature_dim) with no missing or ragged rows; all molecules present in data.csv produce rows in output
- No NaN, inf, or out-of-range values present in serialized tensors; descriptor values fall within expected chemical ranges (e.g., molecular weight > 0, logP in [-10, 10])
- Morgan fingerprints retain exactly 2048 bits per molecule; graph tensors have consistent node/edge dimensions across all molecules (padded if needed)
- Serialized format (HDF5 or pickle) loads without error and tensor dimensions match the expected (num_molecules, feature_dim) schema
- Metadata index correctly maps molecule IDs from data.csv to row indices in the output tensor; round-trip retrieval of a known molecule ID returns the correct feature vector

## Limitations

- Assumes all molecule IDs in data.csv can be successfully converted to valid RDKit molecule objects; molecules with invalid SMILES or missing structures will be dropped or raise exceptions.
- Physicochemical descriptor computation depends on RDKit version (2020.03.4 pinned); newer RDKit versions may compute descriptors differently, leading to non-reproducible results.
- No explicit handling of variable-size molecular graphs; graph padding strategy (if employed) must be specified separately; very large molecules may exceed memory constraints.
- Normalization/scaling of descriptors is not specified in the README; practitioners must implement their own standardization (e.g., z-score, min-max) before stacking to ensure balanced contribution across modalities.
- Output file format (HDF5 vs. pickle) choice affects downstream portability and compression; no guidance provided on optimal choice for large-scale datasets.

## Evidence

- [other] Generate graph-based features (node and edge tensors) from molecular structures using RDKit.: "Generate graph-based features (node and edge tensors) from molecular structures using RDKit."
- [other] Compute Morgan fingerprints (2048-bit vectors) for each molecule using RDKit.: "Compute Morgan fingerprints (2048-bit vectors) for each molecule using RDKit."
- [other] Calculate physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings) using RDKit.: "Calculate physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings) using RDKit."
- [other] Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy.: "Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy."
- [other] Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training.: "Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training."
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [readme] the data is from pubchem and HMDB,due to the copyright we just list the id of molecules in the file.: "the data is from pubchem and HMDB,due to the copyright we just list the id of molecules in the file."
