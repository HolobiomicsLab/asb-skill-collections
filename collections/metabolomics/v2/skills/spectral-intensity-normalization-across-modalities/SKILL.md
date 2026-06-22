---
name: spectral-intensity-normalization-across-modalities
description: Use when you have raw spectral data from multiple complementary spectroscopic techniques (NMR, HSQC, COSY, IR) that must be combined into joint training records for a multimodal deep learning model, and the raw intensity values or chemical shift ranges differ significantly between modalities due to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - numpy
  - Python
  - DataGenerationPipeline (MultiModalSpectralTransformer)
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
evidence_spans:
- No usage/docs found.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-intensity-normalization-across-modalities

## Summary

Normalize intensity ranges and chemical shift scales across heterogeneous spectroscopic modalities (NMR, HSQC, COSY, IR) to create a unified tensor representation suitable for multimodal transformer training. This skill ensures that differences in instrument sensitivity, acquisition parameters, and physical scales do not bias the model toward any single modality.

## When to use

You have raw spectral data from multiple complementary spectroscopic techniques (NMR, HSQC, COSY, IR) that must be combined into joint training records for a multimodal deep learning model, and the raw intensity values or chemical shift ranges differ significantly between modalities due to instrument-specific calibration or physical scale differences.

## When NOT to use

- Input spectral data is already preprocessed and normalized by the instrument vendor (e.g., already unit-normalized intensity).
- Each modality is being analyzed independently rather than combined into a joint multimodal model.
- Intensity variation across modalities is intentionally preserved to encode physical differences (e.g., relative sensitivity).

## Inputs

- Raw spectral data files (NMR, HSQC, COSY, IR) in vendor or standardized format
- Spectral datasets parsed into numpy arrays or pandas DataFrames
- Metadata mapping chemical shift scales and intensity units per modality

## Outputs

- Normalized multimodal spectral tensors (consistent intensity range across all modalities)
- Standardized chemical shift axis definitions per modality
- Quality-validated tensor arrays with no NaN or infinite values

## How to apply

Parse each spectroscopic modality (NMR, HSQC, COSY, IR) into standardized numpy arrays or pandas DataFrames, preserving their native chemical shift or frequency scales. For each modality, compute the intensity range (min and max values across all spectra) and apply min-max scaling or z-score normalization to bring all intensity distributions to a common numeric range (e.g., 0–1 or mean ± σ). Separately document or standardize the chemical shift axis scale for each modality (e.g., ppm for NMR-type spectra), ensuring consistent bin resolution across molecules. After normalization, validate that no NaN or infinite values remain in the tensor arrays and that the output shape matches the expected input format for the MultiModalSpectralTransformer. This ensures that each modality contributes equally to model training without one modality's raw intensity scale dominating the loss landscape.

## Related tools

- **pandas** (Parse and align spectral data into DataFrames; compute per-modality intensity statistics and normalization parameters)
- **numpy** (Perform vectorized min-max scaling, z-score normalization, and NaN/infinite value detection on spectral tensor arrays)
- **DataGenerationPipeline (MultiModalSpectralTransformer)** (Orchestrate loading, preprocessing, normalization, batching, and validation of multimodal spectral tensors) — https://github.com/mpriessner/MultiModalSpectralTransformer

## Examples

```
import pandas as pd; import numpy as np; spectra_nmr = pd.read_csv('nmr_data.csv'); intensity_min, intensity_max = spectra_nmr.iloc[:, 1:].min().min(), spectra_nmr.iloc[:, 1:].max().max(); spectra_nmr_norm = (spectra_nmr.iloc[:, 1:] - intensity_min) / (intensity_max - intensity_min); assert not np.isnan(spectra_nmr_norm.values).any() and not np.isinf(spectra_nmr_norm.values).any()
```

## Evaluation signals

- All spectral intensity values across all four modalities (NMR, HSQC, COSY, IR) fall within the target normalized range (e.g., 0–1 or ±3σ), with no outliers or clipping artifacts.
- Verification that no NaN or infinite values remain in the normalized tensor arrays; check via np.isnan(), np.isinf() on each modality tensor.
- Chemical shift axis scales are consistent within each modality across all molecules; spot-check a sample of spectra to confirm ppm or frequency ranges align with literature expectations.
- Mean and standard deviation of normalized intensities per modality are approximately equal (e.g., all close to 0.5 for min-max, or 0 ± 1 for z-score), confirming balanced contribution across modalities.
- Multimodal joint records pair each molecule with a complete spectroscopic profile across all four modalities with no missing or misaligned modality tensors.

## Limitations

- Normalization assumes that intensity ranges within each modality reflect measurement noise and instrument sensitivity rather than true chemical differences; aggressive scaling may obscure genuine signal variation.
- Chemical shift scales differ fundamentally between modality types (ppm for NMR-family, wavenumber for IR); direct axis normalization is not always appropriate and may require separate scale handling.
- Min-max normalization is sensitive to outliers; a single corrupted spectrum with extreme intensity values can compress the dynamic range for all other spectra in that modality.
- Normalization must be recomputed if the training dataset changes (e.g., new molecules or modalities added), and previous models trained on differently normalized data are not directly comparable.

## Evidence

- [other] Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities.: "Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities."
- [other] Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays.: "Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays."
- [other] The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data used by the MultiModalSpectralTransformer for molecular structure prediction.: "The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data used by the MultiModalSpectralTransformer for"
- [other] Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors.: "Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors."
