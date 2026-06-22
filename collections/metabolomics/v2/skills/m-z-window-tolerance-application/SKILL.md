---
name: m-z-window-tolerance-application
description: Use when after parsing an imzML XML metadata file and loading the corresponding .ibd binary intensity data, when you need to isolate and visualize the spatial distribution of specific isotopes, chemical species, or mass fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pewpew
  - pewlib
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-window-tolerance-application

## Summary

Extract image slices from Imaging Mass Spectrometry binary data (.ibd files) by specifying target m/z values and a mass tolerance window in parts-per-million (ppm). This skill maps mass-to-charge ratios to their corresponding intensity distributions across spatial coordinates, enabling multi-channel image reconstruction.

## When to use

After parsing an imzML XML metadata file and loading the corresponding .ibd binary intensity data, when you need to isolate and visualize the spatial distribution of specific isotopes, chemical species, or mass fragments. Apply this skill for each user-selected or analyst-entered m/z value to build a multi-channel image dataset for downstream analysis (e.g., colocalization, segmentation).

## When NOT to use

- Input data are already in a processed, per-isotope image format (e.g., pre-segmented masks or intensity matrices with m/z already isolated).
- The .ibd file is missing, corrupted, or does not match the imzML metadata (coordinate mismatch or incomplete m/z calibration).
- Mass tolerance is undefined or the instrument mass accuracy is unknown; applying an arbitrary ppm window without calibration may isolate neighboring peaks or miss the target isotope entirely.

## Inputs

- .ibd binary data file (Imaging Mass Spectrometry intensity matrix)
- imzML XML metadata (coordinate system, m/z reference list)
- target m/z value(s) (float or list of floats)
- mass tolerance window (ppm, typically ±5 ppm)

## Outputs

- 2D intensity image slice per target m/z (numpy array or equivalent)
- multi-channel pew² image object (assembled from all m/z slices)
- target masses table (m/z, isotope name, pixel count, intensity statistics)

## How to apply

For each target m/z value, query the .ibd binary file using a mass window defined by the ppm tolerance (e.g., ±5 ppm around the nominal m/z). Sum or aggregate the intensity values across all pixels within that window to produce a 2D image slice. The ppm window accounts for instrument mass accuracy drift and natural isotope peak width, ensuring robust extraction without manual per-mass recalibration. Repeat for all user-selected masses, then assemble the resulting image slices into a multi-channel pew² image object with isotope names and coordinate metadata. Verify extraction by visual inspection of the TIC image and spot-checking single-pixel spectra against expected peak positions.

## Related tools

- **pewlib** (Python library that parses imzML XML, reads .ibd binary data, and provides low-level APIs to extract and aggregate intensity values within a specified m/z tolerance window) — https://github.com/djdt/pewlib
- **pewpew** (GUI application that exposes the m/z window tolerance workflow via an interactive import wizard: displays TIC image, accepts user m/z selections, applies ppm tolerance, and assembles multi-channel output) — https://github.com/djdt/pewpew

## Evaluation signals

- Extracted image slice contains non-NaN intensity values only within the specified ppm tolerance around the target m/z; neighboring masses are excluded.
- Sum or mean intensity of the extracted slice is consistent with the TIC image intensity at that m/z region (sanity check for aggregation correctness).
- Multi-channel image object preserves spatial coordinate metadata (x, y, or laser line indices) and isotope names without loss of dimensionality.
- Single-click spectrum extraction at a known pixel position returns a peak at the target m/z ± ppm tolerance; no spurious peaks outside tolerance.
- Spatial distribution of the extracted m/z image is visually consistent with expected sample chemistry (e.g., element localized to known tissue region or mineral grain).

## Limitations

- Mass accuracy and calibration quality directly affect extraction fidelity; uncalibrated or drifting m/z axes may systematically miss peaks or include noise.
- Overlapping isotopes or isobars within the ppm tolerance window will be co-extracted, requiring downstream deconvolution or manual m/z refinement.
- The .ibd binary format is specific to imzML and instrument-dependent (Agilent, Thermo, PerkinElmer); non-standard formats or corrupted headers will cause import failure.
- No changelog found for pewlib or pewpew; version-specific differences in m/z extraction algorithms or tolerance calculation are not documented.

## Evidence

- [other] For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm) and add to a target masses table.: "For each user-selected or manually-entered m/z value, extract the corresponding image slice from the .ibd at the specified mass window (in ppm)"
- [other] Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list using an XML parser.: "Parse the imzML XML to extract imaging parameters, coordinate systems, and m/z reference list"
- [other] Upon finish, assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata, returning the completed dataset.: "assemble all selected m/z images into a multi-channel pew² image object with isotope names and coordinate metadata"
- [readme] ImzML import wizard for data in the imzML format with mass selection and exploration capabilities.: "ImzML | Import wizard for data in the imzML format | Mass selection and exploration"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib.: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library"
