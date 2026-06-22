---
name: multi-library-comparative-analysis
description: Use when you need to evaluate whether a newly released or candidate library (e.g., spectrum_utils v0.4.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzML
  - pyOpenMS
  - Python
  - pyteomics
  - matplotlib
  - seaborn
  - NumPy
  - spectrum_utils
  - pyteomics.mgf
  - Python time module
  - matplotlib / seaborn
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2)
- pyOpenMS](https://pyopenms.readthedocs.io/) (version 2.7.0)
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- import pyteomics.mgf
- import matplotlib.pyplot as plt
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

# multi-library-comparative-analysis

## Summary

Benchmark competing mass spectrometry data processing libraries (spectrum_utils, pymzML, pyOpenMS) on identical datasets and filtering workflows to quantitatively compare throughput and processing efficiency. This skill isolates algorithmic and implementation differences by applying identical transformations across libraries and measuring wall-clock runtime per spectrum.

## When to use

You need to evaluate whether a newly released or candidate library (e.g., spectrum_utils v0.4.0) achieves measurably higher throughput (spectra per second) than established alternatives (pymzML, pyOpenMS) when processing the same benchmark dataset with identical preprocessing parameters (m/z range 100–1400 Da, precursor removal, intensity filtering with min_intensity=0.05 and max_num_peaks=150, square-root scaling). Use this skill when throughput claims are part of a paper's contribution or when downstream pipeline selection depends on processing speed.

## When NOT to use

- Input dataset or preprocessing parameters differ materially between libraries (e.g., different m/z ranges or filtering thresholds applied); comparison becomes confounded by unequal workflow setup.
- Libraries are evaluated on different hardware, Python versions, or dependency versions without controlling for these confounders; throughput differences may reflect environment rather than algorithmic merit.
- The research question concerns correctness, accuracy, or numerical stability of results rather than throughput; use correctness validation or peak annotation benchmarks instead.

## Inputs

- Mass spectrometry spectral dataset in MGF format (e.g., iPRG2012.mgf)
- Library implementations: spectrum_utils, pymzML, pyOpenMS (Python packages)
- Filter parameters: m/z range (100–1400 Da), intensity threshold (0.05), peak count ceiling (150)
- Spectrum selection criteria: ≥10 peaks, valid charge state

## Outputs

- Median wall-clock runtime per spectrum (milliseconds) for each library
- Processing throughput (spectra per second) for each library
- Tabulated comparison with runtime and rate metrics
- Visualization (e.g., bar plot or box plot) of runtime distributions across libraries

## How to apply

Load a shared benchmark dataset (e.g., iPRG2012.mgf) with pyteomics.mgf.read, filtering spectra to those with ≥10 peaks and valid charge states. For each of the three libraries (spectrum_utils, pymzML, pyOpenMS), apply the identical processing pipeline: set m/z range to 100–1400 Da using library-native methods, remove precursor peaks, apply intensity filtering with min_intensity=0.05 and max_num_peaks=150, and scale intensities by square root. Wrap each library's processing block with Python time.time() calls before and after the loop to measure wall-clock time. Compute the processing rate (spectra per second) as the inverse of the median runtime per spectrum for each library, computed over all filtered spectra. Tabulate median runtimes and throughput rates side-by-side; verify that the candidate library's median time is statistically lower than both comparators using descriptive statistics (median, interquartile range) or a non-parametric test such as the Mann–Whitney U test if sample sizes permit.

## Related tools

- **spectrum_utils** (Candidate library under evaluation for throughput and processing efficiency on mass spectrometry spectra) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (Baseline library for comparative throughput benchmarking) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Baseline library for comparative throughput benchmarking)
- **pyteomics.mgf** (Spectral data loader for reading and filtering MGF-format datasets)
- **Python time module** (Wall-clock timing instrumentation for measuring runtime per spectrum)
- **NumPy** (Median and statistical summary computation on runtime arrays)
- **matplotlib / seaborn** (Visualization of throughput and runtime comparisons across libraries)

## Examples

```
import time; from pyteomics.mgf import read; spectra = [s for s in read('iPRG2012.mgf') if len(s['m/z array']) >= 10]; times = []; [times.append(time.time()); spectrum_utils.Spectrum(...).set_mz_range(100, 1400).remove_precursor_peak(...).filter_intensity(0.05, 150).scale_intensity('root'); times.append(time.time()) for s in spectra]; median_time = sorted([times[i+1]-times[i] for i in range(0, len(times), 2)])[len(times)//4]; print(f'Throughput: {1/median_time:.2f} spectra/sec')
```

## Evaluation signals

- Median runtime per spectrum is computed correctly as the 50th percentile of per-spectrum wall-clock times for each library; verify by spot-checking the timing calculation on a small subset.
- All three libraries process the identical set of filtered spectra (same peaks, m/z ranges, and preprocessing parameters); confirm by logging spectrum IDs and parameters to each library's processing block.
- Throughput (spectra/second) for the candidate library is numerically lower than both baseline libraries in median runtime (or equivalently, higher in spectra per second rate), with the difference substantively exceeding noise (e.g., > 10% improvement).
- Runtime distributions are plotted and visually inspected for outliers, multimodality, or skew that might indicate transient overhead or memory effects; if present, report median + interquartile range rather than mean + SD.
- Benchmark is reproducible: running the workflow on the same dataset and parameters yields throughput metrics within ±5% of reported values, accounting for system load variation.

## Limitations

- Throughput benchmarks are sensitive to hardware (CPU cache, RAM speed, disk I/O) and software (Python version, NumPy/compiled library versions, GC pressure) context; results may not transfer to different environments or larger datasets.
- Processing rate (spectra per second) is a proxy for efficiency but does not capture memory consumption, cache locality, or scalability to millions of spectra; library A may be faster on iPRG2012 but slower or memory-bound on larger cohorts.
- Comparison assumes libraries expose identical or semantically equivalent parameters (e.g., min_intensity, max_num_peaks); if one library lacks a feature, the comparison may be incomplete or force use of library-specific defaults that confound the results.
- The article does not report actual benchmark results; the workflow is prescriptive only, and empirical throughput claims require execution.
- Wall-clock timing is coarse-grained and subject to OS noise; sub-millisecond differences may not be reliable without repeated runs and statistical analysis.

## Evidence

- [other] Does spectrum_utils achieve higher throughput (spectra per second) compared to pymzML and pyOpenMS when processing the same benchmark dataset?: "Does spectrum_utils achieve higher throughput (spectra per second) compared to pymzML and pyOpenMS when processing the same benchmark dataset?"
- [other] For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root.: "For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and"
- [other] Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps.: "Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps."
- [other] Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library.: "Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library."
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
