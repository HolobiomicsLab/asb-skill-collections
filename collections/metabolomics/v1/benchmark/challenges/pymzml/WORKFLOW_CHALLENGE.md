# Workflow Challenge: `coll_pymzml_workflow`


> pymzML is a Python extension that provides easy access to mass spectrometry data through multiple file format handlers, including support for indexed gzip compression and custom database backends.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reconstructs 5 described mechanisms (described in the paper but not separately evaluated there): The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example), followed by index-to-offset mapping pairs, all terminated with a zero byte (\x00). The GSGW class writes indexed gzip files where each chapter is indexed by chapter number and stored in independently accessible compressed blocks. The igzip file header contains ID bytes, version, index length, and offset length fields, followed by chapter-to-offset mappings terminated by a zero byte, enabling random access retrieval. The GSGR class is initialized with a path to an indexed gzip file and supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index, with the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte. The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip, otherwise StandardGzip; for '.db' extensions it instantiates SQLiteDatabase; for all other paths it defaults to StandardMzml. The SQLiteDatabase implementation requires four core components: (1) __init__ accepting a database path and establishing a sqlite3 connection, (2) __getitem__ executing SQL queries to fetch spectrum XML by key and returning Spectrum or Chromatogram objects, (3) get_spectrum_count executing a COUNT query to report total spectra, and (4) read returning spectrum XML sequentially for iteration; registration in FileInterface._open via an elif condition for .db file extensions enables pymzML.run.Reader to transparently access the database.

## Research questions

- What is the binary header structure of the indexed gzip (igzip) file format, and how are index-to-offset pairs encoded within the gzip comment field?
- How does the GSGW class structure indexed gzip files to enable chapter-by-chapter seekability of Moby Dick text, and what is the format of the resulting file header?
- How does the GSGR class read indexed gzip files by parsing the igzip header comment field to retrieve the index-to-offset mapping, and then use that mapping to access specific blocks by integer key?
- How does the FileInterface._open method conditionally dispatch file handlers based on file extension and indexed gzip detection to support multiple mzML file formats?
- How does one implement a custom SQLiteDatabase class that integrates with pymzML's FileInterface to enable random-access retrieval of Spectrum and Chromatogram objects from a SQLite database indexed by spectrum ID?

## Methods overview

Define igzip binary header structure constants: magic ID bytes, VERSION field, IDXLEN and OFFSETLEN metadata. Implement binary packing and serialization functions for index-to-offset pairs using Python struct module with OFFSETLEN-determined widths. Assemble complete header by concatenating magic bytes, version, metadata, index pairs, and zero-terminator. Parse provided Moby Dick hex dump reference to extract expected byte sequences. Validation: compare generated header bytes byte-for-byte against hex dump reference; output must match with 100% fidelity. Create and populate a SQLite database with chapters as rows (ID, text_content), parsing Moby Dick into chapter units. Implement GSGW class with __getitem__() for random chapter retrieval, read() for sequential iteration, and get_spectrum_count() for chapter enumeration. Compress each chapter independently into igzip-compatible blocks and construct indexed .gz header with block offsets and chapter identifiers. Register GSGW in FileInterface._open() via elif branch detecting .db extension and instantiating the wrapper. Validation: verify random access by retrieving chapters via db[id] and confirm sequential iteration via for loop; verify igzip header conforms to specification and all chapter offsets resolve correctly. Open and read the igzip file header to extract the embedded index table. Parse the index into a dictionary structure mapping integer item IDs to byte offsets. Implement __getitem__ to look up the offset for a given key, seek to that position, and decompress the item. Implement a read method to support sequential access by maintaining current item state. Validation: Verify that bracket-notation access (e.g., handler[5]) returns the correct decompressed item content matching the index entry. Define `_open` method with path and encoding parameters. Implement conditional dispatch: inspect file extension (.gz, .db, or default) and call optional indexed-gzip check for .gz files. Instantiate correct handler class (IndexedGzip, StandardGzip, StandardMzml, or SQLiteDatabase) with path and encoding arguments. Return the instantiated handler object to the caller. Validation: Unit test each dispatch branch with representative file paths (uncompressed mzML, standard .mzML.gz, indexed .mzML.gz, .db) and assert handler type is correct; integration test by passing handler to Reader and verifying spectrum retrieval succeeds. Parse source mzML file using pymzML.run.Reader and iterate through all spectra. Create SQLite database with Spectra table (ID INT, xml TEXT) and insert spectrum ID and XML string pairs via parameterized INSERT statements. Implement SQLiteDatabase class with __init__ establishing sqlite3 connection, __getitem__ executing SELECT queries and parsing XML to Spectrum/Chromatogram objects, get_spectrum_count returning COUNT(*) result, and read returning sequential element strings. Register SQLiteDatabase in FileInterface._open by adding elif statement to detect .db extension and instantiate wrapper. Validation: Verify random access by calling db[key] returns a valid Spectrum or Chromatogram object; verify spectrum count matches source mzML file; confirm sequential read() increments current_spectrum_id and returns XML strings.

