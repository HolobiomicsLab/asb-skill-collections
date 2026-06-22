---
name: orbitrap-spectrum-acquisition-interpretation
description: Use when when you have a Thermo Scientific .raw file from an Orbitrap instrument (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - .NET 8.0
  - rawDiag
  - .NET 8.0 runtime
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
- In case you prefer to compile `rawrr.exe` from C# source code, please install the .NET 8.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
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

# orbitrap-spectrum-acquisition-interpretation

## Summary

Extract and interpret spectral metadata and ion trap instrumentation parameters from Thermo Orbitrap raw files to characterize acquisition conditions, charge collection, and scan-level performance metrics. This skill bridges raw binary data access with quantitative understanding of mass spectrometry instrument behavior during data acquisition.

## When to use

When you have a Thermo Scientific .raw file from an Orbitrap instrument (e.g., Q Exactive HF) and need to understand or verify acquisition-time instrument behavior: charge collection in the C-trap, injection time utilization, scan type classification, mass range configuration, or isolation parameters for specific scans. Use this skill to validate whether instrument settings matched experimental intent or to diagnose unexpected spectral characteristics.

## When NOT to use

- Input is not a Thermo .raw file (e.g., mzML, mzXML, Bruker, or Waters formats) — rawrr is instrument-vendor specific.
- You only need to perform statistical analysis or peptide identification on preprocessed peak intensity tables — this skill operates at raw binary data layer, not downstream analysis.
- The .raw file was acquired on a non-Orbitrap Thermo instrument (e.g., TSQ triple quadrupole) — metadata item availability and scan type strings differ.

## Inputs

- Thermo Fisher Scientific .raw file (binary format from Orbitrap instrument)
- Scan identifier(s) or scan filter string (e.g., 'ms' for MS1, 'FTMS + c NSI Full ms2')
- Instrument specification reference (e.g., Q Exactive HF max injection time, C-trap capacity)

## Outputs

- Spectrum object with 119 data items per scan (charge, injection time, m/z, intensity, scan type, activation method, isolation parameters)
- Scan index table with scanType, filterString, retentionTime columns
- Duty-cycle metrics (C-trap charge / max injection time ratio, percentage utilization)
- Run-level header metadata (instrument model, scan count, time range, centroiding/lock mass flags)

## How to apply

Load the raw file using rawrr::readFileHeader() to obtain run-level metadata (scan count, time range, instrument model). Extract the scan index via rawrr::readIndex() and filter by scan type string (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00') to identify scans matching your criteria. Call rawrr::readSpectrum() on selected scans to retrieve the full spectrum object, which contains 119+ data items including C-trap charge collected, injection time, activation method, isolation m/z, and fragmentation energy. Cross-reference collected charge against maximum injection time (e.g., 55 ms for Q Exactive HF) to compute duty-cycle utilization percentage. Verify centroiding and lock mass correction flags in the scan metadata. Compare measured scan-level parameters against instrument's hardware limits and method template settings to assess fidelity.

## Related tools

- **rawrr** (R package wrapping RawFileReader .NET assembly; provides readFileHeader(), readSpectrum(), readIndex(), readChromatogram() functions for direct access to Orbitrap binary data) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (ThermoFisher.CommonCore.RawFileReader) invoked via C# wrapper methods by rawrr; reads binary Orbitrap data on Windows, Linux, macOS) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (R package for LC-MS method optimization and raw file diagnostics; complements rawrr for visualization and interpretation of instrument performance) — https://github.com/fgcz/rawDiag
- **.NET 8.0 runtime** (Execution environment required for RawFileReader .NET assemblies; must be installed and verified before rawrr operation)

## Examples

```
rawfile <- '20181113_010_autoQC01.raw'; H <- rawrr::readFileHeader(rawfile); idx <- rawrr::readIndex(rawfile); filtered_idx <- subset(idx, scanType == 'FTMS + c NSI Full ms2'); S <- rawrr::readSpectrum(rawfile, scan = filtered_idx$scan[1]); cat('C-trap charge:', S[[1]]$charge, 'ions; injection time:', S[[1]]$injectionTime, 'ms\n')
```

## Evaluation signals

- Successful readFileHeader() call returns non-null run metadata including 'Number of scans', 'Time range', and instrument model string.
- readSpectrum() output for a specific scan contains all expected data items (charge, injection time, m/z array, intensity array); length ≥ 119 items verified.
- Scan filter string matches expected instrumentation (e.g., 'FTMS' for Fourier-transform, 'hcd27.00' for 27% normalized collision energy, isolation m/z within instrument range).
- Duty-cycle calculation (C-trap charge / max injection time) yields 0–100% range; values >100% indicate data inconsistency or instrument saturation.
- Centroiding and lock mass correction flags consistently reflect acquisition method template (should match instrument logfile if available).

## Limitations

- rawrr is specific to Thermo Fisher Scientific Orbitrap instruments; cannot read other vendor formats (Bruker, Waters, AB Sciex, etc.).
- On Windows systems, the decimal symbol must be configured as '.' for proper data extraction — locale settings can silently cause parsing failures.
- MsBackendRawFileReader integration with Bioconductor Spectra package is still in development (WIP status) and not yet feature-complete for production pipelines.
- Extracted metadata is read-only from the binary file; instrument configuration changes (e.g., method template updates) cannot be written back.
- Performance benchmarking shows ~0.5 seconds total runtime for typical scan queries, but throughput scales with number of scans and system I/O bandwidth.

## Evidence

- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [results] the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~`r format((2.8/55)*100, digits = 1)`% of the maximum injection time of 55 ms: "the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms"
- [results] In total, the API provides `r length(S[[1]])` data items for this particular scan: "In total, the API provides 119 data items for this particular scan"
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly.: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'"
