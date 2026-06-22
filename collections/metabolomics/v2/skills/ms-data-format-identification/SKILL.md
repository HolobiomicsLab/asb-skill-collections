---
name: ms-data-format-identification
description: 'Use when when receiving raw MS data files of unknown or mixed acquisition modalities and needing to route each to its corresponding analysis pipeline. Specifically, apply this skill when: (1) input files arrive without documented instrument type or chromatographic/mobility dimensionality;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
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
---

# ms-data-format-identification

## Summary

Identify and classify mass spectrometry data types (LC, GC, IMS, MS imaging) by scanning file headers, metadata, and instrument signatures to enable correct routing to specialized analysis modules. This skill is essential for automated MS data workflow dispatch in multi-modality platforms like mzmine.

## When to use

When receiving raw MS data files of unknown or mixed acquisition modalities and needing to route each to its corresponding analysis pipeline. Specifically, apply this skill when: (1) input files arrive without documented instrument type or chromatographic/mobility dimensionality; (2) a batch contains multiple data types (e.g., LC-MS alongside IMS data); or (3) module selection must be automated rather than manual.

## When NOT to use

- Input is already labeled with instrument type by the data provider or acquisition software; classification is redundant.
- The analysis goal does not require module routing (e.g., format conversion only, or meta-analysis of already-processed feature tables).
- File metadata is corrupted, incomplete, or non-standard, making reliable signature extraction impossible without manual annotation.

## Inputs

- Raw MS data file (vendor format or open format: mzML, mzXML, NetCDF, vendor binary)
- File headers and metadata (instrument type, chromatography/mobility dimension flags)
- Known mzmine module entry points registry (module names and accepted data types)

## Outputs

- Data type classification label (LC, GC, IMS, or MS imaging)
- Routing configuration record (JSON or structured format mapping input to target module)
- Validation report (boolean: routing is/is not resolvable against known module entry points)

## How to apply

First, scan the input file headers and metadata fields (file format, instrument type, chromatographic and mobility dimensions) to extract acquisition modality signatures. Second, classify the input as LC, GC, IMS, or MS imaging based on detected instrument signature and presence/absence of chromatographic or ion mobility separation dimensions. Third, generate a routing configuration record (JSON or structured format) mapping the classified input to its target mzmine analysis module (e.g., LC-MS module for LC inputs, IMS module for IMS inputs). Finally, validate routing assignments against known mzmine module entry points to ensure each route is resolvable and the module can accept the classified data type. The rationale is that mzmine's modular architecture requires correct module selection upfront; misclassification leads to processing errors or incompatible parameter sets.

## Related tools

- **mzmine** (Target platform for MS data import, classification, and modular analysis dispatch; provides module registry and routing entry points) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime environment for mzmine; required for file I/O, metadata parsing, and routing logic execution)
- **JavaFX 24** (GUI framework for mzmine; supports display of classification results and routing configuration validation)

## Evaluation signals

- Extracted metadata (instrument type, chromatography/mobility flags) match file format specifications and do not contain null or contradictory values.
- Classification label is one of {LC, GC, IMS, MS imaging} and is consistent with detected instrument signature and dimensionality.
- Routing configuration record maps the classified input to a registered mzmine module name that exists in the module entry points registry.
- Module validation resolves successfully: the target module's input type constraints are satisfied by the classified data type.
- Round-trip check: re-reading the routing record and re-classifying the input produces the same module assignment (deterministic classification).

## Limitations

- File metadata may be incomplete, non-standard, or instrument-vendor-specific, making signature extraction unreliable for rare or legacy instruments.
- Some data types (e.g., hybrid LC-IMS-MS) may have overlapping signatures; classification may be ambiguous without additional context or user override.
- mzmine's module registry is version-dependent; routing may fail if modules are renamed, removed, or have differing input type constraints across releases.
- No changelog found in the repository, so changes to supported data types or module routing rules are not explicitly documented.

## Evidence

- [other] mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across specialized analysis modules.: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
- [other] Input classification method: scan headers and metadata, then map to target modules.: "1. Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality. 2. Classify input as LC, GC, IMS, or MS imaging based on detected instrument"
- [readme] The project provides a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow.: "The goals of the project is to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
- [other] Validation step ensures routing is resolvable against known module entry points.: "Validate routing assignments against known mzmine module entry points to ensure each route is resolvable"
