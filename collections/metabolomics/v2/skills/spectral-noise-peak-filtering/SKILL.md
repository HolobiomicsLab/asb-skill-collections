---
name: spectral-noise-peak-filtering
description: Use when when working with raw or partially processed tandem mass spectrometry
  (MS/MS) spectra that contain low-intensity background noise peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - NumPy
  - Numba
  - spectrum_utils
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
- Spectrum processing in spectrum_utils has been optimized for computational efficiency
  using [NumPy](https://www.numpy.org/)
- import numpy as np
- optimized for computational efficiency using [NumPy](https://www.numpy.org/) and
  [Numba](http://numba.pydata.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-noise-peak-filtering

## Summary

Remove low-intensity noise peaks from mass spectrometry spectra by filtering based on intensity thresholds relative to the base peak and limiting the total number of peaks retained. This preprocessing step enhances signal-to-noise ratio and prepares spectra for downstream peptide fragment annotation and database matching.

## When to use

When working with raw or partially processed tandem mass spectrometry (MS/MS) spectra that contain low-intensity background noise peaks. Apply this skill before peptide fragment annotation or spectral matching when the spectrum contains more than the desired number of peaks or when peaks below a biologically meaningful intensity threshold are introducing noise.

## When NOT to use

- Input spectrum is already a processed feature table or has already undergone noise filtering in acquisition software.
- Analysis goal requires retention of all peaks for isotope pattern analysis or peak shape modeling, where low-intensity peaks carry structural information.
- Spectrum is from targeted or selected-reaction-monitoring (SRM) experiments where only a few diagnostic peaks are expected; blanket peak count limits may remove valid signal.

## Inputs

- MsmsSpectrum object (spectrum_utils)
- minimum intensity threshold (float, typically 0.05–0.1 relative to base peak)
- maximum number of peaks to retain (integer, typically 50)

## Outputs

- MsmsSpectrum object with noise peaks removed and peak count capped
- Filtered m/z and intensity arrays
- Peak count reduction metric

## How to apply

Load an MsmsSpectrum object and call the filter_intensity() method with a minimum intensity threshold (typically 0.05, meaning 5% of the base peak intensity) and a maximum number of peaks to retain (typically 50 most intense peaks). This dual filtering removes noise while preserving the signal-bearing peaks most likely to correspond to actual peptide fragments. The rationale is that peaks below 5% base peak intensity typically represent chemical noise rather than true fragment ions, and limiting to the top 50 peaks reduces computational burden in downstream matching while retaining sufficient information for reliable peptide identification. Apply this filter after removing the precursor peak but before intensity scaling, as the intensity threshold is relative to the current intensity distribution.

## Related tools

- **spectrum_utils** (Provides the filter_intensity() method to remove low-intensity noise peaks and cap peak count) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Underlying array operations for efficient intensity-based filtering) — https://www.numpy.org/
- **Numba** (JIT compilation for optimized filtering performance on large spectral datasets) — http://numba.pydata.org/

## Examples

```
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50)
```

## Evaluation signals

- Peak count is reduced to ≤ specified max_num_peaks (e.g., ≤ 50) after filtering.
- All remaining peaks have intensity ≥ min_intensity × base_peak_intensity (e.g., ≥ 0.05 × max intensity in spectrum).
- Signal-to-noise ratio improves and downstream peptide fragment annotations show higher match scores or lower false discovery rates.
- Remaining peaks correspond to major fragment ions (b, y, a ions) when spectrum is subsequently annotated against a known peptide sequence.
- Peak intensity distribution remains monotonically ordered by intensity (no low-intensity peak remains below a higher-intensity one that was removed).

## Limitations

- Fixed thresholds (5% base peak intensity, 50 peak maximum) may not be optimal for all instrument types, MS/MS acquisition methods, or sample complexity; parameter tuning may be required for highly complex proteomes or targeted applications.
- Filtering is irreversible; important but low-intensity peaks (e.g., weak neutral loss peaks, rare post-translational modification markers) may be lost if intensity thresholds are too stringent.
- Peak count limiting may unfairly penalize spectra from multiply charged precursors or high-mass peptides that naturally produce many fragments; consider spectra-adaptive or charge-aware thresholds for heterogeneous datasets.
- Does not account for background subtraction or mass-calibration drift; spectra with poor quality (e.g., uncalibrated or with systematic background) may yield suboptimal results.

## Evidence

- [other] Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Call filter_intensity(min_intensity=0.05, max_num_peaks=50) to remove noise peaks below 5% base peak intensity and retain the 50 most intense peaks: "Call filter_intensity(min_intensity=0.05, max_num_peaks=50) to remove noise peaks below 5% base peak intensity and retain the 50 most intense peaks"
- [other] spectrum_utils implements four core spectrum preprocessing operations: precursor peak removal, noise peak removal via intensity filtering, and intensity scaling: "spectrum_utils implements four core spectrum preprocessing operations: precursor peak removal, noise peak removal via intensity filtering, and intensity scaling"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba"
