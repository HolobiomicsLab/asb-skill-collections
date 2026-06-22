---
name: file-handler-interface-integration
description: Use when you have mass spectrometry data stored in a non-standard format (SQLite database, custom indexed gzip files, or other database backends) and want to enable pymzML's Reader to access it with both random-access by spectrum ID and sequential iteration capabilities, avoiding the need to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - xml.etree.ElementTree
  - sqlite3
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import xml.etree.ElementTree as et
- import sqlite3
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

# file-handler-interface-integration

## Summary

Implement a custom file-handler class that integrates with pymzML's FileInterface to enable random-access and sequential retrieval of mass spectrometry data from alternative storage backends (e.g., SQLite databases, indexed gzip archives). This skill allows transparent access to spectrum and chromatogram objects through pymzML's standard Reader interface without requiring the data to be in native mzML format.

## When to use

Use this skill when you have mass spectrometry data stored in a non-standard format (SQLite database, custom indexed gzip files, or other database backends) and want to enable pymzML's Reader to access it with both random-access by spectrum ID and sequential iteration capabilities, avoiding the need to convert the entire dataset to mzML format upfront.

## When NOT to use

- Data is already in uncompressed or standard-compressed mzML format — use pymzML's native Reader directly without a custom handler.
- You require write access or need to modify spectra in-place — the FileInterface is designed for read-only access.

## Inputs

- path to data storage (file path, database URI, or equivalent locator)
- spectrum/chromatogram identifier (integer key or string ID)
- optional encoding parameter for XML parsing

## Outputs

- Spectrum object (parsed from XML)
- Chromatogram object (parsed from XML)
- integer spectrum count
- XML element string (for sequential iteration)

## How to apply

Implement a custom class with four core methods: (1) __init__ to establish a connection to your data source (e.g., sqlite3 connection for databases), (2) __getitem__ to execute lookups by spectrum ID and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing, (3) get_spectrum_count to report total spectra via a query or count operation, and (4) read to return spectrum XML sequentially for iteration. Then register the handler in pymzML's FileInterface._open by adding an elif condition that detects your file extension or format signature and instantiates your custom class. This allows pymzML.run.Reader to transparently route file access to your handler, delegating both bracket-notation random access (reader[spectrum_id]) and for-loop iteration (for spectrum in reader) to your implementation.

## Related tools

- **pymzML** (core framework; provides FileInterface base class and Reader for spectrum access via custom handlers) — https://github.com/pymzml/pymzML
- **sqlite3** (optional backend for storing and querying spectrum metadata and XML in a relational table structure)
- **xml.etree.ElementTree** (parses XML element strings returned from storage backend into Spectrum/Chromatogram objects)
- **Python** (language for implementing custom handler class and integrating with pymzML)

## Examples

```
from pymzml import spec; import sqlite3; class SQLiteDatabase: 
    def __init__(self, path): self.conn = sqlite3.connect(path); self.cursor = self.conn.cursor()
    def __getitem__(self, key): self.cursor.execute('SELECT xml FROM spectra WHERE id=?', (key,)); xml_str = self.cursor.fetchone()[0]; return spec.Spectrum(xmlElement=xml.etree.ElementTree.XML(xml_str))
    def get_spectrum_count(self): self.cursor.execute('SELECT COUNT(*) FROM spectra'); return self.cursor.fetchone()[0]
    def read(self): pass
db = SQLiteDatabase('test.db'); my_spec = db[5]
```

## Evaluation signals

- Bracket-notation access returns a valid Spectrum or Chromatogram object: db[5] returns an object with expected attributes (mz, intensity, scan_time, etc.)
- get_spectrum_count returns a positive integer matching the actual number of spectra in the backend
- Sequential iteration yields all spectra in order: for spectrum in iter(handler) completes without error and counts match total
- Random access is truly random (no sequential seeking required): accessing handler[last_id] then handler[first_id] is fast and correct
- pymzML.run.Reader transparently routes access to the custom handler after FileInterface._open registration (no explicit handler instantiation in user code needed)

## Limitations

- FileInterface integration requires modification of pymzML source code (adding elif to FileInterface._open), which may break or require updates if pymzML's internal structure changes.
- Read-only access: the FileInterface pattern does not support write or update operations; spectrum data is immutable once stored.
- Sequential and random access modes may have different performance characteristics depending on the backend; random access on a database with poor indexing will be slow.
- XML parsing of every spectrum on __getitem__ adds per-access overhead; consider caching if the same spectrum is accessed multiple times.

## Evidence

- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects, (3) get_spectrum_count executing a COUNT query to report total spectra, and (4) read returning spectrum XML sequentially for iteration: "four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or"
- [other] registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database: "registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database"
- [readme] pymzML is an extension to Python that offers a very fast parser for mzML data, the standard mass spectrometry data format: "pymzML is an extension to Python that offers a very fast parser for mzML data, the standard mass spectrometry data format"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
