---
name: differential-expression-analysis-algorithm-selection
description: Use when after preprocessing and normalizing count matrices from transcriptomics
  or other omics data, when you need to identify differentially expressed features
  between experimental groups and must choose between edgeR (for flexible formula/contrast
  designs), DESeq2 (for designs with explicit.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - RankProduct (RankProd)
  - Nextflow DSL2
  license_tier: open
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
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

# differential-expression-analysis-algorithm-selection

## Summary

Select and execute a differential expression analysis algorithm (edgeR, DESeq2, or RankProduct) on preprocessed count matrices based on experimental design and samplesheet metadata conventions. This skill dispatches the appropriate statistical method via a configuration parameter, ensuring compatibility between the chosen algorithm and required phenotype columns.

## When to use

After preprocessing and normalizing count matrices from transcriptomics or other omics data, when you need to identify differentially expressed features between experimental groups and must choose between edgeR (for flexible formula/contrast designs), DESeq2 (for designs with explicit condition and batch columns), or RankProduct (for simple 0/1 control-treatment classification). Use this skill when the pipeline or analysis framework requires explicit algorithm selection via a parameter like alg_genes in params.yml.

## When NOT to use

- Input is already a list of significantly differentially expressed features or a pre-computed results table — algorithm selection and execution are not needed.
- Samplesheet metadata does not contain the required columns for the selected algorithm (e.g., missing 'batch' for DESeq2 or 'cl' for RankProduct).
- Count matrix is not preprocessed or normalized; raw sequencing counts have not been filtered, normalized, or batch-corrected.

## Inputs

- preprocessed count matrix (genes, miRNAs, isoforms, proteins, or lipids)
- phenotype/sample metadata file with algorithm-specific required columns (condition, batch, or cl)
- configuration file specifying alg_genes parameter (edgeR, DESeq2, or RankProduct)

## Outputs

- differential expression results table with feature IDs, fold-changes, test statistics, raw p-values, and adjusted p-values
- volcano plot (log2-fold-change vs. -log10 adjusted p-value)
- MA plot (average log-expression vs. log2-fold-change)
- p-value distribution histogram
- hierarchically organized output directory (e.g., /output_directory/genes/ for gene-level results)

## How to apply

Parse the alg_genes parameter from the configuration file (typically params.yml or params_genes.yml, defaulting to 'edger' if unspecified) to determine which algorithm to invoke. Before execution, validate that the samplesheet metadata contains the algorithm-specific required columns: edgeR requires 'condition' for grouping and accepts optional custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for control samples and 1 for treatment samples. Load the preprocessed count matrix and phenotype metadata, execute the selected R package implementation (DESeq2, edgeR, or RankProd) using the sample group assignments from the appropriate metadata column, and generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values. Create diagnostic plots (volcano plot, MA plot, p-value distribution histogram) using ggplot2 and ComplexHeatmap to assess result quality and technical validity.

## Related tools

- **edgeR** (Differential expression analysis for count data using exact tests or generalized linear models with flexible formula and contrast specification)
- **DESeq2** (Differential expression analysis using Wald or LRT tests on count data with explicit condition and batch metadata columns)
- **RankProduct (RankProd)** (Non-parametric differential expression analysis using rank product statistics for 0/1 control-treatment classification)
- **ggplot2** (Visualization of volcano plots, MA plots, and p-value distributions for diagnostic assessment)
- **ComplexHeatmap** (Generation of heatmap visualizations for differential expression results)
- **Nextflow DSL2** (Workflow orchestration for dispatching algorithm-specific differential expression processes) — https://github.com/nf-core/modules

## Evaluation signals

- Results table contains exactly one row per feature with non-null fold-change, test statistic, raw p-value, and adjusted p-value columns.
- Adjusted p-values are monotonically non-decreasing when sorted by raw p-value (Benjamini–Hochberg or equivalent correction applied correctly).
- Volcano plot shows expected separation: features with high fold-change and low adjusted p-value in upper-left and upper-right quadrants; central cloud at low fold-change represents non-significant features.
- MA plot shows mean-variance trend with most points centered around log2-fold-change = 0; variance increases at lower expression levels.
- Output directory structure matches specification (e.g., /output_directory/genes/) and contains all expected diagnostic plots and results files without errors or missing data.

## Limitations

- Algorithm choice is irreversible once execution begins; incorrect samplesheet column names for the selected algorithm will cause execution failure without automatic fallback.
- edgeR, DESeq2, and RankProduct assume different underlying statistical models and distributional assumptions; choice of algorithm can substantially influence significance rankings and p-value distributions, especially at intermediate effect sizes.
- RankProduct's binary 0/1 design is incompatible with multi-group comparisons or continuous covariates; edgeR and DESeq2 are more flexible but require exact column naming for DESeq2.
- Results are sensitive to preprocessing parameters (filtering thresholds, normalization method, batch correction); mismatched preprocessing can propagate into false positives or negatives.

## Evidence

- [other] The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'): "users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger')"
- [other] edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for controls and 1 for treatments: "edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for controls and 1"
- [other] Load the preprocessed count matrix and phenotype/sample metadata file, parse the alg_genes parameter, execute the selected algorithm, generate results table with feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values: "Load the preprocessed count matrix and phenotype/sample metadata file. Parse the alg_genes parameter from params.yml to select the differential expression algorithm. Execute the selected algorithm"
- [other] Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap: "Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap."
- [other] Write results to output directory organized hierarchically by omics type (e.g., /output_directory/genes/): "Write results to output directory organized hierarchically by omics type (e.g., /output_directory/genes/)"
- [methods] Differential expression analysis for Genes, miRNA, isoforms, proteins, lipids using R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analyss | Genes, miRNA, isoforms, proteins, lipids | Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
