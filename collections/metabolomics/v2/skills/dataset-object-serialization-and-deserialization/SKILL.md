---
name: dataset-object-serialization-and-deserialization
description: Use when you have mass spectrometry data arriving through heterogeneous input formats (Task ID from GNPS, Universal Spectrum Identifiers, or Feature-Based Molecular Networking identifiers) and need to load, validate, and store them as a single standardized dataset object for interactive peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Flask
  - usi.py
  - alignment.py
  - dash_get_sets.py
  - pandas
  - requests
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

# dataset-object-serialization-and-deserialization

## Summary

Convert mass spectrometry data from multiple input identifier formats (Task ID, USI, FBMN) into standardized in-memory dataset objects, and persist them as JSON for downstream visualization and analysis. This skill bridges disparate data entry points with a unified internal representation.

## When to use

Apply this skill when you have mass spectrometry data arriving through heterogeneous input formats (Task ID from GNPS, Universal Spectrum Identifiers, or Feature-Based Molecular Networking identifiers) and need to load, validate, and store them as a single standardized dataset object for interactive peak alignment visualization and filtering.

## When NOT to use

- Input data is already a deserialized in-memory dataset object (skip loader routing; proceed directly to validation)
- Mass spectrometry data is in a format not supported by Task ID, USI, or FBMN loaders (e.g., raw mzML or mzXML files without a GNPS Task ID wrapper)
- The identifier format cannot be reliably parsed or validated against expected patterns (malformed USI, invalid Task ID)

## Inputs

- GNPS Task ID string (format: task ID and component number)
- Universal Spectrum Identifier (USI) list (format: mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>)
- FBMN Task ID and component numbers
- Remote API endpoints (GNPS API, GNPS2 spectra service)

## Outputs

- Standardized dataset object (in-memory Python dict/object with aligned peaks, m/z, intensity, scan metadata)
- JSON serialization of dataset (written to ./temp/sets/<session-id>.json)
- Validated dataset object ready for peak alignment visualization

## How to apply

First, parse and validate the incoming identifier to determine its format (Task ID, USI, or FBMN). Route the validated identifier to the appropriate loader function: the Task ID loader calls the GNPS API to fetch molecular networking results, the USI loader retrieves individual spectra from the GNPS2 infrastructure, or the FBMN loader accesses feature-based networking clusters. Execute the selected loader to deserialize the remote or cached mass spectrometry data into a standardized dataset object containing aligned peaks, m/z values, and intensity metadata. Validate the loaded object for completeness (presence of required fields: peaks, m/z ranges, intensity values, and spectrum identifiers). Serialize the validated dataset to JSON format in a temporary storage location (SETS_TEMP_PATH) for session-specific retrieval and rendering by the visualization interface.

## Related tools

- **Flask** (Web framework routing multi-format input identifiers to appropriate loaders)
- **usi.py** (USI parsing and spectrum retrieval utilities for Universal Spectrum Identifier deserialization) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **alignment.py** (Core module for dataset object construction and peak alignment data structure validation) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **dash_get_sets.py** (Data input interface handling identifier ingestion and triggering loader selection) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **pandas** (Data manipulation for peak alignment tabulation and intensity metadata normalization)
- **requests** (HTTP client for remote GNPS API and GNPS2 spectrum service calls during loader execution)

## Evaluation signals

- Loaded dataset object contains non-empty 'peaks' array with m/z and intensity tuples for each spectrum
- All required metadata fields are present: spectrum identifiers (scan numbers or USI), precursor m/z, and alignment set memberships
- JSON serialization round-trip: deserialize the written JSON file and verify that the reconstructed object matches the original in-memory object (field-by-field equality)
- Peak m/z values are within physically plausible range (typically 50–2000 m/z for small molecules; application-dependent) and intensities are non-negative
- Spectrum ordering and alignment set assignments remain consistent across loaders for the same underlying data

## Limitations

- Loader routing is identifier-format dependent; if an identifier does not match Task ID, USI, or FBMN patterns, routing fails and no dataset object is created
- Remote API calls (GNPS, GNPS2) may fail or timeout if the external service is unavailable; no fallback deserialization from local cache is documented
- JSON serialization does not preserve Python object types (e.g., NumPy arrays, custom classes); deserialized objects may require type coercion before downstream analysis
- No changelog documented; version compatibility between loader implementations and remote API schemas is not tracked

## Evidence

- [other] Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object.: "Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object."
- [other] Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification.: "Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification."
- [intro] users to input mass spectrometry data through various formats (Task ID, USI, or FBMN): "users to input mass spectrometry data through various formats (Task ID, USI, or FBMN)"
- [readme] Click 'Process and Save JSON' to generate alignment data: "Click "Process and Save JSON" to generate alignment data"
- [readme] SETS_TEMP_PATH: Temporary storage for processed JSON files (./temp/sets): "SETS_TEMP_PATH: Temporary storage for processed JSON files (`./temp/sets`)"
- [readme] Each USI should follow the format: mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>: "Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`"
