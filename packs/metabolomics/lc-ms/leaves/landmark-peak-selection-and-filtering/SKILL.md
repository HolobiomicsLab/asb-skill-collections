---
name: landmark-peak-selection-and-filtering
description: Use when when preparing mass tracks for retention-time (RT) alignment across multiple LC-MS samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - scipy
  - scipy.signal.find_peaks
  - asari.peaks.quick_detect_unique_elution_peak
  - asari.constructors.set_RT_reference
  - asari.CompositeMap.calibrate_sample_RT
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
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

# landmark-peak-selection-and-filtering

## Summary

Selection and filtering of high-selectivity landmark peaks from reference and sample mass tracks to enable robust retention-time alignment via LOWESS regression. Landmark peaks serve as anchoring points for calibrating RT relationships between LC-MS samples.

## When to use

When preparing mass tracks for retention-time (RT) alignment across multiple LC-MS samples. This skill is triggered after mass track construction but before LOWESS regression fitting: you have a reference sample with its mass tracks and a current sample whose RT needs calibration against the reference. The goal is to identify reproducible, selective peaks that reliably correspond between samples.

## When NOT to use

- Input mass tracks have not yet been aligned across samples by m/z (no MassGrid available)—apply mass separation and alignment first.
- Peak detection has not been performed on the mass tracks—run peak detection with prominence and local-maxima criteria before landmark filtering.
- Sample has very few peaks or low signal-to-noise ratio—landmark selection will fail if there are fewer than ~10 high-selectivity peaks available.

## Inputs

- reference sample mass tracks (list of chromatographic intensity vectors indexed by m/z)
- current sample mass tracks (list of chromatographic intensity vectors indexed by m/z)
- pre-computed mass alignment mapping (MassGrid: m/z-based correspondence between reference and sample)
- peak detection results on each mass track (peak position, height, prominence)

## Outputs

- reference landmark peaks (filtered list: scan number, m/z, peak height, selectivity metrics)
- sample landmark peaks (filtered list: scan number, m/z, peak height, selectivity metrics)
- landmark peak pairs (paired reference and sample scan numbers ready for LOWESS fitting)

## How to apply

Identify high-selectivity landmark peaks in the reference sample by filtering mass tracks on three selectivity criteria: m/z selectivity > 0.99 (single dominant ion), peak prominence > 20% of peak height, and minimum peak height (default 1e5 for Orbitrap). Enforce single-peak-per-mass-track rule to eliminate ambiguous elutions. For the current sample, apply identical selectivity thresholds but restrict the search to mass tracks already aligned to reference landmarks (i.e., pre-filtered by mass grid alignment). This two-stage filtering—stringent on reference, then constrained on sample—ensures only highly confident landmark pairs enter the LOWESS regression. The rationale is that high selectivity reduces false-positive matches and noise-driven distortions in the fitted RT function.

## Related tools

- **scipy.signal.find_peaks** (locates local maxima on mass tracks; output feeds peak height and prominence computation for selectivity filtering)
- **asari.peaks.quick_detect_unique_elution_peak** (identifies and filters single, prominent peaks per mass track to enforce selectivity criterion and one-peak-per-track rule) — https://github.com/shuzhao-li/asari
- **asari.constructors.set_RT_reference** (constructs reference landmark peak set from reference sample mass tracks using selectivity thresholds) — https://github.com/shuzhao-li/asari
- **asari.CompositeMap.calibrate_sample_RT** (filters sample landmark peaks by restricting search to mass tracks already aligned to reference landmarks; applies same selectivity criteria) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.constructors import set_RT_reference; from asari.peaks import quick_detect_unique_elution_peak; ref_landmarks = set_RT_reference(ref_sample_mass_tracks, mSelectivity_min=0.99, min_peak_height=1e5); sample_landmarks = [quick_detect_unique_elution_peak(mt) for mt in sample_mass_tracks if mt.mz in ref_mz_set]
```

## Evaluation signals

- Reference landmark peaks satisfy all three selectivity criteria: mSelectivity > 0.99, peak_height ≥ min_peak_height (default 1e5), prominence > 20% of peak height.
- Sample landmark peaks are a strict subset of mass tracks that appear in the reference MassGrid (100% of sample landmarks have corresponding reference mass tracks).
- Landmark peak pairs are symmetric: every reference landmark has exactly one paired sample landmark, and vice versa (1:1 correspondence).
- Number of landmark pairs is sufficient for stable LOWESS fitting (>= 10 pairs recommended; if < 5, RT alignment will be unreliable).
- Landmark scan numbers cluster near the bulk of sample elution (not at chromatogram edges), indicating selectivity did not bias toward outliers or noise spikes.

## Limitations

- If reference and sample share few high-selectivity peaks (e.g., due to technical variation, different ionization efficiency, or sample degradation), landmark selection may yield too few pairs for stable LOWESS fitting.
- The selectivity thresholds (mSelectivity > 0.99, prominence > 20%, height ≥ 1e5) are tuned for Orbitrap-class high-resolution instruments; lower-resolution MS or different ionization modes may require re-tuning.
- Single-peak-per-mass-track rule eliminates co-eluting isomers or isobars; if a mass track contains two genuine, resolvable peaks, only the most prominent one becomes a landmark.
- Mass grid alignment errors upstream propagate: if the reference-to-sample m/z correspondence is incorrect, sample landmark selection will filter out true landmarks and include false ones.

## Evidence

- [other] Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per mass track: "Identify high-selectivity landmark peaks in the reference sample using criteria: mSelectivity > 0.99, min_peak_height satisfied (default 1e5), prominence > 20% of peak height, and single peak per"
- [other] Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks: "Select good landmark peaks from the current sample by applying the same selectivity criteria, but restricted to mass tracks already aligned to the reference landmarks (see"
- [intro] Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing: "Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing"
- [intro] Peak detection should be performed on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control: "Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control"
