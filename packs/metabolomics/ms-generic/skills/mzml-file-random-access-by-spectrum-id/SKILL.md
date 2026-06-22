---
name: mzml-file-random-access-by-spectrum-id
description: Use when you have a compressed mzML file (mzML.gz or indexed gzip format) and need to extract a single spectrum or a small subset of spectra by their known numeric identifiers, rather than iterating through the entire file sequentially.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# mzml-file-random-access-by-spectrum-id

## Summary

Retrieve a specific mass spectrometry spectrum from a compressed mzML file by its numeric identifier using bracket notation, enabling efficient random access without sequential file parsing. This skill leverages pymzML's indexed gzip support to achieve near-instantaneous lookups in large compressed datasets.

## When to use

You have a compressed mzML file (mzML.gz or indexed gzip format) and need to extract a single spectrum or a small subset of spectra by their known numeric identifiers, rather than iterating through the entire file sequentially. Typical scenarios include targeted spectrum validation, interactive data exploration, or retrieving specific scans for detailed inspection.

## When NOT to use

- Input is uncompressed mzML or other mass spectrometry formats not supported by pymzML's indexed gzip reader (e.g., raw binary .RAW files, netCDF, or HDF5 formats).
- You need to process all spectra in a file—sequential iteration via the Reader's read() method is more efficient than repeated bracket lookups.
- The spectrum ID is unknown or you must search spectra by metadata (retention time, precursor m/z range, polarity) rather than by exact numeric identifier.

## Inputs

- compressed mzML file (mzML.gz with indexed gzip support)
- numeric spectrum identifier (integer)

## Outputs

- Spectrum object (pymzML.spec.Spectrum instance)
- Spectrum attributes: ID, m/z array, intensity array, retention time, precursor m/z

## How to apply

Instantiate pymzML's run.Reader class with the path to a compressed mzML file (e.g., tests/data/BSA1.mzML.gz). Use Python bracket notation with the numeric spectrum ID (e.g., run[2540]) to perform a single random-access lookup. The Reader class transparently leverages indexed gzip format to seek directly to the requested spectrum without parsing intermediate data. Verify the returned object is a valid Spectrum instance by confirming its ID matches the requested identifier and checking that its attributes (m/z, intensity arrays, etc.) are accessible. For batch lookups, repeat the bracket notation call for each desired spectrum ID rather than implementing custom iteration logic.

## Related tools

- **pymzML** (Provides run.Reader class with bracket notation support for random-access spectrum retrieval from compressed mzML files via indexed gzip format.) — https://github.com/pymzml/pymzML
- **Python** (Host language for pymzML; provides ElementTree XML parsing and file I/O primitives underlying spectrum deserialization.)

## Examples

```
from pymzml.run import Reader; run = Reader('tests/data/BSA1.mzML.gz'); spectrum = run[2540]; print(spectrum.ID, spectrum.mz, spectrum.i)
```

## Evaluation signals

- Returned object is a pymzML.spec.Spectrum instance (not None or a string).
- Spectrum.ID matches the requested numeric identifier exactly.
- Spectrum attributes (m/z array, intensity array, retention time) are populated and have consistent non-empty length.
- Random-access lookup completes in sub-second time (orders of magnitude faster than sequential file scan), confirming indexed gzip seek capability.
- Multiple bracket lookups on the same Reader instance yield consistent Spectrum objects for the same spectrum ID.

## Limitations

- Random access is only available for mzML files in indexed gzip format (or natively indexed formats); uncompressed mzML files may require sequential parsing.
- Numeric spectrum identifiers must be known in advance; the bracket notation does not support fuzzy or pattern-based lookups by retention time, m/z, or scan metadata.
- Performance benefit is realized only when accessing a small fraction of spectra; accessing most or all spectra negates the random-access advantage.
- The underlying mzML file must be properly indexed; corrupted or incomplete index structures may cause Reader instantiation or lookup failures.

## Evidence

- [other] pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation: "pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation, enabling retrieval of spectrum 2540 from BSA1.mzML.gz via run[2540]."
- [readme] Module to parse mzML data in Python with ability to write and read indexed gzip files: "Module to parse mzML data in Python based on cElementTree"
- [readme] indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [readme] access the chapters conveniently by the python bracket notation: "access the chapters conveniently by the python bracket notation ([])"
- [readme] pymzML is an extension to Python that offers random access in compressed files: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass"
