---
name: spatial-coordinate-metadata-extraction
description: Use when you have raw imzML files (paired with .ibd binary data) from imaging mass spectrometry experiments and need to construct an AnnData object for spatial metabolomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3382
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

# spatial-coordinate-metadata-extraction

## Summary

Extract and organize spatial coordinates and spot identifiers from imzML mass spectrometry files into structured metadata slots within an AnnData object. This skill enables downstream spatial analysis by parsing binary imaging mass spectrometry data into a unified data structure compatible with multi-omics integration workflows.

## When to use

You have raw imzML files (paired with .ibd binary data) from imaging mass spectrometry experiments and need to construct an AnnData object for spatial metabolomics analysis. This skill is necessary when your input is in imzML format rather than CSV or other tabular formats, and you require spatial coordinates to be preserved as structured metadata for alignment with spatial transcriptomics or other co-registered modalities.

## When NOT to use

- Input is already in CSV or tabular format; use `read_sm_csv_as_anndata` instead.
- Spatial coordinates are not required or data is from non-imaging mass spectrometry.
- The imzML file lacks a corresponding .ibd binary data file needed for complete parsing.

## Inputs

- imzML file (imaging mass spectrometry metadata XML format)
- .ibd file (ion binary data accompanying imzML)

## Outputs

- AnnData object with spatial metabolomics data
- Intensity matrix (.X slot)
- m/z feature annotations (.var slot)
- Spatial coordinates and spot identifiers (.obs slot)

## How to apply

Use the `spatialmeta.pp.read_sm_imzml_as_anndata()` function to load the imzML file and its accompanying .ibd binary file. The function parses mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix where m/z values serve as columns (variables) and spatial coordinates as rows (observations). Spatial coordinates and spot identifiers are stored in the `.obs` slot of the resulting AnnData object, intensity data in `.X`, and m/z values in `.var`. This organization maintains the spatial topology needed for subsequent alignment operations (e.g., `spot_align_byknn`) and cross-modal pattern identification.

## Related tools

- **spatialMETA** (Preprocessing module providing read_sm_imzml_as_anndata function for loading and parsing imzML spatial metabolomics data into AnnData format) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
from spatialmeta.pp import read_sm_imzml_as_anndata; adata = read_sm_imzml_as_anndata('sample.imzML')
```

## Evaluation signals

- Verify that the returned AnnData object has non-empty .obs containing spatial coordinates (x, y pixel positions) and spot identifiers.
- Confirm that .var contains m/z values (mass-to-charge ratios) spanning the expected mass range for the experiment.
- Check that .X intensity matrix has shape (n_spots, n_features) where n_spots matches the number of spatial locations in the imzML file.
- Validate that no spatial coordinates are NaN or out-of-bounds for the instrument's raster region.
- Verify that intensity values are numeric and fall within the expected dynamic range for mass spectrometry data (no truncation artifacts).

## Limitations

- Requires both imzML and .ibd files to be present and valid; missing or corrupted .ibd files will cause parsing failure.
- The function assumes standard imzML structure; non-standard or vendor-specific imzML variants may not parse correctly.
- Spatial resolution is inherited from the instrument's raster acquisition; no upsampling or interpolation is performed by this step alone.
- m/z calibration is not corrected; subsequent steps (e.g., `get_mz_reference`) may be needed for cross-sample m/z alignment.

## Evidence

- [other] Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations).: "Parse mass spectrometry intensities and m/z values from the binary format, organizing them into a feature matrix with m/z as columns (variables) and spatial coordinates as rows (observations)."
- [other] Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream metabolomic analysis.: "Construct an AnnData object with the intensity matrix in the .X slot, m/z values stored in .var, spatial coordinates and spot identifiers in .obs, and return the formatted object for downstream"
- [other] Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module.: "Load the imzML file and its accompanying ibd (ion binary data) file using the read_sm_imzml_as_anndata function from spatialMETA preprocessing module."
- [other] spatialmeta.pp.read_sm_imzml_as_anndata: "spatialmeta.pp.read_sm_imzml_as_anndata"
