---
name: http-api-endpoint-design
description: Use when when you need to expose a multi-step spectral processing workflow (parse → extract → render → annotate → compress) as a web service endpoint that accepts jcamp/RAW/mzML spectral files and must return coordinated output artifacts (modified JCAMP files, peak tables, and PNG images) in a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3172
  tools:
  - Flask
  - Python 3
  - chem-spectra-app
  - proteowizard/pwiz-skyline
  - gunicorn
  techniques:
  - NMR
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0 --port=3007
- Use the file pyproject.toml to determine the version of Python required.
- git clone https://github.com/ComPlat/chem-spectra-app.git
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HTTP API Endpoint Design

## Summary

Design and implement RESTful HTTP POST endpoints that accept file uploads with spectral data, validate input formats, process the data through a computational pipeline, and return compressed artifact collections. This skill bridges client requests for spectral analysis with backend processing services.

## When to use

When you need to expose a multi-step spectral processing workflow (parse → extract → render → annotate → compress) as a web service endpoint that accepts jcamp/RAW/mzML spectral files and must return coordinated output artifacts (modified JCAMP files, peak tables, and PNG images) in a single response.

## When NOT to use

- Input spectral data is already in a processed binary format incompatible with the chem-spectra-app parser
- Client application requires streaming or real-time response rather than a single atomic payload
- Output artifacts exceed practical ZIP archive size limits for your deployment environment

## Inputs

- POST request body with spectral file attachment (.dx or .jdx JCAMP format)
- Spectral data in jcamp, RAW, or mzML format

## Outputs

- ZIP archive containing modified JCAMP file(s) with peak annotations
- PNG image renderings of spectral data with annotated peaks
- Peak table artifacts

## How to apply

Define a POST endpoint (e.g., `/zip_jcamp_n_img`) that receives a spectral file attachment (.dx or .jdx format). Parse and validate the input using a dedicated file parser (chem-spectra-app). Extract spectral peaks and generate peak tables from the parsed data. Render the spectral data as PNG images with annotated peaks. Incorporate peak table annotations into modified JCAMP output file(s). Compress all output artifacts (JCAMP and PNG files) into a single ZIP archive. Return the ZIP with appropriate MIME type and HTTP headers. This design ensures the client receives all derived data products in one atomic transaction, reducing round-trip overhead.

## Related tools

- **Flask** (Web framework for defining and routing the HTTP POST endpoint) — https://github.com/ComPlat/chem-spectra-app
- **chem-spectra-app** (File parser and spectral data processor; validates input formats and extracts peaks) — https://github.com/ComPlat/chem-spectra-app
- **proteowizard/pwiz-skyline** (Docker containerized service for handling RAW and mzML mass spectrometry file formats) — https://github.com/ComPlat/chem-spectra-app
- **gunicorn** (WSGI HTTP server for deploying the Flask endpoint in production) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
curl -X POST -F 'file=@spectrum.jdx' http://localhost:3007/zip_jcamp_n_img -o output.zip
```

## Evaluation signals

- HTTP POST request to the endpoint returns status 200 with a valid ZIP archive in the response body
- ZIP archive contains expected files: at least one modified JCAMP file and one PNG image per input spectrum
- Response MIME type is 'application/zip' and Content-Disposition header specifies appropriate filename
- Peak table data extracted from JCAMP is non-empty and matches the annotations rendered in PNG images
- Input validation rejects malformed or unsupported file formats (not jcamp/RAW/mzML) with a descriptive HTTP 400 error

## Limitations

- Endpoint design assumes single spectral file input per request; handling multiple files in one request requires additional multiplexing logic
- RAW and mzML file processing depends on proteowizard/pwiz-skyline Docker service availability and correct environment configuration
- No explicit timeout or file size limits mentioned; large spectral files may cause memory exhaustion or slow response times
- Peak annotation accuracy and PNG rendering quality are dependent on upstream chem-spectra-app parser correctness and configuration

## Evidence

- [other] Receive POST request with spectral file attachment in .dx or .jdx format at the /zip_jcamp_n_img endpoint: "Receive POST request with spectral file attachment in .dx or .jdx format at the /zip_jcamp_n_img endpoint."
- [other] Parse and validate the input spectral file format using the chem-spectra-app file parser: "Parse and validate the input spectral file format using the chem-spectra-app file parser."
- [other] Extract spectral peaks and generate peak tables from the parsed data: "Extract spectral peaks and generate peak tables from the parsed data."
- [other] Generate PNG image renderings of the spectral data with annotated peaks: "Generate PNG image renderings of the spectral data with annotated peaks."
- [other] Compress all output artifacts (JCAMP files and PNG images) into a single ZIP file: "Compress all output artifacts (JCAMP files and PNG images) into a single ZIP file."
- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Return the ZIP archive to the client with appropriate MIME type and headers: "Return the ZIP archive to the client with appropriate MIME type and headers."
