---
name: indexed-gzip-file-parsing
description: Use when you have compressed mzML.gz files and need to retrieve specific spectra by numeric identifier without decompressing the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# indexed-gzip-file-parsing

## Summary

Parse and randomly access spectra in compressed mzML files using indexed gzip format, which maintains file compression comparable to RAW format while enabling O(1) lookup by spectrum ID. This skill is essential for handling large mass spectrometry datasets where both storage efficiency and random access performance are critical.

## When to use

Use this skill when you have compressed mzML.gz files and need to retrieve specific spectra by numeric identifier without decompressing the entire file. Apply it when disk space is constrained (indexed gzip compression reaches RAW format file sizes) but sequential iteration is not your primary access pattern, or when you need to sample or spot-check specific spectra from large runs.

## When NOT to use

- Input file is uncompressed or unindexed .mzML — use sequential Reader iteration instead
- You need to access all or most spectra in the file — sequential iteration is faster than repeated random seeks
- Spectrum identifier is unknown or must be discovered by scan time or precursor m/z — use regex-based filtering or sequential scan first

## Inputs

- mzML.gz file path (indexed gzip compressed mass spectrometry data)
- numeric spectrum identifier (integer, e.g., 2540)

## Outputs

- Spectrum object (pymzML spec instance with m/z and intensity arrays)
- spectrum metadata (ID, retention time, precursor m/z, fragmentation parameters)

## How to apply

Instantiate pymzML's run.Reader class with the path to a compressed mzML.gz file. Use bracket notation with the numeric spectrum ID (e.g., run[2540]) to perform random-access lookup, which internally uses the indexed gzip layer to seek directly to the spectrum without decompressing preceding data. Verify the returned object is a valid Spectrum instance with the correct ID before processing. The indexed gzip format must have been created during initial file conversion; if unavailable, fall back to sequential iteration or full decompression. The Reader class automatically detects and handles indexed gzip files through its filehandler integration.

## Related tools

- **pymzML** (Provides run.Reader class with __getitem__ bracket notation interface for random-access spectrum retrieval from indexed gzip mzML files) — https://github.com/pymzml/pymzML
- **Python** (Runtime environment for pymzML Reader instantiation and bracket notation spectrum access)

## Examples

```
from pymzml.run import Reader; run = Reader('tests/data/BSA1.mzML.gz'); spectrum = run[2540]; print(spectrum.ID, len(spectrum.mz))
```

## Evaluation signals

- Returned Spectrum object has correct numeric ID matching the lookup key (run[2540].ID == 2540)
- Spectrum object is a valid pymzML Spectrum instance with m/z and intensity array attributes populated
- Lookup completes in constant time independent of file size or spectrum position (no linear decompression overhead)
- File size of indexed gzip remains comparable to original RAW format (typically 10–20% overhead vs. uncompressed mzML)
- Sequential iteration over Reader (for loop) still works, confirming indexed gzip file integrity

## Limitations

- Indexed gzip files must be pre-created during initial file conversion; existing unindexed .mzML.gz files require re-compression
- Random-access lookup performance degrades if the indexed gzip index is corrupted or missing; fallback to sequential iteration is required
- Spectrum ID must be known in advance; no built-in search by retention time, precursor m/z, or scan metadata without sequential preprocessing
- Large files (>10 GB) may incur seek latency on spinning disk storage; performance is optimized for SSD or in-memory index caching

## Evidence

- [intro] pymzML enables parsing of mzML data and supports multiple file formats including mzML, mzML.gz, and indexed gzip files with random access capability: "ability to write and read indexed gzip files"
- [intro] Indexed gzip files allow mzML file sizes to reach levels comparable to the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] Access indexed gzip data using bracket notation: "access the chapters conveniently by the python bracket notation ([])"
- [other] pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation: "pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation, enabling retrieval of spectrum 2540 from BSA1.mzML.gz via run[2540]"
- [other] Implement __getitem__ function for random access in custom file handlers: "we need to implement a class, which needs to implement the __getitem__ function for random access"
