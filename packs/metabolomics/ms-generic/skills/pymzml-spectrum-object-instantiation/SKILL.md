---
name: pymzml-spectrum-object-instantiation
description: Use when when you have mzML spectrum XML already parsed (either from a file, a database query, or an in-memory representation) and need to construct Spectrum or Chromatogram objects that expose methods like accessing MS level, retention time, m/z and intensity arrays, and other metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - pymzML
  - xml.etree.ElementTree
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
- In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pymzml-spectrum-object-instantiation

## Summary

Instantiate pymzML Spectrum or Chromatogram objects from mzML XML elements or from a custom file interface (e.g., SQLite database) to enable programmatic access to mass spectrometry metadata and peak data. This skill is essential when integrating non-standard data sources into pymzML's run.Reader interface.

## When to use

When you have mzML spectrum XML already parsed (either from a file, a database query, or an in-memory representation) and need to construct Spectrum or Chromatogram objects that expose methods like accessing MS level, retention time, m/z and intensity arrays, and other metadata. Specifically use this when implementing a custom FileInterface wrapper (e.g., for SQLite or other databases) that must return pymzML-compatible spectrum objects from __getitem__ or read methods.

## When NOT to use

- The mzML file is already being read directly via pymzml.run.Reader; instantiation is already handled internally.
- You only need to count or filter spectra without accessing individual spectrum data; use get_spectrum_count() instead.
- The input is not valid mzML XML (e.g., malformed or non-standard schema); the constructor will fail or produce incomplete objects.

## Inputs

- mzML XML element (xml.etree.ElementTree.Element)
- spectrum ID (int or string, for lookup)
- database path (str) or file path to mzML source

## Outputs

- pymzML Spectrum object
- pymzML Chromatogram object

## How to apply

Parse the mzML XML element using xml.etree.ElementTree.XML() to obtain an ElementTree Element object. Pass this Element to the pymzML Spectrum or Chromatogram constructor, which internally extracts all spectrum metadata (ID, MS level, precursor m/z, retention time) and intensity/m/z array data from the standardized mzML XML schema. The correct object type (Spectrum vs. Chromatogram) is determined by inspecting the XML element's tag or attributes; in the context of a custom file wrapper, __getitem__ should inspect the spectrum type and instantiate accordingly. Return the constructed object to the caller (e.g., pymzML.run.Reader) so it can be used transparently in iteration or random-access patterns. Verify that the returned object has valid attributes (MS level, scan ID, arrays) and supports iteration over peaks.

## Related tools

- **pymzML** (Provides Spectrum and Chromatogram classes whose constructors accept parsed XML elements and instantiate objects with full metadata and peak data access) — https://github.com/pymzml/pymzML
- **sqlite3** (Enables querying of spectrum XML strings from a SQLite database for subsequent instantiation)
- **xml.etree.ElementTree** (Parses mzML XML strings into Element objects required by Spectrum/Chromatogram constructors)

## Examples

```
import xml.etree.ElementTree as et; import sqlite3; cursor.execute('SELECT xml FROM spectra WHERE id=?', (5,)); xml_str = cursor.fetchone()[0]; elem = et.XML(xml_str); spectrum = pymzml.spec.Spectrum(elem)
```

## Evaluation signals

- Returned object is an instance of pymzML.spec.Spectrum or pymzML.spec.Chromatogram
- Object has valid attributes: scan ID, MS level, retention time, and arrays (if MS1); check via hasattr() or direct attribute access
- Spectrum can be iterated to yield Peaklist objects with m/z and intensity values
- Object's string representation or __repr__ matches expected metadata (e.g., 'Spectrum(scan=5, ms_level=2, rt=10.5)')
- Database query returns the correct spectrum when accessed via db[spectrum_id], and the returned object matches a reference spectrum from the original mzML file

## Limitations

- Spectrum instantiation from XML requires the XML to conform to the mzML standard schema; non-standard or corrupted XML will produce incomplete or invalid objects.
- Performance depends on XML parsing cost; large XML elements or many instantiations in sequence can be slow; consider caching or lazy loading.
- If the mzML file or database does not include m/z or intensity array data (binary arrays), the returned Spectrum object will not support peak access methods.
- Custom file interface implementations must correctly distinguish between Spectrum and Chromatogram elements (by tag or attribute inspection); incorrect classification breaks downstream code.

## Evidence

- [other] Implement the SQLiteDatabase class with __init__ to establish a sqlite3 connection and cursor, __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing: "implement the SQLiteDatabase class with __init__ to establish a sqlite3 connection and cursor, __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [abstract] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools: "pymzML is an extension to Python that offers easy access to mass spectrometry (MS) data that allows the rapid development of tools"
- [other] Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]: "Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]"
