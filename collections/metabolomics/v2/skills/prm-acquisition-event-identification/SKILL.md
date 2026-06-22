---
name: prm-acquisition-event-identification
description: Use when you have a Thermo Fisher Scientific .raw file containing PRM data and need to verify that acquisition of a specific precursor ion (e.g., LGGNEQVTR++ at m/z 487.2567) is happening at regular intervals consistent with your instrument method design.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - rawDiag
  - Spectra
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# PRM Acquisition Event Identification

## Summary

Identify and validate parallel reaction monitoring (PRM) acquisition cycles in Thermo Orbitrap raw files by extracting the scan index, filtering for targeted precursor ion acquisitions, and confirming consistent inter-scan spacing. This skill enables quality control of PRM method consistency and detection of complete acquisition cycles targeting specific peptide precursors.

## When to use

Apply this skill when you have a Thermo Fisher Scientific .raw file containing PRM data and need to verify that acquisition of a specific precursor ion (e.g., LGGNEQVTR++ at m/z 487.2567) is happening at regular intervals consistent with your instrument method design. Use it to detect deviations from expected cycle times (e.g., when the delta between consecutive PRM scans should equal 22 scans but does not), or to extract the actual PRM cycle length from a raw file.

## When NOT to use

- Input file is not a Thermo Orbitrap .raw file (e.g., mzML, mzXML, or data from non-Thermo instruments); use format-specific readers instead.
- Your acquisition method is not PRM but rather DIA (data-independent acquisition) or untargeted MS/MS; the scanType filter will not match DIA patterns.
- You are analyzing a preprocessed feature table or consensus spectrum library rather than raw instrument data; cycle identification requires access to the raw scan index.

## Inputs

- Thermo Fisher Scientific .raw file (binary mass spectrometry data file from Q Exactive HF or similar Orbitrap instrument)
- Expected precursor m/z value (e.g., 487.2567 for LGGNEQVTR++)
- Expected collision energy or scan type filter pattern (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00')
- Expected PRM cycle delta in scans (e.g., 22 scans per complete cycle)

## Outputs

- Filtered scan index data frame containing only PRM acquisition events
- Vector of inter-scan delta values (differences between consecutive PRM scan numbers)
- Pass/fail validation result confirming whether all deltas match expected cycle length
- Summary report with count of PRM scans detected, delta statistics, and cycle consistency status

## How to apply

Install the rawrr R package and its runtime executable (RawFileReader .NET assembly), then call rawrr::readIndex() on the raw file to retrieve the complete scan index table. Filter the resulting data frame to retain only rows where scanType matches your PRM acquisition pattern—typically 'FTMS + c NSI Full ms2' with a fixed precursor m/z and collision energy (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]'). Extract the scan numbers from filtered rows and compute differences between consecutive scan indices. Validate that all inter-scan deltas equal the expected cycle length (e.g., 22 scans); if deltas vary or are inconsistent with your method design, the PRM acquisition is not cycling as intended. Generate a summary report documenting the number of PRM scans detected, the distribution of delta values, and pass/fail status against your cycle criterion.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly to read scan index and metadata from .raw files; primary tool for extracting PRM scan events) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C# compiled code) providing low-level binary access to Thermo .raw file structure; invoked by rawrr via system calls) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (Companion R package for LC-MS diagnostic visualization and method optimization; can visualize PRM cycle structure and scan timing) — https://github.com/fgcz/rawDiag
- **Spectra** (Bioconductor package; rawrr and MsBackendRawFileReader serve as backends for accessing raw spectral data via Spectra API) — https://bioconductor.org/packages/Spectra/

## Examples

```
rawrr::readIndex(rawfile = '20181113_010_autoQC01.raw') |> subset(scanType == 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]') |> {diff(.$scan)} |> table()
```

## Evaluation signals

- All inter-scan delta values for filtered PRM scans are identical to the expected cycle length (e.g., all equal 22); any variance indicates a problem with method execution or instrument timing.
- The count of detected PRM scans matches expectations (e.g., if the run is 60 min and the PRM cycle is 22 scans with a known scan rate, the total PRM count should fall within a plausible range).
- The scanType filter returns rows only for the target precursor m/z and collision energy; rows with different precursor ions or energies are excluded.
- The earliest and latest PRM scan numbers correspond to the expected retention time window for the target peptide.
- Summary report shows 100% pass rate for the 22-scan-cycle criterion; any failure rate indicates missed or extra scans in one or more cycles.

## Limitations

- Requires Windows, Linux, or macOS with .NET runtime installed; RawFileReader .NET assembly access is platform-dependent and requires ThermoFisher.CommonCore DLLs.
- On Windows systems, the decimal symbol must be configured as '.' (period) for proper numeric data extraction; misconfiguration causes parsing errors.
- The rawrr package version and RawFileReader assembly version must be compatible; mismatches may cause unexpected behavior or missing data fields.
- Scan type pattern matching is case-sensitive and exact; minor variations in filter strings (e.g., extra spaces, different ion mobility settings) will not match and will be excluded from analysis.
- Does not detect acquisition quality issues such as low precursor intensity, poor fragmentation, or spectrum artifacts; it only validates cycle timing geometry.

## Evidence

- [other] task_004 description: "Does the parallel reaction monitoring (PRM) acquisition in the example raw file maintain consistent scan spacing across all cycles targeting the LGGNEQVTR++ precursor ion?"
- [other] cycle delta finding: "The delta between consecutive PRM scans targeting LGGNEQVTR++ (487.2567) is consistently 22 scans, representing one complete PRM cycle."
- [other] workflow step 2: "Call rawrr::readIndex() on the 20181113_010_autoQC01.raw file to retrieve the complete scan index table."
- [other] workflow step 3: "Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy)."
- [other] workflow step 4: "Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices."
- [results] readIndex method: "rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)"
- [intro] rawrr package definition: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package."
- [intro] RawFileReader wrapping: "rawrr wraps the functionality of the RawFileReader .NET assembly."
- [discussion] Windows decimal symbol limitation: "On Windows, the decimal symbol has to be configured as a '.'!"
- [methods] example data: "The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
