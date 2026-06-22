---
name: intensity-threshold-noise-filtering
description: Use when you have loaded a raw or partially processed MsmsSpectrum object and need to reduce spectral noise before annotation, matching, or visualization. Use it especially when spectra contain many weak peaks (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# intensity-threshold-noise-filtering

## Summary

Remove low-intensity noise peaks from tandem mass spectra by applying intensity thresholds relative to the base peak intensity and optionally capping the total number of retained peaks. This preprocessing step improves signal-to-noise ratio and reduces computational burden in downstream spectrum matching and visualization.

## When to use

Apply this skill when you have loaded a raw or partially processed MsmsSpectrum object and need to reduce spectral noise before annotation, matching, or visualization. Use it especially when spectra contain many weak peaks (e.g., chemical noise, instrument artifacts) that may confound peptide fragmentation pattern matching or when memory/computational resources are constrained and you want to retain only the strongest signals.

## When NOT to use

- Spectra have already been filtered by a stricter downstream pipeline or quality control step; re-filtering with looser thresholds risks loss of valid diagnostic peaks.
- The analysis requires all detected peaks for spectral entropy, complexity metrics, or similarity scores that depend on full peak representation.
- Input is a processed feature table or quantification matrix rather than a raw spectrum object.

## Inputs

- MsmsSpectrum object with m/z and intensity arrays
- min_intensity threshold (float, 0.0–1.0, relative to base peak)
- max_num_peaks limit (int, peak count cap)

## Outputs

- MsmsSpectrum object with filtered m/z and intensity arrays
- Reduced peak count meeting both intensity and cardinality constraints

## How to apply

Load an MsmsSpectrum object (e.g., via Universal Spectrum Identifier from a public proteomics repository) and apply the filter_intensity() method with two key parameters: min_intensity (typically 0.05, representing the minimum intensity as a fraction of the base peak) and max_num_peaks (typically 50, capping the total number of peaks to retain). The method automatically removes all peaks below the min_intensity threshold; if the remaining peak count exceeds max_num_peaks, only the max_num_peaks strongest peaks are kept. This two-stage filtering balances noise removal with retention of diagnostic fragment ions, and is typically applied after m/z range restriction and precursor peak removal but before intensity scaling for normalization.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum class and the filter_intensity() method for intensity-based noise filtering) — https://github.com/bittremieux/spectrum_utils/

## Examples

```
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50)
```

## Evaluation signals

- The output spectrum's m/z and intensity arrays contain only peaks with intensity ≥ (min_intensity × base_peak_intensity).
- The number of peaks in the filtered spectrum does not exceed max_num_peaks.
- Peaks are sorted by m/z value and intensities are non-negative.
- The base peak (highest intensity) is always retained unless it exactly equals a filtered peak.
- Re-running the filter with identical parameters produces identical output (deterministic).

## Limitations

- Fixed relative thresholds (e.g., 0.05 of base peak) may be too lenient for low signal-to-noise spectra or too strict for high-quality data; instrument type and fragmentation method may require calibration.
- The filter is order-dependent when both min_intensity and max_num_peaks constraints are active: peaks are first thresholded, then capped by rank; this can yield different results than rank-first filtering.
- No adaptive or data-driven threshold optimization is provided; users must manually tune min_intensity and max_num_peaks based on empirical validation.
- Post-filter mass shifts or centroiding artifacts are not corrected; filtering assumes correctly calibrated m/z values.

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count.: "Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count."
- [other] Filter low-intensity noise peaks using .filter_intensity(min_intensity=0.05, max_num_peaks=50): ".filter_intensity(min_intensity=0.05, max_num_peaks=50)"
