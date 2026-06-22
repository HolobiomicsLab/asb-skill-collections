---
name: mass-spectrometry-data-processing
description: Use when you have raw mass spectrometry data in vendor-specific formats (Thermo RAW, Waters RAW, or open formats like mzML/jcamp) that need to be ingested, validated, and converted to a standardized representation for downstream peak detection, quantification, or integration with other NMR/IR/MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python 3
  - Flask
  - Docker
  - proteowizard/pwiz-skyline
  - Docker (msconvert_docker service)
  - Python 3.8+
  - HyperSpec
  - CUDA
  - IDSL.CSA
  - R
  - IDSL.IPA
  - IDSL.FSA
  - JPA
  - XCMS
  - CAMERA
  - MS-Convert
  - metScribeR
  - Shiny
  - chromatographR
  - mzR
  - MSConvert
  - tima R package
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
- doi: 10.1021/acs.jproteome.2c00612
  title: ''
- doi: 10.1021/acs.analchem.3c00376
  title: ''
- doi: 10.3390/metabo12030212
  title: ''
- doi: 10.1021/acs.jproteome.5c00548
  title: ''
- doi: 10.3389/fpls.2019.01329
  title: ''
evidence_spans:
- Use the file pyproject.toml to determine the version of Python required.
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0 --port=3007
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
- HyperSpec requires `Python 3.8+` with `CUDA` environment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autotuner_parameter_selection_cq
    doi: 10.1101/812370
    title: AutoTuner parameter selection
  - build: coll_chemspectra_cq
    doi: 10.1186/s13321-020-00481-0
    title: ChemSpectra
  - build: coll_hyperspec_cq
    doi: 10.1021/acs.jproteome.2c00612
    title: HyperSpec
  - build: coll_idsl_csa_cq
    doi: 10.1021/acs.analchem.3c00376
    title: IDSL.CSA
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  - build: coll_metscriber_cq
    doi: 10.1021/acs.jproteome.5c00548
    title: metScribeR
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_chemspectra_cq
schema_version: 0.2.0
---

# mass-spectrometry-data-processing

## Summary

Convert vendor-specific mass spectrometry file formats (RAW, mzML, jcamp) into standardized internal representations with extracted metadata and peak tables. This skill enables interoperable MS data processing within spectral analysis workflows by normalizing heterogeneous instrument outputs.

## When to use

You have raw mass spectrometry data in vendor-specific formats (Thermo RAW, Waters RAW, or open formats like mzML/jcamp) that need to be ingested, validated, and converted to a standardized representation for downstream peak detection, quantification, or integration with other NMR/IR/MS spectral data in a unified backend service.

## When NOT to use

- Input is already in a validated, standardized format ready for downstream analysis (e.g., vendor software has already performed conversion and QC)
- You need real-time streaming MS data ingestion; this workflow is synchronous POST-based batch conversion
- Input file is corrupted or truncated and cannot be parsed by proteowizard/pwiz-skyline

## Inputs

- RAW spectral file (Thermo/Waters vendor format)
- mzML file (open XML-based mass spectrometry format)
- jcamp file (JCAMP-DX spectral format)

## Outputs

- Standardized jcamp file with extracted metadata
- Peak table (m/z, intensity, retention time)
- Spectral metadata object (instrument, acquisition parameters)

## How to apply

Submit the MS file (RAW, mzML, or jcamp) via HTTP POST to the /api/v1/chemspectra/file/convert endpoint. The backend service validates the input format using proteowizard/pwiz-skyline, which runs as a Docker service (msconvert_docker) to handle vendor-specific RAW format nuances that cannot be parsed by pure Python. The converter extracts spectral parameters, metadata (acquisition conditions, instrument info), and peak data, then serializes the output as jcamp format with normalized peak tables. Verify successful conversion by inspecting the HTTP response for the converted jcamp artifact and confirm metadata extraction (retention time, m/z ranges, scan metadata) is present and sensible.

## Related tools

- **proteowizard/pwiz-skyline** (Vendor-agnostic MS file parser and converter; executes as Docker service to handle proprietary RAW format decoding) — https://github.com/ComPlat/chem-spectra-app
- **Flask** (REST API web framework hosting the /api/v1/chemspectra/file/convert endpoint) — https://github.com/ComPlat/chem-spectra-app
- **Docker (msconvert_docker service)** (Container runtime for proteowizard/pwiz-skyline to isolate vendor library dependencies) — https://github.com/ComPlat/chem-spectra-app
- **Python 3** (Backend service runtime; parses output from proteowizard and serializes to jcamp) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
curl -X POST -F "file=@sample.raw" http://localhost:3007/api/v1/chemspectra/file/convert
```

## Evaluation signals

- HTTP 200 response returned with jcamp artifact in response body; HTTP 4xx/5xx indicates parse/conversion failure
- Output jcamp file contains valid JCAMP-DX header, metadata fields (##ORIGIN, ##OWNER, ##DATE, ##TIME), and ##PEAK= entry with m/z–intensity pairs
- Metadata extraction: verify ##TITLE, instrument info, and acquisition parameters are populated from input file
- Peak table integrity: m/z values are within expected mass range for target analyte; intensity values are positive and non-zero
- Round-trip consistency: re-ingesting converted jcamp should preserve peak positions and metadata within floating-point tolerance

## Limitations

- Requires Docker and proteowizard/pwiz-skyline container to be running; vendor RAW formats cannot be parsed by pure Python libraries
- Conversion fidelity depends on proteowizard's support for the specific RAW file variant (Thermo vs. Waters vs. others); some legacy or proprietary formats may fail silently or lose metadata
- No changelog documented; version compatibility between proteowizard, Docker, and the ChemSpectra backend is not explicitly tracked

## Evidence

- [other] The ChemSpectra App backend web service accepts and processes three spectral file formats: jcamp, RAW, and mzML files for NMR/IR/MS data.: "Backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files"
- [other] Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats.: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats"
- [other] Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters.: "Convert the spectral file to a standardized internal representation, extracting metadata and spectral parameters"
- [other] Serialize the converted file to jcamp output format with peak tables and metadata.: "Serialize the converted file to jcamp output format with peak tables and metadata"
- [other] Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint.: "Receive HTTP POST request containing an uploaded spectral file (jcamp, RAW, or mzML format) at the /api/v1/chemspectra/file/convert endpoint"
