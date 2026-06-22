---
name: count-matrix-preprocessing
description: 'Use when after count matrix quantification (e.g., from Salmon) and before differential expression analysis, when you have: (1) a raw or unfiltered count matrix with potentially low-abundance features; (2) known batch effects or technical covariates documented in sample metadata;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - Salmon
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

# count-matrix-preprocessing

## Summary

Preprocessing of RNA-seq count matrices derived from quantification tools (e.g., Salmon) through configurable filtering, normalization, and batch-effect correction to prepare data for downstream differential expression analysis. This skill applies statistical and computational methods to remove low-abundance features, correct for technical variation, and standardize expression scales across samples.

## When to use

Apply this skill after count matrix quantification (e.g., from Salmon) and before differential expression analysis, when you have: (1) a raw or unfiltered count matrix with potentially low-abundance features; (2) known batch effects or technical covariates documented in sample metadata; (3) a requirement to standardize expression scales across samples using quantile or other normalization methods; (4) configurable filtering thresholds and batch-correction strategies defined in a parameters file (e.g., params_genes.yml).

## When NOT to use

- Input is already a feature table or matrix that has been preprocessed by an upstream pipeline; applying this skill would introduce redundant normalization and risk double-correction artifacts.
- Batch metadata are unavailable or unreliable in the samplesheet; batch correction requires accurate batch column specification and will produce misleading results if batch assignments are incorrect.
- Analysis goal is exploratory and does not require formal batch correction; in this case, filtering and normalization alone may be sufficient, and ComBat/SVA correction could over-correct and remove biological signal.

## Inputs

- count matrix from Salmon quantification (text or RData format)
- samplesheet/phenotype metadata file with sample identifiers, batch, and condition columns
- params_genes.yml configuration file specifying filterByExp thresholds, normalization method, and batch-correction approach

## Outputs

- filtered, normalized, and batch-corrected count matrix (RData format)
- filtered, normalized, and batch-corrected count matrix (text format)
- quality-control visualizations (heatmaps, PCA plots) of preprocessing steps

## How to apply

Load the count matrix output from Salmon quantification along with the phenotype/samplesheet file containing sample annotations and batch/condition metadata. Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds specified in params_genes.yml (e.g., CPM cutoffs). Apply quantile normalization to the filtered matrix using limma to standardize expression distributions. Finally, apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml), specifying the batch and condition columns from the samplesheet metadata. Output the normalized and batch-corrected matrix in both RData and text formats for use in differential expression workflows. The order of operations (filter → normalize → correct) is critical: filtering reduces noise before normalization, and normalization must precede batch correction to ensure proper covariate adjustment.

## Related tools

- **edgeR** (filterByExp feature filtering based on minimum expression cutoffs)
- **limma** (quantile normalization of the count matrix after filtering)
- **sva** (batch-effect correction using SVA, comsva, or svacom approaches)
- **Salmon** (upstream quantification tool producing the count matrix input)
- **ComplexHeatmap** (visualization of preprocessing results and batch effects)
- **ggplot2** (quality-control plotting and diagnostic visualizations)
- **Nextflow** (workflow orchestration and process containerization) — https://github.com/nf-core/modules

## Evaluation signals

- Filtered matrix has dimensions consistent with params_genes.yml threshold settings; verify that the number of retained features is in the expected range and that low-abundance features (below CPM or count cutoff) are removed.
- Quantile normalization is applied symmetrically across all samples; check that median expression, variance, and distribution metrics are equalized post-normalization using box plots or density plots.
- Batch correction reduces between-batch variance while preserving within-condition biological signal; evaluate using PCA or heatmap clustering—samples should cluster by condition (not batch) post-correction, and ComBat/SVA-corrected and uncorrected matrices should show visually distinct separation along batch axes.
- Output matrices match input sample count and feature metadata; verify that row names (feature IDs) and column names (sample IDs) are preserved and correspond to the samplesheet.
- RData and text format outputs are identical; verify checksums or load both formats and confirm numerical equivalence to ensure reproducibility.

## Limitations

- Batch correction assumes that batch effects are technical rather than biological; if batch and condition are confounded, batch correction may remove true biological signal and produce biased differential expression results.
- filterByExp filtering is sensitive to the minimum expression threshold specified in params_genes.yml; incorrect thresholds can either retain too much noise or remove genuine low-abundance transcripts of biological interest.
- Quantile normalization assumes that the majority of features are not differentially expressed between samples; if a large proportion of the transcriptome is perturbed (e.g., in extreme phenotypes or cell types), quantile normalization may introduce bias.
- SVA and ComBat require sufficient sample replication within batches; small or unbalanced batch designs may lead to unstable correction or overfitting.
- The preprocess_matrix subworkflow does not account for compositional bias (library size normalization) prior to filtering; ensure that Salmon quantification or upstream steps have normalized for sequencing depth.

## Evidence

- [other] The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction using combat, sva, comsva, or svacom approaches, with parameters specifying the condition and batch columns from the samplesheet.: "The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect"
- [other] Load the count matrix (output from Salmon) and phenotype/samplesheet file. 2. Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml. 3. Apply quantile normalization to the filtered count matrix using the limma package. 4. Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml) to remove known batch effects specified in the sample metadata. 5. Output the normalized and batch-corrected matrix in RData and text formats for downstream differential expression analysis.: "Load the count matrix (output from Salmon) and phenotype/samplesheet file. Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in"
- [methods] Data preprocessing  [section=methods; evidence='Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap']: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [methods] Differential expression analysis  [section=methods; evidence='Genes, miRNA, isoforms, proteins, lipids | Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap']: "Differential expression analysis | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
- [other] parameters specifying the condition and batch columns from the samplesheet: "parameters specifying the condition and batch columns from the samplesheet"
