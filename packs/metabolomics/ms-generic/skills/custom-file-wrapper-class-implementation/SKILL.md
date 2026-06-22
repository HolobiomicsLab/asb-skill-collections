---
name: custom-file-wrapper-class-implementation
description: Use when when you have mass spectrometry data stored in a database or non-mzML file format and need to integrate it into the pymzML pipeline without converting to mzML. Use this skill when FileInterface does not natively recognize your file extension and you want to avoid data conversion overhead.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - black
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# custom-file-wrapper-class-implementation

## Summary

Implement a custom file wrapper class to enable pymzML to read and randomly access mass spectrometry data stored in non-standard formats (e.g., SQLite databases) by wrapping the data source with __getitem__, read(), and get_spectrum_count() methods that pymzML's FileInterface can detect and instantiate.

## When to use

When you have mass spectrometry data stored in a database or non-mzML file format and need to integrate it into the pymzML pipeline without converting to mzML. Use this skill when FileInterface does not natively recognize your file extension and you want to avoid data conversion overhead.

## When NOT to use

- Your input is already a standard mzML or mzML.gz file — use FileInterface's native mzML parser instead
- You need to modify the core pymzML parsing logic beyond file detection — consider contributing upstream or using pymzML as a library without wrapping
- Your data store does not support fast indexed access (e.g., sequential-only log files) — the __getitem__ method requires random access capability

## Inputs

- Database file (e.g., .db with schema: ID INTEGER, xml TEXT)
- File extension string (e.g., '.db')
- Mass spectrometry spectrum records with unique identifiers

## Outputs

- Custom wrapper class instance registered in FileInterface
- Random-access spectrum retrieval by ID
- Sequential spectrum iteration via read() method
- igzip-compatible compressed block format per spectrum

## How to apply

Create a wrapper class that implements three core methods: __getitem__(key) to retrieve spectra by ID from your underlying data store (e.g., sqlite3 query), read(size=-1) to sequentially iterate through all spectra in order, and get_spectrum_count() to return the total number of spectra. Store each spectrum as xml text in your data source. Register the wrapper in pymzML's FileInterface._open() by adding an elif statement that detects your file extension and instantiates your wrapper class. The wrapper converts each spectrum from your data store into igzip-compatible block format on retrieval. Test random access via db[spectrum_id] lookups and sequential iteration via for loops over the wrapper instance to verify both access patterns work correctly.

## Related tools

- **pymzML** (File interface framework that calls wrapper methods __getitem__ and read() for spectrum access; FileInterface._open() detects wrapper registration) — https://github.com/pymzml/pymzML
- **sqlite3** (Database engine for storing spectrum ID and xml TEXT columns; queried by wrapper's __getitem__ and read() methods)
- **xml.etree.ElementTree** (XML parsing library to convert spectrum records from database into ElementTree objects compatible with pymzML spectrum handling)
- **black** (Code formatter for ensuring wrapper class meets pymzML code style conventions) — https://github.com/psf/black

## Examples

```
class SQLiteDatabase:
    def __init__(self, db_path):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    def __getitem__(self, spectrum_id):
        self.cursor.execute("SELECT xml FROM spectra WHERE ID=?", (spectrum_id,))
        return self.cursor.fetchone()[0]
    def read(self, size=-1):
        self.cursor.execute("SELECT xml FROM spectra")
        for row in self.cursor.fetchall():
            yield row[0]
    def get_spectrum_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM spectra")
        return self.cursor.fetchone()[0]
```

## Evaluation signals

- Wrapper class correctly registered: FileInterface._open() detects the file extension and instantiates the wrapper without errors
- Random access works: db[spectrum_id] returns the correct spectrum record for multiple arbitrary IDs with no sequential dependency
- Sequential iteration works: for spectrum in wrapper_instance returns all spectra in insertion or defined order
- Spectrum count is accurate: get_spectrum_count() matches SELECT COUNT(*) result from database
- igzip block format is valid: compressed spectrum blocks can be read back by pymzML's indexed gzip reader without corruption

## Limitations

- Wrapper performance depends on underlying database query speed; large databases may benefit from indexing on the ID column
- The __getitem__ method must handle KeyError gracefully when a spectrum ID does not exist in the database
- Sequential read() iteration assumes spectra are stored in stable order; if database rows are deleted or reordered, iteration may skip or repeat records
- igzip block compression is applied per-spectrum; this may not match file-level compression efficiency of standard indexed gzip files

## Evidence

- [readme] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [other] def get_spectrum_count(self): self.cursor.execute("SELECT COUNT(*) from spectra"): "def get_spectrum_count(self): self.cursor.execute("SELECT COUNT(*) from spectra")"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [other] Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]: "Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]"
