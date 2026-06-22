---
name: gc-ms-chromatogram-processing
description: Use when when working with raw GC-MS data in NetCDF (ANDI) format that requires peak detection, baseline removal, and retention time alignment before spectral matching against reference libraries such as PNNLMetV20191015.MSL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
---

# gc-ms-chromatogram-processing

## Summary

Extraction and processing of gas chromatography–mass spectrometry (GC-MS) chromatographic peaks from raw NetCDF data, including baseline correction, peak deconvolution, and retention index calibration to enable downstream compound identification via spectral library matching.

## When to use

When working with raw GC-MS data in NetCDF (ANDI) format that requires peak detection, baseline removal, and retention time alignment before spectral matching against reference libraries such as PNNLMetV20191015.MSL. Apply this skill as a prerequisite step when compound identification depends on accurate peak area, retention index, and low-resolution mass spectral extraction.

## When NOT to use

- Input is already a curated feature table or molecular formula assignment table (skip to spectral matching or annotation).
- Data are from high-resolution GC-MS instruments (e.g., GC-Orbitrap) where isotopic fine structure and ultrahigh mass accuracy require FT-MS calibration workflows instead.
- Chromatographic peaks are already manually identified or deconvolved by vendor software; use peak extraction workflows instead.

## Inputs

- Raw GC-MS data in NetCDF/ANDI format (.cdf)
- Instrument parameter metadata (column type, carrier gas, temperature ramp)
- Alkane retention time calibration standard run data
- Mass spectrometry signal data (m/z and intensity pairs per scan)

## Outputs

- Deconvolved chromatographic peaks with assigned retention indices
- Extracted low-resolution mass spectra per peak
- Peak table with compound name, m/z, retention index, peak area (CSV or HDF5)
- Baseline-corrected chromatogram

## How to apply

Load raw GC-MS data using ReadAndiNetCDF to parse instrument parameters and chromatographic signals. Apply baseline detection and subtraction to remove chemical and instrumental noise. Perform peak picking using first and second derivative methods with automatic or manual noise threshold selection. Deconvolve m/z-based chromatographic peaks to isolate individual compounds. Apply GC_RI_Calibration by aligning detected peaks against alkane reference standards (typically C7–C40) to compute retention indices. Extract the low-resolution mass spectrum from each deconvolved peak. Export processed peak tables with retention indices, m/z values, and peak area measurements to CSV or HDF5 format for downstream spectral matching and compound identification.

## Related tools

- **CoreMS** (Provides ReadAndiNetCDF for data loading, GC_RI_Calibration for retention index alignment, baseline detection/subtraction, and peak deconvolution via the LowResMassSpectralMatch class) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Aggregates deconvolved peaks and metadata into structured DataFrames for export and downstream analysis)
- **numpy** (Supports numerical operations for peak shape fitting, derivative calculations, and m/z-based peak deconvolution)
- **Docker** (Containerizes CoreMS environment with dependencies to ensure reproducible chromatogram processing across platforms)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.mass_spectra.input_output.andi_netcdf import ReadAndiNetCDF; gc_ms_data = ReadAndiNetCDF('sample.cdf'); gc_ms_data.apply_tic_normalization(); gc_ms_data.baseline_detection(); gc_ms_data.run_ric_calibration(); df = gc_ms_data.to_pandas()
```

## Evaluation signals

- Baseline removal reduces noise floor by >50% while preserving peak shape (check via visual inspection or SNR ratio before/after).
- Retention indices for alkane standards match expected literature values (e.g., C10 = 1000, C12 = 1200) within ±10 RI units.
- Extracted low-resolution mass spectra show expected isotope ratios and fragmentation patterns consistent with reference spectra or known compounds.
- Peak deconvolution produces non-overlapping m/z traces and individual peak areas sum to total integrated chromatogram area within ±5%.
- Output CSV/HDF5 files contain no missing values for required columns (retention index, m/z, peak area) and all records pass schema validation.

## Limitations

- Baseline detection performance degrades on noisy or heavily contaminated GC-MS runs with low signal-to-noise ratio (<3:1); manual threshold adjustment may be required.
- Peak deconvolution is m/z-based and may fail to resolve co-eluting isomers with highly similar mass spectra; retention index calibration does not distinguish structural isomers.
- Retention index calibration accuracy depends on quality and coverage of alkane standards; missing or poorly resolved alkane peaks can introduce systematic errors (>20 RI units).
- Low-resolution mass spectra (nominal mass accuracy) limit subsequent spectral matching to coarse library searches; high-resolution data or complementary GC-VUV are needed for isomer discrimination.
- The skill assumes single-column GC-MS data; comprehensive two-dimensional GC-MS (GCxGC) or LC-MS workflows require adapted peak deconvolution and retention time modeling.

## Evidence

- [other] Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals.: "Load raw GC-MS data in NetCDF format using ReadAndiNetCDF, parsing instrument parameters and chromatographic signals."
- [other] Apply GC_RI_Calibration to align retention times against reference alkane standards and compute retention indices for each detected peak.: "Apply GC_RI_Calibration to align retention times against reference alkane standards and compute retention indices for each detected peak."
- [readme] Baseline detection, subtraction, smoothing; m/z based Chromatogram Peak Deconvolution, Manual and automatic noise threshold calculation; First and second derivatives peak picking methods; Peak Area Calculation; Retention Index Calibration: "Baseline detection, subtraction, smoothing; m/z based Chromatogram Peak Deconvolution, Manual and automatic noise threshold calculation; First and second derivatives peak picking methods; Peak Area"
- [other] Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index proximity.: "Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index"
- [other] Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank.: "Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank."
