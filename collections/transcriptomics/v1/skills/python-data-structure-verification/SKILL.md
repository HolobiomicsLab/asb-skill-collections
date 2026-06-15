---
name: python-data-structure-verification
description: Use when after executing a spatial analysis function (e.g., squidpy.gr.sepal) that modifies or augments a data object, verify that the expected output fields exist with correct names, data types, and array dimensions before proceeding to interpretation or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3277
  tools:
  - scanpy
  - Python
  - anndata
  - Squidpy
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- It builds on scanpy and anndata
- Spatial Single Cell Analysis in Python
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

# Python Data Structure Verification

## Summary

Validate that computed spatial analysis results conform to expected field names, data types, and dimensions when stored in standard Python data structures (AnnData objects, dictionaries, arrays). This skill ensures output integrity after applying spatial statistics functions and supports downstream analysis reproducibility.

## When to use

After executing a spatial analysis function (e.g., squidpy.gr.sepal) that modifies or augments a data object, verify that the expected output fields exist with correct names, data types, and array dimensions before proceeding to interpretation or visualization. Use this skill when integrating third-party spatial tools into a workflow and you need confidence that results conform to a documented schema.

## When NOT to use

- Input is already a pre-validated result from a trusted, well-tested workflow (e.g., published benchmark dataset); redundant verification adds runtime cost.
- Output is a simple scalar or single-column table for which field-name and dimension checks are unnecessary.
- Tool documentation does not specify expected output schema; use exploratory inspection instead of strict validation.

## Inputs

- AnnData object with .var, .uns, .obsm, or .varm attributes populated by spatial analysis function
- Dictionary or list of expected field names and their expected data types
- Optional: reference schema or API documentation specifying output format

## Outputs

- Boolean or exception result indicating pass/fail of schema validation
- Summary report (DataFrame or dict) documenting field names, data types, array dimensions, and presence confirmation
- Optionally: corrected or validated AnnData object with metadata annotations confirming verification

## How to apply

Inspect the modified AnnData object's .var, .uns, .obsm, or .varm attributes (depending on where the tool stores results) by iterating over dictionary keys or examining array shapes. Cross-reference the field names and data types against the tool's API documentation (e.g., 'sepal returns a ranking column in .var'). Check that ranking columns are numeric and score matrices have dimensions (n_obs, n_features) or (n_features, n_features) as appropriate. For AnnData objects, verify dtype consistency (e.g., float64 for scores, int64 for indices) and absence of NaN values in critical columns. Generate a summary table documenting field names, observed dtypes, observed dimensions, and a boolean confirmation that all required fields are present. Use assertions or exceptions to fail loudly if mandatory fields are missing or malformed.

## Related tools

- **scanpy** (Provides standard AnnData-based workflows and attribute conventions (.var, .obs, .obsm) that structure spatial analysis outputs)
- **anndata** (Defines the core data structure (AnnData) in which spatial results are stored and must be validated; supports attribute introspection via .var, .uns, .obsm)
- **Squidpy** (Spatial analysis tool whose outputs (e.g., from squidpy.gr.sepal) are validated against expected field names and dimensions) — https://github.com/scverse/squidpy
- **Python** (Programming language used to write inspection and assertion code for verifying field names, dtypes, and array shapes)

## Examples

```
import anndata as ad; import squidpy as sq; adata = sq.datasets.slideseqv2(); sq.gr.sepal(adata); assert 'sepal_scores' in adata.var.columns, 'Missing sepal_scores'; assert adata.obsm['sepal_ranking'].shape == (adata.n_obs, adata.n_vars), 'Shape mismatch'; print('Validation passed: sepal output conforms to expected schema.')
```

## Evaluation signals

- All required field names (e.g., 'sepal_scores', 'sepal_ranking') are present in the target attribute (.var, .uns, or .obsm) of the AnnData object.
- Data types of all output columns match expectations (e.g., float64 for spatial statistics scores, int64 for gene indices).
- Array dimensions match the input data shape: ranking/score matrices have shape (n_obs, n_features) or (n_features, n_features) or other documented format; no unexpected singleton or transposed dimensions.
- No NaN or infinite values in critical numeric columns, unless explicitly documented as valid (e.g., for missing data).
- Assertion or exception raised with descriptive message if any required field is absent or malformed, enabling fail-fast debugging.

## Limitations

- Verification assumes the tool's API documentation is accurate and up-to-date; schema mismatches due to documentation lag may cause false positives or negatives.
- Does not validate semantic correctness of values (e.g., whether spatial statistics were computed using the correct neighborhood graph or parameters); only checks structure and type.
- Performance cost increases with AnnData object size when iterating over large .var or .obsm attributes; consider sampling for very large datasets.
- Squidpy and related tools may update output schemas between versions; verification code must be maintained alongside dependency versions.

## Evidence

- [other] Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores): "Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores)."
- [other] Validate that field names and data structures match the expected schema (e.g., presence of ranking columns, score matrices with correct dimensions): "Validate that field names and data structures match the expected schema (e.g., presence of ranking columns, score matrices with correct dimensions)."
- [intro] It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics: "It builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics"
- [intro] Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data: "Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data."
