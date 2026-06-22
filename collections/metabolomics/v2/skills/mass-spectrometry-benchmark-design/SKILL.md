---
name: mass-spectrometry-benchmark-design
description: Use when when claiming that one mass spectrometry processing library achieves higher throughput than competitors, or when evaluating whether a new or optimized implementation delivers the expected computational efficiency gains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  techniques:
  - mass-spectrometry
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

# mass-spectrometry-benchmark-design

## Summary

Design and execute a controlled benchmark experiment to compare the throughput (spectra per second) of multiple mass spectrometry data processing libraries on identical datasets and processing pipelines. This skill validates performance claims by measuring wall-clock execution time and computing processing rates under standardized conditions.

## When to use

When claiming that one mass spectrometry processing library achieves higher throughput than competitors, or when evaluating whether a new or optimized implementation delivers the expected computational efficiency gains. The benchmark is appropriate when you need to isolate the effect of library choice (spectrum_utils vs. pymzML vs. pyOpenMS) by holding dataset, preprocessing steps, and parameters constant.

## When NOT to use

- When the input spectra are already fully processed or cached in memory; benchmark measures disk I/O and parsing time, so pre-loaded data will not reflect real-world library performance differences.
- When comparing libraries with fundamentally different APIs or data structures that require different preprocessing workflows; the benchmark requires identical processing chains to isolate library efficiency.
- When the target library is still under active development or the versions being compared are not stable releases; version mismatch or unreleased code can invalidate throughput claims.

## Inputs

- mass spectrometry spectrum file in MGF format (iPRG2012.mgf or equivalent benchmark dataset)
- list of library names and versions to compare (e.g., spectrum_utils v0.4.0, pymzML v2.5.2, pyOpenMS v2.7.0)
- processing parameters: m/z range (min_mz, max_mz), fragment tolerance (fragment_tol_mass, fragment_tol_mode), intensity filter thresholds (min_intensity, max_num_peaks), scaling method

## Outputs

- median runtime per spectrum (seconds) for each library
- throughput rate (spectra per second) for each library
- comparison table with library names, versions, median runtimes, and throughput ranks
- visualization (bar plot or line chart) showing runtime or throughput comparison

## How to apply

Load a common benchmark dataset (e.g., iPRG2012.mgf) and filter spectra to a consistent quality criterion (≥10 peaks, valid charge states). For each library under comparison, apply identical processing steps in sequence: set m/z range to 100–1400 Da, remove precursor peak using specified fragment tolerance, filter low-intensity peaks (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root. Measure wall-clock time using Python time.time() before and after processing each spectrum. Compute the median runtime per spectrum and convert to throughput (spectra per second) as the inverse of median runtime. Tabulate results side-by-side and verify that the target library's median runtime is lower than competing libraries. Visualize results with bar plots showing median runtimes and throughput rates for clarity.

## Related tools

- **spectrum_utils** (primary library under evaluation; provides optimized spectrum processing methods (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity) that are benchmarked for throughput) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (competing library for throughput comparison; alternative implementation of mzML parsing and spectrum processing) — https://github.com/pymzml/pymzML
- **pyOpenMS** (competing library for throughput comparison; alternative C++ binding library for spectrum processing and MS data handling)
- **pyteomics.mgf** (utility for initial spectrum loading and filtering from MGF files; used to parse input dataset and select spectra with ≥10 peaks and valid charge states)
- **Python time module** (timing utility; measures wall-clock time before and after processing each spectrum to compute median runtime and throughput)
- **matplotlib** (visualization library for creating bar plots and comparison charts of throughput results)
- **seaborn** (statistical visualization library for enhanced visual presentation of benchmark comparison tables and plots)
- **NumPy** (numerical array library for computing median runtimes and throughput statistics)

## Examples

```
import time; from pyteomics import mgf; spectra = [s for s in mgf.read('iPRG2012.mgf') if len(s['m/z array']) >= 10]; timings = []; for s in spectra: start = time.time(); s.set_mz_range(min_mz=100, max_mz=1400); s.remove_precursor_peak(fragment_tol_mass=0.1, fragment_tol_mode='Da'); s.filter_intensity(min_intensity=0.05, max_num_peaks=150); s.scale_intensity('root'); timings.append(time.time() - start); median_time = sorted(timings)[len(timings)//2]; throughput = 1.0 / median_time; print(f'spectrum_utils: {throughput:.2f} spectra/sec')
```

## Evaluation signals

- Median runtime is computed correctly as the 50th percentile of per-spectrum wall-clock times; verify no outliers dominate the calculation (e.g., check 25th and 75th percentiles are similar in magnitude).
- Throughput (spectra/second) is the reciprocal of median runtime and is dimensionally consistent; verify units and magnitude are reasonable (e.g., >1 spectrum/second for modern libraries on standard hardware).
- All three libraries process the same filtered spectrum set (same m/z range 100–1400, same intensity filter thresholds, same precursor tolerance); verify input counts and processing parameters are logged and match across comparisons.
- Reported library versions match the version strings in pip/conda metadata or GitHub tags; verify that v0.4.0, v2.5.2, and v2.7.0 are the exact installed versions used for timing.
- Target library (spectrum_utils) throughput exceeds both comparison libraries by a visible margin (e.g., >20% faster median time or >20% higher spectra/second); verify the ranking is consistent across multiple benchmark runs or datasets.

## Limitations

- Wall-clock timing is sensitive to system load, CPU frequency scaling, and memory pressure; results may vary significantly across machines or runs. Recommend running multiple iterations and reporting statistical summaries (median ± interquartile range).
- Benchmark measures only the named processing operations (m/z filtering, precursor removal, intensity filtering, scaling); it does not include overhead from spectrum I/O, data structure initialization, or memory allocation. True end-to-end latency will be higher.
- MGF format parsing and spectrum object construction overhead is library-specific and may dominate or reduce the impact of the core processing differences. Benchmark results may not generalize to other file formats (mzML, mzXML) where parsing complexity differs.
- The choice of processing parameters (e.g., min_intensity=0.05, max_num_peaks=150) and m/z range may favor one library over another; results are not parameter-invariant. Always document the exact configuration and consider sensitivity analysis.
- No changelog is publicly available for some libraries, making it difficult to verify whether performance improvements between versions are due to algorithmic changes or dependency updates. Version comparisons may conflate library changes with external factors.

## Evidence

- [intro] spectrum_utils provides common spectrum processing operations optimized for computational efficiency: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] benchmark workflow applies identical processing pipeline to spectra from the same dataset across libraries: "For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and"
- [other] throughput is computed as the inverse of median per-spectrum runtime: "Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library."
- [other] wall-clock timing is measured using Python time.time() utility: "Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps."
- [other] success criterion is that target library median runtime is lower than competitors: "Tabulate median runtimes and throughput rates; verify spectrum_utils median is lower than both pymzML and pyOpenMS."
- [other] input dataset is filtered to quality criteria before benchmarking: "Load iPRG2012.mgf dataset and parse spectra using pyteomics.mgf.read, filtering to spectra with ≥10 peaks and valid charge states."
