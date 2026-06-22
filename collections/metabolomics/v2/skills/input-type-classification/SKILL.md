---
name: input-type-classification
description: Use when a web application receives mass spectrometry data through heterogeneous identifier formats and must automatically determine which loader (Task ID, USI, or FBMN) should process the input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - Flask
  - dash_get_sets.py
  - usi.py
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
---

# input-type-classification

## Summary

Classify mass spectrometry data input identifiers (Task ID, USI, or FBMN format) to route them to the correct data loader and retrieval pathway. This skill enables a web application to accept multiple standardized input formats and dispatch them to specialized parsers without manual user intervention.

## When to use

Apply this skill when a web application receives mass spectrometry data through heterogeneous identifier formats and must automatically determine which loader (Task ID, USI, or FBMN) should process the input. Use it at the entry point of data ingestion pipelines where users may provide data in any of the supported formats interchangeably.

## When NOT to use

- Input is already a fully deserialized mass spectrometry dataset object (e.g., already loaded into memory or a feature table)
- Input identifier format is not one of the three supported types (Task ID, USI, FBMN) and requires a custom or external loader
- Data source is pre-cached or pre-indexed and requires no runtime classification or retrieval

## Inputs

- Mass spectrometry data input identifier string (Task ID, USI, or FBMN format)
- Identifier format specification or pattern matching rules

## Outputs

- Classified input type label (Task ID, USI, or FBMN)
- Routed and deserialized mass spectrometry dataset object
- Validation status (pass/fail) indicating dataset completeness

## How to apply

Parse the incoming identifier string to extract its structural features: Task ID identifiers follow a GNPS Task ID pattern, USI identifiers begin with the mzspec: prefix and contain scan= and task-id references, and FBMN identifiers reference Feature-Based Molecular Networking tasks. Validate the parsed format against known patterns for each input type. Route the classified identifier to its corresponding loader (Task ID loader, USI loader, or FBMN loader), which then retrieves and deserializes the mass spectrometry data into a standardized dataset object. Validate the loaded dataset for completeness (presence of required spectra, m/z arrays, intensity arrays) before returning. The rationale is that each format contains metadata that uniquely identifies its source repository and retrieval method, allowing deterministic routing without ambiguity.

## Related tools

- **Flask** (Web framework for routing HTTP requests and invoking the classification logic)
- **dash_get_sets.py** (Data input interface module that orchestrates identifier validation and routing) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **usi.py** (USI-specific processing utilities for parsing and validating Universal Spectrum Identifiers) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website

## Evaluation signals

- Classified input type matches the actual format of the input identifier (verify by regex or pattern matching against known format signatures)
- Routed loader module is the correct one for the classified type (check that Task ID inputs invoke Task ID loader, USI inputs invoke USI loader, etc.)
- Returned dataset object contains all required fields: precursor m/z array, scan identifiers, and intensity arrays for each spectrum
- Validation status is 'pass' only when dataset is non-empty and contains at least one complete spectrum with valid m/z and intensity data
- No dataset is returned or validation fails if the identifier cannot be parsed or the loader returns incomplete data

## Limitations

- Classification relies on deterministic pattern matching; malformed identifiers that partially resemble multiple formats may be misclassified
- The skill assumes identifier formats are mutually exclusive; if a future format shares syntax with an existing one, disambiguation logic must be refined
- No changelog is available to track format specification changes or breaking updates to identifier syntax across GNPS versions
- Classification does not validate that the identifier actually exists in the source repository; it only confirms syntactic correctness

## Evidence

- [other] Parse and validate the identifier format to determine input type. 3. Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification.: "Parse and validate the identifier format to determine input type. 3. Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification."
- [other] The application accepts mass spectrometry data through various formats including Task ID, USI, or FBMN, enabling multiple input pathways for data ingestion.: "The application accepts mass spectrometry data through various formats including Task ID, USI, or FBMN, enabling multiple input pathways for data ingestion."
- [readme] users to input mass spectrometry data through various formats (Task ID, USI, or FBMN): "users to input mass spectrometry data through various formats (Task ID, USI, or FBMN)"
- [readme] Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`: "Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`"
- [other] Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object.: "Execute the selected loader to retrieve and deserialize the mass spectrometry data into a standardized dataset object."
