---
name: total-ion-current-calculation
description: Use when after loading all MS1 scans from a raw or intermediate mass spectrum file (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Aerith
  - R
  - mzR
  - Raxport
  - ThermoRawFileParser
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# total-ion-current-calculation

## Summary

Compute a retention-time-indexed table of summed ion intensities (TIC) from MS1 scan data by aggregating intensities across all m/z values for each scan. This provides a quality-control and visualization-ready representation of chromatographic signal intensity across the full mass-to-charge range.

## When to use

Apply this skill after loading all MS1 scans from a raw or intermediate mass spectrum file (e.g., FT1, mzML, MGF) and you need to (1) verify data quality via scan-level signal intensity trends, (2) identify retention-time windows of strong signal for downstream analysis, or (3) prepare input for chromatographic visualization plots covering a specific retention-time range (e.g., 9–10 min).

## When NOT to use

- Input is already a pre-computed TIC table or chromatogram file — skip directly to filtering and visualization.
- You need MS/MS (MS2) or higher-order MS data — getTIC operates only on MS1 scans; use alternative functions for product-ion spectra.
- Raw file is in a proprietary binary format not supported by readAllScanMS1 (e.g., native Thermo .raw without prior conversion to mzML or FT1) — convert using ThermoRawFileParser or Raxport first.

## Inputs

- MS1 scan list from readAllScanMS1 (mzML, MGF, FT1, or mzR-compatible format)
- Retention-time window parameters (start_time, end_time, interval_width in minutes)

## Outputs

- TIC table: data frame with columns (retention_time, summed_intensity)
- Filtered TIC table restricted to specified retention-time window
- plotTIC visualization (chromatogram plot of intensity vs. retention time)

## How to apply

Use the readAllScanMS1 function in Aerith to load all MS1 scans from the input file. Apply the getTIC function to each scan, which sums all ion intensities across the m/z dimension for that scan and indexes the result by retention time. The output is a table with two columns: retention time and total ion current (summed intensity). Filter this table to the desired retention-time window (specify both start time, end time, and interval width, e.g., 9–10 min with 0.2 min bins) and pass the filtered table to plotTIC for visualization. The workflow validates data quality by revealing gaps, baseline drift, or instrumental artifacts in the TIC trace.

## Related tools

- **Aerith** (Provides readAllScanMS1 and getTIC functions for loading MS1 scans and computing TIC; executes TIC calculation and visualization via plotTIC) — https://github.com/xyz1396/Aerith
- **mzR** (Enables parsing of mzML and MGF files for input to readAllScanMS1)
- **Raxport** (Converts Thermo RAW files to FT1/FT2 format compatible with Aerith readAllScanMS1) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Alternative converter for Thermo RAW files to mzML or MGF for input to readAllScanMS1) — https://github.com/CompOmics/ThermoRawFileParser

## Examples

```
library(Aerith); scans_ms1 <- readAllScanMS1('demo.FT1'); tic_table <- getTIC(scans_ms1); tic_filtered <- tic_table[tic_table$retention_time >= 9.0 & tic_table$retention_time <= 10.0, ]; plotTIC(tic_filtered)
```

## Evaluation signals

- TIC table contains exactly two columns (retention_time, summed_intensity) with no null or NA values in the filtered window.
- All retention-time values are monotonically increasing and fall within the specified window (e.g., 9.0–10.0 min).
- Summed-intensity values are non-negative and consistent with raw scan-level m/z intensity distributions (no negative or implausible values).
- plotTIC produces a smooth or multi-modal chromatogram trace with recognizable peaks, not a flat line or noise; absence of expected peaks may indicate data quality issues.
- Interval width divides the retention-time window evenly; row count ≈ (end_time − start_time) / interval_width.

## Limitations

- getTIC assumes all MS1 scans contain valid m/z and intensity pairs; scans with missing or corrupted data will produce incorrect summed intensities or NAs.
- Retention-time indexing depends on accurate metadata in the input file; clock skew or missing scan timing will produce misaligned TIC traces.
- Very large raw files (>1 GB) may require subset extraction or chunked processing to avoid memory exhaustion; the article recommends leveraging subset files for method development.
- TIC does not distinguish between analyte signal and instrument noise; high baseline noise will inflate the apparent total ion current and obscure weak signals.

## Evidence

- [other] The getTIC function accepts a list of MS1 scans from readAllScanMS1 and produces a TIC table aggregating summed intensities by retention time, which plotTIC then visualizes across a specified retention-time window (e.g., 9–10 min with 0.2 min intervals).: "The getTIC function accepts a list of MS1 scans from readAllScanMS1 and produces a TIC table aggregating summed intensities by retention time, which plotTIC then visualizes across a specified"
- [readme] Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions, score and visualize the PSM (peptide and spectra match), and visualize the TIC (total ion current) using Rcpp.: "Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions, score and visualize"
- [other] Verify data quality using TIC and scan frequency analysis: "Verify data quality using TIC and scan frequency analysis"
- [intro] Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
- [other] Leverage subset files for method development and testing: "Leverage subset files for method development and testing"
