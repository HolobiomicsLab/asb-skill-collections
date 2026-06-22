---
name: spectrum-processing-pipeline-construction
description: Use when you have raw mass spectrometry spectra (in MGF, mzML, or similar formats) that must undergo standardized preprocessing before library matching, similarity searching, or performance benchmarking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
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
  - Python time module
  techniques:
  - LC-MS
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

# spectrum-processing-pipeline-construction

## Summary

Construct an optimized mass spectrometry spectrum processing pipeline by chaining operations (m/z range normalization, precursor/noise removal, intensity filtering, and scaling) in a sequence designed for computational efficiency and reproducibility across multiple spectra. This skill is essential when preparing raw MS/MS spectra for downstream analysis such as spectral library matching or benchmarking.

## When to use

You have raw mass spectrometry spectra (in MGF, mzML, or similar formats) that must undergo standardized preprocessing before library matching, similarity searching, or performance benchmarking. The skill applies when you need to apply identical filtering and normalization steps to large batches of spectra and measure or report the consistency of processing.

## When NOT to use

- Input spectra are already preprocessed and normalized (e.g., from a processed spectral library); re-applying this pipeline would introduce redundant filtering.
- Analysis requires preservation of precursor peak intensity for quantification or charge state inference.
- Raw spectral data format is incompatible with the chosen parsing tool (e.g., attempting to use pymzML on MGF-only data without format conversion).

## Inputs

- mass spectrometry spectrum objects (e.g., pyteomics.mgf records, pymzML spectrum objects, or spectrum_utils Spectrum instances)
- spectrum dataset file (MGF, mzML, or equivalent format)
- precursor m/z tolerance and mode (Da or ppm)
- m/z range boundaries (min_mz, max_mz in Daltons)

## Outputs

- processed spectrum objects with normalized m/z ranges, removed precursor peaks, filtered low-intensity peaks, and scaled intensities
- processing rate metrics (median runtime per spectrum, throughput in spectra per second)
- consistent spectrum representation suitable for library matching or benchmarking

## How to apply

Define the processing pipeline as a sequence of four core operations applied uniformly to each spectrum: (1) set m/z range boundaries (typically 100–1400 Da) to remove out-of-range noise; (2) remove the precursor peak using a specified fragment tolerance (mass or ppm mode); (3) filter low-intensity noise peaks by setting a minimum intensity threshold (e.g., 0.05 relative to base peak) and a maximum peak count (e.g., 150 peaks); (4) scale peak intensities using a transformation (e.g., square root) to reduce dynamic range and improve signal-to-noise ratio. Apply these operations in this order to all spectra in the dataset using a vectorized or loop-based approach. Rationale: the order is important—range filtering first eliminates noise outside the analyte range, precursor removal eliminates the dominant peak that would otherwise skew intensity scaling, intensity filtering removes spurious low-abundance peaks before scaling, and scaling last ensures all peaks are on a consistent scale. Record wall-clock time or throughput (spectra per second) during pipeline execution to verify computational efficiency.

## Related tools

- **spectrum_utils** (Primary library providing Spectrum class and optimized processing methods (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity)) — https://github.com/bittremieuxlab/spectrum_utils
- **pymzML** (Alternative spectrum parsing and processing library for mzML files; used in comparative benchmarking) — https://github.com/pymzml/pymzML
- **pyteomics** (Utility library for parsing MGF and other mass spectrometry file formats)
- **Python time module** (Measurement of wall-clock execution time for pipeline performance profiling)

## Examples

```
from spectrum_utils.spectrum import Spectrum; from pyteomics import mgf; spectra = [Spectrum(s['m/z array'], s['intensity array'], s['params']) for s in mgf.read('iPRG2012.mgf')]; processed = [s.set_mz_range(100, 1400).remove_precursor_peak(0.05, 'Da').filter_intensity(0.05, 150).scale_intensity('root') for s in spectra]
```

## Evaluation signals

- All spectra in the output dataset have m/z values within the specified range (100–1400 Da); no m/z values fall outside this window.
- Precursor peak is absent from processed spectra (verify by checking that the peak at precursor m/z ± tolerance is removed).
- Peak count per spectrum does not exceed max_num_peaks threshold (e.g., ≤150); low-intensity peaks below min_intensity are removed.
- Intensity values are scaled and normalized (e.g., maximum intensity is root-scaled and consistent across spectra); verify by checking that intensity ranges are reduced compared to raw input.
- Processing rate (spectra per second) is consistent and reproducible across repeated runs on the same dataset; median runtime per spectrum is lower than alternative libraries (e.g., pymzML or pyOpenMS) on identical inputs.

## Limitations

- The pipeline assumes all input spectra have valid charge states and precursor m/z values; spectra with missing or invalid precursor information may cause errors or require explicit filtering before pipeline execution.
- The m/z range, intensity threshold, and maximum peak count are fixed hyperparameters; they must be tuned for specific instrument types, ionization methods, and analyte classes (e.g., peptides vs. metabolites) and are not automatically optimized.
- Intensity scaling (e.g., square root) is lossy and may obscure abundance information needed for quantitative analysis; this pipeline is designed for qualitative matching, not quantification.
- The pipeline does not address fragment ion annotation, charge state deconvolution, or other advanced preprocessing steps; it performs basic noise and range normalization only.

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] The pipeline includes explicit method calls for m/z range setting, precursor removal, intensity filtering, and scaling.: "spectrum.set_mz_range(min_mz=100, max_mz=1400), .remove_precursor_peak(fragment_tol_mass, fragment_tol_mode), .filter_intensity(min_intensity=0.05, max_num_peaks=50), .scale_intensity("root")"
- [other] The benchmark workflow applies identical processing steps to each library and measures wall-clock time per spectrum.: "For each library (spectrum_utils, pymzML, pyOpenMS), apply identical processing: set m/z range to 100–1400 Da, remove precursor peak, filter intensity (min_intensity=0.05, max_num_peaks=150), and"
- [other] Processing rate is computed as the inverse of median runtime per spectrum for each library.: "Compute processing rate (spectra per second) as the inverse of median runtime per spectrum for each library."
- [readme] The README confirms the core operations are available as methods on the Spectrum object.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
