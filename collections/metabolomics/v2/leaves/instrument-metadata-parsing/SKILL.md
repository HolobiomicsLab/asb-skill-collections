---
name: instrument-metadata-parsing
description: Use when when you have raw or semi-processed mass spectrometry data files
  in mixed formats (e.g., vendor-native .raw, .d, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
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

# instrument-metadata-parsing

## Summary

Extract and parse instrument type, chromatographic modality, and data acquisition signatures from MS file headers and metadata to enable automated classification and routing of heterogeneous MS data (LC, GC, IMS, MS imaging) to specialized analysis modules. This skill is essential for building flexible, data-type-agnostic workflows that dispatch raw data to the correct downstream processors.

## When to use

When you have raw or semi-processed mass spectrometry data files in mixed formats (e.g., vendor-native .raw, .d, .ms, mzML, or mzXML) acquired on different instrument types (Orbitrap, Q-TOF, MALDI, drift tube IMS) and you need to automatically route each file to its corresponding mzmine analysis module (LC-MS, GC-MS, IMS, or MS imaging) without manual curation. This skill is especially valuable in high-throughput pipelines where manual file classification is infeasible.

## When NOT to use

- Input is already a processed feature table, consensus spectrum, or quantified matrix (skip routing; apply downstream analysis directly).
- Data originates from a single, homogeneous instrument platform and a static analysis module is acceptable (instrument-agnostic routing overhead is not justified).
- File headers are corrupted, redacted, or metadata fields are missing; metadata repair/inference is required first.

## Inputs

- Raw MS data file (vendor-native format: .raw, .d, .ms, or open format: mzML, mzXML)
- File header and metadata (binary or XML serialized)
- Instrument type signature field (e.g., 'instrument model', 'instrument type' metadata tag)
- Chromatographic/mobility dimension indicators (retention time, drift time presence flags)

## Outputs

- Instrument classification label (LC, GC, IMS, or MS imaging)
- Routing configuration record (JSON or key-value map)
- Target mzmine module identifier (e.g., 'LCMSModule', 'IMSModule', 'MSImagingModule')
- Validation status (Boolean or confidence score)

## How to apply

Parse the input file's header and metadata fields (e.g., instrument model, chromatographic dimension presence, ion mobility field) to identify the data acquisition modality. Cross-reference detected instrument signatures and dimensional characteristics (presence of retention time, drift time, imaging coordinates) against known mzmine instrument profiles to classify the input as LC, GC, IMS, or MS imaging. Generate a routing configuration (JSON or structured record) mapping the classified input to its target mzmine module entry point. Validate the routing assignment by confirming the target module is registered in the mzmine module registry and can consume the detected file format. Return the classification result and routing directive for consumption by the dispatch orchestrator.

## Related tools

- **mzmine** (MS data processing framework; host platform that contains the instrument classifier, module registry, and routing dispatcher; receives classification output to instantiate the appropriate LC-MS, GC-MS, IMS, or MS imaging module.) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime environment; required for building and running mzmine metadata parsing and module dispatch logic.)
- **JavaFX 24** (GUI framework for interactive visualization of instrument classification results and routing diagnostics (optional for CLI-only deployments).)

## Evaluation signals

- Classification result matches the expected instrument type (LC, GC, IMS, or MS imaging) for a known test file; verify by manual inspection of vendor metadata or instrument documentation.
- Routing target module is resolvable in the mzmine module registry and its entry point is callable without errors.
- File format consumed by the target module matches the input file format (no format mismatch exceptions on module instantiation).
- Metadata parsing extracts all required fields (instrument model, chromatographic dimension flags, acquisition mode) without null or empty value returns.
- Routing configuration JSON/record is schema-valid and all required keys are populated (classification, target_module, confidence, timestamp).

## Limitations

- Metadata parsing relies on standardized header formats and field naming conventions; non-standard or vendor-specific headers may fail to classify correctly and require custom parsers.
- Instrument signatures are matched against a pre-defined mzmine profile registry; new or rare instrument types not in the registry will be classified as unknown and routed to a default fallback module, potentially causing analysis artifacts.
- Hybrid acquisition modes (e.g., simultaneous LC and IMS) or multi-modality datasets may produce ambiguous classifications; current routing assumes mutually exclusive modalities.
- No changelog found in the repository, so version-specific metadata format changes or new instrument support additions may not be documented.

## Evidence

- [other] mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types: "mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging"
- [other] Scan input file headers and metadata to identify data acquisition modality: "Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality."
- [other] Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature: "Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions."
- [other] Generate a routing configuration record mapping each classified input to its target mzmine analysis module: "Generate a routing configuration record (JSON or structured format) mapping each classified input to its target mzmine analysis module (e.g., LC-MS module for LC inputs, IMS module for IMS inputs)."
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
