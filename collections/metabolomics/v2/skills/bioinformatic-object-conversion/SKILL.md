---
name: bioinformatic-object-conversion
description: Use when when you have processed Cardinal MSI data (normalized peak intensities, optional SSC segmentation results) and need to transition to Seurat-based workflows for differential expression, pathway analysis, or integration with spatial transcriptomics data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - SpaMTP
  - R
  - Cardinal
  - Seurat
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
---

# bioinformatic-object-conversion

## Summary

Conversion of mass spectrometry imaging data from one standardized bioinformatic object format to another—specifically, transforming Cardinal MSImagingExperiment objects into Seurat-compatible SpaMTP objects while preserving spectral intensities, spatial coordinates, feature metadata (m/z values), and any derived annotations (e.g., spatial shrunken centroids clustering). This skill enables seamless integration of MSI data into the Seurat ecosystem for downstream spatial-omics analysis.

## When to use

When you have processed Cardinal MSI data (normalized peak intensities, optional SSC segmentation results) and need to transition to Seurat-based workflows for differential expression, pathway analysis, or integration with spatial transcriptomics data. Specifically: the input is a Cardinal MSImagingExperiment object containing spectral data and spatial pixel coordinates; the analysis goal requires Seurat-native functions (e.g., NormalizeData, ScaleData, pathway assays); and you have metadata annotations (m/z feature info, clustering results) that must transfer intact.

## When NOT to use

- Input is already a Seurat object or other non-Cardinal format—no conversion needed.
- Cardinal object is unprocessed or lacks normalized peak intensities; convert only after normalization and quality control are complete.
- Spatial coordinates are missing or cannot be reliably extracted from the Cardinal object; conversion requires valid x, y pixel positions for each spectrum.

## Inputs

- Cardinal MSImagingExperiment object (processed, with normalized peaks and optional SSC segmentation results)
- m/z feature metadata (mass-to-charge ratio values and associated ion identities)
- Pixel spatial coordinates (x, y pixel positions)
- Optional: Cardinal-derived annotations (SSC clustering labels, peak classifications)

## Outputs

- Seurat object with 'Spatial' assay
- SpaMTP-compatible object (inherits Seurat Class Object)
- Transferred spatial coordinates (in spatial slot)
- Transferred feature metadata (m/z values in feature meta.data)
- Transferred Cardinal annotations (in cell/pixel metadata)

## How to apply

Invoke the CardinalToSeurat conversion function on a loaded and processed Cardinal MSImagingExperiment object. The function extracts three core components: (1) spectral intensities (m/z feature counts per pixel), (2) pixel spatial coordinates (x, y locations), and (3) feature metadata (m/z values and ion identities). These are packaged into a Seurat object with the 'Spatial' assay containing spectral counts, spatial metadata transferred to the object's spatial coordinate slot, and feature metadata (m/z, annotations) preserved in the feature meta.data slot. Any Cardinal-derived annotations—such as SSC-based clustering assignments or peak classifications—are transferred to the Seurat object's cell (pixel) metadata. The rationale: this preserves all experimental and computational context while enabling access to Seurat's rich statistical and visualization ecosystem (differential metabolite analysis, CreatePathwayAssay, ImageDimPlot, etc.).

## Related tools

- **Cardinal** (Source object format; provides MSImagingExperiment class, normalization, and segmentation (SSC) functionality for input data preparation) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Seurat** (Target object format and downstream analysis platform; provides Spatial assay, NormalizeData, ScaleData, pathway assays, and visualization functions post-conversion) — https://satijalab.org/seurat/
- **SpaMTP** (Wrapper package inheriting both Cardinal and Seurat functionalities; implements CardinalToSeurat conversion and provides integrative spatial-omics analysis tools) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
spotted_seurat <- CardinalToSeurat(spotted_cardinal); DefaultAssay(spotted_seurat) <- "Spatial"; spotted_seurat <- NormalizeData(spotted_seurat)
```

## Evaluation signals

- Seurat object is successfully created and contains a 'Spatial' assay with spectral intensity counts matching the original Cardinal object's peak matrix.
- Spatial coordinates (x, y pixel positions) are present in the Seurat object's spatial coordinate slot and match the original Cardinal MSI pixel positions.
- Feature metadata (m/z values and ion annotations) are preserved in the feature meta.data slot with no loss of information.
- Cardinal-derived metadata (e.g., SSC cluster assignments) are transferred to the Seurat object's cell metadata (pixel metadata) and remain accessible via standard Seurat accessors.
- Standard Seurat functions (NormalizeData, ScaleData, CreatePathwayAssay, ImageDimPlot) execute without error on the converted object.

## Limitations

- Conversion assumes the Cardinal object has been previously normalized and quality-filtered; unnormalized or raw data may not transfer meaningful spectral intensities.
- Spatial resolution and pixel metadata are preserved only if they exist in the source Cardinal object; missing spatial information cannot be imputed during conversion.
- The conversion is one-directional (Cardinal → Seurat); reverse conversion back to Cardinal format is not part of this workflow and may require separate tools.
- Feature annotation accuracy depends on prior Cardinal-based m/z assignment and lipid nomenclature curation; errors in m/z matching or ion naming propagate to the converted Seurat object.

## Evidence

- [methods] Load a processed Cardinal MSImagingExperiment object containing normalized peaks and optional spatial shrunken centroids (SSC) segmentation results.: "Load a processed Cardinal MSImagingExperiment object containing normalized peaks and optional spatial shrunken centroids (SSC) segmentation results."
- [methods] Construct a Seurat object with the 'Spatial' assay containing spectral counts, transfer spatial metadata (x, y coordinates) to the object's spatial slot, and preserve feature metadata (m/z values) in the feature meta.data slot.: "Construct a Seurat object with the 'Spatial' assay containing spectral counts, transfer spatial metadata (x, y coordinates) to the object's spatial slot, and preserve feature metadata (m/z values) in"
- [methods] Preserve any Cardinal-derived annotations (e.g., SSC clustering results) in the Seurat object's cell metadata for downstream analysis compatibility.: "Preserve any Cardinal-derived annotations (e.g., SSC clustering results) in the Seurat object's cell metadata for downstream analysis compatibility."
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis. Build on the foundation of a Seurat Class Object: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis. Build on the foundation of a"
