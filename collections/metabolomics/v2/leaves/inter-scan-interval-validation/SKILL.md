---
name: inter-scan-interval-validation
description: Use when after acquiring a PRM experiment on a Thermo Fisher Orbitrap
  instrument when you need to verify that the mass spectrometer's data acquisition
  controller executed the scheduled method with correct temporal spacing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime,
  in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read
  back into memory and parsed into `R` objects using RawFileReader API
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inter-scan-interval-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates that parallel reaction monitoring (PRM) acquisition maintains consistent scan spacing across all targeted cycles by extracting scan indices from a Thermo Fisher Scientific .raw file, filtering for a specific precursor m/z and scan type, and confirming that inter-scan deltas match the expected cycle length. This skill detects acquisition irregularities that would indicate missed or duplicated scans in targeted proteomics workflows.

## When to use

Apply this skill after acquiring a PRM experiment on a Thermo Fisher Orbitrap instrument when you need to verify that the mass spectrometer's data acquisition controller executed the scheduled method with correct temporal spacing. Use it when troubleshooting suspected acquisition glitches, validating instrument configuration before deploying a method to production, or auditing raw data quality in a high-throughput autoQC pipeline.

## When NOT to use

- Input is a non-Thermo format (e.g., mzML, mzXML, Bruker .d): rawrr only reads proprietary Thermo .raw files encoded in the RawFileReader .NET binary format.
- PRM acquisition was not used; the experiment is full MS survey scans or data-dependent MS/MS: inter-scan interval validation assumes a deterministic, regularly-spaced targeting schedule.
- The expected cycle length is unknown or varies dynamically during the run: this skill requires a single fixed inter-scan delta value to serve as the validation criterion.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data file)
- Expected inter-scan delta (integer, representing number of scans in one complete PRM cycle; e.g., 22)
- PRM method signature string (scan type filter, precursor m/z, collision energy; e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00')

## Outputs

- Filtered scan index table (data frame with scan numbers and metadata)
- Vector or list of computed inter-scan deltas (differences between consecutive filtered scan numbers)
- Summary report (count of PRM scans detected, delta value distribution, pass/fail status)

## How to apply

Install the rawrr R package and its runtime executable (RawFileReader .NET assembly), then call rawrr::readIndex() on the .raw file to retrieve the complete scan index table. Filter the returned index data frame to retain only scans matching your PRM acquisition method signature (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z such as 487.2567 and a specific HCD collision energy such as 27.00). Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices. Compare all observed inter-scan deltas against the expected cycle length (e.g., 22 scans for one complete PRM cycle): if all deltas equal the expected value, the acquisition maintained proper spacing; if any delta deviates, flag the scan numbers and report the observed values. Generate a summary report documenting the count of PRM scans detected, the distribution of observed delta values, and a pass/fail verdict based on whether 100% of deltas match the expected interval.

## Related tools

- **rawrr** (R package wrapper around RawFileReader .NET assembly; provides readIndex() function to extract scan metadata and indices from .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly that reads binary Thermo Fisher Scientific .raw files; underlying engine invoked by rawrr via system calls) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend integrating rawrr into the Spectra package ecosystem; alternative interface for accessing raw data if using Spectra workflows) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
rawrr::readIndex(rawfile = "20181113_010_autoQC01.raw") |> subset(scanType == "FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]") |> with(diff(scan)) |> table()
```

## Evaluation signals

- 100% of inter-scan deltas equal the expected cycle length (e.g., all deltas = 22 for one complete PRM cycle).
- The count of filtered PRM scans is consistent with the acquisition duration and the expected frequency (e.g., if the run is 10 minutes and PRM occurs every ~1 second, expect ~600 scans).
- Scan numbers form a strictly increasing sequence with no gaps or decreases within the filtered set.
- No scan numbers match a precursor m/z or collision energy different from the target; re-check the filter string if non-target scans are included.
- The report's pass/fail verdict is reproducible across multiple runs of the same .raw file and independently verifiable by inspecting the raw acquisition log or method file.

## Limitations

- On Windows systems, the decimal symbol must be configured as '.' (not ',') for proper extraction of numeric values from the .raw file metadata.
- The skill detects only regular spacing; it cannot diagnose the ROOT CAUSE of irregular spacing (e.g., C-trap overflow, data loss, instrument error) — further troubleshooting requires access to instrument logs or raw ion chrents.
- The rawrr package invokes RawFileReader via system calls and temporary file I/O, which may be slow for very large .raw files (>10 GB) or on network-mounted storage.
- Filter string construction requires exact knowledge of the PRM method signature; typos in the scan type, precursor m/z, or collision energy will result in zero matches and a false pass.

## Evidence

- [results] Filter scans by type 'FTMS + c NSI Full ms2 487.2567@hcd27.00': "filter = "FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]""
- [results] Call rawrr::readIndex() to retrieve the complete scan index table: "rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)"
- [other] Extract scan numbers and compute differences between consecutive indices: "Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices."
- [other] Expected inter-scan delta of 22 scans for one complete PRM cycle: "The delta between consecutive PRM scans targeting LGGNEQVTR++ (487.2567) is consistently 22 scans, representing one complete PRM cycle."
- [readme] rawrr wraps RawFileReader .NET assembly functionality: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] On Windows, decimal symbol must be configured as '.': "On Windows, the decimal symbol has to be configured as a '.'!"
