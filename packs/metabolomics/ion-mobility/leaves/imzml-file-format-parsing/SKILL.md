---
name: imzml-file-format-parsing
description: Use when you have acquired imaging mass spectrometry (IMS) data stored
  in imzML format (accompanied by an .ibd ion binary data file) and need to load it
  into a Python-based spatial metabolomics workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - spatialMETA
  techniques:
  - LC-MS
  - MS-imaging
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-63915-z
  title: SpatialMETA
evidence_spans:
- spatialMETA is a method for integrating spatial multi-omics data
- spatialmeta.pp.calculate_qc_metrics_sm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spatialmeta_cq
    doi: 10.1038/s41467-025-63915-z
    title: SpatialMETA
  dedup_kept_from: coll_spatialmeta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63915-z
  all_source_dois:
  - 10.1038/s41467-025-63915-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imzml-file-format-parsing

## Summary

Parse imzML files (imaging mass spectrometry data) and their accompanying ibd binary files into a structured AnnData object for spatial metabolomics analysis. This skill converts raw mass spectrometry intensities and m/z values from binary format into a feature matrix organized by spatial coordinates.

## When to use

You have acquired imaging mass spectrometry (IMS) data stored in imzML format (accompanied by an .ibd ion binary data file) and need to load it into a Python-based spatial metabolomics workflow. Use this skill when you are beginning preprocessing of spatial metabolomics data and require a unified AnnData representation compatible with downstream SpatialMETA tools like alignment, filtering, and multi-omics integration.

## When NOT to use

- Input data is already in AnnData format or another preprocessed matrix format (e.g., CSV, TSV feature table) — use direct import instead.
- You are working with non-imaging mass spectrometry data (e.g., bulk metabolomics, untargeted LC-MS without spatial information) — spatial coordinate parsing will fail or be unnecessary.
- The imzML file lacks a corresponding .ibd binary file or the file pair is corrupted — the parser will fail to load intensities.

## Inputs

- imzML file (imaging mass spectrometry data format)
- .ibd file (ion binary data companion file)
- file path(s) pointing to imzML and ibd pair

## Outputs

- AnnData object with intensity matrix in .X slot
- m/z values stored in .var metadata
- spatial coordinates and spot identifiers in .obs metadata

## How to apply

Invoke the read_sm_imzml_as_anndata function from the spatialMETA preprocessing module, passing the imzML file path and its corresponding .ibd file. The function parses mass spectrometry intensities and m/z values from the binary format, constructing a feature matrix where m/z values become columns (variables) and spatial coordinates become rows (observations). Store the intensity matrix in the AnnData .X slot, m/z metadata in .var, spatial coordinates and spot identifiers in .obs, and return the formatted AnnData object for downstream metabolomic analysis steps such as QC filtering, normalization, and spatial alignment.

## Related tools

- **spatialMETA** (Provides the read_sm_imzml_as_anndata preprocessing function for parsing imzML files into AnnData objects; part of the broader spatial multi-omics integration workflow) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.pp import read_sm_imzml_as_anndata; adata = read_sm_imzml_as_anndata('sample.imzML')
```

## Evaluation signals

- AnnData object is returned without parsing errors and validates against the AnnData schema (n_obs > 0, n_vars > 0, .X is a matrix)
- m/z values in .var are numeric, monotonically increasing or sensible range (e.g., 50–2000 m/z), and match the number of columns in .X
- Spatial coordinates in .obs match the number of rows in .X; spot identifiers are unique and traceable to original imzML pixel/scan metadata
- Intensity matrix .X contains non-negative numeric values consistent with mass spectrometry detector output (counts or normalized intensities)
- Downstream SpatialMETA functions (e.g., calculate_qc_metrics_sm, filter_cells_sm) execute without schema or shape mismatches on the returned AnnData object

## Limitations

- Requires both imzML and .ibd files to be present and co-located or explicitly linked; parsing fails silently or with unclear error if either is missing or corrupted.
- No built-in validation of m/z calibration or mass accuracy; assumes the imzML file contains valid, calibrated m/z values from the instrument.
- Memory usage scales with the number of spatial coordinates (pixels/spots) and the number of m/z features; very large imaging datasets may require downsampling or tiling.
- The function does not automatically merge positive and negative ion mode data; use merge_sm_pos_neg separately if both polarities were acquired.

## Evidence

- [other] Load imzML and ibd files using read_sm_imzml_as_anndata: "Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module."
- [other] Parse MS intensities and m/z from binary into feature matrix: "Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations)."
- [other] Construct AnnData with intensity in .X, m/z in .var, coordinates in .obs: "Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream"
- [other] SpatialMETA provides preprocessing functions for spatial metabolomics: "spatialmeta.pp.read_sm_imzml_as_anndata"
