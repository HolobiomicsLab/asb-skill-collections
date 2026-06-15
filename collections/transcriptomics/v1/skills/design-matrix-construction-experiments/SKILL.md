---
name: design-matrix-construction-experiments
description: Use when when you have microarray or RNA-seq expression data paired with phenotype/sample metadata describing experimental conditions, treatments, or group assignments, and you need to fit a linear model to test for differential expression across those conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - edgeR
  - limma
  - R
  - voom
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- calcNormFactors [TMM normalization]
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
- 'Voom: precision weights unlock linear model analysis tools for RNA-seq read counts'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_limmavoom
    doi: 10.1186/gb-2014-15-2-r29
    title: limmavoom
  dedup_kept_from: coll_limmavoom
schema_version: 0.2.0
---

# Design-matrix construction for experiments

## Summary

Construction of a design matrix that encodes experimental groups, conditions, or contrasts to specify the linear model structure for differential expression analysis. A properly constructed design matrix is essential input to limma's lmFit function and determines which coefficients will be estimated and which comparisons can be made.

## When to use

When you have microarray or RNA-seq expression data paired with phenotype/sample metadata describing experimental conditions, treatments, or group assignments, and you need to fit a linear model to test for differential expression across those conditions. Specifically, design-matrix construction is required before applying limma's lmFit or voom pipeline.

## When NOT to use

- The design matrix has already been constructed or is provided as part of the input data object.
- You are performing unsupervised analysis (e.g., clustering, dimensionality reduction) where no experimental group labels are available or relevant.
- The analysis goal is exploratory data quality assessment rather than hypothesis-driven differential expression testing.

## Inputs

- expression matrix (genes × samples)
- sample metadata / phenotype table with experimental group or condition assignments
- experimental design specification (e.g., treatment factor, control vs. treatment labels)

## Outputs

- design matrix (samples × coefficients)
- specification of contrasts or comparisons to be tested

## How to apply

Load expression data and sample metadata from a public repository (e.g., GEO accession). Identify the experimental groups or conditions of interest from the phenotype metadata. Construct a design matrix (typically a numeric matrix with samples as rows and coefficients/contrasts as columns) that encodes these group assignments or experimental factors using R functions such as model.matrix(). The matrix should have one row per sample and columns representing the intercept and contrasts of interest. Verify that all samples are accounted for and that the matrix rank matches the number of estimable parameters. Pass the completed design matrix to lmFit along with the expression matrix to fit coefficients for each gene.

## Related tools

- **limma** (Linear model fitting framework that accepts the design matrix to specify which coefficients to estimate for each gene) — https://github.com/bioc/limma
- **R** (Programming environment for constructing design matrices via model.matrix() or manual specification)
- **edgeR** (Companion package that uses design matrices to specify contrasts and normalization factors in DGEList workflows)

## Examples

```
design <- model.matrix(~condition, data=metadata); fit <- lmFit(expression_matrix, design)
```

## Evaluation signals

- Design matrix has correct dimensions: number of rows equals number of samples, number of columns equals number of estimable parameters.
- All samples from the expression matrix are represented in the design matrix (no missing or extra rows).
- Matrix rank equals the number of columns, ensuring no linear dependencies among predictors that would prevent coefficient estimation.
- Coefficient estimates from lmFit can be extracted and are interpretable in terms of the original experimental contrasts (e.g., log-fold-changes between conditions).
- Comparison of ranked gene lists and adjusted p-values with and without the design matrix shows expected differential expression patterns aligned with known biological effects.

## Limitations

- Design matrix construction requires accurate and complete sample metadata; missing or mislabeled condition assignments will propagate into incorrect coefficient estimates.
- Unbalanced designs (unequal sample sizes across groups) reduce statistical power; the design matrix does not correct for this imbalance but rather encodes it.
- Collinearity among predictors or rank deficiency in the matrix will prevent full rank estimation; careful specification of contrasts or dropping of redundant columns is necessary to avoid singular fits.

## Evidence

- [other] Construct a design matrix encoding the experimental groups or conditions of interest.: "Construct a design matrix encoding the experimental groups or conditions of interest."
- [other] Apply limma's lmFit function to fit a linear model to the expression matrix using the design matrix, obtaining coefficient estimates and residual standard errors.: "Apply limma's lmFit function to fit a linear model to the expression matrix using the design matrix, obtaining coefficient estimates and residual standard errors."
- [other] the use of linear models for analysing designed experiments and the assessment of differential expression: "the use of linear models for analysing designed experiments and the assessment of differential expression"
