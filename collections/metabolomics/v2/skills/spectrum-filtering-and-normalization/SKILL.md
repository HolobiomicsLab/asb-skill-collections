---
name: spectrum-filtering-and-normalization
description: Use when you have raw or minimally processed tandem MS spectra (in mzML, mgf, or other standard formats) and need to prepare them for spectral matching, library searching, or quantitative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - pymzML
  - pyOpenMS
  - Python
  - pyteomics
  - matplotlib
  - seaborn
  - NumPy
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
- pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2)
- pyOpenMS](https://pyopenms.readthedocs.io/) (version 2.7.0)
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
---

# spectrum-filtering-and-normalization

## Summary

A suite of computational operations to clean and standardize mass spectrometry spectra by removing noise, filtering peaks by intensity, adjusting m/z ranges, and applying intensity scaling transformations. These operations optimize spectra for downstream analysis while reducing computational overhead and improving comparability across datasets.

## When to use

Apply this skill when you have raw or minimally processed tandem MS spectra (in mzML, mgf, or other standard formats) and need to prepare them for spectral matching, library searching, or quantitative analysis. Use it specifically when you need to remove instrumental artifacts (precursor peaks, low-intensity noise), standardize intensity scales across spectra with different dynamic ranges, or enforce consistent m/z windows (e.g., 100–1400 Da for peptide fragmentation).

## When NOT to use

- Input spectra are already heavily processed (e.g., already denoised, scaled, and windowed by your vendor software or prior pipeline step); re-applying may introduce artifacts.
- Your analysis requires preservation of full dynamic range or absolute intensity values (e.g., quantitative proteomics relying on precursor intensity); intensity scaling via square root will compress this information.
- You are working with non-peptide analytes (small molecules, lipids, or glycans) where standard m/z windows (100–1400 Da) or peak count limits (e.g., max_num_peaks=150) are inappropriate.

## Inputs

- Raw tandem MS spectra in mzML, mgf, or mzXML format
- Spectrum objects with m/z and intensity arrays
- Precursor m/z and charge state metadata
- Fragment mass tolerance parameters (Da or ppm)

## Outputs

- Filtered and normalized spectrum objects with cleaned peak lists
- Intensity-scaled spectra suitable for spectral matching
- Spectra with uniform m/z range and reduced peak count
- Processing time metrics (wall-clock time per spectrum or throughput in spectra/second)

## How to apply

Load spectra from your dataset using a library compatible with your input format (e.g., pyteomics.mgf.read for .mgf files). Apply filtering and normalization in sequence: (1) set a consistent m/z range using set_mz_range() to remove out-of-range peaks; (2) remove the precursor peak using remove_precursor_peak() with appropriate fragment mass tolerance; (3) filter low-intensity noise by applying filter_intensity() with a minimum intensity threshold (e.g., min_intensity=0.05) and a maximum peak count (e.g., max_num_peaks=150) to focus on dominant fragments; (4) scale peak intensities using scale_intensity() with a root transformation to compress the dynamic range and improve cosine similarity calculations. The order matters: set m/z range first, then remove precursor, then apply intensity filters, then scale. Validate that the median processing time per spectrum is reasonable (benchmarking against pymzML and pyOpenMS can establish baseline expectations for your hardware).

## Related tools

- **spectrum_utils** (Core library providing set_mz_range(), remove_precursor_peak(), filter_intensity(), and scale_intensity() methods for spectrum filtering and normalization) — https://github.com/bittremieuxlab/spectrum_utils
- **pyteomics** (Used to load and parse spectra from mzML, mgf, and mzXML files for input to the filtering pipeline)
- **pymzML** (Alternative library for mzML file parsing; included in comparative benchmarking to evaluate throughput differences) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Alternative library for mass spectrometry data processing; included in comparative benchmarking to establish relative performance baseline)
- **Python** (Runtime environment for executing filtering and normalization scripts; time.time() used for performance measurement)

## Examples

```
from spectrum_utils.spectrum import Spectrum; import pyteomics.mgf; spectra = pyteomics.mgf.read('iPRG2012.mgf'); for spec_dict in spectra: s = Spectrum(spec_dict['m/z array'], spec_dict['intensity array'], spec_dict['params']); s.set_mz_range(min_mz=100, max_mz=1400); s.remove_precursor_peak(fragment_tol_mass=0.1, fragment_tol_mode='Da'); s.filter_intensity(min_intensity=0.05, max_num_peaks=150); s.scale_intensity('root')
```

## Evaluation signals

- Verify that filtered spectra have m/z values strictly within the specified range (e.g., 100–1400 Da); check min and max of m/z arrays post-filtering.
- Confirm that the precursor m/z (± fragment_tol_mass) is absent from the peak list after remove_precursor_peak(); spot-check several spectra.
- Ensure that low-intensity peaks below min_intensity threshold are removed and peak count per spectrum does not exceed max_num_peaks (e.g., ≤150).
- Validate that intensity values are compressed (typically in range 0–1 after square-root scaling) and sum of squared intensities is recalculated for norm-based comparisons (e.g., cosine similarity).
- Measure processing rate (spectra per second) and verify it matches or exceeds the baseline established by benchmarking against pymzML and pyOpenMS on the same hardware and dataset.

## Limitations

- The choice of min_intensity threshold and max_num_peaks is dataset- and instrument-dependent; values optimized for iPRG2012 (min_intensity=0.05, max_num_peaks=150) may not generalize to other datasets, especially for MS/MS from different mass analyzers (Orbitrap vs. TOF) or proteolytic digests (tryptic vs. non-specific).
- Square-root intensity scaling is lossy; absolute intensity information is not preserved and cannot be recovered post-scaling, limiting downstream quantitative analyses that require recovery of ion counts or signal magnitude.
- The m/z window (100–1400 Da) is optimized for tryptic peptide fragmentation; spectra from non-peptide analytes or proteolytic cleavage schemes with different fragmentation patterns may lose relevant fragments outside this range.
- Processing time benchmarks are sensitive to hardware (CPU, memory, I/O bandwidth) and Python version; reported throughput (spectra per second) should be re-benchmarked on your target system.
- The skill assumes clean, annotated spectrum metadata (precursor m/z, charge state); spectra with missing or incorrect precursor annotation will result in incorrect precursor peak removal.

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root.: "apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root."
- [other] spectrum.set_mz_range(min_mz=100, max_mz=1400): "spectrum.set_mz_range(min_mz=100, max_mz=1400)"
- [other] .remove_precursor_peak(fragment_tol_mass, fragment_tol_mode): ".remove_precursor_peak(fragment_tol_mass, fragment_tol_mode)"
- [other] .filter_intensity(min_intensity=0.05, max_num_peaks=50): ".filter_intensity(min_intensity=0.05, max_num_peaks=50)"
- [other] .scale_intensity("root"): ".scale_intensity("root")"
- [other] Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps.: "Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps."
