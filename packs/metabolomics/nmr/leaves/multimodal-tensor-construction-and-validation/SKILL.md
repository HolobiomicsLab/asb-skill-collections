---
name: multimodal-tensor-construction-and-validation
description: Use when when you have downloaded raw spectroscopic datasets from multiple sources (NMR, HSQC, COSY, IR files) and need to combine them into a single coherent training corpus where each molecule is represented by all four modalities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0611
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - pandas
  - numpy
  - Python
  techniques:
  - NMR
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

# multimodal-tensor-construction-and-validation

## Summary

Construct aligned multimodal spectroscopic tensors from heterogeneous NMR, HSQC, COSY, and IR spectral data, then validate their structural integrity, data type consistency, and absence of corrupted values. This skill ensures that disparate spectroscopic modalities are correctly paired by molecular identity and formatted for downstream transformer training.

## When to use

When you have downloaded raw spectroscopic datasets from multiple sources (NMR, HSQC, COSY, IR files) and need to combine them into a single coherent training corpus where each molecule is represented by all four modalities. Apply this skill before feeding data to a multimodal neural network, especially when modalities have been collected at different scales (chemical shift ranges, intensity normalization) and must be aligned by molecular identifier.

## When NOT to use

- Input spectral files are already preprocessed and aligned in a single HDF5 or NetCDF archive — use direct tensor loading instead.
- Only one or two spectroscopic modalities are available and cannot be meaningfully paired with all four modalities — the joint alignment step will produce sparse or incomplete records.
- Molecules lack consistent identifiers across modality files — alignment by molecular ID will fail or produce incorrect pairings.

## Inputs

- Raw NMR spectral files (parsed into numpy arrays or pandas DataFrames)
- Raw HSQC spectral files
- Raw COSY spectral files
- Raw IR spectral files
- Molecular identifier mapping (mapping molecules to their spectral records)

## Outputs

- Aligned multimodal training tensors (4D: batch × modality × spectral_dimension × intensity)
- Joint training records (tuples pairing each molecule to its complete spectroscopic profile)
- DataGenerationPipeline instance (with load, preprocess, batch, and augment methods)
- Validation report (tensor shape, data type, modality coverage, NaN/Inf counts)

## How to apply

First, parse all four spectroscopic modality files (NMR, HSQC, COSY, IR) into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges to a common reference frame. Second, apply quality-based filtering: remove spectra with signal-to-noise ratio below your threshold, peak count outside acceptable bounds, or evidence of corruption (duplicate entries, malformed peak lists). Third, align spectra by molecular identifier across all four modalities, creating joint training records where each molecule maps to a tuple of (NMR array, HSQC array, COSY array, IR array). Fourth, implement a DataGenerationPipeline class with methods to load and batch these aligned records into tensor form. Finally, validate the output: check tensor shape consistency across the batch, verify data types are correct (float32 or equivalent), confirm no NaN or infinite values remain, and assert modality coverage (each record has all four modalities present).

## Related tools

- **pandas** (Parse spectral files into DataFrames and manage molecular identifier alignment across modalities)
- **numpy** (Construct and validate multimodal arrays; normalize intensity ranges and chemical shift scales; check for NaN and infinite values)
- **Python** (Implement DataGenerationPipeline class and custom validation routines)

## Examples

```
from utils_MMT import DataGenerationPipeline; import pandas as pd, numpy as np; pipeline = DataGenerationPipeline(modalities=['NMR', 'HSQC', 'COSY', 'IR'], snr_threshold=5, peak_count_min=3); pipeline.load_and_align(zenodo_repos=['10.5281/zenodo.16076914', '10.5281/zenodo.16257786', '10.5281/zenodo.17284940']); tensors = pipeline.batch(batch_size=32); assert np.isnan(tensors).sum() == 0 and np.isinf(tensors).sum() == 0
```

## Evaluation signals

- Output tensors have consistent shape: (batch_size, 4, spectral_dim, intensity_dim) across all batches.
- Data type verification: all tensor values are float32 (or specified dtype) with no object or mixed types.
- Modality coverage: every molecule record contains exactly 4 spectra (one per modality); no missing modalities.
- Absence of corrupted values: np.isnan(tensors).sum() == 0 and np.isinf(tensors).sum() == 0 for all batches.
- Chemical shift and intensity ranges fall within expected bounds post-normalization (e.g., 0–10 ppm for NMR, 0–1 for normalized intensity).

## Limitations

- Requires high-performance GPU and at least 16 GB RAM to process large-scale spectroscopic datasets (50 GB storage recommended).
- Quality filtering based on signal-to-noise ratio and peak count thresholds may remove valid spectra if thresholds are set too stringently, reducing training data size.
- Molecular identifier inconsistencies across data repositories (e.g., different SMILES variants or registry numbers for the same molecule) can cause misalignment and corrupt joint records.
- Spectral data normalized to different scales in source repositories may introduce artifacts if normalization is not carefully validated post-alignment.

## Evidence

- [other] The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data: "The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data used by the MultiModalSpectralTransformer for"
- [other] Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities.: "Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities."
- [other] Implement data curation functions to filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries.: "Implement data curation functions to filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries."
- [other] Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities.: "Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities."
- [other] Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays.: "Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays."
- [readme] At least 16GB RAM to handle datasets and model training.: "Memory: At least 16GB RAM to handle datasets and model training."
- [other] Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors.: "Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors."
