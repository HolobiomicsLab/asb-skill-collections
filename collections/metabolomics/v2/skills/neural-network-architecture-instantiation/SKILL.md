---
name: neural-network-architecture-instantiation
description: Use when when you have retrieved a model definition file (e.g., TransGNet.py) and need to verify it can be loaded, configured with correct hyperparameters, and executed on representative multimodal inputs (e.g., molecular graphs and SMILES embeddings) before training or inference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3314
  tools:
  - RDKit 2020.03.4
  - torch
  - numpy
  - RDKit
  - scikit-learn
  - CUDA
  - cuDNN
derived_from:
- doi: 10.1007/s10489-022-04351-0
  title: Mass Spectrum Transformer
evidence_spans:
- RDKit == 2020.03.4
- torch >= 1.4.0
- numpy == 1.19.1
- scikit-learn == 0.23.2
- cuda >= 9.0
- cudnn >= 7.0
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

# neural-network-architecture-instantiation

## Summary

Instantiate a PyTorch neural network model from source code and verify its forward pass with multimodal input tensors matching the expected data format. This skill validates that the model architecture accepts and processes the correct input shapes and produces outputs with expected dimensions.

## When to use

When you have retrieved a model definition file (e.g., TransGNet.py) and need to verify it can be loaded, configured with correct hyperparameters, and executed on representative multimodal inputs (e.g., molecular graphs and SMILES embeddings) before training or inference. Apply this skill when you need to confirm the model's input/output contract matches the data preparation pipeline output.

## When NOT to use

- The model definition file is already validated and in production; this skill is for initial verification and debugging, not runtime inference.
- Input data has already been converted to tensors and passed through the model in a training loop; use this skill before that, not during execution.
- You do not have the data_prep.py pipeline output format specification; without knowing multimodal input shapes, you cannot construct representative tensors.

## Inputs

- Model definition file (Python source code, e.g., TransGNet.py)
- Model architecture configuration parameters (graph feature dimensions, SMILES embedding dimensions)
- Sample multimodal input tensors: molecular graph features and SMILES representations
- Data format specification from data_prep.py output

## Outputs

- Instantiated PyTorch model object in memory
- Forward pass output tensors with verified shapes
- Model architecture summary (parameter count, layer structure)
- Input/output dimension log for validation and debugging

## How to apply

Load the model definition from the repository file (TransGNet.py). Instantiate the model class with architecture parameters that match the multimodal input specification—for TransG-Net, this means configuring graph feature dimensions and SMILES embedding dimensions to align with outputs from data_prep.py. Generate or load sample input tensors with the same shape and format as the data preparation pipeline produces (molecular graph representations and SMILES representations). Execute a forward pass by passing sample inputs through the instantiated model. Verify that the forward pass completes without error and that output tensor shapes, parameter counts, and dimensions match expectations documented in the paper or model specification.

## Related tools

- **torch** (PyTorch framework for defining, instantiating, and executing the neural network model with GPU support via CUDA)
- **RDKit** (Generates molecular graph representations and SMILES embeddings used as multimodal inputs to the model)
- **CUDA** (GPU acceleration backend for PyTorch model instantiation and forward pass execution)
- **cuDNN** (GPU-accelerated deep neural network library for optimized model operations)
- **numpy** (Array manipulation and tensor construction for sample input generation)

## Examples

```
import torch; from TransGNet import TransGNet; model = TransGNet(graph_dim=256, smiles_dim=128); graph_input = torch.randn(32, 100, 256); smiles_input = torch.randn(32, 64, 128); output = model(graph_input, smiles_input); print(f'Output shape: {output.shape}'); print(f'Model parameters: {sum(p.numel() for p in model.parameters())}')
```

## Evaluation signals

- Forward pass completes without runtime errors or shape mismatch exceptions
- Output tensor dimensions match expected model output specification (e.g., batch size, prediction dimension)
- Model parameter count is consistent with the paper's architecture description
- Input tensor shapes exactly match the format produced by data_prep.py (multimodal graph and SMILES dimensions)
- No CUDA out-of-memory errors or device placement issues when instantiating on GPU with torch.device('cuda')

## Limitations

- Model instantiation requires the exact dependency versions specified (torch >= 1.4.0, RDKit == 2020.03.4, CUDA >= 9.0, cuDNN >= 7.0); version mismatches may cause incompatibility or altered behavior.
- Sample tensor construction must match the exact multimodal format from data_prep.py; incorrect input shapes will cause forward pass failure without diagnostic detail.
- GPU memory constraints may prevent instantiation of large model configurations; this skill does not address memory profiling or model size optimization.
- The paper refers to specific training settings in external documentation; training hyperparameters are not retrievable from model instantiation alone.

## Evidence

- [readme] the code of TransG-Net is in TransGNet.py: "the code of TransG-Net is in TransGNet.py"
- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [other] TransG-Net is implemented in TransGNet.py and processes multimodal datasets produced by data_prep.py, with model configuration and training parameters specified according to the paper.: "TransG-Net is implemented in TransGNet.py and processes multimodal datasets produced by data_prep.py"
- [other] Instantiate the TransG-Net model with the appropriate architecture parameters matching the multimodal input specification (graph features and SMILES embeddings).: "Instantiate the TransG-Net model with the appropriate architecture parameters matching the multimodal input specification (graph features and SMILES embeddings)."
- [other] Pass the sample inputs through the instantiated model to verify forward pass execution and output tensor shapes.: "Pass the sample inputs through the instantiated model to verify forward pass execution and output tensor shapes."
- [readme] torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time): "torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time)"
- [readme] cuda >= 9.0, cudnn >= 7.0: "cuda >= 9.0, cudnn >= 7.0"
