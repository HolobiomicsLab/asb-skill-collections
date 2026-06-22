---
name: sample-group-metadata-association
description: Use when you have a preprocessed count matrix (genes, miRNAs, isoforms, proteins, or lipids) and need to prepare it for differential expression analysis by linking sample identifiers to their experimental group assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3465
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - R base (data.frame merge/join operations)
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
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

# sample-group-metadata-association

## Summary

Associate preprocessed omics count matrices with sample phenotype metadata and group assignments to enable algorithm-aware differential expression analysis. This skill ensures that sample grouping information (stored in samplesheet columns like 'condition', 'batch', or 'cl') is correctly linked to count data before dispatching to user-selected DE algorithms.

## When to use

Apply this skill when you have a preprocessed count matrix (genes, miRNAs, isoforms, proteins, or lipids) and need to prepare it for differential expression analysis by linking sample identifiers to their experimental group assignments. Specifically, use this skill before invoking edgeR, DESeq2, or RankProduct, since each algorithm enforces different samplesheet column conventions and group encoding schemes.

## When NOT to use

- Count matrix is not yet preprocessed (still requires normalization, batch correction, or outlier removal)
- Samplesheet columns do not match the requirements of the selected algorithm (e.g., attempting DESeq2 analysis without exact 'condition' and 'batch' column names)
- Sample identifiers in the count matrix cannot be reliably matched to samplesheet rows (missing or inconsistent naming)

## Inputs

- Preprocessed count matrix (genes, miRNAs, isoforms, proteins, or lipids)
- Sample phenotype metadata file (samplesheet with algorithm-specific columns)
- Parameter specification: alg_genes value ('edger', 'deseq2', or 'rankproduct')

## Outputs

- Linked count-to-metadata association (in-memory or intermediate data structure)
- Validated sample-group mapping ready for differential expression dispatch
- Algorithm-specific formula or contrast specification derived from metadata

## How to apply

Load the preprocessed count matrix and the phenotype/sample metadata file (samplesheet) into the R environment. Verify that the samplesheet contains the algorithm-specific columns required by your selected differential expression tool: edgeR requires 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with binary encoding (0 for controls, 1 for treatments). Match sample identifiers (row names or column names in the count matrix) to rows in the samplesheet. Merge or join the metadata into the analysis workflow so that group assignments are available when the selected algorithm is invoked via the alg_genes parameter. Document the mapping and validate that no samples are orphaned or duplicated after association.

## Related tools

- **edgeR** (Differential expression algorithm requiring 'condition' column and optional custom formula/contrasts from associated metadata)
- **DESeq2** (Differential expression algorithm requiring exactly-named 'condition' and 'batch' columns from associated metadata)
- **RankProd** (Differential expression algorithm requiring 'cl' column with binary control/treatment encoding from associated metadata)
- **R base (data.frame merge/join operations)** (Perform sample-metadata association and validation)

## Evaluation signals

- All samples in the count matrix are matched to exactly one row in the samplesheet; no orphaned samples remain
- Algorithm-specific metadata columns ('condition', 'batch', 'cl') are present and correctly populated for the selected alg_genes value
- Sample group encoding is unambiguous (e.g., RankProduct 'cl' column contains only 0 and 1, no missing or invalid values)
- Sample order in the count matrix row/column names is consistent with or properly reindexed to match samplesheet row order before DE analysis invocation
- Formula or contrast specification derived from metadata is syntactically valid and captures the intended experimental design

## Limitations

- Algorithm-specific column naming is strict and enforced; mismatched or misspelled column names will cause downstream DE algorithm failure without clear error messaging
- No automatic inference of group assignments; samplesheet must be manually curated or pre-generated with correct column names before association
- Sample identifiers must be unique within the samplesheet; duplicate sample names or identifiers will cause ambiguity during join operations
- RankProduct's binary encoding ('cl' = 0 or 1) does not support > 2-group comparisons; multi-group designs require reformulation or alternative algorithms

## Evidence

- [methods] edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for controls and 1 for treatments: "each algorithm (edgeR, DESeq2, RankProduct) requiring specific samplesheet column conventions: edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named"
- [methods] Load the preprocessed count matrix and phenotype/sample metadata file. Parse the alg_genes parameter from params.yml to select the differential expression algorithm. Execute the selected algorithm using sample group assignments from the required samplesheet column.: "1. Load the preprocessed count matrix and phenotype/sample metadata file. 2. Parse the alg_genes parameter from params.yml to select the differential expression algorithm. 3. Execute the selected"
- [other] The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'): "The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger')"
- [methods] Differential expression analysis is listed as a workflow step applied to genes, miRNA, isoforms, proteins, and lipids using R packages DESeq2, edgeR, and RankProd: "Genes, miRNA, isoforms, proteins, lipids | Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
