---
name: pytorch-model-loading-and-forward-pass
description: Use when when you have a pre-trained PyTorch model checkpoint (e.g.,
  a MWFormer transformer) and structured input data (e.g., electron ionization mass
  spectrum m/z and intensity pairs) that must be converted to tensor format and passed
  through the model to produce a direct numerical output (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - Git
  - rdkit
  - Anaconda
  - MWFormer
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c03781
  title: MWFormer
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.9'
- '[Pytorch](https://pytorch.org/) 1.12'
- Install [Git](https://git-scm.com/downloads)
- conda install -c conda-forge rdkit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwformer_cq
    doi: 10.1021/acs.analchem.4c03781
    title: MWFormer
  dedup_kept_from: coll_mwformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03781
  all_source_dois:
  - 10.1021/acs.analchem.4c03781
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pytorch-model-loading-and-forward-pass

## Summary

Load a pre-trained PyTorch transformer model and execute forward inference to generate predictions on structured input data. This skill bridges model artifact retrieval, tensor preparation, and model inference for end-to-end prediction workflows.

## When to use

When you have a pre-trained PyTorch model checkpoint (e.g., a MWFormer transformer) and structured input data (e.g., electron ionization mass spectrum m/z and intensity pairs) that must be converted to tensor format and passed through the model to produce a direct numerical output (e.g., predicted molecular weight). Use this skill when inference is the goal and the model architecture and weights are already trained and frozen.

## When NOT to use

- Model requires retraining or fine-tuning on new data—use a training loop instead
- Input spectrum is already embedded or pre-computed as features rather than raw m/z and intensity—use a simpler lookup or classifier
- Model checkpoint is not available or has incompatible architecture version

## Inputs

- Pre-trained PyTorch model checkpoint (.pt or .pth file)
- Electron ionization mass spectrum data (m/z values and intensity pairs)
- Spectrum tensor formatted to model input shape (normalized, padded, or standardized)

## Outputs

- Predicted molecular weight (scalar or batch tensor)
- Model output logits or confidence scores (if applicable)

## How to apply

First, ensure the PyTorch environment (1.12 or compatible version) is active and dependencies are installed. Load the pre-trained model checkpoint from the repository using PyTorch's model loading utilities. Parse the input data (e.g., EI-MS spectrum with m/z and intensity values) and reshape it to match the model's expected tensor input format—this typically involves normalizing or padding the spectrum to a fixed size and converting to a torch.Tensor. Call the model's forward method (or __call__) with the prepared tensor as input, which triggers the transformer layers to generate the prediction. Extract and post-process the output (e.g., a scalar molecular weight prediction or logit vector) and record the result. The model operates in inference mode (no gradient computation), so wrap the forward pass in torch.no_grad() for efficiency.

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the pre-trained transformer model in forward inference mode) — https://pytorch.org/
- **MWFormer** (Pre-trained transformer model for direct molecular weight prediction from EI-MS spectra) — https://github.com/zhanghailiangcsu/MWFormer
- **rdkit** (Chemistry toolkit for data preprocessing and validation of molecular structures if needed) — https://www.rdkit.org/
- **Git** (Version control for cloning the model repository and accessing checkpoints) — https://git-scm.com/

## Evaluation signals

- Output tensor shape and dtype match the documented model output specification (e.g., scalar float for MW prediction)
- Predicted molecular weight value falls within chemically plausible range for the input spectrum mass range
- Forward pass completes without gradient tracking (verified by torch.no_grad() context or model.eval() mode)
- Predicted value is deterministic across multiple identical forward passes (no dropout or stochastic layers active in inference)
- Input spectrum tensor has been correctly formatted to the model's expected input dimensions (e.g., batch × features × spectrum_length)

## Limitations

- Model performance depends on input spectrum quality and similarity to training data; EI-MS spectra from novel compounds or atypical ionization patterns may yield inaccurate predictions
- Forward inference does not provide uncertainty estimates or confidence intervals unless the model outputs a distribution
- Pre-trained checkpoint may not be compatible across different PyTorch versions or if model architecture code is not available
- No changelog or version history available in the public repository, making it difficult to track model updates or retraining events

## Evidence

- [other] Load the pre-trained MWFormer model from the repository.: "4. Load the pre-trained MWFormer model from the repository."
- [other] Parse the input EI-MS spectrum data (m/z and intensity values).: "5. Parse the input EI-MS spectrum data (m/z and intensity values)."
- [other] Prepare the spectrum as a tensor input matching the model's expected input format.: "6. Prepare the spectrum as a tensor input matching the model's expected input format."
- [other] Run forward inference through the MWFormer transformer to generate the predicted molecular weight.: "7. Run forward inference through the MWFormer transformer to generate the predicted molecular weight."
- [other] The MWFormer model accepts electron ionization mass spectrum data as input and outputs a direct prediction of the molecular weight through a forward inference operation.: "The MWFormer model accepts electron ionization mass spectrum data as input and outputs a direct prediction of the molecular weight through a forward inference operation."
- [readme] 2.[Pytorch](https://pytorch.org/) 1.12: "2.[Pytorch](https://pytorch.org/) 1.12"
- [readme] Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS.: "Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS."
