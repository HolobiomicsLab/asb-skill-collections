---
name: mass-spectrometry-format-parsing
description: Use when you have mzML or mzXML mass spectrometry data files and need to extract and validate spectral records (m/z and intensity arrays) for lossless compression, lossy transformation, or format conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mspack
  - tinyxml2
  - msconvert
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

# mass-spectrometry-format-parsing

## Summary

Parse and adapt raw mass spectrometry data files (mzML, mzXML) into a format-agnostic internal representation suitable for downstream compression or analysis. This skill bridges vendor-specific or standards-based XML formats to a unified spectral data contract.

## When to use

You have mzML or mzXML mass spectrometry data files and need to extract and validate spectral records (m/z and intensity arrays) for lossless compression, lossy transformation, or format conversion. Use this skill when source data is in raw (uncompressed) array form and you must preserve or transform the spectral values without data loss during parsing.

## When NOT to use

- Input arrays are already compressed (e.g., with zlib or msnumpress); decompress first using msconvert or equivalent.
- Input contains ion mobility data (third dimension beyond m/z and intensity); current mspack implementation requires only m/z and intensity and may fail on non-increasing m/z values when ion mobility is present.
- mzXML files with block-based I/O or 64-bit data; mzXML support is limited to 32-bit and does not support block-based features.

## Inputs

- mzML file (XML-based mass spectrometry data with raw m/z and intensity arrays)
- mzXML file (XML-based mass spectrometry data with raw m/z and intensity arrays)
- format-agnostic API interface definition (e.g., mspack's include/mspack.h)

## Outputs

- Parsed spectral records in format-agnostic internal representation
- Validated m/z and intensity arrays ready for compression or lossy transformation
- Metadata (scan number, retention time, precursor mass, etc.) mapped to API contract

## How to apply

Load the mzML or mzXML file using the format-specific handler (e.g., mspack's mzXML or mzML reader). Parse the XML structure to extract raw m/z and intensity arrays; verify that m/z values are in increasing order (a requirement for mspack's block-based compression). Map each spectral record to the format-agnostic API's internal data representation (typically a spectral object with metadata, m/z array, and intensity array). Validate that no data loss occurs during mapping by spot-checking array lengths and value ranges. Pass the adapted spectral records to the next stage (e.g., compressor or lossy transformer) only after confirming successful parsing and format compliance.

## Related tools

- **mspack** (Provides format-agnostic API, mzML/mzXML parsers, and example implementations for reading and writing mass spectrometry data files) — https://github.com/fhanau/mspack
- **tinyxml2** (XML parsing library used by mspack to parse mzML and mzXML structures)
- **msconvert** (Utility to convert compressed arrays (zlib, msnumpress) to raw form for mspack compatibility)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz
```

## Evaluation signals

- Parse completes without XML schema errors or missing spectral record elements (m/z array, intensity array, scan metadata).
- Spectral m/z values are in strictly increasing order (or flagged for non-increasing case with ion mobility).
- Array lengths match between input file and parsed output; no truncation or expansion.
- Round-trip validation: compress parsed spectra and decompress; byte-compare decompressed output against original file to confirm bit-identical recovery (for lossless pipeline).
- Metadata (scan ID, retention time, precursor m/z if applicable) correctly mapped and retrievable from internal representation.

## Limitations

- Whitespace is not preserved during XML parsing; decoded files will have normalized whitespace, which is functionally equivalent for XML but not bit-identical.
- SHA1 checksum tags are recalculated; original checksums are not preserved.
- m/z values must be in increasing order; files with out-of-order m/z (common when ion mobility is the third dimension) will fail or produce incorrect results.
- Only raw (uncompressed) m/z and intensity arrays are supported; zlib- or msnumpress-compressed arrays must be decompressed beforehand.
- mzXML support is limited to 32-bit files and does not support block-based I/O features (mzML is the preferred format).

## Evidence

- [intro] mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression.: "mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats"
- [intro] The format-agnostic API and example implementations define the contract for spectral data (m/z and intensity arrays with metadata) that must be satisfied by format-specific parsers.: "Examine the provided example implementation for mzXML and mzML format handlers to identify reader/writer patterns"
- [readme] The current implementation depends on the mz values being increasing and fails on files with non-increasing m/z (typical when ion mobility is present).: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility"
- [readme] mzML and mzXML files require raw (uncompressed) arrays; pre-compressed arrays must be converted using msconvert.: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert"
- [readme] Whitespace is not preserved in the decoded file during XML parsing, though this does not cause functional differences.: "whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace"
