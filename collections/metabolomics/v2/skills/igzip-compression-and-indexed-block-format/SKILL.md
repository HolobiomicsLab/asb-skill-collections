---
name: igzip-compression-and-indexed-block-format
description: Use when you have mzML mass spectrometry files that need both compression
  and rapid random access by spectrum ID (e.g., direct retrieval of spectrum 2540
  without sequential scanning).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml
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

# igzip-compression-and-indexed-block-format

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill structures mzML mass spectrometry data into independently seekable compressed blocks using indexed gzip (igzip) format, enabling random access to specific spectra without decompressing the entire file. The technique reduces file sizes to RAW format levels while preserving rapid seek capability across large datasets.

## When to use

Apply this skill when you have mzML mass spectrometry files that need both compression and rapid random access by spectrum ID (e.g., direct retrieval of spectrum 2540 without sequential scanning). Use it specifically when file size reduction is critical but you cannot afford the latency of full-file decompression or sequential iteration through thousands of spectra.

## When NOT to use

- Input is already a fully compressed mzML file without internal structure that needs preservation — use standard gzip instead.
- Sequential access patterns dominate the use case and random seeking is not required — overhead of index construction and maintenance is not justified.
- Spectrum data is already stored in a columnar format (HDF5, Parquet) with native random access — igzip indexing adds no benefit.

## Inputs

- mzML or mzML.gz mass spectrometry file
- SQLite database with two columns: spectrum ID (integer) and spectrum XML content (text)
- Uncompressed or pre-parsed spectrum text blocks

## Outputs

- Indexed .gz file with chapter/spectrum-level offset mappings in header
- SQLite database table with spectrum ID and XML text columns
- Wrapper class instance compatible with pymzML FileInterface

## How to apply

Create a wrapper class (e.g., GSGW) that implements __getitem__(key) for random access and read(size=-1) for sequential iteration over spectra stored in a SQLite database. Store each spectrum's text in a table with two columns: an ID column (spectrum number) and an XML TEXT column (spectrum content as serialized string). Compress each spectrum block independently using igzip-compatible compression, then construct an indexed .gz file header containing a mapping of spectrum IDs to their byte offsets in the file, terminated by a zero byte. Register the wrapper in pymzML's FileInterface._open() method via an elif statement that detects the .db file extension and instantiates the wrapper. Validate by retrieving specific spectra via db[spectrum_id] (random access) and iterating through the wrapper instance (sequential access) to confirm both access modes work correctly.

## Related tools

- **pymzML** (Framework that accepts wrapper classes via FileInterface._open() to parse indexed gzip mzML files and provides Reader API for spectrum access) — https://github.com/pymzml/pymzML
- **sqlite3** (Database layer for storing spectrum ID-to-XML mappings and enabling efficient random access by spectrum number)
- **xml.etree.ElementTree** (XML parsing library for deserializing spectrum content stored as text in the database into ElementTree objects)
- **Python** (Language runtime for implementing wrapper class and integration with pymzML) — https://www.python.org

## Examples

```
db = sqlite3.connect('spectra.db'); wrapper = GSGW(db); spectrum_2540 = wrapper[2540]; for spec in wrapper: print(spec['ms level'])
```

## Evaluation signals

- Random access test: retrieve spectrum at arbitrary ID (e.g., db[2540]) in constant time without sequentially reading prior spectra.
- Sequential iteration test: iterate through wrapper instance via for loop and confirm all spectra are yielded in ascending ID order.
- File header structure test: inspect the .gz file header bytes to verify presence of igzip ID bytes, version field, index length, offset length, and chapter-to-offset mappings terminated by zero byte.
- Compression ratio test: confirm final .gz file size is ≤ original mzML file size, validating that independent block compression achieves expected reduction.
- Seek latency test: measure time to retrieve spectrum by ID (should be O(1) or O(log n)) versus time to retrieve via sequential read (O(n)).

## Limitations

- Index construction overhead: building the SQLite database and igzip header requires parsing and storing all spectra upfront; incremental addition of new spectra requires reindexing.
- Custom regex support: when reading mzML files with non-integer indices or special scan identifiers (e.g., 'scan=1'), a custom regex pattern must be supplied to the pymzML Reader during initialization; the wrapper does not automatically infer format.
- Database lock contention: SQLite is optimized for single-writer access; concurrent spectrum additions or modifications from multiple processes may experience lock timeouts.
- Header format rigidity: the igzip format does not support modification of spectrum order or renumbering after file creation without reconstructing the entire index.

## Evidence

- [readme] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [readme] pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not: "pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not"
- [other] The GSGW class writes indexed gzip files where each chapter is indexed by chapter number and stored in independently accessible compressed blocks. The igzip file header contains ID bytes, version, index length, and offset length fields, followed by chapter-to-offset mappings terminated by a zero byte: "The GSGW class writes indexed gzip files where each chapter is indexed by chapter number and stored in independently accessible compressed blocks. The igzip file header contains ID bytes, version,"
- [readme] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [readme] When reading mzML files with indices wich is not an integer or contains 'scan=1' or similar, you can set a custom regex to parse the index when initializing the reader: "When reading mzML files with indices wich is not an integer or contains 'scan=1' or similar, you can set a custom regex to parse the index when initializing the reader"
