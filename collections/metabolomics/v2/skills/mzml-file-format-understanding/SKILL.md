---
name: mzml-file-format-understanding
description: Use when you have mass spectrometry raw data in mzML format (including
  compressed variants like mzML.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pymzML
  - ElementTree
  - regex
  - numpy
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml_cq
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty046
  all_source_dois:
  - 10.1093/bioinformatics/bty046
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-file-format-understanding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Understanding the structure and access patterns of mzML files, a standard mass spectrometry data format, to enable programmatic parsing and random-access spectrum retrieval. This skill encompasses both standard indexed mzML files and custom index schemes, supporting both sequential and bracket-notation lookups.

## When to use

You have mass spectrometry raw data in mzML format (including compressed variants like mzML.gz or indexed gzip) and need to retrieve spectra by identifier, either using standard index structures or custom parsing rules when mzML files contain non-standard custom index identifiers or database backends.

## When NOT to use

- Input is in a non-mzML mass spectrometry format (e.g., mzXML, mzData, raw vendor formats) — use format-specific parsers instead.
- You need lossless retention of vendor-specific metadata not represented in the mzML standard — mzML may have lossy conversions.
- You require on-the-fly spectrum manipulation or deconvolution before access — use optional dependencies like ms_deisotope for post-retrieval processing.

## Inputs

- mzML file path (standard, gzip-compressed, or indexed gzip)
- custom index_regex pattern with named groups 'ID' and 'offset' (optional)
- spectrum identifier string or integer (for bracket-notation access)

## Outputs

- Spectrum object with parsed metadata and peak data
- Sequential iterator over spectra (via read() method)
- Random-access spectrum retrieval via __getitem__

## How to apply

First, determine whether the mzML file uses standard indexing or requires a custom index_regex pattern with named groups ('ID' and 'offset') to parse custom identifier schemes. If using pymzML.run.Reader, pass the file path and optional custom index_regex parameter during initialization. For standard mzML files, the parser automatically builds an in-memory index during initialization by parsing the XML structure and extracting spectrum offsets. For custom formats (e.g., database-backed spectra), implement a wrapper class with read() and __getitem__() methods that conform to the Reader interface. Access spectra using either sequential iteration (via read()) or random access with bracket notation run[spectrum_id]. Verify the returned object is a valid Spectrum instance by inspecting its ID and XML element attributes. The parser handles compressed formats transparently, enabling file sizes comparable to original RAW format through indexed gzip.

## Related tools

- **pymzML** (Primary parser for mzML files; implements Reader class with indexed access, custom regex support, and support for compressed formats (mzML, mzML.gz, indexed gzip)) — https://github.com/pymzml/pymzML
- **ElementTree** (XML parsing backend used by pymzML to parse mzML document structure and extract spectrum elements)
- **regex** (Required dependency for custom index_regex pattern matching in non-standard mzML index formats)
- **numpy** (Required dependency for efficient spectrum peak data manipulation and numerical operations)

## Examples

```
from pymzML import run; reader = run.Reader('sample.mzML', index_regex=r'(?P<ID>custom_\d+)_offset_(?P<offset>\d+)'); spectrum = reader[1]; print(spectrum.ID)
```

## Evaluation signals

- Returned Spectrum object has valid ID attribute matching the queried identifier
- Spectrum object has accessible XML element representation with standardized mzML tags
- Random access via run[custom_id] returns identical spectrum to sequential iteration lookup
- File offsets extracted by custom index_regex correctly resolve to spectrum data in the binary stream
- Sequential read() iteration yields all spectra without duplication or gaps in identifier coverage

## Limitations

- Custom index_regex requires named groups 'ID' and 'offset' to be explicitly defined — malformed patterns will fail silently or raise parsing errors.
- Index is built into memory during initialization; very large mzML files (>10 GB uncompressed) may require significant RAM or streaming-based access patterns not covered by standard Reader.
- The skill assumes mzML is well-formed and compliant with the standard; corrupted or non-compliant files may not parse correctly.
- Sequential iteration via read() returns whole spectrum XML strings; peak data extraction requires additional deserialization steps not covered by this skill.

## Evidence

- [intro] pymzML enables parsing of mzML data and supports multiple file formats including mzML, mzML.gz, and indexed gzip files with random access capability: "Module to parse mzML data in Python... ability to write and read indexed gzip files"
- [other] The Reader class accepts an index_regex parameter containing named groups for custom identifier parsing: "pymzML.run.Reader accepts an index_regex parameter containing named groups 'ID' and 'offset' to parse custom index formats"
- [intro] Indexed gzip enables file size reduction comparable to vendor RAW formats: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] Custom file handlers require __getitem__ and read implementations for random and sequential access: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [readme] pymzML is a Python extension for fast mzML parsing and spectrum manipulation: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass"
