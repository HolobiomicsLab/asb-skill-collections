---
name: msi-feature-metadata-preservation
description: Use when you are converting a processed Cardinal MSImagingExperiment object (containing normalized peaks, optional spatial shrunken centroids segmentation, and feature m/z annotations) into a Seurat object for downstream pathway analysis, differential metabolite expression, or integrative.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - R
  - Cardinal
  - Seurat
  techniques:
  - CE-MS
  - MS-imaging
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI Feature Metadata Preservation

## Summary

Preserve mass-to-charge (m/z) feature metadata and spatial coordinates during conversion of Cardinal MSI objects to Seurat-compatible spatial objects, ensuring downstream annotation and analysis retain complete feature provenance and spatial context.

## When to use

You are converting a processed Cardinal MSImagingExperiment object (containing normalized peaks, optional spatial shrunken centroids segmentation, and feature m/z annotations) into a Seurat object for downstream pathway analysis, differential metabolite expression, or integrative spatial-omics work, and you need to preserve m/z values, feature identifiers, and pixel spatial coordinates so that later annotation lookups and spatial visualizations remain traceable.

## When NOT to use

- Input data is already a Seurat object with complete m/z and spatial metadata intact — conversion would be redundant.
- Feature m/z values are unavailable or have been stripped from the Cardinal object before conversion — metadata preservation will fail silently.
- Spatial coordinates have been aggregated or summarized (e.g., averaged to tissue regions) — pixel-level coordinate preservation is not applicable.

## Inputs

- Cardinal MSImagingExperiment object (normalized peaks with feature m/z metadata and pixel coordinates)
- Optional spatial shrunken centroids (SSC) segmentation results from Cardinal

## Outputs

- Seurat object with 'Spatial' assay (spectral counts preserved)
- Feature metadata (m/z values) in feature meta.data slot
- Spatial coordinates (x, y pixel positions) in spatial slot
- Cardinal-derived annotations (e.g., SSC clusters) in cell metadata

## How to apply

After loading a normalized Cardinal MSImagingExperiment object, invoke the CardinalToSeurat conversion function to extract three key components: (1) spectral intensity counts from the Cardinal object's spectral matrix, (2) feature metadata including m/z values from the feature annotation slot, and (3) pixel spatial coordinates (x, y) from the spatial metadata. Construct a Seurat object with the 'Spatial' assay containing spectral counts, transfer x and y coordinates to the object's spatial slot (preserving the original pixel grid), and store m/z values in the feature meta.data slot so they remain queryable during annotation and visualization steps (e.g., via SearchAnnotations or FindNearestMZ functions). If Cardinal-derived annotations such as spatial shrunken centroids (SSC) clustering results are present, preserve them in the Seurat object's cell metadata to maintain consistency with any upstream Cardinal segmentation. Verify that the returned SpaMTP Seurat object contains non-empty feature meta.data and intact spatial coordinates by checking object dimensions and metadata slot structure before proceeding to downstream analysis.

## Related tools

- **Cardinal** (Source MSI data object containing normalized spectral intensities, m/z feature metadata, and spatial coordinates to be extracted and transferred) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Seurat** (Target object framework providing 'Spatial' assay and metadata slot architecture for storing transferred m/z values and spatial coordinates)
- **SpaMTP** (R package implementing CardinalToSeurat conversion function and downstream functions (SearchAnnotations, FindNearestMZ) that depend on preserved m/z metadata) — https://github.com/GenomicsMachineLearning/SpaMTP

## Evaluation signals

- Feature meta.data slot is non-empty and contains m/z column with numeric values matching the original Cardinal feature set (e.g., dim(seurat_obj@assays$[redacted-email]) > 0).
- Spatial coordinates are present and identical to original Cardinal pixel coordinates (e.g., all.equal(seurat_obj@images$spatial@coordinates, cardinal_coordinates)).
- SearchAnnotations and FindNearestMZ functions return valid results when queried on the converted Seurat object, confirming m/z metadata is accessible.
- Cell metadata contains any SSC clustering or segmentation labels from Cardinal, preserving upstream biological annotations (e.g., 'clusters' column is present and has expected cardinality).
- Spectral assay dimensions match input Cardinal object (number of m/z features and number of pixels preserved exactly).

## Limitations

- The conversion mechanism is not documented in the provided article text (README contains only headers and badges), so specific handling of edge cases (e.g., missing m/z values, non-standard spatial formats, or metadata naming collisions) is not detailed.
- Metadata preservation depends on Cardinal object completeness; if m/z values or coordinates are absent before conversion, no error handling is described.
- Integration with paired targeted metabolic data or pseudo MS/MS-based refinement sections are marked 'To come!' in the source article, so preservation of refined annotations is not yet specified.

## Evidence

- [other] Extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object.: "Invoke the CardinalToSeurat function to extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object."
- [other] Transfer spatial metadata and preserve feature metadata in slots.: "transfer spatial metadata (x, y coordinates) to the object's spatial slot, and preserve feature metadata (m/z values) in the feature meta.data slot."
- [other] Preserve Cardinal-derived annotations in cell metadata.: "Preserve any Cardinal-derived annotations (e.g., SSC clustering results) in the Seurat object's cell metadata for downstream analysis compatibility."
- [readme] SpaMTP inherits from Cardinal and Seurat for spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis. Build on the foundation of a"
