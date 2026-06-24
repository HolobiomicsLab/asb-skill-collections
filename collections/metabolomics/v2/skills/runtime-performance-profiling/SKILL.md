---
name: runtime-performance-profiling
description: 'Use when when you need to empirically validate that one mass spectrometry
  data processing library achieves higher throughput than competing alternatives.
  Specifically: you have multiple candidate libraries (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3375
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
  - Python time module
  - matplotlib / seaborn
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# runtime-performance-profiling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Measure and compare wall-clock processing time and throughput (spectra per second) across competing libraries on identical benchmark datasets and identical processing pipelines. This skill validates computational efficiency claims by quantifying median runtimes and deriving processing rates.

## When to use

When you need to empirically validate that one mass spectrometry data processing library achieves higher throughput than competing alternatives. Specifically: you have multiple candidate libraries (e.g., spectrum_utils, pymzML, pyOpenMS) that perform similar operations, you have access to a shared benchmark dataset (e.g., iPRG2012.mgf), and you want to measure which processes spectra fastest under identical filtering and normalization conditions.

## When NOT to use

- The libraries being compared perform fundamentally different processing steps or operate on different spectrum formats—use only when pipelines are identical.
- You are profiling memory usage, I/O overhead, or initialization cost rather than per-spectrum processing speed; use memory profilers or I/O benchmarks instead.
- The benchmark dataset is small (< 100 spectra) or unrepresentative of real-world datasets; results may not generalize.

## Inputs

- Mass spectrometry spectrum dataset in MGF or mzML format (e.g., iPRG2012.mgf)
- Three or more candidate spectrum processing libraries (e.g., spectrum_utils v0.4.0, pymzML v2.5.2, pyOpenMS v2.7.0)
- Filtering criteria (minimum peaks, charge state validity, m/z range bounds, intensity thresholds)
- Python environment with time module and candidate libraries installed

## Outputs

- Table of median runtimes per spectrum for each library (in milliseconds or seconds)
- Table of throughput rates (spectra per second) for each library
- Comparison verification: boolean or ratio confirming target library is fastest
- Optional: time-series plots or box plots of per-spectrum runtimes by library

## How to apply

Load the benchmark dataset (e.g., iPRG2012.mgf) and parse spectra using a neutral parser (e.g., pyteomics.mgf.read), filtering to spectra with ≥10 peaks and valid charge states. For each candidate library, apply an identical processing pipeline: set m/z range to 100–1400 Da, remove the precursor peak, apply intensity filtering (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root. Measure wall-clock time using Python time.time() immediately before and after each spectrum's processing steps. Compute the median runtime per spectrum for each library, then calculate the processing rate as the inverse of that median (spectra per second). Tabulate results and confirm that the target library's median runtime is lower and throughput is higher than all competing libraries. The rationale is that identical preprocessing ensures fair comparison; median (rather than mean) mitigates outliers; and wall-clock measurement captures real-world computational cost.

## Related tools

- **spectrum_utils** (Target library being validated for computational efficiency; provides optimized spectrum loading, filtering, and scaling operations) — https://github.com/bittremieux/spectrum_utils/
- **pymzML** (Baseline/competing library for throughput comparison; parses mzML format) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Baseline/competing library for throughput comparison; OpenMS Python bindings)
- **pyteomics** (Neutral spectrum file parser used to load and pre-filter benchmark dataset (MGF reader))
- **Python time module** (Wall-clock timing via time.time() before and after spectrum processing)
- **NumPy** (Compute median runtimes and derive throughput statistics)
- **matplotlib / seaborn** (Optional visualization of runtime distributions and throughput comparisons)

## Examples

```
import time
from pyteomics.mgf import read
from spectrum_utils.spectrum import Spectrum

spectra = [s for s in read('iPRG2012.mgf') if len(s['m/z array']) >= 10]
start = time.time()
for spec_dict in spectra:
    spec = Spectrum(spec_dict['precursor_mz'], spec_dict['m/z array'], spec_dict['intensity array'], spec_dict['precursor_charge'])
    spec.set_mz_range(100, 1400)
    spec.remove_precursor_peak(0.1, 'Da')
    spec.filter_intensity(min_intensity=0.05, max_num_peaks=150)
    spec.scale_intensity('root')
elapsed = time.time() - start
throughput = len(spectra) / elapsed
print(f'Median time per spectrum: {elapsed/len(spectra):.6f}s, Throughput: {throughput:.1f} spectra/sec')
```

## Evaluation signals

- Median runtime per spectrum for the target library is strictly lower than all competing libraries (no ties or inversions).
- Throughput (spectra/second) for the target library is the highest across all candidates; verify by computing 1/median_runtime for each library.
- Per-spectrum processing times are reproducible across multiple runs; coefficient of variation (std / mean) of median runtimes across replicates is < 5% for each library.
- All spectra in the benchmark dataset survive the identical filtering pipeline (≥10 peaks, valid charge state) and are successfully processed by all three libraries with no errors or missing output.
- Plot of per-spectrum runtimes shows no systematic outliers (e.g., a single spectrum 10× slower than others) that would invalidate the median; outliers should be documented if present.

## Limitations

- Results are dataset-specific: throughput on iPRG2012.mgf may not reflect performance on other datasets with different spectrum density, m/z ranges, or complexity.
- Wall-clock timing is sensitive to system load, CPU frequency scaling, and other processes; runs should be conducted with minimal concurrent activity.
- The chosen filtering thresholds (min_intensity=0.05, max_num_peaks=150, m/z 100–1400) directly affect processing cost; changing these will change the relative ranking of libraries.
- Library versions are fixed (e.g., spectrum_utils v0.4.0); performance improvements in later releases may alter conclusions.
- No changelog found in the article; version history and optimization details are not fully documented.

## Evidence

- [other] For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and scale intensities by square root.: "For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and"
- [other] Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps.: "Measure wall-clock time per spectrum for each library using Python time.time() before and after processing steps."
- [other] Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library.: "Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library."
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [readme] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
