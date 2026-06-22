---
name: imaging-mass-spectrometry-characterization
description: Use when you have raw mass spectrometry data files (mzML, NetCDF, or vendor formats) with unknown or mixed acquisition modalities, and you need to automatically determine whether the input is LC-MS, GC-MS, IMS (ion mobility spectrometry), or MS imaging (e.
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

# imaging-mass-spectrometry-characterization

## Summary

Detect and classify mass spectrometry imaging data (e.g., MALDI) from raw instrument output by scanning file headers and metadata, then route the classified input to the appropriate mzmine analysis module. This skill enables flexible handling of multiple MS modalities within a unified workflow.

## When to use

You have raw mass spectrometry data files (mzML, NetCDF, or vendor formats) with unknown or mixed acquisition modalities, and you need to automatically determine whether the input is LC-MS, GC-MS, IMS (ion mobility spectrometry), or MS imaging (e.g., MALDI) in order to dispatch it to the correct downstream processing module.

## When NOT to use

- Input data is already preprocessed and classified by an external system with known validity — skipping re-classification saves computation.
- The data acquisition modality is already documented in project metadata or sample manifest — use existing annotations rather than re-scanning headers.
- Single-modality batch processing where all inputs are guaranteed to be the same modality (e.g., all LC-MS) — direct routing without classification is more efficient.

## Inputs

- Raw mass spectrometry data files (mzML, NetCDF, vendor-specific formats)
- File header metadata and instrument type fields
- Acquisition modality indicators (chromatographic dimensions, ion mobility dimensions, spatial coordinates)

## Outputs

- Data type classification (LC, GC, IMS, or MS imaging)
- Routing configuration record (JSON or structured format)
- Validated routing assignment to target mzmine module
- Dispatched input ready for module-specific processing

## How to apply

Begin by extracting and parsing file headers and instrument metadata fields to identify the data acquisition modality signature (e.g., presence of chromatographic time dimension, ion mobility dimension, or 2D spatial coordinates). Classify the input as one of: LC, GC, IMS, or MS imaging based on the detected instrument signature and dimensional structure. Generate a routing configuration record (JSON or structured format) that maps the classified input to its target mzmine module entry point (e.g., LC-MS module for LC inputs, IMS module for IMS inputs). Validate the routing assignment against the known set of resolvable mzmine module entry points to ensure the route is valid and can be executed. Use mzmine's module dispatch system to automatically route each classified input to its specialized analysis module.

## Related tools

- **mzmine** (Primary platform for MS data analysis; provides modular dispatch system and analysis modules (LC-MS, IMS, MS imaging) for routing classified inputs) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime environment required to build and execute mzmine)
- **JavaFX 24** (GUI framework for mzmine user interface and visualization)

## Evaluation signals

- Extracted instrument metadata fields match known signatures for at least one of: LC, GC, IMS, or MS imaging modality.
- Routing configuration record is valid JSON or structured format and contains a resolvable mzmine module entry point.
- Validation check confirms the target module is registered and accessible in the current mzmine module registry.
- Input file is successfully dispatched to the assigned module without routing errors or module-not-found exceptions.
- Output from the assigned module (e.g., feature detection, ion image reconstruction) is consistent with the data modality (e.g., spatial images for MS imaging, drift-time traces for IMS).

## Limitations

- Relies on complete and correctly formatted file headers and metadata; corrupted or non-standard instrument files may fail classification.
- Classification is based on instrument signature heuristics; hybrid or non-standard acquisition protocols may not fit cleanly into LC, GC, IMS, or MS imaging categories.
- Routing assumes all target modules are installed and registered in the mzmine instance; missing or disabled modules will cause routing failures.
- No changelog available in the repository to track changes to metadata parsing or routing rules across mzmine versions.

## Evidence

- [other] mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging to enable flexible routing across specialized analysis modules.: "mzmine provides a complete set of modules covering the entire MS data analysis workflow, with support for multiple data types including LC, GC, IMS, and MS imaging"
- [other] Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality.: "Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality."
- [other] Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions.: "Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions."
- [other] Generate a routing configuration record (JSON or structured format) mapping each classified input to its target mzmine analysis module.: "Generate a routing configuration record (JSON or structured format) mapping each classified input to its target mzmine analysis module"
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