**Domain:** bioinformatics

**Techniques:** feature-detection, quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** pymzML is a module to parse mzML data in Python based on cElementTree. _[grounded: pymzml_system]_
- **(finding)** pymzML was developed by multiple authors including M. Kösters, J. Leufken, T. Bald, A. Niehues, S. Schulze, K. Sugimoto, R.P. Zahedi, M. Hippler, S.A. Leidel, and C. Fufezan. _[grounded: pymzml_system]_
- **(finding)** Dr. Christian Fufezan is the Group Leader of Experimental Bioinformatics at Cellzome GmbH.
- **(finding)** pymzML offers easy access to mass spectrometry data that allows rapid development of tools. _[grounded: pymzml_system]_
- **(finding)** pymzML supports reading indexed gzip files, which allows mzML file sizes to reach the levels of the original RAW format. _[grounded: pymzml_system]_
- **(finding)** pymzML can rapidly seek into any uncompressed mzML file with or without an included index. _[grounded: pymzml_system]_
- **(finding)** pymzML allows setting a custom regex to parse the index when initializing the reader for non-standard mzML index identifiers. _[grounded: pymzml_system]_
- **(finding)** pymzML's Reader class supports random access via the __getitem__ magic function. _[grounded: pymzml_system]_
- **(finding)** Custom file handler classes for pymzML must implement a read function and a __getitem__ function. _[grounded: pymzml_system]_
- **(finding)** Custom file handlers for pymzML can be enabled by editing the _open function in file_interface.py. _[grounded: pymzml_system]_
- **(finding)** The igzip file format includes a comment field that stores unique IDs, version, index length, and offset length. _[grounded: arch_igzip_format]_
- **(finding)** The GSGW and GSGR classes can be used to index any type of data beyond mzML files. _[grounded: pymzml_system]_
- **(finding)** The GSGW class initializes with parameters for file, max_idx, max_idx_len, and output_path. _[grounded: comp_gsgw]_
- **(finding)** The GSGR class provides bracket notation access to retrieve indexed chapters from compressed files. _[grounded: pymzml_system]_
- **(finding)** pymzML's FileInterface class provides file handler detection based on file path extension. _[grounded: pymzml_system]_
- **(hypothesis)** A Spectrum object in pymzML can be accessed by the bracket notation __getitem__ function. _[grounded: pymzml_system]_
- **(finding)** pymzML supports arithmetic operations on Spectrum objects including addition, subtraction, multiplication, and true division. _[grounded: pymzml_system]_
- **(finding)** The SQLiteDatabase example wrapper for pymzML uses sqlite3 to store spectrum XML elements in a table with ID and xml TEXT columns. _[grounded: pymzml_system]_
- **(finding)** pymzML's Spectrum class includes a to_string() method to serialize spectrum objects to XML strings. _[grounded: pymzml_system]_
- **(finding)** The SQLiteDatabase wrapper's read function increments a current_spectrum_id counter to sequentially read spectra. _[grounded: comp_sqlite_connector]_
- **(finding)** pymzML's Reader class iterates spectra using xml.etree.ElementTree.iterparse. _[grounded: pymzml_system]_
- **(finding)** MS level information can be retrieved from a spectrum object in pymzML using bracket notation. _[grounded: pymzml_system]_
- **(finding)** Total ion current information can be retrieved from a spectrum object in pymzML using bracket notation. _[grounded: pymzml_system]_
- **(finding)** pymzML spectrum objects support checking for the presence of 'collision-induced dissociation' in their keys. _[grounded: pymzml_system]_
- **(finding)** pymzML spectrum objects support checking for the presence of 'high-energy collision-induced dissociation' in their keys. _[grounded: pymzml_system]_
- **(finding)** pymzML supports the StandardMzml file class for accessing uncompressed mzML files. _[grounded: pymzml_system]_
- **(finding)** pymzML supports the StandardGzip file class for accessing gzip-compressed mzML files. _[grounded: pymzml_system]_
- **(finding)** pymzML supports the IndexedGzip file class for accessing indexed gzip-compressed mzML files. _[grounded: pymzml_system]_
- **(finding)** The benchmark dataset used in pymzML documentation contains TMT labeled E.coli cells on human background. _[grounded: pymzml_system]_
- **(finding)** pymzML benchmark files include samples from Orbitrap, Lumos, HF, and HF-X instruments run in DDA mode. _[grounded: pymzml_system]_
- **(finding)** pymzML documentation includes HF benchmark samples designated P0109699E18, P0109699E19, and P0109699E22. _[grounded: pymzml_system]_
- **(finding)** pymzML documentation includes HF-X benchmark samples designated P0174319B7, P0174319B8, and P0174319B9. _[grounded: pymzml_system]_
- **(finding)** pymzML documentation includes Lumos benchmark samples designated P0109699K8, P0109699K9, and P0109699K10. _[grounded: pymzml_system]_
- **(finding)** pymzML documentation includes OrbiElite benchmark samples designated P81464G09 and P81464G10. _[grounded: pymzml_system]_
- **(finding)** pymzML benchmark files in igz format are available at https://drive.google.com/drive/folders/1GbN0cAqiyAEljcuooYKkqW4rcKlOlc5n _[grounded: pymzml_system]_
- **(finding)** The gzip format specification is defined in RFC 1952.
- **(finding)** The igzip format includes a header with ID1, ID2, CM, FLG, MTIME, XFL, and OS fields.
- **(finding)** The igzip format includes CRC32 and ISIZE fields at the end of compressed blocks.
- **(finding)** The igzip format comment field stores Index and Offset data terminated with a zero byte.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Custom file handler classes can be implemented as alternatives to StandardMzml, StandardGzip, or IndexedGzip
- Read smaller chunks of spectrum XML and jump to next spectrum at end of current spectrum

