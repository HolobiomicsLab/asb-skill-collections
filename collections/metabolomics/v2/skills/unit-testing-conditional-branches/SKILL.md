---
name: unit-testing-conditional-branches
description: Use when when implementing or refactoring a FileInterface._open method or similar polymorphic dispatcher that conditionally instantiates different handler classes based on file extension (e.g., .gz, .db) or format metadata (e.g., indexed gzip detection).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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

# unit-testing-conditional-branches

## Summary

Systematically verify that each conditional branch in a file handler dispatch system correctly instantiates the appropriate handler class based on file extension and format detection. This skill ensures that polymorphic routing logic (e.g., .gz with index vs. without, .db, or standard mzML) produces the expected handler instances and integrates correctly with downstream readers.

## When to use

When implementing or refactoring a FileInterface._open method or similar polymorphic dispatcher that conditionally instantiates different handler classes based on file extension (e.g., .gz, .db) or format metadata (e.g., indexed gzip detection). Apply this skill to verify that the dispatch logic correctly routes each file type and that the instantiated handlers preserve file path and encoding parameters.

## When NOT to use

- Input is a single, pre-determined file format (e.g., you know all files are standard mzML); use a direct instantiation instead of conditional dispatch.
- File handler classes do not yet exist or their __init__ signatures are not finalized; defer testing until handler interface is stable.
- The dispatcher itself has not been implemented; write the dispatch logic first, then test it.

## Inputs

- File path string (extension-based: .mzML, .mzML.gz, .db)
- File object or mock file with format metadata (indexed gzip header detection)

## Outputs

- File handler instance (IndexedGzip, StandardGzip, SQLiteDatabase, or StandardMzml)
- Test pass/fail assertions for each conditional branch
- Integration test results confirming spectrum retrieval from dispatched handlers

## How to apply

First, design unit tests for each conditional branch: create or mock files of each supported type (.mzML, .mzML.gz with index, .mzML.gz without index, .db) and call the _open method with each. For each test, verify that the returned handler is an instance of the expected class (IndexedGzip, StandardGzip, SQLiteDatabase, or StandardMzml) and that the handler was initialized with the correct path and encoding. Second, write integration tests by passing the dispatched handlers to downstream Reader operations (e.g., spectrum retrieval via __getitem__ or iteration) to confirm correct spectrum access. Use assertions to check instance types and verify that handler-specific methods (read, __getitem__, get_spectrum_count) execute without error and return expected data types.

## Related tools

- **pymzML** (Provides the FileInterface._open dispatch mechanism and file handler classes (IndexedGzip, StandardGzip, StandardMzml, SQLiteDatabase) whose conditional instantiation is being tested.) — https://github.com/pymzml/pymzML
- **Python** (Language for writing unit and integration tests; provides unittest/pytest framework and isinstance assertions for handler verification.)
- **sqlite3** (Used in tests to verify SQLiteDatabase handler instantiation and spectrum retrieval when .db files are dispatched.)

## Examples

```
import unittest
from pymzml.FileInterface import FileInterface

class TestFileInterfaceDispatch(unittest.TestCase):
    def test_indexed_gzip_dispatch(self):
        handler = FileInterface._open('tests/data/BSA1.mzML.gz')
        self.assertIsInstance(handler, IndexedGzip)
    def test_standard_mzml_dispatch(self):
        handler = FileInterface._open('tests/data/sample.mzML')
        self.assertIsInstance(handler, StandardMzml)
    def test_sqlite_dispatch(self):
        handler = FileInterface._open('test.db')
        self.assertIsInstance(handler, SQLiteDatabase)
```

## Evaluation signals

- isinstance(returned_object, ExpectedHandlerClass) is True for each dispatch branch test.
- Dispatched handler's path and encoding attributes match the input file path and encoding passed to _open.
- Integration test successfully retrieves a spectrum via handler.__getitem__(spectrum_id) and verifies it is a valid spectrum object with expected keys (e.g., 'ms level').
- Iteration over dispatched handler (for spectrum in handler: ...) produces valid spectrum objects without exceptions.
- All conditional branches (indexed .gz, standard .gz, .db, standard mzML) have at least one unit test with a passing assertion.

## Limitations

- Test coverage depends on availability of real or correctly mocked test files (.mzML, .mzML.gz with and without index, .db). Mock files must accurately reflect format metadata (e.g., indexed gzip magic bytes).
- Integration tests require that downstream Reader operations are already implemented and stable; changes to Reader._open or spectrum access API will invalidate integration test expectations.
- Custom regex patterns for non-standard mzML index identifiers (e.g., 'scan=1' instead of integer indices) may require parameterized unit tests to cover each regex variant.
- SQLiteDatabase handler tests require a pre-populated database schema with a spectra table; schema mismatches will cause handler instantiation or spectrum retrieval to fail outside the scope of dispatch testing.

## Evidence

- [other] The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip, otherwise StandardGzip; for '.db' extensions it instantiates SQLiteDatabase; for all other paths it defaults to StandardMzml.: "The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip,"
- [other] Unit test each dispatch branch by calling _open with mock files of each type (.mzML, .mzML.gz with index, .mzML.gz without index, .db) and verify the returned handler is an instance of the expected class.: "Unit test each dispatch branch by calling _open with mock files of each type (.mzML, .mzML.gz with index, .mzML.gz without index, .db) and verify the returned handler is an instance of the expected"
- [other] Integration test by passing dispatched handlers to downstream Reader operations to confirm correct spectrum retrieval.: "Integration test by passing dispatched handlers to downstream Reader operations to confirm correct spectrum retrieval."
- [readme] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
