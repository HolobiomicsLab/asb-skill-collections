---
name: spectroscopic-data-preprocessing
description: Use when when you have raw spectroscopic measurements in heterogeneous formats (IR, Raman, UV-Vis, mass spectra, or NMR) and need to feed them into a spectrum-conditioned diffusion model for de novo molecular structure elucidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - DiffSpectra
  - SpecFormer
derived_from:
- doi: 10.48550/arxiv.2507.06853
  title: DiffSpectra
evidence_spans:
- github.com/AzureLeon1/DiffSpectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_diffspectra_cq
    doi: 10.48550/arxiv.2507.06853
    title: DiffSpectra
  dedup_kept_from: coll_diffspectra_cq
schema_version: 0.2.0
---

# spectroscopic-data-preprocessing

## Summary

Normalize and tokenize multi-modal spectroscopic data (IR, Raman, UV-Vis, mass spectra, NMR) into standardized representations suitable for diffusion-model-based molecular structure generation. This preprocessing step ensures consistent input encoding across heterogeneous spectral modalities and is critical for conditioning the DiffSpectra diffusion pipeline.

## When to use

When you have raw spectroscopic measurements in heterogeneous formats (IR, Raman, UV-Vis, mass spectra, or NMR) and need to feed them into a spectrum-conditioned diffusion model for de novo molecular structure elucidation. Apply this skill when spectral data must be unified across multiple instrumental modalities and when the downstream generative model requires tokenized, normalized representations.

## When NOT to use

- When spectral data is already in a pre-processed, model-ready tensor format and no further standardization or multi-modal alignment is required.
- When working with a single well-characterized spectral modality that does not require normalization across heterogeneous instrumental sources.
- When the downstream model is not SpecFormer or a similarly tokenization-dependent spectral encoder.

## Inputs

- Raw multi-modal spectroscopic data (IR, Raman, UV-Vis, mass spectra, or NMR measurements)
- Spectral data files in native instrument format or preprocessed numeric arrays
- Configuration specifying spectra_version (e.g., 'allspectra', 'ir', 'raman', 'uv')

## Outputs

- Normalized spectral arrays with standardized intensity and frequency scales
- Tokenized spectral representations suitable for SpecFormer encoder input
- Fixed-length tensor batches compatible with diffusion model conditioning

## How to apply

Load raw spectroscopic data in its native format (e.g., IR absorbance curves, Raman shift intensities, UV-Vis absorption wavelengths). Apply DiffSpectra pipeline normalization to standardize intensity scales and frequency ranges across modalities, then tokenize each spectrum according to the SpecFormer encoder's input vocabulary and shape requirements. The preprocessing step is executed within the training/evaluation loop before the spectra are passed to the SpecFormer transformer-based spectral encoder. Verify that normalized spectra fall within expected intensity bounds and that tokenization produces consistent fixed-length representations. This preprocessing ensures intra- and inter-spectrum dependencies are captured correctly by the downstream encoder.

## Related tools

- **DiffSpectra** (Defines the normalization and tokenization pipeline requirements; SpecFormer component consumes preprocessed spectra) — https://github.com/AzureLeon1/DiffSpectra
- **SpecFormer** (Transformer-based spectral encoder that accepts tokenized, normalized spectra and captures intra- and inter-spectrum dependencies) — https://github.com/AzureLeon1/DiffSpectra

## Examples

```
CUDA_VISIBLE_DEVICES=0,1 python main.py --config configs/diffspectra_qm9s.py --config_original_qm9 configs/base_qm9.py --mode train --workdir exp/allspectra --config.data.spectra_version allspectra --config.model.name DMT
```

## Evaluation signals

- Normalized spectral intensities fall within model-expected bounds (e.g., [0, 1] or standardized z-scores) across all modalities.
- Tokenized spectra have consistent fixed length matching SpecFormer input shape; no truncation or padding anomalies.
- Cross-modal alignment verified: spectra of the same molecule from different instruments (e.g., IR and Raman of the same compound) produce semantically coherent representations.
- Training convergence and downstream generation accuracy (top-1, top-10 recovery metrics) are comparable to published DiffSpectra benchmarks (40.76% top-1, 99.49% top-10).
- No NaN, Inf, or out-of-range values in preprocessed tensors; all spectra pass schema validation checks.

## Limitations

- Preprocessing correctness depends on precise knowledge of spectral modality ranges and normalization parameters; misconfigured parameters can degrade downstream model performance.
- Multi-modal fusion during preprocessing assumes all spectral modalities are available or have a defined fallback strategy; missing modalities may require retraining or architectural modification.
- The approach is validated on QM9S dataset; generalization to real experimental spectra with noise, drift, or instrumental artifacts not explicitly addressed in the README.
- Tokenization scheme is specific to the SpecFormer architecture; transferring to other spectral encoders requires re-implementation of preprocessing logic.

## Evidence

- [other] Preprocess spectra according to DiffSpectra pipeline normalization and tokenization requirements.: "Preprocess spectra according to DiffSpectra pipeline normalization and tokenization requirements."
- [readme] SpecFormer: A transformer-based spectral encoder that captures intra- and inter-spectrum dependencies across diverse spectral modalities (e.g., IR, Raman, UV-Vis).: "SpecFormer: A transformer-based spectral encoder that captures intra- and inter-spectrum dependencies across diverse spectral modalities (e.g., IR, Raman, UV-Vis)."
- [other] Load molecular spectroscopic data (mass spectra, NMR, IR, or other format) as input.: "Load molecular spectroscopic data (mass spectra, NMR, IR, or other format) as input."
- [readme] Through spectrum-conditioned diffusion modeling, DiffSpectra unifies multi-modal reasoning with 2D/3D generative modeling.: "Through spectrum-conditioned diffusion modeling, DiffSpectra unifies multi-modal reasoning with 2D/3D generative modeling."
- [readme] Modify the configuration file in `configs/` to set `data.root` to your configured path.: "Modify the configuration file in `configs/` to set `data.root` to your configured path."
