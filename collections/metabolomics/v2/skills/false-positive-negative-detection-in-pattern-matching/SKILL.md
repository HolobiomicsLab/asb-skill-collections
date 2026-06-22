---
name: false-positive-negative-detection-in-pattern-matching
description: Use when when reconstructing or validating the ColumnFinder component in mwtab, you need to assess whether the combined NameMatcher.dict_match and ValueMatcher.series_match operations are correctly populating database-ID columns. Apply this skill after defining NameMatcher patterns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - Python
  - mwtab
  - pandas
  - Python regular expressions (re module)
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- The ``mwtab`` package is a Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# false-positive-negative-detection-in-pattern-matching

## Summary

Detect and validate true matches versus false positives and false negatives when using NameMatcher and ValueMatcher patterns to identify metabolomics database-ID columns in mwTab metabolite metadata. This skill ensures that column name and value patterns correctly identify standardized database identifiers (HMDB, PubChem, KEGG) without spurious matches or missing valid columns.

## When to use

When reconstructing or validating the ColumnFinder component in mwtab, you need to assess whether the combined NameMatcher.dict_match and ValueMatcher.series_match operations are correctly populating database-ID columns. Apply this skill after defining NameMatcher patterns (e.g., alternative names like 'm/z', 'moverz', 'mz') and ValueMatcher regular expressions (e.g., HMDB ID formats with optional 'HMDB' prefix, PubChem CID numeric patterns), to confirm that both matchers' outputs align with the expected standardized column names and that no valid identifiers are missed or misclassified.

## When NOT to use

- If metabolite metadata column headers are already standardized and verified to conform to mwTab schema — apply this skill during initial curation or when column naming conventions are uncertain.
- If database-ID values are already normalized and validated in the input mwTab file — this skill targets raw or semi-curated metadata where pattern matching is the disambiguation step.
- If you are only reading a pre-curated mwTab file without modifying or reconstructing ColumnFinder logic — validation is unnecessary if the file has passed prior curation.

## Inputs

- Test metabolite metadata column headers (list of strings)
- Test database-ID values (pandas Series or list, e.g., HMDB IDs, PubChem CIDs, KEGG compound IDs)
- NameMatcher instance with lists of alternative column names and normalized variants
- ValueMatcher instance with modular regular expressions for database-ID formats
- ColumnFinder instances configured with standard_name attributes

## Outputs

- Validated NameMatcher.dict_match results (dict mapping test headers to matched standard names or None)
- Validated ValueMatcher.series_match results (Series or dict with matched database IDs and normalized formats)
- Populated column_finders dictionary with standardized column names as keys and ColumnFinder instances as values
- Report of false positives (name/value patterns matching incorrectly) and false negatives (valid identifiers not matched)
- Confirmation that ColumnFinder correctly identifies and standardizes database-ID columns

## How to apply

Perform two-stage validation: (1) **Name matching**: Apply NameMatcher.dict_match to test metabolite metadata column headers and verify that the returned matches correspond exactly to the intended standard_name (e.g., 'HMDB_ID', 'PubChem_ID', 'KEGG_ID'), checking that case-insensitive patterns constructed via make_list_regex do not over-match unrelated columns. (2) **Value matching**: Apply ValueMatcher.series_match to test database-ID value samples and confirm that format detection correctly identifies valid identifiers (e.g., stripping optional 'HMDB' prefix in mixed case, recognizing PubChem numeric CIDs, parsing KEGG compound identifiers) while rejecting non-conformant values. (3) **Integration**: Verify that ColumnFinder instances pair matching NameMatcher and ValueMatcher such that when both the column name and a sample of column values pass their respective matchers, the column is flagged for the corresponding database-ID standard_name. Document any edge cases (e.g., columns with names matching the pattern but values that fail, or vice versa) as potential false positives or false negatives.

## Related tools

- **mwtab** (Python library providing NameMatcher, ValueMatcher, and ColumnFinder classes for metabolomics metadata column identification and normalization) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Used to work with tabular metabolite metadata sections (DataFrames) and apply series_match operations on database-ID value columns)
- **Python regular expressions (re module)** (Underlying engine for ValueMatcher regex patterns and make_list_regex construction of case-insensitive column-name patterns)

## Examples

```
from mwtab import NameMatcher, ValueMatcher, ColumnFinder; nm = NameMatcher(['HMDB_ID', 'hmdb', 'hmdb_id']); vm = ValueMatcher(r'^(HMDB)?\d+$'); cf = ColumnFinder(nm, vm, 'HMDB_ID'); test_headers = {'HMDB_ID': True, 'hmdb': True, 'sample': False}; for h in test_headers: assert (cf.name_matcher.dict_match({h: 1}) is not None) == test_headers[h]
```

## Evaluation signals

- NameMatcher.dict_match returns only the correct standard_name for each test header; unrelated column names (e.g., 'sample_id', 'instrument') do not match patterns intended for 'HMDB_ID'.
- ValueMatcher.series_match successfully identifies and normalizes valid database IDs (e.g., 'HMDB0000001' and 'HMDB0001' parsed as equivalent; PubChem '12345' recognized as CID) and rejects invalid formats (e.g., malformed KEGG IDs, non-numeric PubChem strings).
- Column_finders dictionary contains no spurious entries: every key corresponds to a standard_name that genuinely appears in the test metadata with both matching column name and matching values.
- Recall check: all test columns containing valid database IDs are correctly identified and added to column_finders with the appropriate standard_name; no valid ID columns are missed.
- Edge cases documented: columns with matching names but non-conformant values (or vice versa) are clearly logged, indicating whether the ColumnFinder correctly handles partial matches or rejects them.

## Limitations

- Pattern matching relies on predefined alternative column name lists and regex formats; novel or misspelled database-ID column names or value formats not in the patterns will not be detected (false negatives).
- Case-insensitive matching via make_list_regex may over-match if alternative name lists contain common substrings; careful curation of the lists is required to minimize false positives.
- ValueMatcher regex patterns must be kept modular and comprehensive; if database-ID format specifications evolve (e.g., HMDB IDs gain new prefix conventions), patterns must be updated manually.
- No automatic learning or adaptive refinement: the ColumnFinder validation is static and does not update patterns based on observed mismatches; curation requires manual revision of NameMatcher and ValueMatcher configurations.

## Evidence

- [other] NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values, with both matcher types employed together in the ColumnFinder mechanism to populate the column_finders dictionary for database-ID columns such as PubChem/KEGG/HMDB.: "NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values, with both matcher types employed together in"
- [other] Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns.: "Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns"
- [other] Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers).: "Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers)"
- [other] Validate NameMatcher.dict_match method on test metabolite metadata column headers to confirm pattern matching.: "Validate NameMatcher.dict_match method on test metabolite metadata column headers to confirm pattern matching"
- [other] Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case).: "Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case)"
