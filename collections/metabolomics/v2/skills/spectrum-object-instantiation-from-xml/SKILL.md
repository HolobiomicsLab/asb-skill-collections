---
name: spectrum-object-instantiation-from-xml
description: Use when when you have parsed XML elements from an mzML or mzML.gz file (via ElementTree or a similar XML parser) and need to convert those elements into pymzML Spectrum objects for spectrum-level operations such as random access, spectral comparison, or data extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pymzML
  - Python ElementTree
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

# spectrum-object-instantiation-from-xml

## Summary

Instantiate Spectrum objects from XML element representations of spectra in mzML files, enabling random-access retrieval and manipulation of individual mass spectrometry spectra. This skill is essential for converting raw XML data into in-memory Spectrum instances that support further analysis.

## When to use

When you have parsed XML elements from an mzML or mzML.gz file (via ElementTree or a similar XML parser) and need to convert those elements into pymzML Spectrum objects for spectrum-level operations such as random access, spectral comparison, or data extraction. Particularly relevant when using pymzML's run.Reader interface with bracket notation (e.g., run[spectrum_id]) or when iterating over spectra sequentially.

## When NOT to use

- Input is already a Spectrum object (no instantiation needed)
- Working exclusively with aggregated spectrum statistics or summary-level data that does not require individual spectrum objects
- File format is not mzML or mzML.gz (e.g., raw vendor formats, NetCDF, or other MS data containers not supported by pymzML)

## Inputs

- XML element representing a spectrum from mzML document
- File path to mzML or mzML.gz file
- Spectrum numeric identifier or string identifier

## Outputs

- Spectrum object instance with parsed m/z-intensity data
- Accessible spectrum metadata (ID, scan number, MS level)

## How to apply

Retrieve an XML element corresponding to a spectrum from the mzML document (either via random access using __getitem__ or sequential iteration using a read function). Pass this XML element to the pymzML Spectrum class constructor or factory method to instantiate a Spectrum object. The implementation must handle the mzML XML schema correctly, parsing spectrum attributes such as ID, scan number, and m/z-intensity arrays. Verify the returned object is a valid Spectrum instance by checking that it has the expected ID and contains accessible spectrum data (m/z and intensity values). This approach works for both uncompressed mzML files and compressed mzML.gz files with indexed gzip support.

## Related tools

- **pymzML** (Provides run.Reader interface, Spectrum class constructor, and random-access retrieval via bracket notation (__getitem__) and sequential access via read() for spectrum instantiation from XML) — https://github.com/pymzml/pymzML
- **Python ElementTree** (Parses mzML XML documents and provides XML element objects passed to Spectrum constructor)

## Examples

```
from pymzml.run import Reader; run = Reader('tests/data/BSA1.mzML.gz'); spectrum = run[2540]; print(spectrum.ID, len(spectrum.mz))
```

## Evaluation signals

- Returned object is an instance of pymzML.Spectrum (verify via type checking or isinstance)
- Spectrum ID matches the requested identifier (compare spectrum.ID or spectrum.scan against input ID)
- Spectrum contains non-empty m/z and intensity arrays (len(spectrum.mz) > 0 and len(spectrum.intensity) > 0)
- Spectrum metadata fields (MS level, polarity, scan number) are populated correctly from XML
- Random access via bracket notation returns the same Spectrum object on repeated calls with the same ID

## Limitations

- Spectrum instantiation from XML is dependent on correct mzML schema compliance; malformed or non-standard XML elements may fail to parse
- For very large mzML files, repeated instantiation of Spectrum objects can be memory-intensive; indexed gzip format mitigates this but requires pre-indexed files
- Custom mzML data sources (e.g., databases) require implementation of custom API classes with read() and __getitem__() functions before spectrum instantiation is possible
- The skill assumes the underlying XML element structure conforms to the mzML standard; vendor-specific extensions or deviations may not instantiate correctly

## Evidence

- [other] pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation, enabling retrieval of spectrum 2540 from BSA1.mzML.gz via run[2540].: "pymzML's run.Reader class supports random access to spectra in compressed mzML files using bracket notation, enabling retrieval of spectrum 2540 from BSA1.mzML.gz via run[2540]"
- [other] Verify the returned object is a valid Spectrum instance with the correct ID.: "Verify the returned object is a valid Spectrum instance with the correct ID"
- [readme] Module to parse mzML data in Python based on cElementTree: "Module to parse mzML data in Python based on cElementTree"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format c) a set of functions to compare and/or handle spectra d) random access in compressed files: "a set of functions to compare and/or handle spectra d) random access in compressed files"
- [other] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
