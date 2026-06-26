---
name: spectral-feature-extraction-and-integration
description: Use when when you have a base message passing neural network (e.g., chemprop)
  trained on molecular graphs and need to augment it with infrared spectral information
  to improve prediction accuracy for molecular properties.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
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

# spectral-feature-extraction-and-integration

## Summary

Extract and integrate infrared spectral features into message passing neural network architectures to enable molecular property prediction from both graph structure and spectral data. This skill reconstructs extended chemprop models that fuse molecular representations with spectral feature embeddings.

## When to use

When you have a base message passing neural network (e.g., chemprop) trained on molecular graphs and need to augment it with infrared spectral information to improve prediction accuracy for molecular properties. Use this skill when spectral reference data (IR absorption frequencies, intensities, or functional group signatures) are available alongside molecular structure and you want to incorporate them as additional input channels rather than treating them as auxiliary metadata.

## When NOT to use

- Input spectral data is already integrated into node features or molecular descriptors without separate spectral channels—architecture reconstruction will be redundant.
- Spectral information is unavailable or only sparsely populated in your dataset; fusion of incomplete spectral channels may degrade performance.
- Target task does not involve spectral prediction or spectrum-informed molecular property estimation; base chemprop alone may be more interpretable and faster.

## Inputs

- Base chemprop model definition (PyTorch or equivalent)
- Molecular graph representations (node/edge features, adjacency)
- Infrared spectral data (wavenumber intensities, functional group encodings, or normalized spectra vectors)
- chemprop-IR source code repository (for feature processing and architectural modifications)
- Reference model checkpoint or layer documentation from chemprop-IR

## Outputs

- Extended message passing neural network model with spectral input processing
- Spectral feature embedding layers and fusion modules
- Modified output head(s) for spectral prediction tasks
- Updated forward pass that accepts graph and spectral tensors
- Layer-by-layer comparison report (shapes, parameter counts, matches to reference)

## How to apply

Begin by examining the base chemprop architecture to identify the message passing layers, featurization modules, and output heads. Access the chemprop-IR repository to extract spectral feature processing code—specifically new input layers for spectral embeddings, integration points where spectral tensors merge with graph representations, and modified loss functions that account for spectral targets. Implement the spectral feature handling by: (1) designing or reusing spectral embedding layers that convert IR spectrum vectors (e.g., wavenumber intensities or functional group indicators) into latent representations; (2) identifying the fusion point in the message passing backbone where spectral embeddings concatenate with or are aggregated with learned molecular representations; (3) modifying output layers to produce spectral predictions (e.g., absorption spectra or spectral properties) alongside or instead of scalar properties. Validate by comparing layer counts, input/output tensor shapes, and total parameter counts against a reference checkpoint or model summary from the chemprop-IR documentation.

## Related tools

- **chemprop** (Base message passing neural network architecture extended with spectral feature handling for infrared spectral prediction) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Reference implementation of spectral feature extraction, embedding, and fusion modules integrated into the chemprop backbone) — github:gfm-collab__chemprop-IR

## Evaluation signals

- Reconstructed model layer count matches reference chemprop-IR documentation; verify via model.named_modules() or summary output.
- Input tensor shapes for graph and spectral branches are correctly handled through fusion point; validate by tracing forward pass with sample batch of known dimensions.
- Output tensor shape(s) for spectral predictions (e.g., [batch_size, num_wavenumbers] or [batch_size, num_spectral_features]) align with expected target dimensions.
- Total learnable parameter count is within ±5% of reference checkpoint to confirm architectural fidelity.
- Loss function incorporates both molecular and spectral components (if multi-task); verify loss terms in training loop or model definition.

## Limitations

- Architectural reconstruction is repository-dependent; chemprop-IR source must be publicly accessible and well-documented for layer extraction.
- Spectral feature dimensionality (e.g., wavenumber resolution, number of functional groups) must be defined or inferred from the reference model; mismatched dimensions will cause tensor shape errors.
- No changelog or versioning guidance available in the article; updates to chemprop-IR may render prior architectural specifications obsolete.
- Fusion strategy (concatenation, attention, multi-head combination) must be reverse-engineered from source code if not explicitly documented; different fusion approaches yield different computational costs and prediction quality.

## Evidence

- [other] Base chemprop repository examination: "Clone the base chemprop repository from github.com/chemprop/chemprop and examine the core message passing architecture and model classes."
- [intro] chemprop-IR spectral extensions: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [other] Spectral feature documentation and extraction: "Extract and document all new layers, input processing steps, and loss functions specific to infrared spectral prediction from the chemprop-IR source code."
- [other] Architecture validation approach: "Validate that the reconstructed architecture matches the documented chemprop-IR structure by comparing layer counts, input/output tensor shapes, and parameter counts against reference checkpoints or"
- [intro] chemprop-IR extends chemprop with spectral features: "chemprop-IR extends chemprop with new spectral features documented in the repository for infrared spectral predictions using message passing neural networks."
