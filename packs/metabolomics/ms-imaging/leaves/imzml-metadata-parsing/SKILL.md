---
name: imzml-metadata-parsing
description: Use when you have received paired .imzML (XML metadata) and .ibd (binary data) files from an Imaging Mass Spectrometry instrument and need to discover the imaging geometry, m/z calibration, and scan coordinate system before extracting mass images or computing total ion chromatograms (TIC).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pewpew
  - pewlib
  - pewpew (pew²)
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imzML Metadata Parsing

## Summary

Extract imaging parameters, coordinate systems, and m/z reference lists from imzML XML metadata files to enable structured access to Imaging Mass Spectrometry dataset configuration. This skill bridges raw imzML/ibd file pairs and downstream mass-image extraction by validating file integrity and populating the coordinate and spectral metadata needed for pixel-level data access.

## When to use

You have received paired .imzML (XML metadata) and .ibd (binary data) files from an Imaging Mass Spectrometry instrument and need to discover the imaging geometry, m/z calibration, and scan coordinate system before extracting mass images or computing total ion chromatograms (TIC). Apply this skill as the first step in the imzML import workflow whenever both files are present in the same directory.

## When NOT to use

- Input files are in non-imzML formats (e.g., Agilent .b, Thermo CSV, NetCDF); use vendor-specific importers instead.
- Only the .imzML file is present without a paired .ibd binary file; the skill requires both files to succeed.
- The imzML metadata file is corrupted or does not conform to the imzML schema; parsing will fail or produce incomplete metadata.

## Inputs

- .imzML XML metadata file
- .ibd binary mass spectrometry data file
- Directory path containing both paired files

## Outputs

- Parsed imaging parameters (acquisition mode, scan type)
- Coordinate system metadata (x, y, z ranges; pixel/voxel dimensions)
- m/z reference list (mass-to-charge values, calibration coefficients)
- Validated metadata object for downstream mass-image extraction

## How to apply

Verify that both the .imzML XML metadata file and .ibd binary data file are present in the same directory. Parse the imzML XML document using an XML parser to extract imaging acquisition parameters (e.g., line-by-line, spot-wise, or ablation-time-aligned geometry), the coordinate reference system for pixel/voxel locations, and the complete m/z reference list used to index the binary data. Validate that the m/z list and binary data dimensions are internally consistent (e.g., number of m/z values matches the spectral channels in .ibd). Return the extracted metadata as structured fields (imaging mode, coordinate bounds, m/z array, calibration coefficients if present) suitable for downstream mass-image slicing and coordinate mapping. Success is indicated by error-free XML parsing, non-empty m/z list, and consistency between declared and actual data dimensions.

## Related tools

- **pewlib** (Python library that implements XML parsing and metadata extraction for imzML files; provides data structure and calibration support) — https://github.com/djdt/pewlib
- **pewpew (pew²)** (GUI application that wraps pewlib imzML import wizard; displays parsed metadata and enables interactive m/z selection) — https://github.com/djdt/pewpew

## Evaluation signals

- XML parser completes without error and returns a non-null metadata object
- m/z reference list is non-empty and sorted in ascending order; all values are positive numbers (typically 10–3000 for MS)
- Coordinate metadata (x_min, x_max, y_min, y_max) form valid ranges; pixel counts match declared dimensions in .ibd
- Imaging mode field is populated with a recognized value ('line', 'spot', 'ablation-time-aligned')
- Paired .imzML and .ibd files are confirmed to exist in the same directory before parsing begins

## Limitations

- imzML metadata parsing does not validate the binary .ibd file contents; only XML schema compliance is checked.
- Coordinate system extraction assumes imzML v1.x standard; non-standard or custom imzML extensions may not be recognized.
- Large imzML files (>100 MB) may require in-memory XML parsing; streaming or chunked parsing is not addressed by this skill.
- No changelog or version history available in the repository to track imzML format compatibility across pewlib releases.

## Evidence

- [other] Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory.: "Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory."
- [other] Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser.: "Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
- [readme] Import wizard for data in the imzML format | Mass selection and exploration: "ImzML | Import wizard for data in the imzML format | Mass selection and exploration"
- [readme] pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
