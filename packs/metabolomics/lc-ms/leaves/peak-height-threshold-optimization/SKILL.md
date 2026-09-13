---
name: peak-height-threshold-optimization
description: Use when you have raw metabolomic LC-MS data processed through XCMS CentWave
  feature extraction and want to improve true positive feature recovery while controlling
  false positive rate and crash likelihood.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Paramounter
  - XCMS CentWave
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c04758
  title: Paramounter
evidence_spans:
- github.com/HuanLab/Paramounter
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_paramounter_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c04758
  all_source_dois:
  - 10.1021/acs.analchem.1c04758
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-height-threshold-optimization

## Summary

Optimize XCMS CentWave peak-height detection thresholds to maximize true positive metabolomic features while managing false positive rate and software stability trade-offs. This skill uses Paramounter to compute an optimal peak-height value, then applies a mitigation multiplier to balance detection sensitivity against computational robustness.

## When to use

You have raw metabolomic LC-MS data processed through XCMS CentWave feature extraction and want to improve true positive feature recovery while controlling false positive rate and crash likelihood. This skill is especially relevant when you observe either too few detected features (suggesting the peak-height threshold is too high) or an unacceptable false positive burden and extraction instability (suggesting the threshold is too low after optimization).

## When NOT to use

- Input is already a curated, validated feature table; re-optimization may introduce unnecessary noise and invalidate prior QA decisions.
- The analysis goal is to minimize computational cost or runtime; 2× threshold multiplication requires a second full feature extraction pass.
- Peak-height threshold has been manually fixed by experimental protocol or regulatory requirement; optimization assumes threshold is a tunable hyperparameter.

## Inputs

- Raw metabolomic LC-MS data (mzML or NetCDF format)
- XCMS CentWave feature extraction results (initial feature table)
- Paramounter optimization configuration

## Outputs

- Optimized peak-height threshold value
- Feature table extracted at optimized peak-height threshold
- 2×-mitigated feature table (threshold × 2)
- Comparative summary statistics (true positives, false positives, extraction stability metrics)

## How to apply

Load raw metabolomic data and run XCMS CentWave feature extraction with initial parameters. Use Paramounter to compute the optimized peak-height threshold that maximizes the count of true positive features. Apply this optimized threshold to extract an initial feature set, then multiply the threshold by 2× as a mitigation factor to reduce false positives and crash likelihood. Re-extract features using the 2×-elevated threshold and compare the false positive rate, true positive retention, and extraction stability against the non-mitigated result. Document both feature tables (optimized and 2×-mitigated) with summary statistics to inform downstream method choice based on your prioritization of sensitivity versus specificity and computational reliability.

## Related tools

- **XCMS CentWave** (Performs initial centroid-based peak detection and feature extraction from raw LC-MS data; output serves as input to peak-height threshold optimization)
- **Paramounter** (Computes the optimized peak-height threshold that maximizes true positive feature count; outputs the threshold value to be multiplied and applied) — https://github.com/HuanLab/Paramounter

## Evaluation signals

- Optimized peak-height threshold is lower than the 2×-mitigated threshold, confirming the multiplier was correctly applied.
- 2×-mitigated feature table shows reduced false positive count and lower crash/error rate compared to optimized-only extraction, demonstrating stability gain.
- True positive feature count in 2×-mitigated table is within acceptable retention (e.g., ≥80% of optimized count), confirming that mitigation did not eliminate genuine signals.
- Feature dereplication (mzdiff) is consistently applied across both thresholds; verify that features with mass differences below the mzdiff tolerance are treated identically in both outputs.
- Summary statistics report includes the same true positive ground-truth reference set for both conditions, enabling paired comparison of sensitivity and specificity metrics.

## Limitations

- Paramounter's optimized peak-height may increase false positive rate and software crash likelihood; the 2× mitigation is a heuristic and may not be optimal for all datasets.
- True positive metabolic features with mass differences smaller than the mzdiff tolerance value (default 0.001 or 0.01) may be removed by mistake during dereplication, independently of peak-height optimization; mzdiff should be set to a negative value to disable dereplication if this is a concern.
- The skill assumes XCMS CentWave is the feature extraction method; results may not transfer to other peak-picking algorithms or vendor-specific preprocessing.
- No changelog available for Paramounter; version pinning and reproducibility may be challenging across environments.

## Evidence

- [other] Paramounter tunes an optimized peak height to maximize true positive features, but users can mitigate the resulting higher false positive rate and crash likelihood by applying a higher peak height threshold, such as 2X the optimized peak height threshold.: "Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features and the likelihood of"
- [readme] mzdiff is used as the mass tolerance to dereplicate features extracted by XCMS CentWave, with suggested default values of 0.001 or 0.01.: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave. Suggested default value: 0.001 or 0.01."
- [readme] True positive metabolic features with mass differences smaller than the mzdiff tolerance may be removed by mistake during dereplication.: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
- [readme] Dereplication can be disabled by setting mzdiff to any negative value.: "if a user wants to disable the dereplication function, set the mzdiff to be any negative value"
