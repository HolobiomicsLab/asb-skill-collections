---
name: r-data-frame-aggregation
description: Use when when you have extracted multiple spectral attributes (e.g., base-peak m/z, intensity, retention time, scan index) from individual MS scans via accessor functions and need to organize them into a single rectangular data frame for batch analysis, filtering, or export to external tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - R
  - RawFileReader
  - Spectra
  techniques:
  - tandem-MS
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

# R Data Frame Aggregation

## Summary

Consolidate programmatically extracted spectral attributes from individual scans into a single tabular data frame using R subsetting operators and iteration. This is essential for transforming per-scan raw instrument data into analysis-ready tabular formats suitable for downstream statistical and visualization workflows.

## When to use

When you have extracted multiple spectral attributes (e.g., base-peak m/z, intensity, retention time, scan index) from individual MS scans via accessor functions and need to organize them into a single rectangular data frame for batch analysis, filtering, or export to external tools.

## When NOT to use

- Input data is already a feature matrix or aggregated table—skip to statistical analysis or visualization.
- You need to preserve all m/z–intensity pairs for each spectrum, not just base-peak values; use alternative export formats (mzML) or in-memory list structures instead.
- Raw file is in an exchange format (mzML, mzXML) already—use format-specific parsers (mzR, proteowizardR) rather than rawrr.

## Inputs

- rawrrSpectrum objects (extracted via readSpectrum)
- scan index data frame (from readIndex)
- filtered scan numbers (integer vector)

## Outputs

- data frame with columns for scan index and spectral attributes (e.g., base_peak_mz, base_peak_intensity)

## How to apply

Iterate through a filtered scan index (e.g., MS1-level scans obtained via readIndex() and subset on ms_level==1), calling readSpectrum() on each scan number to extract the spectrum object. Use R's subsetting operators ($, [[) to programmatically extract target attributes (base-peak m/z, intensity, scan number) from each rawrrSpectrum object. Aggregate these pairs into vectors or lists, then bind them into a data frame using data.frame() or cbind(). Verify correctness by checking row count matches scan count, column names are meaningful, and data types are appropriate (numeric for m/z/intensity, integer for scan indices).

## Related tools

- **rawrr** (Provides readSpectrum(), readIndex(), and accessor functions to extract spectral data from Thermo .raw files and return rawrrSpectrum objects amenable to subsetting) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly wrapped by rawrr; implements the binary file I/O and spectral data extraction) — https://github.com/thermofisherlsms/RawFileReader
- **Spectra** (Alternative downstream consumer of aggregated MS data; MsBackendRawFileReader integrates rawrr data into Spectra package workflows) — https://bioconductor.org/packages/Spectra

## Examples

```
# Install rawrr and load raw file
rawrr::installRawrrExe()
H <- rawrr::readFileHeader('20181113_010_autoQC01.raw')
idx <- rawrr::readIndex('20181113_010_autoQC01.raw')
idx_ms1 <- subset(idx, idx$ms_level == 1)
df <- data.frame(scan = idx_ms1$scan, base_peak_mz = NA, base_peak_intensity = NA)
for (i in seq_along(idx_ms1$scan)) {
  spec <- rawrr::readSpectrum('20181113_010_autoQC01.raw', idx_ms1$scan[i])
  df$base_peak_mz[i] <- spec$mz[which.max(spec$intensity)]
  df$base_peak_intensity[i] <- max(spec$intensity)
}
```

## Evaluation signals

- Row count in output data frame equals the number of filtered scans (e.g., if 10,000 MS1 scans were selected, result should have 10,000 rows).
- All expected columns are present and named correctly (e.g., 'scan_index', 'base_peak_mz', 'base_peak_intensity').
- No NA or NaN values in key columns unless explicitly expected (e.g., scans with no peaks).
- m/z values are numeric, within instrument's expected mass range (e.g., 50–2000 m/z for typical Orbitrap), and base-peak m/z is the position of maximum intensity within each spectrum.
- Data frame can be successfully written to CSV or loaded into downstream analysis tools (ggplot2, statistical functions) without type conversion errors.

## Limitations

- rawrr requires installation of the compiled RawFileReader executable via rawrr::installRawrrExe(); not all platforms may have stable releases.
- Accessor operators ($, [[]]) on rawrrSpectrum objects are not well-documented; users must rely on package vignettes and examples.
- Iterative extraction via readSpectrum() called per scan is slower than bulk operations; for large datasets (>100,000 scans), performance may be limiting.
- Aggregation into a single data frame assumes all scans contain the same attributes; heterogeneous scan types (MS1 vs MS2 with different metadata) may require pre-filtering or list-of-data-frames structures.
- The article focuses on base-peak extraction; full spectral profiles (all m/z–intensity pairs) require alternative strategies beyond simple data-frame aggregation.

## Evidence

- [other] Iterate through filtered scans and call readSpectrum() on each scan number to extract spectral data: "Iterate through filtered scans and call readSpectrum() on each scan number to extract spectral data. For each spectrum, extract the base-peak m/z and its corresponding intensity."
- [other] rawrr provides accessor functions and subsetting operators to programmatically extract spectral attributes: "rawrr provides accessor functions and subsetting operators ($, [[) to programmatically extract spectral attributes from rawrrSpectrum objects"
- [other] Aggregate extracted m/z and intensity pairs into a data frame: "Aggregate extracted m/z and intensity pairs into a data frame with scan index and base-peak columns."
- [methods] R functions request access to data via C# wrapper methods; extracted information is written to temporary location, read back into memory and parsed into R objects: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call. In order to return extracted data back to the R layer we use file I/O. More"
- [other] Generate scan index using readIndex() to retrieve all scans; filter to retain only MS1-level scans: "Generate a scan index using readIndex() to retrieve all scans. Filter the index to retain only MS1-level scans by subsetting on ms_level==1."
