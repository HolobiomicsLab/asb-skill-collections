---
name: python-class-design-with-dunder-methods
description: Use when when you need to enable bracket notation (e.g., handler[5]) for random access to blocks within a large compressed or remote data source, or when you want to support both random access and sequential iteration over data without materializing all records upfront.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3209
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - xml.etree.ElementTree
  - pymzML
  - sqlite3
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3 import os from pymzml import spec
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml
schema_version: 0.2.0
---

# python-class-design-with-dunder-methods

## Summary

Design Python classes with dunder methods (__getitem__, __init__, read) to enable random-access and sequential iteration over structured data sources such as indexed gzip files or database-backed file handlers. This pattern is essential for implementing efficient, Pythonic interfaces to large compressed or remote data without loading entire files into memory.

## When to use

When you need to enable bracket notation (e.g., handler[5]) for random access to blocks within a large compressed or remote data source, or when you want to support both random access and sequential iteration over data without materializing all records upfront. Typical triggers: indexed gzip files, database-backed file wrappers, or custom file formats where seek-by-index is more efficient than linear scan.

## When NOT to use

- Input is a small, uncompressed file that fits in memory—use direct load instead.
- Data source does not support seeking (e.g., stream or pipe)—implement linear scan with caching instead.
- Index metadata is missing or unreliable—validate index consistency before implementing random access; fall back to sequential scan if validation fails.

## Inputs

- indexed gzip file (.igz or .mzML.gz with embedded index in header comment field)
- database connection (e.g., SQLite) with spectrum/record table
- file path and index metadata (offsets, record IDs, or scan numbers)

## Outputs

- class instance supporting bracket notation __getitem__ for random access by integer key
- individual decompressed/deserialized records (e.g., spectrum objects, database rows)
- iterator protocol support for sequential read() calls

## How to apply

Define a custom class with __init__ to parse and cache metadata (e.g., index-to-offset mappings from gzip headers or database queries), implement __getitem__(key) to translate an integer or string key into a direct seek and decompression/retrieval operation without scanning prior records, and optionally implement read() to support sequential iteration by tracking state (e.g., current item ID) and incrementing it on each call. Parse the file header or metadata source once during __init__ to extract the index structure; store it as a dictionary mapping indices to byte offsets or database IDs. In __getitem__, use the stored mapping to look up the target offset, seek to that position in the underlying stream, and decompress or deserialize only the requested block. This design amortizes header parsing and enables O(1) random access. Test both random access (e.g., handler[target_id]) and iteration (e.g., for item in handler: ...) to verify correctness.

## Related tools

- **pymzML** (Reference implementation for random-access indexed gzip file handler with __getitem__ and read() methods for mzML spectra; provides pattern for embedding index in gzip header comment and seeking by integer scan ID) — https://github.com/pymzml/pymzML
- **Python** (Language for implementing dunder methods and class protocol)
- **xml.etree.ElementTree** (Optional—for parsing mzML or other XML-structured records after seeking and decompressing)
- **sqlite3** (Optional—for implementing database-backed file wrapper class that wraps __getitem__ over SQL queries)

## Examples

```
run = pymzml.run.Reader('tests/data/BSA1.mzML.gz'); spectrum_with_id_2540 = run[2540]
```

## Evaluation signals

- Bracket notation access returns correct record for arbitrary integer keys (e.g., handler[2540] retrieves spectrum with ID 2540 in O(1) time without scanning prior records).
- Iteration protocol works: for loop over handler produces records in expected sequence and respects read() method state tracking.
- Header/metadata parsing during __init__ completes without errors and reconstructs index dictionary with correct offset mappings (e.g., verify via debug print or assertion on dictionary size and key/value ranges).
- Seek position and decompression are performed only for requested block, not entire file (verify via file I/O profiling or mock stream position tracking).
- Both random access and sequential iteration produce identical record contents when applied to the same data source (consistency check via hash or field-by-field comparison).

## Limitations

- Index metadata must be reliably embedded in file header or separately maintained; if header is corrupted or index is stale, random access will fail or return wrong data.
- Seeking and decompression are not optimized for streaming use cases; for append-only or streaming data, linear scan or different architecture may be better.
- Custom regex patterns may be needed if record identifiers are non-standard (e.g., 'scan=123' instead of integer); pymzML supports this via custom regex parameter, but requires manual configuration.
- File handle state and thread safety are not guaranteed; concurrent access to the same handler instance may cause seek position conflicts unless explicitly synchronized.

## Evidence

- [other] The GSGR class is initialized with a path to an indexed gzip file and supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index, with the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte.: "supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index, with the index-to-offset mapping stored in the gzip header comment field"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format.: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data.: "implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [intro] spectrum_with_id_2540 = run[ 2540 ]: "spectrum_with_id_2540 = run[ 2540 ]"
- [intro] When reading mzML files with indices wich is not an integer or contains 'scan=1' or similar, you can set a custom regex to parse the index when initializing the reader.: "When reading mzML files with indices wich is not an integer or contains 'scan=1' or similar, you can set a custom regex to parse the index when initializing the reader"
