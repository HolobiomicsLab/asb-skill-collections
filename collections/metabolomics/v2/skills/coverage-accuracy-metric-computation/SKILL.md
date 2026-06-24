---
name: coverage-accuracy-metric-computation
description: Use when you have two sets of lipid annotations—one from baseline spectral
  library matching and one from an enhanced method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0188
  - http://edamontology.org/topic_3370
  tools:
  - XCMS
  - CAMERA
  - LipidIN Wide-spectrum Modeling Yield (WMY) network
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# coverage-accuracy-metric-computation

## Summary

Compute recall, precision, and coverage metrics to quantify the performance improvement of lipid annotation methods against baseline spectral-matching approaches. This skill measures whether enhanced annotation workflows achieve target performance gains (e.g., ~20% recall boost) by comparing predicted lipid fingerprints against ground-truth annotations.

## When to use

Apply this skill when you have two sets of lipid annotations—one from baseline spectral library matching and one from an enhanced method (e.g., Wide-spectrum Modeling Yield network)—and need to rigorously quantify whether the enhanced method delivers the claimed improvement in annotation recall, precision, or coverage across a lipid dataset.

## When NOT to use

- Input lacks ground truth labels or reference annotations—metric computation requires known correct answers.
- Only a single annotation method is available; this skill requires paired baseline and enhanced annotations for comparative quantification.
- Annotations are already aggregated or de-identified such that individual lipid identities cannot be traced back to predictions.

## Inputs

- Baseline lipid annotations from spectral library matching (CSV or RDA format)
- Enhanced lipid annotations with confidence scores from regenerated fingerprint method
- Ground truth or reference lipid annotations
- MS/MS spectral data with initial annotations

## Outputs

- Recall metric (TP / (TP + FN)) for each method
- Precision metric (TP / (TP + FP)) for each method
- Coverage metric (% of lipids with assigned annotations)
- Estimated recall boost percentage: (recall_enhanced − recall_baseline) / recall_baseline × 100%
- Comparison table (baseline vs. enhanced method metrics)

## How to apply

Load both the baseline annotations (from spectral-matching-only) and the enhanced annotations (from the regenerated fingerprint method). For each lipid candidate, check whether it appears in the ground truth and record true positives, false positives, false negatives, and true negatives. Calculate recall as TP / (TP + FN), precision as TP / (TP + FP), and coverage as the percentage of lipids with assigned annotations. Then compute the estimated recall boost as (recall_enhanced − recall_baseline) / recall_baseline × 100%. Verify that the boost meets or exceeds the reported threshold (~20% for WMY network). Document confidence scores assigned to each prediction to enable threshold sensitivity analysis.

## Related tools

- **XCMS** (Process mass spectrometry data and generate initial spectral-library-matched annotations that serve as the baseline for metric comparison)
- **CAMERA** (Refine spectral annotation and improve peak detection in MS/MS data used to compute baseline metrics)
- **LipidIN Wide-spectrum Modeling Yield (WMY) network** (Generate enhanced lipid fingerprint predictions with confidence scores to be compared against baseline using this skill) — https://github.com/LinShuhaiLAB/LipidIN

## Evaluation signals

- Recall values are in [0, 1] range and enhanced method recall ≥ baseline recall.
- Precision values are in [0, 1] range and sum of TP, FP, FN, TN equals total lipid candidates.
- Estimated recall boost is non-negative and ≥ ~20% when comparing WMY-regenerated fingerprints against baseline.
- Coverage metric reports the percentage of input lipids with non-null annotations (should be transparent about missing predictions).
- Confidence score distributions for TP vs. FP predictions show separation, validating ranking quality of enhanced method.

## Limitations

- Ground truth annotations may be incomplete or contain errors, biasing metric estimates.
- Recall and precision are sensitive to the choice of confidence score threshold; report results across multiple thresholds to characterize performance sensitivity.
- Coverage metric depends on input lipid diversity; performance may vary across lipid classes or chain compositions not well-represented in training data.
- Cross-sample or cross-instrument variability is not captured by aggregate metrics; stratified metric computation by sample or instrument type is recommended.

## Evidence

- [other] Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost in lipid annotation coverage and accuracy?: "Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost"
- [other] Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics.: "Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics"
- [other] Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of ~20% improvement threshold.: "Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of ~20% improvement threshold"
- [readme] Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with 20% estimated recall boosting: "Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with 20% estimated recall boosting"
