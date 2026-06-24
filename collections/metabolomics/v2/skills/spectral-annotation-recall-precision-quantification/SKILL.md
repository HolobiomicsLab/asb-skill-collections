---
name: spectral-annotation-recall-precision-quantification
description: Use when you have run two or more annotation pipelines on the same MS/MS
  spectral dataset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - LipidIN Expeditious Querying (EQ) Module
  - LipidIN Lipid Categories Intelligence (LCI) Module
  - LipidIN Wide-spectrum Modeling Yield (WMY) Network
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

# spectral-annotation-recall-precision-quantification

## Summary

Quantify and compare the recall, precision, and coverage performance of lipid spectral annotation methods against baseline spectral-matching-only approaches. This skill enables rigorous evaluation of whether advanced annotation pipelines (e.g., regenerated fingerprints via neural networks) achieve claimed improvements in detecting and correctly identifying lipids from MS/MS spectra.

## When to use

Apply this skill when you have run two or more annotation pipelines on the same MS/MS spectral dataset (e.g., traditional spectral library matching vs. neural-network-enhanced regeneration) and need to quantify whether one pipeline recovers more true lipid identifications (higher recall), maintains accuracy (precision), or expands annotation breadth (coverage). Trigger: when comparing baseline annotations to those produced by the Wide-spectrum Modeling Yield (WMY) network or similar annotation enhancement methods.

## When NOT to use

- Input annotations are from a single method only (no baseline or enhanced comparator available).
- No reference ground truth or validated lipid identities exist for the spectra being evaluated.
- Spectral data lack MS/MS fragmentation information or are from fundamentally different ionization modes/lipid classes without separate validation stratification.

## Inputs

- mzML-formatted mass spectrometry data files
- baseline lipid annotations from spectral library matching (e.g., CSV with lipid names, m/z, retention time)
- enhanced/regenerated lipid annotations from WMY network or equivalent method (CSV with predicted lipids, confidence scores)
- reference ground truth or validated lipid assignments for the same spectra

## Outputs

- recall metric (fraction of true lipids detected by enhanced method)
- precision metric (fraction of predicted lipids that are true identifications)
- coverage metric (fraction of spectra with ≥1 annotation)
- estimated recall boost percentage: (recall_wmy − recall_baseline) / recall_baseline × 100%
- comparison table or CSV with per-spectrum and aggregate performance metrics

## How to apply

Load processed spectral data with initial annotations from spectral library matching (baseline). Apply the candidate annotation pipeline (e.g., WMY network) to regenerate or refine lipid fingerprints and produce enhanced predictions with confidence scores. For each spectrum, collect true/annotated lipid identities and compare predictions from both baseline and enhanced methods. Calculate recall as (true_positives_enhanced) / (all_true_lipids), precision as (true_positives_enhanced) / (all_predicted_lipids_enhanced), and coverage as the fraction of spectra with at least one annotation. Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of expected improvement thresholds (e.g., ~20% in the LipidIN case). Use consistent MS1 and MS2 m/z tolerances (e.g., 5 ppm and 10 ppm respectively) and filter thresholds (e.g., MS2 fragments >10% of max intensity) across both pipelines to ensure fair comparison.

## Related tools

- **XCMS** (Peak alignment, matching, and preprocessing of mass spectrometry data prior to spectral annotation comparison)
- **CAMERA** (Compound spectra extraction and annotation of MS data to support spectral querying baseline)
- **LipidIN Expeditious Querying (EQ) Module** (Baseline spectral library matching against 168.6 million lipid fragmentation hierarchical library) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN Lipid Categories Intelligence (LCI) Module** (Reduces false positive annotations using relative retention time rules and heuristic re-evaluation; supplies baseline FDR-filtered annotations) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN Wide-spectrum Modeling Yield (WMY) Network** (Enhanced annotation method that regenerates lipid fingerprints to improve coverage and recall; output predictions to compare against baseline) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
# After loading baseline EQ annotations and WMY-regenerated predictions:
recall_baseline <- sum(baseline_predictions$is_correct) / sum(!is.na(baseline_predictions$lipid))
recall_wmy <- sum(wmy_predictions$is_correct) / sum(!is.na(wmy_predictions$lipid))
recall_boost <- ((recall_wmy - recall_baseline) / recall_baseline) * 100
print(paste('Estimated recall boost:', round(recall_boost, 1), '%'))
```

## Evaluation signals

- Recall and precision values are between 0 and 1 (or 0–100%); coverage is also 0–100%.
- Recall boost is non-negative and aligns with reported threshold (e.g., ~20% for WMY); statistical significance (p-value) can be computed if multiple datasets are available.
- True positives, false positives, and false negatives sum correctly: TP + FN = total true lipids; TP + FP = total predicted lipids.
- Enhanced method recall ≥ baseline recall; precision should not degrade significantly, indicating genuine improvement rather than overprediction.
- Coverage increases or remains stable in enhanced method; no spectra should lose annotation unless FDR filtering was stricter.

## Limitations

- Recall and precision depend critically on the quality and completeness of the reference ground truth; if reference is partial or biased, metrics may be misleading.
- Comparison assumes both pipelines use identical MS1/MS2 tolerances and preprocessing filters; mismatched parameters invalidate direct comparison.
- LipidIN WMY network performance is instrument- and matrix-independent according to the README, but generalization to untrained lipid classes or ionization modes may degrade recall.
- The ~20% recall boost claimed in LipidIN is an estimated aggregate; per-lipid-class or per-sample variation is not quantified in the source documents.
- False discovery rate (FDR) is managed separately via the LCI module (5.7% estimated FDR over 8923 lipids); this may mask trade-offs between recall and precision in individual prediction steps.

## Evidence

- [other] Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics.: "Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics"
- [other] Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of ~20% improvement threshold.: "Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of ~20% improvement threshold"
- [intro] Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with a 20% estimated recall boosting: "Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with a 20% estimated recall boosting"
- [intro] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [readme] Using the model to generate reverse lipid fingerprint spectrograms, independent of sample matrices, instruments.: "Using the model to generate reverse lipid fingerprint spectrograms, independent of sample matrices, instruments"
