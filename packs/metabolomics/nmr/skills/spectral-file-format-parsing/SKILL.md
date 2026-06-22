---
name: spectral-file-format-parsing
description: Use when you receive raw spectral data files (jcamp, RAW, or mzML) from NMR, IR, or MS instruments and need to extract peak tables, metadata, and spectral parameters before generating visualizations, performing peak annotation, or converting to standardized output formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Flask
  - Python 3
  - chem-spectra-app
  - proteowizard/pwiz-skyline
  - Docker
  - chem-spectra-app file parser
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

# spectral-file-format-parsing

## Summary

Parse and validate spectral data files in jcamp, RAW, and mzML formats to extract metadata, peaks, and spectral parameters for NMR/IR/MS processing. This skill transforms vendor-specific or standardized spectral formats into an internal representation suitable for downstream analysis and visualization.

## When to use

Apply this skill when you receive raw spectral data files (jcamp, RAW, or mzML) from NMR, IR, or MS instruments and need to extract peak tables, metadata, and spectral parameters before generating visualizations, performing peak annotation, or converting to standardized output formats.

## When NOT to use

- Input file is already in an application-specific processed format (e.g., pre-computed peak lists as CSV/JSON) — use direct ingestion instead of re-parsing.
- Spectral data format is not one of the three supported types (jcamp, RAW, mzML) — the parser will fail or require additional format conversion tooling.
- Input file is corrupted, truncated, or does not conform to the official specification for its declared format — validation will reject it.

## Inputs

- jcamp spectral file (.dx or .jdx format)
- RAW spectral file (vendor-specific binary format from mass spectrometry instruments)
- mzML spectral file (standardized XML-based mass spectrometry data format)
- HTTP POST request with file attachment

## Outputs

- parsed spectral metadata object (instrument type, acquisition parameters, sample info)
- peak table (m/z or chemical shift values with intensities/annotations)
- standardized internal spectral representation
- JCAMP output file with peak table annotations
- PNG image rendering of spectral data with annotated peaks

## How to apply

Receive the uploaded spectral file (jcamp, RAW, or mzML format) via HTTP POST at the appropriate endpoint. Use proteowizard/pwiz-skyline via Docker (msconvert_docker service) to handle vendor-specific RAW formats and parse them into a standardized internal representation. The chem-spectra-app file parser validates the input file format and extracts spectral metadata, peaks, and parameters. For JCAMP files (.dx or .jdx), parse directly using the file parser without requiring Docker conversion. Extract peak tables and spectral parameters from the parsed data, then serialize to the target output format (typically JCAMP with annotations). Validation succeeds when the parsed metadata and peak counts match expected ranges for the instrument type.

## Related tools

- **proteowizard/pwiz-skyline** (Parse and convert vendor-specific RAW spectral files into standardized formats via Docker msconvert service) — https://github.com/ProteoWizard/pwiz
- **chem-spectra-app file parser** (Validate input spectral file format and extract metadata, peaks, and spectral parameters from jcamp/RAW/mzML files) — https://github.com/ComPlat/chem-spectra-app
- **Flask** (HTTP framework for receiving POST requests containing spectral file attachments at API endpoints) — https://github.com/pallets/flask
- **Python 3** (Core language for implementing file parsing logic, format validation, and metadata extraction)
- **Docker** (Container runtime for isolating and executing the msconvert_docker service to handle RAW file conversion)

## Examples

```
curl -X POST -F 'file=@sample.jdx' http://localhost:3007/api/v1/chemspectra/file/convert
```

## Evaluation signals

- Parsed metadata object contains expected keys (instrument type, acquisition date, sample identifier, experimental parameters) with non-null values for the input spectral type
- Peak table extracted contains a number of peaks consistent with the spectral complexity; no peaks indicates parse failure or incorrect format detection
- Round-trip validation: re-serialize the parsed data to JCAMP and verify that key metadata and peak positions remain consistent with the input file
- No parsing errors or warnings logged during file parse step; validation status indicates 'success' or 'valid'
- Output file size and peak count are reasonable relative to instrument type (e.g., MS files typically have more peaks than NMR files of comparable complexity)

## Limitations

- RAW file parsing depends on proteowizard/pwiz-skyline Docker image availability and correct Docker daemon configuration; network or container runtime failures will halt parsing.
- The parser assumes well-formed input files conforming to official JCAMP, RAW, and mzML specifications; corrupted or non-standard variants may parse incorrectly or incompletely.
- Vendor-specific RAW formats are supported only for instruments compatible with proteowizard/pwiz-skyline (primarily mass spectrometry vendors such as Thermo, Bruker, Waters, Agilent); other instrument vendors may not be supported.
- Large spectral files (e.g., high-resolution MS runs with millions of data points) may consume significant memory or processing time during parsing.

## Evidence

- [other] Parse and validate the input file format using chem-spectra-app file parser: "Parse and validate the input file format using the chem-spectra-app file parser."
- [intro] Accept jcamp, RAW, and mzML files as input: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Handle vendor-specific RAW formats using proteowizard: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats."
- [other] Convert to standardized internal representation: "Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters."
- [other] Extract peaks and metadata for NMR/IR/MS: "Extract spectral peaks and generate peak tables from the parsed data."
