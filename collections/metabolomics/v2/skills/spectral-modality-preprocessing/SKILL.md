---
name: spectral-modality-preprocessing
description: Use when you have downloaded raw spectroscopic data files (NMR, HSQC,
  COSY, IR modalities) from the Zenodo repositories and need to convert them into
  the standardized multi-modal input format required by the MultiModalSpectralTransformer
  before inference or retraining.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0634
  - http://edamontology.org/topic_3407
  tools:
  - MultiModalSpectralTransformer
  - RDKit
  - PyTorch
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
- doi: 10.5281/zenodo.16076914
  title: ''
- doi: 10.5281/zenodo.16257786
  title: ''
- doi: 10.5281/zenodo.17284940
  title: ''
evidence_spans:
- github.com/mpriessner/MultiModalSpectralTransformer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmst_cq
    doi: 10.1002/ange.202517611
    title: MMST
  dedup_kept_from: coll_mmst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/ange.202517611
  all_source_dois:
  - 10.1002/ange.202517611
  - 10.5281/zenodo.16076914
  - 10.5281/zenodo.16257786
  - 10.5281/zenodo.17284940
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-modality-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and preprocess multi-modal spectroscopic data (NMR, HSQC, COSY, IR) into the input format expected by the MultiModalSpectralTransformer architecture for automated molecular structure prediction. This skill bridges raw spectral files and the transformer model's tensor inputs.

## When to use

You have downloaded raw spectroscopic data files (NMR, HSQC, COSY, IR modalities) from the Zenodo repositories and need to convert them into the standardized multi-modal input format required by the MultiModalSpectralTransformer before inference or retraining. Use this skill when integrating heterogeneous spectral modalities that must be aligned temporally or spectrally and normalized to a common tensor representation.

## When NOT to use

- Input spectral data are already in tensor form or pre-processed NumPy arrays — skip directly to model inference.
- Only a single spectral modality is available — this skill is designed for multi-modal integration; use single-modality preprocessing pipelines instead.
- Spectral data are from instruments or protocols not represented in the training data repositories — validation and potential transfer learning may be necessary before preprocessing.

## Inputs

- NMR spectral data files (from Zenodo deposit 10.5281/zenodo.16076914, 10.5281/zenodo.16257786, or 10.5281/zenodo.17284940)
- HSQC spectral data files
- COSY spectral data files
- IR spectral data files
- Data dictionary or schema describing file formats and modality-specific metadata

## Outputs

- Multi-modal preprocessed tensor in shape compatible with MultiModalSpectralTransformer input (e.g., [batch_size, num_modalities, frequency_bins])
- Normalization parameters (mean, std, min, max per modality) for inverse transformation
- Alignment mapping (chemical shift or frequency grid used)
- Preprocessed data in HDF5, NumPy, or PyTorch format ready for model inference

## How to apply

Retrieve spectral input files (NMR, HSQC, COSY, IR data) from the three Zenodo deposits. Parse each modality-specific file format and extract spectral intensities, chemical shift ranges, and coupling constants according to the data dictionaries provided in the Zenodo repositories. Normalize each modality independently (e.g., zero-mean, unit-variance scaling or intensity quantile normalization) to ensure comparable signal ranges across different instruments and acquisition parameters. Align all modalities to a common chemical shift or frequency axis if necessary, using interpolation or binning. Stack the normalized, aligned modalities into a multi-channel tensor matching the transformer's expected input shape (typically [batch, modalities, frequency_bins] or similar). The preprocessing pipeline is documented in Section 3 of the Electronic Supplementary Information (ESI) of the paper; refer to that guide for specific parameter choices and modality-specific transformation rules.

## Related tools

- **MultiModalSpectralTransformer** (Primary model architecture that consumes the preprocessed multi-modal spectral tensors; defines the expected input format and modality integration strategy.) — https://github.com/mpriessner/MultiModalSpectralTransformer
- **RDKit** (Used for molecular structure parsing and validation of output molecules and reference structures; may also support spectral feature extraction.)
- **PyTorch** (Tensor manipulation and batching framework; required for converting preprocessed arrays into model-compatible tensor objects.)

## Evaluation signals

- Verify all modalities are present and have matching batch size and aligned frequency/chemical shift grids — check tensor shape is [batch, 4, freq_bins].
- Check normalization statistics: mean ≈ 0 and std ≈ 1 per modality after preprocessing; outliers should be <3 standard deviations from mean.
- Confirm no NaN or infinite values are present in preprocessed tensors; validate data range is within expected bounds (e.g., [-5, 5] for normalized data).
- Compare a preprocessed sample spectrum visually or via histogram against the original to confirm normalization preserves spectral features without information loss.
- Test that the preprocessed tensor loads successfully into the MultiModalSpectralTransformer model without shape or dtype errors during a forward pass.

## Limitations

- Preprocessing assumes all four modalities (NMR, HSQC, COSY, IR) are available; partial modality sets may require masking or imputation strategies not detailed in the provided documentation.
- Normalization strategies may be sensitive to outliers or extreme spectral intensities in low-signal regions; robust scaling or quantile normalization may be needed for noisy spectra.
- Alignment of different modalities relies on accurate chemical shift or frequency calibration; miscalibrated data will degrade integration and model performance.
- The preprocessing pipeline is described in the Electronic Supplementary Information (ESI) of the paper; practitioners without access to that detailed guide may struggle with modality-specific parameters.
- Computational requirements (16GB RAM, high-performance GPU) apply to both preprocessing and model execution; large batch preprocessing on limited hardware may cause memory bottlenecks.

## Evidence

- [full_text] Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format.: "Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format."
- [readme] MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR): "MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR)"
- [readme] Detailed instructions on how to use the software, including the full improvement cycle workflow and the HTML GUI interface, are provided in the Electronic Supplementary Information (ESI) of the paper. Please refer to Section 3 of the ESI for a comprehensive user manual.: "Detailed instructions on how to use the software, including the full improvement cycle workflow and the HTML GUI interface, are provided in the Electronic Supplementary Information (ESI) of the"
- [full_text] Download spectral input files (NMR, HSQC, COSY, IR data) from the three Zenodo deposits (10.5281/zenodo.16076914, 10.5281/zenodo.16257786, 10.5281/zenodo.17284940).: "Download spectral input files (NMR, HSQC, COSY, IR data) from the three Zenodo deposits (10.5281/zenodo.16076914, 10.5281/zenodo.16257786, 10.5281/zenodo.17284940)."
- [readme] Memory: At least 16GB RAM to handle datasets and model training.: "Memory: At least 16GB RAM to handle datasets and model training."
