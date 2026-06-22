---
name: batch-effect-correction-combat-sva
description: Use when you have a normalized count matrix (from Salmon or similar quantification tool) with sample metadata that documents batch variables (e.g., sequencing run, processing date, lab site), and you observe or suspect that batch effects—not biological signal—are driving variance across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0634
  tools:
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - Nextflow
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva'
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

# batch-effect-correction-combat-sva

## Summary

Removes known batch effects from count matrices (typically Salmon-derived expression data) using ComBat or SVA algorithms, with batch source specified via sample metadata columns. This step is essential after normalization to ensure that technical or experimental batch factors do not confound downstream differential expression analysis.

## When to use

Apply this skill when you have a normalized count matrix (from Salmon or similar quantification tool) with sample metadata that documents batch variables (e.g., sequencing run, processing date, lab site), and you observe or suspect that batch effects—not biological signal—are driving variance across samples. Use it before differential expression analysis to prevent batch confounding.

## When NOT to use

- Input count matrix has not yet been filtered or normalized—apply filtering and normalization first.
- No batch variables are documented in the sample metadata—batch correction requires explicit specification of batch source.
- Batch effects are confounded with biological treatment; in this case, correction risks removing true signal and requires careful design review.

## Inputs

- Normalized count matrix (RData or text format, typically output from quantile normalization step)
- Sample metadata/samplesheet file with batch and condition columns

## Outputs

- Batch-corrected count matrix (RData format)
- Batch-corrected count matrix (text format)
- Optional: diagnostic plots (PCA, heatmap) showing batch effect removal

## How to apply

After filtering and quantile normalization, specify the batch and condition columns in your sample metadata (samplesheet). Load the normalized count matrix and the metadata into R. Select a batch-correction method (ComBat for known batch factors, or SVA/comsva/svacom for unsupervised/surrogate variable estimation). Pass the condition variable (e.g., treatment group) to preserve biological signal while removing batch-associated variance. Apply the chosen correction method, then output the corrected matrix in both RData and text formats for downstream differential expression tools (DESeq2, edgeR). Evaluate success by visual inspection (PCA/heatmap before and after correction) to confirm batch clustering is eliminated.

## Related tools

- **sva** (R package providing SVA, ComBat, and surrogate variable estimation methods for batch effect removal)
- **limma** (R package used in conjunction with batch correction for normalization and downstream analysis)
- **edgeR** (R package for count matrix filtering and normalization prior to batch correction)
- **Nextflow** (Workflow orchestration framework that runs batch correction as a containerized process in the preprocessing subworkflow) — https://www.nextflow.io

## Evaluation signals

- PCA plot or heatmap shows reduced clustering by batch variable after correction, while biological replicates/treatment groups cluster together.
- Batch-corrected matrix maintains expected count distributions and variance structure (no artificial zero-inflation or extreme negative values).
- Downstream differential expression results show improved consistency and reduced batch-driven false positives when batch-corrected matrix is used versus uncorrected.
- Corrected matrix schema matches input (same rows/genes, same columns/samples) with numeric values in expected range.
- Optional: ComBat/SVA algorithm converges without warnings; surrogate variables (if SVA) explain residual variance orthogonal to batch.

## Limitations

- Requires accurate specification of batch and condition columns in metadata; misspecification can remove biological signal.
- ComBat assumes batch effects are additive; may fail if batch-by-treatment interactions are strong.
- SVA requires sufficient sample size per batch and group; small sample designs may yield unreliable surrogate variables.
- Batch correction is not reversible; always retain the original normalized (pre-correction) matrix for sensitivity analysis.

## Evidence

- [other] The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction using combat, sva, comsva, or svacom approaches, with parameters specifying the condition and batch columns from the samplesheet.: "batch effect correction using combat, sva, comsva, or svacom approaches, with parameters specifying the condition and batch columns from the samplesheet"
- [other] Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml) to remove known batch effects specified in the sample metadata.: "Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml) to remove known batch effects specified in the sample metadata"
- [methods] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [other] Output the normalized and batch-corrected matrix in RData and text formats for downstream differential expression analysis.: "Output the normalized and batch-corrected matrix in RData and text formats for downstream differential expression analysis"
