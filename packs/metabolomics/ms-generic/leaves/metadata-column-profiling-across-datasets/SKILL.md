---
name: metadata-column-profiling-across-datasets
description: Use when you are curating metabolomics datasets with variable column
  naming conventions and need to detect, normalize, and populate standardized database-ID
  columns (HMDB_ID, PubChem_ID, KEGG_ID, etc.) across many mwTab files before deposition.
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
  - Python 3.6+
  techniques:
  - mass-spectrometry
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

# metadata-column-profiling-across-datasets

## Summary

Systematically identify and standardize database-ID columns (e.g., HMDB, PubChem, KEGG) across heterogeneous metabolomics datasets by combining name-based pattern matching on column headers with value-format validation on column entries. This enables harmonized curation and deposition of metabolite annotations to the Metabolomics Workbench.

## When to use

You are curating metabolomics datasets with variable column naming conventions and need to detect, normalize, and populate standardized database-ID columns (HMDB_ID, PubChem_ID, KEGG_ID, etc.) across many mwTab files before deposition. Use this skill when column headers are heterogeneous (e.g., 'm/z', 'moverz', 'mz' for the same semantic field) and when values require format-based validation (e.g., distinguishing HMDB IDs from free-text descriptions by regex pattern).

## When NOT to use

- Input is a pre-curated dataset where all database-ID columns already follow a single, uniform naming and formatting standard across all files.
- Database-ID values in the dataset are unstructured free-text descriptions with no consistent pattern or prefix (e.g., user-written notes) — regex-based ValueMatcher will not reliably extract them.
- You need to infer metabolite identity de novo from mass or spectral data rather than normalize existing database-ID annotations.

## Inputs

- mwTab format file with metabolite metadata section (column headers and rows)
- lists of alternative column name variants for each database ID type (e.g., HMDB, PubChem, KEGG)
- modular regular expressions for database-ID value formats
- pandas DataFrame or tabular data extracted from mwTab file

## Outputs

- column_finders dictionary with standardized column names as keys and ColumnFinder instances as values
- populated and normalized database-ID columns in the mwTab file
- validation report indicating which columns matched and which values were successfully formatted/normalized
- mwTab file with standardized database-ID column structure ready for deposition

## How to apply

Construct a ColumnFinder registry by defining paired NameMatcher and ValueMatcher objects for each target database-ID column. For each ColumnFinder: (1) define a NameMatcher with lists of alternative column names and normalized variants using make_list_regex to create case-insensitive regex patterns; (2) define a ValueMatcher with modular regular expressions encoding the expected format of database-ID values (e.g., 'HMDB' prefix in mixed case, numeric PubChem CID patterns, KEGG compound identifiers); (3) validate the NameMatcher.dict_match method on test metabolite metadata headers to confirm pattern matching; (4) validate the ValueMatcher.series_match method on test database-ID values to confirm format detection and any normalization (e.g., stripping prefixes, standardizing case). Assemble all ColumnFinder instances into a column_finders dictionary keyed by standardized column name, then apply it to each dataset's column headers and values in sequence.

## Related tools

- **mwtab** (Python library providing MWTabFile class for reading/writing mwTab format, housing ColumnFinder, NameMatcher, and ValueMatcher classes; provides pandas DataFrame access to metadata sections for column matching) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Tabular data manipulation; series_match method operates on pandas Series objects to validate and normalize database-ID values across rows)
- **Python 3.6+** (Runtime environment for mwtab and regex pattern compilation via make_list_regex)

## Examples

```
from mwtab.column_finders import NameMatcher, ValueMatcher, ColumnFinder; nm_hmdb = NameMatcher(['HMDB', 'hmdb_id']); vm_hmdb = ValueMatcher(r'^[Hh][Mm][Dd][Bb]\d{7}$'); cf_hmdb = ColumnFinder(nm_hmdb, vm_hmdb, 'HMDB_ID'); column_finders = {'HMDB_ID': cf_hmdb}; matches = cf_hmdb.name_matcher.dict_match(mwfile.metadata.columns); normalized_values = cf_hmdb.value_matcher.series_match(mwfile.metadata[matches[0]])
```

## Evaluation signals

- NameMatcher.dict_match successfully identifies all expected column variants (e.g., 'm/z', 'moverz', 'mz') in test headers with no false negatives
- ValueMatcher.series_match correctly validates format of known-good database-ID values (true positives) and rejects malformed entries (true negatives); check consistency of prefix stripping and case normalization
- column_finders dictionary contains exactly one ColumnFinder per standardized database-ID column name (HMDB_ID, PubChem_ID, KEGG_ID, etc.); no duplicate or missing keys
- After applying ColumnFinder across a batch of mwTab files, each file's metadata section has standardized database-ID columns populated and normalized; inspect a sample of values to confirm formatting is uniform (e.g., no leading/trailing whitespace, consistent case, prefixes removed if applicable)
- Validation report shows consistent match rates across similar files; sharp drop in matches for a file indicates potential schema drift or format anomaly requiring manual review

## Limitations

- NameMatcher and ValueMatcher rely on pre-defined patterns; if a dataset uses a novel column name or database-ID format not in the make_list_regex dictionary or regex, the column will be missed.
- ValueMatcher.series_match cannot distinguish between valid IDs and incidental matches of the regex pattern in free-text fields; manual curation is needed if value semantics are ambiguous.
- The skill assumes metabolite metadata are organized as tabular rows in mwTab files; it does not handle nested or hierarchical metadata structures.
- No changelog was found in the mwtab repository, making it difficult to track how ColumnFinder behavior may have evolved or whether edge cases in pattern matching have been documented.

## Evidence

- [other] how ColumnFinder logic combines NameMatcher and ValueMatcher: "NameMatcher uses its dict_match method to perform column-name matching operations, while ValueMatcher uses its series_match method to match column values, with both matcher types employed together in"
- [other] NameMatcher construction with regex patterns: "Define NameMatcher with lists of alternative column names and normalized variants (e.g., 'm/z', 'moverz', 'mz') using make_list_regex to construct case-insensitive patterns."
- [other] ValueMatcher construction with database-ID patterns: "Define ValueMatcher with modular regular expressions for database-ID value formats (e.g., HMDB IDs with optional 'HMDB' prefix in mixed case, PubChem CID numeric patterns, KEGG compound identifiers)."
- [other] ColumnFinder assembly and validation workflow: "Create ColumnFinder instances for each standard database-ID column (e.g., 'HMDB_ID', 'PubChem_ID', 'KEGG_ID') pairing a NameMatcher and ValueMatcher with the standard_name attribute. Assemble"
- [intro] mwtab as platform for this skill: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
- [other] pandas role in value matching: "All ValueMatcher attributes are strings and all are used in its only method, series_match."
