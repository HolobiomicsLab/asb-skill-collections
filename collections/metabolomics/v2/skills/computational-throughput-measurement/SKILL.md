---
name: computational-throughput-measurement
description: Use when when you need to compare the computational efficiency of different mass spectrometry libraries on identical data and processing pipelines, or when you want to establish baseline throughput for a library version and validate claims of performance improvement.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
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
  - Python time.time()
  - NumPy, matplotlib, seaborn
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

# computational-throughput-measurement

## Summary

Quantify the processing rate (spectra per second) of mass spectrometry data processing libraries by measuring wall-clock execution time on standardized datasets and filtering parameters. This skill enables fair performance comparison across tools like spectrum_utils, pymzML, and pyOpenMS.

## When to use

When you need to compare the computational efficiency of different mass spectrometry libraries on identical data and processing pipelines, or when you want to establish baseline throughput for a library version and validate claims of performance improvement.

## When NOT to use

- When input spectra have heterogeneous properties (different m/z ranges, peak densities, or charge states) that are not normalized; throughput depends heavily on spectrum complexity.
- When the processing pipeline varies between libraries (e.g., different precursor tolerance, different intensity scaling methods); the result will not be a fair comparison.
- When you only care about peak annotation accuracy or spectral quality rather than computational cost; this skill measures speed, not correctness.

## Inputs

- MGF file (e.g., iPRG2012.mgf) containing mass spectrometry spectra
- Spectrum processing library (spectrum_utils, pymzML, pyOpenMS, or equivalent)
- Filter parameters: m/z range (min_mz, max_mz), intensity thresholds (min_intensity, max_num_peaks), scaling mode

## Outputs

- Median runtime per spectrum (wall-clock time in seconds)
- Processing rate (spectra per second) for each library
- Comparative throughput table with runtimes and rates across all tested libraries

## How to apply

Load a standardized dataset (e.g., iPRG2012.mgf) and apply identical preprocessing to each library: set m/z range to 100–1400 Da, remove precursor peak, filter intensity with min_intensity=0.05 and max_num_peaks=150, and scale intensities by square root. Measure wall-clock time using Python time.time() before and after the processing pipeline for each spectrum. Compute the processing rate as the inverse of the median runtime per spectrum (spectra/second). Repeat across libraries and tabulate median runtimes and throughput rates to identify which library has the lowest median latency per spectrum.

## Related tools

- **spectrum_utils** (Candidate library for throughput comparison; provides optimized spectrum processing operations.) — https://github.com/bittremieux/spectrum_utils/
- **pymzML** (Baseline library for comparative throughput measurement; mzML file parser.) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Comparative library for throughput benchmarking; OpenMS bindings for Python.)
- **pyteomics.mgf** (Dataset parsing and filtering (e.g., spectra with ≥10 peaks, valid charge states).)
- **Python time.time()** (Wall-clock timing mechanism for measuring execution duration per spectrum.)
- **NumPy, matplotlib, seaborn** (Statistical computation and visualization of throughput results.)

## Examples

```
import time; from pyteomics import mgf; from spectrum_utils import Spectrum; times = []; [times.append(time.time()) or spectrum.set_mz_range(100, 1400).remove_precursor_peak().filter_intensity(0.05, 150).scale_intensity('root') or times.append(time.time()) for spectrum in [Spectrum(s) for s in mgf.read('iPRG2012.mgf')]]; throughput = len(times) // 2 / (sum(times[i+1] - times[i] for i in range(0, len(times)-1, 2)) / (len(times) // 2))
```

## Evaluation signals

- Median runtime per spectrum for each library is computed and reported; verify that median is lower than mean (indicating outlier outliers are not distorting the result).
- Processing rates (spectra/second) are strictly the inverse of median runtimes; check dimensional consistency.
- All three libraries process the same filtered dataset with identical parameters (m/z range 100–1400 Da, min_intensity=0.05, max_num_peaks=150, square-root scaling) on each spectrum.
- Wall-clock measurements are collected for the full pipeline (load → filter → scale) and exclude I/O overhead; verify timing blocks exclude file read/write time outside the core processing loop.
- Throughput comparison table shows spectrum_utils median runtime is lower (faster) than both pymzML and pyOpenMS for the benchmark dataset.

## Limitations

- Throughput is hardware-dependent (CPU, memory, system load); results are only valid for the platform and system state on which measurements were taken.
- Processing rate varies with spectrum complexity (number of peaks, m/z range sparsity); single-dataset benchmarks may not generalize to other datasets with different peak distributions or precursor mass ranges.
- Memory allocations, library initialization, and garbage collection can introduce variance in per-spectrum timing; multiple runs and median aggregation reduce but do not eliminate this variance.
- The article provides the workflow design but does not report actual benchmark results; the finding states 'The provided document text does not contain reported throughput comparison results.'

## Evidence

- [other] For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root.: "apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root"
- [other] Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps.: "Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps"
- [other] Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library.: "Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency"
- [other] Load iPRG2012.mgf dataset and parse spectra using pyteomics.mgf.read, filtering to spectra with ≥10 peaks and valid charge states.: "Load iPRG2012.mgf dataset and parse spectra using pyteomics.mgf.read, filtering to spectra with ≥10 peaks and valid charge states"
