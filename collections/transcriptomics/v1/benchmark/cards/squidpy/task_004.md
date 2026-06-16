# SciTask Card: Reproduce the SEPAL spatial variable gene detection using gr.sepal on an example dataset

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:58:24.733366+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_squidpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `visualization`
- DOI: `10.1038/s41592-021-01358-2`
- GitHub: `scverse/squidpy`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `multi-omics-integration`, `spatial-metabolomics`
- Techniques: `clustering`, `dimensionality-reduction`, `machine-learning`, `statistical-analysis`

## Research Question
Does squidpy.gr.sepal successfully compute spatial statistics and attach gene ranking scores to an AnnData object with the expected field names when applied to spatial transcriptomics datasets?

## Connected Finding
Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images, indicating that tools like sepal are designed to integrate spatial analysis results into standard AnnData workflows.

## Task Description
Run squidpy.gr.sepal on a bundled spatial dataset (slideseqv2 or merfish) to compute spatial enrichment and gene rankings, then verify that the resulting scores and gene rankings are correctly attached to the AnnData object under the expected field names.

## Inputs
- Bundled spatial omics dataset (slideseqv2 or merfish format)
- Python environment with Squidpy installed

## Expected Outputs
- AnnData object with sepal results (gene rankings and spatial enrichment scores) stored in .var, .uns, or .obsm
- Verification report listing field names, data types, array shapes, and confirmation of successful computation

## Expected Output File

- `sepal_results_verification.txt`

## Landmark Outputs

- `adata_loaded.h5ad`
- `sepal_fields_manifest.json`
- `sepal_results_verification.txt`

## Tools
- Squidpy
- scanpy
- anndata
- Python

## Skills
- spatial-gene-ranking-computation
- anndata-object-manipulation-and-inspection
- spatial-enrichment-score-validation
- python-data-structure-verification
- spatial-omics-dataset-loading

## Workflow Description
1. Load a bundled spatial dataset using squidpy.datasets (slideseqv2 or merfish) into an AnnData object. 2. Execute squidpy.gr.sepal with default or specified parameters to compute spatial enrichment patterns and gene scores. 3. Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores). 4. Validate that field names and data structures match the expected schema (e.g., presence of ranking columns, score matrices with correct dimensions). 5. Generate a summary report documenting field names, data types, dimensions, and confirmation of successful computation.

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
- SEPAL (Spatial Enrichment Pattern Analysis with Learning) computes gene rankings based on spatial patterns; the algorithm assigns scores reflecting how genes are spatially enriched relative to tissue structure.
- Squidpy stores results in AnnData slots: gene-level scores typically go to .var, neighborhood patterns to .uns, and per-observation spatial metrics to .obsm; field naming follows squidpy conventions (e.g., 'sepal_score', 'sepal_pval').
- Spatial datasets like Slide-seq v2 and MERFISH have different coordinate systems and resolution; SEPAL results will preserve the observation count (n_obs) but may generate different field dimensionalities based on neighborhood definition.
- Verification must confirm that output shapes are (n_obs, n_vars) or (n_vars,) for gene-level metrics and that no NaN or inf values corrupt the scores unless explicitly masked by the algorithm.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Verification report listing field names, data types, array shapes, and confirmation of successful computation.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does squidpy.gr.sepal successfully compute spatial statistics and attach gene ranking scores to an AnnData object with the expected field names when applied to spatial transcriptomics datasets?: 'providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images, indicating that tools like sepal are designed to integrate spatial analysis results into standard AnnData workflows.: 'providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Bundled spatial omics dataset (slideseqv2 or merfish format): 'datasets.slideseqv2
    datasets.merfish'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Python environment with Squidpy installed: 'pip install squidpy'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] AnnData object with sepal results (gene rankings and spatial enrichment scores) stored in .var, .uns, or .obsm: 'gr.sepal'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Verification report listing field names, data types, array shapes, and confirmation of successful computation: 'gr.sepal'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Squidpy: 'gr.sepal'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] scanpy: 'It builds on scanpy and anndata'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] anndata: 'It builds on scanpy and anndata'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Spatial Single Cell Analysis in Python'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists: squidpy package contains squidpy.gr.sepal function
- verify squidpy can be imported and sepal function is callable
- script_runs: load bundled dataset (dataset_slideseqv2 or dataset_merfish) from squidpy.datasets, call squidpy.gr.sepal on the AnnData object, and confirm execution completes without error
- field_present: verify the AnnData object .var or .obs contains gene ranking or score field(s) after sepal execution (exact field names require expert review)
- file_format_is: output is an AnnData-compatible object (.h5ad or in-memory AnnData instance) with sepal results attached

### Expert Review
- confirm the field names and data structure of gene rankings or scores match squidpy.gr.sepal documented output schema
- validate that score values are in expected range and represent meaningful gene importance rankings for the spatial dataset

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load a bundled spatial dataset (slideseqv2 or merfish) via squidpy.datasets into an AnnData container.
2. Execute squidpy.gr.sepal on the loaded AnnData object to compute gene-level spatial enrichment scores and rankings.
3. Extract and inspect output fields from AnnData .var, .uns, and .obsm slots to identify sepal-specific columns and matrices.
4. Validate field names, data types, array dimensions, and absence of unexpected NaN/inf values against squidpy's expected schema.
5. Validation: Confirm that all sepal output fields are present with correct dimensionality and no missing or corrupted values; generate a structured verification report.
6. References: source article (DOI: 10.1038/s41592-021-01358-2)

## Workflow Ports

**Inputs:**

- `spatial_dataset` — Bundled spatial omics dataset (slideseqv2 or merfish) ← `task_001/adata_with_graph`
- `squidpy_env` — Python environment with Squidpy installed

**Outputs:**

- `adata_with_sepal` — AnnData object with sepal results attached
- `verification_report` — Verification report of field names and data structures

**Used:** `urn:asb:port:task_001/adata_with_graph`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__squidpy`
- **Synthesized at:** 2026-06-15T18:06:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
