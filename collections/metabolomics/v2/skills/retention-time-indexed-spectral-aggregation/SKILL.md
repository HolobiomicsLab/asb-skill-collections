---
name: retention-time-indexed-spectral-aggregation
description: Use when you have Thermo Fisher Scientific .raw files from an LC-MS experiment and need to extract spectral features (base-peak m/z, intensity, scan-level properties) indexed by retention time for downstream statistical analysis, method optimization, or diagnostic visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - RawFileReader
  - R
  - rawrr
  - MsBackendRawFileReader
  - rawDiag
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-indexed-spectral-aggregation

## Summary

Programmatically extract and aggregate spectral properties (m/z, intensity, scan metadata) indexed by retention time from Thermo Orbitrap raw files using rawrr's readIndex() and readSpectrum() functions. This skill enables direct access to MS1 or MS2 scan data without external conversion, facilitating modular end-to-end analysis pipelines in R.

## When to use

You have Thermo Fisher Scientific .raw files from an LC-MS experiment and need to extract spectral features (base-peak m/z, intensity, scan-level properties) indexed by retention time for downstream statistical analysis, method optimization, or diagnostic visualization. Use this when you require programmatic, reproducible access to raw spectral data without converting to intermediate formats like mzML.

## When NOT to use

- Input is already a converted mzML, netCDF, or other open exchange format—use standard mzR or MSnbase readers instead.
- You need only high-level statistical summaries and have no need for per-scan spectral detail—consider external preprocessing pipelines like MaxQuant or Skyline.
- Windows/Linux/macOS compatibility is not guaranteed for your environment—rawrr requires .NET runtime and RawFileReader assemblies; test platform support first.

## Inputs

- Thermo Fisher Scientific .raw file (binary proprietary format)
- MS level filter specification (e.g., ms == 1 for MS1, or scan type string)
- Scan number range or filter criteria (optional; default: all scans)

## Outputs

- data.frame or table with columns: scan_number, retention_time, m/z, intensity (or other extracted properties)
- CSV file or R object suitable for statistical analysis or visualization

## How to apply

Install the rawrr executable via rawrr::installRawrrExe(), then load the .raw file path using rawrr::sampleFilePath(). Call readIndex() on the raw file to generate a data.frame indexing all scans, including retention time and MS level. Subset the index to retain only scans of interest (e.g., ms == 1 for MS1-level scans, or specific scan types for targeted methods). Iterate over each selected scan number and call readSpectrum() to retrieve individual rawrrSpectrum objects. Extract desired properties—such as m/z and intensity at maximum intensity, or other scan-level metadata—from each spectrum object. Aggregate extracted values into a table indexed by scan number and retention time, then write to CSV or other tabular format for downstream analysis. The C# wrapper methods via RawFileReader provide compiled access to binary .raw data; extracted information is written to a temporary file, read back into memory, and parsed into R objects.

## Related tools

- **rawrr** (R package providing readIndex() and readSpectrum() functions to programmatically access spectral data from Thermo .raw files without external conversion) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C# wrapper) underlying rawrr, enabling direct binary access to proprietary Thermo raw files on Windows, Linux, and macOS) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Alternative MsBackend for Bioconductor Spectra package, integrating rawrr for on-disk access to raw files via standardized accessor functions) — https://github.com/cpanse/MsBackendRawFileReader
- **rawDiag** (Complementary R package for rational LC-MS method optimization and visualization of raw file diagnostics, uses RawFileReader for fast multiplatform reading) — https://github.com/fgcz/rawDiag

## Examples

```
library(rawrr); rawrr::installRawrrExe(); raw_file <- rawrr::sampleFilePath(); idx <- readIndex(raw_file); ms1_scans <- subset(idx, ms == 1); base_peaks <- do.call(rbind, lapply(ms1_scans$scan, function(s) { spec <- readSpectrum(raw_file, s); list(scan=s, rt=ms1_scans$RT[ms1_scans$scan==s], mz=spec@mz[which.max(spec@intensity)], intensity=max(spec@intensity)) })); write.csv(as.data.frame(base_peaks), 'base_peaks.csv')
```

## Evaluation signals

- Scan index data.frame contains expected columns: scan number, retention time, MS level; length matches total scans in raw file.
- Subsetting for MS1 scans (ms == 1) reduces index to plausible count for the experiment (e.g., ~24,000 scans over 55 min run)
- Base-peak m/z and intensity values extracted per scan are physically plausible (m/z > 0, intensity ≥ 0) and consistent with instrument specifications (e.g., Orbitrap range 50–2000 m/z)
- Retention time values are monotonically increasing and fall within expected LC gradient window (e.g., 0–55 min for the example experiment)
- Output table row count matches count of selected scans; no missing or duplicated scan entries; CSV round-trips successfully

## Limitations

- Requires .NET runtime and RawFileReader assemblies; platform availability may be restricted and installation must be completed via rawrr::installRawrrExe().
- Access is limited to Thermo Fisher Scientific proprietary .raw files; other vendor formats (Waters, Bruker, ABSciex) are not supported.
- File I/O overhead is incurred because data extracted from binary .raw files is written to temporary location on disk, read back into memory, and parsed into R objects; this may be slower than in-memory conversion for very large raw files.
- Big computational proteomics capabilities in R remain in active development; memory efficiency and scalability for proteome-wide analyses have not yet been fully characterized.

## Evidence

- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [other] rawrr provides readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties: "readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties"
- [other] Generate the scan index as a data.frame using readIndex() on the raw file. Subset the index to retain only MS1-level scans (ms == 1). Iterate over each MS1 scan number and call readSpectrum() to retrieve individual spectrum objects.: "Generate the scan index as a data.frame using readIndex() on the raw file. Subset the index to retain only MS1-level scans (ms == 1). Iterate over each MS1 scan number and call readSpectrum()"
- [intro] A library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call. extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
- [results] By using the readIndex() function a data.frame that indexes all scans found in a raw file is returned: "By using the readIndex() function a data.frame that indexes all scans found in a raw file is returned"
- [results] Individual scans or scan collections can be read by the function readSpectrum(): "Individual scans or scan collections (sets) can be read by the function readSpectrum()"
- [results] The example LC-MS run resulted in 24,221 scans over 55 minutes: "The example LC-MS run resulted in 24,221 scans over 55 minutes"
