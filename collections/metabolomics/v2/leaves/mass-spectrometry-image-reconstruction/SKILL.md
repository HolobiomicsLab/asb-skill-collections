---
name: mass-spectrometry-image-reconstruction
description: Use when you have paired .imzML (XML metadata) and .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  tools:
  - pewpew
  - pewlib
  - pewpew (pew²)
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally
  defined threshold
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

# mass-spectrometry-image-reconstruction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reconstruct spatially resolved mass spectrometry images from imzML/ibd file pairs by parsing XML metadata, extracting mass-specific intensity slices from binary data, and assembling multi-channel image objects with isotope annotations and coordinate metadata. This skill enables pixel-level spectral exploration and targeted m/z image generation for imaging mass spectrometry workflows.

## When to use

You have paired .imzML (XML metadata) and .ibd (binary intensity data) files from an imaging mass spectrometry experiment and need to (1) verify file integrity and co-location, (2) explore the total ion chromatogram (TIC) to understand spatial coverage, (3) interactively select or manually specify target m/z values with mass window tolerance (in ppm), and (4) generate calibrated, coordinate-aware multi-channel images for downstream spatial analysis or quantification.

## When NOT to use

- Input data is already in a processed feature-table or matrix format (e.g., CSV intensity matrix); use this skill only for raw imzML/ibd reconstruction.
- The .imzML and .ibd files are in different directories or one file is missing; spatial referencing will fail.
- You need to import LA-ICP-MS data in vendor formats (Agilent .b, Thermo CSV/LDR, PerkinElmer .xl, Nu Vitesse); use format-specific importers instead.

## Inputs

- .imzML XML metadata file (imaging parameters, coordinate systems, m/z reference list)
- .ibd binary intensity data file (co-located with .imzML)
- target m/z value(s) (user-selected or manually entered)
- mass window tolerance in ppm

## Outputs

- multi-channel pew² laser image object (assembled from selected m/z images)
- total ion chromatogram (TIC) visualization
- extracted spectrum at single pixel
- target masses table (m/z values, isotope names, mass windows)

## How to apply

First, verify that both the .imzML XML metadata file and corresponding .ibd binary data file are present in the same directory. Parse the imzML XML using an XML parser to extract imaging parameters (pixel grid, scan pattern), coordinate systems, and the m/z reference list. Compute and display a total ion chromatogram (TIC) image by aggregating all binary intensity values across the m/z dimension, allowing single-click spectrum extraction at any pixel location for interactive exploration. For each target m/z value (either user-selected from the TIC or manually entered), extract the corresponding intensity slice from the .ibd file within the specified mass window tolerance (ppm-based) and record the selected mass in a target masses table. Finally, assemble all selected m/z images into a single multi-channel pew² image object, preserving isotope names, coordinate metadata, and calibration information, and return the completed dataset ready for ROI analysis or quantitative comparisons.

## Related tools

- **pewlib** (Python library that parses imzML XML metadata, reads binary .ibd intensity data, and provides core data structures for image assembly and coordinate mapping) — https://github.com/djdt/pewlib
- **pewpew (pew²)** (GUI application that wraps pewlib to provide interactive TIC visualization, single-click spectrum extraction, manual m/z selection with ppm-based mass windows, and assembly of multi-channel image objects) — https://github.com/djdt/pewpew

## Evaluation signals

- Both .imzML and .ibd files are successfully verified to exist in the same directory before parsing begins.
- TIC image computed from binary intensity aggregation displays expected spatial coverage and signal distribution consistent with experimental design.
- Single-click spectrum extraction at arbitrary pixels returns valid m/z–intensity pairs within the m/z reference range from the parsed XML.
- Each selected m/z slice extracted from .ibd at specified ppm tolerance contains non-NaN intensity values at expected pixel coordinates; mass window boundaries are consistent with tolerance specification.
- Final assembled image object preserves isotope names, coordinate metadata (pixel grid, scan pattern), and calibration data; multi-channel structure matches the count of selected m/z values.

## Limitations

- Requires both .imzML and .ibd files to be co-located and paired; mismatched or missing files will cause parsing or referencing failure.
- Mass window tolerance (ppm) must be specified appropriately for the instrument's mass resolution; inappropriate values may exclude true signal or include noise.
- TIC visualization relies on aggregation across all m/z; sparse or noisy data may obscure weak spatial features.
- No changelog documentation available for version-specific changes or bug fixes.

## Evidence

- [other] Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory.: "Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory."
- [other] Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser.: "Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser."
- [other] Display a total ion chromatogram (TIC) image computed from the aggregated binary intensity data, and allow single-click spectrum extraction at any pixel.: "Display a total ion chromatogram (TIC) image computed from the aggregated binary intensity data, and allow single-click spectrum extraction at any pixel."
- [other] For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table.: "For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table."
- [other] Upon finish, assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata, returning the completed dataset.: "Upon finish, assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata, returning the completed dataset."
- [readme] Import wizard for data in the imzML format. Mass selection and exploration.: "Import wizard for data in the imzML format. Mass selection and exploration."
