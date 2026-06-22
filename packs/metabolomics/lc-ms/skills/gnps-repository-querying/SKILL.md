---
name: gnps-repository-querying
description: Use when when you have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-...
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3200
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - GNPS LCMS Visualization Dashboard
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans:
- GNPS LCMS Visualization Dashboard
- GNPS Analysis Tasks - [mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce
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

# GNPS Repository Querying

## Summary

Resolve Universal Spectrum Identifiers (USI) to retrieve mass spectrometry data from GNPS analysis tasks, MassIVE datasets, MetaboLights, and other public repositories via the GNPS LCMS Visualization Dashboard. This skill enables programmatic and interactive access to spectrum peak lists and metadata across multiple mass spectrometry data sources.

## When to use

When you have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-...:scan:171 or mzspec:MSV000084951:AH22) and need to retrieve the corresponding mass spectrum peak list (m/z and intensity pairs), scan metadata, or extracted ion chromatograms for comparative analysis, QC evaluation, or metabolite identification.

## When NOT to use

- The USI references a data source not supported by GNPS (e.g., a local file system path not ingested into GNPS or MassIVE)
- You need real-time processing of streaming MS data or closed-access proprietary repositories not mirrored in GNPS/MassIVE
- The scan number or file path in the USI is incorrect or has been deleted from the repository

## Inputs

- Universal Spectrum Identifier (USI) string in mzspec format (e.g., mzspec:GNPS:TASK-<id>-<filepath>:scan:<number>)
- Optional: extracted ion chromatogram (XIC) m/z targets (semicolon-delimited list)
- Optional: XIC tolerance in Da
- Optional: MS2 scan identifiers for marker annotation

## Outputs

- Mass spectrum peak list (m/z and intensity pairs)
- Scan metadata (scan number, retention time, precursor m/z, collision energy)
- Extracted ion chromatogram (XIC) traces with optional MS2 markers
- Structured output (JSON or CSV) suitable for comparative analysis or database queries

## How to apply

Parse the USI string to extract the repository identifier (GNPS task ID, MassIVE accession, MetaboLights ID, or file name), scan number, and file path components according to the mzspec USI format specification. Query the GNPS LCMS Visualization Dashboard API or web interface by submitting the USI; the dashboard resolves the resource location and fetches the spectrum data from the underlying repository backend. Optionally specify extracted ion chromatogram (XIC) mass-to-charge (m/z) values (e.g., 841.3170166;842.3170166), XIC tolerance (typically 0.5 Da), and normalization preferences. The dashboard returns the peak list as structured visualization or via API; export as CSV or JSON for downstream processing. Verify retrieval by confirming spectrum metadata (scan number, RT, precursor m/z) match expectations and that peak intensity values are present and non-zero.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Query interface and data retrieval engine for USI resolution; supports mzspec format parsing, XIC extraction, and multi-file comparison) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AGNPS%3ATASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87%2Fdata%2FYao_Streptomyces%2Froseosporus%2F0518_s_BuOH.mzXML%3Ascan%3A171&xicmz=841.3170166%3B842.3170166&xic_tolerance=0.5&xic_norm=No&show_ms2_markers=1
```

## Evaluation signals

- USI resolves without error and returns a valid spectrum record with non-empty peak list
- Returned peak list contains m/z values within expected instrument range (e.g., 50–2000 m/z for metabolomics) and intensity values > 0
- Scan metadata (retention time, precursor m/z, scan number) are consistent with the input USI and instrument type (Thermo, Sciex, Bruker, Waters, Agilent)
- If XIC targets were specified, extracted chromatogram traces are computed and plotted without NaN or missing values
- Cross-validation: peak list retrieved via USI matches peaks in the original raw data file when accessed through alternative means (e.g., mzML parser)

## Limitations

- USI resolution requires the GNPS LCMS Visualization Dashboard to be running and network-accessible; not suitable for offline-only workflows
- Only repositories with mzspec USI support (GNPS, MassIVE, MetaboLights) are queryable; custom or institutional repositories require implementation of USI specification and code updates to download.py
- Large datasets or many simultaneous USI queries may be rate-limited or cause dashboard performance degradation; batch processing requires care
- Scan numbers and file paths must be exact; typos in USI will result in 404 or resolution failure without detailed diagnostic information

## Evidence

- [other] GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number, which the GNPS LCMS Visualization Dashboard uses as a data source to retrieve and display mass spectrometry data.: "GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number, which the GNPS LCMS Visualization Dashboard uses as a data source to retrieve"
- [other] Parse the USI string to extract the GNPS task ID and scan number using the USI format specification. Query the GNPS data repository API or access the GNPS LCMS Visualization Dashboard to retrieve the spectrum metadata and scan data associated with the task ID. Fetch the peak list (m/z and intensity pairs) from the resolved scan. Format and export the peak list as a structured output file (CSV or JSON).: "Parse the USI string to extract the GNPS task ID and scan number using the USI format specification. Query the GNPS data repository API or access the GNPS LCMS Visualization Dashboard to retrieve the"
- [readme] Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from. If you want to provide a new data source, you'll have to implement the following: 1. USI Specification that denotes what the resource is and how to get data 2. Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI.: "Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from. If you want to provide a new data source, you'll have to implement the following 1. USI"
- [readme] What we can easily do is paste in the QC molecules and pull them out in one fell swoop: 271.0315;278.1902;279.0909;285.0205;311.0805;314.1381: "paste in the QC molecules and pull them out in one fell swoop: 271.0315;278.1902;279.0909;285.0205;311.0805;314.1381"
