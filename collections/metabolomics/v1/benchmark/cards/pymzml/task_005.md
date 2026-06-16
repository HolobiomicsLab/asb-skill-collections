# SciTask Card: Implement the SQLiteDatabase custom file-class connector and verify spectrum retrieval via the pymzml run.Reader interface

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:28:47.137382+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pymzml/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `pymzml/pymzML`
- Input from: `task_004`
- Quality: Score 2/5 — Coherent: false, placeholder, 3 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `quality-control`

## Research Question
How does one implement a custom SQLiteDatabase class that integrates with pymzML's FileInterface to enable random-access retrieval of Spectrum and Chromatogram objects from a SQLite database indexed by spectrum ID?

## Connected Finding
The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects, (3) get_spectrum_count executing a COUNT query to report total spectra, and (4) read returning spectrum XML sequentially for iteration; registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database.

## Task Description
Implement a SQLiteDatabase wrapper class with __init__, __getitem__, get_spectrum_count, and read methods to enable pymzML's run.Reader to retrieve Spectrum and Chromatogram objects by integer key from a populated SQLite database, then register the wrapper in FileInterface._open for .db file detection.

## Inputs
- mzML file (e.g., BSA1.mzML.gz) to populate the SQLite database
- pymzML Reader-compatible mzML file path to iterate spectra during database creation

## Expected Outputs
- SQLite database file (.db) populated with spectrum ID and XML element string pairs in Spectra table
- Verified Spectrum or Chromatogram object retrieved by integer key from SQLiteDatabase instance
- Confirmed FileInterface._open correctly detects .db file extensions and instantiates SQLiteDatabase handler

## Expected Output File

- `test.db`

## Landmark Outputs

- `test.db`
- `spectrum_count_verified.txt`
- `random_access_retrieval_verified.txt`

## Tools
- sqlite3
- Python
- pymzML
- xml.etree.ElementTree

## Skills
- database-schema-design-and-implementation
- sqlite-query-execution-and-cursor-management
- xml-element-parsing-and-object-serialization
- pymzml-spectrum-object-instantiation
- file-handler-interface-integration-and-registration
- random-access-and-sequential-iteration-pattern-implementation

## Workflow Description
1. Create a SQLite database from an mzML file by parsing each spectrum using pymzML.run.Reader and storing the spectrum ID and XML string representation in a Spectra table with two columns (ID INT, xml TEXT). 2. Implement the SQLiteDatabase class with __init__ to establish a sqlite3 connection and cursor, __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing, get_spectrum_count to return the total row count from the Spectra table via SELECT COUNT(*), and read to sequentially return XML element strings by current_spectrum_id. 3. Modify FileInterface._open to add an elif statement checking for .db file endings and instantiate SQLiteDatabase(path, encoding) as the file_handler. 4. Verify random access by calling db[unique_id] and confirming a Spectrum or Chromatogram object is returned. 5. Verify sequential iteration by calling iter(et.iterparse(SQLiteDatabase('test.db'))) and iterating through results.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/plot.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, bug fixes, or feature additions available

## Domain Knowledge
- SQLiteDatabase wrapper must implement both __getitem__ (random access by spectrum ID) and read (sequential iteration) to be compatible with pymzML's run.Reader and file_interface expectations.
- Spectrum and Chromatogram objects are instantiated by parsing XML elements retrieved from the database and checking the element tag for 'spectrum' or 'chromatogram' keywords before object construction.
- FileInterface._open registration requires detecting file path extension (.db) and instantiating the custom handler class with path and encoding parameters to be integrated into the pymzML parsing pipeline.
- The Spectra table must store both spectrum ID (INT) and the full XML representation as a string to enable reconstruction of spec.Spectrum and spec.Chromatogram objects on retrieval.
- Sequential read() method must track current_spectrum_id state and increment it after each call to simulate file-like behavior for iterparse compatibility.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] How does one implement a custom SQLiteDatabase class that integrates with pymzML's FileInterface to enable random-access retrieval of Spectrum and Chromatogram objects from a SQLite database indexed by spectrum ID?: 'a new class needs to be written, which implements a `read` and a `__getitem__` function'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects, (3) get_spectrum_count executing a COUNT query to report total spectra, and (4) read returning spectrum XML sequentially for iteration; registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database.: 'class SQLiteDatabase(object):
		def __init__(self, path):
			connection = sqlite3.connect(path)
			self.cursor = connection.cursor()
		def __getitem__(self, key):
			self.cursor.execute('SELECT *'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] mzML file (e.g., BSA1.mzML.gz) to populate the SQLite database: 'At first, a database with a specific layout needs to be created. Here, we use a single mzML file and store each spectrum in a table with 2 columns'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] pymzML Reader-compatible mzML file path to iterate spectra during database creation: 'Run = Reader(os.path.abspath(mzml_path))'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] SQLite database file (.db) populated with spectrum ID and XML element string pairs in Spectra table: 'def create_database_from_file(db_name, mzml_path):
        conn = sqlite3.connect(db_name+'.db')
        Run = Reader(os.path.abspath(mzml_path))
        with conn:
            cursor ='
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Verified Spectrum or Chromatogram object retrieved by integer key from SQLiteDatabase instance: 'my_spec = db[unique_id]'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Confirmed FileInterface._open correctly detects .db file extensions and instantiates SQLiteDatabase handler: 'elif path.endswith('db'):
            from SQLiteConnector import SQLiteDatabase
            self.file_handler = SQLiteDatabase(path, encoding)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] sqlite3: 'import sqlite3'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Python: 'import sqlite3
    import os
    from pymzml import spec'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] pymzML: 'In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] xml.etree.ElementTree: 'import xml.etree.ElementTree as et'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, bug fixes, or feature additions available: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists in pymzML repository at path matching 'tests/data/BSA1.mzML.gz' or equivalent test dataset
