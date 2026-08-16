---
name: api-adapter-layer-design
description: Use when when you have multiple mass spectrometry data formats (mzML,
  mzXML, or others) that must be ingested into a single format-agnostic processing
  engine (e.g., mspack compression), and you need to avoid replicating the core logic
  for each format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - mspack
  - tinyxml2
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# api-adapter-layer-design

## Summary

Design and implement an adapter layer between a format-agnostic API and specific data format handlers (e.g., mzML/mzXML) to enable seamless integration of heterogeneous mass spectrometry data into a unified processing pipeline. This skill ensures that format-specific parsing logic is decoupled from the core compression or analysis engine.

## When to use

When you have multiple mass spectrometry data formats (mzML, mzXML, or others) that must be ingested into a single format-agnostic processing engine (e.g., mspack compression), and you need to avoid replicating the core logic for each format. Specifically, when the formats share a common logical data model (e.g., spectral arrays with m/z and intensity values) but differ in serialization, XML structure, or encoding.

## When NOT to use

- Input data is already in the internal canonical format or already decoded into memory structures — adapter layer is redundant.
- Only a single data format needs to be supported — a simpler, format-specific reader/writer may be more maintainable.
- Format specifications are incompatible or map to fundamentally different data models (e.g., one stores aggregated spectra, the other stores individual scan events) — adapter layer cannot bridge the semantic gap without custom preprocessing.

## Inputs

- mzML file (XML-based mass spectrometry data with optional base64-encoded or compressed m/z and intensity arrays)
- mzXML file (legacy XML-based mass spectrometry data format)
- format-agnostic API specification (header file or interface definition documenting spectral data contract)
- example format handlers or reference implementations

## Outputs

- adapter layer implementation (C++ classes or functions mapping format-specific records to canonical spectral representation)
- validated spectral objects ready for downstream compression or analysis
- logs or reports confirming successful parsing and data integrity across both formats

## How to apply

First, review the format-agnostic API contract (e.g., mspack's include/mspack.h) to understand the spectral data structure, required fields, and method signatures that the core engine expects. Second, examine example implementations for each source format (mzXML and mzML handlers in mspack) to identify reader/writer patterns and extract common operations: XML parsing, array decoding, metadata mapping, and validation logic. Third, implement the adapter layer as a translation bridge that maps format-specific spectral records to the engine's canonical internal representation, handling format-specific quirks (e.g., base64 encoding, zlib compression in arrays, whitespace normalization). Finally, validate that spectra from both formats can be successfully parsed, serialized to the internal representation, and passed to the downstream compression stage without data loss, format errors, or missed metadata.

## Related tools

- **mspack** (Core format-agnostic compression engine for which the adapter layer translates mzML/mzXML spectral data into the internal representation) — https://github.com/fhanau/mspack
- **tinyxml2** (XML parsing library used by mspack to deserialize mzML and mzXML element hierarchies)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz
```

## Evaluation signals

- Both mzML and mzXML files are successfully parsed without errors or exceptions when passed through the adapter layer.
- Spectral m/z and intensity arrays are correctly extracted, decoded (if base64 or compressed), and match the original values when compared against the input file.
- Adapter layer output passes downstream validation: spectra can be compressed and decompressed with no data loss (for lossless mode).
- Metadata fields (scan time, precursor m/z, charge state, etc.) are preserved and correctly mapped between formats.
- No orphaned or missing spectral records; the number of output spectra equals the number in the input file.

## Limitations

- Whitespace is not preserved in decoded XML files, although this does not cause functional differences because XML is invariant to whitespace addition or removal.
- The implementation depends on m/z values being monotonically increasing; this constraint is violated when a third data point (e.g., ion mobility) is present in addition to m/z and intensity.
- The adapter can only ingest raw (uncompressed) m/z and intensity arrays; if arrays are compressed with zlib or msnumpress, the file must be converted using msconvert before use.
- mzXML implementation does not support all features because the format has been superseded by mzML; mzXML is limited to 32-bit files and does not support block-based I/O.
- SHA1 checksum tags are recalculated when needed during decode, so checksums in the output file may not match the input.

## Evidence

- [other] mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression.: "mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats"
- [readme] The API is defined in include/mspack.h. The mspack binary represents an example implementation to showcase the capabilities of the program.: "The API is defined in ```include/mspack.h```. The mspack binary represents an example implementation"
- [other] Users should examine provided example implementations to identify reader/writer patterns.: "Examine the provided example implementation for mzXML and mzML format handlers to identify reader/writer patterns"
- [readme] Due to the XML library used, whitespace is not preserved in the decoded file, although this does not cause a functional difference.: "whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file"
- [readme] The current implementation depends on the mz values being increasing, which is sometimes not the case if a third data point is present.: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present"
- [readme] The implementation can only use raw mz and intensity arrays; if compressed, the file can be converted using msconvert.: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert"
