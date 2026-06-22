---
name: retention-time-scan-mapping
description: Use when when you have loaded an LC-MS spectrum file (mzML, mzXML, or equivalent) into the GNPS LCMS Visualization Dashboard and need to annotate extracted ion chromatograms with the precise retention time or scan ID positions where MS2 events occurred.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GNPS LCMS Visualization Dashboard
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-scan-mapping

## Summary

Map MS2 precursor scan positions to their corresponding retention times or scan identifiers on extracted ion chromatograms (XIC). This skill enables overlay of tandem mass spectrometry data points onto LC-MS chromatographic displays when the show_ms2_markers parameter is enabled.

## When to use

When you have loaded an LC-MS spectrum file (mzML, mzXML, or equivalent) into the GNPS LCMS Visualization Dashboard and need to annotate extracted ion chromatograms with the precise retention time or scan ID positions where MS2 events occurred. Use this when show_ms2_markers is set to True and you want to validate that precursor ions were successfully fragmented at expected chromatographic positions.

## When NOT to use

- The spectrum file contains only MS1 (full-scan) data with no MS/MS events — there will be no precursor positions to map.
- The show_ms2_markers parameter is set to False or absent — the dashboard will not display marker annotations regardless of mapping output.
- The spectrum file format is not compatible with standard parsers (mzML, mzXML, or supported equivalents) — precursor metadata cannot be reliably extracted.

## Inputs

- LC-MS spectrum file (mzML, mzXML, or equivalent format)
- MS/MS scan metadata (precursor scan indices, retention times, scan identifiers)
- show_ms2_markers parameter (boolean: True/False)
- ms2_identifier parameter (marker identifier or set of identifiers)

## Outputs

- Structured marker position file (JSON, CSV, or TSV) with retention time + scan ID pairs
- XIC display with overlaid MS2 precursor markers at chromatographic retention times
- Annotated extracted ion chromatogram showing MS2 event locations

## How to apply

Parse the MS/MS scan metadata from the loaded spectrum file to extract precursor scan indices and their associated retention times or scan identifiers. Filter and validate each precursor position to confirm it corresponds to an actual MS2 event in the spectrum data. Compile the set of validated marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output format (JSON, CSV, or TSV) suitable for XIC annotation. Pass this compiled set to the dashboard's XIC display layer via the ms2_identifier parameter, which will overlay the markers at their corresponding chromatographic coordinates.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Accepts resolved spectrum files and displays XIC with overlaid MS2 markers when show_ms2_markers is enabled and ms2_identifier is provided) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AGNPS%3ATASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87%2Fdata%2FYao_Streptomyces%2Froseosporus%2F0518_s_BuOH.mzXML%3Ascan%3A171&show_ms2_markers=1&ms2_identifier=MS2%3A1176
```

## Evaluation signals

- MS2 marker positions appear at correct retention times on the XIC display (visual alignment with expected chromatographic peak positions).
- Each marker corresponds to exactly one validated MS2 event in the parsed spectrum metadata (no spurious or duplicate markers).
- Marker output file (JSON/CSV/TSV) contains non-empty, well-formed retention time + scan ID pairs.
- When the same spectrum is queried multiple times, marker positions remain consistent (deterministic mapping).
- Markers respect the xic_tolerance parameter and appear only within the specified m/z window on the extracted ion chromatogram.

## Limitations

- Marker accuracy depends on correct parsing of precursor scan metadata; malformed or corrupt spectrum headers may produce incomplete or misaligned markers.
- The mapping assumes a one-to-one correspondence between scan indices and retention times; non-linear or ambiguous scan-RT relationships may cause misalignment.
- Large spectrum files with thousands of MS2 events may incur performance overhead when compiling and rendering all markers simultaneously.
- The ms2_identifier parameter accepts only a single identifier or set of identifiers; filtering to a subset of MS2 events requires pre-filtering before submission to the dashboard.

## Evidence

- [other] When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display, enabling users to overlay tandem mass spectrometry data points at their corresponding retention times or scan IDs on extracted ion chromatograms.: "When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display"
- [other] Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers.: "Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers"
- [other] Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum.: "Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum"
- [other] Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV) suitable for XIC annotation.: "Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV)"
- [other] Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory.: "Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory"
