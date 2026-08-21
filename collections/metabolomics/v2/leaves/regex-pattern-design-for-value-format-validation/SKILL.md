---
name: regex-pattern-design-for-value-format-validation
description: Use when when you have a metabolomics metadata table and need to automatically
  identify and standardize database-ID columns (HMDB_ID, PubChem_ID, KEGG_ID, etc.)
  whose values follow known format conventions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0002
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - mwtab
  - pandas
  - Python re module
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regex-pattern-design-for-value-format-validation

## Summary

Design and apply modular regular expressions to detect and normalize database-ID value formats (e.g., HMDB, PubChem, KEGG identifiers) in metabolomics metadata columns. This skill enables ValueMatcher to validate that column values conform to expected format patterns and optionally strip prefixes or normalize case during matching.

## When to use

When you have a metabolomics metadata table and need to automatically identify and standardize database-ID columns (HMDB_ID, PubChem_ID, KEGG_ID, etc.) whose values follow known format conventions. Apply this skill when column names alone are ambiguous or missing, but the actual values in the column—such as 'HMDB0000001', 'hmdb0000001', 'CID12345', or 'C00001'—reveal the column's identity through their format signature.

## When NOT to use

- Input column contains free-text descriptions or chemical names rather than structured database identifiers; regex-based value matching will produce false positives.
- Column format is already standardized and validated (e.g., already populated in an mwTab file with confirmed HMDB IDs); applying ValueMatcher would be redundant.
- Database-ID formats are unknown or highly variable across experimental studies, making it impractical to define precise modular regex patterns.

## Inputs

- pandas.Series (column of potential database-ID values)
- Metabolomics metadata table column (mwTab or tabular format)

## Outputs

- List of matched database-ID values (normalized and validated)
- ValueMatcher.series_match method result (matched indices and normalized values)
- Assembled ColumnFinder instances mapping standard column names to (NameMatcher, ValueMatcher) pairs

## How to apply

First, decompose each database-ID format into its constituent patterns: HMDB IDs have an optional case-insensitive 'HMDB' prefix followed by 7 digits (e.g., 'HMDB0000001'); PubChem CIDs are numeric (e.g., '12345'); KEGG compound IDs follow 'C' plus 5 digits (e.g., 'C00001'). Construct modular regular expressions for each format using Python's `re` module, allowing optional prefixes and flexible case handling. Encode these patterns as attributes of a ValueMatcher class, then invoke its `series_match` method on a pandas Series to test each value against the regex; the method returns matches with optional normalization (e.g., prefix stripping, case standardization). Validate successful matches by spot-checking that detected values align with the expected format and that prefix/case transformations produce canonical identifiers ready for database lookup.

## Related tools

- **mwtab** (Python library providing ValueMatcher class and series_match method for applying regex patterns to metabolomics metadata columns) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (DataFrame and Series objects for holding and iterating over metabolomics metadata columns)
- **Python re module** (Standard library for constructing and compiling regular expressions for database-ID format matching)

## Examples

```
from mwtab.matching import ValueMatcher; import pandas as pd; hmdb_matcher = ValueMatcher(regex=r'^(?:hmdb)?\d{7}$'); series = pd.Series(['HMDB0000001', 'hmdb0000002', '0000003']); matches = hmdb_matcher.series_match(series)
```

## Evaluation signals

- All returned values match their expected database-ID format pattern (e.g., HMDB values have 'HMDB' prefix or digits-only form, no spurious characters).
- Normalization produces consistent canonical form (e.g., all HMDB IDs in output are lowercase with numeric suffix, no mixed case or prefix variants).
- series_match method returns match indices that correspond to rows in the original metabolomics table, enabling downstream column assignment.
- Spot-check a random sample of 5–10 matched values by querying them against the actual HMDB/PubChem/KEGG API or local database to confirm they resolve to metabolite records.
- ValueMatcher.series_match coverage: at least 80% of rows in a known-good column (e.g., a gold-standard HMDB_ID column) are detected and matched.

## Limitations

- Regex patterns are rigid and brittle; any deviation from the expected format (e.g., extra whitespace, unexpected characters, prefix variants not explicitly allowed) will cause matches to fail silently.
- No built-in mechanism to resolve conflicting matches if a value could belong to multiple database-ID formats (e.g., a numeric string that is both a valid PubChem CID and a KEGG ID segment).
- Regex validation confirms format only; it does not verify that a matched ID actually exists in the target database or maps to a real metabolite.
- Case sensitivity and prefix variations must be explicitly encoded in the regex; the article indicates 'optional HMDB prefix in mixed case', but implementation must handle all observed case/prefix combinations.

## Evidence

- [other] Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers).: "Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers)."
- [other] All ValueMatcher attributes are strings and all are used in its only method, series_match.: "All ValueMatcher attributes are strings and all are used in its only method, series_match."
- [other] Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case).: "Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case)."
- [other] ValueMatcher uses its series_match method to match column values, with both matcher types employed together in the ColumnFinder mechanism to populate the column_finders dictionary for database-ID columns such as PubChem/KEGG/HMDB.: "ValueMatcher uses its series_match method to match column values, with both matcher types employed together in the ColumnFinder mechanism to populate the column_finders dictionary for database-ID"
