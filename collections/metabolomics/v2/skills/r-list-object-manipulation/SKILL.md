---
name: r-list-object-manipulation
description: Use when you have extracted metadata or spectral information from a Thermo Fisher Scientific .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
---

# R List Object Manipulation

## Summary

Convert R list objects returned from binary file readers (such as rawrr::readFileHeader()) into serialized formats like JSON, enabling interoperability with downstream analysis tools and reproducible storage of extracted metadata. This skill bridges proprietary binary data access with standard data exchange formats.

## When to use

You have extracted metadata or spectral information from a Thermo Fisher Scientific .raw file (or similar binary format) as an R list object using functions like readFileHeader(), readIndex(), or readChromatogram(), and you need to persist, share, or pass that structured data to non-R tools or store it in a language-agnostic format for reproducibility and version control.

## When NOT to use

- Input is already in a standard serialized format (e.g., mzML, NetCDF, or CSV); conversion is unnecessary.
- You are performing statistical analysis within R and do not need to export intermediate metadata structures.
- The list object contains non-serializable elements (e.g., function pointers, external pointers) that jsonlite cannot handle.

## Inputs

- R list object (output from rawrr::readFileHeader(), readIndex(), readChromatogram(), or readSpectrum())
- File path or connection to write output

## Outputs

- .json file containing serialized list metadata
- JSON-formatted string representation of the R list

## How to apply

After calling a rawrr reader function (e.g., rawrr::readFileHeader()) to obtain an R list object containing dynamic items such as instrument model, file name, time range, and number of scans, apply a JSON serialization function (e.g., jsonlite::toJSON()) to convert the list into a portable JSON string. Write the serialized output to a named .json file using standard R I/O functions (e.g., write() or jsonlite::write_json()). Verify the JSON is well-formed and contains all expected keys and values by parsing it back or inspecting the file structure. This workflow ensures metadata extracted from binary files is captured in a format compatible with downstream statistical tools, documentation systems, and cross-platform pipelines.

## Related tools

- **rawrr** (R package providing reader functions (readFileHeader, readIndex, readSpectrum, readChromatogram) that return list objects from Thermo Fisher Scientific .raw files) — https://github.com/fgcz/rawrr
- **jsonlite** (R package for JSON serialization and deserialization of R objects, including toJSON() and write_json() functions)
- **RawFileReader** (.NET assembly providing low-level binary access to Thermo Fisher Scientific raw files; wrapped by rawrr) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
H <- rawrr::readFileHeader('sample.raw'); jsonlite::write_json(H, 'sample_header.json', pretty=TRUE)
```

## Evaluation signals

- Output .json file exists and is readable without parse errors (validate with a JSON parser).
- JSON keys match the original R list names; all numeric, string, and logical values are preserved.
- Parsing the JSON back into R (e.g., jsonlite::fromJSON()) recovers an equivalent or structurally identical list.
- File size and content match expectations (e.g., presence of expected metadata fields such as 'instrument model', 'time range', 'number of scans').
- JSON output is consumable by downstream tools or workflows that require standard data exchange formats.

## Limitations

- jsonlite serialization may lose R-specific type information (e.g., factors, POSIXct datetime objects may be coerced to strings); round-trip fidelity should be verified.
- Very large list objects (e.g., from readSpectrum() on thousands of scans) may produce large JSON files; streaming or chunked serialization may be necessary.
- Non-serializable R objects (function closures, external pointers) within a list will cause serialization to fail; such elements must be removed or handled separately.
- JSON does not natively support all R data structures (e.g., matrices, arrays); conversion may flatten or reshape nested data.

## Evidence

- [other] readFileHeader() extraction and metadata serialization workflow: "Call rawrr::readFileHeader() on the raw file to retrieve header metadata as an R list object. 3. Serialize the list object to JSON format using standard R JSON serialization (e.g.,"
- [results] readFileHeader() returns list with dynamic metadata fields: "The respective function is called `readFileHeader()` and returns a simple `R` object of type `list`"
- [other] List contents include instrument model, file name, time range, and scan counts: "rawrr::readFileHeader() reads meta information from a raw file header and returns a list object containing dynamic data items such as instrument model, file name, time range, and number of scans"
- [readme] rawrr provides access to Thermo Fisher Scientific Orbitrap data as R list objects: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package."
- [methods] Extracted data undergoes file I/O serialization workflow: "In order to return extracted data back to the `R` layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and"
