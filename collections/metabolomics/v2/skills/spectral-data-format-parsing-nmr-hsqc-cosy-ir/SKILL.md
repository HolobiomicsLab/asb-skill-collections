---
name: spectral-data-format-parsing-nmr-hsqc-cosy-ir
description: Use when when you have downloaded raw spectral datasets from multiple spectroscopic modalities (NMR, HSQC, COSY, IR) in their native or proprietary formats and need to convert them into aligned, standardized tensors for multimodal machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - numpy
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-format-parsing-nmr-hsqc-cosy-ir

## Summary

Parse raw NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames with normalized chemical shift scales and intensity ranges. This skill bridges raw spectroscopic data formats and the tensor representations required by multimodal transformer training.

## When to use

When you have downloaded raw spectral datasets from multiple spectroscopic modalities (NMR, HSQC, COSY, IR) in their native or proprietary formats and need to convert them into aligned, standardized tensors for multimodal machine learning. Specifically apply this skill before data curation, quality filtering, or alignment by molecular identifier.

## When NOT to use

- Spectral data is already in pre-parsed tensor or HDF5 format ready for alignment — skip directly to data curation.
- You are working with a single modality or instrument type and do not require cross-modality normalization.
- Raw spectral files lack consistent structure or metadata — consider manual inspection and format standardization before parsing.

## Inputs

- Raw spectral files (NMR, HSQC, COSY, IR) from Zenodo repositories in native or text formats
- File list or manifest mapping spectral filenames to molecular identifiers
- Chemical shift reference standards or instrument calibration metadata (optional)

## Outputs

- Normalized numpy arrays or pandas DataFrames for each spectroscopic modality
- Parsing metadata (chemical shift offset, intensity scale factor, units)
- Standardized column names and index labels (e.g., chemical shift in ppm, intensity in AU)

## How to apply

Load spectral files from the three Zenodo data repositories using pandas or numpy I/O functions appropriate to each modality's format (e.g., text, binary, or HDF5). Normalize chemical shift scales across modalities to a common reference frame (typically ppm for NMR-family spectra) and standardize intensity ranges (e.g., min–max scaling or z-score normalization) to make different instruments and acquisition parameters comparable. Validate that parsed arrays have consistent shape and data type across all four modalities for a given molecule. Document the parsing logic (offset, scale factor, unit conversion) for reproducibility. Use this standardized output as input to subsequent data curation (quality filtering by SNR and peak count) and multi-modal record alignment steps.

## Related tools

- **pandas** (Read and manipulate spectral data tables; normalize intensity and chemical shift columns)
- **numpy** (Store parsed spectra as multi-dimensional arrays and apply vectorized normalization transformations)
- **Python** (Primary language for implementing file I/O, format conversion, and normalization logic)

## Examples

```
import pandas as pd; import numpy as np; nmr_data = pd.read_csv('raw_nmr.txt', delimiter='\t', usecols=['ppm', 'intensity']); nmr_norm = nmr_data.copy(); nmr_norm['intensity'] = (nmr_data['intensity'] - nmr_data['intensity'].min()) / (nmr_data['intensity'].max() - nmr_data['intensity'].min()); nmr_array = nmr_norm.values.astype(np.float32)
```

## Evaluation signals

- Parsed arrays have identical shape and data type across all four modalities for each molecular record (e.g., NMR, HSQC, COSY, IR all return float32 arrays of expected dimensions).
- Chemical shift values fall within expected ppm ranges (typically −10 to +200 ppm for NMR-family spectra, after normalization); intensity values are non-negative and bounded (e.g., 0–1 after min–max scaling).
- No NaN, infinite, or out-of-range values remain in parsed tensor arrays after normalization.
- Molecular identifiers in parsed records are consistent with and traceable to source filenames and repository metadata.
- Parsing round-trip validation: re-export a subset of parsed arrays and compare against original files to confirm lossless conversion (within floating-point precision).

## Limitations

- Parsing logic is modality-specific and format-dependent; different instrument manufacturers or raw data formats (e.g., Bruker, Varian, JEOL, or generic CSV) require separate parsers or manual format inspection.
- Chemical shift normalization assumes access to reference standards or calibration metadata; without these, offsets may introduce systematic error.
- Intensity normalization (e.g., min–max vs. z-score) affects downstream model behavior; choice should be documented and justified.
- Large spectral datasets (50+ GB as recommended) may require chunked I/O or memory-mapped arrays to avoid out-of-memory errors on systems with <16 GB RAM.

## Evidence

- [other] Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities.: "Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities."
- [other] The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data: "The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data"
- [other] Download and extract spectral datasets from the three Zenodo repositories (10.5281/zenodo.16076914, 10.5281/zenodo.16257786, 10.5281/zenodo.17284940).: "Download and extract spectral datasets from the three Zenodo repositories (10.5281/zenodo.16076914, 10.5281/zenodo.16257786, 10.5281/zenodo.17284940)."
- [readme] At least 16GB RAM to handle datasets and model training.: "At least 16GB RAM to handle datasets and model training."
- [other] Implement data curation functions to filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries.: "Implement data curation functions to filter spectra by quality metrics (signal-to-noise ratio, peak count thresholds) and remove duplicates or corrupted entries."
