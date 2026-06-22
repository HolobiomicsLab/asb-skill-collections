---
name: ms1-scan-extraction-and-filtering
description: Use when you have a Thermo Fisher Scientific .raw file from an Orbitrap instrument and need to programmatically retrieve MS1 spectral attributes (base-peak m/z, intensity, retention time) for downstream statistical analysis or quality control in R, rather than relying on external preprocessing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - R
  - RawFileReader
  - MsBackendRawFileReader
  - Bioconductor ExperimentHub
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- The `rawrr` executable will run out of the box
- '`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods'
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
- methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_cq
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

# MS1 scan extraction and filtering

## Summary

Extract base-peak m/z and intensity values from MS1-level scans in Thermo Fisher Scientific raw files and organize them into tabular data frames using rawrr accessor functions. This skill closes the gap for direct raw data reading in R, enabling modular end-to-end proteomics pipeline development without intermediate format conversion.

## When to use

You have a Thermo Fisher Scientific .raw file from an Orbitrap instrument and need to programmatically retrieve MS1 spectral attributes (base-peak m/z, intensity, retention time) for downstream statistical analysis or quality control in R, rather than relying on external preprocessing tools or exchange format conversion.

## When NOT to use

- Input data is already in an exchange format (mzML, netCDF) or has been preprocessed by external tools like MaxQuant — use standard R libraries (MSnbase, Spectra) instead.
- You require MS2 or higher-order fragmentation scan data — this skill is specific to MS1-level scans; use ms_level==2 or higher in the filter instead.
- You need only summary statistics (total ion current, scan duration) without individual spectral attributes — use readFileHeader() or readChromatogram() instead.

## Inputs

- Thermo Fisher Scientific .raw binary file (e.g., 20181113_010_autoQC01.raw from MassIVE MSV000086542)
- Scan index data frame (output from readIndex())
- MS level filter criterion (ms_level == 1)

## Outputs

- Data frame with columns: scan index, base-peak m/z, base-peak intensity
- rawrrSpectrum objects (intermediate, containing m/z and intensity vectors)

## How to apply

Install the rawrr executable using rawrr::installRawrrExe(), then load the raw file and generate a scan index via readIndex(). Subset the index to retain only ms_level==1 scans. Iterate through filtered scan numbers and call readSpectrum() on each to retrieve spectral data objects. Use rawrr's accessor functions ($ and [[ operators) to extract the maximum intensity m/z value and corresponding intensity from each rawrrSpectrum object. Aggregate the extracted base-peak m/z and intensity pairs with scan indices into a data frame. The rationale is that rawrr wraps the vendor-provided RawFileReader .NET API, enabling direct access to binary raw files without unfavorable conversion to exchange formats like mzML, while aligning with R conventions through non-standard objects (mass spectrum) familiar to analytical scientists.

## Related tools

- **rawrr** (Provides R accessor functions ($, [[) and reader functions (readIndex, readSpectrum) to programmatically extract and subset MS1 spectral data from Thermo .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly that rawrr wraps to access proprietary Thermo raw file binary format) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional integration layer providing rawrr as an on-disk MsBackend for the Bioconductor Spectra package, enabling further modular analysis) — https://github.com/fgcz/MsBackendRawFileReader
- **Bioconductor ExperimentHub** (Provides test raw files (EH4547) for reproducible workflow validation)

## Examples

```
library(rawrr); rawrr::installRawrrExe(); f <- '20181113_010_autoQC01.raw'; idx <- readIndex(f); idx_ms1 <- subset(idx, ms_level==1); bp <- data.frame(scan=idx_ms1$scan, mz=NA_real_, intensity=NA_real_); for(i in seq_len(nrow(bp))) { s <- readSpectrum(f, idx_ms1$scan[i]); bp$mz[i] <- s$mz[which.max(s$intensity)]; bp$intensity[i] <- max(s$intensity) }
```

## Evaluation signals

- Extracted data frame contains exactly one row per MS1 scan in the input file, with no duplicates or missing scans after filtering ms_level==1
- Base-peak m/z values are present and numeric; base-peak intensity values are positive numbers corresponding to the maximum intensity in each MS1 spectrum
- Scan indices are monotonically increasing and match the row numbers in the original scan index after filtering
- Retention times (if extracted) exhibit linear behavior with expected instrument timescale (e.g., 55 min total run = 3300 seconds for the example dataset)
- Data frame schema matches expected columns (scan_number, base_peak_mz, base_peak_intensity); no missing values or NaN entries

## Limitations

- rawrr requires Windows, Linux, or macOS with .NET runtime and access to the compiled RawFileReader assembly; installation of rawrr::installRawrrExe() is mandatory and may fail on unsupported platforms
- The skill extracts only base-peak (single most intense m/z) per scan; full m/z-intensity vector pairs require additional post-processing of rawrrSpectrum objects
- File I/O overhead: rawrr writes extracted data to temporary disk location and reads it back into R memory, which may be slow for very large raw files (>100k scans)
- Currently aligned with rawrr v1.x API; future versions may introduce breaking changes as the package moves toward full Spectra ecosystem integration (planned but not yet completed)

## Evidence

- [other] rawrr provides accessor functions and subsetting operators ($, [[) to programmatically extract spectral attributes from rawrrSpectrum objects, enabling conversion of scan data into tabular formats.: "rawrr provides accessor functions and subsetting operators ($, [[) to programmatically extract spectral attributes from rawrrSpectrum objects"
- [other] Iterate through filtered scans and call readSpectrum() on each scan number to extract spectral data; for each spectrum, extract the base-peak m/z and its corresponding intensity.: "Iterate through filtered scans and call readSpectrum() on each scan number to extract spectral data. For each spectrum, extract the base-peak m/z (maximum intensity m/z value) and its corresponding"
- [other] Filter the index to retain only MS1-level scans by subsetting on ms_level==1.: "Filter the index to retain only MS1-level scans by subsetting on ms_level==1."
- [intro] rawrr utilizes a vendor-provided API named RawFileReader to access spectral data logged in proprietary Thermo Fisher Scientific raw files: "rawrr utilizes a vendor-provided API named RawFileReader to access spectral data logged in proprietary Thermo Fisher Scientific raw files"
- [intro] We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [discussion] provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats: "provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats"
- [results] Individual scans or scan collections (sets) can be read by the function `readSpectrum()`: "Individual scans or scan collections (sets) can be read by the function `readSpectrum()`"
- [results] By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned: "By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned"
