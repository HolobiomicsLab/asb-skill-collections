---
name: ppm-mass-accuracy-filtering
description: Use when when processing imzML/ibd Imaging Mass Spectrometry datasets and you need to extract ion density maps for specific analytes or isotopes. Apply this skill after importing the .imzML metadata and .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pewpew
  - pewlib
  - pewpew (pew²)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ppm-mass-accuracy-filtering

## Summary

Extract ion images from Imaging Mass Spectrometry data by selecting specific m/z values within a user-defined parts-per-million (ppm) mass window tolerance. This skill filters the binary intensity data to isolate signals at target masses, enabling multi-channel image construction for spatial metabolite or element mapping.

## When to use

When processing imzML/ibd Imaging Mass Spectrometry datasets and you need to extract ion density maps for specific analytes or isotopes. Apply this skill after importing the .imzML metadata and .ibd binary files, viewing the total ion chromatogram (TIC), and deciding which m/z values to image. Trigger this skill for each target mass (either user-selected interactively or manually entered) to build a multi-channel pew² image object.

## When NOT to use

- Input data is already a pre-processed feature table or abundance matrix (not raw binary IMS data).
- .imzML and .ibd files are in different directories or one is missing (workflow requires both files co-located).
- ppm tolerance is set so wide that it captures overlapping m/z signals from distinct analytes (mass ambiguity will result).

## Inputs

- .ibd binary data file (Imaging Mass Spectrometry intensity matrix)
- .imzML XML metadata file (imaging parameters, coordinate systems, m/z reference list)
- target m/z value(s) (numeric, user-selected or entered)
- ppm mass window tolerance (numeric, typically 5–10 ppm)

## Outputs

- extracted m/z image slice (2D spatial intensity array)
- target masses table (m/z, isotope name, coordinates)
- multi-channel pew² image object (all selected m/z images assembled with metadata)

## How to apply

For each user-selected or manually-entered m/z value, query the .ibd binary data file to extract intensity values at that mass within a specified ppm tolerance window. The ppm window defines the mass accuracy threshold (e.g., ±5 ppm around the nominal m/z) and should be set based on the instrument's mass resolution and the analyte's expected isotope pattern. Extract the corresponding image slice—a 2D spatial array of intensities at that m/z—and add it to a target masses table. Repeat for all desired analytes, then assemble all extracted m/z images into a single multi-channel pew² image object with isotope names and coordinate metadata. Verify that extracted images have non-zero signal intensity and that m/z values fall within the reference m/z list parsed from the imzML XML.

## Related tools

- **pewlib** (Python library that implements .ibd binary parsing, m/z extraction, and image slicing within the specified ppm window) — https://github.com/djdt/pewlib
- **pewpew (pew²)** (GUI wrapper that provides interactive m/z selection, TIC visualization, single-click spectrum extraction, and assembly of multi-channel images with ppm tolerance configuration) — https://github.com/djdt/pewpew

## Evaluation signals

- Extracted m/z image has spatial structure matching the imaging coordinates (non-uniform intensity, not all NaN or zero).
- All returned m/z values fall within the reference m/z list from the imzML XML and satisfy the ppm tolerance constraint: |observed_mz - nominal_mz| / nominal_mz × 1e6 ≤ ppm_window.
- Multi-channel image object contains the correct number of channels (matching the number of target masses selected) and each channel has valid coordinate metadata from the imzML.
- Pixel-level intensity values in each m/z image slice are non-negative and within the dynamic range of the instrument (no spurious negative or overflow values).
- Target masses table is populated with all user-selected m/z values, isotope names, and associated coordinate system labels from the imzML header.

## Limitations

- Requires .imzML and .ibd files to be in the same directory; mismatched or missing files will cause import failure.
- ppm tolerance is static across all m/z extractions; overlapping analyte signals with similar m/z will not be resolved and may co-extract.
- Single-click spectrum extraction requires visual inspection of the TIC image; automated m/z selection (e.g., peak-picking) is not built into the imzML import wizard.
- No built-in deconvolution of complex isotope patterns; extracted image at a given m/z may contain contributions from multiple isotopologues if ppm window is too wide.

## Evidence

- [other] For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm): "For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table."
- [other] Display a total ion chromatogram (TIC) image computed from the aggregated binary intensity data, and allow single-click spectrum extraction at any pixel.: "Display a total ion chromatogram (TIC) image computed from the aggregated binary intensity data, and allow single-click spectrum extraction at any pixel."
- [other] Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser.: "Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser."
- [other] Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory.: "Accept paths to .imzML XML metadata file and .ibd binary data file, verify both files are present in the same directory."
- [readme] ImzML | Import wizard for data in the imzML format | Mass selection and exploration: "ImzML | Import wizard for data in the imzML format | Mass selection and exploration"
