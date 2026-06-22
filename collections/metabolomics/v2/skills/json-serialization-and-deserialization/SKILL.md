---
name: json-serialization-and-deserialization
description: Use when after extracting header metadata from a Thermo Fisher Scientific .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RawFileReader
  - rawrr
  - jsonlite
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
- methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-serialization-and-deserialization

## Summary

Convert R list objects containing mass spectrometry metadata (e.g., instrument model, file name, time range, number of scans) extracted from Thermo Fisher Scientific .raw file headers into JSON format and write to disk, or read JSON files back into R objects for downstream analysis. This bridges vendor binary formats with interoperable text-based interchange.

## When to use

After extracting header metadata from a Thermo Fisher Scientific .raw file using rawrr::readFileHeader() or similar RawFileReader API calls, and you need to (1) share the metadata with non-R tools or pipelines, (2) archive it in a human-readable format, or (3) reload it later without re-reading the binary raw file. Also applies when ingesting JSON-encoded metadata from external LC-MS workflows into R for statistical analysis.

## When NOT to use

- Input is already a feature matrix or spectral data frame requiring column-wise statistical operations; use tabular serialization (CSV/TSV) instead.
- Metadata is small enough to fit in command-line arguments or environment variables; overhead of JSON serialization is unnecessary.
- Output must be read by legacy bioinformatic tools that only accept vendor binary formats or mzML/mzXML; consider ProteoWizard or ThermoRawFileParser conversion instead.

## Inputs

- Thermo Fisher Scientific .raw file (binary format)
- R list object (output of rawrr::readFileHeader())
- JSON-formatted text file containing serialized metadata

## Outputs

- JSON-formatted text file (.json extension) containing serialized header metadata
- R list object deserialized from JSON

## How to apply

Load a Thermo Fisher Scientific .raw file and call rawrr::readFileHeader() to retrieve header metadata as an R list object containing dynamic data items (instrument model, file name, time range, number of scans). Serialize the list to JSON using jsonlite::toJSON() or equivalent R JSON library, specifying appropriate auto_unbox and pretty options to balance readability and file size. Write the resulting JSON string to a named output file with .json extension using writeLines() or write(). To deserialize, read the JSON file back into memory with jsonlite::fromJSON() and validate schema and data type consistency before passing to downstream R functions. Use explicit column naming and type coercion to handle heterogeneous metadata types (strings, integers, timestamps).

## Related tools

- **rawrr** (Extracts header metadata and spectral data from Thermo Fisher Scientific .raw files via RawFileReader API; provides R list objects to serialize) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided .NET assembly that reads proprietary Thermo Fisher Scientific raw file format and exposes metadata for capture by rawrr) — https://github.com/thermofisherlsms/RawFileReader
- **jsonlite** (R package for JSON serialization and deserialization; converts R objects to/from JSON text)

## Examples

```
H <- rawrr::readFileHeader('sample.raw'); json_string <- jsonlite::toJSON(H, auto_unbox=TRUE, pretty=TRUE); writeLines(json_string, 'sample_header.json')
```

## Evaluation signals

- JSON output file is valid according to JSON schema (checked by json.tool or online validator); no parse errors when read back with fromJSON().
- Deserialized R object has identical structure, names, and data types to the original pre-serialized list (verify with identical() or all.equal()).
- JSON file contains all expected keys from the raw file header: instrument model, file name, time range, number of scans; no data is lost during round-trip serialization/deserialization.
- File size and readability trade-off is acceptable; auto_unbox=TRUE reduces file size; pretty=TRUE enhances human readability for inspection.
- Downstream R functions (e.g., statistical analysis pipelines) accept the deserialized list object without type coercion errors or missing-value warnings.

## Limitations

- JSON does not natively represent all R data types (e.g., factors, raw byte vectors, complex numbers); may require custom encoding/decoding logic for non-standard metadata.
- Large header objects or many scans indexed in metadata can result in large JSON files; consider compression (.json.gz) for archival.
- Cross-platform timestamp handling: JSON does not enforce timezone information; explicitly include timezone or ISO 8601 format in serialization to avoid ambiguity when deserializing on different systems.
- rawrr requires installation of RawFileReader .NET assembly and the rawrr executable; unavailable on non-Windows platforms without mono/dotnet runtime.
- Security: JSON deserialization can execute arbitrary code in some contexts; validate schema and sanitize input before deserializing untrusted JSON.

## Evidence

- [results] readFileHeader() returns metadata as R list: "The respective function is called `readFileHeader()` and returns a simple `R` object of type `list`"
- [other] Metadata includes instrument model, file name, time range, scan counts: "returns a list object containing dynamic data items such as instrument model, file name, time range, and number of scans, extracted directly from the binary raw file via the RawFileReader API"
- [other] JSON serialization workflow for header metadata: "Serialize the list object to JSON format using standard R JSON serialization (e.g., jsonlite::toJSON()). 4. Write the JSON-serialized header to a named output file with .json extension."
- [methods] R functions invoke C# wrapper methods via system calls: "`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call."
- [methods] File I/O bridge between .NET and R layer: "In order to return extracted data back to the `R` layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and"
