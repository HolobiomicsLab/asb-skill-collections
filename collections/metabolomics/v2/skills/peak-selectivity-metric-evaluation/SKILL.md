---
name: peak-selectivity-metric-evaluation
description: Use when when identifying landmark peaks for retention time alignment
  in multi-sample LC-MS metabolomics workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - scipy
  - scipy.signal.find_peaks
  - asari (peaks.quick_detect_unique_elution_peak)
  - asari (CompositeMap.calibrate_sample_RT)
  - asari (constructors.set_RT_reference)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- scipy.signal module for LOWESS fitting via the regression function
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-selectivity-metric-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate and filter LC-MS peaks based on selectivity metrics to identify high-confidence landmark peaks suitable for retention time (RT) alignment and mass calibration. Peak selectivity (threshold m/z selectivity > 0.99) prioritizes peaks with minimal mass overlap across samples, enabling robust alignment functions.

## When to use

When identifying landmark peaks for retention time alignment in multi-sample LC-MS metabolomics workflows. Apply this skill after mass track extraction but before LOWESS regression calibration, especially when you need to ensure that RT correction relies only on peaks with high confidence in mass identity (low contamination from co-eluting ions at nearby m/z values).

## When NOT to use

- Peak selectivity filtering assumes high mass resolution (e.g., Orbitrap) where m/z separation is achievable; applying to low-resolution data (quadrupole, time-of-flight < 50k resolution) may eliminate too many peaks.
- If your goal is feature detection on a single sample in isolation (not multi-sample alignment), selectivity-based filtering may be unnecessarily stringent.
- If peaks have already been validated by orthogonal methods (e.g., MS/MS annotation or standards) or are from a targeted assay with known identities, filtering by mass selectivity alone may be redundant.

## Inputs

- mass tracks (EICs) with intensity arrays indexed by scan number
- reference sample designation or composite map with mass grid
- peak candidates with m/z, retention time, and intensity values
- parameters: mSelectivity threshold, min_peak_height, prominence threshold

## Outputs

- subset of peaks passing selectivity criteria (high-selectivity landmark peaks)
- annotation of each peak with mSelectivity value and pass/fail status
- list of (sample_RT, reference_RT) pairs from good landmark peaks, ready for LOWESS fitting

## How to apply

For each mass track candidate, calculate selectivity as the ratio of peak intensity at the exact m/z to total intensity in a mass window around that m/z. Filter peaks using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5 for Orbitrap), prominence > 20% of peak height, and exactly one peak per mass track per sample. Restrict evaluation to the reference sample first (constructors.set_RT_reference), then apply the same criteria to current samples but only on mass tracks already aligned to reference landmarks (CompositeMap.calibrate_sample_RT). This two-stage approach ensures that only high-fidelity peaks enter the LOWESS regression, preventing RT misalignment caused by mass ambiguity.

## Related tools

- **scipy.signal.find_peaks** (Detects local maxima in mass tracks to identify peak candidates before selectivity evaluation) — https://scipy.org
- **asari (peaks.quick_detect_unique_elution_peak)** (Implements reference sample landmark peak selection with selectivity and prominence constraints) — https://github.com/shuzhao-li/asari
- **asari (CompositeMap.calibrate_sample_RT)** (Applies selectivity filtering to current sample peaks restricted to pre-aligned mass tracks) — https://github.com/shuzhao-li/asari
- **asari (constructors.set_RT_reference)** (Identifies and stores high-selectivity landmark peaks from reference sample for downstream alignment) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.constructors import set_RT_reference; from asari.peaks import quick_detect_unique_elution_peak; landmark_peaks = quick_detect_unique_elution_peak(composite_map, selectivity_threshold=0.99, min_peak_height=1e5, prominence_ratio=0.2)
```

## Evaluation signals

- Verified: at least 10–50 landmark peaks per sample pass selectivity criteria (fewer may indicate too-stringent threshold or poor data quality); document the count in audit log
- Verified: mSelectivity values for retained peaks are consistently > 0.99; peaks below this threshold are rejected
- Verified: peak prominence (ratio of peak height to surrounding baseline) exceeds 20% of peak height; this ensures peaks are morphologically distinct from noise
- Verified: RT alignment function (LOWESS) fitted on landmark peaks has residuals (sample_RT_predicted − sample_RT_observed) with median absolute error < 0.2 scans; large errors suggest low-quality landmarks
- Verified: each mass track in reference sample yields exactly one landmark peak; multiple peaks per track indicate co-elution or data artifacts

## Limitations

- Selectivity threshold (0.99) is empirically tuned for Orbitrap mass spectrometry; lower-resolution instruments may require relaxed thresholds (e.g., 0.95), or may have insufficient selectivity for reliable RT alignment.
- Peak prominence criterion (> 20% of peak height) assumes Gaussian-like peak shapes; very broad or asymmetric peaks may fail this test despite being genuine metabolites.
- Requires a stable reference sample (high SNR, broad metabolite coverage); if reference sample is degraded or has atypical ion suppression, landmark peak selection will propagate errors to all downstream samples.
- Does not account for sample-specific effects (matrix suppression, instrument drift within run); peaks passing selectivity in reference may still have altered selectivity in other samples due to co-eluting contaminants unique to that sample.
- Assumes mass tracks are already extracted and roughly co-registered across samples; peaks in mass tracks with poor alignment will have low selectivity and be excluded, leading to sparse landmark sets.

## Evidence

- [other] Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per mass track: "Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per"
- [other] Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks: "Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks (see"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [intro] Peak quality and selectivity metrics can be tracked on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
