---
name: anndata-object-initialization-and-structuring
description: Use when when you have imzML and accompanying ibd (ion binary data) files
  from spatial metabolomics experiments and need to load them into a unified AnnData
  object representation for integration with spatial transcriptomics or other spatial
  multi-omics data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
  license_tier: open
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

# anndata-object-initialization-and-structuring

## Summary

Construct and populate AnnData objects from spatial metabolomics imzML files by parsing mass spectrometry intensities, m/z values, and spatial coordinates into a structured matrix format. This skill is essential for integrating spatial metabolomics data into the SpatialMETA workflow for downstream multi-omics analysis.

## When to use

When you have imzML and accompanying ibd (ion binary data) files from spatial metabolomics experiments and need to load them into a unified AnnData object representation for integration with spatial transcriptomics or other spatial multi-omics data. Use this skill as the first preprocessing step before alignment, filtering, or cross-modal pattern identification.

## When NOT to use

- Input metabolomics data is already in CSV or tabular format — use read_sm_csv_as_anndata instead
- Data is from spatial transcriptomics (ST) rather than spatial metabolomics (SM) — use appropriate ST readers
- You have pre-processed AnnData objects that are ready for alignment — skip to joint_adata_sm_st step

## Inputs

- imzML file (imaging mass spectrometry XML format descriptor)
- ibd file (ion binary data file accompanying imzML)
- spatial coordinates (x, y positions or spot identifiers from imzML metadata)

## Outputs

- AnnData object with intensity matrix in .X slot
- m/z values stored in .var (feature metadata)
- spatial coordinates and spot identifiers in .obs (observation metadata)

## How to apply

Use the read_sm_imzml_as_anndata function from the spatialMETA preprocessing module to load and parse the imzML file along with its ibd binary companion. The function extracts mass spectrometry intensities and m/z values from the binary format and organizes them into a feature matrix where m/z values serve as columns (variables/features) and spatial coordinates with spot identifiers form the rows (observations). Populate the AnnData object by storing the intensity matrix in the .X slot, m/z values in .var, spatial coordinates and spot identifiers in .obs, then return the formatted object. This structure ensures compatibility with subsequent SpatialMETA workflow steps including normalization, alignment, and joint analysis with spatial transcriptomics data.

## Related tools

- **spatialMETA** (Provides the read_sm_imzml_as_anndata preprocessing function and AnnData-based framework for spatial metabolomics data integration) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.pp import read_sm_imzml_as_anndata; adata_sm = read_sm_imzml_as_anndata('sample.imzML')
```

## Evaluation signals

- AnnData object X matrix has shape (n_spots, n_mz_features) with numeric intensity values
- .var contains m/z values as a continuous feature index with no missing values
- .obs contains spatial coordinate columns and spot identifiers matching the imzML file
- No NaN or inf values in intensity matrix after parsing; all intensity values are non-negative
- Object can be successfully passed to downstream SpatialMETA functions (e.g., filter_cells_sm, filter_metabolites_sm, normalize_total_joint_adata_sm_st)

## Limitations

- Requires both imzML and ibd files to be present and co-located; missing ibd file will cause parsing failure
- Binary data parsing depends on correct imzML schema version; non-standard or corrupted imzML headers may fail silently or produce incorrect feature matrices
- Spatial resolution and coordinate precision are inherited from the imzML file; no resampling or coordinate validation is performed during initialization
- Very large imzML files may cause memory issues; no streaming or chunked reading is mentioned in the workflow

## Evidence

- [other] Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module.: "Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module"
- [other] Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations).: "Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations)"
- [other] Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream metabolomic analysis.: "Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream"
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
- [other] spatialmeta.pp.read_sm_imzml_as_anndata: "spatialmeta.pp.read_sm_imzml_as_anndata"
