---
name: spectral-peak-intensity-scaling
description: Use when after filtering and noise removal when you have a cleaned spectrum with m/z and intensity pairs and need to normalize the intensity distribution prior to peptide fragment annotation, spectral library matching, or machine learning-based spectrum analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pymzML
  - pyOpenMS
  - Python
  - seaborn
  - NumPy
  - pyteomics
  - Numba
  - spectrum_utils
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- pymzML (version 2.5.2)
- pyOpenMS (version 2.7.0)
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
- import seaborn as sns
- Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/)
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

# spectral-peak-intensity-scaling

## Summary

Apply square-root or other intensity scaling transformations to mass spectrometry spectrum peak intensities to de-emphasize overly intense peaks and improve dynamic range for downstream spectral analysis and matching. This normalization step is critical for making weak and strong peaks more comparable in intensity-based search algorithms.

## When to use

Apply this skill after filtering and noise removal when you have a cleaned spectrum with m/z and intensity pairs and need to normalize the intensity distribution prior to peptide fragment annotation, spectral library matching, or machine learning-based spectrum analysis. Use it when the dynamic range of peak intensities spans several orders of magnitude and you want to reduce the dominance of the most intense peaks in similarity calculations.

## When NOT to use

- Do not apply if your downstream analysis explicitly requires raw, unscaled intensities (e.g., some quantification or absolute abundance calculations).
- Do not apply if the spectrum has already been intensity-normalized by another method (e.g., TIC normalization or z-score scaling) without understanding the interaction.
- Do not apply as a substitute for proper noise filtering—intensity scaling does not remove noise peaks, only reduces their relative importance.

## Inputs

- MsmsSpectrum object (or equivalent m/z–intensity pairs) after m/z range restriction and precursor/noise filtering
- Peak intensity values (float array)
- Scaling method identifier (e.g., 'root' for square root)

## Outputs

- MsmsSpectrum object with square-root-scaled peak intensities
- Normalized intensity array (float array with values between 0 and ~1 after scaling)

## How to apply

After restricting the m/z range (e.g., 100–1400), removing the precursor peak, and filtering low-intensity noise peaks (e.g., retaining only peaks ≥5% of base peak intensity), apply square-root scaling to all remaining peak intensities. This transformation compresses the intensity scale non-linearly, so that strong peaks lose relative dominance while weak peaks are amplified. The rationale is that peak intensity in mass spectrometry often reflects chemical ionization efficiency rather than abundance, making raw intensity a poor proxy for fragment importance; square-root scaling brings the intensity distribution closer to log-normal and improves consistency in spectral similarity scoring across spectra with varying dynamic ranges.

## Related tools

- **spectrum_utils** (Provides the scale_intensity() method to apply square-root and other scaling transformations to MsmsSpectrum objects) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Used internally by spectrum_utils for vectorized intensity scaling operations)
- **Numba** (Provides just-in-time compilation for optimized computational efficiency of intensity scaling loops)

## Examples

```
spectrum.scale_intensity('root')
```

## Evaluation signals

- Verify that all peak intensities are transformed by the specified scaling function (e.g., new_intensity = sqrt(old_intensity)); spot-check a few values manually.
- Confirm that the maximum intensity after scaling is close to 1.0 (or √max_original if square root is used), and all scaled values are in the range [0, 1] or [0, √max].
- Check that weak peaks (e.g., 5% of base peak intensity) are amplified relative to strong peaks; for example, after square-root scaling, a peak at 0.05 becomes ~0.224, and a peak at 1.0 remains 1.0.
- Verify that spectral similarity scores (e.g., dot product or cosine similarity) computed on scaled spectra are more balanced across spectra with different dynamic ranges than on unscaled spectra.
- Ensure the output MsmsSpectrum object retains all metadata (m/z values, charge state, precursor m/z) while only intensities are transformed.

## Limitations

- Square-root scaling is a heuristic choice; other scaling methods (e.g., log, z-score, or no scaling) may be more appropriate for certain mass spectrometry data types (e.g., high-resolution vs. low-resolution, or data from different ionization methods).
- Scaling does not address the fundamental issue of peak intensity being instrument- and compound-dependent rather than stoichiometry-dependent; it is a normalization heuristic, not a quantitative abundance measure.
- If the spectrum contains zero or near-zero intensity values, square-root scaling will not cause numerical errors but will not amplify them meaningfully either (√0 = 0).
- The article provides no comparison of different scaling methods or guidance on selecting the scaling function for new data domains; the choice of square root is empirically motivated but not universally optimal.

## Evidence

- [other] Scale the peak intensities by their square root to de-emphasize overly intense peaks: "Scale the peak intensities by their square root to de-emphasize overly intense peaks"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency"
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba"
- [other] Call scale_intensity('root') to scale peak intensities by their square root to de-emphasize overly intense peaks: "Call scale_intensity('root') to scale peak intensities by their square root to de-emphasize overly intense peaks"
