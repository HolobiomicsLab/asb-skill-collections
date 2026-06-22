---
name: enrichment-visualization-and-annotation
description: Use when after pathway enrichment analysis has been executed by clusterProfiler or biotranslator on differentially expressed features filtered by layer-specific p-value cutoffs (genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_3673
  tools:
  - clusterProfiler
  - biotranslator
  - ggplot2
  - ComplexHeatmap
  - R
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

# enrichment-visualization-and-annotation

## Summary

This skill organizes and visualizes pathway enrichment analysis results (enrichment scores, adjusted p-values, annotated plots) hierarchically by omics layer (genes, miRNA, proteins, lipids) and tool choice (clusterProfiler or biotranslator), producing publication-ready summary statistics and intermediate R objects for downstream integration.

## When to use

After pathway enrichment analysis has been executed by clusterProfiler or biotranslator on differentially expressed features filtered by layer-specific p-value cutoffs (genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5). Use this skill when you need to consolidate enrichment results across multiple omics layers into a coherent, hierarchically organized output structure for multi-omics integration or publication.

## When NOT to use

- Enrichment analysis has not yet been executed — use the pathway enrichment routing skill first
- Results are from a single omics layer and multi-layer integration is not planned — simpler flat output structures may suffice
- Raw p-value tables have not been filtered by layer-specific cutoffs — apply filtering before visualization

## Inputs

- enrichment scores table (from clusterProfiler or biotranslator execution)
- adjusted p-values table (from clusterProfiler or biotranslator execution)
- intermediate R objects from enrichment tool
- layer identifier (genes, miRNA, proteins, or lipids)
- tool selection identifier (clusterProfiler or biotranslator)

## Outputs

- hierarchically organized enrichment results directory structure
- annotated enrichment plots (ggplot2/ComplexHeatmap)
- enrichment summary statistics tables
- intermediate R objects for downstream analysis
- layer-specific subdirectories with tool-prefixed naming

## How to apply

Retrieve enrichment analysis outputs (enrichment scores and adjusted p-values tables) from the selected tool (clusterProfiler or biotranslator) and organize them hierarchically into layer-specific directories (e.g., /genes/clusterprofiler/, /mirna/biotranslator/, /proteins/, /lipids/). Generate annotated plots using ggplot2 and ComplexHeatmap to visualize enrichment statistics. Bundle all intermediate R objects, tabular results, and plots together in the output directory structure (user_defined_output_directory/{layer}/{tool_name}/), ensuring consistent naming and metadata across layers. This hierarchical organization enables cross-layer comparison and facilitates the subsequent multi-omics data integration step.

## Related tools

- **ggplot2** (Generate publication-ready annotated plots for enrichment statistics visualization)
- **ComplexHeatmap** (Create complex heatmap visualizations of enrichment results across layers and pathways)
- **clusterProfiler** (Source of enrichment scores and adjusted p-values for organization and visualization)
- **biotranslator** (Alternative source of enrichment scores and adjusted p-values for organization and visualization)
- **R** (Execution environment for organizing outputs and generating visualizations)

## Evaluation signals

- Output directory structure matches expected hierarchy: /user_defined_output_directory/{layer}/{tool_name}/ with all four layers (genes, mirna, proteins, lipids) present
- All enrichment tables contain required columns: enrichment scores and adjusted p-values with no null/missing values in key statistics
- Annotated plots are generated for each layer-tool combination with labeled axes, legends, and statistical annotations visible
- Intermediate R objects are serialized and retrievable (e.g., .RData or .rds format) for downstream multi-omics integration
- File naming and directory structure is consistent across all layers and tool choices (e.g., consistent naming scheme for plots, tables)

## Limitations

- Hierarchical organization requires user to pre-specify output_directory parameter; missing or inaccessible paths will cause failures
- Visualization tools (ggplot2, ComplexHeatmap) may produce large plots for datasets with hundreds of pathways; down-sampling or faceting strategies may be needed for readability
- The skill does not validate upstream enrichment results; garbage input (e.g., invalid p-value distributions, missing identifiers) will produce poorly annotated outputs
- Cross-layer visualization (e.g., joint heatmaps of genes and proteins) requires manual post-processing; this skill organizes layer-specific results only

## Evidence

- [methods] Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or /genes/clusterprofiler/) with annotated plots and summary statistics.: "Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or"
- [methods] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [methods] Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values.: "Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values."
- [methods] The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids: "The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for"
