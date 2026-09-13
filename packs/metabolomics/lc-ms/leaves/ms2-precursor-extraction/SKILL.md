---
name: ms2-precursor-extraction
description: Use when when you have a resolved spectrum file in mzML or mzXML format
  and need to identify where MS2 (tandem mass spectrometry) scans occur within an
  LC-MS run, particularly to annotate XIC displays with MS2 precursor positions or
  validate that MS2 events align with expected chromatographic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GNPS LCMS Visualization Dashboard
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Precursor Extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and locate MS2 precursor scan positions from resolved spectrum files (mzML, mzXML) to enable overlay of tandem mass spectrometry data points on extracted ion chromatograms (XICs). This skill reconstructs the mapping between MS2 events and their retention times or scan identifiers for visualization and annotation.

## When to use

When you have a resolved spectrum file in mzML or mzXML format and need to identify where MS2 (tandem mass spectrometry) scans occur within an LC-MS run, particularly to annotate XIC displays with MS2 precursor positions or validate that MS2 events align with expected chromatographic features.

## When NOT to use

- Input spectrum file is in an unresolved or vendor-proprietary binary format that cannot be parsed for MS2 metadata extraction.
- Analysis goal is MS1-only chromatographic feature detection; MS2 precursor positions are not needed for the workflow.
- Spectrum file contains only MS1 (survey) scans with no MS2 events, making precursor extraction inapplicable.

## Inputs

- Resolved spectrum file (mzML or mzXML format)
- MS2 identifier parameter (scan ID or retention time reference)
- XIC tolerance value (e.g., 0.5 m/z)

## Outputs

- Structured marker position file (JSON, CSV, or TSV)
- Annotated XIC display with MS2 precursor overlays
- Set of retention time + scan ID pairs or single precursor identifiers

## How to apply

Load the spectrum file into memory and parse its MS/MS scan metadata to extract precursor scan indices and their associated retention times or scan identifiers. Filter and validate these precursor positions to ensure they correspond to actual MS2 events in the spectrum data. Compile the validated marker positions (retention time + scan ID pairs or single identifiers) into a structured output format (JSON, CSV, or TSV) suitable for XIC annotation. When using the GNPS LCMS Visualization Dashboard, set the show_ms2_markers parameter to True and specify an ms2_identifier parameter to mark these positions on the XIC display.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Accepts show_ms2_markers parameter to overlay extracted precursor positions on XIC displays; visualizes and validates marker reconstruction) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AGNPS%3ATASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87%2Fdata%2FYao_Streptomyces%2Froseosporus%2F0518_s_BuOH.mzXML%3Ascan%3A171&xicmz=841.3170166%3B842.3170166&xic_tolerance=0.5&xic_norm=No&show_ms2_markers=1&ms2_identifier=MS2%3A1176
```

## Evaluation signals

- Precursor markers appear at correct retention times or scan positions on the XIC overlay, visually aligning with observed chromatographic peaks.
- All extracted precursor scan indices correspond to valid MS2 events in the raw spectrum file metadata (no orphaned or invalid IDs).
- Output file format (JSON, CSV, or TSV) is well-formed and contains expected fields: scan ID, retention time, and optional precursor m/z value.
- When loaded into the GNPS Dashboard with show_ms2_markers=True, markers render without errors and map to the correct USI spectrum.
- Precursor count and distribution match expectations from the original spectrum file's scan header entries.

## Limitations

- Extraction accuracy depends on the completeness and correctness of MS/MS metadata embedded in the spectrum file; corrupted or incomplete headers may yield missing or spurious markers.
- Retention time precision and scan ID resolution vary by instrument vendor and file format version; some formats may encode only approximate retention times.
- Large spectrum files (e.g., long LC-MS runs with thousands of MS2 scans) may require substantial memory and parsing time; streaming approaches may be necessary for production workflows.
- Some vendor formats may not encode retention times explicitly; fallback to scan index mapping may be less intuitive for interpretation.

## Evidence

- [other] When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display, enabling users to overlay tandem mass spectrometry data points at their corresponding retention times or scan IDs on extracted ion chromatograms.: "When show_ms2_markers is set to True, the dashboard accepts an ms2_identifier parameter to mark MS2 precursor positions on the XIC display"
- [other] Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory. 2. Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers. 3. Filter and validate precursor positions to ensure they correspond to actual MS2 events in the spectrum.: "Load the resolved spectrum file (mzML, mzXML, or equivalent format) into memory. 2. Parse MS/MS (MS2) scan metadata to extract precursor scan indices and associated retention times or scan identifiers"
- [other] Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV) suitable for XIC annotation.: "Compile the set of marker positions (retention time + scan ID pairs or single identifier per precursor) into a structured output file (JSON, CSV, or TSV)"
- [readme] show_ms2_markers=1&ms2_identifier=MS2%3A1176: "show_ms2_markers=1&ms2_identifier=MS2%3A1176"
