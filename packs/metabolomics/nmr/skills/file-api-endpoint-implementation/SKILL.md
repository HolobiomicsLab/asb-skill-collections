---
name: file-api-endpoint-implementation
description: Use when when you need to construct a POST endpoint that ingests raw spectral data files from multiple vendor formats (jcamp, RAW, mzML) and must standardize them for downstream processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Python 3
  - Flask
  - Docker
  - proteowizard/pwiz-skyline
  - gunicorn
  techniques:
  - NMR
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- Use the file pyproject.toml to determine the version of Python required.
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0 --port=3007
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemspectra_cq
    doi: 10.1186/s13321-020-00481-0
    title: ChemSpectra
  dedup_kept_from: coll_chemspectra_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00481-0
  all_source_dois:
  - 10.1186/s13321-020-00481-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-api-endpoint-implementation

## Summary

Implement a file conversion REST API endpoint that accepts spectral files in jcamp, RAW, or mzML formats, validates and converts them to a standardized internal representation, and returns the converted output in jcamp format with extracted metadata and peak tables. This skill is essential for building backend web services that integrate vendor-specific spectral data from NMR, IR, and MS instruments.

## When to use

When you need to construct a POST endpoint that ingests raw spectral data files from multiple vendor formats (jcamp, RAW, mzML) and must standardize them for downstream processing. Specifically, when vendor-specific binary formats (RAW) require format-agnostic parsing via third-party conversion services, and the output must preserve metadata and peak information in a single canonical format.

## When NOT to use

- Input is already in standardized jcamp format and requires no conversion or metadata extraction.
- Endpoint is for non-spectral file types (images, documents, genomic sequences) — this skill is specific to NMR/IR/MS spectral processing.
- Real-time streaming of spectral data is required; this endpoint assumes discrete file uploads and batch conversion.

## Inputs

- HTTP POST request body containing file upload (jcamp, RAW, or mzML format)
- Spectral file (binary or text): jcamp, RAW (vendor-specific), mzML (XML-based MS format)

## Outputs

- HTTP response: converted spectral file in jcamp format
- jcamp file with extracted metadata and peak tables
- Serialized internal spectral representation with metadata

## How to apply

Design a Flask POST endpoint at /api/v1/chemspectra/file/convert that receives an uploaded spectral file. Parse and validate the input file format, routing binary RAW files through a Docker containerized proteowizard/pwiz-skyline msconvert service to handle vendor-specific formats. Extract spectral parameters and metadata during conversion. Serialize the standardized representation to jcamp output format, ensuring peak tables and metadata annotations are preserved. Return the converted artifact to the client as the HTTP response body. The rationale is that vendor-specific formats require specialized parsers (msconvert), but normalizing to jcamp provides a single contract for downstream consumers (peak picking, annotation, visualization).

## Related tools

- **Flask** (Web framework for implementing the REST API endpoint and HTTP request/response handling)
- **proteowizard/pwiz-skyline** (Docker-containerized format converter for parsing and converting vendor-specific RAW spectral files to standardized formats) — https://github.com/ComPlat/chem-spectra-app
- **Docker** (Container runtime for isolating and executing the msconvert_docker service without vendor library dependencies on the host)
- **Python 3** (Language for implementing endpoint logic, file parsing, serialization, and Docker orchestration)
- **gunicorn** (WSGI server for deploying the Flask endpoint in production with multiple worker processes)

## Examples

```
curl -X POST -F 'file=@sample.raw' http://localhost:3007/api/v1/chemspectra/file/convert -o output.jcamp
```

## Evaluation signals

- Successfully parse and validate input file format before conversion (jcamp/RAW/mzML format detection).
- Verify HTTP 200 response and presence of jcamp-formatted output file with metadata fields (e.g., title, sample, solvent, frequency).
- Confirm that peak tables are preserved in converted output — compare peak count and intensity ranges between input and output.
- Test error handling: return appropriate HTTP error codes (400 Bad Request) for unsupported formats or malformed files.
- Validate that metadata extracted from vendor-specific formats (e.g., acquisition date, instrument model from RAW files) appears in jcamp output headers.

## Limitations

- RAW file conversion depends on proteowizard/pwiz-skyline Docker image availability and vendor library licensing; vendor formats may not be fully supported.
- mzML parsing may lose instrument-specific metadata not encoded in the XML schema; lossless round-trip conversion is not guaranteed.
- Endpoint performance scales with file size and conversion complexity; large binary RAW files may incur latency due to Docker container startup and format conversion overhead.
- No changelog available in the repository; version stability and backward compatibility of the jcamp output format are not formally documented.

## Evidence

- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint.: "Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint."
- [other] Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats.: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats."
- [other] Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters.: "Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters."
- [other] Serialize the converted file to jcamp output format with peak tables and metadata.: "Serialize the converted file to jcamp output format with peak tables and metadata."
- [other] docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses: "docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses"
