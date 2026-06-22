---
name: custom-file-handler-class-design-for-indexed-access
description: Use when your input is a large mzML or text file that would benefit from compression without sacrificing random-access performance, and you need to retrieve specific logical blocks (e.g., a chapter, spectrum, or database record) by key without decompressing the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ElementTree
  - pymzML
  - ElementTree (xml.etree.ElementTree)
  - sqlite3
  - Black (psf/black)
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
---

# custom-file-handler-class-design-for-indexed-access

## Summary

Design and integrate a custom file handler class that implements random and sequential access to blockwise-indexed data structures (e.g., compressed gzip archives with chapter-level or spectrum-level indexing). This skill enables rapid access to large mzML files by mapping logical blocks to byte offsets in compressed storage.

## When to use

Your input is a large mzML or text file that would benefit from compression without sacrificing random-access performance, and you need to retrieve specific logical blocks (e.g., a chapter, spectrum, or database record) by key without decompressing the entire file. This is especially valuable when file sizes approach or exceed the original uncompressed RAW format and sequential iteration is too slow.

## When NOT to use

- Input file is already a standard format with native random-access support (e.g., HDF5, NetCDF, or uncompressed mzML already integrated into pymzML).
- Access patterns are entirely sequential with no need for random lookup; standard gzip or block compression is sufficient.
- Blockwise boundaries are undefined or highly irregular, making index maintenance error-prone or memory-intensive.

## Inputs

- Large text or XML file (e.g., mzML, or narrative text like Moby Dick)
- Block definitions or delimiters (e.g., chapter boundaries, spectrum boundaries, database record IDs)
- Optional pre-existing index file mapping keys to byte offsets

## Outputs

- Indexed gzip (.gz) file with embedded or external index structure
- Custom file handler class instance supporting __getitem__() and read() interfaces
- Index mapping (dictionary or list) of key → byte offset pairs

## How to apply

First, parse your input file blockwise—each logical unit (chapter, spectrum, XML element) is written in a single operation using a Generalized Seekable Gzip Writer (GSGW) pattern, with each block indexed by an integer or string identifier and a corresponding byte offset recorded in an index structure. Second, create a custom wrapper class that implements two core methods: __getitem__(key) for random access via bracket notation and read() for sequential iteration. Third, maintain an index mapping (dictionary or list) that stores the byte offset for each key. Fourth, integrate the custom handler into pymzML's FileInterface._open() method by adding a conditional branch (elif statement) that detects the file type (e.g., file extension or magic bytes) and instantiates your wrapper instead of the default handler. Finally, use a Generalized Seekable Gzip Reader (GSGR) class or equivalent to seek to the correct byte offset in the compressed file and decompress only the requested block on demand.

## Related tools

- **pymzML** (Provides FileInterface abstraction and integration point (FileInterface._open() method) for plugging in custom file handlers; handles mzML parsing and spectrum iteration.) — https://github.com/pymzml/pymzML
- **ElementTree (xml.etree.ElementTree)** (Parses and represents XML structure of mzML blocks within the handler class.)
- **sqlite3** (Optional backend for storing block metadata and index mappings as an alternative to in-memory dictionaries.)
- **Black (psf/black)** (Code formatter for maintaining consistent style in the custom handler implementation.) — https://github.com/psf/black

## Examples

```
from pymzml import spec
handler = spec.MzMLIndexedGzipHandler('moby_dick_by_chapter.mzml.gz')
chapter_3 = handler[3]
for block in handler.read():
    print(block.get('id'))
```

## Evaluation signals

- Random access via bracket notation (handler[key]) returns the correct decompressed block matching the input key without decompressing adjacent blocks.
- Sequential iteration via read() yields all blocks in order without data loss, corruption, or skipped entries.
- Index structure is accurate: byte offsets in the index map correspond to the actual start positions of each block within the compressed file.
- File sizes after compression reach parity with the original RAW format (verify via file size comparison).
- Round-trip validation: decompress a random sample of blocks from the indexed gzip file, parse them as XML (if mzML), and confirm schema correctness and data integrity.

## Limitations

- Index maintenance requires careful synchronization with the compressed file; corruption of the index file will break random access.
- Initial blockwise parsing and index creation is I/O-intensive; latency may be significant for very large files on slow storage.
- Custom handler implementation must correctly detect file type and instantiate the appropriate wrapper; integration into FileInterface requires careful testing to avoid conflicts with existing handlers.
- Memory overhead for storing the full index in RAM may be prohibitive for extremely large files with millions of blocks; consider database-backed or lazy-loaded index strategies.
- Not suitable for file formats where block boundaries are data-dependent or context-sensitive (e.g., files requiring lookahead to detect block ends).

## Evidence

- [other] GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then finalized with write_index() to create an indexed gzip file.: "GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers"
- [other] Create a custom wrapper class implementing __getitem__() for random access by key and read() for sequential iteration over compressed blocks.: "Create a custom wrapper class implementing __getitem__() for random access by key and read() for sequential iteration over compressed blocks"
- [other] Integrate the custom handler into pymzML's FileInterface._open() method by adding an elif statement to detect the file type and instantiate the wrapper.: "Integrate the custom handler into pymzML's FileInterface._open() method by adding an elif statement to detect the file type and instantiate the wrapper"
- [readme] indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
