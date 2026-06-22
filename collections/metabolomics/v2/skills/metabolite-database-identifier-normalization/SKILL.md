---
name: metabolite-database-identifier-normalization
description: Use when you have metabolomics metadata in mwTab or tabular format with column headers and values that may contain database identifiers (e.g., HMDB IDs, PubChem CIDs, KEGG compound IDs) in heterogeneous or non-canonical formats (mixed case, optional prefixes, variable naming conventions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - mwtab
  - pandas
  - Python 3.6+
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
---

# metabolite-database-identifier-normalization

## Summary

Identify and normalize database-identifier columns (HMDB, PubChem, KEGG) in metabolomics metadata by combining regex-based name matching on column headers with format-specific value pattern matching, then standardize identifiers by stripping prefixes and normalizing case. This ensures consistent, canonical representation of metabolite cross-references across mwTab files prior to deposition or curation.

## When to use

You have metabolomics metadata in mwTab or tabular format with column headers and values that may contain database identifiers (e.g., HMDB IDs, PubChem CIDs, KEGG compound IDs) in heterogeneous or non-canonical formats (mixed case, optional prefixes, variable naming conventions). Use this skill when you need to populate and standardize a column_finders dictionary to automatically detect and normalize these identifiers across multiple files or before validating against Metabolomics Workbench schema.

## When NOT to use

- Input metadata contains no structured database identifiers (e.g., only chemical names or formulae).
- Column headers and values are already in canonical, vendor-controlled format (e.g., official HMDB export tables with guaranteed uniform 'HMDB_ID' naming and 'HMDB' prefixes).
- The metabolomics study uses only in-house or non-standard compound identifiers with no cross-reference to public databases.

## Inputs

- pandas DataFrame column headers (list of strings)
- pandas Series of database-identifier values (strings or mixed types)
- list of alternative column name variants per database (list of lists of strings)
- modular regex pattern strings for database-ID formats (e.g., HMDB7-digit pattern)

## Outputs

- standardized database-identifier Series (normalized case, prefixes stripped)
- column_finders dictionary mapping standard names to ColumnFinder instances
- boolean Series or mask indicating which values matched the ValueMatcher pattern
- dict mapping detected column indices to their canonical standard_name

## How to apply

First, construct a NameMatcher for each target database-ID column by defining a list of alternative column names (e.g., 'HMDB_ID', 'HMDB ID', 'hmdb') and using make_list_regex to create a case-insensitive regex pattern. Second, construct a ValueMatcher with modular regex patterns for the expected database-ID format (e.g., HMDB IDs as 'HMDB[0-9]{7}' or optional 'HMDB' prefix with 7 digits in mixed case). Third, pair each NameMatcher and ValueMatcher as a ColumnFinder instance with the standard_name attribute set to the canonical column name. Fourth, assemble these ColumnFinder instances into a column_finders dictionary keyed by standardized names. Fifth, apply NameMatcher.dict_match to test column headers against the assembled dictionary to identify matching columns. Sixth, apply ValueMatcher.series_match to the identified column values to validate format conformance and extract or normalize identifiers (stripping prefixes, standardizing case) into canonical form. The rationale is that NameMatcher handles the syntactic variability of column naming while ValueMatcher enforces semantic conformance to database-ID syntax, together ensuring both detection and standardization.

## Related tools

- **mwtab** (Python library providing ColumnFinder, NameMatcher, ValueMatcher, and make_list_regex utilities for constructing and applying regex-based column and value matchers to mwTab file metadata) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (tabular data manipulation library used to represent column headers as dictionaries and values as Series for matching operations)
- **Python 3.6+** (runtime environment for mwtab and regex-based matching logic)

## Examples

```
# Construct NameMatcher for HMDB_ID with alternative names, then ColumnFinder paired with ValueMatcher
from mwtab.utils.column_finders import NameMatcher, ValueMatcher, ColumnFinder
hmdb_names = NameMatcher(['HMDB_ID', 'HMDB ID', 'hmdb'])
hmdb_values = ValueMatcher('(?:HMDB)?[0-9]{7}')
hmdb_finder = ColumnFinder(hmdb_names, hmdb_values, standard_name='HMDB_ID')
column_finders = {'HMDB_ID': hmdb_finder}
# Apply to test headers and values
matched_col = hmdb_names.dict_match({'HMDB ID': 0, 'Name': 1})
normalized = hmdb_values.series_match(df['HMDB ID'])
```

## Evaluation signals

- NameMatcher.dict_match successfully identifies all columns with alternative names in test metabolite metadata (e.g., 'HMDB_ID', 'hmdb id', 'HMDB' all map to canonical 'HMDB_ID').
- ValueMatcher.series_match returns 100% true positives on a known-good metabolite identifier Series and correctly rejects malformed identifiers (e.g., HMDB IDs with incorrect digit count or missing leading zeros).
- Normalized identifiers conform to canonical format: HMDB IDs are 'HMDB[0-9]{7}' (7 digits, uppercase prefix), PubChem CIDs are numeric only, KEGG IDs match official KEGG compound naming (e.g., 'C00001').
- column_finders dictionary keys match expected standard names and each ColumnFinder instance has both a valid NameMatcher and ValueMatcher populated.
- Round-trip validation: identifiers normalized via ValueMatcher.series_match can be re-matched by the same pattern without loss or case drift.

## Limitations

- NameMatcher and ValueMatcher are regex-based and rely on consistent, well-defined naming and format conventions; highly irregular or misspelled column headers or malformed identifiers may not be detected.
- make_list_regex case-insensitivity applies only to ASCII; Unicode or locale-specific case variants may not be normalized correctly.
- ValueMatcher patterns must be manually constructed and maintained for each database (HMDB, PubChem, KEGG); changes to database ID formats or new databases require explicit pattern updates.
- The skill does not validate biological plausibility or check for duplicate/conflicting identifiers across matched columns; it assumes input identifiers are semantically correct.

## Evidence

- [other] NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values: "NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values"
- [other] All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match.: "All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match."
- [other] All ValueMatcher attributes are strings and all are used in its only method, series_match.: "All ValueMatcher attributes are strings and all are used in its only method, series_match."
- [other] Define NameMatcher with lists of alternative column names and normalized variants using make_list_regex to construct case-insensitive patterns.: "Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns."
- [other] Define ValueMatcher with modular regular expressions for database-ID value formats for HMDB, PubChem, KEGG.: "Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers)."
- [other] Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case).: "Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case)."
- [readme] The mwtab package facilitates reading and writing files in mwTab format used by the Metabolomics Workbench for archival of Mass Spectrometry and Nuclear Magnetic Resonance experimental data.: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
