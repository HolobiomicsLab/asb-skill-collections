---
name: rsd-threshold-parameter-optimization
description: Use when when preparing XCMS peak tables for quality classification and
  you observe that the default RSD threshold (0.3 or 30%) is either too permissive
  (retaining noisy EICs) or too stringent (discarding valid signals).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MetaClean
  - XCMS
  - caret
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- getEvalObj is called to extract the relevant data from the three objects provided
  by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
- MetaClean is a package for building classifiers to identify low quality integrations
  in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package
  `caret`) for building a predictive model.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# RSD Threshold Parameter Optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize the relative standard deviation (RSD) percentage threshold used by MetaClean's rsdFilter() function to selectively remove low-quality extracted ion chromatograms (EICs) prior to peak quality metric calculation and classifier training. This parameter controls the stringency of quality control sample variability filtering in untargeted LC-MS metabolomics pipelines.

## When to use

When preparing XCMS peak tables for quality classification and you observe that the default RSD threshold (0.3 or 30%) is either too permissive (retaining noisy EICs) or too stringent (discarding valid signals). Optimization is warranted when QC sample replicates show systematic variability patterns or when downstream classifier performance is suboptimal due to inclusion/exclusion of borderline-quality EICs.

## When NOT to use

- Input is already a curated feature table or the RSD threshold has been pre-determined by study protocol or published method — skip optimization and apply the fixed threshold directly.
- QC sample replicates are not available or insufficient (<3 replicates) — RSD estimation becomes unreliable and threshold optimization is not meaningful.
- The goal is exploratory data visualization rather than classifier training — RSD filtering may obscure weak but genuine signals and is not necessary for initial QC assessment.

## Inputs

- XCMS peakTable output (data.frame with m/z, retention time, and peak intensity values across samples)
- Covariate file or sample metadata (to identify QC sample column names with SampleType='LQC')
- Candidate RSD threshold values (numeric vector, e.g., seq(0.2, 0.5, by=0.1))
- Reference dataset or ground truth peak quality labels (for cross-validation evaluation)

## Outputs

- Filtered peak table containing only EICs with RSD ≤ optimized threshold
- Comparison table of classifier evaluation measures (sensitivity, specificity, balanced accuracy) for each threshold tested
- Optimal RSD threshold value and associated filtering statistics (count of retained/filtered EICs)

## How to apply

Begin by calculating RSD values across quality control (QC) sample replicates (identified from covariate file where SampleType='LQC') for all EICs in the XCMS peak table. Invoke rsdFilter() iteratively with candidate thresholds (e.g., 0.2, 0.3, 0.4, 0.5) and examine the number of retained vs. filtered EICs at each level. For each threshold configuration, train the MetaClean classifier (using getPeakQualityMetrics followed by runCrossValidation) and compare evaluation measures (sensitivity, specificity, balanced accuracy) to identify the threshold that maximizes classifier performance without excessive data loss. The optimal threshold balances QC sample reproducibility requirements with retention of sufficient training signal; domain knowledge about your LC-MS platform's typical RSD variability should inform the search range.

## Related tools

- **MetaClean** (Provides rsdFilter() function to filter EICs by RSD threshold and subsequent classifier training functions (getPeakQualityMetrics, runCrossValidation, getEvaluationMeasures) to evaluate threshold performance) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Pre-processing software that produces peakTable output containing EIC intensity values across samples; MetaClean is designed for integration with XCMS workflows)
- **R** (Programming language in which MetaClean and rsdFilter() are implemented; used for threshold iteration, RSD calculation, and classifier evaluation)
- **caret** (R package underlying the 8 classification algorithms used by MetaClean's runCrossValidation for cross-validation training at each threshold level)

## Examples

```
rsdFilter(peakTable = xcms_peaks, eicCol = 'EICNo', qcSampleNames = c('LQC_1', 'LQC_2', 'LQC_3'), rsdThreshold = 0.3)
```

## Evaluation signals

- For each tested threshold: all retained EICs have RSD ≤ threshold and all filtered-out EICs have RSD > threshold (correctness of filtering logic).
- Classifier evaluation measures (sensitivity, specificity, balanced accuracy, AUC) show a peak or plateau at the optimal threshold; performance degrades noticeably at more permissive or more stringent thresholds (monotonic trend indicating true optimization, not random variation).
- The count of retained EICs decreases monotonically as threshold decreases; at the optimal threshold, data loss is <20–30% (typical for quality filtering) relative to unfiltered peak table.
- Cross-validation folds or test set predictions are stable across the optimal threshold range (±0.05), indicating robustness of the choice.
- Post-optimization classifier (trained on filtered peak table with optimal threshold) achieves higher sensitivity/specificity on held-out test set compared to classifiers trained with default threshold or no filtering.

## Limitations

- RSD filtering assumes QC samples are representative of biological sample variability; if QC samples differ systematically in composition or ionization efficiency, RSD thresholds may not generalize.
- Threshold optimization requires sufficient QC replicates (typically ≥3) and a labeled reference dataset; absent these, optimization becomes a heuristic exercise without ground truth validation.
- The relationship between RSD threshold and downstream classifier performance is data- and platform-dependent; optimal thresholds are not transferable across different LC-MS instruments, ionization methods, or metabolite panels without re-optimization.
- Aggressive RSD filtering (low thresholds) may remove genuine low-abundance or biologically relevant analytes that happen to show high QC variability due to matrix effects or instrumental drift rather than poor peak integration.

## Evidence

- [methods] the user can optionally filter out EICs by RSD % using the rsdFilter() function.: "the user can optionally filter out EICs by RSD % using the rsdFilter() function."
- [other] Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3).: "Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3)."
- [other] Confirm that all retained EICs have RSD ≤ threshold and that all filtered-out EICs have RSD > threshold.: "Confirm that all retained EICs have RSD ≤ threshold and that all filtered-out EICs have RSD > threshold."
- [other] removes extracted ion chromatograms (EICs) based on a relative standard deviation (RSD) percentage threshold specified by the user prior to subsequent peak quality metric calculation and classifier training.: "removes extracted ion chromatograms (EICs) based on a relative standard deviation (RSD) percentage threshold specified by the user prior to subsequent peak quality metric calculation and classifier"
- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data.: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
