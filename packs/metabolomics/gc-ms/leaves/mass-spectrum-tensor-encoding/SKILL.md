---
name: mass-spectrum-tensor-encoding
description: Use when when you have parsed EI-MS spectrum data (m/z and intensity values) and need to feed it into a pre-trained MWFormer transformer model for direct molecular weight prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Git
  - rdkit
  - Anaconda
  - PyTorch
  - Python 3.9
  - NumPy
  - MWFormer
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c03781
  title: MWFormer
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.9'
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

# mass-spectrum-tensor-encoding

## Summary

Convert electron ionization mass spectrum data (m/z and intensity pairs) into a tensor format compatible with transformer-based neural network inference for molecular weight prediction. This skill bridges raw spectroscopic data and deep learning model inputs.

## When to use

When you have parsed EI-MS spectrum data (m/z and intensity values) and need to feed it into a pre-trained MWFormer transformer model for direct molecular weight prediction. Use this skill as the final preprocessing step before model inference, after spectrum parsing but before forward pass.

## When NOT to use

- Spectrum data is already in tensor format — skip directly to model inference.
- Input is a different mass spectrometry modality (e.g. MALDI, ESI, or tandem MS) — MWFormer is trained specifically on electron ionization (EI) spectra.
- Molecular weight is already known or empirically determined — this skill is for computational prediction, not validation.

## Inputs

- parsed EI-MS spectrum (m/z values as array)
- parsed EI-MS spectrum (intensity values as array)
- MWFormer model configuration or input shape specification

## Outputs

- PyTorch tensor (spectrum representation ready for model inference)
- tensor metadata (shape, dtype, device placement)

## How to apply

Parse the input EI-MS spectrum to extract m/z values and their corresponding intensity measurements. Normalize or standardize the intensity values according to the MWFormer model's expected input range (inferred from the model architecture documentation or requirements.txt specifications). Stack the m/z and intensity pairs into a 2D or higher-dimensional tensor structure matching the model's input layer dimensions. Convert the tensor to the appropriate PyTorch dtype (typically float32) and device (CPU or CUDA). Validate tensor shape matches the model's expected input: the README and workflow indicate the model accepts 'spectrum as a tensor input matching the model's expected input format,' which is determined by the transformer's embedding and sequence processing layers.

## Related tools

- **PyTorch** (Tensor construction, device placement (CPU/CUDA), and dtype management during spectrum encoding) — https://pytorch.org/
- **Python 3.9** (Runtime environment for tensor manipulation and spectrum parsing utilities)
- **NumPy** (Array-based spectrum data handling and normalization prior to tensor conversion (implicit in requirements.txt))
- **MWFormer** (Defines the expected tensor input format and shape constraints for spectrum encoding) — https://github.com/zhanghailiangcsu/MWFormer

## Evaluation signals

- Tensor shape matches the model's input_size parameter (verify via model.eval() or architecture inspection)
- Tensor dtype is float32 (or the dtype specified in model configuration)
- No NaN or Inf values present after normalization (check torch.isnan(), torch.isinf())
- Intensity values are within expected range (e.g., [0, 1] or [0, 100] depending on normalization scheme) — verify against requirements.txt or example notebooks in the repository
- Forward pass executes without shape mismatch errors: `output = model(encoded_spectrum)` completes successfully and returns a scalar or 1D tensor with the predicted molecular weight

## Limitations

- MWFormer is trained exclusively on electron ionization (EI) mass spectra; encoding and inference on other ionization methods (MALDI, ESI, etc.) may yield unreliable predictions.
- The repository README does not provide explicit documentation of the tensor shape, normalization scheme, or value ranges expected by the model; practitioners must infer this from example usage notebooks or the model weights file.
- No changelog or versioning history is provided (README indicates 'No changelog found'), making it unclear whether tensor encoding requirements have evolved across model releases.
- The article and README do not document how the model handles spectra of variable length or sparse m/z ranges; encoding strategy for edge cases (very low or very high mass, missing intensity measurements) is not specified.

## Evidence

- [other] Parse the input EI-MS spectrum data (m/z and intensity values).: "Parse the input EI-MS spectrum data (m/z and intensity values)."
- [other] Prepare the spectrum as a tensor input matching the model's expected input format.: "Prepare the spectrum as a tensor input matching the model's expected input format."
- [other] Run forward inference through the MWFormer transformer to generate the predicted molecular weight.: "Run forward inference through the MWFormer transformer to generate the predicted molecular weight."
- [readme] You can download the trained model on Github. Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS.: "You can download the trained model on Github. Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS."
- [readme] MWFormer: Direct Prediction of Molecular Mass from Electron lonization Mass Spectrum by Transformer: "MWFormer: Direct Prediction of Molecular Mass from Electron lonization Mass Spectrum by Transformer"
