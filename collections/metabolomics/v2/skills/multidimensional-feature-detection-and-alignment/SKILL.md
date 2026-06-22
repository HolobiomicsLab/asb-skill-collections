---
name: multidimensional-feature-detection-and-alignment
description: Use when when you have acquired LC-IMS-MS/MS data (mzML or mzML.gz format) from multiple samples and need to detect features that exploit simultaneous separation in m/z, drift time, and retention time to improve detection sensitivity and reduce false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - Snakemake
  - ProteoWizard msconvert
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment with required dependencies.
- 'Install DEIMoS using `pip <https://pypi.org/project/pip/>`_: ``pip install -e .``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
schema_version: 0.2.0
---

# multidimensional-feature-detection-and-alignment

## Summary

Apply N-dimensional feature detection and cross-sample alignment to LC-IMS-MS/MS data to identify and characterize molecular features with improved sensitivity and confidence. DEIMoS implements persistent homology-based peak detection across m/z, drift time, and retention time dimensions, then aligns detected features across multiple samples while assigning mass, CCS, tandem spectra, and isotopic signatures.

## When to use

When you have acquired LC-IMS-MS/MS data (mzML or mzML.gz format) from multiple samples and need to detect features that exploit simultaneous separation in m/z, drift time, and retention time to improve detection sensitivity and reduce false positives. Use this skill especially when baseline noise or peak convolution artifacts are present, or when you need high-confidence feature matching across datasets.

## When NOT to use

- Input data are already preprocessed into aligned feature tables or consensus spectra — skip to downstream analysis (e.g., annotation, statistical testing).
- Instruments do not provide drift time or have only 1–2 separation dimensions — consider single-dimension peak picking instead.
- Data are in formats other than mzML/mzML.gz without conversion (e.g., raw vendor formats) — use ProteoWizard msconvert first.

## Inputs

- mzML.gz or mzML files with m/z, drift_time, retention_time accessions
- YAML configuration file specifying algorithm parameters (threshold, index factors)
- Multiple sample files for cross-sample alignment

## Outputs

- Aligned feature table (HDF5 or tabular format) with m/z, drift_time, retention_time, intensity
- Feature metadata: mass, collision cross section (CCS), tandem mass spectra (MS/MS), isotopic signatures
- Per-sample peak lists (MS1 and MS2) in HDF5 format

## How to apply

Load mzML.gz data by parsing instrument-specific CVaccession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time) to extract N-dimensional ion coordinates. Apply threshold filtering (default threshold=500) to remove low-intensity noise, then build indices from these factors. Apply persistent homology-based peak detection to identify local maxima in the m/z–drift_time–retention_time space that satisfy signal criteria across all three dimensions simultaneously. Align detected peaks across all input samples using multi-dimensional matching to maximize overlap confidence. Filter isotopic signatures to retain only those with ≥3 members to ensure statistical robustness. Output characterized features annotated with mass, CCS, fragmentation spectra, and isotope cluster membership.

## Related tools

- **DEIMoS** (Core Python API and CLI tool that implements N-dimensional feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution) — http://github.com/pnnl/deimos
- **Snakemake** (Workflow orchestration engine used to define and execute the feature detection and alignment DAG across multiple input files and parameter sweeps) — https://snakemake.readthedocs.io
- **ProteoWizard msconvert** (Converts mass spectrometry data from vendor formats to mzML for input to DEIMoS)
- **conda** (Environment and dependency manager for creating isolated Python environments with DEIMoS and required libraries)
- **pip** (Python package installer used to install DEIMoS from source)

## Examples

```
data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'}); ms1_peaks = deimos.peakpick.persistent_homology(data, dims=['mz', 'drift_time', 'retention_time'], threshold=500)
```

## Evaluation signals

- All expected output files are produced in output/ directory with correct naming scheme (one per input mzML file).
- Output HDF5 files contain populated datasets for m/z, drift_time, retention_time, and intensity with non-zero row counts matching detected peaks.
- Aligned feature table row counts are consistent across samples after alignment (same feature set present in each).
- Isotope signatures retained have ≥3 members per cluster; no singleton isotopes remain in final output.
- CCS calibration r-squared metric is ≥0.999, indicating high-fidelity linear fit to reference tune parameters.
- MS/MS spectral deconvolution produces reproducible tandem spectra with reduced baseline convolution noise compared to non-deconvolved spectra.

## Limitations

- DEIMoS is largely agnostic to acquisition instrumentation, but requires mzML format with populated CVaccessions for m/z, drift_time, and retention_time; instruments that do not provide drift time information cannot fully exploit N-dimensional separation benefits.
- Feature alignment confidence depends on sample similarity and parameter tuning; poor parameter choices (e.g., overly high threshold) may suppress weak features before alignment.
- No changelog is available in the repository, making it difficult to track breaking changes or newly supported CVaccessions across versions.
- Persistent homology-based peak detection is computationally intensive for very large datasets; memory and runtime scale with data dimensionality and sample count.

## Evidence

- [intro] N-dimensional algorithm implementations and improved detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
- [other] Persistent homology peak detection and accession parsing methodology: "DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500), index building from"
- [readme] Feature alignment and CCS calibration as core functionality: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [results] Isotope filtering criterion: "A good first screening is to only consider those isotopic signatures with at least 3 members"
- [intro] Multiple separation dimensions reduce convolution artifacts: "algorithm implementations simultaneously utilize all dimensions to (iii) mitigate convolution artifacts in tandem mass spectra"
- [readme] mzML format and accession requirements: "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
