---
name: fold-change-log2-transformation
description: Use when when preparing fold-change measurements from multiple metabolomics studies for quantitative meta-analysis via weighted averaging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - amanida
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fold-change-log2-transformation

## Summary

Log2 transformation of fold-change values enables symmetric representation of up- and down-regulation and facilitates study-size-weighted averaging in quantitative metabolomics meta-analysis. This transformation is a prerequisite step before combining fold-changes across multiple studies using weighted averaging methods.

## When to use

When preparing fold-change measurements from multiple metabolomics studies for quantitative meta-analysis via weighted averaging. Specifically, apply this transformation immediately after importing fold-change columns and handling negative values (via reciprocal transformation), and before computing study-size-weighted averages of the combined fold-change metric.

## When NOT to use

- Input fold-change values have not been validated for positivity (i.e., negative values have not been reciprocally transformed first).
- Analysis goal is qualitative vote-counting only (which uses trend labels, not fold-change magnitudes).
- Raw individual-level data are available; use difference-of-means effect size and variance-weighted methods instead.

## Inputs

- fold-change column (numeric vector, positive real values after negative-value reciprocal transformation)
- study size column (N, sample counts per study)
- tibble or data frame with required columns: identifier, p-value, fold-change, N, reference

## Outputs

- log2-transformed fold-change vector (numeric, symmetric around 0)
- study-size-weighted average fold-change (single numeric value)
- meta-analysis @stat results table (including weighted fold-change and trend direction)

## How to apply

Transform each fold-change value using the log2 function: log2(fold-change). This log-scale transformation converts multiplicative fold-changes into an additive metric where up-regulation (FC > 1) yields positive log2 values and down-regulation (FC < 1) yields negative log2 values, with a symmetric zero point. The log2-transformed fold-changes are then weighted by each study's sample size (N) and averaged across all studies to produce a single meta-analytic fold-change estimate. This weighting scheme accounts for the statistical power contributed by larger studies, ensuring that well-powered studies exert proportionally greater influence on the combined effect size.

## Related tools

- **amanida** (R package that applies log2 transformation to fold-changes and computes study-size-weighted averaging within the compute_amanida function) — https://github.com/mariallr/amanida
- **R** (Computing environment for executing log2 transformation and weighted meta-analysis functions)

## Examples

```
amanida_result <- compute_amanida(datafile, comp.inf = F)
# Access @stat table containing log2-transformed, study-size-weighted fold-change estimates
head(amanida_result@stat)
```

## Evaluation signals

- All log2-transformed fold-change values are numeric with symmetric distribution around 0 (negative for down-regulation, positive for up-regulation).
- Verify that log2(1) = 0 (no change), log2(2) ≈ 1.0 (2-fold up), log2(0.5) ≈ -1.0 (2-fold down).
- The final study-size-weighted average fold-change is accessible via @stat table in the amanida result object.
- Trend direction annotation (up-regulation, down-regulation, or no trend) is consistent with the sign and magnitude of the weighted log2-transformed fold-change.
- Volcano plot visualization shows log2(fold-change) on the x-axis with proper symmetry around zero.

## Limitations

- Log2 transformation assumes fold-change values are positive; negative values must be reciprocally transformed (1/value) before log2 application to avoid undefined logarithms.
- Fold-change values very close to 1 (e.g., 1.01) produce small log2 values; if many studies report minimal changes, the weighted average may be dominated by measurement noise rather than biological signal.
- Log2 transformation increases sensitivity to outlier fold-change values (e.g., extreme ratios > 100 or < 0.01); outlier detection or robust weighting schemes are not discussed in the article.
- The weighted averaging scheme assumes study size (N) is the appropriate weighting metric; alternative weighting by study variance or quality is not implemented in amanida.

## Evidence

- [other] Transform fold-changes using log2 logarithmic transformation. Compute study-size-weighted average of the transformed fold-changes.: "Transform fold-changes using log2 logarithmic transformation. 4. Compute study-size-weighted average of the transformed fold-changes."
- [readme] Fold-change combination: logarithmic transformation for average with weighting by number of participants.: "Fold-change combination: logarithmic transformation for average with weighting by number of participants."
- [intro] In metabolomics, the comparison between groups is disclosed using relative change rather than difference of means: "In metabolomics, the comparison between groups is disclosed using relative change rather than difference of means"
- [intro] negative values of fold-change are transformed to positive (1/value): "negative values of fold-change are transformed to positive (1/value)"
- [other] Execute compute_amanida function in R to generate the @stat results table, including trend direction (up-regulation, down-regulation, or no trend) and N_total (sum of study sizes across all contributing studies).: "Execute compute_amanida function in R to generate the @stat results table, including trend direction (up-regulation, down-regulation, or no trend)"
