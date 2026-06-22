---
name: gene-identifier-format-standardization
description: Use when when you have differential expression results from genes, miRNAs, proteins, or lipids with heterogeneous identifier formats (raw gene names, Ensembl accessions, RefSeq IDs, or gene symbols) and need to perform pathway enrichment analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0230
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0085
  tools:
  - clusterProfiler
  - biotranslator
  - ggplot2
  - ComplexHeatmap
  - 'R packages: edgeR, limma, sva'
  - DESeq2
  - 'R packages: ggplot2, ComplexHeatmap'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gene-identifier-format-standardization

## Summary

Standardize gene identifiers to a consistent format (e.g., Entrez IDs, gene symbols, Ensembl IDs) before routing differentially expressed features to pathway enrichment tools. This ensures downstream tools (clusterProfiler, biotranslator) can correctly map genes to pathway databases without identifier mismatches.

## When to use

When you have differential expression results from genes, miRNAs, proteins, or lipids with heterogeneous identifier formats (raw gene names, Ensembl accessions, RefSeq IDs, or gene symbols) and need to perform pathway enrichment analysis. Standardization is required before clusterProfiler or biotranslator can reliably annotate features to biological pathways, especially when integrating multi-omics data from different sequencing/proteomics platforms.

## When NOT to use

- Input identifiers are already consistently formatted and verified against the target pathway database schema.
- Downstream tool (clusterProfiler or biotranslator) natively accepts the raw identifier format without conversion.
- Multi-species or cross-species analysis where organism-specific identifier schemes conflict; re-mapping must be organism-aware.

## Inputs

- Differential expression analysis output (DEA table with gene identifiers, p-values, log fold-change)
- Gene identifier mapping reference (e.g., Ensembl-to-Entrez lookup table)
- Configuration parameter specifying target identifier format and p-value cutoff thresholds

## Outputs

- Standardized gene identifier list filtered by p-value threshold
- Mapping audit log (original → standardized identifiers, unmapped count)
- Formatted input table ready for clusterProfiler or biotranslator ingestion

## How to apply

After differential expression analysis (e.g., DESeq2, edgeR, RankProd), read the DEA output table containing p-values and log fold-change values. Inspect the gene identifier column to detect its current format (e.g., Ensembl, RefSeq, gene symbol). Apply format conversion using R packages or mapping tables to standardize all identifiers to the target format (typically Entrez gene IDs or gene symbols, depending on tool requirements). Apply the configured p-value cutoff (genes_genespval, mirna_genespval, proteins_genespval, lipids_genespval) to filter significant features before standardization. Validate that no identifiers are lost or duplicated during conversion; check for one-to-one mapping integrity. Pass the standardized, filtered feature list to the selected pathway enrichment tool (clusterProfiler or biotranslator) via the pea_genes parameter.

## Related tools

- **R packages: edgeR, limma, sva** (Pre-processing and normalization of DEA input before identifier standardization)
- **clusterProfiler** (Receives standardized gene identifiers for pathway enrichment analysis)
- **biotranslator** (Receives standardized gene identifiers for pathway enrichment analysis)
- **DESeq2** (Upstream differential expression caller producing feature lists with identifiers)
- **R packages: ggplot2, ComplexHeatmap** (Visualization of identifier mapping audit and standardized feature distributions)

## Evaluation signals

- Verify all gene identifiers in the standardized output match the expected format (e.g., all 5–10 digit Entrez IDs, or all HGNC gene symbols).
- Check for 100% mapping success rate (or document justified unmapped identifiers with reason codes).
- Confirm one-to-one mapping: no duplicate identifiers after standardization, no data rows lost after p-value filtering.
- Run downstream tool (clusterProfiler or biotranslator) and confirm no identifier lookup errors or warnings in pathway database cross-reference step.
- Compare feature count before and after standardization; document any intentional loss due to p-value threshold application vs. mapping failure.

## Limitations

- Identifier mapping is organism-specific; cross-species analyses require separate mapping tables per organism.
- Some genes may have multiple identifiers in source data (isoforms, alternative names) leading to one-to-many or many-to-one mappings; resolution strategy must be pre-specified (e.g., collapse by gene symbol, keep longest isoform).
- Older or lesser-used organisms may lack complete mapping resources; unmapped identifiers must be handled gracefully (filtered, reported, or flagged for manual review).
- Different pathway databases (KEGG, GO, Reactome) may expect different identifier formats; tool selection (clusterProfiler vs. biotranslator) constrains valid formats.

## Evidence

- [other] The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids.: "pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins,"
- [other] If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results.: "If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results."
- [methods] Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
- [other] Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml to determine tool selection.: "Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml to determine tool selection."
