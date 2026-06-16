---
name: random-access-and-sequential-iteration-pattern-implementation
description: Use when when you need to support fast, non-sequential lookups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
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

# random-access-and-sequential-iteration-pattern-implementation

## Summary

Implement a custom file-handler class that enables both random-access (via __getitem__) and sequential iteration (via read) over structured data sources like SQLite databases, integrating seamlessly with pymzML's FileInterface to support transparent spectrum retrieval. This pattern decouples data storage backends from the parsing interface, allowing alternative representations (database, archive, remote) to be accessed through a uniform API.

## When to use

When you need to support fast, non-sequential lookups (e.g., spectrum by ID) on a large mzML dataset stored in a non-standard format (SQLite database, HDF5, archive), and you also want to preserve the ability to iterate sequentially through all records without loading the entire dataset into memory. Use this pattern when integrating custom storage backends with pymzML or similar parsers that expect both __getitem__ and iteration support.

## When NOT to use

- Input is an uncompressed or indexed mzML file that pymzML already handles natively with __getitem__ and iteration — the overhead of database lookup outweighs the benefit.
- Data source is small enough to fit in memory; direct in-memory caching or standard mzML parsing is more efficient.
- Random-access lookup patterns are not required; if your workflow only iterates sequentially, a simpler streaming parser suffices.

## Inputs

- SQLite database file (.db) with indexed spectrum records (ID INT, xml TEXT columns)
- mzML source file (for initial database population)
- Database file path (string)
- Spectrum ID or index (int or string key for random access)

## Outputs

- Spectrum or Chromatogram object (parsed from XML)
- Iterator over Spectrum/Chromatogram objects (for sequential access)
- Spectrum count (int)
- Custom file-handler instance integrated into FileInterface

## How to apply

Implement a custom wrapper class with four required methods: (1) __init__ accepting a data source path (e.g., SQLite database file) and establishing a connection or file handle; (2) __getitem__(key) executing a direct lookup query (e.g., SQL SELECT by spectrum ID) and returning a parsed object (Spectrum or Chromatogram); (3) get_spectrum_count() returning the total record count via a COUNT query; (4) read() yielding or returning XML/structured data sequentially by internal cursor position to support iteration. Register the wrapper in the host library's file interface by adding a file-extension detection rule (e.g., elif path.endswith('.db'): return SQLiteDatabase(path, encoding)). Verify correctness by testing both random access (db[unique_id] returns correct object) and sequential iteration (iterating through parsed objects matches expected order and count).

## Related tools

- **pymzML** (Parser framework defining FileInterface and providing Spectrum/Chromatogram object models; your custom class registers via FileInterface._open and inherits expected method signatures) — https://github.com/pymzml/pymzML
- **sqlite3** (Database connection and query execution in __init__, __getitem__, get_spectrum_count, and read methods)
- **xml.etree.ElementTree** (Parsing stored XML strings (from database TEXT column) into Spectrum/Chromatogram objects using XML() constructor)
- **Python** (Implementation language for wrapper class definition and pymzML integration)

## Examples

```
import sqlite3
from pymzml.spec import Spectrum
import xml.etree.ElementTree as et

class SQLiteDatabase:
    def __init__(self, path, encoding='utf-8'):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.current_spectrum_id = 0
    
    def __getitem__(self, key):
        self.cursor.execute("SELECT xml FROM spectra WHERE ID = ?", (key,))
        row = self.cursor.fetchone()
        return Spectrum(et.XML(row[0]))
    
    def get_spectrum_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM spectra")
        return self.cursor.fetchone()[0]
    
    def read(self):
        self.cursor.execute("SELECT xml FROM spectra ORDER BY ID")
        for row in self.cursor.fetchall():
            yield et.XML(row[0])

db = SQLiteDatabase('test.db')
my_spectrum = db[5]
for spectrum_xml in db.read():
    print(spectrum_xml)
```

## Evaluation signals

- db[unique_id] returns a Spectrum or Chromatogram object with correct attributes (m/z, intensity, metadata) matching the original mzML entry.
- get_spectrum_count() matches SELECT COUNT(*) from the database; consistent across repeated calls.
- Iterating through iter(db) or manually calling db.read() yields all spectra in insertion/ID order without skipping or duplicating records.
- FileInterface._open correctly detects .db file extension and instantiates SQLiteDatabase; pymzml.run.Reader(db_file) succeeds without errors.
- Random-access latency is sub-second for typical spectra counts (10k–100k records); sequential iteration completes in time consistent with mzML parsing overhead.

## Limitations

- Database schema is assumed to have exactly two columns (ID INT, xml TEXT); non-standard schemas require wrapper modifications.
- XML parsing performance depends on spectrum complexity and database indexing; non-indexed lookups on large tables degrade linearly.
- Read-only access pattern: the wrapper does not support spectrum modification or insertion; re-creating the database is required for updates.
- Sequential iteration order is defined by the database's insertion or ID order, not by user-defined sort keys; custom ordering requires additional sorting logic.
- No built-in support for indexed gzip compression (unlike native mzML parsing in pymzML); storage footprint may be larger than compressed .mzML.gz files.

## Evidence

- [other] The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects, (3) get_spectrum_count executing a COUNT query to report total spectra, and (4) read returning spectrum XML sequentially for iteration: "The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum"
- [other] registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database: "registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [other] def get_spectrum_count(self):
            self.cursor.execute("SELECT COUNT(*) from spectra"): "def get_spectrum_count(self):
            self.cursor.execute("SELECT COUNT(*) from spectra")"
- [intro] pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not: "pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included"
