---
name: spatial-coordinate-integration-with-imaging-data
description: Use when you have a spatial omics dataset (AnnData object with coordinate columns like 'x', 'y', 'z') and an associated tissue image file (e.g., TIFF, PNG, or HE-stained histology), and you need to extract image-based morphological features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3382
  - http://edamontology.org/topic_0769
  tools:
  - scanpy
  - Squidpy
  - anndata
  - napari-spatialdata
  - dask
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- It builds on scanpy and anndata
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_squidpy
    doi: 10.1038/s41592-021-01358-2
    title: squidpy
  dedup_kept_from: coll_squidpy
schema_version: 0.2.0
---

# spatial-coordinate-integration-with-imaging-data

## Summary

Integrate spatial coordinate information from a single-cell dataset with associated tissue microscopy images via an ImageContainer object, enabling joint analysis of morphological features and spatial context. This skill bridges omics data (stored in AnnData) with imaging data to unlock spatially-resolved feature extraction and visualization.

## When to use

You have a spatial omics dataset (AnnData object with coordinate columns like 'x', 'y', 'z') and an associated tissue image file (e.g., TIFF, PNG, or HE-stained histology), and you need to extract image-based morphological features (e.g., texture, intensity, structure) indexed to the spatial observations, or visualize omics measurements overlaid on the tissue image.

## When NOT to use

- Image data is already aligned to a different coordinate system and requires non-trivial reprojection (ImageContainer assumes direct pixel-to-spatial mapping)
- The spatial dataset lacks coordinate information or the image cannot be spatially registered to observations
- You only need statistical summaries of image intensity per region; ImageContainer is optimized for per-observation feature extraction, not bulk aggregation

## Inputs

- AnnData object with spatial coordinates (e.g., obsm['spatial'] or columns 'x', 'y')
- Image file path (TIFF, PNG, or other raster format) coregistered to the coordinate space
- Optional: scale factor or metadata mapping pixel coordinates to spatial observations

## Outputs

- squidpy.im.ImageContainer object (linking AnnData and image data)
- AnnData object with extracted image features stored in obsm (e.g., 'image_features'), obsp (pairwise), or var (per-feature)
- Optional: intermediate dask arrays (if lazy=True) for further custom processing

## How to apply

Create a squidpy.im.ImageContainer by passing the image file path and the coordinate-annotated AnnData object. The ImageContainer automatically aligns pixel coordinates to spatial observation coordinates using the coordinate columns and optional scale parameters. Once instantiated, you can call im.calculate_image_features to extract spatial features (e.g., via Gaussian blur, morphological operators, or deep learning backbones) in either lazy (dask) or eager mode. Lazy computation allows memory-efficient processing of large images; features are materialized into the AnnData object's obsm, obsp, or var slots on demand. Verify alignment by cross-checking observation indices and feature matrix dimensions against the input AnnData.

## Related tools

- **Squidpy** (Provides ImageContainer and im.calculate_image_features for integrating spatial coordinates with microscopy images and extracting spatial features) — https://github.com/scverse/squidpy
- **scanpy** (Provides the AnnData ecosystem and spatial analysis utilities that Squidpy builds upon)
- **anndata** (Defines the AnnData data structure for storing spatial coordinates and feature matrices)
- **napari-spatialdata** (Provides interactive visualization and annotation of the integrated spatial omics and imaging data) — https://github.com/scverse/napari-spatialdata
- **dask** (Enables lazy (out-of-core) computation of image features for memory-efficient processing of large images)

## Examples

```
import squidpy as sq
import anndata as ad
adata = ad.read_h5ad('tissue.h5ad')
im_container = sq.im.ImageContainer(image_path='tissue.tif', adata=adata)
sq.im.calculate_image_features(adata, im_container, features=['texture', 'intensity'], lazy=True)
adata.obsm['image_features']
```

## Evaluation signals

- ImageContainer instantiation succeeds without coordinate mismatch errors; image dimensions and observation count are logged correctly
- Extracted features match the number of spatial observations (e.g., obsm['image_features'].shape[0] == adata.n_obs)
- Features are stored in the correct AnnData slot (obsm, obsp, or var) as intended by the feature extraction call
- If lazy=True, intermediate dask arrays remain unevaluated until .compute() is called; materialization produces expected feature ranges and no NaN/Inf values
- Visual overlay of extracted features on the original tissue image shows expected spatial localization (e.g., high texture features align with tissue boundaries or cell clusters)

## Limitations

- ImageContainer assumes pixel-to-spatial coordinate mapping is linear; non-linear image distortion or multi-section slides may require custom preprocessing
- Feature extraction performance depends on image resolution and dask task graph complexity; very large or multi-gigapixel images may exhaust available memory even with lazy evaluation
- The article emphasizes streamlined APIs but does not detail handling of missing coordinate values, misaligned observations, or partial image overlap

## Evidence

- [other] Instantiate squidpy.im.ImageContainer with the image data and AnnData object.: "Instantiate squidpy.im.ImageContainer with the image data and AnnData object."
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.: "providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [other] Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image.: "Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image."
- [other] Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var).: "Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var)."
- [readme] It builds on scanpy and anndata: "It builds on scanpy and anndata"
