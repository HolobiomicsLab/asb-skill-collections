---
name: xml-parsing-and-element-tree-serialization
description: Use when when spectrum or chromatogram data is stored as serialized XML strings in a database or file system and must be converted into pymzML Spectrum or Chromatogram objects for programmatic access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - ElementTree
  - pymzML
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

# xml-parsing-and-element-tree-serialization

## Summary

Parse XML element strings retrieved from data sources (such as SQLite databases) into structured XML trees using ElementTree, enabling random-access retrieval and deserialization of mass spectrometry spectrum objects. This skill bridges raw XML storage with pymzML's Spectrum and Chromatogram object instantiation.

## When to use

When spectrum or chromatogram data is stored as serialized XML strings in a database or file system and must be converted into pymzML Spectrum or Chromatogram objects for programmatic access. Specifically when implementing a custom file handler class that requires __getitem__ to return parsed spectrum objects rather than raw XML strings.

## When NOT to use

- Input XML is already in memory as an ElementTree object (parse only if string)
- mzML data is stored in standard compressed formats (.mzML.gz, indexed gzip) for which pymzML already has native handlers
- Performance requirements demand streaming without object instantiation; use read() for sequential XML strings instead

## Inputs

- XML string (serialized spectrum or chromatogram element)
- Integer or string key identifier
- SQLite query result row containing spectrum ID and XML element

## Outputs

- xml.etree.ElementTree.Element object
- pymzML Spectrum object
- pymzML Chromatogram object

## How to apply

Import xml.etree.ElementTree to parse XML strings retrieved from a data source (e.g., via SQL query) into Element objects. Pass the parsed Element to pymzML's spec module (e.g., spec.Spectrum or spec.Chromatogram) to deserialize the XML into a spectrum object. Store the deserialized object in a dictionary or return it directly from __getitem__(key). Test that both integer and string keys return valid spectrum objects with expected attributes (mz, intensity, ID). Verify that the read() method returns raw XML strings sequentially while __getitem__ returns fully instantiated spectrum objects.

## Related tools

- **ElementTree** (Parse XML strings into Element objects for spectrum deserialization)
- **pymzML** (Instantiate Spectrum and Chromatogram objects from parsed XML Elements) — https://github.com/pymzml/pymzML
- **sqlite3** (Retrieve serialized XML strings from database queries)

## Examples

```
import xml.etree.ElementTree as et; xml_str = cursor.execute('SELECT xml_element FROM Spectra WHERE id = ?', (spectrum_id,)).fetchone()[0]; elem = et.fromstring(xml_str); spectrum = spec.Spectrum(elem)
```

## Evaluation signals

- Parsed Element object is of type xml.etree.ElementTree.Element and not None
- Instantiated Spectrum object contains valid mz and intensity arrays with matching lengths
- Spectrum object has a non-empty ID attribute matching the queried spectrum identifier
- __getitem__(integer_key) returns a Spectrum object and __getitem__(string_key) returns the same object or appropriate Chromatogram
- read() method returns sequential raw XML strings, while __getitem__ returns instantiated objects (not XML strings)

## Limitations

- ElementTree parser performance degrades with very large XML elements; consider streaming for files > 100 MB
- Malformed or incomplete XML strings will raise parsing exceptions; validation of XML schema before parsing is recommended
- Random access via __getitem__ requires pre-computed index mapping; sequential access via read() is simpler but slower for non-contiguous spectra
- Memory footprint grows linearly with number of instantiated Spectrum objects held in cache; implement LRU eviction for large datasets

## Evidence

- [other] import xml.etree.ElementTree as et: "import xml.etree.ElementTree as et"
- [other] parse XML and return Spectrum or Chromatogram objects via pymzML's spec module: "__getitem__ should parse XML and return Spectrum or Chromatogram objects via pymzML's spec module"
- [other] store each spectrum in a table with 2 columns, one for the identifier and one for the xml element: "store each spectrum in a table with 2 columns, one for the identifier and one for the xml element"
- [other] a read function used to sequentiallly read in data for iterating the database. In this simple approach, the read function always returns a whole spectra xml string.: "a read function used to sequentiallly read in data for iterating the database. In this simple approach, the read function always returns a whole spectra xml string."
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
