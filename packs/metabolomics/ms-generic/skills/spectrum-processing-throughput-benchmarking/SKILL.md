---
name: spectrum-processing-throughput-benchmarking
description: Use when when selecting a spectrum processing library for high-throughput proteomics or metabolomics workflows, or when optimizing an existing pipeline for computational efficiency. Apply this skill when you have access to representative raw MS data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - spectrum_utils
  - pymzML
  - pyOpenMS
  - Python
  - seaborn
  - NumPy
  - pyteomics
  - pyteomics.mgf
  - matplotlib
  techniques:
  - mass-spectrometry
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

# spectrum-processing-throughput-benchmarking

## Summary

Measure and compare the per-spectrum processing throughput (spectra per second) of different mass spectrometry data processing libraries under identical filtering and scaling operations. This skill establishes whether one library outperforms alternatives for production workflows.

## When to use

When selecting a spectrum processing library for high-throughput proteomics or metabolomics workflows, or when optimizing an existing pipeline for computational efficiency. Apply this skill when you have access to representative raw MS data (e.g., MGF files with ≥10-peak spectra and charge state metadata) and need empirical evidence of which library (e.g., spectrum_utils, pymzML, pyOpenMS) achieves the fastest median per-spectrum processing time under your intended filtering regime.

## When NOT to use

- Input spectra do not meet validation criteria (fewer than 10 peaks, missing charge state, or incompatible format) — standardize or filter data first.
- Libraries are called with non-identical parameter sets or filtering chains — differences in latency will confound throughput comparison.
- Target use case does not require per-spectrum throughput optimization (e.g., single-analysis reporting, exploratory research) — simpler criteria (e.g., usability, accuracy) may be more relevant.

## Inputs

- MGF (Mascot Generic Format) file containing tandem MS spectra
- Spectrum dataset with charge state and intensity metadata
- List of candidate spectrum processing libraries (e.g., spectrum_utils v0.4.0, pymzML v2.5.2, pyOpenMS v2.7.0)

## Outputs

- Per-spectrum processing time measurements (milliseconds or seconds per spectrum) for each library
- Boxplot visualization comparing median, quartiles, and distribution of processing times on log scale
- Summary statistics (median, IQR, outliers) by library

## How to apply

Load a representative dataset (e.g., iPRG2012.mgf) and parse spectra to identify valid candidates (≥10 peaks, charge state present). For each candidate library, apply an identical processing chain: restrict m/z range (e.g., 100–1400), remove precursor peak (e.g., 0.02 Da tolerance), filter by intensity threshold (e.g., 5% base peak intensity, max 150 peaks), and apply square-root intensity scaling. Time each library's execution across all valid spectra using Python's standard timing utilities. Collect per-spectrum runtimes, compute median and distribution statistics, and visualize results using a boxplot on log scale to account for outliers and variance. The library with the lowest median processing time and tightest interquartile range under these standardized conditions is preferred for throughput-critical applications.

## Related tools

- **spectrum_utils** (Primary candidate library for spectrum processing throughput benchmarking; provides precursor removal, intensity filtering, and square-root scaling operations optimized for computational efficiency using NumPy and Numba) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (Comparative library for benchmarking; parses mzML/MGF spectra and applies noise removal, normalization, and intensity scaling for throughput comparison) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Comparative library for benchmarking; provides spectrum filtering, normalization, and peak restriction operations for throughput measurement) — https://pyopenms.readthedocs.io/
- **pyteomics.mgf** (MGF file parser used to load and extract spectra from raw dataset prior to benchmarking)
- **NumPy** (Underlying vectorized computation engine for spectrum_utils processing efficiency) — https://www.numpy.org/
- **matplotlib** (Visualization library for generating boxplot comparisons of per-spectrum processing times across libraries)
- **seaborn** (Statistical visualization library for enhanced boxplot rendering and distribution summary)

## Examples

```
import time; from pyteomics import mgf; from spectrum_utils.spectrum import Spectrum; import numpy as np
spectra = [s for s in mgf.read('iPRG2012.mgf') if len(s['m/z array']) >= 10]
times = []
for sp in spectra:
  s = Spectrum(mz=sp['m/z array'], intensity=sp['intensity array'], precursor_mz=sp['params']['pepmass'][0])
  t0 = time.time()
  s.set_mz_range(100, 1400); s.remove_precursor_peak(0.02, 'Da'); s.filter_intensity(0.05, 150); s.scale_intensity('root')
  times.append(time.time() - t0)
print(f'Median: {np.median(times):.6f}s/spectrum')
```

## Evaluation signals

- All valid spectra (≥10 peaks, charge state present) are successfully processed by each library without exception or timeout.
- Identical preprocessing chain (m/z range 100–1400, precursor removal at 0.02 Da, 5% intensity filter, max 150 peaks, square-root scaling) is applied to each library with no functional deviations.
- Per-spectrum runtimes are measured consistently (same hardware, same Python environment, same system load conditions) for fair comparison.
- Median processing time for spectrum_utils is lower than pymzML and pyOpenMS under the standardized pipeline; interquartile range narrows relative to competitors, indicating more predictable performance.
- Boxplot on log scale shows no pathological outliers (e.g., >10× median) that would indicate memory thrashing or I/O contention affecting a single library.

## Limitations

- Throughput benchmarks are hardware- and environment-dependent; results may not generalize across different CPU architectures, memory configurations, or system load profiles.
- Comparison is specific to the versions tested (e.g., spectrum_utils v0.4.0, pymzML v2.5.2, pyOpenMS v2.7.0); library performance may improve or degrade in future releases.
- Benchmark uses a single representative dataset (iPRG2012.mgf); results may not reflect throughput on datasets with different spectral complexity, charge state distributions, or peak density.
- Identical parameter sets across libraries may not represent each library's optimal tuning; some libraries may expose additional or alternative filtering modes that could alter relative performance.
- Per-spectrum latency does not capture memory overhead, initialization cost, or I/O throughput; for large-scale workflows, end-to-end wall-clock time on complete pipelines should also be measured.

## Evidence

- [other] Comparison of library versions and metrics: "spectrum_utils version 0.4.0 is reported to be faster than alternative libraries pymzML version 2.5.2 and pyOpenMS version 2.7.0"
- [other] Spectrum filtering and preprocessing pipeline: "set m/z range to 100–1400, remove precursor peak (0.02 Da tolerance), filter by 5% base peak intensity (max 150 peaks), and scale by square root"
- [other] Computational efficiency optimization approach: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba"
- [other] Benchmarking workflow and data collection: "Collect runtimes for all three libraries across all valid spectra. Generate boxplot comparing median and distribution of per-spectrum processing times (log scale)"
- [other] Visualization and output presentation: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency"
