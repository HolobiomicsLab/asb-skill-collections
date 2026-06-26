---
name: spectral-data-filtering
description: Use when you have loaded a full set of MS scans (e.g., all MS1 scans
  from readAllScanMS1 in Aerith) and need to restrict analysis to a specific retention-time
  window (e.g., 9–10 min with 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - mzR
  - Raxport
  - ThermoRawFileParser
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-filtering

## Summary

Filter mass spectrometry spectral data by retention time, MS level, or scan properties to isolate a subset of scans relevant to a specific analysis window or quality control objective. This skill is essential for reducing computational burden, focusing visualization on regions of interest, and verifying data quality before downstream analysis.

## When to use

Apply this skill when you have loaded a full set of MS scans (e.g., all MS1 scans from readAllScanMS1 in Aerith) and need to restrict analysis to a specific retention-time window (e.g., 9–10 min with 0.2 min intervals), exclude noisy or low-quality scans, or prepare a subset of scans for method development and testing before running a full workflow.

## When NOT to use

- Input is already a pre-filtered or subset file optimized for a specific analysis — re-filtering risks data loss or inconsistent binning.
- Retention-time window is undefined or broader than the entire acquisition range — filtering would have no effect; use the full scan list instead.
- Raw file contains only MS2 scans or has already been processed into a feature or consensus table — filtering at scan level is no longer applicable.

## Inputs

- List of MS1 scans with retention-time indices (e.g., output of readAllScanMS1 in Aerith)
- Retention-time window boundaries (e.g., 9–10 min)
- Optional: scan metadata including MS level, frequency, or intensity statistics

## Outputs

- Filtered scan list or retention-time-indexed table (subset of input scans)
- TIC table aggregating summed intensities by retention time within the window
- Quality control summary (scan frequency, intensity distribution)

## How to apply

After reading all scans from a raw file using readAllScanMS1 or equivalent MS1 extraction function, identify the retention-time boundaries of interest (e.g., 9–10 min). Filter the scan list to retain only records whose retention time falls within that window, using the scan's indexed retention time as the selection criterion. If performing quality control, apply scan-frequency analysis and TIC (total ion current) visualization across the filtered subset to verify that scans are evenly distributed and intensities are reasonable. The filtered table (retention time vs. aggregated ion intensity) then becomes input-ready for downstream visualization (e.g., plotTIC) or scoring workflows. Parameter selection (e.g., retention-time interval width of 0.2 min) should be applied consistently across related samples to ensure reproducibility.

## Related tools

- **Aerith** (Provides readAllScanMS1 function to load MS1 scans and plotTIC to visualize the filtered TIC table; integrates retention-time indexing and filtering workflows) — https://github.com/xyz1396/Aerith
- **mzR** (Bioconductor integration for direct parsing of mzML and MGF files; enables retrieval of scan metadata including retention time)
- **Raxport** (Extracts scans from Thermo RAW files and generates .FT1 or .FT2 files with MS1/MS2 scans and retention-time information for downstream filtering) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Converts Thermo RAW files to open formats (MGF, mzML, Parquet); supports selection by MS level and retention-time range via command-line filtering options) — https://github.com/CompOmics/ThermoRawFileParser

## Examples

```
# Load demo.FT1 and extract all MS1 scans; filter to 9–10 min window
scans <- readAllScanMS1('demo.FT1')
filtered_scans <- scans[scans$retentionTime >= 9.0 & scans$retentionTime <= 10.0, ]
tic_table <- getTIC(filtered_scans)
plotTIC(tic_table, rtWindow = c(9, 10), rtInterval = 0.2)
```

## Evaluation signals

- Filtered scan count is less than or equal to the total number of input scans; no scans are added or duplicated.
- All retention times in the output table fall within the specified window (e.g., 9.0–10.0 min); scans outside the boundary are absent.
- TIC values are aggregated correctly: summed intensity at each retention-time bin matches the sum of m/z intensities from all scans in that bin.
- Scan frequency is uniform or near-uniform across the retention-time window, indicating no gaps or data dropout in the filtered region.
- Visualization (plotTIC) shows a continuous chromatographic profile within the window with no artifactual spikes or discontinuities at boundary transitions.

## Limitations

- Retention-time filtering assumes that retention time is reliably recorded in the raw file and is monotonically increasing; errors in retention-time metadata will propagate to the filtered output.
- Filtering by retention time alone does not address low signal-to-noise scans, chemical noise, or contamination; additional quality filters (e.g., intensity thresholds, scan-frequency analysis) should be applied in parallel if data quality verification is needed.
- Interval width (e.g., 0.2 min bins) is a user-specified parameter; suboptimal choice can lead to over-binning (loss of temporal resolution) or under-binning (sparse or noisy bins); consistency across samples is critical for comparative analysis.

## Evidence

- [other] Filter the resulting TIC table to retain only scans within the 9–10 min retention-time window.: "Filter the resulting TIC table to retain only scans within the 9–10 min retention-time window."
- [other] Apply getTIC to compute total ion current by summing intensities across all m/z values for each scan, indexed by retention time.: "Apply getTIC to compute total ion current by summing intensities across all m/z values for each scan, indexed by retention time."
- [other] Always verify data quality using TIC and scan frequency analysis.: "Always verify data quality using TIC and scan frequency analysis"
- [other] Leverage subset files for method development and testing.: "Leverage subset files for method development and testing"
- [other] Apply consistent parameter selection across related samples.: "Apply consistent parameter selection across related samples"
- [readme] Aerith is an R package that provides interfaces to read and write mass spectrum scans: "Aerith is an R package that provides interfaces to read and write mass spectrum scans"
