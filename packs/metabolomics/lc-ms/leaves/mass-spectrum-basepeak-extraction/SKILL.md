---
name: mass-spectrum-basepeak-extraction
description: Use when when you have Thermo Fisher Scientific .raw files from Orbitrap instruments and need to build a quantitative summary of MS1 acquisition intensity dynamics across a run—specifically, the m/z and intensity of the most intense peak in each MS1 scan.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - R
  - rawrr
  - MsBackendRawFileReader
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo
- Our implementation consists of two language layers, the top `R` layer and the hidden `C#` layer.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-basepeak-extraction

## Summary

Programmatically extract base-peak m/z and intensity values from individual MS1 scans in Thermo Orbitrap raw files using the rawrr package. This skill enables construction of scan-indexed base-peak tables without external file conversion, facilitating direct integration of raw spectral data into R-based proteomics pipelines.

## When to use

When you have Thermo Fisher Scientific .raw files from Orbitrap instruments and need to build a quantitative summary of MS1 acquisition intensity dynamics across a run—specifically, the m/z and intensity of the most intense peak in each MS1 scan. This is useful for quality control, retention time alignment, and rapid characterization of acquisition performance without full spectra processing.

## When NOT to use

- Input is already in a converted exchange format (mzML, netCDF, HDF5) — use that parser instead of re-reading the raw file.
- You need full spectral data (all peaks in each scan, not just the maximum) — use readSpectrum() directly without the max-intensity filter.
- Raw file is from a non-Thermo instrument (e.g., Bruker, Waters, Sciex) — rawrr does not support those formats.

## Inputs

- Thermo Fisher Scientific Orbitrap .raw file
- Scan index data.frame (output of readIndex())
- MS1-level scan numbers (integer vector, ms == 1)

## Outputs

- Base-peak table (data.frame with columns: scan_number, basepeak_mz, basepeak_intensity)
- CSV file of base-peak per-scan summary

## How to apply

Install the rawrr executable via rawrr::installRawrrExe(), then load the raw file and generate a scan index data.frame using readIndex(). Subset the index to retain only MS1-level scans (ms == 1). For each MS1 scan number, call readSpectrum() to retrieve the rawrrSpectrum object, then extract the m/z value and intensity at the maximum intensity point—these form the base-peak pair. Aggregate the scan number, base-peak m/z, and base-peak intensity into a two-column (or three-column) data.frame and write to CSV. The rationale is that base-peak intensity tracks ionization and transmission efficiency across the run, while base-peak m/z variation reveals scan-to-scan precursor mass shifts or contamination.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly to read spectra and metadata from .raw files; provides readIndex(), readSpectrum(), and accessor functions for extracting base-peak m/z and intensity) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided .NET assembly (C#) that implements low-level binary .raw file parsing; called by rawrr via system calls) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional: Bioconductor-compliant MsBackend that wraps rawrr to allow on-disk spectral data access via the Spectra package ecosystem) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
index <- rawrr::readIndex(rawrr::sampleFilePath()); ms1_idx <- subset(index, ms == 1); bp_table <- do.call(rbind, lapply(ms1_idx$scan, function(s) { sp <- rawrr::readSpectrum(rawrr::sampleFilePath(), scan = s); max_idx <- which.max(sp@intensity); data.frame(scan = s, bp_mz = sp@mz[max_idx], bp_int = sp@intensity[max_idx]) })); write.csv(bp_table, 'basepeak_ms1.csv')
```

## Evaluation signals

- Output base-peak table has one row per MS1 scan in the raw file; no missing or duplicate scan numbers.
- Base-peak m/z values fall within the instrument's calibrated mass range and show continuous or slow drift across the run (not random jumps).
- Base-peak intensity values are positive, lie within the instrument's dynamic range, and follow expected chromatographic envelope shape (rise and fall with elution).
- Comparison with external validation (e.g., ThermoRawFileParser or Skyline export of the same file) shows row-by-row agreement in scan numbers and base-peak m/z ± 0.01 Da and intensity ± 1%.
- CSV output is well-formed (no trailing commas, proper headers, numeric columns parse without errors).

## Limitations

- rawrr requires the RawFileReader .NET assembly, which must be installed and runs via system calls; performance degrades with very large raw files (>10 GB) due to file I/O overhead during spectrum parsing.
- Base-peak extraction is deterministic only if spectra have been calibrated; uncalibrated or badly calibrated raw files may show erratic m/z or intensity values.
- The skill currently does not handle MS2+ scans (only MS1 = 1); filtering by scan type (e.g., 'FTMS + c NSI Full ms2') is available but requires extension to the workflow.
- On Linux and macOS, the .NET runtime (Mono or .NET Core) must be installed separately; Windows support is native.

## Evidence

- [full_text] rawrr provides readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties, enabling construction of base-peak tables from raw files without external conversion.: "rawrr provides readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties, enabling construction of"
- [full_text] 1. Install rawrr executable using rawrr::installRawrrExe(). 2. Load the sample raw file path using rawrr::sampleFilePath(). 3. Generate the scan index as a data.frame using readIndex() on the raw file. 4. Subset the index to retain only MS1-level scans (ms == 1). 5. Iterate over each MS1 scan number and call readSpectrum() to retrieve individual spectrum objects. 6. Extract the base-peak m/z (mz value at maximum intensity) and intensity from each rawrrSpectrum object. 7. Aggregate base-peak m/z and intensity into a two-column table indexed by scan number and write to CSV.: "Iterate over each MS1 scan number and call readSpectrum() to retrieve individual spectrum objects. 6. Extract the base-peak m/z (mz value at maximum intensity) and intensity from each rawrrSpectrum"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] R functions request access to data from binary raw files via compiled C# wrapper methods using system calls: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [results] Individual scans or scan collections (sets) can be read by the function readSpectrum(): "Individual scans or scan collections (sets) can be read by the function readSpectrum()"
