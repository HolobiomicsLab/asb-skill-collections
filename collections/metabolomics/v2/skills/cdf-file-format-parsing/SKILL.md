---
name: cdf-file-format-parsing
description: 'Use when when you have multiple CDF files from mass spectrometry imaging
  experiments (e.g., root tissue MALDI-MS data) that need to be ingested into Matlab
  for linear imaging analysis. Trigger: presence of .'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Matlab (netCDF/CDF I/O functions)
  - DIMPLE-code
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
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

# cdf-file-format-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Batch parsing of NetCDF/CDF imaging files to extract and structure mass spectrometry spectral data (m/z values, intensity arrays, spatial coordinates) into Matlab workspace arrays for downstream DIMPLE pipeline analysis.

## When to use

When you have multiple CDF files from mass spectrometry imaging experiments (e.g., root tissue MALDI-MS data) that need to be ingested into Matlab for linear imaging analysis. Trigger: presence of .cdf file directories and a requirement to aggregate spectral intensity, m/z calibration, and spatial metadata into a unified workspace structure.

## When NOT to use

- CDF files are already loaded into Matlab workspace or pre-converted to .mat format (use directly instead)
- Input data are in non-CDF formats (mzML, mzXML, HDF5); use format-specific parsers
- Only single CDF file needs parsing; use native ncread() or netCDF libraries directly

## Inputs

- Cell array of CDF file paths (e.g., {'B73-root11/*.cdf', 'OG1/*.cdf'})
- Directory tree of .cdf files from mass spectrometry imaging experiments
- Matlab workspace or script environment

## Outputs

- Matlab workspace struct/cell array containing aggregated spectral data, m/z calibration vectors, and spatial metadata
- Pre-processed imaging arrays ready for DIMPLE linear analysis pipeline

## How to apply

The batchcdfread function iterates through a cell array or file list of CDF file paths, using Matlab's native NetCDF/CDF I/O functions to read each file. For each CDF file, extract the spectral intensity arrays, m/z values (mass-to-charge calibration), and spatial coordinates (x, y position or linear position along the root axis). Organize these heterogeneous arrays into a structured cell or struct array with consistent field names (spectra, mz, spatial_metadata). Aggregate all batch results into a single workspace structure compatible with downstream DIMPLE analysis steps, ensuring all files are parsed with matching m/z binning and spatial reference frames.

## Related tools

- **Matlab (netCDF/CDF I/O functions)** (Reads and parses CDF file format; extracts spectral intensity, m/z values, and spatial coordinates)
- **DIMPLE-code** (Downstream pipeline that consumes batchcdfread output for mass spectrometry imaging analysis along a linear axis) — github.com/dickinsonlab/DIMPLE-code

## Examples

```
batchcdfread({'B73-root11/*.cdf', 'OG1/*.cdf'}, output_workspace)
```

## Evaluation signals

- Workspace struct contains expected fields (spectra, mz, spatial_metadata) with consistent dimensions across all batch files
- m/z values are monotonically increasing and match instrumental calibration (no NaN or Inf values)
- Spectral intensity arrays match the dimensions of spatial coordinates (e.g., if 100 x/y positions, intensity matrix is 100 × mz_bins)
- All input CDF files are represented in output struct (no missing files or corrupted reads)
- Output workspace is compatible with downstream DIMPLE pipeline functions (no type mismatches or missing required fields)

## Limitations

- Function assumes all CDF files share compatible m/z binning and instrument calibration; heterogeneous calibrations across files may require alignment preprocessing
- Spatial coordinates must be extractable from CDF metadata; files lacking valid x, y, or linear position information will fail or require manual annotation
- No built-in handling of corrupted or incomplete CDF files; error handling and validation must be implemented upstream
- Batch processing performance scales with file count and spectral resolution; very large datasets may require memory management or chunked I/O

## Evidence

- [other] The batchcdfread function was developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University to enable batch processing of CDF files into Matlab workspaces for use in the DIMPLE pipeline.: "The batchcdfread function was developed by Yifan Meng in Dr. Richard N. Zare's lab at Stanford University to enable batch processing of CDF files into Matlab workspaces for use in the DIMPLE pipeline."
- [other] 1. Parse input CDF file paths provided as a cell array or file list. 2. Iterate through each CDF file and read the spectral data using Matlab's netCDF/CDF I/O functions. 3. Extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position) from each CDF file. 4. Organize extracted data into a structured array or cell array with fields for spectra, m/z values, and spatial metadata. 5. Return the aggregated workspace structure containing all batch spectra in a format compatible with downstream DIMPLE pipeline analysis.: "Iterate through each CDF file and read the spectral data using Matlab's netCDF/CDF I/O functions. Extract spectral intensity arrays, m/z values, and spatial coordinates (x, y, or linear position)"
- [readme] cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025.: "cdf files and available Matlab workspaces are provided for the roots that were analyzed in Sama et al. 2025."
- [readme] Computational pipeline for analyzing mass spectrometry imaging data along a linear axis.: "Computational pipeline for analyzing mass spectrometry imaging data along a linear axis."
