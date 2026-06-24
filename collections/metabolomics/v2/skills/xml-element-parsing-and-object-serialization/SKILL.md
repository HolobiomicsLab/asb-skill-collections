---
name: xml-element-parsing-and-object-serialization
description: Use when you have spectrum or chromatogram data stored as XML strings
  (e.g., in a SQLite database indexed by spectrum ID) and need to access individual
  spectra by ID or iterate through them sequentially while working with a library
  like pymzML that expects Spectrum or Chromatogram objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
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

# xml-element-parsing-and-object-serialization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse XML element strings retrieved from a data source (e.g., a database) and deserialize them into typed spectrum or chromatogram objects for downstream analysis. This skill bridges storage formats and in-memory object models in mass spectrometry data workflows.

## When to use

You have spectrum or chromatogram data stored as XML strings (e.g., in a SQLite database indexed by spectrum ID) and need to access individual spectra by ID or iterate through them sequentially while working with a library like pymzML that expects Spectrum or Chromatogram objects.

## When NOT to use

- Input is already a deserialized Spectrum or Chromatogram object in memory.
- XML data is embedded in a standard mzML file with built-in indexing; use pymzML.run.Reader directly instead.
- Performance-critical access patterns require avoiding repeated XML parsing; consider caching deserialized objects.

## Inputs

- XML string representation of a spectrum or chromatogram
- Spectrum or chromatogram ID (integer or string key)
- Database handle or file object containing XML strings indexed by ID

## Outputs

- pymzML Spectrum object
- pymzML Chromatogram object
- xml.etree.ElementTree Element

## How to apply

Use xml.etree.ElementTree.XML to parse an XML string retrieved from storage into an ElementTree Element object. Pass the Element to the spectrum/chromatogram parser provided by your analysis library (e.g., pymzML.spec.Spectrum) to instantiate the typed object. For random-access patterns, implement a __getitem__ method that retrieves the XML string by ID, parses it, and returns the deserialized object. For sequential iteration, implement a read method that yields XML strings in order, allowing the iteration protocol to call the parser on each. This approach decouples storage (flat XML strings) from the in-memory representation (structured objects with methods and attributes).

## Related tools

- **pymzML** (Provides Spectrum and Chromatogram classes to instantiate from parsed XML; FileInterface allows registration of custom file handlers that implement __getitem__ and read methods for random-access and sequential retrieval.) — https://github.com/pymzml/pymzML
- **xml.etree.ElementTree** (Parses XML strings into Element trees that can be passed to pymzML spectrum constructors.)
- **sqlite3** (Retrieves XML strings from a relational database by spectrum ID.)

## Examples

```
import xml.etree.ElementTree as et; import sqlite3; conn = sqlite3.connect('test.db'); cursor = conn.cursor(); cursor.execute('SELECT xml FROM spectra WHERE id=5'); xml_str = cursor.fetchone()[0]; elem = et.XML(xml_str); spectrum = pymzml.spec.Spectrum(xmlElement=elem)
```

## Evaluation signals

- Deserialized object is an instance of pymzML.spec.Spectrum or pymzML.spec.Chromatogram with accessible attributes (ms_level, ID, mz, intensity arrays).
- Random-access via db[unique_id] returns a valid Spectrum object without raising KeyError or parsing errors.
- Sequential iteration via iter() over the file handler returns all spectra in database order without duplicates or missing IDs.
- XML Element parse time and object instantiation time remain sub-second for typical mzML spectrum XML (~1–10 KB).
- Round-trip consistency: spectrum.ID matches the query key; spectrum arrays (mz, intensity) match the original mzML values within floating-point tolerance.

## Limitations

- XML parsing is performed on every access; caching is not built in, so repeated access to the same spectrum ID will re-parse the XML.
- Performance scales with XML document size; large spectra with many m/z–intensity pairs may incur noticeable parse overhead.
- Custom regex patterns for non-standard spectrum ID formats (e.g., 'scan=1' vs. integers) must be configured separately in the pymzML Reader; this skill assumes IDs are extractable from database keys.
- Memory usage grows linearly with the number of deserialized objects held in memory simultaneously.

## Evidence

- [other] __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing: "__getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects"
- [other] read to sequentially return XML element strings by current_spectrum_id: "read to sequentially return XML element strings by current_spectrum_id"
- [other] Implement custom file wrapper class that needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [readme] Easy access to mass spectrometry (MS) data that allows the rapid development of tools: "easy access to mass spectrometry (MS) data that allows the rapid development of tools"
- [readme] a very fast parser for mzML data, the standard mass spectrometry data format: "a very fast parser for mzML data, the standard mass spectrometry data format"
