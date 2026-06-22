---
name: prefix-stripping-and-case-standardization
description: Use when valueMatcher.series_match has detected database-ID values (HMDB IDs, PubChem CIDs, KEGG compound identifiers) in raw metabolite metadata columns and you need to normalize them into a canonical form for storage in standardized database-ID columns (e.g., HMDB_ID, PubChem_ID, KEGG_ID).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - mwtab
  - pandas
  - Python re module
  techniques:
  - mass-spectrometry
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

# Prefix-stripping and case standardization

## Summary

Normalize database-ID values by removing optional prefixes (e.g., 'HMDB', 'PubChem') and standardizing character case to enable consistent matching and storage in metabolomics metadata. This is a critical preprocessing step within the ColumnFinder mechanism of mwtab that validates and prepares detected database-ID values for population into standardized mwTab columns.

## When to use

Apply this skill when ValueMatcher.series_match has detected database-ID values (HMDB IDs, PubChem CIDs, KEGG compound identifiers) in raw metabolite metadata columns and you need to normalize them into a canonical form for storage in standardized database-ID columns (e.g., HMDB_ID, PubChem_ID, KEGG_ID). Specifically, use this step after value pattern matching has confirmed format compliance but before populating the mwTab file structure.

## When NOT to use

- Input values are already validated and stored in the standard mwTab column format (e.g., already in HMDB_ID column)—normalization is redundant.
- The source data contains database IDs from custom or non-standard databases not covered by the ColumnFinder definition—apply custom prefix/case rules instead.
- The input is a raw string header name rather than column values—use NameMatcher.dict_match for column-name matching instead.

## Inputs

- pandas Series of raw database-ID values with optional prefixes and mixed case (e.g., raw column from metabolite metadata)
- Regular expression pattern defining the expected database-ID format with optional prefix capture group
- Standard prefix string(s) to strip (e.g., 'HMDB', 'PubChem')

## Outputs

- pandas Series of normalized database-ID values with prefixes removed and case standardized
- Mapping or record of transformations applied (prefix stripped, case changed) for validation and traceability

## How to apply

After ValueMatcher.series_match identifies a database-ID value using modular regular expressions (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case), extract and strip the optional prefix (if present) using regex capture groups or string methods, then convert the remaining alphanumeric identifier to a canonical case form (typically uppercase for HMDB and KEGG, numeric-only for PubChem CID). The rationale is that source metabolite metadata often contains inconsistently formatted database IDs—some prefixed ('HMDB0000001'), some not ('0000001')—and mixed case variants ('hmdb', 'HMDB', 'Hmdb'). Normalizing to the standard form ensures that the ColumnFinder can reliably populate the standardized columns and that subsequent data validation and curation steps operate on consistent identifiers. Validate the transformation by confirming that the normalized value still matches the expected format and that no information is lost.

## Related tools

- **mwtab** (Provides ValueMatcher class and series_match method for database-ID format detection; encapsulates prefix-stripping and case-standardization logic within ColumnFinder mechanism for mwTab file population) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Supplies Series data structure and string methods (str.replace, str.upper, str.lower, str.extract) for efficient column-wise prefix and case transformations)
- **Python re module** (Provides regular expression pattern matching and capture groups to identify and extract database-ID components after prefix removal)

## Examples

```
from mwtab import ValueMatcher; import re; vm = ValueMatcher(regex=r'(HMDB)?0{0,4}\d{4,7}', case_standardization='upper'); normalized = vm.series_match(raw_hmdb_column, standardize=True)
```

## Evaluation signals

- All normalized values match the regex pattern defined for the standard database-ID column (e.g., HMDB pattern '(HMDB)?0{0,4}\d{4,7}' matches normalized output)
- No values retain optional prefixes after transformation (e.g., 'HMDB0000001' → '0000001', 'hmdb123' → '123')
- Case standardization is applied uniformly (e.g., all HMDB IDs uppercase, all KEGG IDs uppercase and prefixed with 'C')
- Series length and non-null count remain unchanged; no rows are dropped during normalization
- Diff comparison between raw input and normalized output shows only prefix removal and case changes; no digits or core identifier content is altered

## Limitations

- Prefix-stripping assumes prefixes are optional and separable from the core identifier; if prefix is fused or ambiguous (e.g., 'ID123' where 'ID' may or may not be a prefix), false positives or false negatives may occur.
- Case standardization relies on a predefined canonical form for each database; if the standard shifts (e.g., HMDB moves to lowercase) or if multiple standards coexist in the same dataset, conflicts may arise.
- Values that do not conform to the expected database-ID format after prefix stripping are not recovered; they may be dropped or flagged as validation failures by downstream schema checks.
- No changelog or version history is available for the mwtab library, making it difficult to track whether prefix-stripping rules have changed across releases.

## Evidence

- [other] ValueMatcher uses modular regular expressions for database-ID value formats with optional prefix handling: "Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers)."
- [other] Validation includes format detection and normalization of database-ID values, such as stripping prefixes and standardizing case: "Validate ValueMatcher.series_match method on test database-ID values to confirm format detection and normalization (e.g., stripping prefixes, standardizing case)."
- [other] ColumnFinder pairs NameMatcher and ValueMatcher to populate database-ID columns: "Create ColumnFinder instances for each standard database-ID column (e.g., 'HMDB_ID', 'PubChem_ID', 'KEGG_ID') pairing a NameMatcher and ValueMatcher with the standard_name attribute."
- [readme] The mwtab package facilitates reading and writing mwTab format files used by Metabolomics Workbench: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
