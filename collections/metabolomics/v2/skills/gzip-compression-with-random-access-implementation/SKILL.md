---
name: gzip-compression-with-random-access-implementation
description: Use when you have a large text or structured file (mzML, XML, plain text)
  that you want to compress while retaining the ability to retrieve specific logical
  blocks (chapters, spectra, records) by identifier without decompressing the entire
  file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - ElementTree
  - pymzML
  - Python
  - sqlite3
  - black
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import xml.etree.ElementTree as et
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

# gzip-compression-with-random-access-implementation

## Summary

Implement a Generalized Seekable Gzip Writer (GSGW) pattern to create indexed gzip archives that support both random access by key and sequential iteration, enabling compressed storage of blockwise-parsed data (e.g., mzML spectra or book chapters) with byte-offset indexing.

## When to use

You have a large text or structured file (mzML, XML, plain text) that you want to compress while retaining the ability to retrieve specific logical blocks (chapters, spectra, records) by identifier without decompressing the entire file. Random access latency and file size are both constraints.

## When NOT to use

- Input file is small enough to fit entirely in memory or disk is not a constraint; standard gzip or uncompressed storage is sufficient.
- Blocks are not naturally aligned or logically independent (e.g., streaming time-series data with no clear boundaries); GSGW requires discrete, self-contained blocks.
- Sequential-only access is acceptable; the overhead of indexing and random-access support is not justified.

## Inputs

- Plain text file or XML file (e.g., mzML, book text) with logical block structure
- Block identifiers (integer or string keys mapping to chapters, spectra IDs, or record numbers)
- File path string for output indexed gzip archive

## Outputs

- Indexed gzip file (.gz with embedded key-to-offset index)
- Custom file handler class implementing __getitem__() and read() methods
- Key-offset mapping (internal to archive or exported as metadata)

## How to apply

Parse your source file into logical blocks (e.g., chapters, spectra, database rows), each identified by an integer or string key. For each block, call add_data(block_content) on a GSGW instance, which writes it to gzip format and records its byte offset in an internal index. After all blocks are written, call write_index() to serialize the key-to-offset mapping into the archive header. Wrap the indexed gzip reader in a custom class that implements __getitem__(key) for random access (seeks to the offset, decompresses one block) and read() for sequential iteration. Integrate this wrapper into pymzML's FileInterface._open() by adding an elif branch to detect the indexed gzip file extension and instantiate your handler. Validate by confirming that bracket notation (e.g., handler['chapter_5']) retrieves the correct block and that sequential read() calls iterate through all blocks without data loss.

## Related tools

- **pymzML** (File interface abstraction layer into which the custom GSGW handler is integrated via FileInterface._open(); also provides the Spectrum and Run classes for mzML block representation) — https://github.com/pymzml/pymzML
- **Python** (Runtime environment; gzip module for compression; ElementTree for XML parsing)
- **ElementTree** (XML parsing of mzML blocks before compression)
- **sqlite3** (Optional: backend for alternative block storage (database rows as blocks instead of file offsets))
- **black** (Code formatter for maintaining consistent style in the custom wrapper class) — https://github.com/psf/black

## Examples

```
from pymzml import FileInterface; handler = FileInterface._open('data.mzML.indexed.gz'); spectrum = handler['scan=1234']; for spec in handler.read(): print(spec.ID)
```

## Evaluation signals

- Random access via bracket notation (e.g., handler['scan_1234']) returns the correct XML element or block content without decompressing the entire file.
- Sequential read() calls iterate through all blocks in order with no data loss or corruption; verify by comparing output hash or element count against the original file.
- Byte offsets in the index are unique and monotonically increasing; verify that each block's stored offset correctly maps to its position in the gzip stream.
- File size of the indexed gzip archive is comparable to or smaller than the original RAW or uncompressed mzML file (order-of-magnitude reduction expected).
- Integration test: pymzML._open() correctly detects the file extension and instantiates the custom handler; queries via bracket notation and iteration both succeed.

## Limitations

- Index is written at the end of the archive, so the entire compressed data must be buffered in memory or streamed to disk during write before indexing can be finalized.
- Blocks must be written sequentially and finalized; random or out-of-order block addition is not supported by the GSGW pattern.
- Index overhead grows linearly with the number of blocks; for millions of small blocks, the index itself may become significant.
- Compatibility is limited to pymzML and custom consumers; standard gzip tools cannot interpret the embedded index.

## Evidence

- [other] GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then finalized with write_index() to create an indexed gzip file.: "GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then"
- [other] Create a custom wrapper class implementing __getitem__() for random access by key and read() for sequential iteration over compressed blocks.: "Create a custom wrapper class implementing __getitem__() for random access by key and read() for sequential iteration over compressed blocks"
- [readme] pymzML is an extension to Python that offers random access in compressed files: "pymzML is an extension to Python that offers random access in compressed files"
- [readme] indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler: "to add another elif statement which decides which handler to use"
