---
name: raw-chromatography-data-parsing
description: Use when you have raw GC-MS output files (vendor formats or netCDF) from a chromatography instrument and need to prepare them for automated peak deconvolution and spectral analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MSHub
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-chromatography-data-parsing

## Summary

Load and parse raw gas chromatography–mass spectrometry (GC-MS) data from vendor or open formats (netCDF, mzML) to prepare input for downstream peak deconvolution and molecular networking. This skill extracts the underlying mass spectrum and retention time information needed for chemical component separation.

## When to use

You have raw GC-MS output files (vendor formats or netCDF) from a chromatography instrument and need to prepare them for automated peak deconvolution and spectral analysis. Use this skill when working with complex chemical mixtures where individual component spectra are obscured by overlapping chromatographic peaks.

## When NOT to use

- Input is already deconvolved spectra or a feature table (e.g., already peak-picked or aligned across samples).
- Data is from liquid chromatography–mass spectrometry (LC-MS) rather than GC-MS; the chromatographic and ionization properties differ.
- Working with already-processed spectral libraries or reference databases that do not require raw parsing.

## Inputs

- Raw GC-MS data files in vendor format (Agilent .D, Thermo .raw, etc.)
- Raw GC-MS data in netCDF format (.nc or .cdf)
- Raw GC-MS data in mzML format

## Outputs

- Parsed 3D GC-MS data structure (m/z, retention time, intensity matrix)
- Standardized spectral data in MGF or mzML format for downstream deconvolution

## How to apply

Load raw GC-MS files in netCDF or vendor format using MSHub or compatible I/O libraries that support those formats. Parse the 3D data structure (m/z, retention time, intensity) to extract mass spectra across the chromatographic dimension. Validate that the parsed output preserves the full m/z range, retention time alignment, and intensity calibration required by downstream deconvolution algorithms. The parsing step is essential because raw vendor formats often compress or obscure peak structure; converting to a standardized intermediate (such as mzML or netCDF if not already in that format) ensures compatibility with the auto-deconvolution module.

## Related tools

- **MSHub** (Core deconvolution engine that consumes parsed GC-MS data and resolves overlapping chromatographic peaks into individual component mass spectra) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Parsed data retains the full m/z range (typically 50–1000 m/z) with no artifacts or truncation.
- Retention time axis is monotonically increasing and covers the full chromatographic run duration.
- Intensity values span the expected dynamic range for the instrument (typically 10³–10⁷ counts); values <0 or NaN indicate parsing failure.
- Output format (MGF or mzML) validates against schema and is accepted without error by the MSHub auto-deconvolution module.
- Spot-check: manually inspect one parsed spectrum at a known retention time (e.g., from a standard compound) to confirm m/z peaks match reference spectra.

## Limitations

- Vendor format parsers are instrument-specific and may require proprietary libraries (e.g., Agilent ChemStation, Thermo TuneLab) that are not open source.
- netCDF parsing assumes standard encoding of the 3D data structure; non-standard or corrupted netCDF files may fail to parse or yield incorrect m/z/RT alignment.
- Baseline noise and instrument artifacts (electrical spikes, column bleed) are preserved during parsing and must be handled by downstream filtering in the deconvolution step.
- Very large raw files (>1 GB) may exhaust memory during parsing; streaming or chunked I/O may be required.

## Evidence

- [other] Load raw GC-MS files (netCDF or vendor format) from the companion repository or deposited dataset.: "Load raw GC-MS files (netCDF or vendor format) from the companion repository or deposited dataset."
- [other] Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis.: "Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis."
- [other] The manuscript describes auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis, with implementation available in the companion repository.: "auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
- [readme] This is a companion repository to the following manuscript on auto-deconvolution and molecular networking of GC-MS data.: "This is a companion repository to the following manuscript: ... Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data"
