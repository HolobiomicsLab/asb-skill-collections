---
name: spectral-image-rendering
description: Use when when you have parsed and validated spectral data (jcamp, RAW, or mzML format) from NMR/IR/MS instruments and need to create visual representations with peak annotations for inspection, annotation, or publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3500
  - http://edamontology.org/topic_0593
  tools:
  - Flask
  - Python 3
  - chem-spectra-app
  - proteowizard/pwiz-skyline
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
---

# spectral-image-rendering

## Summary

Generate PNG image renderings of parsed spectral data with annotated peaks from NMR, IR, or MS input files. This skill converts raw spectral measurements into publication-ready visualizations that highlight detected peaks and their annotations.

## When to use

When you have parsed and validated spectral data (jcamp, RAW, or mzML format) from NMR/IR/MS instruments and need to create visual representations with peak annotations for inspection, annotation, or publication. Use this skill after spectral peaks have been extracted but before final output delivery.

## When NOT to use

- Input spectral file is not yet validated or parsed—parse and extract peaks first.
- Peak table is empty or incomplete—rendering requires extracted peak data with at least position and intensity values.
- Output format requirement is vector graphics (SVG) or raster formats other than PNG—use appropriate format conversion tools instead.

## Inputs

- Spectral file in jcamp format (.dx or .jdx extension)
- Spectral file in RAW format
- Spectral file in mzML format
- Parsed spectral peak table (extracted peaks with positions and intensities)

## Outputs

- PNG image file with spectral plot and annotated peaks
- ZIP archive containing PNG images and modified JCAMP files

## How to apply

After receiving and validating a spectral input file (jcamp/RAW/mzML) via POST request, parse the spectral data using the chem-spectra-app file parser to extract peak positions and intensities. Generate a PNG image rendering that overlays annotated peaks on the spectral baseline. The rendering should incorporate peak table data to annotate each identified peak with its chemical shift, intensity, or other metadata. Include all extracted peaks in the visualization and ensure the PNG includes proper axis labels and scaling. Return the rendered image as part of the output artifact bundle (typically compressed with modified JCAMP files into a ZIP archive).

## Related tools

- **chem-spectra-app** (File parser and spectral peak extraction engine; generates peak tables used for annotation in rendering) — https://github.com/ComPlat/chem-spectra-app
- **Flask** (Web framework hosting the /zip_jcamp_n_img POST endpoint that orchestrates file reception, parsing, peak extraction, image rendering, and ZIP archive assembly)
- **Python 3** (Runtime environment for spectral processing and image generation scripts)
- **proteowizard/pwiz-skyline** (Supporting service for RAW and mzML file format conversion and preprocessing) — https://hub.docker.com/r/proteowizard/pwiz-skyline

## Examples

```
curl -X POST -F 'file=@spectrum.jdx' http://localhost:3007/api/v1/chemspectra/zip_jcamp_n_img -o output.zip
```

## Evaluation signals

- PNG file is generated and non-empty (file size > 0 bytes, valid PNG magic bytes).
- Image contains visible spectral baseline plot with proper axis scaling and labels.
- All extracted peaks from the peak table are rendered and annotated on the image; verify by spot-checking peak count and positions against input peak table.
- PNG is successfully included in the returned ZIP archive alongside modified JCAMP file(s) with correct MIME type headers.
- Image rendering preserves peak intensity ratios and chemical shift values within acceptable tolerance (visual verification or pixel-coordinate comparison to peak table).

## Limitations

- Rendering quality and readability depend on spectral resolution and peak density; dense spectra may exhibit overlapping annotations.
- Only PNG format is explicitly mentioned; other output image formats (TIFF, SVG) are not documented in the ChemSpectra workflow.
- Peak annotation relies on prior successful extraction by chem-spectra-app parser; malformed or corrupted spectral files will produce incomplete or incorrect visualizations.
- No changelog documented; version-specific rendering behavior changes are not tracked in the repository.

## Evidence

- [other] Generate PNG image renderings of the spectral data with annotated peaks.: "Generate PNG image renderings of the spectral data with annotated peaks."
- [other] The ChemSpectra backend web service accepts jcamp, RAW, and mzML files as input.: "The ChemSpectra backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Extract spectral peaks and generate peak tables; create modified JCAMP output incorporating peak annotations.: "Extract spectral peaks and generate peak tables from the parsed data. 4. Generate PNG image renderings of the spectral data with annotated peaks. 5. Create modified JCAMP output file(s) incorporating"
- [other] Receive POST request with spectral file at /zip_jcamp_n_img endpoint and return ZIP archive.: "Receive POST request with spectral file attachment in .dx or .jdx format at the /zip_jcamp_n_img endpoint. 6. Compress all output artifacts (JCAMP files and PNG images) into a single ZIP file."
- [other] Parse and validate input spectral file format using chem-spectra-app file parser.: "Parse and validate the input spectral file format using the chem-spectra-app file parser."
