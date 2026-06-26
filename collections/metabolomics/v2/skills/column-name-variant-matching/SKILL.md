---
name: column-name-variant-matching
description: Use when when processing mwTab metabolomics data files with variable
  column naming conventions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - mwtab
  - pandas
  techniques:
  - NMR
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

# column-name-variant-matching

## Summary

Matches metabolomics metadata column headers against lists of alternative column names and normalized variants using case-insensitive regex patterns to identify and standardize database-ID columns (e.g., m/z, HMDB_ID, PubChem_ID). This skill enables robust column discovery in heterogeneously formatted mwTab files where the same semantic column may appear under multiple naming conventions.

## When to use

When processing mwTab metabolomics data files with variable column naming conventions (e.g., 'm/z', 'moverz', 'mz' for mass-to-charge ratio), you need to identify and standardize database-ID columns (HMDB, PubChem, KEGG) prior to populating the ColumnFinder mechanism or merging with external metabolite reference databases. Apply this skill before ValueMatcher filtering to ensure semantic columns are correctly detected regardless of capitalization, spacing, or abbreviation style.

## When NOT to use

- Input column headers are already validated and standardized to a single canonical naming scheme — apply name matching only when heterogeneous naming is expected.
- You are matching on column values rather than column names — use ValueMatcher.series_match instead for database-ID format detection within a column's values.
- The mwTab file is missing the metadata section entirely — NameMatcher requires accessible column header dictionaries to operate.

## Inputs

- mwTab metadata column headers (dict or list of strings)
- NameMatcher lists of alternative column names and normalized variants
- metadata dictionary from MWTabFile instance

## Outputs

- Standardized column name mapping (dict: original_header → canonical_name)
- ColumnFinder dictionary with matched database-ID columns
- Boolean validation result (column found and normalized or not)

## How to apply

Construct a NameMatcher instance by defining lists of alternative column names for each semantic column (e.g., ['m/z', 'moverz', 'mz']) and normalized variants, then use the make_list_regex helper function to generate case-insensitive regex patterns from these lists. Apply the NameMatcher.dict_match method to the actual column headers from your mwTab metadata section, passing the dictionary of column names as input. The dict_match method performs column-name matching operations and returns matched columns standardized to the NameMatcher's canonical form. Pair the validated NameMatcher with a ValueMatcher (which enforces database-ID format constraints) and assemble both into a ColumnFinder instance keyed by the standard column name (e.g., 'HMDB_ID'). This two-stage approach (name matching followed by value matching) ensures both syntactic and semantic validation before accepting a column as identified.

## Related tools

- **mwtab** (Core library providing NameMatcher class, dict_match method, make_list_regex pattern generator, and MWTabFile data structure for reading mwTab metabolomics metadata) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Tabular data manipulation for accessing and transforming column headers and metadata dictionaries from mwTab sections)
- **Python** (Programming language runtime (3.6+) for executing NameMatcher logic and regex operations)

## Examples

```
from mwtab import NameMatcher, make_list_regex; nm = NameMatcher(make_list_regex(['m/z', 'moverz', 'mz']), 'm/z'); matched = nm.dict_match({'m/z': 0, 'intensity': 1, 'mZ': 2})
```

## Evaluation signals

- NameMatcher.dict_match returns matched headers for all expected column name variants (e.g., 'm/z', 'moverz', 'mz' all map to the same canonical column)
- Matched column is standardized to the NameMatcher's standard_name attribute and can be looked up in the ColumnFinder dictionary
- Case-insensitive matching works: 'M/Z', 'M/z', and 'm/z' all produce the same standardized output
- Unrelated column headers do not match (false-positive rate = 0 for adjacent or similarly-named non-matching columns)
- ColumnFinder assembly succeeds when NameMatcher output is paired with corresponding ValueMatcher (e.g., for 'HMDB_ID' column: name matched AND value format validates)

## Limitations

- NameMatcher operates only on column headers, not on cell values — columns with correct names but non-conformant database-ID values will pass name matching but may fail ValueMatcher validation.
- Regex patterns are case-insensitive but do not handle typos or phonetic variations (e.g., 'mz' matches but 'mass_charge' does not).
- The make_list_regex function requires explicit enumeration of all expected variants; novel or domain-specific naming conventions not in the variant list will not be detected.
- No changelog is available in the repository, so regression or breaking changes in NameMatcher behavior across mwtab versions may not be documented.

## Evidence

- [other] NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values, with both matcher types employed together in the ColumnFinder mechanism to populate the column_finders dictionary for database-ID columns such as PubChem/KEGG/HMDB.: "NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values, with both matcher types employed together in"
- [other] Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns.: "Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns"
- [other] All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match.: "All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match"
- [other] Validate NameMatcher.dict_match method on test metabolite metadata column headers to confirm pattern matching.: "Validate NameMatcher.dict_match method on test metabolite metadata column headers to confirm pattern matching"
- [readme] The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data.: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
