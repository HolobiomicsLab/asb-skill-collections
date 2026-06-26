---
name: infrared-spectral-prediction-task-design
description: Use when when you have a dataset of molecules with experimentally measured
  or simulated infrared spectra and want to train a graph neural network to predict
  spectral features (e.g., absorption peaks, intensities) from molecular structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - chemprop
  - chemprop-IR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations
  for Property Prediction]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir_cq
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  dedup_kept_from: coll_chemprop_ir_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.1c00055
  all_source_dois:
  - 10.1021/acs.jcim.1c00055
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# infrared-spectral-prediction-task-design

## Summary

Design and implement an infrared spectral prediction task by extending a message passing neural network (chemprop) with spectral feature processing and output layers. This skill enables molecular property models to predict infrared absorption spectra from molecular graphs.

## When to use

When you have a dataset of molecules with experimentally measured or simulated infrared spectra and want to train a graph neural network to predict spectral features (e.g., absorption peaks, intensities) from molecular structure. Use this skill if your goal is to extend an existing chemprop implementation with spectral-specific featurization and loss functions rather than predicting scalar molecular properties.

## When NOT to use

- Your goal is to predict a scalar molecular property (e.g., logP, melting point, solubility) — use base chemprop directly instead.
- You lack a documented chemprop-IR source repository or architectural specification — you cannot reliably reverse-engineer spectral modifications without reference.
- Your infrared data are already preprocessed into hand-crafted feature vectors — task design assumes raw or minimally processed spectra that require end-to-end learning.

## Inputs

- Molecular graph representations (SMILES or molecular structure data)
- Experimental or simulated infrared spectra (wavenumber–intensity pairs or spectral features)
- Base chemprop repository source code
- chemprop-IR repository source code documenting architectural modifications

## Outputs

- Extended chemprop model architecture with spectral feature modules and output layers
- Featurization pipeline for infrared spectral prediction
- Loss functions and metrics for spectral prediction tasks
- Reconstructed model documentation with layer counts, tensor shapes, and parameter counts

## How to apply

Begin by cloning the base chemprop repository to understand the core message passing architecture and model classes. Then access the chemprop-IR extension to identify spectral-feature additions and modifications relative to base chemprop. Extract all new layers, input processing steps, and loss functions specific to infrared spectral prediction from the chemprop-IR source code. Modify chemprop's model definition to incorporate spectral feature handling, featurization modules, and output layers that produce infrared spectral predictions rather than scalar values. Finally, validate that your reconstructed architecture matches the documented chemprop-IR structure by comparing layer counts, input/output tensor shapes, and parameter counts against reference checkpoints or model summary documentation to ensure correctness.

## Related tools

- **chemprop** (Base message passing neural network framework extended with spectral feature handling and infrared prediction output layers) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extension of chemprop documenting spectral-specific architectural modifications, featurization modules, and loss functions for infrared spectral prediction) — github:gfm-collab__chemprop-IR

## Examples

```
# Clone base chemprop, examine core architecture
git clone https://github.com/chemprop/chemprop && cd chemprop
# Access chemprop-IR to extract spectral modifications
# Modify model.py to add spectral feature layers and infrared output head
# Validate tensor shapes: molecular_graphs -> message_passing -> spectral_features -> [wavenumber, intensity, ...] predictions
```

## Evaluation signals

- Layer-by-layer comparison: reconstructed model layer counts, types, and parameter counts match documented chemprop-IR reference checkpoints exactly
- Tensor shape validation: input/output tensor shapes for molecular graphs and spectral features conform to expected dimensions throughout the pipeline
- Model summary consistency: model summary documentation (e.g., from model.summary() or equivalent) matches the published chemprop-IR specification
- Featurization module verification: spectral feature input processing and molecular graph encoding produce activations within expected value ranges
- Checkpoint loading test: trained chemprop-IR model checkpoints load without shape or parameter mismatches into reconstructed architecture

## Limitations

- No changelog was found in the chemprop-IR repository, making it difficult to trace incremental modifications from base chemprop or identify deprecated components
- Architecture reconstruction depends entirely on source code availability and clarity; undocumented or obfuscated spectral modifications cannot be reliably identified
- The skill assumes infrared spectra are available in a consistent format (e.g., wavenumber–intensity pairs or fixed-length spectral vectors); heterogeneous spectral formats require additional preprocessing
- Validation requires reference model checkpoints or detailed model summary documentation; task design cannot be verified without ground truth architectural specifications

## Evidence

- [intro] Extension of chemprop with spectral features: "chemprop-IR extends chemprop with new spectral features documented in the repository for infrared spectral predictions using message passing neural networks."
- [other] Core workflow for architecture reconstruction: "Extract and document all new layers, input processing steps, and loss functions specific to infrared spectral prediction from the chemprop-IR source code."
- [other] Validation by architectural comparison: "Validate that the reconstructed architecture matches the documented chemprop-IR structure by comparing layer counts, input/output tensor shapes, and parameter counts against reference checkpoints or"
- [intro] Message passing neural network foundation: "message passing neural networks for spectral predictions as described in the paper [Message Passing Neural Networks for Infrared Spectral Predictions]"
- [intro] Source repositories for implementation: "available in the [chemprop GiHub repository](https://github.com/chemprop/chemprop)"
