---
name: raw-vendor-file-format-handling
description: Use when you have collected imaging mass spectrometry data in vendor-specific raw format (.raw files from Bruker, Waters, Thermo, or other instrument manufacturers) and need to convert it to the open, vendor-agnostic mzML XML format before downstream imzML construction and spatial alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3649
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ProteoWizard
  - Python
  - msconvert
  - Docker
  - imzML Writer
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
- On PC, download the latest msconvert release from ProteoWizard
- 'On PC, this can be installed normally from Proteowizard: https://proteowizard.sourceforge.io/download.html'
- import os import imzml_writer.utils as iw_utils
- iw_utils.mzML_to_imzML_convert(PATH=mzML_path)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_imzml_writer_cq
    doi: 10.1021/acs.analchem.4c06520
    title: imzML Writer
  dedup_kept_from: coll_imzml_writer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06520
  all_source_dois:
  - 10.1021/acs.analchem.4c06520
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-vendor-file-format-handling

## Summary

Convert proprietary vendor mass spectrometry raw files (.raw) to the open mzML format using msconvert, with platform-specific deployment (ProteoWizard on Windows, Docker on macOS). This is the prerequisite step for imaging mass spectrometry data that will subsequently be aligned and annotated into imzML format.

## When to use

You have collected imaging mass spectrometry data in vendor-specific raw format (.raw files from Bruker, Waters, Thermo, or other instrument manufacturers) and need to convert it to the open, vendor-agnostic mzML XML format before downstream imzML construction and spatial alignment. Use this skill when beginning a full imzML Writer conversion pipeline or when you need to validate raw-to-mzML conversion as a standalone step.

## When NOT to use

- Input data is already in mzML or imzML format — proceed directly to mzML-to-imzML conversion or metadata annotation.
- msconvert cannot be installed (e.g., restrictive institutional policies on ProteoWizard licensing or Docker) — consider institutional alternative mass spectrometry conversion services.
- Raw files are from non-standard or unsupported vendor formats — verify instrument vendor compatibility with ProteoWizard before beginning.

## Inputs

- vendor raw mass spectrometry data file (.raw)
- directory path containing one or more .raw files

## Outputs

- mzML file(s) in open XML format
- mzML output directory with valid XML structure

## How to apply

First, verify platform-specific prerequisites: on Windows, ensure msconvert from ProteoWizard is installed and accessible via system PATH or note its installation directory; on macOS, ensure Docker is running and pre-pull the image `chambm/pwiz-skyline-i-agree-to-the-vendor-licenses` to avoid delays during first conversion. Second, locate the directory containing the input .raw file(s). Third, invoke `iw_utils.RAW_to_mzML(raw_data_path)`, which internally calls msconvert with default peakPicking settings for centroid conversion. Monitor progress and verify that mzML file(s) are generated in the output directory with correct file naming and valid XML structure (well-formed tags, expected namespace declarations, presence of spectrum and chromatogram elements). If using the GUI, imzML Writer will prompt for the msconvert path on first use if not already in PATH.

## Related tools

- **msconvert** (Core conversion engine that translates vendor proprietary raw binary format to open mzML XML using peakPicking for centroid data) — https://proteowizard.sourceforge.io/download.html
- **ProteoWizard** (Windows native installation package providing msconvert executable and vendor format parsers) — https://proteowizard.sourceforge.io/download.html
- **Docker** (macOS container runtime for running msconvert via chambm/pwiz-skyline-i-agree-to-the-vendor-licenses image) — https://www.docker.com/products/docker-desktop/
- **imzML Writer** (Python wrapper and orchestration layer providing iw_utils.RAW_to_mzML() function and GUI prompting for msconvert configuration) — https://github.com/VIU-Metabolomics/imzML_Writer

## Examples

```
from imzml_writer import iw_utils; iw_utils.RAW_to_mzML('/path/to/raw_data_directory')
```

## Evaluation signals

- Output mzML file exists in the expected output directory with matching or derived filename from input .raw
- mzML XML is well-formed: parseable by standard XML validators with expected namespace declarations and spectrum/chromatogram elements
- mzML file size is reasonable (typically 50–500 MB for typical imaging runs, depending on m/z range and scan count)
- Conversion log or progress output indicates zero errors and successful msconvert invocation (on Windows, explicit return code 0; on macOS via Docker, container exits cleanly)
- Subsequent mzML-to-imzML conversion step (iw_utils.mzML_to_imzML_convert) runs without format errors, confirming mzML integrity

## Limitations

- Vendor raw file format support depends entirely on ProteoWizard's installed vendor libraries — some newer instruments or proprietary formats may not be supported; check ProteoWizard release notes.
- On macOS, Docker image download and container initialization add ~2–5 minutes overhead on first use; subsequent conversions are faster.
- msconvert default peakPicking is applied universally; users requiring profile-mode output or custom peak-picking parameters must invoke msconvert separately.
- imzML Writer prompts for msconvert path interactively on first use if not in PATH; automation of multiple conversions may require pre-configuration.

## Evidence

- [other] On PC, msconvert is installed from ProteoWizard and imzML Writer prompts for its path on first use; on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand.: "On PC, msconvert is installed from ProteoWizard and imzML Writer prompts for its path on first use; on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that"
- [other] Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings to convert vendor raw data to mzML format.: "Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings to convert vendor raw data to mzML format."
- [readme] Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML. On PC, this can be installed normally from Proteowizard: "Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML. On PC, this can be installed normally from Proteowizard"
- [other] Monitor conversion progress and confirm mzML file(s) are generated in the output location with correct file naming and valid XML structure.: "Monitor conversion progress and confirm mzML file(s) are generated in the output location with correct file naming and valid XML structure."
- [readme] On Mac, you can still run msconvert via a docker image. First, install Docker: https://www.docker.com/products/docker-desktop/: "On Mac, you can still run msconvert via a docker image. First, install Docker"
