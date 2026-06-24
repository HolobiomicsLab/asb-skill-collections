---
name: mzml-mzxml-spectrum-reading
description: Use when when you have raw mzML or mzXML files containing uncompressed
  m/z and intensity arrays and need to load spectra into a uniform data contract before
  compression, cross-format comparison, or algorithmic processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mspack
  - msconvert
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

# mzml-mzxml-spectrum-reading

## Summary

Parse and validate mzML and mzXML mass spectrometry data files into a standardized in-memory spectral representation using mspack's format-agnostic API. This skill bridges heterogeneous mass spectrometry formats to enable downstream compression, analysis, or transformation workflows.

## When to use

When you have raw mzML or mzXML files containing uncompressed m/z and intensity arrays and need to load spectra into a uniform data contract before compression, cross-format comparison, or algorithmic processing. Specifically applicable when source files contain raw (not zlib- or msnumpress-compressed) array data and m/z values are monotonically increasing.

## When NOT to use

- Input arrays are already compressed with zlib or msnumpress—use msconvert to decompress first
- m/z values are not monotonically increasing (e.g., when ion mobility data introduces a third dimension)
- mzXML files are 32-bit and require block-based I/O, which is not supported by the current mzXML implementation

## Inputs

- mzML file with raw (uncompressed) m/z and intensity arrays
- mzXML file with raw (uncompressed) m/z and intensity arrays
- mspack format-agnostic API specification (mspack.h)

## Outputs

- In-memory spectrum collection conforming to mspack's internal spectral data representation
- Validated spectral metadata (scan ID, retention time, m/z range, intensity range)
- Parse validation report (scan count, data loss check, format error log)

## How to apply

First, review mspack's format-agnostic API interface (mspack.h) to understand the spectral data contract and required fields. Examine the provided mzXML and mzML example implementations to identify the reader/writer patterns and how they map XML elements to the internal compressor data representation. Instantiate the appropriate format handler (mzXML or mzML) and invoke the parser on your input file; the handler will deserialize all spectra and validate the m/z monotonicity constraint. Map each parsed spectrum's m/z and intensity arrays into the compressor's internal representation, verifying that no data is lost during conversion. Finally, pass the standardized spectra to the next workflow stage (typically compression or analysis). Success is confirmed when all spectra parse without format errors and the spectral record count matches the source file.

## Related tools

- **mspack** (Provides the format-agnostic API, example mzXML and mzML readers, and the spectral data contract for unified spectrum representation) — https://github.com/fhanau/mspack
- **msconvert** (Utility to decompress zlib- or msnumpress-encoded arrays in mzML/mzXML files prior to mspack ingestion)
- **tinyxml2** (XML parsing library used by mspack to deserialize mzML and mzXML file structure)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz
```

## Evaluation signals

- All spectra from the source file parse without XML schema or format errors
- Parsed spectrum count equals expected scan count from file metadata
- m/z and intensity arrays are preserved without truncation or data loss during conversion to internal representation
- m/z values in each spectrum are monotonically increasing (or logged error if not)
- Spectral metadata (retention time, scan ID, polarity) are correctly mapped and retrievable from the internal representation

## Limitations

- Whitespace is not preserved during XML parsing; decoded files differ cosmetically but are functionally equivalent
- Implementation requires m/z values to be strictly increasing; files with ion mobility or other third dimensions may fail
- Only raw m/z and intensity arrays are supported; pre-compressed arrays (zlib, msnumpress) must be decompressed externally
- mzXML implementation is incomplete and does not support all mzXML features, 32-bit files, or block-based I/O
- SHA1 checksum tags are recalculated during parsing and may not match original file

## Evidence

- [other] mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression: "mspack provides a format-agnostic API as well as an example implementation for mzXML and mzML"
- [readme] The API is defined in include/mspack.h and users are encouraged to use it for advanced usage: "The API is defined in ```include/mspack.h```. Users are encouraged to use the API for advanced usage"
- [readme] Arrays must be raw and uncompressed; pre-compressed files require conversion: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert"
- [readme] m/z monotonicity is a critical constraint for the implementation: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present"
- [readme] mzXML implementation is limited compared to mzML: "The mzXML implementation does not support all features as the format has been superseded by mzML. mzXML is limited to 32-bit files and does not support the block-based I/O feature"
