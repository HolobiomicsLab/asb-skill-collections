---
name: multi-omics-output-directory-organization
description: Use when after completing pathway enrichment analysis on differentially expressed features from genes, miRNA, proteins, or lipids using either clusterProfiler or biotranslator.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3572
  tools:
  - clusterProfiler
  - biotranslator
  - ggplot2
  - ComplexHeatmap
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Pathway enrichment analysis | Clusterprofiler, Biotranslator
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap'
- 'R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-omics-output-directory-organization

## Summary

Organize enrichment analysis results hierarchically by data type (genes, miRNA, proteins, lipids) and tool choice (clusterProfiler or biotranslator), storing annotated plots, summary statistics, and intermediate R objects in a structured output directory. This skill ensures reproducible, navigable results across multi-omics pathway enrichment workflows.

## When to use

After completing pathway enrichment analysis on differentially expressed features from genes, miRNA, proteins, or lipids using either clusterProfiler or biotranslator. Apply this skill when you have enrichment statistics (enrichment scores, adjusted p-values) and want to deposit results in a standardized, multi-level directory structure that separates by omics data type and tool selection.

## When NOT to use

- Input is already organized in a tool-specific or institution-specific directory structure that must be preserved for downstream processing.
- Enrichment analysis has not been completed yet; pathway enrichment tool selection and execution must occur first.
- User requires a flat directory structure without multi-level nesting by data type and tool.

## Inputs

- Differential expression analysis output (DEA gene lists with p-values and log fold-change values)
- Enrichment analysis results from clusterProfiler or biotranslator (enrichment scores, adjusted p-values, pathway annotations)
- Generated visualization objects (ggplot2 and ComplexHeatmap plots)
- Intermediate R objects from enrichment computation
- User-defined output directory path

## Outputs

- Hierarchical output directory structure organized by data type and tool (e.g., /user_defined_output_directory/genes/clusterProfiler/, /user_defined_output_directory/mirna/biotranslator/)
- Enrichment results tables (with enrichment scores and adjusted p-values)
- Annotated plots (ggplot2 and ComplexHeatmap visualizations)
- Summary statistics files
- Intermediate R objects (serialized enrichment result objects)

## How to apply

After executing the selected enrichment tool (clusterProfiler or biotranslator) on filtered DEA output, create a hierarchical output directory structure rooted at user_defined_output_directory and nested first by data type (e.g., /genes/, /mirna/, /proteins/, /lipids/) and then by tool name (e.g., /clusterProfiler/ or /biotranslator/). Deposit enrichment results tables (containing enrichment scores and adjusted p-values), generated plots (via ggplot2 and ComplexHeatmap), and intermediate R objects (e.g., enrichment result objects) into the corresponding nested directories. This organization enables rapid navigation and comparison of results across multiple omics layers and tool choices. Validate that all expected output files exist in the correct subdirectory and that plot images render without corruption.

## Related tools

- **clusterProfiler** (Pathway enrichment analysis tool; generates enrichment scores and adjusted p-values for gene sets)
- **biotranslator** (Alternative pathway enrichment analysis tool; generates enrichment scores and adjusted p-values for gene sets)
- **ggplot2** (Generates annotated plots for visualization of enrichment results)
- **ComplexHeatmap** (Generates complex heatmap visualizations for multi-omics enrichment results)

## Evaluation signals

- All expected subdirectories exist and are populated: /genes/clusterProfiler/ (or biotranslator), /mirna/clusterProfiler/ (or biotranslator), /proteins/clusterProfiler/ (or biotranslator), /lipids/clusterProfiler/ (or biotranslator).
- Each subdirectory contains tables with enrichment scores and adjusted p-values in consistent formats (e.g., tab-delimited or CSV).
- Plot files (.pdf, .png, or .svg) render correctly and display enrichment statistics visualizations.
- Intermediate R objects are present and can be reloaded in subsequent analysis sessions without errors.
- Directory structure matches the schema: /user_defined_output_directory/{data_type}/{tool_name}/ with no missing or misplaced files.

## Limitations

- Directory organization is tool-specific; switching between clusterProfiler and biotranslator creates separate directory branches, which may duplicate storage if both tools are run on the same data.
- No automated schema validation is mentioned in the article; manual inspection required to confirm correct nesting and file placement.
- The article does not specify handling of naming collisions if multiple runs of the same tool are performed on the same data type; users must implement custom naming conventions (e.g., timestamps or run IDs) to avoid overwriting results.

## Evidence

- [methods] If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results.: "If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results."
- [methods] Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or /genes/clusterprofiler/) with annotated plots and summary statistics.: "Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or"
- [methods] Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values.: "Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values."
- [readme] The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process: "The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process"
