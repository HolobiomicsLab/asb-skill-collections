---
name: conditional-dispatch-routing-logic
description: Use when a mass spectrometry analysis pipeline must accept data from
  multiple sources with different identifier schemes (GNPS Task ID, Universal Spectrum
  Identifiers, or Feature-Based Molecular Networking task IDs), and you need to transparently
  route each to the correct loader without requiring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Flask
  - usi.py module
  - dash_get_sets.py module
  - requests library
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conditional-dispatch-routing-logic

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Routes mass spectrometry data inputs from heterogeneous identifier formats (Task ID, USI, FBMN) to their respective specialized data loaders. This skill enables a web application to accept multiple input pathways and deserialize them into a standardized dataset object for downstream analysis.

## When to use

Use this skill when a mass spectrometry analysis pipeline must accept data from multiple sources with different identifier schemes (GNPS Task ID, Universal Spectrum Identifiers, or Feature-Based Molecular Networking task IDs), and you need to transparently route each to the correct loader without requiring the user to specify the input type explicitly.

## When NOT to use

- Input is already a deserialized standardized dataset object (e.g., pre-loaded peak table or feature matrix) — skip routing and proceed directly to analysis.
- Mass spectrometry data format is not Task ID, USI, or FBMN (e.g., raw mzML or mgf files) — use direct file ingestion instead of format-based dispatch.
- Multiple input formats are present in a single batch and format detection is ambiguous — clarify user intent before routing.

## Inputs

- Mass spectrometry data identifier string (Task ID, USI, or FBMN format)
- User-provided input from web form or API endpoint

## Outputs

- Standardized dataset object containing deserialized mass spectrometry data
- Validated peak alignment or spectral data ready for visualization or analysis

## How to apply

Receive the mass spectrometry data input identifier from the user. Parse and validate the identifier format to determine which of three types it represents: Task ID (GNPS task number), USI (formatted as 'mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>'), or FBMN task ID. Route the classified identifier to the corresponding loader module (Task ID loader, USI loader, or FBMN loader). Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object. Validate the loaded dataset for completeness (presence of required fields such as m/z values, intensities, and scan metadata) before returning the routed dataset.

## Related tools

- **Flask** (Web framework for receiving and routing input identifiers through HTTP endpoints)
- **usi.py module** (Parses and processes Universal Spectrum Identifier (USI) format inputs) — https://github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **dash_get_sets.py module** (Data input interface that accepts Task ID and FBMN identifiers and routes to appropriate loaders) — https://github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **requests library** (HTTP library used by loaders to fetch remote spectral data after routing)

## Examples

```
# Python snippet demonstrating conditional routing within the Flask application
identifier = request.form.get('identifier')
if identifier.startswith('mzspec:GNPS2:'):
    dataset = usi_loader.load(identifier)
elif identifier.startswith('TASK-'):
    dataset = task_id_loader.load(identifier, component_num)
else:
    dataset = fbmn_loader.load(identifier, component_num)
validate_dataset(dataset)
```

## Evaluation signals

- The output dataset object contains required mass spectrometry fields: m/z values, intensities, scan numbers, and precursor information without missing or null values.
- The correct loader module was invoked based on identifier format (confirmed via execution logs or code instrumentation).
- Peak alignment or spectral metadata is consistent with the source system (e.g., GNPS task results match the Task ID that was routed).
- The deserialized dataset conforms to the expected schema for downstream visualization (e.g., compatible with plotly or Dash rendering in the spectra alignment visualizer).
- No data loss or format corruption occurred during deserialization (e.g., intensity values remain numeric and m/z values remain within expected mass ranges).

## Limitations

- Identifier parsing relies on strict format matching; ambiguous or malformed identifiers may fail to route correctly or produce cryptic error messages to the user.
- If the remote data source (e.g., GNPS server) is unavailable or returns incomplete data, the loader will fail after routing; no fallback mechanism is documented.
- USI format validation is sensitive to exact string structure (e.g., 'mzspec:GNPS2:TASK-...-nf_output/clustering/specs_ms.mgf:scan:...'); deviations from this pattern will not be recognized.
- Routing logic does not support hybrid or nested formats; each input must be identified as exactly one of Task ID, USI, or FBMN.

## Evidence

- [intro] The application accepts mass spectrometry data through various formats including Task ID, USI, or FBMN, enabling multiple input pathways for data ingestion.: "users to input mass spectrometry data through various formats (Task ID, USI, or FBMN)"
- [other] Parse and validate the identifier format to determine which loader to invoke, then execute the loader to retrieve and deserialize the data into a standardized dataset object.: "Parse and validate the identifier format to determine input type. 3. Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification. 4. Execute the"
- [readme] USI format specification with required structure for GNPS task-based spectral data.: "Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`"
- [readme] The input interface accepts Task ID with component number for GNPS molecular networking results.: "Enter a GNPS Task ID and component number. The application will fetch and process the molecular networking results"
- [other] Validation of the loaded dataset ensures completeness before returning the standardized object.: "Validate the loaded dataset object for completeness and return the routed dataset."
