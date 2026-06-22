---
name: ion-mobility-dimension-detection
description: Use when when processing raw mass spectrometry data files of unknown or mixed provenance, and you need to automatically route IMS inputs to their corresponding analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3823
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

# ion-mobility-dimension-detection

## Summary

Detect and classify ion mobility spectrometry (IMS) data dimensions from raw MS file headers and metadata to enable routing to specialized IMS analysis modules. This skill disambiguates IMS inputs from LC-MS, GC-MS, and MS imaging modalities by scanning instrument signatures and chromatographic/mobility dimensional markers.

## When to use

When processing raw mass spectrometry data files of unknown or mixed provenance, and you need to automatically route IMS inputs to their corresponding analysis pipeline. Use this skill at the entry point of a data processing workflow when file format and instrument type are available but the data modality (LC vs. GC vs. IMS vs. MS imaging) has not yet been explicitly declared.

## When NOT to use

- Input data is already classified as LC-MS, GC-MS, or MS imaging and routing decision is already made.
- File headers lack sufficient metadata to distinguish mobility dimensions from chromatographic retention time.
- IMS module is not available or not installed in the target mzmine instance.

## Inputs

- Raw MS data file (mzML, mzXML, or native instrument format)
- File header and metadata structure (instrument type, acquisition modality fields)
- Known mzmine module entry points registry

## Outputs

- Data modality classification label (e.g., 'IMS')
- Routing configuration record (JSON or structured format)
- Validated module dispatch target

## How to apply

Scan the input file headers and metadata fields (file format identifier, instrument type descriptor, and chromatographic/mobility dimension markers) to identify the presence of an ion mobility dimension. Compare detected instrument signatures and dimensional structure against known IMS instrument profiles (e.g., TIMS, DTIMS, TWIMS). If an ion mobility time or drift time field is found in the metadata or alongside m/z and retention time axes, classify the input as IMS. Generate a routing configuration record (JSON or structured format) mapping the IMS-classified input to the mzmine IMS analysis module. Validate the routing assignment by confirming that the target IMS module entry point is resolvable in the current mzmine instance.

## Related tools

- **mzmine** (Primary MS data processing platform providing IMS module and routing dispatch infrastructure) — https://github.com/mzmine/mzmine
- **JDK 25** (Java runtime environment for mzmine execution and metadata parsing)
- **JavaFX 24** (UI framework for mzmine visualization of detected data modality and routing results)

## Evaluation signals

- Detected modality label matches ground truth instrument type (e.g., IMS classification confirmed by TIMS/DTIMS instrument ID in header).
- Routing configuration is valid JSON/structured format and contains resolvable mzmine module entry point.
- Routed input successfully opens and processes in the target IMS module without metadata or dimensionality errors.
- Ion mobility dimension (drift time or mobility coefficient) is extractable and non-null after routing.
- Validation check confirms target module entry point exists in current mzmine instance (no 'module not found' exception).

## Limitations

- Detection accuracy depends on completeness and consistency of file header metadata; incomplete or non-standard headers may cause misclassification.
- Distinction between IMS and fast chromatography dimensions may be ambiguous if file format does not explicitly tag the mobility axis.
- mzmine support for IMS requires the IMS module to be installed; routing will fail if module is unavailable.
- No changelog is available in the repository to track changes in IMS metadata parsing or module interface over versions.

## Evidence

- [other] Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality.: "Scan input file headers and metadata (file format, instrument type fields) to identify data acquisition modality"
- [other] Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions.: "Classify input as LC, GC, IMS, or MS imaging based on detected instrument signature and chromatographic/mobility dimensions"
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
- [readme] mzmine aims to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow: "complete set of modules covering the entire MS data analysis workflow"
- [other] Validate routing assignments against known mzmine module entry points to ensure each route is resolvable.: "Validate routing assignments against known mzmine module entry points to ensure each route is resolvable"
