---
name: tabular-data-transformation-with-pandas
description: Use when when converting mwTab-formatted metabolomics files (containing MS/NMR tabular data blocks) to JSON, or when you need to extract, manipulate, and re-serialize tabular sections from mwTab files while maintaining column structure and type information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - pandas
  - jsonschema
  - mwtab
  - Python json module
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- The ``mwtab`` package is a Python library
- pandas_ for working with tabular data sections within the mwTab format
- pandas_ for working with tabular data sections within the mwTab format.
- jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema
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

# tabular-data-transformation-with-pandas

## Summary

Use pandas to handle and transform tabular data sections (e.g., METABOLITES, DATA blocks) within mwTab files during format conversion, preserving column names and data types. This skill enables reliable serialization of structured metabolomics data into JSON-compatible formats while maintaining data integrity.

## When to use

When converting mwTab-formatted metabolomics files (containing MS/NMR tabular data blocks) to JSON, or when you need to extract, manipulate, and re-serialize tabular sections from mwTab files while maintaining column structure and type information. Specifically apply this when your mwTab file contains METABOLITES, DATA, or other structured tabular blocks that must be preserved during cross-format conversion.

## When NOT to use

- Input is already in JSON format or has already been deserialized—no transformation step needed.
- Tabular sections contain binary or non-text data types incompatible with JSON encoding.
- Performance-critical pipelines on very large metabolomics datasets where pandas overhead is prohibitive; consider streaming or columnar formats instead.

## Inputs

- mwTab file (text format)
- MWTabFile object (parsed in-memory representation)
- mwTab tabular sections (METABOLITES, DATA blocks as pandas-compatible structures)

## Outputs

- pandas DataFrame(s) representing tabular sections
- JSON-serialized dictionary(ies) with preserved column names and data types
- JSON file with tabular data encoded in JSON-compatible format

## How to apply

Load the mwTab file using mwtab.fileio.read_files to instantiate an MWTabFile object representing parsed metadata and tabular sections. Use pandas DataFrames to represent each tabular section (METABOLITES, DATA blocks, etc.), leveraging pandas' built-in column and dtype preservation to maintain data integrity. Apply pandas operations (filtering, renaming, type casting) as needed for your transformation goal. Before serialization, validate that column names and data types have been preserved through inspection of DataFrame.dtypes and DataFrame.columns. Finally, convert the DataFrame to a JSON-compatible dictionary structure using pandas' to_dict() method with appropriate orient parameter, then serialize with Python's json module, ensuring proper encoding of nested structures.

## Related tools

- **mwtab** (Provides MWTabFile object and file I/O (read_files) to load and parse mwTab-formatted metabolomics files; output objects are then processed by pandas for tabular transformation) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Handles tabular data sections (METABOLITES, DATA blocks) during conversion, preserving column names and data types through DataFrame structures before JSON serialization)
- **Python json module** (Serializes transformed pandas DataFrames (converted to dictionaries) into JSON format with proper encoding of nested objects and arrays)
- **jsonschema** (Validates the converted JSON output against a JSON schema to confirm structural correctness after tabular transformation)

## Examples

```
import mwtab; import pandas as pd; mwfile = next(mwtab.read_files('1')); df = pd.DataFrame(mwfile['METABOLITES']); json_dict = df.to_dict(orient='records'); import json; json.dump(json_dict, open('metabolites.json', 'w'))
```

## Evaluation signals

- Verify all column names from the original mwTab tabular sections are present in the JSON output (compare via json.keys() or pandas DataFrame.columns).
- Confirm data types are preserved: numeric columns remain numeric (int, float), text columns remain strings; inspect DataFrame.dtypes before and after transformation.
- Validate JSON output against the jsonschema-defined schema to ensure structural correctness and no loss of tabular integrity.
- Compare row counts between the original mwTab section and the JSON output (len(DataFrame) should equal JSON array length).
- Spot-check a sample of values: verify that representative cells from the original mwTab match their JSON-serialized equivalents (accounting for type coercion).

## Limitations

- Column and data-type preservation depends on accurate mwTab parsing; malformed or non-standard mwTab files may result in incorrect DataFrame construction.
- JSON encoding has limitations on floating-point precision; very large or very precise numeric data (e.g., high-resolution MS m/z values) may lose precision in JSON serialization.
- pandas operations on very large metabolomics datasets (thousands of rows, hundreds of columns) can consume significant memory; no streaming alternative is described in the article.
- Non-text or binary metadata within mwTab files cannot be directly represented in JSON and may require custom encoding or omission.

## Evidence

- [other] Use the pandas library to handle tabular data sections (e.g., METABOLITES, DATA blocks) during conversion, preserving column names and data types.: "Use the pandas library to handle tabular data sections (e.g., METABOLITES, DATA blocks) during conversion, preserving column names and data types."
- [readme] The mwtab package provides facilities to convert mwTab formatted files into their equivalent JSONized representation and vice versa.: "The ``mwtab`` package provides facilities to convert ``mwTab`` formatted files into their equivalent ``JSON`` ized representation and vice versa."
- [other] Apply the converter module functions to traverse the MWTabFile object and transform metadata and tabular sections into JSON-compatible dictionary structures.: "Apply the converter module functions to traverse the MWTabFile object and transform metadata and tabular sections into JSON-compatible dictionary structures."
- [other] Serialize the converted dictionary structure to JSON format using Python's built-in json module, ensuring proper encoding of nested objects and arrays.: "Serialize the converted dictionary structure to JSON format using Python's built-in json module, ensuring proper encoding of nested objects and arrays."
- [other] Write the JSON output to a file with proper formatting and validation against the jsonschema-defined JSON schema to confirm structural correctness.: "Write the JSON output to a file with proper formatting and validation against the jsonschema-defined JSON schema to confirm structural correctness."
