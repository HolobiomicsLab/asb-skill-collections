---
name: factor-design-specification
description: Use when when setting up a DESeqDataSet from count matrices or transcript quantification, you must specify a design formula before running DESeq() if your experiment has batch effects, multiple treatment groups, or multi-factor designs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - IHW
  - tximport
  - tximeta
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- A Bioconductor package, [IHW](http://bioconductor.org/packages/IHW), is available that implements the method of *Independent Hypothesis Weighting*
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

# Factor Design Specification

## Summary

Define and encode the experimental design formula in DESeq2 that specifies which variables (factors) explain variation in RNA-seq counts, including covariates (batch effects, treatment groups) and their interactions. Proper design specification is foundational to accurate differential expression analysis, as it determines which coefficients are estimated and tested.

## When to use

When setting up a DESeqDataSet from count matrices or transcript quantification, you must specify a design formula before running DESeq() if your experiment has batch effects, multiple treatment groups, or multi-factor designs. For example, use this skill when you have airway samples with both cell type and dexamethasone treatment factors, or when HTSeq-count files include samples from different sequencing runs that need batch adjustment.

## When NOT to use

- Your experiment has no batch effects or multi-factor structure—a simple `~ condition` design may be sufficient, avoiding unnecessary model complexity.
- You are working with pre-processed, batch-corrected expression matrices rather than raw counts—design specification applies only to negative binomial count models.
- Sample metadata is incomplete or factors are not reliably recorded—design specification cannot correct for unmeasured or misclassified covariates.

## Inputs

- Count matrix (genes × samples)
- Column metadata (colData) with sample-level covariates and factors
- Design formula string (R model syntax)

## Outputs

- DESeqDataSet object with design slot populated
- GLM coefficient estimates and standard errors after DESeq()
- Extractable results tables (one per contrast or coefficient name)

## How to apply

Construct a design formula using R's model formula syntax (e.g., `~ batch + condition` or `~ cell + dex`) that lists all covariates and factors explaining count variation. Include batch variables (e.g., sequencing run, plate) early in the formula to account for technical variation before biological factors of interest. For multi-factor designs, specify interactions explicitly (e.g., `~ batch + condition + batch:condition`) if you expect condition effects to vary by batch. Pass this formula to DESeqDataSetFromMatrix(), DESeqDataSetFromTximport(), or the DESeqDataSet constructor. The design determines which coefficients DESeq() will estimate via negative binomial GLM, and which results can be extracted via results(dds, name=...). Verify that factor levels are set correctly (e.g., with factor(..., levels=c(...)) to ensure the reference level is appropriate for contrast interpretation.

## Related tools

- **DESeq2** (Accepts design formula and constructs/fits the negative binomial GLM; design determines which coefficients are estimated and tested) — https://github.com/thelovelab/DESeq2
- **tximport** (Produces SummarizedExperiment with colData that supplies sample-level metadata and factors for design specification)
- **tximeta** (Imports transcript quantification and automatically constructs SummarizedExperiment with metadata, allowing downstream design formula assignment)

## Examples

```
dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design = ~ batch + condition); dds$condition <- factor(dds$condition, levels = c("control", "treatment")); dds <- DESeq(dds); res <- results(dds, name="condition_treatment_vs_control")
```

## Evaluation signals

- DESeqDataSet object created without error; design(dds) returns the specified formula.
- After DESeq(dds), check that the number of estimated coefficients matches expected: intercept + (number of factor levels − 1) per factor, plus interactions.
- results(dds, name="factorname_levelB_vs_levelA") returns a valid table with log2FoldChange, pvalue, and padj columns; names match coefficient names printed by resultsNames(dds).
- Summary statistics show expected numbers of genes with padj < 0.1 or padj < 0.05; nonsensical results (e.g., no significant genes, all genes significant) may indicate design misspecification.
- Factor level order and reference level are correct: verify that dds$condition shows expected levels and that the reference (first level alphabetically or explicitly set) matches the intended comparison baseline.

## Limitations

- Design formula cannot account for unmeasured confounders or hidden batch effects not recorded in colData; only explicit factors in the formula are adjusted for.
- Interaction terms increase model complexity and reduce degrees of freedom; they should be used only if biological evidence or preliminary data supports interaction, not by default.
- Factors with very few samples per level may lead to unstable or non-convergent GLM fits, especially if combined with high dispersion in those groups.
- Design specification in DESeq2 assumes that the negative binomial model and standard GLM inference are appropriate; designs should be checked with exploratory plots (e.g., PCA, sample clustering) to ensure they reflect true experimental structure.

## Evidence

- [methods] The formula specifies which variables explain variation in counts: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] Design determines which coefficients are estimated and tested: "res <- results(dds, name="condition_trt_vs_untrt")"
- [other] Factor levels must be set to ensure correct reference for contrast: "dds$condition <- factor(dds$condition, levels = c("untreated","treated"))"
- [other] Design formula is passed at DESeqDataSet construction: "ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
- [other] Batch effects and treatment groups are both captured in design: "Load the airway SummarizedExperiment dataset and construct a DESeqDataSet with design ~ cell + dex using DESeq2"
