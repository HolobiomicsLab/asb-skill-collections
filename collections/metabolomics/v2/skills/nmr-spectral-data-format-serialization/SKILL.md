---
name: nmr-spectral-data-format-serialization
description: Use when you have generated 1D FID time-domain data and Fourier-transformed frequency-domain 1H NMR spectra, or computed 2D COSY/HSQC correlation matrices, and need to write them to disk in a format that standard NMR software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetAssimulo 2
  - h5py
  - scipy.io.netcdf / netCDF4-python
  techniques:
  - NMR
derived_from:
- doi: 10.1093/bioinformatics/btaf045
  title: MetAssimulo 2.0
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metassimulo_2_0_cq
    doi: 10.1093/bioinformatics/btaf045
    title: MetAssimulo 2.0
  dedup_kept_from: coll_metassimulo_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf045
  all_source_dois:
  - 10.1093/bioinformatics/btaf045
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectral-data-format-serialization

## Summary

Serialize simulated 1D and 2D 1H NMR spectral arrays into standard data interchange formats (HDF5 or netCDF) to ensure compatibility with downstream NMR analysis pipelines and long-term data archival. This skill bridges NMR simulation engines and format-agnostic metabolomic workflows.

## When to use

You have generated 1D FID time-domain data and Fourier-transformed frequency-domain 1H NMR spectra, or computed 2D COSY/HSQC correlation matrices, and need to write them to disk in a format that standard NMR software (e.g., TopSpin, VNMR, MNova) and metabolomic analysis tools can read directly without re-parsing or reimplementation.

## When NOT to use

- Input is raw simulation parameters (spin systems, chemical shifts, J-values) rather than computed spectral arrays; use this skill only after Fourier transformation and multiplet convolution are complete.
- Downstream analysis requires real-time streaming or in-memory spectral access; HDF5/netCDF serialization introduces I/O latency unsuitable for interactive visualization loops.
- Target system is a proprietary NMR vendor format (JCAMP-DX, Bruker FID, Varian fid) with binary checksums or encryption; this skill produces open interchange formats only.

## Inputs

- 1D FID (time-domain free induction decay array, float32 or float64)
- 1D frequency-domain 1H NMR spectrum (intensity array after Fourier transform, float32 or float64)
- 2D COSY correlation matrix (real-valued, 2D float array)
- 2D HSQC/HMQC heteronuclear correlation matrix (complex or real-valued, 2D float array)
- Chemical shift axis (1D array, ppm units)
- Metabolite metadata (concentration, spin-system identifiers, J-coupling constants)

## Outputs

- HDF5 spectral file (.h5; hierarchical datasets for 1D and 2D spectra with metadata groups)
- netCDF spectral file (.nc; CF-compliant multidimensional array with dimension scales and coordinate variables)
- Spectral array integrity report (shape, dtype, axis bounds, metadata checksums)

## How to apply

After completing spectral simulation (step 4 for 1D and step 5 for 2D in the MetAssimulo 2 workflow), serialize the spectral arrays—including chemical shift axes, intensity values, and metadata (metabolite identities, J-coupling constants, pulse sequence parameters)—into HDF5 or netCDF files. HDF5 is preferred for hierarchical storage of multiple 2D datasets (e.g., individual COSY and HSQC experiments) and metadata trees; netCDF is standard for NMR archival and interchange with legacy systems. Use the appropriate library (e.g., h5py for HDF5, scipy.io.netcdf for netCDF) to write floating-point spectral arrays as multidimensional datasets, preserving axis labels and units (ppm for 1H chemical shift, Hz for frequency). Validate the output by confirming file integrity (readable by h5dump or ncdump utilities) and round-trip testing: reload the serialized file and verify spectral intensity and axis values match pre-serialization arrays to within machine precision.

## Related tools

- **MetAssimulo 2** (Web application that generates 1D and 2D NMR spectra and performs serialization to HDF5 or netCDF as final output step) — https://github.com/yanyan5420/MetAssimulo_2
- **h5py** (Python library for writing and reading HDF5 spectral arrays with hierarchical metadata storage)
- **scipy.io.netcdf / netCDF4-python** (Python library for writing netCDF-compliant spectral files with CF dimension scales)

## Examples

```
python3 apps/index.py -p Input/parameters.txt && # simulates spectra, then serializes to HDF5/netCDF as configured in parameters.txt
```

## Evaluation signals

- File is readable by standard utilities (h5dump for HDF5, ncdump for netCDF) without error or data corruption warnings.
- Round-trip validation: reload the serialized file and verify that spectral intensity arrays and chemical shift axes match the pre-serialization arrays to within machine epsilon (float32: ~1e-6, float64: ~1e-15).
- Metadata hierarchy is present and structured: metabolite identifiers, J-coupling constants, and pulse sequence parameters are recoverable from file inspection (h5ls or ncdump output).
- Axis dimensions are correctly labeled (e.g., 'ppm' for chemical shift, 'Hz' for frequency) and coordinate ranges are physically plausible (1H NMR: 0–12 ppm; 13C: 0–220 ppm for HSQC indirect dimension).
- File size is consistent with expected array sizes and compression ratio (if compression is applied, expected ~2–5× reduction for float32 NMR spectra).

## Limitations

- No support for vendor-specific binary NMR formats (Bruker FID, Varian fid, Agilent) or JCAMP-DX; output is limited to HDF5 and netCDF, which may require additional conversion for legacy instrument software.
- No integrated handling of nonuniform spectral arrays (e.g., variable-width bins from adaptive apodization); assumes regular gridding in both 1D and 2D.
- Metadata standardization (e.g., FAIR data provenance, experiment parameters) depends on user compliance; no automated schema validation or controlled vocabulary enforcement in current MetAssimulo 2 implementation.
- netCDF output may not preserve complex-valued 2D data (HSQC phase information) without ad-hoc separation into real and imaginary datasets; HDF5 is more flexible for complex arrays.

## Evidence

- [other] Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats.: "Save simulated 1D and 2D spectra as HDF5 or netCDF spectral arrays compatible with standard NMR data formats."
- [other] MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra.: "MetAssimulo 2 is a web application designed to simulate realistic 1D and 2D metabolomic 1H NMR spectra."
- [other] Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum.: "Combine individual metabolite spectra into a single 1D FID and apply Fourier transformation to produce frequency-domain 1H NMR spectrum."
- [other] For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution.: "For 2D spectra, compute 1H–1H correlation (COSY) or 1H–13C heteronuclear (HSQC/HMQC) multiplets using appropriate 2D pulse sequences and indirect-dimension evolution."
