---
name: mass-spectrometry-metadata-interpretation
description: Use when you have a Thermo Fisher .raw file and need to verify or document instrument configuration (resolving power, AGC target, injection time, scan filter strings) before downstream analysis, or when troubleshooting spectral quality issues by examining per-scan metadata such as signal-to-noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  - rawDiag
  - Spectra
derived_from:
- doi: 10.1021/acs.jproteome.0c00866
  title: rawrr
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1021/acs.jproteome.0c00866
    title: rawrr
  dedup_kept_from: coll_rawrr
schema_version: 0.2.0
---

# mass-spectrometry-metadata-interpretation

## Summary

Extract and validate instrument metadata and quality indicators from Thermo Fisher Scientific Orbitrap raw mass spectrometry files to confirm spectral acquisition parameters and assess data integrity. This skill enables direct programmatic access to proprietary binary raw file metadata without GUI-based software, supporting reproducible method optimization and quality control in bottom-up proteomics workflows.

## When to use

Apply this skill when you have a Thermo Fisher .raw file and need to verify or document instrument configuration (resolving power, AGC target, injection time, scan filter strings) before downstream analysis, or when troubleshooting spectral quality issues by examining per-scan metadata such as signal-to-noise ratios, baseline noise floors, or acquisition time budgets. Particularly useful when integrating raw data into modular R-based pipelines where GUI tools like MaxQuant or Skyline would constrain analytical flexibility.

## When NOT to use

- Input is not a Thermo Fisher .raw file (e.g., mzML, mzXML, or other vendor formats) — use vendor-neutral tools like ProteoWizard or pyteomics instead.
- Analysis goal is high-level statistical aggregation of preprocessed peptide-level data — use MSstats, MSqRob, or other downstream R packages that operate on feature tables, not raw spectra.
- Windows system without decimal symbol configured as '.' — rawrr requires this locale setting for proper parsing of numeric fields in the binary file.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap FTMS format)
- scan number (integer identifier, e.g., 9594)
- precursor peptide sequence (for theoretical y-fragment m/z calculation, optional but recommended for quality checks)
- scan filter string or scan type descriptor (optional, for pre-filtering scans, e.g., 'FTMS + c NSI Full ms2 [mass_range]')

## Outputs

- rawrrSpectrum object containing 119+ metadata fields per scan
- instrument parameters: resolving power, AGC target, injection time (ms), scan type
- m/z and intensity arrays (centroided)
- signal-to-noise ratios for identified y-ions
- per-scan quality metrics (baseline noise floor, peak intensity distribution)

## How to apply

Load the .raw file using rawrr::readFileHeader() to retrieve run-level metadata (scan count, time range, instrument model). Then invoke rawrr::readSpectrum() with the target scan number to extract a rawrrSpectrum object containing 119+ data items. Parse the returned object to retrieve instrument-specific parameters: resolving power (e.g., 30,000 at 200 m/z for Orbitrap FTMS), AGC target (e.g., 100,000 charges), and injection time in milliseconds. For quality assessment, extract m/z and intensity arrays from the centroided spectrum; identify y-ion signals by matching observed m/z to theoretical fragment m/z of the known precursor peptide; calculate signal-to-noise ratio per y-ion by comparing peak intensity to local baseline noise. Confirm all y-ions exceed tens to hundreds of counts above noise floor to validate high spectral quality. The workflow relies on compiled C# wrapper methods (RawFileReader API) invoked via system calls, with temporary file I/O for data marshalling back to R.

## Related tools

- **rawrr** (Bioconductor R package providing direct programmatic access to Thermo Fisher .raw file spectra and metadata via RawFileReader API wrapper; primary tool for this skill) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C#) that implements low-level binary parsing of Orbitrap .raw files; wrapped by rawrr and invoked via system call) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend serving rawrr as a modular Spectra accessor for on-disk raw file access; optional integration for Bioconductor ecosystem) — https://github.com/cpanse/MsBackendRawFileReader
- **rawDiag** (Companion R package for visualization and rational LC-MS method optimization using rawrr data; useful for interactive exploration of metadata and QC metrics) — https://github.com/fgcz/rawDiag
- **Spectra** (Bioconductor package providing unified accessor interface for mass spectrometry data; MsBackendRawFileReader allows Spectra to read .raw files via rawrr)

## Examples

```
S <- rawrr::readSpectrum(rawfile = "20181113_010_autoQC01.raw", scan = 9594); H <- rawrr::readFileHeader(rawfile = "20181113_010_autoQC01.raw"); cat('Resolving Power:', S[[1]]$`Resolving Power`, 'AGC Time (ms):', S[[1]]$`Injection Time (ms)`)
```

## Evaluation signals

- Extracted resolving power matches instrument specification sheet (e.g., exactly 30,000 at 200 m/z for Q Exactive HF Orbitrap).
- AGC injection time is within plausible bounds relative to maximum allowed (e.g., 2.8 ms out of 55 ms max ≈ 5%).
- All identified y-ions for known peptide have signal-to-noise ratios ≥ 10:1 (several tens to hundreds of counts above noise floor).
- Centroided spectrum contains expected number of peaks for the peptide (e.g., 9 y-ions for a 10-residue peptide); absence of key ions signals acquisition or calibration problems.
- No parsing errors or null values in mandatory metadata fields (scan type, filter string, m/z range, centroiding flag); file I/O round-trip consistency verified.

## Limitations

- Windows systems require decimal symbol configured as '.' for proper numeric parsing; locale misconfiguration causes data extraction failure.
- MsBackendRawFileReader backend is still under development (WIP status) and not yet stable for production use; rawrr stand-alone package is recommended.
- Metadata interpretation depends on correct centroiding and lock mass correction applied during acquisition; if either is disabled, baseline noise estimates and S/N calculations become unreliable.
- rawrr provides access only to Thermo Fisher Scientific Orbitrap instruments; other vendors (Waters, Bruker, Sciex, etc.) require alternative tools (e.g., ProteoWizard, ThermoRawFileParser for non-native formats).
- On-disk backend performance for very large .raw files (>6.6 million scans as in the example) may be constrained by file I/O overhead; temporary file staging required for each spectrum read.

## Evidence

- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package"
- [other] Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms (~5% of maximum 55 ms); all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality.: "Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms (~5% of maximum 55 ms); all y-ion signals for"
- [methods] In order to return extracted data back to the R layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
- [methods] Specifically, R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [results] In total, the API provides 119 data items for this particular scan: "In total, the API provides 119 data items for this particular scan"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [intro] We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
