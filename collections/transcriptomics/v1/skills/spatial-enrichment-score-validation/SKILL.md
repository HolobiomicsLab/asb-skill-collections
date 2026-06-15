---
name: spatial-enrichment-score-validation
description: Use when after executing a spatial statistics function (e.g., squidpy.gr.sepal) on a spatial transcriptomics dataset in AnnData format, and before using the computed rankings or enrichment scores in downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - scanpy
  - Squidpy
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

# spatial-enrichment-score-validation

## Summary

Validate that spatial enrichment statistics and gene ranking scores computed by tools like squidpy.gr.sepal are correctly attached to an AnnData object with expected field names, data types, and dimensions. This skill ensures the output schema matches the downstream analysis contract.

## When to use

After executing a spatial statistics function (e.g., squidpy.gr.sepal) on a spatial transcriptomics dataset in AnnData format, and before using the computed rankings or enrichment scores in downstream analysis. Use this skill when you need to confirm that gene scores, ranking columns, and spatial enrichment matrices are present, correctly dimensioned, and accessible via standard AnnData slots (.var, .uns, .obsm).

## When NOT to use

- Input AnnData object has not yet been processed by the spatial statistics function; run the upstream computation first.
- Expected output fields are already known to be present and correct from a prior validation run; skip to downstream analysis.
- The spatial statistics tool has not been executed with the correct dataset format or parameters; debug the computation itself rather than validating malformed output.

## Inputs

- AnnData object with .X (expression matrix), .var (gene metadata), .obs (cell/spot metadata), and .obsm (optional embeddings)
- Spatial transcriptomics dataset (slideseqv2, merfish, or similar format loaded via squidpy.datasets)

## Outputs

- Validation report (dict or DataFrame) listing field names, data types, dimensions, and pass/fail status
- Annotated AnnData object with confirmed .var columns (gene rankings), .uns entries (enrichment parameters), and .obsm matrices (score arrays) tagged as validated

## How to apply

Load the AnnData object produced by the spatial statistics computation (e.g., from squidpy.gr.sepal applied to a slideseqv2 or merfish dataset). Systematically inspect the object's .var attribute for gene ranking columns, .uns for metadata or parameter records, and .obsm for score matrices or spatial enrichment results. Verify that field names match the tool's documented output schema, that data types are appropriate (numeric arrays for scores, categorical for rankings), and that matrix dimensions align with the number of observations (cells/spots) and features (genes). Generate a summary report listing all detected output fields, their data types, shape, and a binary pass/fail confirmation. Compare against the tool's API documentation to ensure no expected fields are missing.

## Related tools

- **Squidpy** (Computes spatial enrichment statistics and gene ranking scores via squidpy.gr.sepal; outputs are validated) — https://github.com/scverse/squidpy
- **scanpy** (Provides AnnData object infrastructure and gene/cell metadata manipulation utilities used during validation)
- **anndata** (Defines the .var, .uns, .obsm slots that are inspected and validated for schema compliance)

## Examples

```
import squidpy as sq; import scanpy as sc; adata = sq.datasets.slideseqv2(); sq.gr.sepal(adata); print(adata.var.columns); print(adata.obsm.keys()); print(adata.uns.keys())
```

## Evaluation signals

- All expected gene ranking columns are present in .var and contain numeric or categorical values with no missing data for the full gene set
- All spatial enrichment score matrices in .obsm have shape (n_obs, n_features) or (n_obs, n_embeddings) matching the AnnData object's dimensions
- Metadata and parameters stored in .uns are retrievable and match the input arguments to the spatial statistics function (e.g., parameter names, gene subsets used)
- Data types are appropriate: numeric arrays (float64, float32, or int) for scores; categorical or int for rankings; string for field names
- No duplicate field names exist across .var columns, .uns keys, and .obsm matrices; each output slot is unique and accessible

## Limitations

- Validation assumes the spatial statistics tool has already been executed; the skill does not diagnose upstream computation failures or parameter mismatches.
- The skill does not assess the statistical significance or biological plausibility of the enrichment scores—only schema and structural correctness.
- If the AnnData object was created with a non-standard layout or custom naming conventions, field name matching may require manual adjustment.
- Validation does not cross-check consistency between gene rankings and enrichment score magnitudes; that is a downstream interpretation task.

## Evidence

- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images, indicating that tools like sepal are designed to integrate spatial analysis results into standard AnnData workflows.: "providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [methods] The task workflow includes inspecting .var, .uns, and .obsm attributes to locate output fields (gene rankings, spatial enrichment scores), and validating that field names and data structures match the expected schema.: "Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores). Validate that field names and data structures match the expected"
- [methods] The skill culminates in generating a summary report documenting field names, data types, dimensions, and confirmation of successful computation.: "Generate a summary report documenting field names, data types, dimensions, and confirmation of successful computation."
- [readme] Squidpy builds on scanpy and anndata, emphasizing the modularity and scalability of the AnnData-based workflow.: "It builds on scanpy and anndata"
