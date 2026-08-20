---
name: metabolomics-feature-transformation
description: Use when when you have a feature intensity table (samples × compounds)
  from targeted or non-targeted metabolomics and need to prepare it for statistical
  modeling or multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GetFeatistics
  - ggplot2
  - XCMS
  - MS-Dial
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration
  of metabolomics data
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-transformation

## Summary

Sequential application of missing value replacement, log transformation, and scaling (mean-centering, auto-scaling, Pareto, or range scaling) to metabolomics feature intensity tables, with automatic tracking of intermediate transformation steps via compound column name suffixes and saved name vectors.

## When to use

When you have a feature intensity table (samples × compounds) from targeted or non-targeted metabolomics and need to prepare it for statistical modeling or multivariate analysis. Use this skill when raw peak areas or intensities contain missing values, show right-skewed distributions, or have features with widely varying dynamic ranges—all common in LC-MS or GC-MS metabolomics data.

## When NOT to use

- Input is already a pre-transformed, normalized, or scaled feature table—applying additional transformations risks over-processing and loss of interpretability.
- Missing value rate exceeds domain-specific tolerance (e.g., >50% missing in a feature)—missing value replacement may introduce artifacts without sufficient information.
- Feature intensities are already approximately normally distributed or follow a known, non-log-normal distribution—log transformation may worsen fit.

## Inputs

- Feature intensity table (matrix or data.frame: samples × compounds with numeric intensity or peak area values)
- Legend table (optional; data.frame with sample identifiers, sample type classification (blank/curve/qc/unknown), and known concentration values for curve and QC samples)

## Outputs

- Transformed feature table with columns named using compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) reflecting transformation sequence
- Name vectors saved in global environment (prefixed vectors documenting original feature names and their transformed column identifiers for each transformation step)

## How to apply

Load the feature table (samples in rows, compounds in columns) and optionally a legend table specifying sample types (blank, curve, qc, unknown) and concentrations. Call the transf_data function from GetFeatistics, enabling missing_replace=TRUE to substitute NA values (producing _mr suffix), log_transf=TRUE to apply natural logarithm transformation (adding _ln suffix), and specify a scaling method (scaling=TRUE with scale_type='pareto_scale' for Pareto scaling, producing _paretosc suffix). Set vect_names_transf=TRUE to automatically save intermediate column name vectors to the global environment with user-specified prefixes (name_vect_names argument). The function applies transformations sequentially and generates output columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) documenting the transformation lineage. Monitor the name vectors to verify correct feature tracking through each step.

## Related tools

- **GetFeatistics** (R package providing transf_data function for sequential feature transformation with missing value replacement, log transformation, and scaling options) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Runtime environment (version ≥ 4.3.1) required for executing GetFeatistics package functions)
- **ggplot2** (Used to visualize transformed feature distributions and relationships post-transformation)
- **XCMS** (Upstream non-targeted feature extraction tool; output feature tables are typical input to transformation workflow)
- **MS-Dial** (Alternative upstream non-targeted feature extraction tool; output feature tables are typical input to transformation workflow)

## Examples

```
library(GetFeatistics); transf_data(data = feature_table, missing_replace = TRUE, log_transf = TRUE, scaling = TRUE, scale_type = 'pareto_scale', vect_names_transf = TRUE, name_vect_names = 'feat')
```

## Evaluation signals

- Output column names follow expected compound suffix pattern (_mr, _mr_ln, _mr_ln_paretosc) and increase in length with each transformation step applied.
- Name vectors saved to global environment have correct length matching the number of features and document original feature identifiers before and after each transformation.
- No missing (NA) values remain in _mr or downstream columns if missing_replace=TRUE was specified.
- Log-transformed columns (_ln) contain only finite numeric values (no -Inf or NaN from log of zero or negative); negative values or zeros in original intensities should trigger investigation.
- Scaled columns (_paretosc for Pareto scaling) have mean near zero and standard deviation near unity across all samples; verify via colMeans() and apply(data, 2, sd).
- Comparing pre- and post-transformation univariate distributions (e.g., via qqplot or Shapiro-Wilk test on log-transformed columns) shows improved normality approximation.

## Limitations

- Missing value replacement strategy (simple substitution) does not account for missing-at-random mechanisms; sophisticated imputation (KNN, multiple imputation) is not implemented in transf_data.
- Log transformation assumes all intensity values are positive; zero or negative intensities (rare but possible in some instrumental artifacts or data entry errors) must be pre-screened or handled via offset parameter before calling transf_data.
- Pareto scaling and other scaling methods assume features have sufficient variance; features with near-zero standard deviation may produce non-finite scaled values.
- Sequential transformation order (missing → log → scaling) is fixed; alternative orders (e.g., scaling before log) are not supported by transf_data and must be implemented manually.
- Name vector tracking relies on user-specified prefixes in name_vect_names argument; omitting or misspecifying this argument results in loss of transformation lineage documentation.

## Evidence

- [other] Sequential transformation pattern with naming convention: "The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale,"
- [other] Name vector tracking and global environment storage: "the vect_names_transf argument automatically saves intermediate column name vectors in the global environment with prefixes specified in name_vect_names"
- [intro] Data format requirements and transformation steps: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] Missing value and log transformation implementation: "If _missing_replace_ is TRUE, each NA in the data will be replaced...If _log_transf_ is TRUE, the data will be log-transformed"
- [intro] Scaling parameter activation and method selection: "If _scaling_ is TRUE, data will be scaled"
- [other] Pareto scaling mathematical definition: "Apply Pareto scaling to produce columns with paretosc suffix, dividing each feature by the square root of its standard deviation"
- [readme] Installation and invocation pattern: "devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)"
