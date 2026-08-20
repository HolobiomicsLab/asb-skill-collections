---
name: mzml-to-imzml-format-conversion
description: Use when you have mzML files generated from raw vendor mass spectrometry
  imaging data and need to create imzML output compatible with software like Cardinal
  MSI, METASPACE, M2aia, or SCiLS Lab.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - imzML Writer
  - Python
  - msconvert
  - imzML Scout
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c06520
  title: imzML Writer
evidence_spans:
- iw_utils.RAW_to_mzML(raw_data_path)
- 'imzML Writer is available as: (1) A distributable package on pypi (for CLI, stable
  GUI, `pip install imzML-Writer`)'
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

# mzml-to-imzml-format-conversion

## Summary

Convert intermediate mzML mass spectrometry files into the imzML imaging format, aligning pixel coordinates and annotating with experimental parameters (scan speed, step size, lock mass). This bridges the gap between vendor raw data (converted to mzML via msconvert) and imzML readers used for spatial metabolomics visualization.

## When to use

You have mzML files generated from raw vendor mass spectrometry imaging data and need to create imzML output compatible with software like Cardinal MSI, METASPACE, M2aia, or SCiLS Lab. The conversion requires known imaging acquisition parameters: X scan speed (µm/s), Y step size (µm), lock mass (m/z reference), and data mode (centroid or profile).

## When NOT to use

- Input files are already in imzML format (use imzML metadata update instead).
- Raw vendor files have not yet been converted to mzML (perform raw-to-mzML conversion first).
- Required imaging parameters (X scan speed, Y step size) are unknown or unavailable.

## Inputs

- mzML files (from msconvert conversion of raw vendor data)
- X scan speed parameter (µm/s)
- Y step size parameter (µm)
- Lock mass value (m/z of internal standard)
- MS data mode specification (centroid or profile)

## Outputs

- imzML files with pixel-aligned coordinate structure
- Annotated imzML files with experimental metadata
- Files organized by scan filter in output directory

## How to apply

Load mzML files from a target directory using imzML Writer's file discovery. Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write the barebones imzML structure and align pixel coordinates according to X scan speed and Y step size parameters. Next, call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate the imzML files with experimental metadata including lock mass for mass recalibration, imaging coordinates, and MS acquisition details. Finally, place the annotated imzML files in the output directory, organized by scan filter as specified in the source mzML files. Apply lock mass recalibration during this step to correct mass measurement errors using the m/z of a known internal standard.

## Related tools

- **imzML Writer** (Primary conversion and metadata annotation framework; orchestrates mzML-to-imzML conversion and pixel alignment) — https://github.com/VIU-Metabolomics/imzML_Writer
- **msconvert** (Prerequisite tool; converts raw vendor files to mzML format before imzML conversion begins) — https://proteowizard.sourceforge.io/download.html
- **imzML Scout** (Downstream visualization and validation tool; enables viewing of converted imzML files to verify conversion success) — https://github.com/VIU-Metabolomics/imzML_Writer

## Examples

```
import imzml_writer.imzML_Writer as iw; iw_utils.mzML_to_imzML_convert(PATH='/path/to/mzml_files'); iw_utils.imzML_metadata_process(model_files='/path/to/mzml_files', x_speed=100.0, y_step=50.0, path='/path/to/raw_data')
```

## Evaluation signals

- Output imzML files are readable by at least one compatible software (Cardinal MSI, METASPACE, M2aia, MSIReader, SCiLS Lab, or Mozaic).
- Pixel dimensions in imzML header match input scan parameters (X speed × acquisition duration, Y step × number of steps).
- Mass recalibration using lock mass reference produces expected m/z shifts (typically < 5 ppm correction for high-resolution instruments).
- Ion images displayed in imzML Scout show coherent spatial structure consistent with imaging acquisition geometry.
- Metadata elements (imaging coordinates, MS acquisition mode, scan filters) are present in imzML XML header.

## Limitations

- Documentation does not explicitly describe the internal conversion algorithm or pixel alignment mechanism; implementation details are opaque.
- Pixel dimensions must be written as integers for SCiLS Lab compatibility, potentially causing rounding artifacts.
- Lock mass recalibration assumes availability of a suitable internal standard; misidentified lock mass will introduce systematic mass errors.
- Conversion success depends on well-formed mzML input; malformed or incomplete mzML files may produce invalid imzML output.

## Evidence

- [other] Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters.: "Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters."
- [other] Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass recalibration, imaging coordinates, and MS acquisition metadata).: "Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass"
- [readme] Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML.: "Using imzML Writer depends on msconvert for conversion of raw vendor files to the open format mzML."
- [readme] Many imzML file readers are available both commercially and as open-source software. Of the popular software we've tested, file compatible for imzML's generated with imzML_Writer are listed in: "Many imzML file readers are available both commercially and as open-source software. Of the popular software we've tested, file compatible for imzML's generated with imzML_Writer are listed in"
- [methods] Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors: "Lock mass: m/z of a known ion (typically m/z of an internal standard). This serves as a reference point to correct any mass measurement errors"
