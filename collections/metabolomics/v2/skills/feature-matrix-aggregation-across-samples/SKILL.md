---
name: feature-matrix-aggregation-across-samples
description: Use when after per-sample quantification is complete (e.g., salmon has
  produced quant.sf files for all samples in the cohort) and you need to prepare data
  for differential expression analysis, quality control comparisons, or multi-omics
  integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0091
  tools:
  - SRA toolkit
  - trimgalore
  - Docker
  - Singularity
  - edgeR
  - limma
  - DESeq2
  - Salmon
  - Nextflow
  - nf-core/rnaseq
  license_tier: open
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Genes, miRNA, isoforms | SRA download | SRA toolkit
- Genes, miRNA, isoforms | Quality control | FastQC, trimgalore
- It uses Docker/Singularity containers making installation trivial and results highly
  reproducible.
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

# feature-matrix-aggregation-across-samples

## Summary

Aggregate per-sample quantification results (e.g. transcript-level counts and TPM values from salmon quant.sf files) into a unified feature matrix for downstream statistical analysis. This consolidates single-sample outputs into a sample-by-feature table suitable for differential expression, clustering, or integration workflows.

## When to use

After per-sample quantification is complete (e.g., salmon has produced quant.sf files for all samples in the cohort) and you need to prepare data for differential expression analysis, quality control comparisons, or multi-omics integration. Triggered when you have N independent sample quantifications that must be aligned by feature ID and combined into rows=samples, columns=features.

## When NOT to use

- Input is already a pre-aggregated feature table or expression matrix (e.g., from a prior analysis run).
- Quantification has not yet completed; per-sample outputs are missing or incomplete.
- Samples require batch effect correction before aggregation; perform harmonization (e.g., SVA, ComBat) after aggregation, not before.

## Inputs

- Per-sample salmon quant.sf files (one per sample in $OUTDIR/salmon_genes/$sampleID/quant.sf)
- Sample metadata table (CSV/TSV with sample IDs, conditions, batch, replicates)
- Feature annotation reference (gene ID, transcript ID, or isoform mapping)

## Outputs

- Feature matrix (samples × features, typically in R data.frame, matrix, or SummarizedExperiment format)
- Sample metadata annotations (linked to rows of the feature matrix)
- Quality control report (e.g., sequencing depth per sample, feature coverage histogram)

## How to apply

Collect all per-sample quantification outputs (e.g., $OUTDIR/salmon_genes/$sampleID/quant.sf files) and read them into a unified data structure, matching feature identifiers across samples. Ensure consistent feature annotation (transcript name, gene ID) and unit alignment (raw counts, TPM, or normalized values as required by downstream analysis). Use R packages such as edgeR, limma, or DESeq2 to construct the feature matrix with appropriate sample metadata (e.g., condition, batch, replicate ID). Validate that all samples are represented, no features are missing, and quantitative values fall within expected ranges for the chosen unit (e.g., TPM typically 0–10,000; raw counts non-negative integers). The aggregated matrix becomes the input for differential expression analysis, which may employ DESeq2, edgeR, or RankProd depending on the experimental design.

## Related tools

- **edgeR** (R package for reading, normalizing, and storing aggregated count matrices; differentially expressed gene detection)
- **limma** (R package for quality control, preprocessing, and differential expression modeling on aggregated feature matrices)
- **DESeq2** (R package for differential expression analysis on aggregated count matrices with sample metadata)
- **Salmon** (Produces per-sample quant.sf files that serve as the quantification input to aggregation) — https://github.com/COMBINE-lab/salmon
- **Nextflow** (Workflow orchestration tool that manages per-sample quantification and orchestrates downstream aggregation) — https://www.nextflow.io
- **nf-core/rnaseq** (Reference best-practice RNAseq pipeline that implements the quantification-to-aggregation workflow) — https://github.com/nf-core/rnaseq

## Evaluation signals

- All N samples are represented as rows; feature dimension matches expected transcript/gene count.
- No missing values (NAs) in quantitative columns; if present, document reason (e.g., genes with zero count across all samples).
- Feature IDs are consistent and deduplicated; each row corresponds to one unique feature.
- Quantitative values fall within expected ranges: TPM typically 0–10,000; raw counts are non-negative integers; replicates show correlated expression patterns in preliminary correlation plot.
- Sample metadata columns (condition, batch, replicate ID) are correctly linked and match sample order in the feature matrix.

## Limitations

- Aggregation does not handle missing or incomplete per-sample outputs; all samples must have completed quantification successfully.
- Feature annotation must be consistent across samples; discrepancies in transcript ID naming or versioning will cause alignment errors.
- The aggregated matrix is sensitive to sequencing depth differences; differential expression analysis should include normalization (e.g., TMM, DESeq2's geometric mean) to account for library size variation.
- Batch effects introduced during sample processing are preserved in the aggregated matrix; batch correction (e.g., ComBat, SVA) is a separate, post-aggregation step and should not be conflated with aggregation itself.

## Evidence

- [methods] Aggregate quantification results across all samples into a feature matrix for downstream analysis.: "Aggregate quantification results across all samples into a feature matrix for downstream analysis."
- [methods] Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files containing transcript-level counts and TPM values.: "Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files containing transcript-level counts and TPM values."
- [other] The genes workflow front-end processes raw sequencing data through four sequential stages: (1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC, (3) adapter detection and removal with Trimgalore, and (4) quantification using salmon to produce quant.sf files in the directory structure $OUTDIR/salmon_genes/$sampleID/quant.sf.: "$OUTDIR/salmon_genes/$sampleID/quant.sf"
- [other] Data preprocessing uses R packages including edger, limma, sva, ggplot2, ComplexHeatmap, followed by differential expression analysis using DESeq2, edger, or RankProd.: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [other] Differential expression analysis | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analysis | R packages: DESeq2, edger, RankProd"
