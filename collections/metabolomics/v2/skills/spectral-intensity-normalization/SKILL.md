---
name: spectral-intensity-normalization
description: Use when after removing precursor and noise peaks from an MsmsSpectrum object when the spectrum contains peaks with highly variable intensities (e.g., one or two dominant peaks with many weaker fragments).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
- Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/)
- import numpy as np
- optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)
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

# spectral-intensity-normalization

## Summary

Normalize peak intensities in tandem mass spectrometry spectra by applying scaling transformations (e.g., square-root scaling) to de-emphasize overly intense peaks and improve downstream spectral comparison and matching. This is a critical preprocessing step that follows noise removal and precedes spectral annotation or database matching.

## When to use

Apply this skill after removing precursor and noise peaks from an MsmsSpectrum object when the spectrum contains peaks with highly variable intensities (e.g., one or two dominant peaks with many weaker fragments). Intensity scaling is particularly needed before spectral similarity computations, database searches, or when feeding spectra to machine learning pipelines that assume normalized feature ranges.

## When NOT to use

- The spectrum has already been normalized or intensity-scaled by upstream preprocessing.
- Your analysis requires raw, unnormalized intensities for absolute quantitation or ion current measurements.
- You are working with ion mobility or retention time data where intensity normalization is not applicable.

## Inputs

- MsmsSpectrum object (filtered for m/z range, with precursor peak removed and noise-filtered)
- Peak intensity array with peaks at ≥5% base peak intensity

## Outputs

- MsmsSpectrum object with square-root-scaled peak intensities
- Normalized intensity array suitable for spectral similarity and matching workflows

## How to apply

After loading an MsmsSpectrum and applying precursor peak removal and intensity filtering (retaining peaks ≥5% base peak intensity and the top 50 most intense peaks), call the scale_intensity() method with the 'root' parameter to apply square-root scaling. This transformation compresses the dynamic range by taking the square root of each peak intensity, which reduces the influence of the most intense peaks while preserving the relative ordering of smaller peaks. The choice of 'root' scaling is motivated by the goal of de-emphasizing overly intense peaks that would otherwise dominate spectral matching metrics. Apply this normalization consistently across all spectra in a cohort to ensure fair comparison.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum.scale_intensity() method with 'root' parameter and the complete spectrum preprocessing pipeline (precursor/noise removal, intensity filtering, and scaling).) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Underlying computational library used by spectrum_utils to implement intensity scaling operations efficiently.) — https://www.numpy.org/
- **Numba** (JIT compiler used to optimize intensity normalization computations for large-scale spectral datasets.) — http://numba.pydata.org/

## Examples

```
spectrum.scale_intensity('root')
```

## Evaluation signals

- Verify that the scaled spectrum has intensities in the range [0, sqrt(base_peak_intensity)], with the base peak scaled to its square root.
- Confirm that peak intensity ordering is preserved after scaling (if peak A > peak B before scaling, then scaled(A) > scaled(B) after).
- Check that the spectrum object retains all fragment peak annotations (m/z, intensity, and any peptide fragment labels) after scaling.
- Validate that the normalized spectrum can be successfully used in downstream spectral similarity calculations (e.g., cosine similarity with reference spectra) without producing NaN or Inf values.
- Ensure that the number of peaks in the spectrum remains ≤50 after scaling (i.e., no peaks are added or removed by the normalization step).

## Limitations

- Square-root scaling assumes that peak intensity follows a power-law or log-normal distribution; this may not hold for spectra with unusual intensity distributions or very weak signals.
- The 'root' scaling method is one of several possible normalization approaches; alternative scaling functions (e.g., log, arcsinh, or z-score normalization) may be more appropriate for certain spectral types or downstream analyses.
- Intensity normalization is applied uniformly across all peaks regardless of their mass-to-charge ratio; this does not account for m/z-dependent systematic biases in mass spectrometer ion detection efficiency.
- The normalization step does not correct for charge state, fragmentation efficiency, or other physical properties that affect absolute peak intensities; it is a relative, not absolute, normalization.

## Evidence

- [other] Scale the peak intensities by their square root to de-emphasize overly intense peaks: "Scale the peak intensities by their square root to de-emphasize overly intense peaks"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, and intensity scaling) optimized for computational efficiency: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, and intensity scaling) optimized for computational efficiency."
- [other] Remove low-intensity noise peaks by retaining peaks at least 5% of base peak intensity and restrict to 50 most intense peaks: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Spectrum processing in spectrum_utils optimized using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [other] Call scale_intensity with root parameter as part of sequential preprocessing workflow: "Call scale_intensity('root') to scale peak intensities by their square root to de-emphasize overly intense peaks"
