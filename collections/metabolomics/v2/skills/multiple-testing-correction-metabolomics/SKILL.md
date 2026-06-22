---
name: multiple-testing-correction-metabolomics
description: Use when you have computed raw p-values from partial Spearman correlations (or other univariate tests) between each metabolite in a SummarizedExperiment object and a phenotype of interest, adjusted for epidemiological confounders (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  tools:
  - MWASTools
  - R
  - Bioconductor
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-testing-correction-metabolomics

## Summary

Apply multiple-testing correction (Benjamini-Hochberg) to raw p-values from metabolome-wide association studies to control false discovery rate across thousands of metabolic features. This is essential when conducting univariate hypothesis testing on NMR or MS metabolomic data to distinguish true metabolite-phenotype associations from spurious correlations.

## When to use

You have computed raw p-values from partial Spearman correlations (or other univariate tests) between each metabolite in a SummarizedExperiment object and a phenotype of interest, adjusted for epidemiological confounders (e.g., age, gender, disease status), and need to report corrected significance thresholds suitable for metabolome-scale inference (typically thousands of features).

## When NOT to use

- Raw p-values have not yet been computed (correction requires individual test statistics).
- Sample size is very small (n < 10) and multiple-testing correction may be overly conservative or unstable.
- You are conducting a single hypothesis test on one pre-specified metabolite (correction is unnecessary for one test).

## Inputs

- vector of raw p-values from univariate tests (one per metabolite)
- effect size estimates (Spearman r coefficients or GLM coefficients)
- metabolite identifiers (ppm values, m/z, or compound names)

## Outputs

- BH-corrected p-values (pFDR) vector aligned to input metabolites
- three-column MWAS results matrix with columns [r, p, pFDR]
- metabolite-indexed matrix suitable for downstream filtering and visualization

## How to apply

After computing raw p-values from partial correlation or generalized linear model tests in MWASTools, apply Benjamini-Hochberg (BH) correction to the p-value vector to generate adjusted p-values (pFDR). The BH method controls the false discovery rate by ranking p-values and computing a correction threshold that accounts for the number of simultaneous tests (number of metabolites). Assemble the corrected p-values alongside the raw p-values and effect size estimates (e.g., r coefficients from Spearman correlations) into a results matrix with metabolite identifiers (ppm values or compound names) as row names. Report both raw and BH-corrected p-values to allow readers to evaluate evidence at different stringency levels and to distinguish genome/metabolome-wide significance thresholds.

## Related tools

- **MWASTools** (R/Bioconductor package that implements MWAS_stats function to compute raw p-values from partial correlations and generalized linear models; returns results ready for BH correction) — https://github.com/AndreaRMICL/MWASTools
- **R** (Statistical computing environment; base R function p.adjust() or BiocGenerics methods apply BH correction to p-value vectors)
- **Bioconductor** (R framework providing SummarizedExperiment class for metabolomic data and statistical correction utilities)

## Evaluation signals

- pFDR values are monotonically non-decreasing when sorted by raw p-value rank (Benjamini-Hochberg maintains this order invariant).
- All pFDR values are ≥ their corresponding raw p-values (correction inflates p-values).
- pFDR values do not exceed 1.0 (bounded probability).
- Number of output rows (corrected p-values) equals number of input metabolites tested.
- Results matrix contains exactly three columns with interpretable column names [r, p, pFDR] and metabolite identifiers as row names.

## Limitations

- Benjamini-Hochberg correction assumes independence or positive dependence among p-values; metabolomic features often show correlation, which may lead to conservative (overly stringent) thresholds.
- BH method controls false discovery rate (FDR), not family-wise error rate (FWER); if FWER control is required (e.g., Bonferroni), a different correction should be applied.
- Multiple-testing correction reduces statistical power; true metabolite-phenotype associations with modest effect sizes may fall below the corrected significance threshold.
- Correction depends on the total number of metabolites tested; removal or addition of features post-hoc invalidates the correction applied to the original set.

## Evidence

- [other] MWAS_stats function application with p-value and pFDR computation: "Apply Benjamini-Hochberg correction to generate adjusted p-values (pFDR). Assemble results into a three-column matrix with columns [r, p, pFDR]"
- [intro] Confounding and multivariate model limitation justifying univariate correction: "a major limitation of these multivariate models from the epidemiological perspective is that they do not properly account for cofounding factors (e.g. age, gender), which might distort the observed"
- [intro] MWASTools provides metabolite-phenotype association models with confounder adjustment: "metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders"
- [intro] MWAS using univariate hypothesis testing with confounder handling: "we present a package to perform MWAS using univariate hypothesis testing with efficient handling of epidemiological confounders"