## Steps

### Step `task_001`
- Title: Reconstruct the igzip file format header encoding and index/offset mapping
- Task kind: `component_reconstruction`
- Task: Implement the binary header structure for igzip indexed gzip files (ID bytes, VERSION, IDXLEN, OFFSETLEN, and index entry pairs) according to the pymzML specification, and validate the implementation against a provided hex dump reference.
- Inputs:
  - igzip binary format specification documenting header structure (ID bytes, VERSION, IDXLEN, OFFSETLEN, index pairs, zero-terminator)
  - Moby Dick example hex dump showing expected igzip header bytes for validation
- Expected outputs:
  - Python module or script implementing igzip header binary structure encoding functions (pack_header, encode_index_pairs, write_header_bytes)
  - Test report or validation script output showing byte-for-byte match between generated and reference hex dump
- Tools: pymzML, Python
- Landmark output files: igzip_header_encoder.py, test_igzip_header_against_moby_dick.py, validation_output.txt
- Primary expected artifact: `igzip_header_validator.py`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the GSGW indexed gzip writer for chapter-level block indexing of Moby Dick
- Task kind: `component_reconstruction`
- Task: Implement a custom file wrapper class (GSGW) that parses Moby Dick chapter-by-chapter, writes each chapter as an independently seekable compressed block, and produces an indexed .gz file conforming to the igzip specification with a functioning __getitem__ method for random access and read() method for sequential iteration.
- Inputs:
  - Moby Dick plain text file or chapter-segmented text source
  - SQLite3 database connection configuration and path specification
- Expected outputs:
  - Indexed .gz file with igzip-compatible header containing chapter offsets and block metadata
  - GSGW wrapper class implementation with __getitem__, read(), and get_spectrum_count() methods
  - Modified FileInterface._open() method with elif statement for .db file detection and GSGW instantiation
