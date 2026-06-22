---
name: identifier-format-parsing-and-validation
description: Use when you receive mass spectrometry data through heterogeneous identifier formats—specifically when the input could be a GNPS Task ID, a Universal Spectrum Identifier (USI), or a Feature-Based Molecular Networking (FBMN) identifier—and you need to programmatically determine which format was.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GNPS (Global Natural Products Social Molecular Networking)
  - USI (Universal Spectrum Identifier) Registry
  - usi.py (USI processing utilities)
  - Flask
  techniques:
  - LC-MS
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

# identifier-format-parsing-and-validation

## Summary

Parse and validate mass spectrometry data input identifiers (Task ID, USI, or FBMN format) to determine their type and route them to the appropriate data loader. This skill enables a web application to accept multiple input pathways for molecular networking data ingestion.

## When to use

Apply this skill when you receive mass spectrometry data through heterogeneous identifier formats—specifically when the input could be a GNPS Task ID, a Universal Spectrum Identifier (USI), or a Feature-Based Molecular Networking (FBMN) identifier—and you need to programmatically determine which format was provided and dispatch it to the correct loader without manual intervention.

## When NOT to use

- Input is already pre-classified with its format type and requires no re-validation
- Input data are already deserialized into a standardized dataset object (parsing is redundant)
- Input follows a proprietary or non-standard identifier format not covered by Task ID, USI, or FBMN specifications

## Inputs

- mass spectrometry data input identifier string (raw user input)
- identifier format specification or schema (Task ID pattern, USI pattern, FBMN pattern)

## Outputs

- classified identifier type (one of: 'Task ID', 'USI', 'FBMN')
- validated identifier object with format-specific metadata
- loader routing instruction (e.g., invoke Task ID loader, USI loader, or FBMN loader)

## How to apply

Implement a classification workflow that examines the structure and format of the input identifier string. First, attempt to match against known patterns: Task IDs typically follow alphanumeric task naming; USI identifiers follow the format mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>; FBMN identifiers are FBMN Task IDs with component numbers. Once format is identified, validate structural correctness (character counts, special characters, required fields). Then route the validated identifier to its respective loader: Task ID loader retrieves and processes molecular networking results; USI loader fetches individual spectra from the USI registry; FBMN loader processes feature-based networking clusters. Return the identifier type classification and validated identifier object for downstream processing.

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (source registry and workflow engine providing Task ID and FBMN identifiers for molecular networking results)
- **USI (Universal Spectrum Identifier) Registry** (standardized identifier format and lookup service for individual mass spectra across distributed repositories)
- **usi.py (USI processing utilities)** (Python module for parsing, validating, and resolving USI format identifiers to retrieve spectrum data) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **Flask** (web framework for receiving and routing parsed identifier formats to appropriate backend loaders)

## Evaluation signals

- Identifier classification matches expected format (e.g., USI string contains 'mzspec:GNPS2:TASK-' prefix and 'scan:' field)
- Parsed identifier passes structural validation (required fields present, character types match pattern, no truncation or corruption)
- Identifier is successfully routed to correct loader and produces non-null dataset retrieval response
- Multiple input formats in a batch are classified with 100% accuracy against ground-truth labels
- Routed dataset object contains standardized mass spectrometry fields (e.g., m/z values, intensities, scan metadata)

## Limitations

- Ambiguous or malformed identifiers that partially match multiple format patterns may require interactive user confirmation rather than automatic classification
- USI resolution depends on registry availability and network connectivity; offline or degraded registry service will cause USI validation to fail
- Task ID and FBMN loaders depend on GNPS web service availability; network failures or deprecated task IDs will prevent data retrieval
- No changelog or version history documented in the application, making it unclear whether identifier format specifications have evolved over time

## Evidence

- [intro] The application accepts mass spectrometry data through various formats including Task ID, USI, or FBMN, enabling multiple input pathways for data ingestion.: "users to input mass spectrometry data through various formats (Task ID, USI, or FBMN)"
- [other] Workflow demonstrates parsing and classification as the first steps before routing to loaders.: "Parse and validate the identifier format to determine input type. 3. Route to the appropriate loader: Task ID loader, USI loader, or FBMN loader based on identifier classification."
- [readme] USI identifiers follow a structured format specification.: "Each USI should follow the format: `mzspec:GNPS2:TASK-<task-id>-nf_output/clustering/specs_ms.mgf:scan:<scan-number>`"
- [readme] The usi.py module is explicitly used for USI processing.: "usi.py                          # USI processing utilities"
