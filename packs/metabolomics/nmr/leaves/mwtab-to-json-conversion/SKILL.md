---
name: mwtab-to-json-conversion
description: Use when you have mwTab-formatted files from the Metabolomics Workbench containing MS or NMR experimental metadata and data blocks that need to be converted to JSON for integration with REST APIs, web applications, or downstream tools that expect JSON input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mwtab
  - Python
  - jsonschema
  - pandas
  - Python json module
  techniques:
  - NMR
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- The ``mwtab`` package is a Python library that facilitates reading and writing files in
- The ``mwtab`` package is a Python library
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mwtab-to-json-conversion

## Summary

Convert mwTab-formatted files (used by the Metabolomics Workbench for MS and NMR experimental data archival) into equivalent JSON representations and vice versa. This skill enables interoperability between the mwTab format and JSON by traversing parsed mwTab objects, transforming metadata and tabular sections into JSON-compatible structures, and validating output against a jsonschema-defined schema.

## When to use

Use this skill when you have mwTab-formatted files from the Metabolomics Workbench containing MS or NMR experimental metadata and data blocks that need to be converted to JSON for integration with REST APIs, web applications, or downstream tools that expect JSON input. Also apply when converting JSON representations back to mwTab format for deposition or archival.

## When NOT to use

- Input data is already in JSON format and schema validation is the only goal (use jsonschema directly)
- mwTab files are malformed or lack required metadata sections that cannot be parsed by mwtab.fileio.read_files()
- Conversion is needed for file formats other than mwTab or JSON (e.g., mzML, NetCDF)

## Inputs

- mwTab-formatted text file (from Metabolomics Workbench)
- MWTabFile object (in-memory parsed representation)
- JSON file (for reverse conversion)

## Outputs

- JSON file with equivalent representation of mwTab data
- mwTab-formatted file (from JSON source)
- Validation report (schema conformance)

## How to apply

Load the mwTab file using mwtab.fileio.read_files() to parse the text-based mwTab structure into an in-memory MWTabFile object. Traverse the MWTabFile object's metadata sections (e.g., study identifiers, analysis parameters) and tabular data blocks (e.g., METABOLITES, DATA sections) using pandas for handling columnar data while preserving column names and data types. Transform the hierarchical object structure into JSON-compatible nested dictionaries and arrays. Serialize the converted dictionary to JSON using Python's json module with proper formatting. Validate the resulting JSON structure against the mwTab jsonschema definition to confirm that all required fields, data types, and structural constraints are satisfied before writing to file.

## Related tools

- **mwtab** (Core library providing MWTabFile class, file I/O functions, and converter module for transforming between mwTab and JSON formats) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Handles parsing and conversion of tabular data sections (e.g., METABOLITES, DATA blocks) during mwTab-to-JSON transformation, preserving column names and data types)
- **jsonschema** (Validates converted JSON structures against the mwTab-defined JSON schema to confirm structural correctness and required field presence)
- **Python json module** (Serializes converted dictionary structures to JSON format with proper encoding of nested objects and arrays)

## Examples

```
for mwfile in mwtab.read_files("1", "2"):
    json_dict = mwtab.mwtab.MWTabFile_to_dict(mwfile)
    with open(f"{mwfile.analysis_id}.json", "w") as f:
        json.dump(json_dict, f, indent=2)
    jsonschema.validate(instance=json_dict, schema=mwtab.schema)
```

## Evaluation signals

- JSON output conforms to mwTab jsonschema definition (zero validation errors reported by jsonschema validator)
- All metadata fields from the input mwTab file are present in the JSON output with correct data types and hierarchical nesting
- Tabular data sections preserve row and column counts, column names, and numeric precision when converted via pandas
- Round-trip conversion (mwTab → JSON → mwTab) produces structurally equivalent files with no loss of metadata or data
- JSON output is parseable and human-readable with proper indentation and no encoding errors

## Limitations

- Conversion relies on mwtab.fileio.read_files() successfully parsing the input mwTab file; malformed or non-standard mwTab files will fail to load
- pandas data type inference during tabular section conversion may require manual type specification for edge cases (e.g., leading zeros, ambiguous numeric formats)
- No changelog is available in the repository, making it difficult to track breaking changes or conversion behavior modifications across versions
- Round-trip fidelity (JSON → mwTab → JSON) may differ from forward conversion if the mwTab format includes format-specific directives or comments not preserved in JSON

## Evidence

- [readme] The mwtab package provides facilities to convert mwTab formatted files into their equivalent JSONized representation and vice versa.: "The ``mwtab`` package provides facilities to convert ``mwTab`` formatted files into their equivalent ``JSON`` ized representation and vice versa."
- [other] mwtab transforms metadata and tabular sections into JSON-compatible structures using converter module traversal.: "Apply the converter module functions to traverse the MWTabFile object and transform metadata and tabular sections into JSON-compatible dictionary structures."
- [other] pandas is used to handle tabular data sections during conversion, preserving column names and data types.: "Use the pandas library to handle tabular data sections (e.g., METABOLITES, DATA blocks) during conversion, preserving column names and data types."
- [other] JSON output is validated against jsonschema-defined schema to confirm structural correctness.: "Write the JSON output to a file with proper formatting and validation against the jsonschema-defined JSON schema to confirm structural correctness."
- [readme] mwTab format is used by the Metabolomics Workbench for archival of MS and NMR experimental data.: "files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data"
