---
name: multimodal-input-tensor-construction
description: Use when when you have completed multimodal dataset production via data_prep.py and need to prepare sample or production input batches that combine molecular graph features and SMILES embeddings for forward pass validation or model training on TransG-Net.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0154
  tools:
  - RDKit 2020.03.4
  - torch
  - numpy
  - RDKit
  - scikit-learn
  - CUDA
  - cuDNN
  - TransGNet.py
  - data_prep.py
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
---

# multimodal-input-tensor-construction

## Summary

Construct PyTorch tensor pairs that combine graph and SMILES representations of molecules to serve as input to the TransG-Net multimodal neural network. This skill bridges the data preparation pipeline output with the model's dual input specification.

## When to use

When you have completed multimodal dataset production via data_prep.py and need to prepare sample or production input batches that combine molecular graph features and SMILES embeddings for forward pass validation or model training on TransG-Net.

## When NOT to use

- Input molecules have not yet been processed through data_prep.py — use that workflow first.
- You are working with single-modality input (e.g., SMILES or graphs alone) — this skill assumes dual-modal alignment.
- Tensor dimensions are already verified and model has been trained; this skill is for setup and validation, not inference at scale.

## Inputs

- Molecular graph representation (node features, edge list, or adjacency matrix as PyTorch tensor)
- SMILES string embeddings (dense vector or sequence representation as PyTorch tensor)
- TransGNet.py model definition file
- data_prep.py output format specification (schema or example)

## Outputs

- Pair of aligned PyTorch input tensors (graph tensor, SMILES tensor)
- Model output tensor from forward pass
- Model architecture summary (parameter count, layer dimensions, input/output shapes)

## How to apply

Load or generate sample multimodal data consistent with the output format of data_prep.py, which produces paired molecular graphs and SMILES representations. Construct two aligned PyTorch tensors: one encoding graph features (adjacency, node attributes, or node embeddings) and one encoding SMILES string embeddings. Verify tensor shapes and data types match the model's expected input specification by consulting TransGNet.py. Pass both tensors simultaneously through the instantiated model's forward method to confirm execution without shape mismatches. Log the resulting output tensor dimensions and compare against the paper's reported output specification to confirm correct dimensionality propagation through the network.

## Related tools

- **torch** (Tensor construction, model instantiation, and forward pass execution for multimodal input validation)
- **RDKit** (Molecular graph extraction and SMILES parsing during multimodal dataset preparation)
- **numpy** (Numerical array operations for tensor data preparation and validation)
- **TransGNet.py** (Model definition and forward pass target; specifies expected input tensor architecture) — github.com/chensaian/TransG-Net
- **data_prep.py** (Source script that generates the multimodal dataset format consumed by tensor construction) — github.com/chensaian/TransG-Net

## Examples

```
import torch
from TransGNet import TransGNet
graph_tensor = torch.randn(32, 50, 64)  # batch_size=32, nodes=50, node_features=64
smiles_tensor = torch.randn(32, 100, 128)  # batch_size=32, seq_len=100, embedding_dim=128
model = TransGNet()
output = model(graph_tensor, smiles_tensor)
print(f'Output shape: {output.shape}')
```

## Evaluation signals

- Output tensor shapes from forward pass match the paper's reported model output dimensions
- No shape mismatch or dtype errors during forward pass execution
- Parameter count and layer dimensions logged from model.summary() or inspection match the paper's architecture description
- Graph tensor and SMILES tensor are aligned (same batch size, consistent indexing across modalities)
- Input tensor dtypes (float32 for features, long for indices if applicable) are compatible with model weights

## Limitations

- Requires exact alignment between graph and SMILES tensors by molecule index; misalignment will cause spurious model behavior.
- The skill does not validate chemical correctness of graph or SMILES representations — assumes data_prep.py output is valid.
- Tensor memory footprint can become prohibitive for large batch sizes on limited GPU memory (CUDA >= 9.0 required).
- No specific training settings guidance is provided in the README; refer to the paper for hyperparameters and batch composition.

## Evidence

- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [other] Instantiate the TransG-Net model with the appropriate architecture parameters matching the multimodal input specification (graph features and SMILES embeddings).: "Instantiate the TransG-Net model with the appropriate architecture parameters matching the multimodal input specification (graph features and SMILES embeddings)."
- [other] Generate or load sample multimodal input tensors consistent with the output format of data_prep.py (molecular graphs and SMILES representations).: "Generate or load sample multimodal input tensors consistent with the output format of data_prep.py (molecular graphs and SMILES representations)."
- [other] Pass the sample inputs through the instantiated model to verify forward pass execution and output tensor shapes.: "Pass the sample inputs through the instantiated model to verify forward pass execution and output tensor shapes."
- [other] Log and record the model architecture summary, parameter count, and input/output tensor dimensions.: "Log and record the model architecture summary, parameter count, and input/output tensor dimensions."
- [readme] torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time): "torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time)"
