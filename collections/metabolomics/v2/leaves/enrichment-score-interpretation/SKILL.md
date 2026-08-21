---
name: enrichment-score-interpretation
description: Use when after differential expression analysis has produced gene lists
  with p-values and log fold-change values, and after pathway enrichment tools (clusterProfiler
  or biotranslator) have computed enrichment scores and adjusted p-values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3391
  tools:
  - clusterProfiler
  - biotranslator
  - ggplot2
  - ComplexHeatmap
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Pathway enrichment analysis | Clusterprofiler, Biotranslator
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger,
  limma, sva, ggplot2, ComplexHeatmap'
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

# enrichment-score-interpretation

## Summary

Interpret and organize pathway enrichment statistics (enrichment scores and adjusted p-values) computed by clusterProfiler or biotranslator to identify significantly enriched biological pathways and functional modules in multi-omics datasets. This skill bridges differential expression filtering and downstream annotation by translating raw enrichment metrics into hierarchically organized, annotated results suitable for biological interpretation.

## When to use

Apply this skill after differential expression analysis has produced gene lists with p-values and log fold-change values, and after pathway enrichment tools (clusterProfiler or biotranslator) have computed enrichment scores and adjusted p-values. Use it when you need to systematically filter, organize, and visualize enrichment results to identify which biological pathways or functional categories are significantly perturbed across genes, miRNA, proteins, or lipids in your multi-omics study.

## When NOT to use

- Input enrichment data has not yet been computed by clusterProfiler or biotranslator — first run the pathway enrichment tool.
- Differential expression analysis has not been completed or p-value filtering has not been applied to feature lists.
- Enrichment results are already integrated into a downstream multi-omics summary and no additional annotation or reorganization is required.

## Inputs

- Differential expression analysis output (gene/miRNA/protein/lipid list with p-values and log fold-change values)
- Enrichment score tables from clusterProfiler or biotranslator
- Adjusted p-value tables from pathway enrichment tools
- Intermediate R objects from enrichment computation

## Outputs

- Hierarchically organized enrichment results directory (stratified by data type and tool)
- Filtered and annotated enrichment tables (pathways passing adjusted p-value threshold)
- Annotated enrichment plots (e.g., bar plots, dot plots, network visualizations)
- Summary statistics files with enrichment scores and adjusted p-values
- R objects for downstream multi-omics integration

## How to apply

After running clusterProfiler or biotranslator on filtered DEA output (using p-value cutoffs such as genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5), extract the enrichment scores and adjusted p-values from each tool's output. Apply a statistical significance threshold (typically adjusted p < 0.05) to the enrichment results to identify credible pathway hits. Organize all enrichment tables, plots, and intermediate R objects hierarchically into the output directory structure, stratified by data type (genes, miRNA, proteins, lipids) and tool choice (clusterProfiler or biotranslator). Annotate plots and summary statistics with enrichment scores, adjusted p-values, and supporting metrics so that downstream users can rapidly identify the most enriched and biologically relevant pathways. This hierarchical organization and annotation ensure reproducibility and facilitate integration with multi-omics results.

## Related tools

- **clusterProfiler** (Computes and outputs enrichment scores and adjusted p-values for gene/protein/metabolite pathway enrichment analysis)
- **biotranslator** (Alternative pathway enrichment tool; computes enrichment statistics and adjusted p-values for multi-omics features)
- **ggplot2** (Generates annotated enrichment visualizations (bar plots, dot plots, scatter plots) for pathway results)
- **ComplexHeatmap** (Produces hierarchical and annotated heatmap visualizations of enrichment patterns across multiple data types)

## Evaluation signals

- Enrichment results directory exists and is hierarchically organized by data type (genes, miRNA, proteins, lipids) and tool selection (clusterProfiler or biotranslator).
- All enrichment tables contain enrichment scores, adjusted p-values, and pathway/feature identifiers; tables are filtered to include only results with adjusted p < 0.05 (or user-specified threshold).
- Annotated plots (bar plots, dot plots, network diagrams) are present for each data type and enrichment tool combination; plots display enrichment scores and adjusted p-values on axes or in legends.
- Summary statistics files report counts of significant pathways, ranges of enrichment scores and adjusted p-values, and data-type-specific metrics.
- R objects from enrichment computation are preserved in intermediate results directory for downstream multi-omics integration workflows.

## Limitations

- Enrichment interpretation depends critically on the choice of statistical significance threshold (adjusted p-value cutoff); the article specifies configurable cutoffs per data type but does not provide guidance on how to select them for novel datasets.
- Output organization and annotation are dependent on user configuration via params.yml (pea_genes parameter and per-data-type p-value cutoffs); misconfigured parameters may produce incomplete or incorrectly organized results.
- Enrichment scores and adjusted p-values are tool-specific; direct comparison of clusterProfiler and biotranslator results may not be appropriate without normalization or calibration.
- The skill assumes that DEA filtering has been correctly applied upstream; if feature list filtering is incomplete or incorrect, enrichment interpretation will be biased.

## Evidence

- [other] Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values.: "Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values."
- [other] Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or /genes/clusterprofiler/) with annotated plots and summary statistics.: "Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or"
- [other] The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids: "The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for"
- [methods] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [methods] Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
