---
name: expression-level-filtering-with-edger
description: Use when when you have a raw count matrix derived from Salmon or similar quantification tools and need to remove lowly-expressed features before normalization and batch correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - edgeR
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - Nextflow
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva'
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
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
---

# expression-level-filtering-with-edger

## Summary

Apply edgeR-based filterByExp or cutoff-based filtering to retain features in a count matrix that meet minimum expression thresholds, removing low-abundance genes before downstream differential expression analysis. This is a critical preprocessing step for RNA-seq data to reduce noise and improve statistical power.

## When to use

When you have a raw count matrix derived from Salmon or similar quantification tools and need to remove lowly-expressed features before normalization and batch correction. Apply this skill when the count matrix contains many genes with near-zero or sporadic expression across samples, which can inflate false discovery rates in differential expression testing.

## When NOT to use

- Input is already a filtered or normalized feature table from a previous analysis step.
- The experimental design has very few replicates or extremely sparse conditions where aggressive filtering would remove genuine biological signal.
- You are working with rare transcript or isoform data where low-abundance features are of primary interest.

## Inputs

- count matrix (RData or text format, output from Salmon quantification)
- samplesheet/phenotype file (specifying experimental condition and batch columns)
- params_genes.yml configuration file (specifying filterByExp vs. cutoff method and threshold values)

## Outputs

- filtered count matrix (RData format)
- filtered count matrix (text format)
- filtering report or summary statistics

## How to apply

Load the raw count matrix (in RData or text format) alongside the samplesheet specifying experimental conditions. Configure filtering parameters in params_genes.yml to specify either filterByExp (which uses edgeR's built-in logic to identify features meeting minimum expression thresholds across replicates) or explicit cutoff values (e.g., minimum count threshold or minimum number of samples above a CPM cutoff). Apply the chosen filter using edgeR to subset the count matrix, retaining only features that meet the threshold. The rationale is that genes with very low counts across all or most samples contribute mainly noise and lack statistical power for detection, whereas genes meeting the threshold are likely to have sufficient biological signal. Output the filtered matrix in both RData and text formats for subsequent normalization and batch-effect correction steps.

## Related tools

- **edgeR** (Performs filterByExp filtering and provides minimum expression threshold methods for count matrix preprocessing)
- **Nextflow** (Workflow orchestration tool used to run the preprocess_matrix subworkflow across compute infrastructure) — https://www.nextflow.io

## Evaluation signals

- Verify that the output matrix has fewer rows (genes) than the input matrix, confirming that filtering was applied.
- Check that filtered genes meet the specified threshold (e.g., minimum CPM > X in at least Y samples).
- Confirm that the filtered matrix retains the same number of columns (samples) as the input.
- Compare the distribution of expression values before and after filtering; lowly-expressed tail should be removed.
- Inspect the filtering report or log to confirm the number and percentage of features retained vs. removed.

## Limitations

- filterByExp method is condition-aware but may perform unpredictably if conditions have very different library sizes or sequencing depths.
- Choice of threshold is somewhat arbitrary and sensitive; overly aggressive filtering may remove real but lowly-expressed genes of biological interest.
- Filtering is applied uniformly across all features; spike-ins or quality control features may need special handling.
- The skill does not account for differential expression patterns (i.e., a gene expressed only in one condition may be filtered out even if it is biologically important).

## Evidence

- [methods] Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml.: "Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml"
- [other] The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values: "filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction"
- [methods] Load the count matrix (output from Salmon) and phenotype/samplesheet file.: "Load the count matrix (output from Salmon) and phenotype/samplesheet file. 2. Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds"
- [readme] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
