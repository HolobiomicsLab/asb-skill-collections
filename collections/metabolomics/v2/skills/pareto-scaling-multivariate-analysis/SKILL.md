---
name: pareto-scaling-multivariate-analysis
description: Use when apply Pareto scaling when preparing normalized metabolomics data for unsupervised multivariate analysis (PCA or hierarchical clustering heatmaps) where features span multiple orders of magnitude in intensity and you want to reduce the influence of high-abundance metabolites without.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GetFeatistics
  - ggplot2
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pareto-scaling-multivariate-analysis

## Summary

Pareto scaling is a variance-stabilizing transformation applied to metabolomics feature intensity tables to equalize the contribution of features across multivariate analyses (PCA, clustering) by dividing each feature by the square root of its standard deviation, reducing dominance of high-abundance compounds while preserving low-abundance signal.

## When to use

Apply Pareto scaling when preparing normalized metabolomics data for unsupervised multivariate analysis (PCA or hierarchical clustering heatmaps) where features span multiple orders of magnitude in intensity and you want to reduce the influence of high-abundance metabolites without completely suppressing them, as Pareto scaling offers a middle ground between auto-scaling (which can amplify noise in low-intensity features) and mean-centering alone.

## When NOT to use

- Input is already Pareto-scaled or auto-scaled from another preprocessing pipeline (risk of over-correction).
- Analysis goal requires preservation of absolute quantitative differences (e.g., absolute fold-change reporting or dose–response fitting) rather than relative multivariate patterns.
- Feature table contains negative intensity values or zero-variance features (square root of standard deviation undefined or zero).

## Inputs

- Feature intensity table (samples × compounds, numeric matrix or data.frame)
- Log-transformed and mean-replaced feature columns (suffix _mr_ln)
- Sample metadata or legend table (optional, for stratification in downstream analysis)

## Outputs

- Pareto-scaled feature columns (suffix _mr_ln_paretosc)
- Column name vector tracking (saved in global environment with prefix from name_vect_names argument)
- Scaled feature table ready for PCA or clustering input

## How to apply

After applying missing value replacement (producing _mr suffix) and log-transformation (producing _mr_ln suffix) to the feature intensity table, invoke the transf_data function with scaling='pareto_scale' to produce columns with paretosc suffix. The function divides each feature by the square root of its standard deviation, computed across all samples. The vect_names_transf argument automatically saves intermediate and final column name vectors in the global environment with prefixes specified in name_vect_names, allowing traceability of transformation steps. The resulting scaled feature table is then suitable for PCA or hierarchical clustering heatmap generation using ggplot2-based visualization functions in GetFeatistics.

## Related tools

- **GetFeatistics** (R package providing transf_data() function for sequential application of missing value replacement, log transformation, and Pareto scaling with automatic column naming and vector tracking) — https://github.com/FrigerioGianfranco/GetFeatistics
- **ggplot2** (Used to generate PCA and hierarchical clustering heatmap visualizations from Pareto-scaled feature data)
- **R** (Language and environment (≥4.3.1) required to execute GetFeatistics and downstream multivariate functions)

## Evaluation signals

- Output columns have _mr_ln_paretosc suffix and match expected compound count (invariant: no features dropped during scaling unless they have zero variance).
- Feature variance after Pareto scaling is proportional to the reciprocal of original standard deviation; high-variance features are downweighted relative to low-variance features (can verify by comparing coefficient of variation before/after).
- Column name vectors saved in global environment (with name_vect_names prefix) correctly map original feature names to transformed column identifiers; vect_names_transf argument succeeded if no error or warning raised.
- PCA biplot or heatmap computed from Pareto-scaled data shows more balanced contribution across features compared to unscaled or auto-scaled versions; low-abundance metabolites are visible without being suppressed.
- No NA or Inf values introduced in scaled columns (check: all(!is.na(...)) and all(is.finite(...)) on scaled columns).

## Limitations

- Pareto scaling assumes features follow approximately log-normal or normal distributions; features with highly skewed or bimodal intensity distributions may not be adequately normalized.
- Scaling by standard deviation amplifies variance of features with low biological signal and high technical noise, potentially introducing spurious multivariate patterns.
- Requires log-transformation as a preceding step to stabilize variance across the intensity range; raw untransformed intensities may not scale appropriately.
- Features with zero or near-zero standard deviation (constant intensity across samples) cannot be Pareto-scaled and may cause numerical issues; GetFeatistics behavior in this edge case is not explicitly documented in the provided text.

## Evidence

- [other] The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale, auto_scale, pareto_scale, or range_scale (suffix paretosc for pareto).: "The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale,"
- [other] Apply Pareto scaling to produce columns with paretosc suffix, dividing each feature by the square root of its standard deviation.: "Apply Pareto scaling to produce columns with paretosc suffix, dividing each feature by the square root of its standard deviation."
- [other] Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors in the global environment with prefixes specified in name_vect_names.: "Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors in the global environment with"
- [intro] Data normalization with missing value replacement, log transformation, and scaling options [are provided]. If _scaling_ is TRUE, data will be scaled.: "Data normalization with missing value replacement, log transformation, and scaling options"
- [intro] Multivariate analysis with PCA and hierarchical clustering heatmaps [are supported]. Principal Component Analysis (PCA)...heat map with or without cluster analysis.: "Multivariate analysis with PCA and hierarchical clustering heatmaps"
- [readme] All the figures of this package are created as ggplot object, so they can be furhter modified following the ggplot2 sintax: "All the figures of this package are created as ggplot object, so they can be furhter modified following the ggplot2 sintax"