- Tools: pymzML, sqlite3, Python, xml.etree.ElementTree
- Landmark output files: moby_dick.db, chapter_offsets.json, moby_dick_indexed.db.gz, gsgw_wrapper.py, fileinterface_patch.py
- Primary expected artifact: `moby_dick_indexed.db.gz`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the GSGR indexed gzip reader for random-access chapter retrieval from the Moby Dick igz file
- Task kind: `component_reconstruction`
- Task: Implement a custom file handler class (GSGR) that reads an igzip-compressed index from a file header and enables bracket-notation random access to retrieve individual items (e.g., chapters) by integer index, returning the decompressed content as output.
- Inputs:
  - igzip-compressed file with embedded index in header (e.g., Moby Dick compressed with igzip)
- Expected outputs:
  - Retrieved item content (text or binary) corresponding to the requested integer index
- Tools: pymzML, Python, xml.etree.ElementTree
- Landmark output files: index_dict.json, item_retrieval_test.txt

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the FileInterface dispatch logic for routing mzML file types to their respective handler classes
- Task kind: `component_reconstruction`
- Task: Implement the `_open` method in `FileInterface` to conditionally dispatch file handling to `IndexedGzip`, `StandardGzip`, `StandardMzml`, or `SQLiteDatabase` based on file extension, and verify each dispatch branch correctly instantiates the appropriate handler class.
- Inputs:
  - File path to mzML file (uncompressed, standard gzip, or indexed gzip format)
  - File path to SQLite database file containing spectra table
  - Encoding parameter for text file handling (e.g., UTF-8)
- Expected outputs:
  - File handler instance (IndexedGzip, StandardGzip, StandardMzml, or SQLiteDatabase) correctly instantiated for the input file type
  - Test report documenting correct dispatch to each of the four handler classes with passing assertions
- Tools: pymzML, Python, sqlite3, xml.etree.ElementTree
- Landmark output files: handler_dispatch_matrix.csv, test_indexed_gzip_handler.log, test_standard_gzip_handler.log, test_standard_mzml_handler.log, test_sqlite_handler.log, spectrum_retrieval_integration_test.log
- Primary expected artifact: `file_interface_open_method.py`

### Step `task_005`
- Depends on: `task_004`
- Title: Implement the SQLiteDatabase custom file-class connector and verify spectrum retrieval via the pymzml run.Reader interface
- Task kind: `component_reconstruction`
- Task: Implement a SQLiteDatabase wrapper class with __init__, __getitem__, get_spectrum_count, and read methods to enable pymzML's run.Reader to retrieve Spectrum and Chromatogram objects by integer key from a populated SQLite database, then register the wrapper in FileInterface._open for .db file detection.
- Inputs:
  - mzML file (e.g., BSA1.mzML.gz) to populate the SQLite database
  - pymzML Reader-compatible mzML file path to iterate spectra during database creation
- Expected outputs:
  - SQLite database file (.db) populated with spectrum ID and XML element string pairs in Spectra table
  - Verified Spectrum or Chromatogram object retrieved by integer key from SQLiteDatabase instance
  - Confirmed FileInterface._open correctly detects .db file extensions and instantiates SQLiteDatabase handler
- Tools: sqlite3, Python, pymzML, xml.etree.ElementTree
- Landmark output files: test.db, spectrum_count_verified.txt, random_access_retrieval_verified.txt
- Primary expected artifact: `test.db`

## Final expected outputs

- `Retrieved item content (text or binary) corresponding to the requested integer index` (type: file, tolerance: hash)
- `SQLite database file (.db) populated with spectrum ID and XML element string pairs in Spectra table` (type: file, tolerance: hash)
- `Verified Spectrum or Chromatogram object retrieved by integer key from SQLiteDatabase instance` (type: file, tolerance: hash)
- `Confirmed FileInterface._open correctly detects .db file extensions and instantiates SQLiteDatabase handler` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** dynamic

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_pymzml_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Retrieved item content (text or binary) corresponding to the requested integer index": "<locator>",
    "SQLite database file (.db) populated with spectrum ID and XML element string pairs in Spectra table": "<locator>",
    "Verified Spectrum or Chromatogram object retrieved by integer key from SQLiteDatabase instance": "<locator>",
    "Confirmed FileInterface._open correctly detects .db file extensions and instantiates SQLiteDatabase handler": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
