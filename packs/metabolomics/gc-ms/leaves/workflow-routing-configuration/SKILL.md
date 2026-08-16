---
name: workflow-routing-configuration
description: Use when when you have raw mass spectrometry data files from multiple acquisition modalities (LC-MS, GC-MS, ion mobility, or imaging) and need to automatically route each to the correct downstream analysis module without manual intervention.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1038/s41587-023-01690-2
  title: mzmine3
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzmine_3_data_processing_annotation_prot_cq
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  dedup_kept_from: coll_mzmine_3_data_processing_annotation_prot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01690-2
  all_source_dois:
  - 10.1038/s41587-023-01690-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-routing-configuration

## Summary

Detect and classify mass spectrometry input data types (LC, GC, IMS, MS imaging) from file headers and metadata, then generate a routing configuration that maps each classified input to its corresponding mzmine analysis module. This enables flexible dispatch of heterogeneous MS data to specialized processing pipelines.

## When to use

When you have raw mass spectrometry data files from multiple acquisition modalities (LC-MS, GC-MS, ion mobility, or imaging) and need to automatically route each to the correct downstream analysis module without manual intervention. Applicable at the entry point of a mzmine workflow when input data type is unknown or heterogeneous.

## When NOT to use

- Input data type is already known and pre-classified upstream
- Single-modality workflow where all inputs are guaranteed to be the same type (e.g., LC-MS only)
- Data has already been processed and imported; routing is only needed at raw data ingestion

## Inputs

- Raw MS data file (various formats: mzML, mzXML, proprietary vendor formats)
- File header metadata and instrument type fields
- mzmine module registry or configuration schema

## Outputs

- Routing configuration record (JSON or structured format)
- Classified data type label (LC | GC | IMS | MS imaging)
- Target module entry point reference

## How to apply

Scan raw MS input file headers and embedded metadata fields (file format signature, instrument type, presence of chromatographic or mobility dimensions) to identify the acquisition modality. Classify the input as LC, GC, IMS, or MS imaging based on detected instrument signatures and dimensional characteristics. Generate a routing configuration record (JSON or structured format) that maps the classified input to its target mzmine module entry point (e.g., LC-MS module for LC inputs, IMS module for IMS inputs). Validate each routing assignment against known mzmine module entry points to ensure the route is resolvable and will not fail at dispatch time.

## Related tools

- **mzmine** (Modular MS data analysis platform providing specialized analysis modules for LC, GC, IMS, and MS imaging; the routing configuration dispatches input data to the appropriate module) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime and compilation environment for building and executing mzmine)
- **JavaFX 24** (UI toolkit for mzmine graphical interface and workflow configuration display)

## Evaluation signals

- Routing configuration is valid JSON or structured format with no parse errors
- Classified data type (LC | GC | IMS | MS imaging) matches the actual instrument modality in the raw file metadata
- Target module entry point exists in mzmine module registry and is resolvable without exception
- Routed data successfully enters the correct analysis module without type mismatch errors
- Routing assignment is deterministic and reproducible for the same input file on repeated runs

## Limitations

- Accuracy depends on presence and correctness of file header metadata; malformed or missing instrument type fields may lead to misclassification
- mzmine module registry must be up-to-date; new or deprecated modules may cause routing to fail
- No changelog documented in the project; breaking changes to module entry points or supported data types may not be tracked
- Hybrid or non-standard data types not matching the primary four categories (LC, GC, IMS, MS imaging) may not be routable

## Evidence

- [other] Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality. Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions.: "Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality. Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature"
- [other] Generate a routing configuration record (JSON or structured format) mapping each classified input to its target mzmine analysis module (e.g., LC-MS module for LC inputs, IMS module for IMS inputs).: "Generate a routing configuration record (JSON or structured format) mapping each classified input to its target mzmine analysis module (e.g., LC-MS module for LC inputs, IMS module for IMS inputs)."
- [other] mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across specialized analysis modules.: "mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across"
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
- [readme] The goals of the project is to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow: "The goals of the project is to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
