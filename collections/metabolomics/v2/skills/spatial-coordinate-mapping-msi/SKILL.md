---
name: spatial-coordinate-mapping-msi
description: Use when after loading and preprocessing a Cardinal MSImagingExperiment
  object (with normalized peaks and optional spatial segmentation results), and before
  conducting spatial statistical tests or co-localization analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  tools:
  - SpaMTP
  - R
  - Cardinal
  - Seurat
  techniques:
  - CE-MS
  - MS-imaging
  license_tier: restricted
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

# Spatial coordinate mapping for MSI

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transfer pixel-level x,y spatial coordinates from a Cardinal MSImagingExperiment object into a Seurat spatial object, preserving the geometric layout of mass spectrometry imaging data for downstream spatial analysis and visualization.

## When to use

After loading and preprocessing a Cardinal MSImagingExperiment object (with normalized peaks and optional spatial segmentation results), and before conducting spatial statistical tests or co-localization analyses. Use this skill when you need to convert MSI pixel coordinates into Seurat's spatial metadata framework to enable integrated spatial-omics visualization and analysis (e.g., ImageDimPlot, ImageMZPlot).

## When NOT to use

- Input data is already a Seurat object with spatial coordinates intact — coordinate mapping has already been performed.
- MSI data lacks pixel-level spatial information (e.g., profiling data without imaging coordinates).
- Coordinates are provided in a non-Cartesian system (e.g., cylindrical or spherical) without prior transformation to x,y Euclidean form.

## Inputs

- Cardinal MSImagingExperiment object (with loaded .imzML or similar MSI data file)
- Pixel spatial coordinates (x, y) from Cardinal coordinates slot
- Spectral intensity matrix (m/z features × pixels)
- Feature metadata (m/z values)

## Outputs

- Seurat object with 'Spatial' assay
- Seurat spatial slot populated with pixel x,y coordinates
- Seurat object ready for spatial visualization (ImageDimPlot, ImageMZPlot) and spatial analysis

## How to apply

Extract the pixel spatial coordinates (x, y) from the Cardinal MSImagingExperiment object's coordinate metadata. Transfer these coordinates into the Seurat object's spatial slot during or immediately after object construction, ensuring each pixel's coordinate pair is correctly mapped to its corresponding feature vector (spectral intensities). Verify that all pixels retain their original x,y positions without rotation, translation, or loss; this preservation is critical for accurate spatial visualization and for downstream spatial statistics that depend on Euclidean distance or neighborhood relationships. Document the coordinate system used (pixel indices vs. physical units) and confirm consistency with any spatial shrunken centroids or segmentation masks also being transferred from Cardinal.

## Related tools

- **Cardinal** (Source MSI data object; provides coordinate extraction and pixel metadata) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Seurat** (Target spatial object framework; receives and stores mapped coordinates in spatial slot) — https://satijalab.org/seurat/
- **SpaMTP** (Wrapper/conversion layer; implements CardinalToSeurat function for coordinate mapping and object conversion) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
# Pseudocode (exact function not publicly documented):
# cardinal_obj <- readImzML('sample.imzML')
# seurat_obj <- CardinalToSeurat(cardinal_obj)
# # Seurat object now has spatial slot with x,y coordinates and 'Spatial' assay populated
```

## Evaluation signals

- All pixels from the original Cardinal object appear in the Seurat spatial slot with correct x,y coordinates; pixel count matches source data.
- Seurat object's spatial coordinates are identical to Cardinal's coordinates (no unexpected translation, rotation, or scaling).
- Spatial visualization functions (ImageDimPlot, ImageMZPlot) render the tissue/sample footprint with correct spatial geometry and no distortion.
- Downstream spatial statistics (neighbor detection, spatial correlation) produce results consistent with manual validation on known tissue landmarks or annotated regions.
- Feature metadata (m/z values) and cell metadata (e.g., SSC cluster assignments) are preserved in parallel with coordinate transfer.

## Limitations

- Coordinate mapping assumes Cardinal and Seurat use compatible coordinate systems; mismatch in origin, scale, or axis orientation will silently produce misaligned spatial objects.
- Large MSI datasets (millions of pixels) may require memory optimization or subsetting before coordinate transfer to avoid computational overhead.
- Spatial coordinate fidelity depends on accurate pixel registration during MSI acquisition; systematic registration errors in the instrument will propagate into the mapped object.
- The README and source code do not provide explicit documentation of the CardinalToSeurat function; implementation details and parameter control are not publicly visible.

## Evidence

- [other] Invoke the CardinalToSeurat function to extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object.: "Invoke the CardinalToSeurat function to extract spectral intensities, m/z feature information, and pixel spatial coordinates from the Cardinal object."
- [other] transfer spatial metadata (x, y coordinates) to the object's spatial slot: "transfer spatial metadata (x, y coordinates) to the object's spatial slot, and preserve feature metadata (m/z values) in the feature meta.data slot."
- [other] Return the converted SpaMTP Seurat object with all Cardinal metadata and spatial information intact.: "Return the converted SpaMTP Seurat object with all Cardinal metadata and spatial information intact."
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat): "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis."
- [readme] Build on the foundation of a Seurat Class Object, this package has three major functionalities: "Build on the foundation of a Seurat Class Object, this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical"
