---
name: dask-array-materialization-and-collection
description: Use when you have performed lazy dask-backed feature extraction on an ImageContainer using im.calculate_image_features and need to persist the computed spatial features into the AnnData object while controlling when and how dask graph computation is triggered.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3518
  - http://edamontology.org/topic_3361
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

# dask-array-materialization-and-collection

## Summary

Materialize and collect lazy dask arrays into concrete AnnData object slots (obsm, obsp, var) after lazy feature extraction via im.calculate_image_features, ensuring intermediate computations remain deferred until explicitly triggered. This skill bridges lazy image feature computation with persistent storage in spatial omics workflows.

## When to use

You have performed lazy dask-backed feature extraction on an ImageContainer using im.calculate_image_features and need to persist the computed spatial features into the AnnData object while controlling when and how dask graph computation is triggered. Use this when you want to avoid premature materialization during intermediate steps but must finalize results for downstream analysis.

## When NOT to use

- Input features are already materialized (non-dask numpy arrays) — materialization is redundant
- Downstream analysis requires lazy evaluation throughout the full pipeline — premature collection defeats deferred computation benefits
- Memory constraints forbid full graph materialization — collect() will force all intermediate results into RAM

## Inputs

- AnnData object with spatial coordinates
- tissue image file or loaded image data
- ImageContainer with dask-backed lazy computation state
- Feature extraction parameters for im.calculate_image_features

## Outputs

- AnnData object with materialized feature arrays in obsm, obsp, or var slots
- concrete numpy/dense arrays (no longer dask arrays)
- computed spatial features indexed by observation or variable

## How to apply

After calling im.calculate_image_features with lazy=True (or dask-backed computation enabled), inspect the AnnData object to confirm intermediate results remain as dask arrays rather than numpy arrays. Trigger materialization by calling .compute() on dask arrays or by using squidpy's collection methods that automatically resolve lazy computations and store results in the appropriate AnnData slots (obsm for per-observation features, obsp for pairwise observations, var for variables). Verify that computed features are stored in the correct slots post-materialization and that the dask task graph was fully executed by checking array type and shape consistency.

## Related tools

- **Squidpy** (provides im.calculate_image_features and ImageContainer APIs for lazy image feature extraction) — https://github.com/scverse/squidpy
- **dask** (enables lazy array computation, task graphs, and deferred evaluation; provides .compute() for materialization)
- **anndata** (defines AnnData object slots (obsm, obsp, var) where materialized features are stored)
- **scanpy** (provides ecosystem utilities for spatial analysis that integrate with squidpy feature storage)

## Examples

```
import squidpy as sq; import dask.array as da; ic = sq.im.ImageContainer(image=img, library_key='spatial'); sq.im.calculate_image_features(adata, ic=ic, features=['texture']); computed = adata.obsm['texture'].compute() if hasattr(adata.obsm['texture'], 'compute') else adata.obsm['texture']
```

## Evaluation signals

- Intermediate results before materialization are of type dask.array.Array or dask.dataframe.DataFrame, not numpy.ndarray
- After collection, feature arrays in AnnData slots (adata.obsm['feature_name']) are concrete numpy arrays with no remaining dask graph references
- Shape and dtype of materialized arrays match expectations from feature extraction parameters
- All dask tasks in the computational graph have been executed (confirmed by absence of pending tasks in the dask scheduler)
- Feature values are reproducible and match deterministic computation from the same input image and parameters

## Limitations

- Materializing very large dask graphs may exhaust available system memory if intermediate arrays are not chunked appropriately
- Calling .compute() synchronously blocks execution until all tasks complete; asynchronous collection is not exposed in the task_005 workflow
- The article does not provide explicit guidance on optimal chunk sizes or dask scheduler selection for image feature extraction
- No changelog found documenting changes to lazy computation behavior across squidpy versions

## Evidence

- [other] Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image.: "Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image."
- [other] Verify intermediate computation results remain as dask arrays before materialization.: "Verify intermediate computation results remain as dask arrays before materialization."
- [other] Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var).: "Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var)."
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images."
- [intro] It builds on scanpy and anndata: "It builds on scanpy and anndata"
