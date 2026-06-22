---
name: mean-centering-normalization
description: Use when apply mean-centering when you have a feature intensity table (samples × compounds) from metabolomics analysis and you need to standardize feature intensities by removing the average signal before multivariate analysis (e.g., PCA) or downstream statistical modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - GetFeatistics
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
---

# mean-centering-normalization

## Summary

Mean-centering (mean-scaling) is a feature-wise data transformation that subtracts the mean intensity of each compound across all samples, producing normalized columns with _mr suffix. It is applied as the first step in the GetFeatistics sequential transformation pipeline before log-transformation and Pareto scaling, used to center metabolomics feature intensities around zero.

## When to use

Apply mean-centering when you have a feature intensity table (samples × compounds) from metabolomics analysis and you need to standardize feature intensities by removing the average signal before multivariate analysis (e.g., PCA) or downstream statistical modeling. This is typically the first normalization step in the GetFeatistics workflow, before log-transformation or scaling; use it when raw peak area intensities still contain additive baseline shifts that should be removed prior to variance-stabilizing transformations.

## When NOT to use

- Input feature table is already log-transformed or pre-scaled (applying mean-centering to log-scale data may remove meaningful intensity differences).
- Data contains strong sample-wise batch effects or instrumental drift that require reference-sample normalization (e.g., QC-based LOESS) instead of global mean-centering.
- Analysis requires preservation of absolute intensities for concentration estimation or calibration curve fitting (mean-centering destroys the zero-intensity reference point).

## Inputs

- Feature intensity table: samples in rows, compounds in columns, with numeric peak area or intensity values
- Sample metadata/legend table: optional, used for stratified mean computation if QC-aware normalization is desired

## Outputs

- Mean-centered feature intensity table with columns suffixed _mr
- Column name vector tracking original identifiers and _mr-transformed identifiers (saved in global environment if vect_names_transf=TRUE)

## How to apply

The transf_data function applies mean-centering by subtracting the mean intensity of each compound across all samples, producing output columns with _mr suffix (mean-replaced). This transformation is applied sequentially: first mean-centering (_mr), then optionally log-transformation (_ln), then optional scaling (e.g., Pareto, auto-, range-, or mean-scale). The function automatically tracks transformed column names in name vectors with user-specified prefixes saved to the global environment via the vect_names_transf argument. Mean-centering is element-wise subtraction (intensity_centered = intensity_raw - mean(intensity_raw across all samples)) and does not require tuning; it is deterministic and reproducible once the mean is computed from the input table.

## Related tools

- **GetFeatistics** (R package providing the transf_data function that implements sequential mean-centering, log-transformation, and scaling of metabolomics feature tables) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Runtime environment for executing GetFeatistics and transf_data)

## Examples

```
library(GetFeatistics); data_norm <- transf_data(data_table, log_transf=FALSE, missing_replace=TRUE, scaling=FALSE, vect_names_transf=TRUE)
```

## Evaluation signals

- Output columns carry _mr suffix in column names; original column names are documented in vect_names_transf vectors
- For each compound, the mean of the _mr-transformed values across all samples should equal or be very close to zero (within floating-point rounding tolerance ~1e-10)
- The rank ordering and relative differences between samples within each compound should be preserved; only the additive offset changes
- If log-transformation follows (_ln suffix), the log-space values should be computed from _mr intensities, not raw intensities
- Downstream Pareto-scaled or auto-scaled columns should reference the _mr values, documented by compound naming chains like _mr_ln_paretosc

## Limitations

- Mean-centering does not stabilize variance; features with naturally high variance will remain high-variance after centering. Pareto or auto-scaling must follow to address heteroscedasticity.
- If missing values (NAs) are present and not replaced first, the mean computation will return NA, propagating missingness. The transf_data function requires missing_replace=TRUE to be set before mean-centering to handle this.
- Global mean-centering assumes all samples should contribute equally to the feature baseline; it is not QC-aware and does not adapt to instrumental drift or batch effects within the sample set.
- Centering around zero loses the absolute intensity scale; subsequent statistical models fitted on centered data will have intercepts near zero, which may require careful interpretation if absolute concentrations or peak areas are scientifically meaningful.

## Evidence

- [other] Apply mean-centering transformation to produce columns with _mr suffix, subtracting the mean of each feature across all samples.: "Apply mean-centering transformation to produce columns with _mr suffix, subtracting the mean of each feature across all samples."
- [other] The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale, auto_scale, pareto_scale, or range_scale (suffix paretosc for pareto). Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors in the global environment with prefixes specified in name_vect_names.: "The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale,"
- [intro] Data normalization with missing value replacement, log transformation, and scaling options: "If _missing_replace_ is TRUE, each NA in the data will be replaced...If _log_transf_ is TRUE, the data will be log-transformed...If _scaling_ is TRUE, data will be scaled"
- [intro] The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
