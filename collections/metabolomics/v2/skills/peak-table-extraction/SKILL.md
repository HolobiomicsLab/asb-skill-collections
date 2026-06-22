---
name: peak-table-extraction
description: Use when you have raw or converted spectral data (jcamp, RAW, or mzML format) from NMR, IR, or MS instruments and need to identify individual peaks, extract their properties (chemical shift, m/z, intensity, width), and generate a structured peak table for annotation, comparison, or publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3520
  tools:
  - Python 3
  - Flask
  - Docker
  - proteowizard/pwiz-skyline
  - chem-spectra-app
  - Docker (msconvert_docker service)
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- Use the file pyproject.toml to determine the version of Python required.
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0 --port=3007
- docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
- git clone https://github.com/ComPlat/chem-spectra-app.git
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

# peak-table-extraction

## Summary

Extract and annotate spectral peaks into tabular form from NMR/IR/MS spectral files (jcamp, RAW, mzML). This skill parses vendor-agnostic or vendor-specific spectral data, identifies peak positions and intensities, and produces structured peak tables suitable for downstream analysis or visualization.

## When to use

Apply this skill when you have raw or converted spectral data (jcamp, RAW, or mzML format) from NMR, IR, or MS instruments and need to identify individual peaks, extract their properties (chemical shift, m/z, intensity, width), and generate a structured peak table for annotation, comparison, or publication.

## When NOT to use

- Input is already a pre-processed feature table or peak list (e.g., from external metabolomics software); use direct import instead.
- Spectral data is severely corrupted, truncated, or in an unsupported format not listed (jcamp, RAW, mzML).
- Analysis goal is raw spectral comparison or fingerprinting without peak identification; consider direct spectral alignment or dot-product matching instead.

## Inputs

- jcamp spectral file (.dx or .jdx format)
- RAW vendor-specific spectral file (Orbitrap, Bruker, Agilent, Waters format)
- mzML mass spectrometry data file
- Parsed spectral data structure with metadata and intensity arrays

## Outputs

- Peak table (CSV or tabular format with columns: m/z or ppm, intensity, line width, assignment)
- Annotated JCAMP file with peak table metadata embedded
- PNG image rendering with annotated peaks overlaid on spectrum

## How to apply

Parse the input spectral file using the chem-spectra-app file parser to validate format and extract spectral metadata and raw data arrays. For vendor-specific RAW formats, route through proteowizard/pwiz-skyline via Docker (msconvert_docker service) to normalize to an intermediate representation. Identify peaks by applying spectral feature detection (local maxima, intensity thresholding, or deconvolution as implemented in chem-spectra-app). Extract each peak's position (chemical shift in ppm or m/z in Da), intensity (height or area), and optional line width or signal-to-noise ratio. Serialize the peak list into a structured table format (e.g., CSV or embedded in JCAMP output) with columns for chemical shift/m/z, intensity, assignment, and confidence. Validate that peak count and positions are consistent with the input spectral baseline and signal intensity distribution.

## Related tools

- **chem-spectra-app** (Core file parser and peak detection engine; validates input spectral formats and extracts peak lists and metadata) — https://github.com/ComPlat/chem-spectra-app
- **proteowizard/pwiz-skyline** (Vendor-specific RAW file format decoder; normalizes Orbitrap, Bruker, Agilent, Waters formats via msconvert)
- **Docker (msconvert_docker service)** (Containerized service runner for proteowizard; isolates vendor library dependencies)
- **Flask** (HTTP API framework; serves /api/v1/chemspectra/file/convert and /zip_jcamp_n_img endpoints for peak extraction requests) — https://github.com/ComPlat/chem-spectra-app
- **Python 3** (Implementation language for file parsing, peak detection, and table serialization logic)

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/file/convert -F 'file=@sample.jdx' | jq '.peak_table'
```

## Evaluation signals

- Peak table row count matches expected number of spectral features (validate against manual inspection or literature baseline for reference compounds).
- Peak positions (ppm or m/z values) align with known chemical shift or mass ranges for target analyte class (e.g., aromatic 1H NMR 7–8 ppm, aliphatic 0–3 ppm).
- Peak intensity distribution is consistent with baseline-corrected spectral amplitude (no negative intensities, max intensity ≤ 100% normalized scale).
- Output JCAMP file is well-formed (parseable by downstream tools; metadata headers present and non-empty).
- Generated PNG visualization correctly overlays annotated peaks on spectrum without misalignment or clipping.

## Limitations

- Peak detection accuracy depends on spectral signal-to-noise ratio; weak peaks or overlapping multiplets may be missed or merged.
- RAW file support is limited to formats recognized by proteowizard/pwiz-skyline; newer vendor formats may require library updates.
- mzML import assumes standards-compliant encoding; malformed or non-standard mzML files may fail to parse.
- Chemical shift assignment (e.g., 1H → carbon chain or aromatic group) is not automatic; peak table contains position and intensity only unless external reference library is provided.

## Evidence

- [other] Extract spectral peaks and generate peak tables from the parsed data.: "Extract spectral peaks and generate peak tables from the parsed data."
- [other] Parse and validate the input spectral file format using the chem-spectra-app file parser.: "Parse and validate the input spectral file format using the chem-spectra-app file parser."
- [other] Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats.: "Parse and validate the input file format using proteowizard/pwiz-skyline via the Docker msconvert_docker service to handle vendor-specific RAW formats."
- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Create modified JCAMP output file(s) incorporating the peak table annotations.: "Create modified JCAMP output file(s) incorporating the peak table annotations."
