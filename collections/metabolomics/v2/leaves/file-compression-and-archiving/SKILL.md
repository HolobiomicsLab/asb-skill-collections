---
name: file-compression-and-archiving
description: Use when when a spectral processing operation produces multiple output
  artifacts in different formats (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Flask
  - Python 3
  - chem-spectra-app
  - proteowizard/pwiz-skyline
  - Python 3 zipfile module
  license_tier: open
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0
  --port=3007
- Use the file pyproject.toml to determine the version of Python required.
- git clone https://github.com/ComPlat/chem-spectra-app.git
- docker run --detach --name msconvert_docker --rm -it -e WINEDEBUG=-all -v ./chem_spectra/tmp:/data
  proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses bash
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

# file-compression-and-archiving

## Summary

Compress and archive multiple heterogeneous output artifacts (spectral images, annotated data files) into a single ZIP container for efficient delivery and client-side extraction. This skill is essential in spectral processing workflows where the analysis produces multiple file types (PNG images, modified JCAMP files) that must be bundled and transmitted together.

## When to use

When a spectral processing operation produces multiple output artifacts in different formats (e.g., both PNG renderings and JCAMP peak-annotated files) that need to be returned to a client as a single downloadable unit, or when transmission efficiency or atomic delivery of interdependent outputs is required.

## When NOT to use

- When output artifacts need to be retrieved independently or asynchronously (use streaming or individual endpoints instead)
- When the total uncompressed size exceeds available server memory or client storage capacity
- When downstream workflows require individual file access before decompression (prefer multi-part form responses or indexed storage)

## Inputs

- Multiple PNG image files (rendered spectral plots with annotated peaks)
- One or more JCAMP files (peak-annotated spectral data files in .dx or .jdx format)
- Metadata or log files associated with the spectral processing operation

## Outputs

- Single ZIP archive file containing all input artifacts
- HTTP response with application/zip MIME type and Content-Disposition header

## How to apply

After generating all output artifacts from spectral peak detection and image rendering, collect all files (JCAMP files and PNG images) into a staging directory. Use Python's standard zipfile module or equivalent to recursively compress all outputs into a single ZIP archive. Set appropriate MIME type (application/zip) and HTTP headers (Content-Disposition with attachment filename) before returning the archive to the client. The rationale is to provide atomic, self-contained delivery of all analysis outputs in a single HTTP response, eliminating the need for multiple round-trips and simplifying client-side file management.

## Related tools

- **Python 3 zipfile module** (Native archiving and compression of multiple output files into a single ZIP container)
- **Flask** (HTTP framework for setting MIME type, headers, and serving the ZIP archive to the client) — https://github.com/ComPlat/chem-spectra-app
- **chem-spectra-app** (Backend service that generates the PNG and JCAMP artifacts to be archived) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
import zipfile; z = zipfile.ZipFile('output.zip', 'w'); z.write('spectrum_plot.png'); z.write('peaks_annotated.jdx'); z.close()
```

## Evaluation signals

- ZIP archive is valid and can be extracted without corruption (verify with `unzip -t` or equivalent)
- All expected output files (PNG images and JCAMP files) are present in the archive with correct counts and filenames
- HTTP response headers include Content-Type: application/zip and appropriate Content-Disposition attachment filename
- Compressed file size is smaller than the sum of uncompressed artifacts (compression ratio > 0 for lossless formats like text JCAMP)
- Client can successfully download, decompress, and access individual artifacts without data loss or format corruption

## Limitations

- ZIP compression is lossless but provides limited compression for already-compressed formats (PNG images); JCAMP text files compress better
- Large archives may exceed client memory or disk constraints; no streaming or chunked delivery mechanism is described
- No versioning or incremental archiving strategy is documented; all outputs must be regenerated and re-archived for each request
- The skill assumes all outputs fit in server memory before archiving; no out-of-core or temporary file strategies are mentioned

## Evidence

- [other] Create modified JCAMP output file(s) incorporating the peak table annotations. Compress all output artifacts (JCAMP files and PNG images) into a single ZIP file.: "Compress all output artifacts (JCAMP files and PNG images) into a single ZIP file."
- [other] Return the ZIP archive to the client with appropriate MIME type and headers.: "Return the ZIP archive to the client with appropriate MIME type and headers."
- [other] Receive POST request with spectral file attachment in .dx or .jdx format at the /zip_jcamp_n_img endpoint.: "Receive POST request with spectral file attachment in .dx or .jdx format at the /zip_jcamp_n_img endpoint."
