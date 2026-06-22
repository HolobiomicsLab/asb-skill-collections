---
name: batch-effect-correction-reference-based
description: Use when when you have log-transformed metabolite abundance data from multiple batches (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - CordBat
  - R
  - ggplot2
  - dplyr
derived_from:
- doi: 10.1021/acs.analchem.2c05748
  title: CordBat
evidence_spans:
- fit <- CordBat( X = X_mat, batch = batch_vec, group = group_vec, ref.batch = "Ref", grouping = FALSE, print.detail = FALSE )
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
---

# batch-effect-correction-reference-based

## Summary

Apply concordance-based batch effect correction to log-transformed metabolomics data by designating a reference batch and disabling group-level stratification. This skill removes batch-driven signal drift while preserving biological group differences in large-scale metabolite matrices.

## When to use

When you have log-transformed metabolite abundance data from multiple batches (e.g., mass spectrometry runs or sample processing cohorts), a single batch can be nominated as a stable reference standard, and you want to correct all other batches to match the reference's statistical properties without stratifying correction within biological groups.

## When NOT to use

- Data is not log-transformed; CordBat expects log-scale input to model multiplicative batch effects.
- No clear reference batch exists or reference batch quality is questionable; design should nominate a batch known to have minimal technical variability.
- Correction should preserve or exploit group-level batch heterogeneity; set grouping=FALSE assumes batch effects are consistent across groups, which may not hold if group×batch interactions are strong.

## Inputs

- log2-transformed metabolite abundance matrix (numeric; samples × metabolites)
- batch assignment vector (character or factor; length = number of samples)
- group assignment vector (character or factor; length = number of samples)
- reference batch label (character; must match one unique value in batch vector)

## Outputs

- corrected log2-scale metabolite matrix (numeric; samples × metabolites; from fit$X.cor)
- fitted CordBat object (contains convergence details and model parameters)

## How to apply

Prepare a log2-transformed metabolite matrix (rows = samples, columns = metabolites), a batch assignment vector identifying which batch each sample belongs to (with one batch labeled 'Ref'), and a group assignment vector. Call CordBat() with the log-transformed matrix, batch vector, group vector, ref.batch='Ref', and grouping=FALSE. CordBat uses concordance-based normalization to align batch statistics to the reference batch without iterative loops. Extract the corrected log2-scale matrix from the fit object (fit$X.cor). Back-transform by exponentiating (2^corrected_mat) for downstream visualization or statistical testing. The reference batch acts as the anchor; all other batches' systematic offsets are measured and removed relative to it.

## Related tools

- **CordBat** (Performs concordance-based batch effect correction on log-transformed metabolite matrices with reference batch specification and optional group stratification.) — https://github.com/BorchLab/CordBat
- **R** (Runtime environment for executing CordBat function calls and data transformations.)
- **ggplot2** (Visualization of PCA results before and after batch correction to assess removal of batch effects.)
- **dplyr** (Data wrangling and preparation of batch and group assignment vectors from metadata.)

## Examples

```
fit <- CordBat(X = as.matrix(log2(cordbat_example[metabolite_cols])), batch = batch_vec, group = group_vec, ref.batch = "Ref", grouping = FALSE, print.detail = FALSE); corrected_mat <- fit$X.cor
```

## Evaluation signals

- PCA plot on back-transformed corrected data (2^corrected_mat) shows samples from different batches overlapping in principal component space, whereas uncorrected PCA showed clear batch-driven clustering.
- Corrected matrix retains original dimensions and range; no NaN, Inf, or unexpected values introduced.
- fit object contains convergence status and model parameters; print.detail=FALSE still allows inspection of fit$X.cor.
- Biological group signal is preserved: mean log2-abundance differences between groups remain statistically significant post-correction.
- Reference batch samples remain numerically unchanged or minimally perturbed in corrected matrix (ref.batch acts as anchor).

## Limitations

- Assumes batch effects are multiplicative and uniform across metabolites; if batch effects are additive or highly metabolite-specific, correction may be incomplete.
- Requires designation of a high-quality reference batch; poor reference choice propagates bias to all corrected batches.
- grouping=FALSE means correction does not account for group×batch interactions; if such interactions are present, residual group-confounded batch signal may persist.
- CordBat is optimized for large-scale metabolomics (25+ metabolites per sample in the example); performance or stability on very small datasets not characterized.

## Evidence

- [other] CordBat() accepts a log-transformed metabolite matrix (X_mat), batch assignment vector (batch_vec), group assignment vector (group_vec), a reference batch label ('Ref'), and a grouping parameter set to FALSE, producing a fitted object from which the corrected matrix is extracted via fit$X.cor.: "CordBat() accepts a log-transformed metabolite matrix (X_mat), batch assignment vector (batch_vec), group assignment vector (group_vec), a reference batch label ("Ref"), and a grouping parameter set"
- [methods] fit <- CordBat(
  X          = X_mat,
  batch      = batch_vec,
  group      = group_vec,
  ref.batch  = "Ref",
  grouping   = FALSE,        
  print.detail = FALSE
): "fit <- CordBat(
  X          = X_mat,
  batch      = batch_vec,
  group      = group_vec,
  ref.batch  = "Ref",
  grouping   = FALSE,        
  print.detail = FALSE
)"
- [methods] Log-transform metabolite measurements and extract the corrected log2-scale matrix from fit$X.cor.: "X_mat      <- as.matrix(log2(cordbat_example[met_cols]))"
- [readme] This is a R package implementation of the Concordance-Based Batch Effect Correction for Large-Scale Metabolomics (CordBat).: "This is a R package implementation of the Concordance-Based Batch Effect Correction for Large-Scale Metabolomics (CordBat)."
- [readme] There is no methodologic change within the CordBat package from the original publication, however, substantial changes have been made to improve computational efficiency and limit iterative loops.: "There is no methodologic change within the CordBat package from the original publication, however, substantial changes have been made to improve computational efficiency and limit iterative loops."
