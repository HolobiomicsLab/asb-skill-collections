---
name: mass-spectrometry-method-cycle-verification
description: Use when when you have a Thermo Fisher Scientific Orbitrap .raw file and need to confirm that a targeted acquisition method (e.g., PRM targeting a specific precursor m/z) is achieving uniform cycle timing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
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

# mass-spectrometry-method-cycle-verification

## Summary

Verify that parallel reaction monitoring (PRM) or targeted MS/MS acquisition maintains consistent scan spacing across all monitoring cycles by extracting scan indices from raw Orbitrap files and validating inter-scan deltas. This skill ensures that the mass spectrometry method is executing as designed without drift or missed cycles.

## When to use

When you have a Thermo Fisher Scientific Orbitrap .raw file and need to confirm that a targeted acquisition method (e.g., PRM targeting a specific precursor m/z) is achieving uniform cycle timing. Use this skill if you suspect incomplete or irregular scan spacing, or when validating a new LC-MS method's consistency across a large number of targeted scans.

## When NOT to use

- Input is already a feature table or peptide-level quantitation result — use this skill only on raw scan-level data.
- The raw file contains only full-scan (MS1) data without targeted MS/MS cycles.
- The LC-MS method does not use fixed-precursor-ion targeting (e.g., untargeted data-dependent acquisition).

## Inputs

- Thermo Fisher Scientific .raw file (e.g., 20181113_010_autoQC01.raw)
- Target precursor m/z and scan type filter pattern
- Expected cycle length (number of scans per complete targeting cycle)

## Outputs

- Filtered scan index data frame (rows matching target scanType)
- Array of inter-scan delta values
- Summary report: count of PRM scans, observed deltas, pass/fail status

## How to apply

Load the raw file using rawrr::readIndex() to retrieve the complete scan index table, which contains metadata for every scan including scanType and precursor m/z. Filter the index to retain only rows matching your target acquisition pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy). Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices. Validate that all inter-scan deltas equal the expected cycle length (e.g., 22 scans for one complete PRM cycle targeting LGGNEQVTR++ at 487.2567 m/z). Document the number of PRM scans detected, observed delta values, and pass/fail status; any deviation from the expected delta indicates method drift, missed scans, or acquisition irregularities.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly; provides readIndex() function to extract scan metadata and scanType information from .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C#) underlying rawrr; implements low-level binary file parsing and data extraction from Thermo Fisher Orbitrap .raw files) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (R package for LC-MS method optimization and quality control; can visualize scan-level metrics and detect acquisition irregularities) — https://github.com/fgcz/rawDiag

## Examples

```
rawrr::readIndex(rawfile = "20181113_010_autoQC01.raw") |> subset(scanType == "FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]") |> {function(df) { deltas <- diff(df$scan); all(deltas == 22) }}
```

## Evaluation signals

- All inter-scan deltas equal the expected cycle length (e.g., 22 scans); any delta ≠ expected value indicates acquisition disruption.
- The count of filtered PRM scans matches the expected number of monitoring cycles across the LC-MS run duration.
- scanType filter matches the intended acquisition method (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]' for PRM).
- No gaps or missing scans in the filtered scan sequence; consecutive scan numbers form a contiguous arithmetic progression with the expected common difference.
- Summary report passes the 22-scan-cycle (or applicable cycle length) criterion, confirming one complete targeting cycle between consecutive monitored precursor ions.

## Limitations

- Requires installation of RawFileReader .NET runtime executable and the rawrr R package; on Windows, the decimal symbol must be configured as '.' for proper data extraction.
- Applicable only to Thermo Fisher Scientific Orbitrap instrument data in .raw format; cannot be used on other vendor formats (e.g., mzML, Bruker .d).
- Does not detect instrument hardware failures or transient acquisition anomalies that do not alter scan spacing; focuses only on temporal regularity of scans, not their spectral quality or intensity.

## Evidence

- [other] The delta between consecutive PRM scans targeting LGGNEQVTR++ (487.2567) is consistently 22 scans, representing one complete PRM cycle.: "The delta between consecutive PRM scans targeting LGGNEQVTR++ (487.2567) is consistently 22 scans, representing one complete PRM cycle."
- [other] Call rawrr::readIndex() on the 20181113_010_autoQC01.raw file to retrieve the complete scan index table.: "Call rawrr::readIndex() on the 20181113_010_autoQC01.raw file to retrieve the complete scan index table."
- [other] Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy).: "Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy)."
- [other] Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices.: "Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices."
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [other] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
