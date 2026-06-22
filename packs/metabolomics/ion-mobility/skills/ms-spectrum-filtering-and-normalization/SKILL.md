---
name: ms-spectrum-filtering-and-normalization
description: Use when you have raw or parsed tandem MS spectra (MGF, mzML, or in-memory Spectrum objects) and need to remove artifacts and normalize intensities prior to spectral matching, library searching, or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - pymzML
  - pyOpenMS
  - Python
  - seaborn
  - NumPy
  - pyteomics
  - Numba
  - matplotlib
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
- pymzML (version 2.5.2)
- pyOpenMS (version 2.7.0)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS spectrum filtering and normalization

## Summary

A workflow to preprocess tandem mass spectrometry spectra by removing noise, truncating m/z ranges, eliminating precursor peaks, and applying intensity scaling. This skill is essential for standardizing spectra before database searching, spectral comparison, or machine learning pipelines.

## When to use

Apply this skill when you have raw or parsed tandem MS spectra (MGF, mzML, or in-memory Spectrum objects) and need to remove artifacts and normalize intensities prior to spectral matching, library searching, or downstream analysis. Use it when spectra contain low-intensity noise, extreme m/z values outside the peptide fragment region (typically 100–1400 m/z), or when precursor-ion contamination is present.

## When NOT to use

- Spectra already filtered and normalized by the data provider or upstream pipeline
- High-resolution accurate-mass MS data where precursor mass tolerance must be <5 ppm (requires different tolerance parameters than shown)
- Native ion mobility or trapped ion mobility spectra, which may require orthogonal filtering strategies

## Inputs

- Raw or parsed tandem MS spectra (MGF file format, mzML file, or in-memory Spectrum objects)
- Spectrum metadata including m/z values, intensities, precursor m/z, precursor charge state, and mass tolerance parameters

## Outputs

- Filtered and normalized spectra with cleaned peak lists
- Peak intensity matrix (m/z, normalized intensity) ready for spectral matching or annotation
- Per-spectrum processing runtimes (for performance benchmarking)

## How to apply

Load spectra using a parser (e.g., pyteomics.mgf or spectrum_utils' USI mechanism). Apply filtering in sequence: (1) restrict m/z range to 100–1400 to exclude out-of-scope peaks; (2) remove the precursor peak using a mass tolerance (e.g., ±0.02 Da); (3) filter peaks below 5% of the base peak intensity and optionally cap to the 50–150 most intense peaks to reduce noise; (4) scale all remaining peak intensities by their square root to de-emphasize overly intense peaks and improve dynamic range. The square-root scaling is particularly important for down-weighting dominant peaks that might otherwise dominate spectral matching. Use spectrum_utils, pymzML, or pyOpenMS APIs to apply these operations; spectrum_utils v0.4.0 offers optimized NumPy and Numba-backed implementations for throughput.

## Related tools

- **spectrum_utils** (Primary optimized library for spectrum filtering, precursor removal, intensity filtering, scaling, and visualization; provides NumPy and Numba-accelerated implementations) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (Alternative library for parsing and filtering mzML spectra; supports precursor removal and intensity normalization) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Alternative library for spectrum processing including m/z range restriction, precursor removal, and intensity normalization) — https://pyopenms.readthedocs.io/
- **pyteomics** (Parser for MGF and mzML files to load raw spectra into memory) — https://pyteomics.readthedocs.io/
- **NumPy** (Vectorized numerical operations underlying optimized spectrum processing in spectrum_utils) — https://www.numpy.org/
- **Numba** (Just-in-time compiler for computational kernels used in spectrum_utils peak filtering and scaling) — http://numba.pydata.org/
- **matplotlib** (Visualization of filtered spectra and generation of boxplots comparing processing times across libraries) — https://matplotlib.org/

## Examples

```
from spectrum_utils.spectrum import Spectrum; spectrum.set_mz_range(min_mz=100, max_mz=1400); spectrum.remove_precursor_peak(fragment_tol_mass=0.02, fragment_tol_mode='Da'); spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=150); spectrum.scale_intensity('root')
```

## Evaluation signals

- Verify m/z range: all retained peaks fall within 100–1400 m/z (or user-specified bounds)
- Confirm precursor peak removal: no peak within ±0.02 Da (or specified tolerance) of the precursor m/z remains
- Check intensity normalization: largest peak after filtering and scaling is <1.0 (normalized to fraction of base peak), and square-root scaling is visibly applied (log-scale boxplot should show reduced dynamic range vs. raw)
- Validate peak count reduction: filtered spectrum contains ≤150 peaks (or specified cap) with no peaks <5% base peak intensity
- Confirm processing throughput: spectrum_utils completes filtering faster than pymzML and pyOpenMS on the same spectra set (median processing time per spectrum in milliseconds should be lower)

## Limitations

- Fixed m/z range (100–1400) may not be appropriate for all MS configurations (e.g., high-mass protein complexes, negative-ion mode)
- Square-root intensity scaling de-emphasizes intense peaks but may suppress weak signal-to-noise ratio peaks; alternative scaling strategies (e.g., TIC normalization, log) may be needed for certain applications
- 5% base peak intensity threshold assumes sufficient signal-to-noise; very noisy spectra may require stricter thresholds or alternative denoising (e.g., wavelet)
- Precursor mass tolerance (±0.02 Da) is instrument-dependent; high-resolution Orbitrap or FTICR data may require tighter tolerances (≤5 ppm)
- No changelog documented; version compatibility and backward-compatibility guarantees between spectrum_utils releases are unclear

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Restrict the mass range to 100–1400 m/z to filter out irrelevant peaks: "Restrict the mass range to 100–1400 _m_/_z_ to filter out irrelevant peaks"
- [other] Remove low-intensity noise peaks by only retaining peaks at least 5% of the base peak intensity: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Scale the peak intensities by their square root to de-emphasize overly intense peaks: "Scale the peak intensities by their square root to de-emphasize overly intense peaks"
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [other] spectrum_utils (version 0.4.0) is faster than alternative libraries, such as pymzML (version 2.5.2) and pyOpenMS (version 2.7.0): "spectrum_utils (version 0.4.0) is faster than alternative libraries, such as [pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2) and [pyOpenMS](https://pyopenms.readthedocs.io/) (version"
