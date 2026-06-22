---
name: dataset-serialization-for-deep-learning
description: Use when after generating aligned multimodal feature tensors from molecular structures (graph-based features, Morgan fingerprints, and physicochemical descriptors) and before initiating model training loops.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0154
  tools:
  - RDKit 2020.03.4
  - RDKit
  - numpy
  - pandas
  - scikit-learn
  - h5py
  - pickle
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

# dataset-serialization-for-deep-learning

## Summary

Serialize preprocessed multimodal molecular feature tensors (graph structures, fingerprints, physicochemical descriptors) into structured output files (HDF5 or pickle) aligned for downstream deep learning model training. This skill ensures reproducible, efficient data loading and prevents recomputation of expensive feature engineering steps.

## When to use

After generating aligned multimodal feature tensors from molecular structures (graph-based features, Morgan fingerprints, and physicochemical descriptors) and before initiating model training loops. Use this skill when you have heterogeneous feature modalities that must be co-indexed and efficiently accessed during batch sampling on GPU.

## When NOT to use

- Input is already a serialized HDF5 or pickle file ready for model training (skip to data loading).
- Modalities are not aligned by molecule ID or contain mismatched sample counts (fix alignment in preprocessing first).
- Dataset is small enough to hold entirely in memory and will only be iterated once (in-memory numpy arrays are simpler).

## Inputs

- numpy arrays of graph-based node and edge tensors
- numpy arrays of Morgan fingerprints (2048-bit vectors)
- numpy arrays of physicochemical descriptors (molecular weight, logP, HBA, HBD, rotatable bonds, aromatic rings)
- pandas DataFrame or list of molecule IDs and metadata from data.csv
- aligned index mapping across all feature modalities

## Outputs

- serialized multimodal dataset file in HDF5 or pickle format
- feature schema documentation (modality names, tensor shapes, dtypes, normalization parameters)
- indexed molecule ID mapping with database origin (PubChem/HMDB) for traceability

## How to apply

Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy, ensuring consistent indexing across all modalities by molecule ID from the source data.csv. Serialize the aligned tensors and their metadata (molecule IDs, source database origin, feature provenance) into a structured output file in HDF5 or pickle format. HDF5 is preferred for large-scale datasets (>100K molecules) to enable memory-mapped access; pickle is suitable for smaller datasets. Validate serialization by loading a random subsample and confirming shape consistency, dtype correctness, and index alignment. Document the feature schema (modality names, tensor shapes, dtype, and normalization applied) alongside the serialized file to enable downstream model initialization and hyperparameter tuning.

## Related tools

- **numpy** (Stack and align multimodal feature tensors into contiguous arrays; manage tensor shape and dtype consistency.)
- **pandas** (Load and index molecule IDs and metadata from data.csv; maintain index correspondence across modalities.)
- **h5py** (Serialize aligned tensors and metadata into HDF5 format for memory-mapped access and large-scale datasets.)
- **pickle** (Serialize aligned tensors and metadata into Python pickle format for smaller datasets and rapid prototyping.)
- **RDKit 2020.03.4** (Generate upstream graph, fingerprint, and descriptor features that are then serialized by this skill.)

## Evaluation signals

- Verify that all three modalities (graph, fingerprint, descriptor) are present in the serialized file and have identical sample counts and matching molecule ID indices.
- Load a random subsample from the serialized file and confirm tensor shapes match expectations (e.g., graph nodes/edges match molecule structure complexity, fingerprints are 2048-bit, descriptor count = 6).
- Check that dtype and value ranges are preserved: fingerprints should be binary (0/1) or integer counts; descriptors should be floats with domain-appropriate ranges (e.g., molecular weight > 0, logP typically –5 to +10).
- Verify file size is reasonable for dataset scale (HDF5 should compress well, pickle should fit within available memory).
- Cross-validate a subset of serialized samples against the original upstream feature generation to confirm no data corruption or reordering occurred.

## Limitations

- Serialization format choice (HDF5 vs. pickle) affects memory efficiency and I/O performance; large datasets (>1M molecules) may exceed pickle memory overhead or require memory-mapped access only HDF5 provides.
- No built-in schema validation in pickle; HDF5 is more robust to schema drift and partial reads but requires additional metadata documentation.
- Modality alignment assumes consistent indexing across all feature generation steps; any mismatch in preprocessing will propagate to the serialized file and degrade training.
- The README does not specify compression settings, chunk sizes, or memory-mapping strategies for HDF5; practitioners must tune these for their hardware and dataset scale.

## Evidence

- [other] Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy.: "Stack graph, fingerprint, and descriptor modalities into aligned multimodal feature tensors using numpy."
- [other] Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training.: "Serialize preprocessed features and metadata into a structured output file (HDF5 or pickle format) for downstream model training."
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [readme] the data used for training and test are in data.csv the data is from pubchem and HMDB: "the data used for training and test are in data.csv the data is from pubchem and HMDB"
