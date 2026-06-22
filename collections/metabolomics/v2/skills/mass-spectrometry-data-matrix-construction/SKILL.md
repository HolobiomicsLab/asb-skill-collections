---
name: mass-spectrometry-data-matrix-construction
description: Use when you have raw spatial metabolomics imzML files (paired with .ibd binary data files) that need to be loaded into a unified AnnData format for integration with spatial transcriptomics data or for cross-modal spatial pattern identification in single or multiple sample datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - spatialMETA
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-matrix-construction

## Summary

Parse mass spectrometry intensities and m/z values from binary imzML files and organize them into a feature matrix where m/z values form columns (variables) and spatial coordinates form rows (observations), then encapsulate into an AnnData object for downstream metabolomic analysis.

## When to use

You have raw spatial metabolomics imzML files (paired with .ibd binary data files) that need to be loaded into a unified AnnData format for integration with spatial transcriptomics data or for cross-modal spatial pattern identification in single or multiple sample datasets.

## When NOT to use

- Input is already in CSV or tabular format (use read_sm_csv_as_anndata instead)
- Data lacks spatial coordinates or spot identifiers
- Binary data file (.ibd) is missing or corrupted

## Inputs

- imzML file (spatial metabolomics metadata file)
- ibd file (ion binary data file, paired with imzML)

## Outputs

- AnnData object with intensity matrix in .X, m/z values in .var, spatial coordinates in .obs

## How to apply

Use spatialmeta.pp.read_sm_imzml_as_anndata to simultaneously parse the imzML XML metadata and accompanying .ibd (ion binary data) file. Extract mass spectrometry intensities and their corresponding m/z values from the binary format, organizing intensities into a feature matrix with observations indexed by spatial coordinates (x, y positions) and variables indexed by m/z ratios. Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var (variable metadata), spatial coordinates and spot identifiers in .obs (observation metadata), ensuring consistent indexing and data types. This structured format enables subsequent alignment to a unified resolution with spatial transcriptomics data and cross-modal pattern discovery.

## Related tools

- **spatialMETA** (Provides read_sm_imzml_as_anndata preprocessing function for loading and parsing imzML files into AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.pp import read_sm_imzml_as_anndata; adata_sm = read_sm_imzml_as_anndata('sample.imzML')
```

## Evaluation signals

- AnnData .X matrix has shape (n_spots, n_mz_features) with non-negative intensity values
- .var index contains unique m/z values sorted in ascending order
- .obs index contains spatial coordinates (x, y) and spot identifiers with no missing values
- Data types are consistent: intensities as float/int, m/z as float, coordinates as numeric
- No NaN or infinite values in intensity matrix; m/z values fall within expected mass range (e.g., 50–2000 m/z for typical spatial metabolomics)

## Limitations

- Requires both imzML and .ibd files to be present and correctly paired; missing or corrupted binary data will cause parsing failure
- Performance depends on file size; very large imzML datasets may require substantial memory for full matrix construction
- m/z alignment across samples requires subsequent use of get_mz_reference or manual harmonization to handle mass shift or calibration drift

## Evidence

- [other] Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module.: "Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module"
- [other] Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations).: "Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations)"
- [other] Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream metabolomic analysis.: "Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream"
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [other] spatialmeta.pp.read_sm_imzml_as_anndata: "spatialmeta.pp.read_sm_imzml_as_anndata"
