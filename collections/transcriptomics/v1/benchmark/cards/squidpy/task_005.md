# SciTask Card: Analyze lazy dask-backed image processing via im.calculate_image_features on the ImageContainer

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:58:24.733366+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_squidpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`
- DOI: `10.1038/s41592-021-01358-2`
- GitHub: `scverse/squidpy`
- Input from: `task_001`

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `multi-omics-integration`, `spatial-metabolomics`
- Techniques: `clustering`, `dimensionality-reduction`, `machine-learning`, `statistical-analysis`

## Research Question
Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate computations as dask arrays?

## Connected Finding
Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.

## Task Description
Load a spatially resolved dataset with an associated tissue image into squidpy.im.ImageContainer, compute image features using im.calculate_image_features with dask lazy computation enabled, and verify that feature outputs are materialized into the AnnData object while intermediate computations remain as dask arrays before collection.

## Inputs
- AnnData object with spatial coordinates
- Tissue image file (TIFF, Zarr, or equivalent)

## Expected Outputs
- AnnData object with computed image features stored in obsm or var slots
- Verification log or report showing dask array status before and after materialization

## Expected Output File

- `annotated_adata_with_image_features.h5ad`

## Landmark Outputs

- `image_container.pkl`
- `feature_names.txt`
- `dask_array_metadata.json`
- `materialized_features.h5ad`

## Tools
- Squidpy
- scanpy
- anndata
- Python

## Skills
- image-feature-extraction-from-tissue-sections
- lazy-computation-orchestration-with-dask
- spatial-coordinate-integration-with-imaging-data
- anndata-object-manipulation-and-storage
- dask-array-materialization-and-collection

## Workflow Description
1. Create or load a spatial dataset (AnnData object) with coordinate information and an associated tissue image file. 2. Instantiate squidpy.im.ImageContainer with the image data and AnnData object. 3. Call im.calculate_image_features with dask lazy computation enabled to extract spatial features from the image. 4. Verify intermediate computation results remain as dask arrays before materialization. 5. Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are stored in the appropriate slots (obsm, obsp, or var).

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ContainerShow_axis.png` | figure | False |
| `figures/ContainerShow_channel.png` | figure | False |
| `figures/ContainerShow_channelwise.png` | figure | False |
| `figures/ContainerShow_channelwise_segmentation.png` | figure | False |
| `figures/ContainerShow_imshow_kwargs.png` | figure | False |
| `figures/ContainerShow_library_id.png` | figure | False |
| `figures/ContainerShow_scale_mask_circle_crop.png` | figure | False |
| `figures/ContainerShow_segmentation.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_False_False.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_False_True.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_True_False.png` | figure | False |
| `figures/ContainerShow_transpose_channelwise_True_True.png` | figure | False |
| `figures/DetectTissue_detect_tissue_felzenszwalb.png` | figure | False |
| `figures/DetectTissue_detect_tissue_otsu.png` | figure | False |
| `figures/figure1.png` | figure | False |
| `figures/squidpy_horizontal.png` | figure | False |
| `figures/squidpy_vertical.png` | figure | False |
| `figures/test_img.jpg` | figure | False |
| `figures/tissue_hires_image.png` | figure | False |
| `figures/tissue_lowres_image.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- squidpy.im.ImageContainer wraps tissue images and links them to spatial omics data via AnnData, enabling feature extraction on pixel-level image data.
- Dask lazy computation in im.calculate_image_features defers actual computation until explicit collection, reducing memory footprint for large images while maintaining reproducibility.
- Image features computed by squidpy are typically stored in AnnData.obsm (cell-level features) or AnnData.var (gene-level features), depending on the feature granularity and aggregation method.
- Intermediate dask arrays must remain unevaluated until explicitly collected; premature materialization breaks lazy evaluation and defeats the memory efficiency of dask-based pipelines.
- ImageContainer supports multiple image storage backends (TIFF, Zarr, remote Zarr stores) and can handle multi-scale and Z-dimension data, making backend verification essential before feature extraction.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Verification log or report showing dask array status before and after materialization.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does squidpy's im.calculate_image_features function support lazy computation via dask, and does it correctly materialize computed features into the AnnData object while preserving intermediate computations as dask arrays?: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.: 'providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AnnData object with spatial coordinates: 'a spatially resolved dataset with an associated tissue image'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Tissue image file (TIFF, Zarr, or equivalent): 'associated tissue image'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] AnnData object with computed image features stored in obsm or var slots: 'feature outputs are correctly materialized into the AnnData object'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Verification log or report showing dask array status before and after materialization: 'intermediate computations remain dask arrays before collection'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Squidpy: 'Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] scanpy: 'It builds on scanpy and anndata'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] anndata: 'It builds on scanpy and anndata'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Spatial Single Cell Analysis in Python'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists: squidpy/im/_container.py (ImageContainer implementation)
- verify file exists: squidpy/im/_features.py (calculate_image_features implementation)
- script_runs: load a test spatially resolved dataset with tissue image using squidpy.im.ImageContainer without errors
- script_runs: execute im.calculate_image_features with dask lazy computation enabled (e.g., passing compute=False or equivalent parameter) without errors
- verify output_matches_reference: intermediate computation objects before collection are dask arrays (type check: dask.array.Array or dask.dataframe.DataFrame), robust to different dask versions
- verify output_matches_reference: final feature outputs after materialization are correctly integrated into AnnData.obs or AnnData.obsm as numpy arrays or DataFrames
- script_runs: verify AnnData object structure is valid after feature materialization (obsm/obs dimensions match n_obs)
- file_format_is: output AnnData object is HDF5-based (.h5ad) or zarr-backed, with no dask arrays remaining in final artifact

### Expert Review
- confirm that dask lazy evaluation semantics are correctly preserved during im.calculate_image_features pipeline (no premature materialization)
- confirm that feature values computed via dask lazy execution match those computed with eager evaluation (numerical accuracy and consistency)
- confirm that memory efficiency gains from lazy computation are realizable on a moderately sized tissue image dataset

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load spatial coordinates and image file into squidpy.im.ImageContainer and link to AnnData object.
2. Enable dask lazy computation mode in im.calculate_image_features to defer actual pixel-level calculations.
3. Extract image features across specified scales or layers, storing intermediate results as dask arrays in memory.
4. Explicitly collect and materialize dask arrays into AnnData.obsm or AnnData.var slots.
5. Validation: Confirm all requested features are present in the output AnnData object, intermediate computation arrays remained as dask objects before collection, and no data loss occurred during materialization.
6. References: source article (DOI: 10.1038/s41592-021-01358-2)

## Workflow Ports

**Inputs:**

- `spatial_adata` — AnnData object with spatial coordinates ← `task_001/adata_with_graph`
- `tissue_image` — Tissue image file

**Outputs:**

- `annotated_adata` — AnnData object with image features materialized
- `dask_verification_report` — Verification report of dask array handling

**Used:** `urn:asb:port:task_001/adata_with_graph`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__squidpy`
- **Synthesized at:** 2026-06-15T18:06:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
