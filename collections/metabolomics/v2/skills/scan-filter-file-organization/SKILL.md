---
name: scan-filter-file-organization
description: Use when when converting mzML files to imzML format and the source mzML
  contains multiple scan filters (e.g., different MS/MS isolation windows, ionization
  modes, or mass ranges acquired in a single imaging experiment).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - imzML Writer
  - msconvert
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# scan-filter-file-organization

## Summary

Organize mass spectrometry imaging data files by scan filter type during mzML-to-imzML conversion, ensuring that output imzML files preserve the instrumental scan configuration metadata embedded in source mzML files. This skill is essential for maintaining data provenance and enabling downstream analysis tools to correctly interpret imaging acquisition parameters.

## When to use

When converting mzML files to imzML format and the source mzML contains multiple scan filters (e.g., different MS/MS isolation windows, ionization modes, or mass ranges acquired in a single imaging experiment). Scan filter organization becomes necessary when: (1) you have heterogeneous acquisition modes in a single raw file, (2) you need to preserve which pixels belong to which acquisition configuration, or (3) you are preparing data for analysis tools that require homogeneous scan settings per file.

## When NOT to use

- Input mzML files contain only a single, uniform scan filter (no heterogeneous acquisition modes); organize by a simpler scheme.
- Output is destined for visualization-only analysis (e.g., viewing ion images in imzML Scout); scan filter organization is unnecessary for single-image rendering.
- Raw vendor files have not yet been converted to mzML; this skill applies post-msconvert, not to raw .raw or proprietary formats.

## Inputs

- mzML files containing one or more scan filters
- X scan speed parameter (µm/s)
- Y step size parameter (µm)
- Lock mass value (m/z)
- MS data mode specification (Centroid or Profile)

## Outputs

- imzML files organized by scan filter
- Directory structure sorted according to scan filter classes
- Annotated imzML metadata reflecting scan filter assignments

## How to apply

After calling iw_utils.mzML_to_imzML_convert() to generate barebones imzML structure with pixel alignment based on X scan speed (µm/s) and Y step size (µm) parameters, extract the scan filter metadata from source mzML files and group output imzML files by their corresponding scan filter identifiers. During the metadata annotation step (iw_utils.imzML_metadata_process()), pass the scan filter information to correctly assign experimental parameters (lock mass, imaging coordinates, MS acquisition metadata) to each scan-filter-specific imzML file. Place each annotated imzML file in the output directory using a directory structure or filename convention that reflects its scan filter class, enabling downstream tools to rapidly identify and load acquisition-homogeneous datasets.

## Related tools

- **imzML Writer** (Executes mzML-to-imzML conversion and file organization via iw_utils.mzML_to_imzML_convert() and iw_utils.imzML_metadata_process() functions; provides GUI for specifying scan parameters and output directory structure.) — https://github.com/VIU-Metabolomics/imzML_Writer
- **msconvert** (Converts raw vendor files to mzML format upstream; embeds scan filter metadata in mzML scan headers that are later extracted during organization.) — https://proteowizard.sourceforge.io/download.html

## Examples

```
from imzml_writer import iw_utils
iw_utils.mzML_to_imzML_convert(PATH='/path/to/mzML_files')
iw_utils.imzML_metadata_process(model_files='/path/to/mzML_files', x_speed=500, y_step=50, path='/output/directory')
```

## Evaluation signals

- Verify that each output imzML file contains scan events from only one scan filter class by inspecting the <scanList> elements in the imzML XML header.
- Confirm that pixel coordinates (X, Y) are correctly aligned within each scan-filter-specific imzML, matching expected imaging raster dimensions derived from X scan speed and Y step size.
- Check that metadata annotations (lock mass, imaging coordinates, MS acquisition parameters) are present and consistent across all pixels within a single scan-filter imzML file.
- Validate that the output directory structure or filename convention unambiguously identifies the scan filter for each imzML file, enabling automated batch processing downstream.
- Cross-reference output imzML files against source mzML scan headers to ensure no scan filter groups are missing and no spurious cross-filter assignments exist.

## Limitations

- Documentation does not explicitly detail the internal algorithm by which scan filters are identified and grouped from mzML <scan> elements; reverse-engineering may be required for complex heterogeneous acquisition modes.
- imzML Writer does not provide a preview or validation UI for scan filter organization before conversion; users must verify output manually or through downstream tools.
- Scan filter organization is only applied during the mzML-to-imzML conversion step; if you use the 'Write imzML Metadata' option alone on previously converted imzML files, scan filter re-organization is not performed.

## Evidence

- [other] Place annotated imzML files in the output directory, organized by scan filter as specified in the source mzML files.: "Place annotated imzML files in the output directory, organized by scan filter as specified in the source mzML files."
- [other] Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters.: "Call iw_utils.mzML_to_imzML_convert(PATH=mzML_path) to write barebones imzML structure and align pixels according to X scan speed (µm/s) and Y step size (µm) parameters."
- [other] Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass recalibration, imaging coordinates, and MS acquisition metadata).: "Call iw_utils.imzML_metadata_process(model_files=mzML_path, x_speed=x_scan_speed, y_step=y_step_size, path=raw_data_path) to annotate imzML files with experimental parameters (lock mass for mass"
- [methods] Select one of the conversion options (i.e., Full Conversion, mzML to imzML, or Write imzML Metadata): "Select one of the conversion options (i.e., Full Conversion, mzML to imzML, or Write imzML Metadata)"
