---
name: summarized-experiment-object-handling
description: Use when you have cross-validated, filtered metabolomic NMR or MS data in a SummarizedExperiment container and need to prepare it for metabolome-wide association studies (MWAS) with epidemiological confounders.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
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
---

# summarized-experiment-object-handling

## Summary

Load, validate, and prepare SummarizedExperiment objects containing metabolomic data with integrated phenotype information for downstream association analysis. This skill ensures that metabolite abundance matrices and clinical metadata are properly aligned and accessible for confounder-adjusted statistical modeling.

## When to use

You have cross-validated, filtered metabolomic NMR or MS data in a SummarizedExperiment container and need to prepare it for metabolome-wide association studies (MWAS) with epidemiological confounders. Specifically, when phenotype data (BMI, age, gender, disease status) must be linked to metabolite features (ppm values, m/z identifiers) for partial correlation or generalized linear model-based association testing.

## When NOT to use

- Phenotype data is not yet quality-controlled or contains unmapped/misaligned sample identifiers — conduct sample matching and QC first.
- Metabolite features have not been cross-validated or filtered for technical quality — apply QC and feature selection before constructing the SummarizedExperiment.
- Required confounder columns (e.g., age, gender) are missing from phenotype data — imputation or exclusion decisions must precede this step.

## Inputs

- SummarizedExperiment object (metabo_SE) with metabolite abundances in assay slot
- Phenotype table with clinical variables: disease phenotype (e.g., BMI), confounders (age, gender, T2D status), sample identifiers

## Outputs

- Validated SummarizedExperiment object with aligned metabolite assay and phenotype data (colData)
- Phenotype subset or data frame ready for confounder specification in association functions

## How to apply

Load the CV-filtered metabolomic SummarizedExperiment object (metabo_SE) and verify that the phenotype data (colData) includes all required variables: the primary phenotype of interest (e.g., BMI), confounder columns (age, gender, type II diabetes status), and any stratification variables. Inspect the assay matrix to confirm metabolite features are in rows and samples in columns, with row names set to metabolite identifiers (ppm values or m/z). Check for missing values in phenotype columns and handle according to downstream analysis requirements (e.g., complete-case analysis for partial correlations). This preparation step is critical because MWAS_stats and other association functions in MWASTools expect the SummarizedExperiment structure to enforce sample ordering consistency and avoid row-column misalignment errors during confounder adjustment.

## Related tools

- **MWASTools** (Metabolome-wide association statistics framework that consumes the validated SummarizedExperiment object to compute partial correlations and GLM-based associations with confounder adjustment) — github.com/AndreaRMICL/MWASTools
- **Bioconductor** (Provides SummarizedExperiment class definition and standard container semantics for genomic/metabolomic data)
- **R** (Programming environment for loading, validating, and manipulating SummarizedExperiment objects)

## Examples

```
library(Bioconductor); metabo_SE <- readRDS('metabo_SE_filtered.rds'); colData(metabo_SE)
```

## Evaluation signals

- SummarizedExperiment object successfully loads without errors; assay dimensions are consistent (metabolites × samples).
- Row names correspond to metabolite identifiers (ppm values) and column names to sample IDs; all samples in colData match assay columns.
- Phenotype columns for primary phenotype and all confounders (age, gender, T2D) are present, non-empty, and of appropriate data type (numeric or factor).
- No row-sample misalignment: metabolite counts and sample counts match between assay and colData after subsetting to complete cases.
- Downstream MWAS_stats function accepts the object without sample/row reordering or renaming errors.

## Limitations

- SummarizedExperiment enforces tight coupling of assay rows and colData rows; any unequal filtering must be done before object construction to avoid silent misalignment.
- Missing values in confounder columns will cause exclusion of samples in downstream association functions; imputation strategy must be specified a priori.
- Large metabolomic assays (>10,000 features) may incur memory overhead if the SummarizedExperiment is replicated across workers in parallel MWAS analyses.

## Evidence

- [other] Load the CV-filtered metabolomic SummarizedExperiment object (metabo_SE) and ensure phenotype data includes BMI, Age, Gender, and T2D status.: "Load the CV-filtered metabolomic SummarizedExperiment object (metabo_SE) and ensure phenotype data includes BMI, Age, Gender, and T2D status."
- [other] MWASTools is an R package designed to provide an integrated and user-friendly pipeline for metabolome-wide association studies.: "'MWASTools' is an R package designed to provide an integrated and user-friendly pipeline"
- [other] Assuming that R (>=3.3) and Bioconductor have been correctly installed: "Assuming that R (>=3.3) and Bioconductor have been correctly installed"
- [other] metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders: "metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders"
