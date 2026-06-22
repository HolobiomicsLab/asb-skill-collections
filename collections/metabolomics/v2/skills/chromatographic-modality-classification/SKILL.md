---
name: chromatographic-modality-classification
description: Use when when ingesting raw or vendor-format mass spectrometry data files of unknown or mixed acquisition modality, and you need to automatically determine whether the input originated from liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), or MS imaging (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01690-2
  all_source_dois:
  - 10.1038/s41587-023-01690-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-modality-classification

## Summary

Detects and classifies mass spectrometry input data by acquisition modality (LC, GC, IMS, MS imaging) through file header and metadata inspection, enabling automatic routing to the appropriate mzmine analysis module. This skill is essential for flexible, modality-aware data processing workflows that must handle heterogeneous MS instrument types.

## When to use

When ingesting raw or vendor-format mass spectrometry data files of unknown or mixed acquisition modality, and you need to automatically determine whether the input originated from liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), or MS imaging (e.g., MALDI) systems, so that it can be routed to the correct downstream analysis module.

## When NOT to use

- Input data has already been processed and annotated with explicit modality metadata from a prior step; skip classification and use the existing label directly.
- The mass spectrometry data is from an instrument type not covered by mzmine's supported modalities (LC, GC, IMS, MS imaging); classification will fail or misroute.
- File headers are corrupted, missing, or use non-standard metadata fields incompatible with mzmine's header-scanning logic; metadata inspection will yield unreliable classification.

## Inputs

- Raw mass spectrometry data file (vendor format or mzML/NetCDF)
- File header metadata (instrument type, chromatographic/mobility dimensions)
- mzmine module registry or entry-point configuration

## Outputs

- Classified data modality label (LC | GC | IMS | MS imaging)
- Routing configuration record (JSON or structured format)
- Validated module dispatch target (entry point reference)

## How to apply

Scan the input file's header metadata and instrument-type fields to extract the data acquisition signature (e.g., chromatographic dimension presence, mobility dimension presence, imaging raster information). Classify the input into one of four categories—LC, GC, IMS, or MS imaging—based on detected instrument identifiers and dimensional characteristics. Generate a structured routing configuration (JSON or equivalent format) that maps the classified input to its target mzmine analysis module (e.g., LC-MS module for LC inputs, IMS module for IMS inputs). Validate the routing assignment against the known entry points of mzmine's module registry to ensure the route is resolvable before dispatch. This approach leverages mzmine's modular architecture to support the entire MS data analysis workflow without requiring manual user intervention to specify the data type.

## Related tools

- **mzmine** (Open-source mass spectrometry data processing framework that provides the modular analysis infrastructure, module registry, and metadata inspection APIs required to classify input data and dispatch to LC, GC, IMS, or MS imaging modules.) — https://github.com/mzmine/mzmine
- **JDK 25** (Java Development Kit version used to build and run mzmine; required for compilation and runtime of the classification and routing logic.)
- **JavaFX 24** (GUI framework used by mzmine to display classification results and module routing configuration in the user interface.)

## Evaluation signals

- Classified modality label is one of the four known categories (LC, GC, IMS, MS imaging) and matches the expected instrument type from the file header or metadata.
- Generated routing configuration JSON is well-formed, contains no null module references, and all module entry points resolve against the mzmine module registry without exceptions.
- Routing target matches the modality classification: LC inputs → LC-MS module, IMS inputs → IMS module, GC inputs → GC module, MS imaging inputs → imaging module.
- File header metadata extraction does not fail or throw exceptions; all required fields (instrument type, chromatographic/mobility dimensions) are successfully parsed.
- Manual spot-check of a representative sample of classified files confirms that the assigned modality and module target are appropriate for downstream analysis (e.g., LC data routed to LC-MS is processed correctly without dimension mismatch errors).

## Limitations

- Metadata-driven classification depends on file headers being present, well-formed, and populated with standard instrument-type and dimensional fields; vendors or custom instruments with non-standard or missing headers will cause misclassification or routing failures.
- mzmine's current module support is limited to LC, GC, IMS, and MS imaging; hybrid or emerging modalities (e.g., LC-IMS-MS) may not have unambiguous classification paths and could be misrouted or require post-hoc correction.
- No changelog or versioning information provided; it is unclear whether metadata field names or routing logic have changed across mzmine versions, which could affect reproducibility of classification across different mzmine releases.

## Evidence

- [other] How does mzmine detect and differentiate input data types (LC, GC, IMS, MS imaging) to route each to its corresponding analysis module?: "How does mzmine detect and differentiate input data types (LC, GC, IMS, MS imaging) to route each to its corresponding analysis module?"
- [other] Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality.: "Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality."
- [other] Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions.: "Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions."
- [other] mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across specialized analysis modules.: "mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across"
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
