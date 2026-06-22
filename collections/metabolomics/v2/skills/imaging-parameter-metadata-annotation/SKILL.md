---
name: imaging-parameter-metadata-annotation
description: Use when after mzML-to-imzML conversion has produced barebones imzML files with pixel alignment but no experimental metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - imzML Writer
  - iw_utils.imzML_metadata_process
  - msconvert
  - ProteoWizard
  - Docker
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
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

# imaging-parameter-metadata-annotation

## Summary

Annotate imzML mass spectrometry imaging files with experimental acquisition parameters (scan speed, step size, lock mass, MS mode) and imaging coordinates to enable proper spatial-spectral alignment and mass recalibration. This skill ensures that imzML files produced by format conversion retain critical metadata linking pixel positions to instrument settings and known reference masses.

## When to use

Apply this skill after mzML-to-imzML conversion has produced barebones imzML files with pixel alignment but no experimental metadata. Use it when you have: (1) mzML source files with embedded acquisition metadata, (2) known imaging parameters (X scan speed in µm/s, Y step size in µm, lock mass m/z value), and (3) a requirement to enable mass recalibration and proper interpretation of ion images by downstream software (e.g., Cardinal MSI, METASPACE, M2aia). This is essential before sharing or analyzing imzML files with external readers.

## When NOT to use

- Input is already a fully annotated imzML file from a native vendor format importer; re-annotation may overwrite correct metadata.
- Experimental parameters (scan speed, step size, lock mass) are unknown or unavailable; metadata annotation requires these inputs.
- The imzML files are in raw vendor format; use msconvert and mzML-to-imzML conversion before applying this skill.

## Inputs

- mzML files (from prior msconvert conversion of raw vendor files)
- barebones imzML files (pixel-aligned, pre-metadata)
- raw vendor mass spectrometry data path
- experimental parameters: X scan speed (µm/s), Y step size (µm), lock mass (m/z), MS data mode (centroid or profile)

## Outputs

- annotated imzML files with embedded experimental metadata
- imzML files organized by scan filter
- imzML files with imaging coordinates and mass recalibration reference

## How to apply

Load the raw vendor mass spectrometry data path and mzML-derived imzML files into imzML Writer. Extract or specify the experimental parameters: X scan speed (µm/s), Y step size (µm), lock mass (m/z of internal standard, typically used as a reference point to correct mass measurement errors), and MS acquisition metadata (centroid vs. profile mode, scan filters). Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to write these parameters into the imzML XML header and associate them with the barebones pixel grid. Verify that the annotated imzML files are organized by scan filter as specified in the source mzML files and placed in the output directory. The lock mass value serves as a reference point to enable downstream mass recalibration, and the imaging coordinates (X, Y) must match the pixel dimensions written during the mzML-to-imzML conversion step.

## Related tools

- **imzML Writer** (Orchestrates file discovery, parameter input, and calls to iw_utils functions for metadata annotation) — https://github.com/VIU-Metabolomics/imzML_Writer
- **iw_utils.imzML_metadata_process** (Core function that annotates imzML XML header with experimental parameters and imaging coordinates) — https://github.com/VIU-Metabolomics/imzML_Writer
- **msconvert** (Prerequisite tool that converts raw vendor files to mzML, embedding acquisition metadata that is later extracted for imzML annotation) — https://proteowizard.sourceforge.io/download.html
- **ProteoWizard** (Distribution source for msconvert on Windows) — https://proteowizard.sourceforge.io/download.html
- **Docker** (Required to run msconvert on macOS before metadata annotation can proceed) — https://www.docker.com/products/docker-desktop/

## Examples

```
from imzml_writer import iw_utils; iw_utils.imzML_metadata_process(model_files='./mzML_files/sample.mzML', x_speed=50.0, y_step=100.0, path='./raw_data/', lock_mass=391.28425)
```

## Evaluation signals

- Annotated imzML files are valid XML and pass imzML schema validation (check against imzML specification 1.1 or 1.2)
- Lock mass parameter is present in the imzML file and matches the specified m/z value; verify by parsing the XML and confirming mass calibration element
- Imaging coordinates (X, Y pixel positions) align with X scan speed and Y step size; verify by calculating expected spatial extent and comparing to ion image dimensions
- imzML files are readable by at least one known downstream reader (e.g., Cardinal MSI, METASPACE, M2aia); successful import confirms metadata is syntactically correct
- Mass recalibration using lock mass produces expected mass accuracy improvement (typically within instrument specification, e.g., ±5 ppm for Orbitrap)

## Limitations

- Lock mass annotation requires a known internal standard or reference ion; if lock mass is incorrectly specified, mass recalibration will introduce systematic error.
- Imaging parameters (X scan speed, Y step size) must be manually entered or extracted from raw file headers; no automated detection is documented, risking parameter mismatch if user provides incorrect values.
- imzML metadata annotation does not validate spatial or mass accuracy against raw data; errors in pixel alignment or mass calibration are not flagged during annotation.
- Pixel dimensions must be written as integers for compatibility with some readers (e.g., SCiLS Lab); floating-point pixel dimensions may cause read failures in certain software.

## Evidence

- [methods] Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass recalibration, imaging coordinates, and MS acquisition metadata).: "iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass"
- [methods] Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors: "Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors"
- [methods] Type in the experimental parameters (i.e., X scan speed, Y step, Lock mass) and choose the MS data mode of interest (i.e., Centroid or Profile): "Type in the experimental parameters (i.e., X scan speed, Y step, Lock mass) and choose the MS data mode of interest (i.e., Centroid or Profile)"
- [methods] imzML files generated with imzML_Writer are compatible with multiple imzML file readers both commercially and as open-source software: "imzML files generated with imzML_Writer are compatible with multiple imzML file readers both commercially and as open-source software"
- [readme] Pixel dimensions must be written as an integer to be read properly: "Pixel dimensions must be written as an integer to be read properly"
