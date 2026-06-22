---
name: metabolite-feature-organization
description: Use when you have raw imzML and ibd (ion binary data) files from spatial mass spectrometry imaging and need to convert them into a standardized AnnData representation where m/z values are features (columns), spatial spots are observations (rows), and intensities form the feature matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
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

# metabolite-feature-organization

## Summary

Organize spatial metabolomics mass spectrometry data into a structured AnnData object by parsing binary imzML files, extracting m/z values and intensity matrices, and mapping them to spatial coordinates. This skill is essential for downstream cross-modal spatial analysis in multi-omics workflows.

## When to use

You have raw imzML and ibd (ion binary data) files from spatial mass spectrometry imaging and need to convert them into a standardized AnnData representation where m/z values are features (columns), spatial spots are observations (rows), and intensities form the feature matrix. Use this skill before alignment, normalization, or cross-modal integration with spatial transcriptomics data.

## When NOT to use

- Input data is already in CSV or tabular format (use read_sm_csv_as_anndata instead)
- Mass spectrometry data is from a non-spatial experiment (imzML is specific to spatial imaging)
- AnnData object has already been constructed and validated

## Inputs

- imzML file (text metadata file describing mass spectrometry imaging experiment)
- ibd file (ion binary data file containing mass spectrometry intensities)

## Outputs

- AnnData object with intensity matrix in .X, m/z values in .var, spatial coordinates and spot IDs in .obs

## How to apply

Load the imzML file and its accompanying ibd file using the spatialmeta.pp.read_sm_imzml_as_anndata function from the spatialMETA preprocessing module. This function parses mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations). Construct an AnnData object with the intensity matrix stored in the .X slot, m/z values in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream metabolomic analysis. Verify that all spatial spots are represented, m/z values are numeric and monotonically ordered, and intensity values are non-negative.

## Related tools

- **spatialMETA** (Provides the read_sm_imzml_as_anndata preprocessing function that parses imzML/ibd files and constructs AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.pp import read_sm_imzml_as_anndata; adata = read_sm_imzml_as_anndata(imzml_file='sample.imzML', ibd_file='sample.ibd')
```

## Evaluation signals

- AnnData object .X contains non-negative intensity values with shape matching (n_spots, n_mz_features)
- m/z values in .var are numeric, unique, and properly ordered
- Spatial coordinates in .obs correspond exactly to imzML coordinate system (x, y pixel positions)
- No missing values (NaN) in intensity matrix or coordinate data
- Total m/z feature count matches the number of parsed ions in the ibd binary data

## Limitations

- Requires both imzML and ibd files to be present and co-located; missing ibd file will cause read failure
- Binary format compatibility depends on imzML specification version and vendor implementation
- Large imzML files with very high mass resolution or large spatial imaging areas may require substantial memory

## Evidence

- [other] Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module.: "Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module"
- [other] Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations).: "Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations)"
- [other] Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream metabolomic analysis.: "Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream"
- [readme] spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
