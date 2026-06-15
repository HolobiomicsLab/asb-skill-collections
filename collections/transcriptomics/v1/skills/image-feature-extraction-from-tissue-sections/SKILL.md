---
name: image-feature-extraction-from-tissue-sections
description: Use when you have a spatial transcriptomics dataset (AnnData object) with cell/spot coordinates and an associated tissue microscopy image file, and you need to compute image-derived features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_3452
  tools:
  - scanpy
  - Squidpy
  - AnnData
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

# image-feature-extraction-from-tissue-sections

## Summary

Extract spatial and morphological features from tissue microscopy images aligned to single-cell spatial transcriptomics data using lazy dask computation, then materialize results into an AnnData object. This skill enables scalable feature discovery from high-resolution tissue images without loading entire images into memory.

## When to use

You have a spatial transcriptomics dataset (AnnData object) with cell/spot coordinates and an associated tissue microscopy image file, and you need to compute image-derived features (e.g., texture, morphology, intensity statistics) for downstream integration with gene expression or spatial analysis. Use this skill when the image is large enough that eager computation is infeasible or when you want to preserve intermediate computation graphs for inspection before materializing results.

## When NOT to use

- Input image is already summarized as a feature table or embedding — skip image extraction and directly integrate the pre-computed features.
- Tissue image is unavailable or registration to spatial coordinates is unreliable — feature extraction depends on accurate coordinate mapping.
- Feature extraction parameters (e.g., filter kernels, neighborhood radii) are unknown for your tissue type or image resolution — validate on a small test region first.

## Inputs

- AnnData object with .obs containing spatial coordinates (e.g., 'x', 'y')
- Path to tissue microscopy image file (e.g., TIFF, PNG, or other formats supported by squidpy.im.ImageContainer)
- Optional: pre-instantiated squidpy.im.ImageContainer object

## Outputs

- AnnData object with computed features stored in .obsm (per-observation feature arrays), .obsp (pairwise distances), and/or .var (feature annotations)
- Dask array objects (if lazy=True and .compute() not yet called) representing intermediate feature tensors

## How to apply

Load your spatial dataset as an AnnData object and instantiate a squidpy.im.ImageContainer wrapping both the image file and coordinate metadata. Call im.calculate_image_features with lazy=True to enable dask-backed computation, which defers materialization and preserves intermediate arrays as dask graph objects. Optionally inspect dask arrays before calling .compute() or letting squidpy auto-materialize results into obsm (per-cell feature matrices), obsp (pairwise feature distances), or var (feature metadata) slots. The function automatically handles image coordinate alignment and feature storage placement based on the feature type and image resolution relative to cell/spot density.

## Related tools

- **Squidpy** (Primary API for image feature extraction and spatial analysis; provides im.ImageContainer and im.calculate_image_features for lazy and eager feature computation) — https://github.com/scverse/squidpy
- **AnnData** (Data structure for storing spatial coordinates, gene expression, and image-derived features across observations and feature spaces)
- **scanpy** (Inherited modularity and integration framework for spatial single-cell analysis; used for downstream statistical and clustering workflows on extracted features)
- **dask** (Lazy evaluation engine for deferred image processing and feature computation; allows inspection and inspection of computation graphs before materialization)

## Examples

```
import squidpy as sq; import anndata as ad; adata = ad.read_h5ad('spatial.h5ad'); img_container = sq.im.ImageContainer(image_path='tissue.tiff', adata=adata); sq.im.calculate_image_features(adata, img_container, features='all', lazy=True); adata.obsm
```

## Evaluation signals

- Extracted features appear in the AnnData object slots (.obsm, .obsp, .var) with expected shape matching observation count and feature dimensionality.
- If lazy=True, dask array objects are present before .compute() and contain valid task graph structure; after materialization, arrays convert to numpy without errors.
- Feature values are within expected ranges for the image type and filter parameters (e.g., texture features typically 0–255 for uint8 images, normalized features 0–1).
- Per-observation feature vectors are non-zero and non-NaN across the majority of observations, indicating successful image-to-coordinate alignment.
- Dask task graph size and memory footprint remain manageable (no out-of-memory errors) even for large images, validating lazy computation benefit.

## Limitations

- Feature extraction accuracy depends on accurate spatial coordinate registration between the image and AnnData object; misalignment will produce meaningless features.
- Lazy computation with dask introduces overhead for very small images or simple feature sets; eager computation may be faster in those cases.
- Image file format support is limited to formats readable by squidpy.im.ImageContainer and underlying libraries (typically TIFF, PNG, OME-TIFF); proprietary microscopy formats may require conversion.
- Feature types and parameters (e.g., filter kernels, neighborhood radii) are not automatically optimized for tissue type or image resolution; users must set these manually or rely on sensible defaults.

## Evidence

- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [other] The research question explicitly asks whether squidpy's im.calculate_image_features function supports lazy computation via dask and correctly materializes computed features into the AnnData object while preserving intermediate computations.: "Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate"
- [other] The workflow describes instantiating squidpy.im.ImageContainer with image data and AnnData object, then calling im.calculate_image_features with dask lazy computation enabled.: "Instantiate squidpy.im.ImageContainer with the image data and AnnData object. 3. Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image"
- [other] The workflow specifies verification of intermediate computation results as dask arrays before materialization and confirmation of feature outputs in appropriate AnnData slots.: "Verify intermediate computation results remain as dask arrays before materialization. 5. Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are"
