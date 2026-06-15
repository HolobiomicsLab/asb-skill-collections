---
name: lazy-computation-orchestration-with-dask
description: Use when your input is a spatial dataset (AnnData object with coordinate metadata) paired with a large tissue image, and you need to extract spatial features (via squidpy.im.calculate_image_features or similar operations) without loading the entire computation graph into memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3070
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
  tools:
  - scanpy
  - Squidpy
  - dask
  - anndata
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

# lazy-computation-orchestration-with-dask

## Summary

Enable deferred evaluation of large-scale image feature extraction and spatial analysis workflows using dask-backed computation, allowing intermediate results to remain as lazy arrays until explicit materialization into an AnnData object. This skill is essential when working with high-resolution tissue images or large spatial datasets where eager evaluation would exhaust memory.

## When to use

Your input is a spatial dataset (AnnData object with coordinate metadata) paired with a large tissue image, and you need to extract spatial features (via squidpy.im.calculate_image_features or similar operations) without loading the entire computation graph into memory. Use this skill when the image dimensions or feature extraction complexity would exceed available RAM in eager mode, or when you want to inspect intermediate dask task graphs before triggering full materialization.

## When NOT to use

- Input image is already small enough to fit in RAM and eager computation completes in acceptable time — lazy evaluation adds overhead without benefit.
- Feature extraction is a one-off operation that does not need inspection of intermediate results — eager execution is simpler and more straightforward.
- Downstream analysis requires immediate, synchronous access to features (e.g., interactive exploration in a notebook) — dask task graph delays must be resolved anyway, negating lazy benefits.

## Inputs

- AnnData object with spatial coordinates (adata.obsm['spatial'] or equivalent)
- tissue image file (supported formats: .png, .jpg, .tif, .h5ad-embedded image)
- squidpy.im.ImageContainer instance linking image and AnnData
- feature extraction parameters (e.g., layer names, segmentation masks, filter types)

## Outputs

- dask.array objects representing intermediate feature computations (before materialization)
- materialized feature matrices stored in adata.obsm, adata.obsp, or adata.var
- AnnData object with computed spatial features persisted to disk or memory

## How to apply

Create or load a spatial AnnData object with coordinate information and associate it with an ImageContainer wrapping the tissue image file. Call im.calculate_image_features with lazy computation enabled (dask backend), which defers all array operations into a task graph. Verify that intermediate feature arrays remain as dask.array objects by inspecting their type and task graph metadata before calling .compute() or triggering collection. Once verified, materialize the lazy arrays into the AnnData object (storing results in obsm, obsp, or var slots depending on feature type), at which point dask schedules and executes the deferred computation in chunks. The key decision point is whether to materialize all at once (simpler but higher memory) or partition materialization across subsets of observations or spatial regions (more granular control).

## Related tools

- **Squidpy** (provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images via im.calculate_image_features) — https://github.com/scverse/squidpy
- **dask** (backend for lazy array computation and task graph scheduling in image feature extraction workflows)
- **scanpy** (foundation library for spatial single-cell analysis providing AnnData integration and utility functions)
- **anndata** (core data structure storing spatial coordinates, feature matrices, and metadata in obsm, obsp, var slots)

## Examples

```
import squidpy as sq; import anndata as ad; adata = ad.read_h5ad('spatial_data.h5ad'); img = sq.im.ImageContainer('tissue.tif'); sq.im.calculate_image_features(adata, img, layer_names=['nuclei'], features='summary', lazy=True); print(type(adata.obsm['features'])); adata.obsm['features'].compute()
```

## Evaluation signals

- Intermediate feature arrays returned by im.calculate_image_features are confirmed to be dask.array type (not numpy.ndarray) before materialization, verifiable via type() or .name attribute.
- dask task graph is non-empty and contains deferred operations (verify via array.dask or array.__dask_graph__) before .compute() is called.
- After materialization, resulting feature matrices appear in expected AnnData slots (adata.obsm, adata.obsp, or adata.var) with shape matching input observations and feature dimensions.
- Memory footprint during computation remains below peak expected usage (monitor via psutil or system tools); if it exceeds predictions, partition and materialize in batches.
- Feature values are numerically consistent between lazy and materialized forms (spot-check a few coordinates: dask-backed and eagerly computed results should be identical up to floating-point precision).

## Limitations

- Dask scheduling overhead and inter-task dependencies can make very fine-grained lazy operations slower than eager computation for small images; profile before deploying to production workflows.
- Intermediate dask arrays consume disk/memory when persisted or spilled; large task graphs may require explicit memory limits and spillover configuration.
- Debugging failed tasks in a dask graph is more complex than eager exceptions; error messages and tracebacks are less immediately actionable.
- Some Squidpy operations may not support dask backend or may fall back to eager evaluation silently; verify documentation for each im.* function used.

## Evidence

- [other] Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate computations as dask arrays?: "Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate"
- [other] Create or load a spatial dataset (AnnData object) with coordinate information and an associated tissue image file. Instantiate squidpy.im.ImageContainer with the image data and AnnData object. Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image. Verify intermediate computation results remain as dask arrays before materialization. Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var).: "Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image. Verify intermediate computation results remain as dask arrays before materialization."
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images."
- [intro] It builds on scanpy and anndata: "It builds on scanpy and anndata"
