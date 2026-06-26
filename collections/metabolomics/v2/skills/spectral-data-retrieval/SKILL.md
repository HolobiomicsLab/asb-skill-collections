---
name: spectral-data-retrieval
description: Use when you have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/...
  or mzspec:MSV000084951:AH22) and need to extract the corresponding mass spectrum
  peak list (m/z and intensity pairs) for downstream analysis, visualization, or cross-repository
  comparison.
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

# spectral-data-retrieval

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Resolve a Universal Spectrum Identifier (USI) string to retrieve mass spectrometry peak lists from distributed repositories (GNPS, MassIVE, MetaboLights). This skill enables programmatic access to raw and processed MS data across multiple data sources using a standardized identifier format.

## When to use

You have a USI string (e.g., mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/... or mzspec:MSV000084951:AH22) and need to extract the corresponding mass spectrum peak list (m/z and intensity pairs) for downstream analysis, visualization, or cross-repository comparison. This is essential when working with publicly archived metabolomics or proteomics data and need to avoid manual file downloads.

## When NOT to use

- The USI format is invalid or does not conform to mzspec specification for the target repository.
- The spectrum or file referenced by the USI has been removed or is not publicly accessible in the target repository.
- You require processed or annotated spectral libraries rather than raw scan data; use spectral matching tools instead.

## Inputs

- USI string (mzspec:REPOSITORY:IDENTIFIER[:optional_scan_number])
- GNPS task identifier and file path (for GNPS analysis tasks)
- MassIVE dataset identifier (MSV) and file name
- MetaboLights study identifier (MTBLS) and file name
- Optional: scan number or MS level filter

## Outputs

- Peak list (m/z and intensity pairs) as structured data (CSV, JSON)
- Spectrum metadata (scan number, retention time, precursor m/z if MS/MS)
- Spectrum visualization (XIC, TIC) via GNPS LCMS Dashboard
- Remote data source URL resolved from USI

## How to apply

Parse the USI string according to the USI format specification to extract the repository identifier (GNPS, MSV, MTBLS), the file or task path, and optionally the scan number. Query the GNPS LCMS Visualization Dashboard API or the underlying data repository to resolve the USI to a remote data source URL. Fetch the spectrum metadata and scan data from the resolved source—for GNPS analysis tasks, this includes querying by task ID and file path; for MassIVE datasets, by dataset ID (MSV) and file name; for MetaboLights, by study ID (MTBLS) and file name. Extract the peak list (m/z and intensity pairs) from the retrieved spectrum scan. Format and export the peak list as a structured file (CSV or JSON) for downstream use. Validate that the resolved spectrum contains valid m/z and intensity values within expected ranges for the instrument vendor and data type (e.g., Thermo, Sciex, Bruker, Waters, Agilent).

## Related tools

- **GNPS LCMS Visualization Dashboard** (Primary interface for resolving USI strings and retrieving spectrum data; provides API endpoint /mspreview?usi=<usi> for programmatic access and browser-based XIC/TIC visualization.) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard

## Evaluation signals

- Resolved URL is valid and accessible; HTTP 200 response from remote data source.
- Extracted peak list contains valid m/z values (typically 50–2000 m/z) and non-negative intensity values.
- Scan metadata (retention time, scan number, precursor m/z) is present and consistent with instrument and data type.
- Peak list can be visualized in the GNPS LCMS Dashboard without errors or data loss.
- Exported CSV/JSON file parses without schema violations and round-trips to original peak data.

## Limitations

- USI resolution depends on network availability and remote repository uptime; transient failures may require retry logic.
- Some data sources (e.g., private MassIVE datasets, embargoed MetaboLights studies) may not be accessible via public USI endpoints.
- Large datasets or high-resolution proteomics files (e.g., Sciex SWATH) may require significant bandwidth and local storage for peak list export.
- USI format currently supports only a limited set of repositories; new data sources require implementation of resolver logic in download.py.

## Evidence

- [other] How can a USI string referencing a GNPS analysis task be resolved to extract the corresponding mass spectrum peak list?: "How can a USI string referencing a GNPS analysis task be resolved to extract the corresponding mass spectrum peak list?"
- [other] GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number, which the GNPS LCMS Visualization Dashboard uses as a data source to retrieve and display mass spectrometry data.: "GNPS analysis tasks are accessible via mzspec USI format containing the GNPS task identifier, file path, and scan number, which the GNPS LCMS Visualization Dashboard uses as a data source to retrieve"
- [other] Parse the USI string to extract the GNPS task ID and scan number using the USI format specification. Query the GNPS data repository API or access the GNPS LCMS Visualization Dashboard to retrieve the spectrum metadata and scan data associated with the task ID. Fetch the peak list (m/z and intensity pairs) from the resolved scan. Format and export the peak list as a structured output file (CSV or JSON).: "Parse the USI string to extract the GNPS task ID and scan number using the USI format specification. Query the GNPS data repository API or access the GNPS LCMS Visualization Dashboard to retrieve the"
- [readme] Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from. If you want to provide a new data source, you'll have to implement the following: 1. USI Specification that denotes what the resource is and how to get data. 2. Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI.: "Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI."
- [readme] Example Sources of Data: 1. GNPS Analysis Tasks - [mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171]: "GNPS Analysis Tasks - [mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171]"
- [readme] GNPS/MassIVE public datasets and Metabolights public datasets: "GNPS/MassIVE public datasets - mzspec:MSV000084951:AH22 and Metabolights public datasets - mzspec:MTBLS1124:QC07.mzML"
