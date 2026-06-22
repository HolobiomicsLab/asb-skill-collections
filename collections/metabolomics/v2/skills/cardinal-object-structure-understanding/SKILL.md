---
name: cardinal-object-structure-understanding
description: Use when when you have loaded a raw or processed Cardinal MSImagingExperiment object from MS imaging data and need to (1) extract spectral intensities and m/z feature information for conversion to other formats (e.g., Seurat), (2) verify that normalization or spatial segmentation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - Cardinal
  - R
  - Seurat
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(Cardinal)
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

# Cardinal Object Structure Understanding

## Summary

Comprehending the internal structure and slots of a Cardinal MSImagingExperiment object—including spectral intensities, feature metadata (m/z values), spatial coordinates, and optional segmentation results—is foundational for correct extraction, transformation, and downstream analysis in spatial mass spectrometry imaging workflows.

## When to use

When you have loaded a raw or processed Cardinal MSImagingExperiment object from MS imaging data and need to (1) extract spectral intensities and m/z feature information for conversion to other formats (e.g., Seurat), (2) verify that normalization or spatial segmentation (e.g., SSC clustering) results are correctly stored in the object's metadata slots, or (3) plan a transformation or export step that depends on knowing which slots contain spectral counts, pixel coordinates, and annotations.

## When NOT to use

- Input data is already in Seurat format or another non-Cardinal R format; skip directly to Seurat-native workflows.
- You are only performing mass spectrometry peak detection or alignment and do not yet have a processed Cardinal object; structure understanding is premature.
- Your goal is to filter or subset Cardinal data by m/z range without downstream conversion; basic subsetting does not require deep structure inspection.

## Inputs

- Cardinal MSImagingExperiment object (processed, with normalized peaks)
- Optional: Cardinal MSImagingExperiment with spatial segmentation results (e.g., SSC clustering)

## Outputs

- Documented understanding of object structure and slot contents
- Verified spatial coordinate and m/z feature metadata
- Confirmation of segmentation or annotation metadata presence (if applicable)

## How to apply

Begin by loading a Cardinal MSImagingExperiment object (typically from a processed Cardinal object containing normalized peaks and optional spatial shrunken centroids segmentation). Inspect the object's internal structure by examining (1) the main assay slot containing spectral intensity matrices indexed by m/z features and pixel coordinates, (2) the feature metadata (fData or rowData) storing m/z values and feature-level annotations, (3) the spatial metadata (pData or colData) containing x, y pixel coordinates and any sample-level metadata, and (4) any stored results from prior analyses such as SSC clustering assignments or annotation tables. Verify that spatial coordinates are numeric and correctly paired to pixel identifiers, and that feature m/z values are present and in the expected mass range. This understanding enables correct routing of data to conversion functions (e.g., CardinalToSeurat) and ensures downstream tools receive properly structured input.

## Related tools

- **Cardinal** (R package providing MSImagingExperiment class and data containers for MS imaging object structure and slot access) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Seurat** (Target R package for downstream analysis; understanding Cardinal structure enables correct conversion to Seurat Spatial assay) — https://satijalab.org/seurat/
- **SpaMTP** (R package that wraps Cardinal and Seurat classes and provides conversion functions; requires understanding of Cardinal object structure for input validation) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
library(Cardinal); cardinal_obj <- readRDS('processed_cardinal.RDS'); str(cardinal_obj); fData(cardinal_obj)[1:5, ]; pData(cardinal_obj)[1:5, ]
```

## Evaluation signals

- Spectral intensity matrix is accessible and indexed by m/z features (rows) and pixel coordinates (columns).
- Feature metadata (fData/rowData) contains valid m/z values in the expected mass range for the instrument used.
- Spatial metadata (pData/colData) contains numeric x and y coordinates with one entry per pixel, matching the column count of the intensity matrix.
- Any segmentation results (e.g., SSC clustering assignments) are stored in cell metadata and can be retrieved without error.
- Conversion functions (e.g., CardinalToSeurat) can successfully extract and transfer all required slots to the output object without data loss or coordinate mismatch.

## Limitations

- The provided article section contained only a README header and placeholder badge; no detailed documentation of Cardinal slot names, access functions, or metadata column conventions is present in the source material.
- Cardinal object structure may vary between Cardinal versions (e.g., Cardinal 2.x vs. Cardinal 3.x); vignettes are referenced but not fully excerpted in the provided context.
- Spatial coordinate systems (e.g., pixel units vs. physical microns) and m/z calibration state must be verified separately; object structure alone does not confirm data correctness.

## Evidence

- [methods] Load a processed Cardinal MSImagingExperiment object containing normalized peaks and optional spatial shrunken centroids (SSC) segmentation results.: "Load a processed Cardinal MSImagingExperiment object containing normalized peaks and optional spatial shrunken centroids (SSC) segmentation results."
- [methods] Extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object.: "extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object"
- [methods] Preserve any Cardinal-derived annotations (e.g., SSC clustering results) in the Seurat object's cell metadata.: "Preserve any Cardinal-derived annotations (e.g., SSC clustering results) in the Seurat object's cell metadata"
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat).: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat)"
