---
name: rna-seq-experimental-design-specification
description: Use when before constructing a DESeqDataSet from count data or tximport output, when you have raw RNA-seq samples that need to be annotated with experimental conditions, treatment groups, batch effects, or other covariates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - DESeq2
  - Salmon
  - tximportData
  - readr
  - R base (stats, formula objects)
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- txi <- tximport(files, type="salmon", tx2gene=tx2gene)
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- files <- file.path(dir,"salmon", samples$run, "quant.sf.gz")
- library("tximportData") dir <- system.file("extdata", package="tximportData")
- library("readr") tx2gene <- read_csv(file.path(dir, "tx2gene.gencode.v27.csv"))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deseq2
    doi: 10.1186/s13059-014-0550-8
    title: deseq2
  dedup_kept_from: coll_deseq2
schema_version: 0.2.0
---

# RNA-seq Experimental Design Specification

## Summary

Define sample metadata, condition labels, and design formulas that specify the biological contrasts and statistical model for differential expression testing in DESeq2. This skill ensures the experiment's biological structure is formally encoded before count matrix construction.

## When to use

Before constructing a DESeqDataSet from count data or tximport output, when you have raw RNA-seq samples that need to be annotated with experimental conditions, treatment groups, batch effects, or other covariates. Apply this skill when you need to specify which samples belong to which group and what statistical model will be used to test for differences between groups.

## When NOT to use

- Count data has already been normalized or library-size scaled prior to model fitting; design specification is only for raw count inputs.
- Experimental samples lack defined biological conditions or contrasts (e.g., purely observational cohort without treatment groups); design formula requires at least one covariate that varies across samples.
- Sample metadata is incomplete or inconsistent with the count matrix dimensions.

## Inputs

- Sample identifiers (run IDs, sample names)
- Condition labels or treatment group assignments
- Batch/blocking variables (optional but recommended)
- Count matrix or tximport list object (to validate sample count)

## Outputs

- Sample metadata table (data frame with samples as rows, covariates as columns)
- Design formula object (R formula specifying statistical model)
- Factor-encoded condition variable with explicit level ordering

## How to apply

Create a sample metadata table (data frame) with one row per RNA-seq sample and columns for sample identifiers, experimental condition (e.g., 'treated' vs. 'untreated'), and any batch or blocking variables. Assign condition labels to each sample as a factor with explicit level ordering to control which group serves as the reference in downstream contrasts (e.g., `factor(condition, levels=c('untreated','treated'))`). Construct a design formula using R formula notation (e.g., `~condition` or `~batch+condition`) that specifies which variables explain expression variation. The design formula is then passed to DESeqDataSetFromMatrix(), DESeqDataSetFromTximport(), or similar constructors to instantiate the statistical model. Verify the design is valid by confirming the number of rows in metadata matches the number of samples in the count matrix and that all condition levels are represented.

## Related tools

- **DESeq2** (Receives design formula and sample metadata to construct DESeqDataSet and fit negative binomial generalized linear model) — https://github.com/thelovelab/DESeq2
- **tximport** (Aggregates transcript-level abundance to gene level; output is passed to DESeqDataSetFromTximport with the design formula and metadata)
- **R base (stats, formula objects)** (Provides formula syntax for specifying statistical models used in design argument)

## Examples

```
samples <- data.frame(run=c('run1','run2','run3','run4'), condition=factor(c('A','A','B','B'), levels=c('A','B')), row.names='run'); ddsTxi <- DESeqDataSetFromTximport(txi, colData=samples, design=~condition)
```

## Evaluation signals

- Metadata table has exactly as many rows as there are samples in the count matrix (or tximport list), with matching sample identifiers as row names or a consistent ID column.
- All factor levels in the condition column are represented by at least one sample (no empty levels that would cause rank-deficient design matrix).
- Design formula is syntactically valid R formula (e.g., parseable as `formula(design_string)`) and contains only variables present as columns in the metadata.
- When DESeqDataSetFromMatrix() or DESeqDataSetFromTximport() is called with the metadata and design, no error about missing variables or row count mismatch is raised.
- Reference level (first level in factor ordering) is biologically sensible for downstream contrast interpretation (e.g., 'untreated' or 'control' as baseline).

## Limitations

- The design formula specifies the model structure but does not enforce sample replication; ensure each condition has multiple biological replicates to estimate dispersion accurately.
- Design matrix must be of full rank; avoid including linearly dependent variables (e.g., a batch variable that perfectly confounds with condition). DESeq2 will detect and report rank-deficiency but analysis will fail.
- Factor level ordering is critical for interpretation of log2 fold changes; changing level order changes which group is the reference but does not affect statistical significance or adjusted p-values.

## Evidence

- [other] Load the tximportData package and retrieve the sample metadata table, assigning condition labels (A and B) and setting run IDs as row names.: "Load the tximportData package and retrieve the sample metadata table, assigning condition labels (A and B) and setting run IDs as row names."
- [other] Construct a DESeqDataSet from the tximport output using DESeqDataSetFromTximport(), specifying the sample metadata and design formula (~condition).: "Construct a DESeqDataSet from the tximport output using DESeqDataSetFromTximport(), specifying the sample metadata and design formula (~condition)."
- [other] Set factor levels for reference comparison: 'dds$condition <- factor(dds$condition, levels = c("untreated","treated"))': "dds$condition <- factor(dds$condition, levels = c("untreated","treated"))"
- [other] Construct DESeqDataSet from count matrix: 'dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)': "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
