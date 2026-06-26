---
name: pathway-enrichment-analysis-tool-selection
description: Use when you have completed differential expression analysis (DEA) on
  genes, miRNA, proteins, or lipids and need to identify significantly enriched biological
  pathways. The multiOmicsIntegrator pipeline requires explicit tool selection via
  the pea_genes parameter in params.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0602
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

# pathway-enrichment-analysis-tool-selection

## Summary

Select and configure the appropriate pathway enrichment analysis tool (clusterProfiler or biotranslator) based on user preference, then apply tool-specific p-value thresholds to filter differentially expressed features before computing enrichment statistics. This skill governs the routing of multi-omics DEA results through feature-type–specific enrichment pipelines.

## When to use

You have completed differential expression analysis (DEA) on genes, miRNA, proteins, or lipids and need to identify significantly enriched biological pathways. The multiOmicsIntegrator pipeline requires explicit tool selection via the pea_genes parameter in params.yml, with separate p-value cutoffs per feature type (genes_genespval, mirna_genespval, proteins_genespval, lipids_genespval). Use this skill when you must route DEA outputs to enrichment analysis while respecting both tool availability and feature-specific significance thresholds.

## When NOT to use

- Input is already a pre-computed pathway enrichment result table—skip tool selection and proceed to interpretation.
- DEA p-values are missing or unreliable; do not apply threshold filtering until p-value quality is verified.
- User has not specified pea_genes parameter in params.yml; clarify tool preference before routing to enrichment analysis.

## Inputs

- DEA results table (gene/miRNA/protein/lipid identifiers with p-values and log fold-change)
- params.yml configuration file specifying pea_genes tool selection
- Feature-type–specific p-value thresholds (genes_genespval, mirna_genespval, proteins_genespval, lipids_genespval)

## Outputs

- Filtered feature list (significant features above p-value threshold)
- Pathway enrichment statistics table (enrichment scores, adjusted p-values, pathway annotations)
- Enrichment plots (e.g., dot plots, bar charts, ggplot2 visualizations)
- Hierarchical output directory structure (/user_defined_output_directory/[feature_type]/[tool_name]/)
- Intermediate R objects and annotation data

## How to apply

First, read the pea_genes parameter from params.yml to determine whether to invoke clusterProfiler or biotranslator. Load the DEA output table containing gene/miRNA/protein/lipid identifiers, log fold-change values, and p-values. Apply the appropriate p-value cutoff threshold (e.g., genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5) to filter features by significance. Reformat feature identifiers to match the selected tool's input requirements (e.g., Entrez IDs, gene symbols). Execute the chosen enrichment tool to compute pathway enrichment statistics including enrichment scores and adjusted p-values. Organize results hierarchically into the output directory (e.g., /user_defined_output_directory/genes/clusterProfiler/ or /genes/biotranslator/) with annotated plots and summary statistics tables.

## Related tools

- **clusterProfiler** (Pathway enrichment analysis tool for genes, miRNA, and other features; computes enrichment statistics and adjusted p-values)
- **biotranslator** (Alternative pathway enrichment analysis tool; functional equivalent to clusterProfiler with different statistical implementations)
- **ggplot2** (Visualization of enrichment results; generates annotated plots (dot plots, bar charts))
- **ComplexHeatmap** (Advanced heatmap visualization for enrichment annotation and multi-feature pathway results)

## Evaluation signals

- Tool selection parameter (pea_genes) is correctly read from params.yml and matches one of the two supported tools.
- Feature filtering achieves expected count reduction: significant features after applying p-value threshold should be ≤ input feature count.
- Enrichment results are organized in the correct directory hierarchy matching the pattern /[feature_type]/[tool_name]/ with all expected outputs (tables, plots, R objects).
- Enrichment statistics contain expected columns: pathway ID, enrichment score, adjusted p-value, feature count per pathway.
- No features with p-value above the configured threshold appear in the final enriched pathway results.

## Limitations

- Tool selection is binary (clusterProfiler or biotranslator only); no option to run both tools or use a hybrid approach within a single execution.
- Feature-type–specific p-value thresholds are hard-coded in the configuration; dynamic threshold adjustment mid-pipeline is not supported.
- Output directory structure assumes a standard hierarchical layout; custom output paths require manual parameter override.
- Identifier format compatibility depends on upstream DEA tool and selected enrichment tool; mismatched formats will cause silent failures or incomplete mappings.

## Evidence

- [other] The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids (genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5).: "pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins,"
- [other] 1. Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml to determine tool selection. 2. If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results. 3. If pea_genes selects biotranslator, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results. 4. Execute the selected tool (clusterProfiler or biotranslator) to compute pathway enrichment statistics including enrichment scores and adjusted p-values.: "Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml to determine tool selection... format gene identifiers and apply the configured"
- [other] Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or /genes/clusterprofiler/) with annotated plots and summary statistics.: "Organize all enrichment results (tables, plots, and intermediate R objects) hierarchically into the output directory structure (e.g., /user_defined_output_directory/genes/biotranslator/ or"
- [methods] Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
