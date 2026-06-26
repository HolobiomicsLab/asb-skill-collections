---
name: r-package-parameter-configuration
description: Use when when preparing to preprocess Salmon-derived count matrices or
  other omics abundance data, and you need to specify multiple configurable options
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - Nextflow
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger,
  limma, sva'
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

# r-package-parameter-configuration

## Summary

Configure R package parameters (filtering thresholds, normalization methods, batch correction approaches) in YAML or config files to control preprocessing of count matrices and downstream omics analysis. This skill ensures reproducible, parameterized control of edgeR, limma, and sva operations without hardcoding values in analysis scripts.

## When to use

When preparing to preprocess Salmon-derived count matrices or other omics abundance data, and you need to specify multiple configurable options (e.g., filterByExp vs. cutoff filtering, quantile vs. calcNorm normalization, or choice among combat/sva/comsva/svacom batch correction methods) in a way that can be reused across runs, shared with collaborators, or version-controlled without modifying source code.

## When NOT to use

- Input count matrix is already normalized and batch-corrected by upstream tools; reconfiguring R package parameters would introduce redundant processing.
- Samplesheet lacks required batch or condition columns referenced in the parameter configuration; the workflow will fail at runtime.
- Parameters specify a batch correction method (e.g., sva) but the samplesheet does not identify a batch variable; the method cannot be applied meaningfully.

## Inputs

- YAML configuration file (params_genes.yml) with filtering, normalization, and batch correction parameters
- Samplesheet/phenotype file with metadata columns (condition, batch, sample names)
- Salmon count matrix (RData or text format)

## Outputs

- Normalized and batch-corrected count matrix (RData format)
- Normalized and batch-corrected count matrix (text/TSV format)
- Applied parameter log or metadata record documenting which filters, normalization, and batch methods were used

## How to apply

Define a params_genes.yml or equivalent YAML configuration file that specifies: (1) filtering strategy (filterByExp boolean or cutoff threshold values); (2) normalization method (e.g., 'quantile' or 'calcNorm'); (3) batch correction approach (e.g., 'combat', 'sva', 'comsva', or 'svacom'); (4) column names from the samplesheet identifying condition and batch variables. Pass this config to the preprocess_matrix subworkflow via Nextflow's params mechanism. The R scripts (using edgeR, limma, sva packages) will read these parameters at runtime, apply the specified filtering, normalization, and batch correction operations sequentially, and output the processed RData and text matrices. Validate that parameters align with the samplesheet column names and that numeric thresholds are appropriate for your data scale (e.g., cutoff values in CPM or raw count units).

## Related tools

- **edgeR** (Performs filterByExp filtering to retain features meeting minimum expression thresholds on count matrices)
- **limma** (Applies quantile normalization (or other normalization strategies) to filtered count matrices)
- **sva** (Implements batch effect correction using ComBat, SVA, or combined approaches (comsva, svacom) based on config parameters)
- **Nextflow** (Workflow engine that parses YAML parameter files and passes them to R preprocessing subprocesses) — https://github.com/nf-core/modules

## Evaluation signals

- Configuration file is valid YAML with no syntax errors and all required keys (filtering method, normalization method, batch correction method, samplesheet column names) are present.
- Samplesheet contains the exact column names referenced in the batch and condition parameters; no missing or misspelled metadata fields.
- Output count matrix dimensions and feature/sample counts remain consistent with input (filtering should reduce features but not duplicate samples).
- Numeric filtering parameters (cutoff values) are within the expected range for the data scale (e.g., CPM or raw counts); extremely low or high thresholds may indicate misconfiguration.
- Batch effect correction has been applied: PCA or other unsupervised clustering plots show reduced batch-driven separation compared to pre-correction data.

## Limitations

- If samplesheet column names do not exactly match those specified in params_genes.yml, the workflow will fail at the batch correction or filtering stage.
- Some batch correction methods (e.g., sva) require multiple samples per batch level; insufficient replication may cause convergence failures or unstable estimates.
- Parameter choices (e.g., filterByExp threshold, normalization method) are user-defined; incorrect choices can remove biologically important features or introduce artifacts. Validation against domain knowledge is essential.
- No automatic parameter optimization or sensitivity analysis is performed; users must manually test alternative configurations if results are unexpected.

## Evidence

- [other] The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction using combat, sva, comsva, or svacom approaches, with parameters specifying the condition and batch columns from the samplesheet.: "filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction using combat, sva, comsva, or svacom approaches"
- [other] Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml.: "Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml"
- [other] Apply quantile normalization to the filtered count matrix using the limma package.: "Apply quantile normalization to the filtered count matrix using the limma package"
- [other] Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml) to remove known batch effects specified in the sample metadata.: "Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml) to remove known batch effects"
- [readme] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
