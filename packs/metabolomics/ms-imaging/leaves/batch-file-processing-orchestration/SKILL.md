---
name: batch-file-processing-orchestration
description: Use when when you have multiple CDF imaging files (e.g., from mass spectrometry imaging scans of biological samples) that need to be read into a single Matlab workspace with consistent structure and metadata (spectral intensity, m/z arrays, spatial coordinates).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Matlab NetCDF/CDF I/O functions
  - batchcdfread function
  - DIMPLE pipeline
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1101/2025.09.22.677919v1
  title: DIMPLE
evidence_spans: []
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

# batch-file-processing-orchestration

## Summary

Orchestrate batch ingestion of multiple CDF (NetCDF) imaging files into a structured Matlab workspace, aggregating spectral data, m/z values, and spatial coordinates for downstream mass spectrometry analysis. This skill enables efficient parallel or sequential processing of large imaging datasets typical in developmental mass spectrometry imaging workflows.

## When to use

When you have multiple CDF imaging files (e.g., from mass spectrometry imaging scans of biological samples) that need to be read into a single Matlab workspace with consistent structure and metadata (spectral intensity, m/z arrays, spatial coordinates). Typical trigger: a directory or file list containing 3+ CDF files destined for a linear or spatial imaging pipeline like DIMPLE.

## When NOT to use

- Input files are already merged into a single CDF or HDF5 file — use direct read instead.
- Spectral data are in non-imaging formats (e.g., single MS profiles without spatial metadata) — use simpler file I/O.
- You require real-time streaming or on-disk processing of files too large to aggregate in memory — use chunked or memory-mapped I/O instead.

## Inputs

- cell array of CDF file paths
- file list or directory containing CDF imaging files
- NetCDF/CDF file format spectra with embedded m/z and spatial metadata

## Outputs

- aggregated Matlab workspace structure with all batch spectra
- cell array or struct array with fields: spectra (intensity matrices), m/z values, spatial coordinates
- Matlab .mat file suitable for downstream DIMPLE pipeline analysis

## How to apply

Parse the input CDF file paths as a cell array or file list. Iterate through each CDF file using Matlab's NetCDF/CDF I/O functions (e.g., netcdf functions or dedicated CDF readers). For each file, extract spectral intensity arrays, m/z value vectors, and spatial coordinates (x, y position or linear position along the root/sample axis). Organize extracted data into a structured array or cell array with consistent fields (spectra, m/z, spatial metadata). Return the aggregated workspace structure containing all batch spectra in a format compatible with downstream pipeline analysis (e.g., DIMPLE filtering and segmentation). Validate that all spectra share the same m/z axis and that spatial metadata align with the sample geometry.

## Related tools

- **Matlab NetCDF/CDF I/O functions** (Read spectral intensity arrays, m/z values, and spatial metadata from individual CDF files)
- **batchcdfread function** (Custom batch orchestration function developed in Dr. Zare's lab; wraps NetCDF reads and aggregates output into workspace structure) — github.com/dickinsonlab/DIMPLE-code
- **DIMPLE pipeline** (Downstream consumer of aggregated batch workspace; performs filtering, segmentation, and linear imaging analysis) — github.com/dickinsonlab/DIMPLE-code

## Evaluation signals

- Output workspace contains one entry per input CDF file with no missing or truncated spectra.
- All spectra in the aggregated structure share the same m/z axis (vector length and values match across batch).
- Spatial coordinates are populated and consistent with sample geometry (e.g., linear positions 1 to N for N-scan root imaging).
- Output struct or cell array fields (spectra, m/z, spatial metadata) are present and non-empty for every batch member.
- Aggregated workspace can be directly loaded and processed by DIMPLE filtering/segmentation functions without schema errors.

## Limitations

- Requires sufficient RAM to hold all spectra in memory; large imaging datasets may exceed available workspace.
- Assumes all CDF files follow a consistent internal structure and metadata naming convention (e.g., all contain 'intensity', 'm/z', 'x', 'y' or 'position' fields); heterogeneous or malformed CDF files may cause read failures.
- No built-in error recovery or partial batch completion; a single corrupted CDF file halts the entire batch unless wrapped in error handling.
- Performance scales linearly with file count; no parallelization mentioned in the source material.

## Evidence

- [readme] batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University: "batchcdfread function developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University"
- [other] Iterate through each CDF file and read the spectral data using Matlab's netCDF/CDF I/O functions. 3. Extract spectral intensity arrays, m/z values, and spatial coordinates: "Iterate through each CDF file and read the spectral data using Matlab's netCDF/CDF I/O functions. 3. Extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position)"
- [other] Organize extracted data into a structured array or cell array with fields for spectra, m/z values, and spatial metadata. 5. Return the aggregated workspace structure containing all batch spectra in a format compatible with downstream DIMPLE pipeline analysis.: "Organize extracted data into a structured array or cell array with fields for spectra, m/z values, and spatial metadata. 5. Return the aggregated workspace structure containing all batch spectra in a"
- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