- file_format_is: SQLite database file (.db extension) created by implementation
- script_runs: Python script instantiating SQLiteDatabase class with __init__, __getitem__, get_spectrum_count, and read methods without errors
- field_present: SQLiteDatabase instance has callable methods __init__, __getitem__, get_spectrum_count, read
- output_matches_reference: Spectrum or Chromatogram object returned from db[integer_key] is of pymzML spec.Spectrum or spec.Chromatogram type
- value_in_range: get_spectrum_count() returns non-negative integer matching actual record count in spectra table
- contains_substring: FileInterface registration includes conditional branch detecting .db file extension and routing to SQLiteDatabase class
- script_runs: pymzml.run.Reader instantiated on populated SQLite database file returns reader object without exception, robust to parameter choices in table schema

### Expert Review
- Verify that __getitem__ random-access implementation correctly maps integer keys to spectrum records without data corruption or misalignment
- Verify that read() sequential iteration method properly yields all Spectrum/Chromatogram objects in database order matching stored sequence
- Verify that spectrum/chromatogram objects returned from database query contain expected metadata fields (m/z, intensity, scan number, MS level) matching mzML source
- Verify that FileInterface registration does not conflict with existing file type handlers and correctly dispatches SQLiteDatabase on .db extension

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Parse source mzML file using pymzML.run.Reader and iterate through all spectra.
2. Create SQLite database with Spectra table (ID INT, xml TEXT) and insert spectrum ID and XML string pairs via parameterized INSERT statements.
3. Implement SQLiteDatabase class with __init__ establishing sqlite3 connection, __getitem__ executing SELECT queries and parsing XML to Spectrum/Chromatogram objects, get_spectrum_count returning COUNT(*) result, and read returning sequential element strings.
4. Register SQLiteDatabase in FileInterface._open by adding elif statement to detect .db extension and instantiate wrapper.
5. Validation: Verify random access by calling db[key] returns a valid Spectrum or Chromatogram object; verify spectrum count matches source mzML file; confirm sequential read() increments current_spectrum_id and returns XML strings.

## Workflow Ports

**Inputs:**

- `mzml_file` — mzML file to populate SQLite database ← `task_004/file_handler`

**Outputs:**

- `sqlite_db` — SQLite database file with Spectra table
- `spectrum_object` — Retrieved Spectrum or Chromatogram object by key

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:pymzML__pymzML`
- **Synthesized at:** 2026-06-16T07:35:06+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (3):
  - finding: evidence_span truncated and incomplete—does not match full finding text about four core components, SQL queries, registration in FileInterface, or run.Reader integration
  - finding: evidence_span shows only __init__ stub without __getitem__, get_spectrum_count, or read method implementations that the finding claims are required
  - research_question: evidence_span ('a new class needs to be written, which implements a `read` and a `__getitem__` function') is generic and does not specifically address SQLite integration, FileInterface registration, or spectrum/chromatogram object return types
- Notes: This card has significant coherence and grounding issues. The research_question and finding do not align semantically—the RQ asks a procedural 'how' question while the finding prescribes specific implementation components. The evidence_span for the finding is demonstrably incomplete (truncated at 'SELECT *') and fails to support claims about get_spectrum_count, read method behavior, or FileInterface registration. The research_question evidence_span is generic placeholder language that could apply to any wrapper class implementation. The workflow_description and domain_knowledge sections are detailed and helpful, but the core RQ-Finding pair lacks sufficient specificity and groundedness. Recommend: (1) rewrite RQ to match finding's prescriptive scope; (2) provide complete code evidence_spans for all four claimed methods; (3) include evidence for FileInterface._open registration; (4) verify evidence_spans are not truncated by source extraction.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
