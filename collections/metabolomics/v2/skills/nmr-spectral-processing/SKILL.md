---
name: nmr-spectral-processing
description: Use when you have raw NMR/IR/MS spectral data in vendor-specific (RAW),
  open (jcamp), or mass spectrometry (mzML) formats and need to parse, validate, and
  convert them to a standardized internal representation with extracted metadata and
  peak tables for visualization or further analysis in.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - Python 3
  - Flask
  - Docker
  - proteowizard/pwiz-skyline
  - Python 3.12
  - chem-spectra-client
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- Use the file pyproject.toml to determine the version of Python required.
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0
  --port=3007
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data
  proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
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

# nmr-spectral-processing

## Summary

Convert and standardize NMR spectral files (jcamp, RAW, mzML formats) to a unified internal representation, extracting metadata and peak tables for downstream analysis and visualization. This skill handles vendor-specific binary formats through containerized proteowizard conversion and outputs normalized jcamp artifacts.

## When to use

You have raw NMR/IR/MS spectral data in vendor-specific (RAW), open (jcamp), or mass spectrometry (mzML) formats and need to parse, validate, and convert them to a standardized internal representation with extracted metadata and peak tables for visualization or further analysis in ChemSpectra.

## When NOT to use

- Input spectral data is already in validated jcamp format and requires only visualization, not re-conversion or metadata extraction.
- The raw file requires custom vendor-specific processing beyond standard proteowizard capabilities (e.g., proprietary closed-source instrument formats not supported by pwiz-skyline).
- You need to process gigabyte-scale batch datasets without access to the Docker/msconvert infrastructure or adequate compute resources.

## Inputs

- jcamp spectral file (text-based NMR/IR format)
- RAW spectral file (vendor-specific binary format from mass spectrometers)
- mzML spectral file (mass spectrometry markup language format)

## Outputs

- Converted jcamp file with extracted metadata
- Peak table (tabular representation of spectral peaks)
- Normalized spectral parameters and metadata

## How to apply

Submit the spectral file (jcamp, RAW, or mzML) via HTTP POST to the /api/v1/chemspectra/file/convert endpoint on the ChemSpectra backend service. The backend validates the input format and uses a Docker-containerized proteowizard/pwiz-skyline service (msconvert_docker) to handle vendor-specific binary formats like RAW. The conversion pipeline parses the file, extracts spectral metadata and peak parameters, and serializes the output to jcamp format with normalized peak tables. Verify successful conversion by checking the HTTP response contains valid jcamp output and that metadata fields (e.g., acquisition parameters, solvent, pulse sequence) are correctly populated.

## Related tools

- **proteowizard/pwiz-skyline** (Docker-containerized service (msconvert_docker) for parsing and converting vendor-specific RAW spectral formats to standardized representations) — https://github.com/ProteoWizard/pwiz
- **Flask** (Web framework hosting the /api/v1/chemspectra/file/convert endpoint and managing HTTP request/response lifecycle)
- **Docker** (Container runtime for isolating and executing proteowizard conversion service with vendor library dependencies)
- **Python 3.12** (Primary language for parsing, validation, metadata extraction, and jcamp serialization logic) — https://github.com/ComPlat/chem-spectra-app
- **chem-spectra-client** (Frontend JavaScript/React interface for user submission of spectral files and visualization of converted results) — https://github.com/ComPlat/chem-spectra-client

## Examples

```
curl -X POST -F 'file=@spectrum.raw' http://localhost:3007/api/v1/chemspectra/file/convert
```

## Evaluation signals

- HTTP response status is 200 OK and response body contains valid jcamp-formatted text with JCAMP-DX header and spectral data blocks.
- Extracted metadata fields (acquisition date, instrument type, solvent, pulse sequence, chemical shift reference) are non-empty and match values in the original raw file.
- Peak table is present and contains expected number of peaks with chemical shift (ppm), intensity, and integration values within typical NMR ranges (e.g., 0–12 ppm for 1H NMR).
- File size of converted jcamp output is reasonable relative to input (significant compression expected for binary RAW → text jcamp conversion indicates potential parsing failure).
- Round-trip validation: re-ingesting the converted jcamp file produces consistent peak positions and metadata without data loss.

## Limitations

- Vendor-specific RAW format support is limited to instruments covered by proteowizard/pwiz-skyline (primarily Waters, Agilent, Bruker, Thermo); proprietary or legacy formats may not be recognized.
- The msconvert_docker service requires Docker daemon availability and appropriate system resources; conversion may fail or timeout on very large spectral files or resource-constrained environments.
- Metadata extraction fidelity depends on compliance of the input file with JCAMP-DX or mzML standards; malformed or non-standard files may produce incomplete or incorrect metadata.
- No changelog provided in repository; version compatibility and breaking changes between updates are not explicitly documented.

## Evidence

- [other] The ChemSpectra App backend web service accepts and processes three spectral file formats: jcamp, RAW, and mzML files for NMR/IR/MS data.: "The ChemSpectra App backend web service accepts and processes three spectral file formats: jcamp, RAW, and mzML files for NMR/IR/MS data."
- [other] Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint.: "Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint."
- [other] Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats.: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats."
- [other] Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters.: "Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters."
- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
