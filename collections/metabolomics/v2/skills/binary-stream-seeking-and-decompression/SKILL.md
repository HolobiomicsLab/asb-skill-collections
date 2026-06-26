---
name: binary-stream-seeking-and-decompression
description: Use when you have a large gzip-compressed file (e.g., mzML.gz) with an
  embedded index structure in the gzip header comment field, and you need to retrieve
  specific blocks (e.g., mass spectra by scan number, chapters by ID) without decompressing
  the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - xml.etree.ElementTree
  - pymzML
  - Python gzip module
  license_tier: open
  provenance_tier: literature
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

# binary-stream-seeking-and-decompression

## Summary

Implement random-access decompression of indexed gzip files by parsing binary metadata embedded in the gzip header comment field to extract index-to-offset mappings, then use those mappings to seek directly to and decompress specific blocks without scanning the entire file. This skill is essential for rapid access to large compressed scientific data formats like mzML without requiring sequential iteration.

## When to use

You have a large gzip-compressed file (e.g., mzML.gz) with an embedded index structure in the gzip header comment field, and you need to retrieve specific blocks (e.g., mass spectra by scan number, chapters by ID) without decompressing the entire file. This is particularly valuable when file sizes approach or exceed RAW format scales and random-access latency is critical for interactive analysis or high-throughput queries.

## When NOT to use

- Input gzip file has no embedded index metadata in the header comment field — use sequential decompression instead.
- File is uncompressed or uses a different compression format without index support (e.g., standard gzip, bzip2, xz) — use standard stream reading.
- Access pattern is purely sequential and latency to first item is not critical — overhead of index parsing and seeking may not justify the complexity.

## Inputs

- indexed gzip-compressed file path (str) with binary index metadata in gzip header comment field
- integer block/item key (int) for random access queries

## Outputs

- decompressed block/item data (bytes or parsed object)
- parsed index-to-offset mapping dictionary (dict[int, int])

## How to apply

Parse the gzip file header to extract the comment field containing binary index metadata structured as ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte. Decode this binary structure into a dictionary mapping integer indices to byte offsets within the compressed stream. Implement a `__getitem__` method that accepts an integer key, queries the index dictionary for the corresponding offset, seeks to that position in the file stream using `seek()`, and decompresses only that block using `gzip.GzipFile` or similar. Optionally implement a `read()` method for sequential iteration by tracking the current item ID and incrementing it on each call. The key rationale is that indexed gzip allows file sizes to match RAW format levels while maintaining rapid seek capability without requiring separate index files.

## Related tools

- **pymzML** (Provides Reader class with built-in support for indexed gzip seeking and random access by integer index without requiring separate index files) — https://github.com/pymzml/pymzML
- **Python gzip module** (Core library for opening, seeking, and decompressing gzip file streams)
- **xml.etree.ElementTree** (Parses mzML XML structure after decompressed blocks are retrieved, demonstrating typical downstream use)

## Examples

```
run = pymzml.run.Reader('tests/data/BSA1.mzML.gz'); spectrum = run[2540]
```

## Evaluation signals

- Index dictionary correctly maps integer keys to byte offsets: verify by checking that seek(offset) followed by decompression yields the expected block content.
- Random-access latency is sub-linear in file size: confirm that retrieval time for block N is independent of blocks 0 to N−1.
- Decompressed block content is identical to sequential decompression: validate by comparing `reader[k]` output to the k-th block in a full sequential decompress.
- Index parsing correctly interprets binary metadata structure: confirm IDXLEN and OFFSETLEN bytes correctly determine how many bytes to read for each index and offset value.
- Sequential iteration via `read()` method yields blocks in order without gaps or duplicates: iterate through all blocks and confirm IDs are monotonic and match index keys.

## Limitations

- Requires index metadata to be pre-embedded in the gzip header comment field at file creation time; cannot add or repair an index in an already-compressed file without re-compression.
- Index size grows linearly with the number of blocks, which may consume significant memory for files with millions of small blocks; trade-off between access speed and memory footprint.
- Relies on correct IDXLEN and OFFSETLEN byte counts; malformed or corrupted metadata in the gzip header will silently produce incorrect offsets and return wrong blocks.
- Custom regex patterns for non-integer or non-standard index identifiers (e.g., 'scan=1' notation) must be specified at Reader initialization; not all mzML index formats are automatically recognized.

## Evidence

- [other] The GSGR class is initialized with a path to an indexed gzip file and supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index, with the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte.: "index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not: "pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [intro] spectrum_with_id_2540 = run[ 2540 ]: "spectrum_with_id_2540 = run[ 2540 ]"
