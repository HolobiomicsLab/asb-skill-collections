---
name: mass-spectrometry-file-conversion
description: Use when you have vendor raw mass spectrometry data files (.raw) from a commercial instrument and need to convert them to open formats (mzML for spectral data, imzML for imaging mass spectrometry) for compatibility with third-party analysis software or to meet open-data standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ProteoWizard
  - Python
  - msconvert
  - Docker
  - imzML Writer
  - imzML Scout
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-file-conversion

## Summary

Convert vendor-specific raw mass spectrometry data to open standardized formats (mzML, imzML) using msconvert, either via ProteoWizard on Windows or Docker on macOS. This skill is essential for enabling downstream analysis with platform-independent tools and ensuring data reproducibility and interoperability.

## When to use

You have vendor raw mass spectrometry data files (.raw) from a commercial instrument and need to convert them to open formats (mzML for spectral data, imzML for imaging mass spectrometry) for compatibility with third-party analysis software or to meet open-data standards. This is the entry point before any downstream processing like peak picking, normalization, or spatial annotation.

## When NOT to use

- Input data is already in mzML or imzML format — skip directly to downstream analysis
- You need vendor-specific proprietary features not preserved in mzML conversion — use vendor software instead
- Raw data is from an unsupported mass spectrometry instrument — msconvert may not recognize the file format

## Inputs

- vendor raw mass spectrometry data files (.raw format)
- directory path containing .raw files
- optional: imaging parameters (X scan speed, Y step, lock mass m/z)

## Outputs

- mzML format files (intermediate open format for spectral data)
- imzML format files (final open format for imaging mass spectrometry data)
- conversion log or progress report

## How to apply

First, verify your platform: on Windows, confirm msconvert from ProteoWizard is installed and in the system PATH, or be prepared to provide its install directory when prompted; on macOS, ensure Docker is running and pre-pull the chambm/pwiz-skyline-i-agree-to-the-vendor-licenses image to avoid delays on first conversion. Then invoke the conversion via imzML Writer's iw_utils.RAW_to_mzML(raw_data_path) function, specifying the directory containing the .raw file(s); msconvert will apply default peakPicking settings during conversion. Monitor the process for completion and verify that mzML file(s) appear in the output directory with correct file naming, valid XML structure, and expected file size relative to input raw data. If using imzML Writer's GUI, select the source folder containing .raw files, choose your MS data mode (Centroid for peak-picked or Profile for raw intensities), and select 'Full Conversion' to execute both RAW→mzML and mzML→imzML stages.

## Related tools

- **msconvert** (Core conversion engine that translates vendor raw files to mzML using peakPicking methods; invoked by imzML Writer) — https://proteowizard.sourceforge.io/download.html
- **ProteoWizard** (Windows distribution platform for msconvert; provides GUI and CLI tools for mass spectrometry file conversion) — https://proteowizard.sourceforge.io/download.html
- **Docker** (Container runtime for macOS; enables msconvert execution via the chambm/pwiz-skyline image without native Windows environment) — https://www.docker.com/products/docker-desktop/
- **imzML Writer** (High-level wrapper orchestrating RAW→mzML→imzML conversion pipeline with GUI and Python API; manages msconvert invocation and metadata annotation) — https://github.com/VIU-Metabolomics/imzML_Writer
- **imzML Scout** (Visualization and validation tool for inspecting converted imzML files; supports pixel-level mass spectrum inspection and batch export) — https://github.com/VIU-Metabolomics/imzML_Writer

## Examples

```
import imzml_writer.iw_utils as iw_utils
iw_utils.RAW_to_mzML('/path/to/raw_data_directory')
```

## Evaluation signals

- mzML output file(s) are present in the output directory with non-zero file size and match the naming scheme of input .raw files
- mzML files parse without XML schema errors when validated against the mzML specification
- File size ratio (mzML output / raw input) is reasonable for your data type (typically 0.5–2× for centroid mode)
- Opening imzML file in imzML Scout displays a valid pixel map without corruption and allows pixel-level mass spectrum inspection
- Conversion log shows no errors or warnings related to unsupported vendor formats or missing peakPicking parameters

## Limitations

- msconvert supports only vendor formats for which ProteoWizard has licensed readers; some proprietary formats may not be recognized
- On macOS, Docker must be running and the image must be downloaded (~2–5 GB); first conversion may be delayed by image pull time
- Peak picking is applied by default during RAW→mzML conversion; Profile mode data cannot be recovered post-conversion if Centroid mode is selected
- Lock mass recalibration is a separate post-conversion step and requires known reference ion m/z; mass accuracy of mzML depends on instrument calibration at acquisition time
- No changelog documented; upgrade compatibility and breaking changes between imzML Writer versions are not tracked

## Evidence

- [other] On PC, msconvert is installed from ProteoWizard and imzML Writer prompts for its path on first use; on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that is downloaded on demand.: "On PC, msconvert is installed from ProteoWizard and imzML Writer prompts for its path on first use; on Mac, msconvert runs via a Docker image (chambm/pwiz-skyline-i-agree-to-the-vendor-licenses) that"
- [other] Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings to convert vendor raw data to mzML format.: "Invoke iw_utils.RAW_to_mzML(raw_data_path) on the directory containing the .raw file, which internally calls msconvert with default peakPicking settings to convert vendor raw data to mzML format."
- [readme] Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML.: "Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML."
- [methods] Click select Folder to choose the directory containing the `.raw`, `.mzML`, or `.imzML` data files: "Click select Folder to choose the directory containing the `.raw`, `.mzML`, or `.imzML` data files"
- [methods] Centroid: Writes centroid data using msconvert's peakPicking method.: "Centroid: Writes centroid data using msconvert's peakPicking method."
- [readme] Similarly, imzML Writer will prompt you to download the docker image the first time you try to call it.: "Similarly, imzML Writer will prompt you to download the docker image the first time you try to call it."
