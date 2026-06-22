---
name: basepeak-intensity-identification
description: Use when when you have Thermo Fisher Scientific .raw files from an Orbitrap instrument and need to identify the m/z value and corresponding intensity of the most abundant ion in each MS1 scan for quality control, method optimization, or feature extraction in a modular R-based proteomics pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - R
  - RawFileReader
  - MsBackendRawFileReader
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
---

# Base-Peak Intensity Identification

## Summary

Extract the base-peak m/z and intensity values (maximum intensity peak) from individual MS1 scans in Thermo Fisher raw files and organize them into a tabular data frame. This skill enables direct access to fundamental spectral descriptors without conversion to exchange formats.

## When to use

When you have Thermo Fisher Scientific .raw files from an Orbitrap instrument and need to identify the m/z value and corresponding intensity of the most abundant ion in each MS1 scan for quality control, method optimization, or feature extraction in a modular R-based proteomics pipeline.

## When NOT to use

- Input is already in mzML, mzXML, or other exchange format—use format-agnostic parsers (e.g., MSnbase) instead of rawrr, which is specific to Thermo .raw files.
- You need to extract all peaks or construct full MS1 feature tables—base-peak extraction is a single-value summary per scan; use readSpectrum() with full spectral processing for comprehensive feature matrices.
- Working with non-Thermo instruments (e.g., Bruker, Waters, ABSciex)—rawrr wraps the Thermo RawFileReader API and cannot read other vendor formats.

## Inputs

- Thermo Fisher Scientific .raw file (proprietary binary format)
- MS scan index (data.frame with scan metadata including ms_level)
- MS1 scan identifiers (positive integers)

## Outputs

- data.frame with columns: scan index, base-peak m/z, base-peak intensity
- rawrrSpectrum objects (intermediate)
- numeric vectors of m/z and intensity pairs

## How to apply

Install the rawrr R package and its compiled executable via rawrr::installRawrrExe(). Load the .raw file and generate a scan index using readIndex() to retrieve all scans. Filter the index to retain only MS1-level scans by subsetting on ms_level==1. Iterate through each filtered scan number and call readSpectrum() to extract spectral data as a rawrrSpectrum object. For each spectrum, use accessor functions ($ or [[) to retrieve the m/z and intensity arrays, identify the m/z position corresponding to the maximum intensity value, and extract both the base-peak m/z and its intensity. Aggregate the scan index, base-peak m/z, and base-peak intensity into a data frame for downstream analysis or visualization.

## Related tools

- **rawrr** (Primary R package providing accessor functions and subsetting operators to extract spectral attributes from rawrrSpectrum objects and convert scan data into tabular formats) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly wrapped by rawrr; provides low-level API to read binary Thermo .raw file data via system calls) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional: serves as an MsBackend for the Bioconductor Spectra package, enabling integration of rawrr-based spectral extraction into modular analysis workflows) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
library(rawrr); rawrr::installRawrrExe(); idx <- readIndex('20181113_010_autoQC01.raw'); ms1_idx <- subset(idx, ms_level == 1); basepeak_df <- data.frame(scan = ms1_idx$scan, bp_mz = NA_real_, bp_intensity = NA_real_); for(i in seq_along(ms1_idx$scan)) { spec <- readSpectrum('20181113_010_autoQC01.raw', scans = ms1_idx$scan[i]); max_idx <- which.max(spec$intensity[[1]]); basepeak_df$bp_mz[i] <- spec$mz[[1]][max_idx]; basepeak_df$bp_intensity[i] <- spec$intensity[[1]][max_idx]; }
```

## Evaluation signals

- Extracted data frame has no missing values in base-peak m/z or intensity columns for any MS1 scan.
- Base-peak intensity value for each scan matches the maximum value in the corresponding spectrum's intensity array.
- Base-peak m/z value is the m/z coordinate at the position of maximum intensity in the spectrum.
- Number of rows in output data frame equals the number of MS1 scans in the input .raw file (validate via length of filtered readIndex() result).
- Retention time or scan-level metadata from the index aligns with the extracted base-peak rows (1:1 correspondence by scan number).

## Limitations

- rawrr is specific to Thermo Fisher Scientific Orbitrap instruments and cannot read .raw files from other vendors (Bruker, Waters, ABSciex).
- Requires installation of the rawrr compiled executable; platform-specific compilation may be needed on non-standard systems.
- Base-peak extraction is a summary statistic and loses information about the full peak distribution; not suitable for isotope pattern analysis or charge-state deconvolution.
- Performance scales linearly with the number of scans; very large .raw files (>100,000 scans) may require iterative processing or memory management.
- Accessor functions ($, [[]]) assume rawrrSpectrum object structure; malformed or corrupt scans may raise parsing errors or return NA values.

## Evidence

- [other] Filter MS scans using ms filter: "Filter the index to retain only MS1-level scans by subsetting on ms_level==1"
- [other] Iterate and extract base-peak values: "Iterate through filtered scans and call readSpectrum() on each scan number to extract spectral data. For each spectrum, extract the base-peak m/z (maximum intensity m/z value) and its corresponding"
- [other] Accessor functions enable tabular extraction: "rawrr provides accessor functions and subsetting operators ($, [[) to programmatically extract spectral attributes from rawrrSpectrum objects, enabling conversion of scan data into tabular formats."
- [other] Installation procedure: "Install the rawrr executable using rawrr::installRawrrExe()"
- [readme] Direct binary file access rationale: "provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats"
- [readme] Spectral data representation: "spectral data is presented by using only two non-standard objects representing data items well known to analytical scientists (mass spectrum and mass chromatogram)"
