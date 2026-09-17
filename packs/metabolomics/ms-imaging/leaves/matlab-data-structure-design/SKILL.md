---
name: matlab-data-structure-design
description: Use when you have multiple CDF files containing mass spectrometry imaging
  data (spectra, m/z arrays, and spatial coordinates) that need to be ingested into
  MATLAB for the DIMPLE pipeline or similar linear-axis mass spectrometry imaging
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Matlab
  - MATLAB netCDF/CDF I/O functions
  - batchcdfread
  - DIMPLE pipeline
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.09.22.677919v1
  title: DIMPLE
evidence_spans:
- cdf files and available Matlab workspaces are provided
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dimple_cq
    doi: 10.1101/2025.09.22.677919v1
    title: DIMPLE
  dedup_kept_from: coll_dimple_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.09.22.677919v1
  all_source_dois:
  - 10.1101/2025.09.22.677919v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MATLAB Data Structure Design for Mass Spectrometry Imaging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and organize MATLAB data structures to aggregate batch-processed CDF imaging files into a unified workspace format compatible with downstream mass spectrometry analysis pipelines. This skill ensures that spectral intensities, m/z values, and spatial metadata are coherently structured for linear imaging workflows.

## When to use

You have multiple CDF files containing mass spectrometry imaging data (spectra, m/z arrays, and spatial coordinates) that need to be ingested into MATLAB for the DIMPLE pipeline or similar linear-axis mass spectrometry imaging analysis. Apply this skill when raw CDF files must be transformed into a single, consistently-formatted workspace that preserves spectral intensities, m/z calibration, and spatial position metadata.

## When NOT to use

- CDF files have already been converted to a different format (e.g., HDF5, MAT) by another preprocessing step — use the converted format directly instead.
- Spectral data is already loaded into MATLAB as a pre-assembled array or table — design your structure based on existing format rather than re-ingesting from CDF.
- You are performing real-time streaming analysis where data cannot be held in memory as a unified structure — use file-based or incremental processing instead.

## Inputs

- CDF files (NetCDF format) containing spectral intensity arrays, m/z values, and spatial coordinates
- File paths or cell array of CDF file names
- Spatial metadata (linear position, x, y coordinates, or sample identifiers)

## Outputs

- MATLAB workspace struct or cell array with fields: spectra (intensity arrays), mz (m/z calibration vectors), and spatial_metadata (coordinates or positions)
- .mat file (e.g., B73-root11-workspace.mat) containing the aggregated structure for downstream pipeline use

## How to apply

After reading individual CDF files using MATLAB's netCDF I/O functions, extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position) from each file. Organize these extracted fields into a structured array or cell array with consistent field names and data types across all samples. Aggregate the individual structures into a single workspace object (e.g., a struct array or table) that maintains the correspondence between spectra, m/z calibration, and spatial metadata. Validate that all samples have matching m/z array lengths and that spatial coordinates are numeric and non-negative. Save the aggregated workspace as a .mat file compatible with downstream DIMPLE pipeline functions.

## Related tools

- **MATLAB netCDF/CDF I/O functions** (Read raw spectral data, m/z arrays, and metadata from CDF files into MATLAB workspace)
- **batchcdfread** (Batch process multiple CDF files and iterate through each to extract and aggregate spectral data) — github.com/dickinsonlab/DIMPLE-code
- **DIMPLE pipeline** (Downstream consumer of the aggregated workspace structure for mass spectrometry imaging analysis along a linear axis) — github.com/dickinsonlab/DIMPLE-code

## Evaluation signals

- All CDF files in the batch are successfully read and no files are skipped or cause read errors.
- The output structure has consistent field names and data types across all samples (e.g., all spectra are numeric arrays, all mz vectors are equal-length, all spatial coordinates are numeric).
- m/z array lengths match across all samples in the structure; spectral intensity array dimensions are consistent within each sample.
- Spatial metadata (position, x/y coordinates) are present, numeric, non-negative, and correspond one-to-one with each spectrum.
- The aggregated .mat file can be loaded and used by downstream DIMPLE pipeline functions without format or dimension mismatches.

## Limitations

- The skill assumes all CDF files conform to a consistent schema (same m/z range, sampling resolution, and metadata fields); heterogeneous CDF formats may require per-file preprocessing.
- Memory constraints may limit batch size for very large imaging datasets; incremental processing or file-based aggregation may be necessary for datasets exceeding available RAM.
- Spatial coordinate metadata must be explicitly present in the CDF files or provided separately; if missing or inconsistent, manual alignment or augmentation is required before structure design.
- No validation is performed on m/z calibration accuracy or spectral quality; downstream pipeline is responsible for flagging or filtering poor-quality spectra.

## Evidence

- [other] Extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position) from each CDF file.: "Extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position) from each CDF file."
- [other] Organize extracted data into a structured array or cell array with fields for spectra, m/z values, and spatial metadata.: "Organize extracted data into a structured array or cell array with fields for spectra, m/z values, and spatial metadata."
- [other] Return the aggregated workspace structure containing all batch spectra in a format compatible with downstream DIMPLE pipeline analysis.: "Return the aggregated workspace structure containing all batch spectra in a format compatible with downstream DIMPLE pipeline analysis."
- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025.: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
- [readme] batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
