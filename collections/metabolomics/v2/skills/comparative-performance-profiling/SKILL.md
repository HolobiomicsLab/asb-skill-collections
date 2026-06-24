---
name: comparative-performance-profiling
description: 'Use when when you have implemented a new or optimized mass spectrometry
  data processing library and need to demonstrate its computational advantage over
  established alternatives (e.g., pymzML, pyOpenMS) on real proteomics data. Trigger
  on availability of: (1) a common input dataset (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
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
  - spectrum_utils
  - pyteomics.mgf
  - Python timeit / wall-clock timer
  - matplotlib / seaborn
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- pymzML (version 2.5.2)
- pyOpenMS (version 2.7.0)
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
- import seaborn as sns
- Spectrum processing in spectrum_utils has been optimized for computational efficiency
  using [NumPy](https://www.numpy.org/)
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

# comparative-performance-profiling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Measure and compare spectrum processing throughput (spectra per second) across multiple libraries under identical filtering and normalization conditions to quantify computational efficiency gains. This skill applies standardized workflows to competing tools to produce boxplots and summary statistics that reveal performance differences.

## When to use

When you have implemented a new or optimized mass spectrometry data processing library and need to demonstrate its computational advantage over established alternatives (e.g., pymzML, pyOpenMS) on real proteomics data. Trigger on availability of: (1) a common input dataset (e.g., MGF file with thousands of spectra), (2) functionally equivalent processing implementations in all candidate libraries, and (3) a need to quantify per-spectrum latency or throughput in a standardized way.

## When NOT to use

- Input spectra are already heavily preprocessed or differ in filtering history; preprocessing disparities will confound library-level performance differences.
- Candidate libraries implement functionally different processing logic (e.g., different precursor tolerance strategies); results will reflect feature trade-offs, not pure throughput.
- Goal is to profile memory usage, I/O latency, or full pipeline wall-clock time rather than per-spectrum algorithmic latency; this skill isolates core processing logic.

## Inputs

- MGF file (e.g., iPRG2012.mgf or similar proteomics dataset with ≥1000 spectra)
- Spectrum objects parsed by neutral library (e.g., pyteomics.mgf)
- Implementation of identical filtering workflow in each candidate library

## Outputs

- Per-spectrum processing times (milliseconds or seconds) for each library
- Boxplot visualization with log-scale y-axis comparing median and distribution across libraries
- Summary statistics (median, Q1, Q3, min, max) for each library

## How to apply

Load a shared MGF file and parse spectra using a neutral parser (e.g., pyteomics.mgf) to ensure fair input preparation. Filter valid spectra by criteria such as ≥10 peaks and presence of charge state. Implement identical processing workflows in each library: set m/z range (e.g., 100–1400 Da), remove precursor peak (with tolerance, e.g., 0.02 Da), filter by base peak intensity threshold (e.g., 5%), cap peak count (e.g., 150 peaks), and apply square-root intensity scaling. Use Python's timeit or wall-clock timing to measure per-spectrum processing latency for each library across all valid spectra. Generate a boxplot on logarithmic scale to visualize median, quartiles, and outliers for each library. Rationale: standardized filtering and normalization steps ensure results reflect algorithmic efficiency (e.g., NumPy/Numba optimization) rather than feature differences; log-scale plots reveal both absolute timing and distributional tail behavior.

## Related tools

- **spectrum_utils** (optimized candidate library being profiled; core implementation using NumPy and Numba for efficient spectrum filtering and scaling) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (reference competitor library for throughput comparison) — https://github.com/pymzml/pymzML
- **pyOpenMS** (reference competitor library for throughput comparison)
- **pyteomics.mgf** (neutral spectrum file parser to ensure fair input preparation across all libraries)
- **Python timeit / wall-clock timer** (measurement tool for per-spectrum latency collection)
- **matplotlib / seaborn** (visualization of boxplot comparisons on log-scale y-axis)
- **NumPy** (performance-critical numerics underlying spectrum_utils optimization)

## Examples

```
import time; from pyteomics import mgf; spectra = list(mgf.read('iPRG2012.mgf')); valid = [s for s in spectra if len(s['m/z array']) >= 10 and 'params' in s]; times_su = []; times_pymzml = []; times_pyopenms = []; 
for spec in valid: 
  t0 = time.perf_counter(); spectrum_utils.set_mz_range(spec, 100, 1400).remove_precursor_peak(0.02, 'Da').filter_intensity(0.05, 150).scale_intensity('root'); times_su.append(time.perf_counter() - t0);
import matplotlib.pyplot as plt; plt.boxplot([times_su, times_pymzml, times_pyopenms], yscale='log'); plt.ylabel('Time (s)'); plt.show()
```

## Evaluation signals

- All three libraries process the same set of filtered spectra (identical ≥10 peaks, charge state, and m/z range 100–1400) under identical parameter settings (0.02 Da precursor tolerance, 5% base peak intensity, 150 peak cap, square-root scaling).
- Per-spectrum processing times for each library are normally or log-normally distributed; median and quartiles are visibly distinct on boxplot, indicating real separation rather than measurement noise.
- spectrum_utils median per-spectrum latency is lower than pymzML and pyOpenMS by at least a factor consistent with NumPy/Numba optimization claims (typically 2–5× on modern hardware).
- Outliers and tail behavior (Q3, max) are consistent across replicates, indicating stable timing; no individual spectrum shows anomalous latency for a single library.
- Total processing time across all valid spectra scales linearly with spectrum count, confirming O(n) complexity per library.

## Limitations

- Performance depends on hardware (CPU cores, RAM bandwidth, cache size); results may not transfer to different platforms or cloud environments.
- MGF file I/O (disk read, parsing overhead) is excluded; total wall-clock time will include this component, which may dominate on slow I/O or very large files.
- Only measures algorithmic latency for the specific workflow tested (precursor removal, intensity filtering, scaling); other operations (e.g., fragment annotation with ProForma, spectrum plotting) are not profiled.
- Peak memory usage and GC overhead are not directly measured; library with lower per-spectrum latency may have higher total memory footprint.
- Results are sensitive to spectrum characteristics (charge state distribution, number of peaks, intensity range); heterogeneous datasets or edge-case spectra may show different ranking than median case.

## Evidence

- [other] spectrum_utils version 0.4.0 is reported to be faster than alternative libraries pymzML version 2.5.2 and pyOpenMS version 2.7.0.: "spectrum_utils version 0.4.0 is reported to be faster than alternative libraries pymzML version 2.5.2 and pyOpenMS version 2.7.0."
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba.: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [other] Load MGF file and parse spectra, filter valid spectra, apply identical processing workflows (m/z range, precursor removal, intensity filtering, scaling), collect runtimes, and generate boxplot on log scale.: "1. Load MGF file (iPRG2012.mgf) and parse spectra using pyteomics.mgf. 2. Filter valid spectra (≥10 peaks, charge state present). 3. Time spectrum_utils processing: set m/z range to 100–1400, remove"
- [intro] Common spectrum processing operations optimized for computational efficiency: precursor & noise peak removal, intensity filtering, intensity scaling.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
