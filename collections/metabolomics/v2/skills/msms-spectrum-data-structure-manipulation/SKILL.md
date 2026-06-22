---
name: msms-spectrum-data-structure-manipulation
description: Use when you have raw or downloaded MSMS spectra (from online resources via Universal Spectrum Identifier, or from local mzML/mzXML files) that require standardization, cleaning, and fragment assignment before visualization, statistical comparison, or machine-learning feature extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - matplotlib
  - NumPy
  - Numba
  - PSI-MOD
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msms-spectrum-data-structure-manipulation

## Summary

Load, filter, annotate, and transform tandem mass spectrometry (MSMS) spectra using the spectrum_utils MsmsSpectrum data structure, enabling preparation of spectra for publication-quality visualization and downstream analysis. This skill encompasses mass range restriction, noise/precursor removal, intensity normalization, and fragment annotation via ProForma 2.0 peptide strings.

## When to use

You have raw or downloaded MSMS spectra (from online resources via Universal Spectrum Identifier, or from local mzML/mzXML files) that require standardization, cleaning, and fragment assignment before visualization, statistical comparison, or machine-learning feature extraction. Apply this skill when you need to enforce consistent m/z ranges, remove chemical noise or instrument artifacts, normalize peak intensities, or map theoretical fragment ions to observed peaks.

## When NOT to use

- Input is not a tandem MSMS spectrum (e.g., intact protein MALDI imaging, or already-processed feature table).
- Fragment tolerance or ion types are unknown or inapplicable (e.g., de novo MS/MS without a peptide sequence).
- ProForma 2.0 representation is unsupported by the annotation target (check spectrum_utils documentation for modification coverage).

## Inputs

- MsmsSpectrum object (from spectrum_utils.spectrum module)
- Universal Spectrum Identifier (USI) string (e.g., 'mzspec:MSV000082283:f07074:scan:5475')
- ProForma 2.0 peptide string (modified or unmodified peptidoform, e.g., '[Acetyl]-PEPTIDE')
- Fragment tolerance parameters (mass value and mode: 'Th' or 'Da')
- Ion type specification string (e.g., 'aby' for a/b/y fragments)

## Outputs

- Annotated and filtered MsmsSpectrum object with m/z-restricted, intensity-scaled, and fragment-annotated peaks
- NumPy arrays of m/z values and intensities (accessible via spectrum.mz and spectrum.intensity)
- Annotation metadata (fragment ion assignments accessible via spectrum annotations property)

## How to apply

Begin by loading an MsmsSpectrum object from a USI string using MsmsSpectrum.from_usi() or by parsing a spectrum file. Apply sequential filtering operations in this order: (1) restrict the m/z window using set_mz_range() to exclude out-of-range noise (e.g., 100–1400 m/z); (2) remove the precursor ion with remove_precursor_peak(), specifying fragment tolerance (mass and mode, typically 'Th' or 'Da'); (3) remove low-intensity noise peaks via filter_intensity() by setting a minimum intensity threshold (e.g., 5% of base peak) and capping peak count (e.g., 50 most intense); (4) normalize intensities using scale_intensity() with a chosen function such as 'root' to reduce the dynamic range. Finally, annotate the spectrum by calling annotate_proforma() with a ProForma 2.0 peptide string, specifying fragment ion types ('a', 'b', 'y', etc.) and neutral loss rules. Each operation modifies the spectrum in-place; verify success by inspecting the spectrum's peaks attribute and annotation status before downstream use.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum data structure, filtering operations (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity), annotation (annotate_proforma), and plotting utilities.) — https://github.com/bittremieux/spectrum_utils
- **matplotlib** (Backend for rendering filtered and annotated spectra to static publication-quality plots.)
- **NumPy** (Underlying array storage and operations for spectrum m/z and intensity data; optimized for computational efficiency.)
- **Numba** (JIT compilation for performance-critical spectrum processing loops.)
- **PSI-MOD** (Ontology defining protein modification terms referenced by ProForma 2.0 peptidoform annotations.) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
spectrum.set_mz_range(min_mz=100, max_mz=1400)
spectrum.remove_precursor_peak(fragment_tol_mass=0.05, fragment_tol_mode='Da')
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50)
spectrum.scale_intensity('root')
spectrum.annotate_proforma('[Acetyl]-PEPTIDE', fragment_tol_mass=0.05, fragment_tol_mode='Da', ion_types='aby')
```

## Evaluation signals

- Filtered spectrum's m/z range falls within specified bounds (e.g., 100–1400 m/z); check via min(spectrum.mz) and max(spectrum.mz).
- Precursor peak is absent from the filtered spectrum; verify its m/z is no longer in the peaks list.
- Peak count after filter_intensity() is ≤ max_num_peaks parameter (e.g., ≤ 50); all remaining peaks have intensity ≥ min_intensity threshold (e.g., ≥ 0.05 of base peak).
- Intensity scaling applied: all intensities should be non-negative and in a narrower dynamic range; e.g., after 'root' scaling, max intensity < original max intensity for most spectra.
- Annotated spectrum contains fragment assignments: spectrum.annotation should be a non-empty list or dict with ion type keys; verify at least one b/y ion matches within the specified fragment_tol_mass tolerance.

## Limitations

- ProForma 2.0 support is limited to modifications defined in PSI-MOD; custom or very recent modifications may not be recognized.
- Fragment annotation assumes a linear peptide; no built-in support for cyclic or branched peptidoforms.
- USI loading requires network access to remote proteomics repositories (ProteomeXchange, MassIVE); offline workflows must use local file parsing.
- Neutral loss annotation is optional and may require manual configuration per experiment type (e.g., phospho-specific loss).
- No changelog available in the official repository; versioning and API stability should be verified via GitHub releases or the official documentation.

## Evidence

- [readme] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
- [other] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [intro] Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting.: "Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting."
- [other] Restrict the mass range to 100–1400 m/z to filter out irrelevant peaks: "Restrict the mass range to 100–1400 _m_/_z_ to filter out irrelevant peaks"
- [other] Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Scale the peak intensities by their square root to de-emphasize overly intense peaks: "Scale the peak intensities by their square root to de-emphasize overly intense peaks"
- [other] Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string: "Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a [ProForma 2.0](https://www.psidev.info/proforma) peptide string"
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [other] Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI): "Load a spectrum from an online data resource by its [Universal Spectrum Identifier (USI)](https://www.psidev.info/usi)"
