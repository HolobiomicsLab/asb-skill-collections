---
name: false-positive-mitigation-tuning
description: Use when after running Paramounter's peak-height optimization on XCMS
  CentWave-extracted metabolomic features, if the downstream analysis or feature validation
  reveals an unacceptable rate of false positives, or if the extraction workflow is
  experiencing software crashes or timeout failures due to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Paramounter
  - XCMS CentWave
  techniques:
  - LC-MS
  license_tier: open
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

# False-positive-mitigation-tuning

## Summary

A post-optimization tuning strategy that mitigates the false positive rate and crash likelihood introduced by Paramounter's peak-height optimization in metabolomic feature extraction. By applying a multiplicative threshold adjustment (typically 2×) to the optimized peak-height value, practitioners trade some true positive sensitivity for substantially reduced false positives and improved software stability.

## When to use

After running Paramounter's peak-height optimization on XCMS CentWave-extracted metabolomic features, if the downstream analysis or feature validation reveals an unacceptable rate of false positives, or if the extraction workflow is experiencing software crashes or timeout failures due to the aggressive optimized threshold.

## When NOT to use

- Input feature table is already deduplicated and validated; no re-extraction is needed.
- Analysis goal prioritizes sensitivity over specificity and false positives are already acceptable or lower-priority than missing true signals.
- Raw metabolomic data is unavailable or the original XCMS CentWave run cannot be reproduced with modified parameters.

## Inputs

- Raw metabolomic data (mzML or NetCDF format)
- Paramounter-computed optimized peak-height threshold (numeric scalar)
- XCMS CentWave initial parameter set

## Outputs

- Feature table extracted with mitigated (elevated) peak-height threshold
- Feature table extracted with optimized (non-mitigated) peak-height threshold
- Comparison summary: true positive count, false positive count, extraction stability metrics for both thresholds

## How to apply

Starting from the optimized peak-height threshold computed by Paramounter (which maximizes true positive count), multiply it by a mitigation factor—typically 2×—to obtain an elevated threshold. Re-run feature extraction using XCMS CentWave with this elevated threshold instead of the optimized value. This reduces the computational burden and false positive rate at the cost of missing some marginal true positives. Compare the resulting feature table (elevated threshold) against the non-mitigated result using summary statistics: count of true positives, false positives, and extraction stability (crash rate or runtime). Document both results to enable downstream validation of whether the false positive reduction justifies the true positive loss for your specific biological question.

## Related tools

- **Paramounter** (Computes optimized peak-height threshold that maximizes true positive features; mitigation tuning multiplies this threshold by user-defined factor (e.g., 2×) to reduce false positives and crashes.) — github.com/HuanLab/Paramounter
- **XCMS CentWave** (Performs feature extraction and dereplication on raw metabolomic data using mass tolerance (mzdiff) and peak-height threshold; re-run with mitigated threshold to produce alternative feature set.)

## Evaluation signals

- False positive count in the mitigated (2×-threshold) feature table is strictly lower than in the optimized feature table.
- True positive count in the mitigated feature table is lower than the optimized set but remains above a domain-acceptable minimum (validation against independent standard or literature).
- Extraction stability: mitigated run completes without crashes or timeouts; optimized run may show crash frequency > 0.
- Feature dereplication statistics (mzdiff filtering behavior) remain consistent between runs; only peak-height threshold varies.
- Summary statistics (e.g., feature count, mass range, retention time distribution) for true positives in mitigated set differ by a predictable, quantifiable amount from optimized set.

## Limitations

- The 2× mitigation factor is a heuristic; optimal multiplier varies by dataset, instrument, and biology and must be determined empirically.
- Mitigation trades true positive sensitivity for false positive reduction; there is no guarantee that the lost true positives are not biologically relevant for the research question.
- Dereplication at low mzdiff values (< 0.001 m/z) may still remove true positives even with elevated peak-height thresholds; users can disable dereplication by setting mzdiff to a negative value.
- No automated mechanism to select the optimal mitigation factor; practitioners must manually compare outputs and validate against orthogonal evidence (e.g., standards, MS/MS confirmation).

## Evidence

- [readme] Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features and the likelihood of software crash.: "Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features and the likelihood of"
- [readme] users can try a higher peak height threshold to reduce the number of false positive features (e.g., 2X the optimized peak height threshold).: "users can try a higher peak height threshold to reduce the number of false positive features (e.g., 2X the optimized peak height threshold)"
- [readme] mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave.: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave"
- [readme] some true positive metabolic features with mass differences smaller than that value may be removed by mistake.: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
