---
name: format-agnostic-data-ingestion
description: Use when when you have mass spectrometry data in multiple formats (mzML, mzXML) that must be fed into a compression, analysis, or transformation pipeline that operates on a single canonical spectral data model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mspack
  - msconvert
  - tinyxml2
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1093/bioinformatics/btab636/6363791
  title: mspack
evidence_spans:
- mspack is a C++ program for lossless and lossy mass spectrometry data compression
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspack_cq
    doi: 10.1093/bioinformatics/btab636/6363791
    title: mspack
  dedup_kept_from: coll_mspack_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab636/6363791
  all_source_dois:
  - 10.1093/bioinformatics/btab636/6363791
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# format-agnostic-data-ingestion

## Summary

Implement adapter layers that map heterogeneous mass spectrometry data formats (mzML, mzXML) to a unified, format-agnostic internal representation, enabling downstream processing pipelines to operate on raw spectral records without format-specific branching logic.

## When to use

When you have mass spectrometry data in multiple formats (mzML, mzXML) that must be fed into a compression, analysis, or transformation pipeline that operates on a single canonical spectral data model. Use this skill to eliminate format-specific conditional logic and ensure consistent ingestion of mz/intensity arrays across file types.

## When NOT to use

- Input spectra are already compressed (e.g., with zlib or msnumpress); convert them first using msconvert before adapter ingestion.
- mz values are not monotonically increasing and ion mobility (third dimension) is present; the current implementation cannot handle unordered mz arrays.
- Input is a pre-parsed in-memory data structure (e.g., a Python object or NumPy array); no adapter layer is needed.

## Inputs

- mzML file (raw mass spectrometry spectral data in mzML XML format)
- mzXML file (raw mass spectrometry spectral data in mzXML XML format)
- Format-agnostic API specification (C++ header defining internal spectral record structure)

## Outputs

- Parsed spectral record stream conforming to the format-agnostic internal representation
- Mapped mz/intensity arrays ready for downstream compression or analysis

## How to apply

First, review the format-agnostic API contract (defined in mspack/include/mspack.h) to understand the spectral data structure that the downstream pipeline expects (mz values, intensity values, and associated metadata). Second, examine the mspack example implementations for mzXML and mzML format handlers to identify the reader/parser patterns for each format. Third, implement or instantiate adapter code that maps the XML spectral records from either format into the canonical internal representation, ensuring both raw (uncompressed) mz and intensity arrays are extracted. Fourth, validate by parsing spectra from both formats through the adapter and confirming that data is successfully passed to the compression or processing stage without data loss, format errors, or type mismatches. Pay special attention to the ordering contract: mspack currently requires mz values to be monotonically increasing.

## Related tools

- **mspack** (C++ compression framework providing the format-agnostic API contract and example mzXML/mzML handlers that serve as reference implementations for the adapter layer) — https://github.com/fhanau/mspack
- **msconvert** (Pre-processing tool to decompress mzML/mzXML files that have been compressed with zlib or msnumpress before they can be ingested by the adapter)
- **tinyxml2** (XML parsing library used by mspack to deserialize mzML/mzXML spectral records)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz
```

## Evaluation signals

- Successfully parse representative mzML and mzXML test files without XML deserialization errors or format exceptions.
- Verify that spectral metadata (scan ID, retention time, precursor m/z) and raw mz/intensity arrays from both formats map to identical internal representation values when given the same underlying spectrum.
- Confirm that all spectra pass through the adapter layer to the downstream compression/processing stage without data loss (e.g., by comparing record counts and checksums pre- and post-adaptation).
- Validate that mz arrays extracted by the adapter are monotonically increasing; reject spectra or warn if this invariant is violated.
- Check that decoded output files (after compression and decompression cycles) retain functional equivalence despite whitespace normalization and SHA1 recalculation by the XML handler.

## Limitations

- Current implementation requires mz values to be monotonically increasing; unordered mz arrays (e.g., when ion mobility is present as a third dimension) will fail or produce incorrect results.
- The adapter can only ingest raw (uncompressed) mz and intensity arrays; spectra compressed with zlib or msnumpress must be decompressed first using msconvert.
- mzXML support is limited because the format has been superseded by mzML; mzXML is restricted to 32-bit files and does not support the block-based I/O feature.
- XML whitespace is not preserved in decoded output; although this does not cause functional differences for XML-parsed data, byte-for-byte identity with the original file is not guaranteed.

## Evidence

- [intro] Format-agnostic API enables integration with specific mass spectrometry data formats: "mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression"
- [readme] API is the entry point for custom implementations: "The API is defined in ```include/mspack.h```. The mspack binary represents an example implementation to showcase the capabilities of the program. Users are encouraged to use the API for advanced usage"
- [readme] Raw arrays are the ingestion requirement: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert"
- [readme] Monotonic mz ordering is a critical invariant: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility"
- [readme] Format-specific limitations for mzXML: "The mzXML implementation does not support all features as the format has been superseded by mzML. mzXML is limited to 32-bit files and does not support the block-based I/O feature"
