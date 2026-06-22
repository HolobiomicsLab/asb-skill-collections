---
name: run-order-dependency-modeling
description: Use when your feature table includes QC (quality control) sample replicates distributed throughout the analytical run sequence, and you observe systematic intensity variation correlated with sample injection order or batch identifier—typical indicators of instrumental drift in untargeted LC-MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MetCorR
  - R
  - OUKS
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- New QC-GAM method (MetCorR) with associated scripts were introduced.
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# run-order-dependency-modeling

## Summary

Model and correct run-order-dependent signal drift in LC-MS metabolomic feature tables using Generalized Additive Models (GAM) fitted to QC sample intensities across the analytical sequence. This skill applies the MetCorR QC-GAM method to estimate correction factors that account for instrument drift and batch effects that vary systematically with sample injection order.

## When to use

Your feature table includes QC (quality control) sample replicates distributed throughout the analytical run sequence, and you observe systematic intensity variation correlated with sample injection order or batch identifier—typical indicators of instrumental drift in untargeted LC-MS metabolomics. Apply this skill before statistical hypothesis testing to remove technical variation that could mask or confound biological signals.

## When NOT to use

- Feature table has fewer than ~5–10 QC replicates distributed across the run; GAM fitting requires sufficient reference points to estimate smooth drift trends reliably.
- QC samples are clustered at run start/end only; scattered QC placement throughout the sequence is needed to capture run-order dependency.
- Input data are already batch-corrected or normalized by other means (e.g., ComBat, quantile normalization); applying MetCorR QC-GAM after such corrections may introduce artifacts or redundant adjustment.

## Inputs

- Feature intensity matrix (samples × features, numeric; QC and analytical samples)
- Run order vector (integer sequence indicating injection order for each sample)
- Sample class/group vector with QC sample label (e.g., 'QC' string identifier)
- Batch identifier vector (if multi-batch correction desired; optional)

## Outputs

- Corrected feature intensity matrix (same dimensions as input, drift-adjusted)
- GAM model object (contains fitted smoothing terms and correction coefficients)
- Correction factor predictions (per-feature, per-sample abundance adjustments)

## How to apply

Load the feature intensity table (samples × features) alongside metadata specifying run order (injection sequence position) and QC sample labels. Fit a Generalized Additive Model using QC samples as reference points, with run order (and optionally batch) as smoothing terms via spline basis functions to capture nonlinear drift patterns. The GAM estimates correction factors—multiplicative offsets per feature per run position—by modeling how QC feature intensities deviate from a smoothed trend. Apply the fitted correction factors to all samples (QC and analytical) to produce a corrected feature table. Use method=2 (run order + batch) if multiple analytical batches are present; method=1 (run order only) if a single batch. Validate correction by confirming that RLA (Relative Log Abundance) plots and correlogram heatmaps show reduced within-batch variance post-correction.

## Related tools

- **MetCorR** (R package implementing the QC-GAM correction method; fits and applies run-order-dependent drift correction to feature tables) — github.com/plyush1993/MetCorR
- **R** (Statistical computing environment for executing MetCorR scripts and GAM model fitting (≥4.1.2 required)) — https://cran.r-project.org/index.html
- **OUKS** (Broader R-based metabolomics workflow; integrates MetCorR as step 4 (Correction) in nine-step LC-MS processing pipeline) — github.com/plyush1993/OUKS

## Examples

```
library(MetCorR); data(example_intensity, package = "MetCorR"); data(example_meta, package = "MetCorR"); out <- MetCorR(method = 2, int_data = example_intensity, order = example_meta$order, class = example_meta$class, batch = example_meta$batch, qc_label = "QC")
```

## Evaluation signals

- RLA (Relative Log Abundance) plots for QC samples before/after correction: post-correction RLA should cluster tightly around zero across all run positions, indicating removal of run-order drift.
- Feature-wise correlation heatmaps: within-batch correlation structure should improve (higher correlations among QC replicates) post-correction; visual inspection of reduced horizontal/vertical banding artifacts.
- D-Ratio metric (technical variance / biological variance): should decrease after correction, confirming reduction of technical signal drift relative to biological variation.
- Spline smoothness visualization: inspect fitted GAM curves for each feature to confirm smooth, monotonic or unimodal drift trends (not overfitting noise); degrees of freedom should be reasonable (e.g., 2–5 per smooth term).
- Preservation of sample ranks: corrected intensities should preserve the relative ordering of analytical samples (no sign flips or rank reversals of feature abundances for biological samples).

## Limitations

- Requires QC samples embedded throughout the run; sparse or terminal-only QC placement compromises drift estimation, especially at run extremes.
- GAM smoothness parameter (basis dimension, knot placement) selection is not extensively documented; over-smoothing can mask real biological variation, while under-smoothing may preserve instrumental artifacts.
- Method assumes that QC sample composition is representative of analytical samples' chemical space; if QC and samples differ drastically in ionization efficiency or metabolite classes, correction may be ineffective or introduce bias.
- No explicit handling of missing values (NAs) in feature table; imputation or removal of missing features should precede MetCorR application.
- Multi-batch correction (method=2) requires batch identifiers; if batch assignments are incorrect or unknown, correction may fail or worsen batch confounding.

## Evidence

- [other] models batch-dependent signal drift using QC samples as reference points and applies Generalized Additive Models (GAM) to estimate run-order-dependent correction factors: "models batch-dependent signal drift using QC samples as reference points and applies Generalized Additive Models (GAM) to estimate run-order-dependent correction factors"
- [other] Does the MetCorR QC-GAM correction method successfully produce a corrected feature table when applied to QC-annotated metabolomic data?: "Does the MetCorR QC-GAM correction method successfully produce a corrected feature table when applied to QC-annotated metabolomic data?"
- [other] Execute the MetCorR QC-GAM correction algorithm via the MetCorR package, which models batch-dependent signal drift using QC samples as reference points: "Execute the MetCorR QC-GAM correction algorithm via the MetCorR package, which models batch-dependent signal drift using QC samples as reference points"
- [readme] Method 2 has been selected Used formula: y ~ s(order, batch) Fitting GAMs on QC samples... Predicting for all samples...: "Method 2 has been selected Used formula: y ~ s(order, batch) Fitting GAMs on QC samples... Predicting for all samples..."
- [other] New QC-GAM method (MetCorR) with associated scripts were introduced: "New QC-GAM method (MetCorR) with associated scripts were introduced"
- [other] Apply the fitted correction factors to all feature abundances across the entire table. 4. Output the corrected feature table in CSV or tabular format: "Apply the fitted correction factors to all feature abundances across the entire table. 4. Output the corrected feature table in CSV or tabular format"
