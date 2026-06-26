---
name: data-type-classification-schema-design
description: Use when building or auditing a multi-instrument MS data processing system
  that must route different chromatography modes (LC, GC), ion mobility, or imaging
  modalities (MALDI) to distinct processing workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-021-23953-9
  title: iimn
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iimn
    doi: 10.1038/s41467-021-23953-9
    title: iimn
  dedup_kept_from: coll_iimn
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-021-23953-9
  all_source_dois:
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-type-classification-schema-design

## Summary

Design and implement a data-type classification schema that declares and categorizes mass spectrometry input types (LC, GC, IMS, MS imaging) to enable selective, type-aware processing module dispatch. This skill bridges raw data ingestion with intelligent module routing, ensuring each input is processed by the appropriate analytical pipeline.

## When to use

Apply this skill when building or auditing a multi-instrument MS data processing system that must route different chromatography modes (LC, GC), ion mobility, or imaging modalities (MALDI) to distinct processing workflows. Use it when you need to formalize how input data declares its type so that downstream modules can conditionally activate based on that declaration.

## When NOT to use

- Input data already carries explicit, validated type annotations from a trusted upstream system—classify only once, at the earliest ingestion point.
- The analysis pipeline is single-instrument or single-modality and does not require type-conditional branching.
- Type information is permanently embedded in file structure (e.g., a read-only binary header) with no ambiguity—schema design is unnecessary; only implement direct lookup.

## Inputs

- Raw MS data files (mzML, NetCDF, vendor formats) with embedded or declared data-type metadata
- Configuration or UI selection indicating chromatography mode or imaging modality
- Module registry or factory configuration (e.g., Spring beans, interface implementations)
- Optional: instrument vendor name or file format hint

## Outputs

- Data-type classification schema (enum, class hierarchy, or interface definition)
- Type-to-module routing map (conditional dispatch rules, decision tree, or factory configuration)
- Control-flow diagram or pseudocode documenting all dispatch pathways and fallback behavior
- Validated routing logic with coverage matrix (each data type → assigned module set)

## How to apply

First, identify or design the enumeration or interface that represents the set of supported data types (LC, GC, IMS, MS imaging). Second, establish where and how input files or metadata declare their type—this may be embedded in file headers, user UI selections, or configuration parameters. Third, trace the conditional logic (if/switch statements, factory pattern, or dependency injection) that maps each declared type to its corresponding processing module set. Fourth, document the fallback behavior when type is ambiguous or unsupported. Fifth, validate the schema by checking that all known instrument types from the supported MS ecosystem can be unambiguously classified into one of the declared categories. Finally, synthesize the complete routing logic as control-flow pseudocode or a decision diagram, including edge cases such as hybrid instruments or type-detection failures.

## Related tools

- **mzmine** (Host software platform that implements module dispatch routing for LC, GC, IMS, and MS imaging data types; serves as the reference implementation for this schema design skill) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime and language framework used to implement the type classification schema and dispatch conditionals)
- **JavaFX 24** (UI framework for presenting data-type selection and routing status to users during input configuration)

## Evaluation signals

- All declared data types (LC, GC, IMS, MS imaging) have unambiguous dispatch rules; no type falls through to a default or error handler unless explicitly intended as a fallback.
- Each supported MS instrument in the ecosystem can be classified into exactly one data type; coverage matrix shows no gaps or overlaps.
- When a known instrument file (e.g., a Thermo .raw or Waters .raw with known chromatography mode) is ingested, the schema correctly identifies and routes it to the expected module set.
- Conditional logic in the routing code (if/switch/factory) is exhaustive and matches the schema diagram; no unreachable branches or missing cases.
- User or automated system can explicitly override inferred type; override is validated against the schema and either accepted or rejected with a clear error message.

## Limitations

- Type declaration may be ambiguous or missing in legacy or vendor-specific file formats; fallback behavior must be documented and tested.
- Hybrid instruments (e.g., LC-IM-MS or imaging coupled to chromatography) may not fit cleanly into a single category; schema must either define composite types or document how such instruments are decomposed into sequential single-type analyses.
- Schema version evolution: as new MS modalities emerge (e.g., trapped ion mobility, hybrid imaging modes), the enum or interface must be extended; backward compatibility of existing dispatch rules is not guaranteed.

## Evidence

- [intro] mzmine supports selective processing module dispatch across liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), and MS imaging (e.g., MALDI) data types: "mzmine supports selective processing module dispatch across liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), and MS imaging (e.g., MALDI) data types"
- [other] The workflow explicitly traces conditional branching logic (if/switch statements or factory pattern) that maps each data type to its corresponding processing module: "Trace the conditional branching logic (if/switch statements or factory pattern) that maps each data type to its corresponding processing module."
- [readme] mzmine provides a complete set of modules covering the entire MS data analysis workflow with support for most MS instruments: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
- [other] The workflow requires synthesizing routing logic as a control-flow diagram or pseudocode, documenting each pathway and the criteria that trigger it: "Synthesize the routing logic as a control-flow diagram or pseudocode, documenting each pathway and the criteria that trigger it."
