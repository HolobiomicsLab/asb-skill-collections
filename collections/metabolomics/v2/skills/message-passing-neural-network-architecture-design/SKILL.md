---
name: message-passing-neural-network-architecture-design
description: Use when when you have a working base MPNN implementation (e.g., chemprop) and need to adapt it for a new molecular property target (e.g., spectral data) that requires custom input processing, intermediate feature representations, or output layer modifications beyond the original model's scope.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0602
  tools:
  - chemprop
  - chemprop-IR
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]
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
---

# message-passing-neural-network-architecture-design

## Summary

Design and implement extensions to message-passing neural network (MPNN) architectures for molecular property prediction tasks, such as infrared spectral forecasting. This skill involves identifying architectural bottlenecks in a base MPNN framework, adding task-specific featurization and output layers, and validating that the extended model matches expected structural signatures.

## When to use

When you have a working base MPNN implementation (e.g., chemprop) and need to adapt it for a new molecular property target (e.g., spectral data) that requires custom input processing, intermediate feature representations, or output layer modifications beyond the original model's scope.

## When NOT to use

- The base MPNN already natively supports the target property or output format without modification.
- Input molecular data is already preprocessed as hand-crafted features or fixed-length vectors rather than molecular graphs.
- You are tasked only with hyperparameter tuning or training regime optimization on a pre-implemented architecture, not architectural extension or redesign.

## Inputs

- Base MPNN source code repository (e.g., github.com/chemprop/chemprop)
- Extended MPNN variant source code (e.g., github:gfm-collab__chemprop-IR)
- Target molecular input format (e.g., SMILES strings, molecular graphs)
- Expected output specification (e.g., infrared spectral predictions, frequency bands)

## Outputs

- Reconstructed extended MPNN model definition (Python source code)
- Layer-by-layer architectural specification document (counts, shapes, parameters)
- Validated model checkpoint or summary matching reference implementation
- Featurization and loss function module implementations

## How to apply

Begin by cloning and examining the base MPNN repository (chemprop) to document core message passing layers, featurization input shapes, and loss functions. Access the extended variant repository (chemprop-IR) to extract and enumerate all new layers, spectral-specific input processing steps, and output head architectures relative to the base. Implement the extended model by modifying the base MPNN's model definition class to incorporate the new featurization modules and loss functions. Validate architectural parity by comparing layer counts, input/output tensor shapes, and total parameter counts against reference checkpoints or printed model summaries from the extended repository.

## Related tools

- **chemprop** (Base message-passing neural network framework to be extended with spectral feature handling and output layers) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Reference extended architecture implementing infrared spectral prediction; used to extract and document architectural modifications relative to base chemprop) — github:gfm-collab__chemprop-IR

## Evaluation signals

- Layer count of reconstructed model exactly matches reference checkpoint model summary (e.g., number of message passing blocks, featurization layers, output heads).
- Input tensor shape to extended model accepts spectral-specific features (e.g., new featurization dimension for infrared data) without shape mismatch errors.
- Total trainable parameter count of reconstructed model is within ±2% of reference checkpoint, indicating correct layer definitions and dimensionality.
- Forward pass through reconstructed model produces output tensor with correct shape for target property (e.g., infrared spectrum with expected frequency bands or wavelength range).
- Loss function evaluates successfully on mock batch without NaN or shape broadcasting errors, confirming spectral loss head integration.

## Limitations

- No publicly available changelog or migration guide was identified; architectural differences must be reverse-engineered from source code comparison.
- Validation relies on visual model summary or checkpoint inspection; quantitative performance parity on held-out spectral data is not established by architectural alignment alone.
- Spectral feature definitions and preprocessing steps may not be fully documented in repository; domain knowledge of infrared spectroscopy may be required to correctly integrate featurization.

## Evidence

- [other] Architectural reconstruction and validation steps: "Extract and document all new layers, input processing steps, and loss functions specific to infrared spectral prediction from the chemprop-IR source code."
- [other] Model comparison criterion: parameter and shape parity: "Validate that the reconstructed architecture matches the documented chemprop-IR structure by comparing layer counts, input/output tensor shapes, and parameter counts against reference checkpoints or"
- [intro] Purpose and baseline framework: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [intro] Core finding: spectral feature extension: "chemprop-IR extends chemprop with new spectral features for infrared spectral prediction tasks"
