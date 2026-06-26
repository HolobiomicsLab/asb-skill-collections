---
name: batch-vector-preparation
description: Use when you have a metabolomics dataset with samples collected across
  multiple batches (e.g., different MS runs, sample preparation rounds, or instrument
  configurations) and need to apply batch-aware correction methods such as CordBat.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - CordBat
  - R
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c05748
  title: CordBat
evidence_spans:
- fit <- CordBat( X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref",
  grouping = FALSE, print.detail = FALSE )
- '%\VignetteEngine{knitr::rmarkdown}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cordbat_cq
    doi: 10.1021/acs.analchem.2c05748
    title: CordBat
  dedup_kept_from: coll_cordbat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05748
  all_source_dois:
  - 10.1021/acs.analchem.2c05748
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-vector-preparation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a categorical batch assignment vector from metabolomics sample metadata to label each observation with its batch provenance. This vector is a required input to concordance-based batch correction workflows and must align dimensionally with the metabolite matrix rows.

## When to use

You have a metabolomics dataset with samples collected across multiple batches (e.g., different MS runs, sample preparation rounds, or instrument configurations) and need to apply batch-aware correction methods such as CordBat. Batch labeling must be encoded as a vector with one entry per sample, matching the row order of the metabolite matrix.

## When NOT to use

- Samples have no batch structure or all samples come from a single batch — batch correction is unnecessary.
- Batch labels are already embedded in row names of the metabolite matrix and cannot be reliably extracted as a separate vector.
- The metadata contains missing or ambiguous batch assignments that cannot be unambiguously mapped to samples.

## Inputs

- sample metadata table (data frame with batch assignment column)
- metabolite matrix (rows = samples, columns = metabolites)

## Outputs

- batch assignment vector (character or factor; length = number of samples)

## How to apply

Extract the batch assignment column(s) from your sample metadata table and construct a vector with length equal to the number of rows in your metabolite matrix. Each entry should be a batch label (e.g., 'Batch1', 'Batch2', or 'Ref') corresponding to the batch in which that sample was analyzed. The vector must be in the same row order as your metabolite data matrix. Pass this vector as the `batch` parameter to CordBat() along with log2-transformed metabolite measurements and a group assignment vector. Verify that the vector contains no missing values and that all unique batch labels are represented; if one batch is designated as a reference (e.g., 'Ref'), ensure it is explicitly labeled so it can be specified via the `ref.batch` parameter.

## Related tools

- **CordBat** (Accepts batch-vector as input parameter to perform concordance-based batch effect correction on log-transformed metabolite matrices) — https://github.com/BorchLab/CordBat
- **R** (Language environment for constructing vectors from data frames and executing batch correction workflows)

## Examples

```
batch_vec <- cordbat_example$batch; fit <- CordBat(X=X_mat, batch=batch_vec, group=group_vec, ref.batch="Ref", grouping=FALSE, print.detail=FALSE)
```

## Evaluation signals

- batch_vec length equals number of rows in metabolite matrix (nrow(X_mat))
- batch_vec contains no NA or NULL entries
- All unique batch labels in batch_vec are valid strings (e.g., no whitespace-only entries)
- If ref.batch='Ref' is specified in CordBat call, 'Ref' is present in batch_vec with at least one occurrence
- Row order of batch_vec matches row order of metabolite matrix (samples at index i in both structures correspond)

## Limitations

- Batch vector does not account for confounding effects beyond batch; group effects must be specified separately via group_vec parameter.
- Concordance-based correction assumes batch effects are multiplicative on log-scale; highly non-linear or sample-specific batch artifacts may not be adequately corrected.
- Reference batch selection influences the scale and direction of corrections; misspecification of ref.batch can bias results.

## Evidence

- [other] CordBat() accepts a log-transformed metabolite matrix (X_mat), batch assignment vector (batch_vec), group assignment vector (group_vec), a reference batch label ("Ref"), and a grouping parameter set to FALSE: "CordBat() accepts a log-transformed metabolite matrix (X_mat), batch assignment vector (batch_vec), group assignment vector (group_vec), a reference batch label ("Ref")"
- [other] Log2-transform the metabolite matrix and prepare batch and group vectors from metadata.: "Log2-transform the metabolite matrix and prepare batch and group vectors from metadata"
- [other] Run CordBat() with X=log2-transformed matrix, batch=batch vector, group=group vector, ref.batch='Ref', grouping=FALSE, and print.detail=FALSE.: "Run CordBat() with X=log2-transformed matrix, batch=batch vector, group=group vector, ref.batch='Ref', grouping=FALSE"
- [methods] fit <- CordBat( X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref", grouping = FALSE, print.detail = FALSE ): "fit <- CordBat(
  X          = X_mat,
  batch      = batch_vec,
  group      = group_vec,
  ref.batch  = "Ref",
  grouping   = FALSE,        
  print.detail = FALSE
)"
- [readme] Concordance-Based Batch Effect Correction for Large-Scale Metabolomics: "Concordance-Based Batch Effect Correction for Large-Scale Metabolomics"
