---
name: data-pipeline-module-design-and-integration
description: Use when you have raw spectroscopic datasets from heterogeneous sources
  (multiple Zenodo repositories with different file formats and scales) that must
  be jointly normalized, deduplicated, and aligned by molecular identifier to feed
  a multimodal deep learning architecture.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - numpy
  - Python
  techniques:
  - NMR
  license_tier: restricted
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
  - 10.5281/zenodo.16076914
  - 10.5281/zenodo.16257786
  - 10.5281/zenodo.17284940
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Data Pipeline Module Design and Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and integrate a modular data pipeline that ingests, parses, normalizes, and curates multimodal spectroscopic data (NMR, HSQC, COSY, IR) into aligned, quality-filtered tensor batches for transformer model training. This skill bridges raw spectroscopic datasets to machine-ready tensors by implementing standardized I/O contracts, cross-modal alignment, and deterministic quality gates.

## When to use

You have raw spectroscopic datasets from heterogeneous sources (multiple Zenodo repositories with different file formats and scales) that must be jointly normalized, deduplicated, and aligned by molecular identifier to feed a multimodal deep learning architecture. The trigger is: multiple spectroscopic modalities exist for the same set of molecules, but they are not yet co-located, co-indexed, or validated for completeness and correctness.

## When NOT to use

- Input spectral data is already single-modality or fully pre-aligned in a unified database; use simpler single-source loaders instead.
- Molecules do not have consistent IDs across modality files; resolve identifier conflicts before applying this pipeline.
- Quality filtering thresholds are unknown or poorly defined; establish baselines (e.g., SNR cutoffs, peak density bounds) before designing the pipeline.

## Inputs

- Raw spectral datasets from Zenodo repositories (10.5281/zenodo.16076914, 10.5281/zenodo.16257786, 10.5281/zenodo.17284940) in mixed file formats (NMR, HSQC, COSY, IR spectral files)
- Molecular identifier mappings linking spectra across modalities
- Quality metric thresholds (signal-to-noise ratio cutoffs, peak count bounds)

## Outputs

- Curated multimodal tensor batches (numpy arrays or PyTorch tensors) with consistent shapes and dtypes
- Joint training records pairing each molecule with aligned NMR, HSQC, COSY, and IR spectra
- Data validity report (shape, type, modality coverage, NaN/infinite value count)

## How to apply

Implement a DataGenerationPipeline class with five sequential stages: (1) Download and extract raw spectral files from all source repositories using pandas/numpy I/O; (2) Parse each modality (NMR, HSQC, COSY, IR) into standardized numpy arrays or DataFrames, applying modality-specific normalizations (e.g., chemical shift scale alignment, intensity range standardization); (3) Apply data curation filters based on signal-to-noise ratio thresholds and peak count requirements, removing duplicates and corrupted entries; (4) Join records by molecular identifier across all four modalities to create unified training instances where each molecule carries its complete spectroscopic profile; (5) Batch and (optionally) augment the aligned tensors, then validate output shapes, dtypes, and coverage, ensuring no NaN or infinite values remain. The rationale is that misaligned or incomplete modality sets will degrade model learning; explicit quality gates and alignment checks prevent silent data corruption.

## Related tools

- **pandas** (Parse, align, and join spectral records by molecular identifier; manage metadata and filtering operations across modalities)
- **numpy** (Normalize chemical shift scales and intensity ranges; create standardized tensor arrays; perform batch-level validation and NaN checks)
- **Python** (Language for implementing DataGenerationPipeline class with modular load, preprocess, batch, and augment methods)

## Examples

```
import pandas as pd; import numpy as np; pipeline = DataGenerationPipeline(zenodo_repos=['10.5281/zenodo.16076914', '10.5281/zenodo.16257786', '10.5281/zenodo.17284940']); tensors = pipeline.load_and_preprocess(snr_threshold=5.0, peak_count_min=10); pipeline.validate_output(tensors)
```

## Evaluation signals

- Output tensor shapes are consistent across all records and match expected dimensions for each modality (e.g., NMR shape [num_samples, num_features], no broadcasting mismatches).
- All molecules present in the training set have complete coverage: each record contains valid (non-NaN, non-infinite) spectra for all four modalities (NMR, HSQC, COSY, IR).
- Chemical shift scales and intensity ranges are normalized to defined ranges (e.g., [0, 1] or z-score standardization) consistently across all modalities and records.
- No duplicate records remain after deduplication; molecular identifiers are unique within the final dataset.
- Quality filter metrics (SNR, peak count) fall within expected ranges; filtered-out records are logged and justified by threshold violations.

## Limitations

- Requires significant storage (≥50GB) to download and temporarily hold three Zenodo repositories; compression and streaming may be necessary for resource-constrained environments.
- Assumes molecular identifiers are consistent and unambiguous across all four spectroscopic modalities; identifier conflicts or mismatches will cause alignment failures and must be resolved manually.
- Quality filtering thresholds (SNR cutoffs, peak count bounds) are problem-specific and must be calibrated empirically; inappropriate thresholds may discard valid data or admit noise.
- Spectroscopic file formats may vary within each modality (e.g., different NMR vendor formats); the pipeline must implement format-specific parsers for each sub-type or standardize inputs upstream.

## Evidence

- [other] The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data used by the MultiModalSpectralTransformer for molecular structure prediction.: "The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data"
- [other] Download and extract spectral datasets from the three Zenodo repositories; Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities.: "Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities"
- [other] Implement data curation functions to filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries.: "filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries"
- [other] Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities.: "Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities"
- [other] Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors.: "Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors"
- [other] Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays.: "Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays"
- [readme] At least 50GB storage space for datasets, model checkpoints, and results.: "At least 50GB storage space for datasets, model checkpoints, and results"
- [readme] Step-by-step guide for data preparation: "Step-by-step guide for data preparation"
