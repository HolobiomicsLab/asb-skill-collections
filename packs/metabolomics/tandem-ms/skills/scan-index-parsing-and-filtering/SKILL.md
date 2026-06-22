---
name: scan-index-parsing-and-filtering
description: Use when you have a Thermo Orbitrap .raw file and need to (1) verify that a targeted acquisition method (e.g., PRM) maintains consistent scan spacing across all cycles; (2) extract only scans matching a specific precursor ion and fragmentation method;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
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

# scan-index-parsing-and-filtering

## Summary

Parse the complete scan index table from a Thermo Fisher Scientific Orbitrap .raw file and filter scans by acquisition method, precursor m/z, and collision energy to isolate targeted MS/MS cycles. This skill enables validation of acquisition consistency metrics such as inter-scan deltas and cycle structure in parallel reaction monitoring (PRM) workflows.

## When to use

You have a Thermo Orbitrap .raw file and need to (1) verify that a targeted acquisition method (e.g., PRM) maintains consistent scan spacing across all cycles; (2) extract only scans matching a specific precursor ion and fragmentation method; or (3) audit the structure and regularity of a multi-cycle MS/MS acquisition without loading full spectral data.

## When NOT to use

- You need full spectral peak lists or intensity data — use rawrr::readSpectrum() instead of readIndex().
- You are analyzing non-Thermo instruments (e.g., Bruker, Waters, Sciex) — rawrr wraps RawFileReader which is Thermo-specific.
- The scan index has already been extracted and cached — re-reading via readIndex() adds I/O overhead.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data)
- target precursor m/z (e.g., 487.2567 for LGGNEQVTR++)
- target scanType pattern (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00')
- expected inter-scan delta or cycle length (e.g., 22 scans)

## Outputs

- filtered scan index data frame (subset of full index matching scanType criteria)
- vector of inter-scan delta values (differences between consecutive filtered scan numbers)
- summary report including: total number of filtered PRM scans, observed delta distribution, pass/fail status for cycle consistency

## How to apply

Call rawrr::readIndex() on the .raw file to retrieve the complete scan index table as a data frame. Filter the index by scanType using string matching (e.g., 'FTMS + c NSI Full ms2' with fixed precursor m/z and HCD collision energy value) to retain only rows corresponding to your targeted method. Extract scan numbers from the filtered rows, compute differences between consecutive scan indices, and validate that all inter-scan deltas match the expected cycle length (e.g., 22 scans for one complete PRM cycle). Document the number of scans detected, observed delta values, and pass/fail status against the criterion. This approach avoids loading full spectra and is ideal for rapid method auditing.

## Related tools

- **rawrr** (R package providing readIndex() function to parse and return scan index table from Thermo .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly (wrapped by rawrr) that performs low-level binary file parsing and index extraction) — https://github.com/thermofisherlsms/RawFileReader
- **Spectra** (Optional Bioconductor backend that can use rawrr for on-disk access to Orbitrap scan metadata) — https://bioconductor.org/packages/Spectra/

## Examples

```
rawrr::readIndex(rawfile = '20181113_010_autoQC01.raw') |> subset(scanType == 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]') |> \(x) {scans <- x$scan; deltas <- diff(scans); cat('PRM scans:', length(scans), 'Deltas:', unique(deltas), '\n')}
```

## Evaluation signals

- All inter-scan deltas in the filtered index equal the expected cycle length (e.g., all deltas == 22 for a single-cycle PRM method).
- The number of filtered scans is consistent with the expected number of PRM cycles in the run (e.g., 6,600,000 total scans ÷ 22-scan cycle = ~300,000 PRM acquisitions).
- The scanType string extracted from each filtered row matches the input filter pattern exactly (no partial matches or spurious variants).
- Scan numbers are in strict ascending order within the filtered subset, confirming no reordering or duplication artifacts.
- The first and last filtered scan numbers align with the expected retention-time range and method start/end markers in the file header.

## Limitations

- On Windows, the decimal symbol must be configured as '.' for proper data extraction — system locale misconfigurations may cause silent errors or corrupt numeric fields.
- readIndex() returns only metadata (scan number, scan type, retention time, precursor m/z); it does not provide peak intensity or mass accuracy — full spectral validation requires readSpectrum().
- Filter syntax is case-sensitive and must match the exact scanType string in the raw file; abbreviated or fuzzy filters may miss scans or return empty results.
- The approach assumes single-method acquisition; complex multi-method files may require iterative filtering over multiple scanType patterns to isolate all targeted cycles.

## Evidence

- [methods] Call rawrr::readIndex() on the file to retrieve the complete scan index table: "Call rawrr::readIndex() on the 20181113_010_autoQC01.raw file to retrieve the complete scan index table."
- [methods] Filter the index data frame by scanType matching the PRM acquisition method pattern: "Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy)."
- [methods] Extract scan numbers and compute differences between consecutive indices: "Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices."
- [methods] Validate that all inter-scan deltas equal the expected cycle length: "Validate that all inter-scan deltas equal 22 scans, confirming one complete MS/MS cycle between consecutive targeted acquisitions."
- [readme] rawrr wraps the RawFileReader .NET assembly for Thermo data access: "rawrr wraps the functionality of the RawFileReader .NET assembly. Test files are provided by the tartare ExperimentData package."
- [results] readIndex() usage example from results section: "rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)"
- [discussion] Windows decimal symbol configuration requirement: "On Windows, the decimal symbol has to be configured as a '.'!"
