---
name: binary-spectral-data-extraction
description: Use when you have parsed imzML XML metadata and loaded the corresponding
  .ibd binary intensity file, and need to extract specific ion images at one or more
  target m/z values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3173
  tools:
  - pewpew
  - pewlib
  - pewpew (pew²)
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: restricted
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

# binary-spectral-data-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract mass-to-charge (m/z) image slices from binary imzML/ibd Imaging Mass Spectrometry data files at user-specified masses within a defined mass window tolerance. This skill enables selective ion image construction for downstream quantification and spatial analysis of LA-ICP-MS or IMS datasets.

## When to use

Apply this skill when you have parsed imzML XML metadata and loaded the corresponding .ibd binary intensity file, and need to extract specific ion images at one or more target m/z values. Typical triggers include: (1) after TIC inspection to identify regions of interest, (2) when you have a predefined list of isotopes or analytes to image, or (3) when you need to build a multi-channel image object with isotope-specific intensity data at mass-window-corrected precision.

## When NOT to use

- Input is already a processed feature table or intensity matrix (e.g., CSV of m/z vs. intensity); this skill is for raw binary extraction only.
- imzML and .ibd files are not co-located or only one file is present; verify file integrity first.
- Mass window is not defined or calibration is unknown; establish instrumental mass resolution or ppm tolerance before extraction.

## Inputs

- .imzML XML metadata file (parsed into coordinate system and m/z reference list)
- .ibd binary data file (co-located with .imzML)
- Target m/z value(s) (user-selected or predefined list)
- Mass window in ppm (instrument-specific tolerance, typically 5–50 ppm)

## Outputs

- Multi-channel pew² image object (one channel per target m/z)
- Per-channel metadata: m/z center, isotope name, ppm window bounds, pixel-level intensity arrays
- Coordinate metadata preserved from original imzML (pixel x, y, ablation time if available)

## How to apply

After confirming both .imzML and .ibd files are co-located and XML metadata has been parsed to extract the m/z reference list and imaging parameters (pixel coordinates, scan order), iterate over each target m/z value. For each mass, query the .ibd binary payload using the mass window (in ppm) to define upper and lower m/z bounds, then extract all pixel-level intensity values at that mass and assemble into a 2D image array aligned to the original pixel grid. Populate metadata (isotope name, m/z center, ppm tolerance) for each extracted slice. Aggregate all selected m/z images into a multi-channel image object with consistent coordinate metadata before returning. Rationale: ppm-window queries account for instrument mass resolution; binary-level access avoids re-parsing the entire dataset; metadata preservation ensures downstream analysis (calibration, segmentation, export) can reference mass and spatial provenance.

## Related tools

- **pewlib** (Core Python library that parses imzML/ibd binary data, extracts intensity slices at specified m/z, and assembles multi-channel image objects with coordinate metadata.) — https://github.com/djdt/pewlib
- **pewpew (pew²)** (GUI application wrapping pewlib; provides interactive TIC visualization, single-click spectrum extraction, and dialog-driven m/z selection and image assembly for imzML import workflow.) — https://github.com/djdt/pewpew

## Evaluation signals

- Verify extracted image array shape matches expected pixel grid dimensions from imzML coordinate metadata (x × y pixel count).
- Check that all m/z images are aligned to the same pixel coordinate system; overlay should have no spatial drift.
- Confirm intensity values are populated only within the specified ppm mass window; pixels outside the window or with no signal are set to NaN.
- Validate that m/z center and isotope name metadata are correctly propagated from user input to output multi-channel object.
- Spot-check a single pixel spectrum: extract intensity at that (x, y) across all target m/z channels and verify values match the original binary data within rounding tolerance.

## Limitations

- imzML specification does not mandate a single canonical coordinate system; rotated, flipped, or non-uniformly sampled pixel grids may require custom alignment logic beyond basic parsing.
- Binary .ibd file format is not fully standardized; vendor-specific metadata in imzML may require different parsing strategies for Agilent, Thermo, or PerkinElmer instruments.
- Mass window (ppm) must be defined before extraction; no automatic mass calibration is performed; uncalibrated data will produce systematically offset m/z queries.
- Large datasets (e.g., high-resolution IMS with millions of pixels or thousands of m/z values) may exceed memory if naively extracting all slices; streaming or tile-based extraction may be necessary.

## Evidence

- [other] Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory.: "Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory."
- [other] Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser.: "Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser."
- [other] For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table.: "For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table."
- [other] Upon finish, assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata, returning the completed dataset.: "Upon finish, assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata, returning the completed dataset."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library [pewlib]"
- [readme] ImzML: Import wizard for data in the imzML format, Mass selection and exploration: "ImzML: Import wizard for data in the imzML format, Mass selection and exploration"
