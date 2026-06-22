---
name: mass-spectrometry-data-loader-integration
description: Use when you have mass spectrometry data available in multiple identifier formats (GNPS Task ID, Universal Spectrum Identifier, or Feature-Based Molecular Networking task reference) and need to route each format to its specific loader without manual preprocessing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - usi.py
  - alignment.py
  - dash_get_sets.py
  - requests (Python library)
  - pandas
  - networkx
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.5c00237
  title: MMSA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmsa_cq
    doi: 10.1021/jasms.5c00237
    title: MMSA
  dedup_kept_from: coll_mmsa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00237
  all_source_dois:
  - 10.1021/jasms.5c00237
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mass Spectrometry Data Loader Integration

## Summary

This skill routes mass spectrometry data inputs from heterogeneous identifier formats (Task ID, USI, or FBMN) to their respective data loaders, enabling standardized ingestion and deserialization of spectral datasets. It is essential for web-based platforms that must accept multiple input pathways while maintaining a unified downstream analysis interface.

## When to use

Apply this skill when you have mass spectrometry data available in multiple identifier formats (GNPS Task ID, Universal Spectrum Identifier, or Feature-Based Molecular Networking task reference) and need to route each format to its specific loader without manual preprocessing. Use it when building a multi-input web application where users must flexibly choose their input method while the backend expects a standardized dataset object.

## When NOT to use

- Input is already a validated, deserialized spectrum or feature table in memory — use this skill only at the ingestion boundary, not on intermediate processed data.
- Mass spectrometry data is supplied in raw proprietary vendor formats (e.g., .raw, .d) without GNPS Task ID, USI, or FBMN reference — this skill presupposes access to GNPS infrastructure.
- The application does not require multi-format support or already enforces a single input pathway — this skill adds complexity only when heterogeneous input methods must coexist.

## Inputs

- GNPS Task ID (string)
- Universal Spectrum Identifier (USI) list (one per line)
- Feature-Based Molecular Networking (FBMN) Task ID and component numbers
- Identifier format (categorical: 'Task ID', 'USI', or 'FBMN')

## Outputs

- Standardized dataset object (pandas DataFrame or Dash table)
- Deserialized mass spectrometry peak data (m/z, intensity, scan metadata)
- Molecular network graph (networkx object, for FBMN input)
- Validation status report (boolean + error log)

## How to apply

First, receive the user-supplied mass spectrometry data identifier and parse it to determine its format category (Task ID, USI, or FBMN). Validate the identifier against format-specific patterns (e.g., USI follows mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number> syntax). Route the identifier to the appropriate loader function based on classification. Execute the selected loader to retrieve and deserialize the spectral data into a standardized dataset object (e.g., Dash/Plotly-compatible table or networkx graph for molecular networking results). Finally, validate the loaded dataset for completeness (e.g., presence of required columns: m/z, intensity, scan metadata) before returning it to downstream visualization or filtering modules.

## Related tools

- **usi.py** (Parses, validates, and processes Universal Spectrum Identifier strings; handles USI-to-spectrum retrieval and deserialization) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **alignment.py** (Core module that receives standardized dataset objects from loaders and performs peak alignment and set analysis across multiple spectra) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **dash_get_sets.py** (Data input interface that exposes the routing logic to users; handles form submission and dispatches identifiers to the appropriate loader) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **requests (Python library)** (HTTP client used by loaders to fetch spectral data and task metadata from GNPS servers)
- **pandas** (Data manipulation and schema validation; converts heterogeneous input formats into standardized DataFrame representation)
- **networkx** (Network analysis library used to construct and validate molecular network graphs returned by FBMN loaders)

## Evaluation signals

- Identifier format is correctly classified: Task ID, USI, and FBMN inputs are routed to their respective loaders without cross-format errors.
- Loaded dataset schema is complete and consistent: required columns (m/z, intensity, scan metadata, precursor m/z) are present and populated; no null or NaN in critical fields.
- Deserialized spectral data matches the source: spot-check peak m/z and intensity values against the original GNPS task or USI source to confirm no corruption during round-trip.
- Downstream modules (alignment.py, visualization) execute without schema or type errors on the returned dataset object; data flows seamlessly from loader to analyzer.
- Validation report explicitly confirms dataset completeness (boolean True) before returning; error log remains empty for successful ingestion or contains actionable error messages (e.g., 'USI not found', 'Task ID invalid') on failure.

## Limitations

- No changelog or versioning information is available in the repository, making it unclear whether breaking changes to identifier formats or loader signatures have been introduced.
- The skill depends entirely on GNPS infrastructure availability and API stability; network outages or GNPS server changes will cause loader failures without local fallback.
- USI format validation is string-pattern-based; the skill may not detect semantically invalid USIs that pass the regex but reference non-existent spectra until the loader attempts remote fetch.
- The skill does not handle partial or corrupted data from GNPS sources; loaders will fail on malformed responses rather than gracefully downsampling or imputing missing peaks.

## Evidence

- [intro] The application accepts mass spectrometry data through various formats including Task ID, USI, or FBMN, enabling multiple input pathways for data ingestion.: "users to input mass spectrometry data through various formats (Task ID, USI, or FBMN)"
- [other] The routing workflow validates the input identifier, classifies it, and dispatches it to the appropriate loader function.: "Parse and validate the identifier format to determine input type. 3. Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification."
- [other] The loader executes and returns a standardized dataset object after deserialization and completeness validation.: "Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object. 5. Validate the loaded dataset object for completeness and return the routed"
- [readme] USI format specification includes mzspec protocol and GNPS task reference structure.: "Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`"
- [readme] The usi.py module is explicitly responsible for USI processing utilities within the application architecture.: "usi.py                          # USI processing utilities"
