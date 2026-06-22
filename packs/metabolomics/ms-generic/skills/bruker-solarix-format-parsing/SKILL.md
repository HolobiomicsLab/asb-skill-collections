---
name: bruker-solarix-format-parsing
description: Use when you have acquired Bruker Solarix FT-ICR-MS raw data (e.g., ESI_NEG_SRFA.d) and need to programmatically access the transient time-domain signal and metadata for zero-filling, apodization windowing (e.g., Hanning), or mass calibration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - Bruker Solarix
  - numpy
  - matplotlib
  - Bruker Solarix instrument
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
- import numpy as np
- from matplotlib import pyplot
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bruker-solarix-format-parsing

## Summary

Parse and load raw Bruker Solarix FT-ICR transient data files (.d directories containing ser/fid files) into an in-memory mass spectrum object. This skill enables downstream signal processing, apodization, and peak detection on vendor-specific FTICR formats without manual format conversion.

## When to use

You have acquired Bruker Solarix FT-ICR-MS raw data (e.g., ESI_NEG_SRFA.d) and need to programmatically access the transient time-domain signal and metadata for zero-filling, apodization windowing (e.g., Hanning), or mass calibration. Use this when raw vendor files must be loaded into a unified Python object model rather than exported to intermediate formats.

## When NOT to use

- Input is already a centroided or processed mass list (CSV, mzML, or Excel); use generic mass list import instead.
- Raw transient file is corrupted or metadata is missing; pre-validate .d directory structure and ser/fid file integrity.
- You require access to all isotopic fine structure or need multi-scan averaging beyond what the transient acquisition provides.

## Inputs

- Bruker Solarix .d directory (containing ser or fid transient file and metadata)
- File path string to .d directory
- CoreMS MSParameters configuration object

## Outputs

- CoreMS MassSpectrum object with m/z peaks, abundances, and metadata
- Processed FT-magnitude spectrum (m/z array, abundance array)
- Spectrum quality metrics (resolving power, peak count, m/z range)

## How to apply

Import the ReadBrukerSolarix class from corems.transient.input.brukerSolarix and instantiate it with the file path to the .d directory. The parser reads the transient (ser/fid) file and metadata, populating a mass spectrum object with time-domain signal, acquisition parameters, and instrument configuration. Configure CoreMS MSParameters (e.g., apodization window function, zero-fill settings) before calling the processing pipeline to generate the final m/z-domain spectrum. The resulting object contains detected m/z peaks, abundances, and resolving power metrics suitable for molecular formula assignment or spectral quality evaluation.

## Related tools

- **CoreMS** (Provides ReadBrukerSolarix class to parse Bruker Solarix transient files and MassSpectrum object model for signal processing and peak detection.) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Array manipulation and mathematical operations on transient time-domain signal during apodization and FFT.)
- **Bruker Solarix instrument** (Source of raw .d directory format and transient acquisition parameters.)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix
ms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d').mass_spectrum
print(f'Peaks: {len(ms.peaks)}, m/z range: {ms.min_mz:.2f}-{ms.max_mz:.2f}')
```

## Evaluation signals

- MassSpectrum object is successfully instantiated with non-empty m/z and abundance arrays after parsing.
- Detected m/z range matches expected analyte region (e.g., 155.87 to 999.66 m/z for SRFA ESI-MS).
- Peak count is consistent with prior acquisitions or expected complexity (e.g., 10588 peaks for ESI_NEG_SRFA.d with stated parameters).
- Metadata fields (instrument model, acquisition date, transient length) are correctly extracted and accessible.
- Apodization window and zero-fill parameters are reflected in the processed spectrum properties without errors.

## Limitations

- Parser supports Bruker Solarix CompassXtract and raw transient formats (ser/fid) in FT magnitude mode only; does not support phase-corrected or other vendor formats.
- Requires Bruker .d directory structure to be intact; partial or reorganized files will fail to load.
- No automatic retry or recovery for incomplete or corrupted transient data; user must validate file integrity before parsing.
- Performance depends on transient file size and system memory; very large transients (>1 GB) may require in-memory management.

## Evidence

- [other] Import the ReadBrukerSolarix class from CoreMS and load the ESI_NEG_SRFA.d transient file.: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [readme] Bruker Solarix transient data loading capability.: "Bruker Solarix transients, ser and fid (FT magnitude mode only)"
- [other] Result of parsing: 10588 detected m/z peaks spanning from 155.87 to 999.66.: "Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66."
- [readme] Framework supports vendor data format access.: "CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows"
- [readme] Self-containing hierarchical data structure design.: "The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data"
