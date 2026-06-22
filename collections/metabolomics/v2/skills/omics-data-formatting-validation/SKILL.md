---
name: omics-data-formatting-validation
description: Use when when preparing raw omics data (gene expression matrices, differential abundance tables, or other quantitative omics assays) paired with sample/group metadata for import into a visualization dashboard.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0092
  tools:
  - R Shiny
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# omics-data-formatting-validation

## Summary

Parse and validate CSV expression matrices and group annotation files to ensure structural compatibility before visualization. This skill enforces consistent row/column ordering, data type alignment, and metadata coherence required by downstream omics visualization components.

## When to use

When preparing raw omics data (gene expression matrices, differential abundance tables, or other quantitative omics assays) paired with sample/group metadata for import into a visualization dashboard. Specifically apply this skill if you have two separate CSV files—one containing numeric expression/abundance values and another containing categorical group or sample annotations—and need to confirm they align before rendering heatmaps, volcano plots, or other multi-sample visualizations.

## When NOT to use

- Input files are already in HDF5, NetCDF, or binary serialized format (use format conversion skill first).
- Expression matrix is already pre-clustered or reordered and you need to preserve that order (validation may re-sort rows/columns during clustering).
- Group annotations are continuous or numeric variables requiring regression modeling rather than categorical stratification.

## Inputs

- Expression matrix CSV file (samples × genes or genes × samples numeric table)
- Group annotation CSV file (sample identifiers and group/category labels)

## Outputs

- Validated and aligned expression matrix (ready for clustering and rendering)
- Validated group annotation metadata (ready for overlay as heatmap sidebars or plot stratification)

## How to apply

Load the expression matrix CSV (e.g., heatmap_test.csv with genes as rows and samples as columns) and the group annotation CSV (e.g., group_info.csv with sample identifiers and group labels) using standard R data I/O functions. Validate that all sample identifiers in the expression matrix have corresponding entries in the group annotation file, and vice versa. Check that the expression matrix contains only numeric values in the data cells, and that group labels are non-null and finite in length. Verify row and column counts match expected dimensions and that there are no duplicated sample or gene identifiers. Only after these checks pass should the paired data be handed to the visualization renderer, which will apply clustering and color scaling to the validated matrix.

## Related tools

- **R Shiny** (Web application framework used to render interactive visualizations after validation; receives parsed and validated data structures) — github.com/databio2022/GraphBio

## Examples

```
# In R: read and validate paired CSVs before heatmap rendering
expr <- read.csv('heatmap_test.csv', row.names=1); group <- read.csv('group_info.csv', row.names=1); stopifnot(all(colnames(expr) %in% rownames(group)), all(!is.na(group[colnames(expr),])))
```

## Evaluation signals

- All sample identifiers in the expression matrix are present in the group annotation file with no mismatches or orphaned samples.
- Expression matrix contains only numeric values (no text, NA, or Inf entries in data cells); group labels are non-empty strings.
- Row and column dimensions of the expression matrix match the count of unique genes and samples respectively; no duplicated identifiers.
- Heatmap rendering completes without dimension mismatch errors or missing annotation warnings.
- Clustering and color scaling are applied uniformly to all samples, indicating consistent metadata alignment.

## Limitations

- Validation does not impute missing values (NA or zero); files must be complete before validation.
- Sample order is not preserved during heatmap clustering; if preservation is required, use a pre-clustered or fixed-order variant.
- Large matrices (>>10,000 genes × >>1,000 samples) may experience memory or rendering delays in R Shiny; no explicit size limits are documented.
- Validation assumes CSV format; other delimiters (TSV, space-separated) must be handled by prior format conversion.

## Evidence

- [intro] expression_matrix_loading_and_structure_check: "Load the expression matrix (heatmap_test.csv) and group annotation data (group_info.csv) using R data I/O functions. 2. Parse and validate the expression matrix structure and group labels for"
- [other] graphbio_heatmap_data_requirements: "The heatmap component consumes two CSV files: heatmap_test.csv (expression matrix) and group_info.csv (group annotations) to produce the heatmap visualization."
- [intro] integration_of_group_metadata: "Integrate group annotation metadata as heatmap annotations (e.g., colored sidebars or labels)."
- [readme] demo_data_file_specifications: "heatmap_test.csv and group_info.csv for heatmap."
