---
name: retention-time-windowing
description: Use when you have a complete TIC (total ion current) table indexed by
  retention time and need to visualize or analyze only a specific time interval—for
  example, when isolating a chromatographic peak region (9–10 min) before plotting
  or when a mass spectrometry run spans a time range wider than the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  techniques:
  - mass-spectrometry
  license_tier: open
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

# retention-time-windowing

## Summary

Filter a retention-time-indexed table of summed ion intensities to retain only scans within a specified retention-time window, preparing chromatographic data for visualization. This skill extracts a contiguous time interval from a TIC table to focus analysis on a region of interest.

## When to use

Apply this skill when you have a complete TIC (total ion current) table indexed by retention time and need to visualize or analyze only a specific time interval—for example, when isolating a chromatographic peak region (9–10 min) before plotting or when a mass spectrometry run spans a time range wider than the region of biological interest.

## When NOT to use

- Input is raw MS1 scan data (not yet aggregated into a TIC table); use getTIC first.
- Retention-time boundaries are unknown or unspecified; clarify the analysis goal and chromatographic region of interest before windowing.
- The entire TIC range is already of analytical interest; windowing would discard potentially relevant signal.

## Inputs

- TIC table (retention time indexed, with summed ion intensities per scan)
- retention time start boundary (numeric, in minutes)
- retention time end boundary (numeric, in minutes)

## Outputs

- filtered TIC table (subset of rows within the specified retention-time window, retention time vs. summed intensity format)
- retention-time-windowed intensity matrix (ready for plotTIC visualization)

## How to apply

After computing a TIC table using getTIC (which aggregates summed intensities by retention time across all m/z values for each MS1 scan), filter the table to retain only rows where retention time falls within your target window (e.g., 9–10 min). The filtering is typically performed by selecting rows where retention_time >= start_time AND retention_time <= end_time, using the same time unit (minutes) and precision (e.g., 0.2 min intervals) as the input TIC table. The filtered output—a retention time vs. summed intensity table—is then formatted as input-ready for downstream visualization (plotTIC) or further analysis. The choice of window boundaries depends on the chromatographic region of interest and should align with the scan frequency and time resolution of the mass spectrometry data.

## Related tools

- **Aerith** (R package that computes TIC tables via getTIC and visualizes windowed TIC data via plotTIC) — https://github.com/xyz1396/Aerith
- **R** (Scripting environment for performing retention-time filtering operations on TIC tables)

## Evaluation signals

- Verify that all rows in the filtered output have retention_time >= start_boundary and retention_time <= end_boundary.
- Confirm that the filtered table preserves the original retention-time index and intensity values (no data corruption or unit conversion errors).
- Check that the row count of the filtered table is less than or equal to the original TIC table (expected to be strictly less if windowing is restrictive).
- Validate that plotTIC successfully accepts the filtered table as input and renders a chromatogram spanning only the specified retention-time interval.
- Ensure that no scans within the window boundaries are dropped and no scans outside the boundaries are retained.

## Limitations

- Retention-time window boundaries must be specified by the user and must lie within the range of the input TIC table; misaligned boundaries will return empty or unexpected subsets.
- The filtering preserves only the time intervals present in the input TIC table; if the table was computed with coarse time resolution (e.g., 1 min intervals), sub-minute precision windowing is not possible.
- Windowing operates on aggregated intensity (summed across m/z); m/z-specific or mass-resolved filtering requires earlier intervention in the getTIC or readAllScanMS1 pipeline.

## Evidence

- [other] Filter the resulting TIC table to retain only scans within the 9–10 min retention-time window.: "Filter the resulting TIC table to retain only scans within the 9–10 min retention-time window."
- [other] The getTIC function accepts a list of MS1 scans from readAllScanMS1 and produces a TIC table aggregating summed intensities by retention time, which plotTIC then visualizes across a specified retention-time window (e.g., 9–10 min with 0.2 min intervals).: "The getTIC function accepts a list of MS1 scans from readAllScanMS1 and produces a TIC table aggregating summed intensities by retention time, which plotTIC then visualizes across a specified"
- [other] Format the filtered table (retention time vs summed intensity) as input-ready for plotTIC visualization.: "Format the filtered table (retention time vs summed intensity) as input-ready for plotTIC visualization."
