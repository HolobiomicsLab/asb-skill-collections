---
name: json-format-conversion
description: Use when when you have extracted file metadata or scan summaries as R
  list objects from .raw files using readFileHeader(), readIndex(), or readSpectrum(),
  and need to persist them to disk, share them across systems, or feed them into downstream
  tools that consume JSON (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rjson
  - rawrr
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in
  the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method
  typically results in the execution of methods defined in the `RawFileReader` dynamic
  link library provided by Thermo
- rjson::toJSON
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-format-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert R list objects extracted from Thermo Fisher Scientific binary raw files into JSON format for serialization and storage. This skill enables portable exchange and downstream parsing of structured proteomics metadata and spectral summaries.

## When to use

When you have extracted file metadata or scan summaries as R list objects from .raw files using readFileHeader(), readIndex(), or readSpectrum(), and need to persist them to disk, share them across systems, or feed them into downstream tools that consume JSON (e.g., JSON-schema validators, web services, or non-R analysis pipelines).

## When NOT to use

- Input is already in JSON format or another exchange format (mzML, mzXML) — deserialize and parse directly instead.
- Raw spectral m/z and intensity arrays are very large (>10⁶ data points per scan) — JSON text serialization may be inefficient; consider binary formats (HDF5, Parquet, msgpack) or streaming protocols instead.
- Downstream tool expects a specific schema or dialect of JSON not guaranteed by rjson::toJSON() — validate or post-process JSON output against schema.

## Inputs

- R list object returned by rawrr reader functions (readFileHeader, readSpectrum, readIndex, readChromatogram, etc.)
- File path for output (character string with .json extension)

## Outputs

- .json file on disk containing serialized R list as JSON
- JSON text string (if writing to string rather than file)

## How to apply

After calling readFileHeader() or similar rawrr reader functions to produce an R list object containing instrument metadata, chromatogram data, or scan indices, pass the R list to rjson::toJSON() to serialize it to JSON text. Write the JSON string to a file with .json extension using base R file I/O (e.g., writeLines() or write()). Verify the output file exists and contains valid JSON structure by parsing it back (e.g., rjson::fromJSON()) to confirm round-trip fidelity. The JSON representation will dynamically include all data items returned by the reader function, which vary by instrument model and control software version.

## Related tools

- **rjson** (R package that serializes R list objects to JSON text using toJSON() function) — https://cran.r-project.org/package=rjson
- **rawrr** (R package providing reader functions (readFileHeader, readSpectrum, etc.) that produce list objects suitable for JSON conversion) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly wrapped by rawrr; provides underlying C# API for accessing binary raw file data) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
H <- readFileHeader(rawfile); json_str <- toJSON(H); writeLines(json_str, 'metadata.json')
```

## Evaluation signals

- Output .json file exists on disk at specified path and is readable by the file system.
- Round-trip parsing succeeds: rjson::fromJSON(readLines(output_file)) returns an R list with identical structure and values as the input list (exact equality or checksums match).
- JSON structure is valid: json linting tools (e.g., Python json.tool, online validators) accept the file without syntax errors.
- All metadata fields from the original R list are preserved in the JSON output (no missing keys or truncated values).
- Field names and data types in JSON match the instrument model and software version (e.g., 'Time range', 'Number of scans', 'Instrument model' are present for a given instrument).

## Limitations

- rjson::toJSON() may not handle all R object types equally (e.g., factors, S3/S4 classes); convert complex objects to vectors/lists before serialization.
- JSON text is larger than binary formats; for high-volume spectral data, consider compression (.json.gz) or binary alternatives (HDF5, msgpack).
- No built-in schema validation: JSON output conforms to rjson's serialization rules but may not match a specific downstream tool's JSON schema; post-validate against schema if required.
- Floating-point precision loss possible during serialization/deserialization; round-trip values may differ at machine epsilon scale.
- Large spectral data (millions of scans, high m/z resolution) can produce JSON files too large for in-memory parsing in some environments.

## Evidence

- [other] readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing dynamically-generated data items that vary by instrument model and control software version.: "readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing"
- [other] Call readFileHeader() to extract the file header as an R list object. 3. Serialize the list to JSON format using rjson::toJSON. 4. Write the serialized JSON to an output file with .json extension. 5. Verify that the JSON file exists and contains valid JSON structure.: "Serialize the list to JSON format using rjson::toJSON. 4. Write the serialized JSON to an output file with .json extension. 5. Verify that the JSON file exists and contains valid JSON structure"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call. In order to return extracted data back to the R layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call. extracted information is written to a temporary location on the harddrive,"
