---
name: msi-preprocessing-parameter-configuration
description: Use when you have raw line-scan MSI data (from Bruker .d/.baf, converted
  to .mzML, or other supported formats) and need to configure MSIGen before calling
  msigen() to generate image arrays.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyBaf2Sql
  - ProteoWizard MSConvert
  - MSIGen
  - Python
  - Anaconda
  - Miniconda
  - Git
  - Anaconda/Miniconda
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
- you can convert it to the open-source .mzML format using ProteoWizard's MSConvert
  tool. You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html
- You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html.
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI Preprocessing Parameter Configuration

## Summary

Define and validate processing parameters (file paths, mass tolerances, image dimensions, normalization mode) before initializing MSIGen for conversion of raw mass spectrometry imaging line-scan data to visualizable NumPy arrays. This skill ensures correct parameter alignment with input data characteristics and desired output resolution.

## When to use

Apply this skill when you have raw line-scan MSI data (from Bruker .d/.baf, converted to .mzML, or other supported formats) and need to configure MSIGen before calling msigen() to generate image arrays. Specifically use it when you know the physical image dimensions (height, width in pixels or lines), possess a mass list file (.xlsx format with m/z targets), and must decide on mass tolerance windows (MS1, precursor, fragment, and optional ion mobility) to match peaks correctly.

## When NOT to use

- Input is already a processed NumPy array (.npy) with associated metadata JSON — use msigen.load_pixels() instead.
- Mass list is in a non-.xlsx format and no conversion step is performed — MSIGen expects .xlsx by design.
- Image dimensions are unknown and cannot be recovered from acquisition metadata — parameter configuration will fail at runtime.

## Inputs

- Raw MSI data file (Bruker .d/.baf converted to .mzML, or equivalent supported format)
- Mass list file (.xlsx) with target m/z values
- Image acquisition metadata (physical dimensions: height, width in pixels; pixels per line)
- Instrument specifications (mass resolving power or mass accuracy in ppm/Da)

## Outputs

- Configured MSIGen object (msigen instance) ready for get_image_data() call
- Validated parameter dictionary (file paths, tolerances, dimensions, normalization settings)
- Log of parameter choices for reproducibility

## How to apply

Begin by preparing a mass list file in .xlsx format containing target m/z values, and determine physical image dimensions (img_height, img_width in pixels) and pixels per line from your acquisition metadata. Set mass_tolerance_MS1 and mass_tolerance_MS1_units based on your instrument's resolving power (e.g., 5 ppm for high-resolution or 0.1 Da for lower-resolution instruments); if MS/MS data is present, also specify mass_tolerance_prec and mass_tolerance_frag with corresponding units. If ion mobility dimension exists, set mobility_tolerance and mobility_tolerance_units. Choose normalization mode ('TIC', 'intl_std', or None) based on sample complexity and availability of internal standard m/z values. Pass all parameters to the msigen() constructor (example_file, mass_list_dir, mass_tolerance_MS1, mass_tolerance_MS1_units, img_height, img_width, pixels_per_line, normalize_img_sizes, output_file_loc, and optional normalize). The rationale: correct tolerances prevent false peak matches or missed peaks; accurate dimensions prevent pixel mapping errors; normalization choice affects downstream quantitative interpretation.

## Related tools

- **MSIGen** (Main processing engine that accepts configured parameters and generates image arrays from line-scan MSI data) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Prerequisite for converting Bruker .d/.baf data to readable format before parameter configuration if starting from raw Bruker files) — https://github.com/gtluu/pyBaf2Sql
- **ProteoWizard MSConvert** (Alternative tool to convert Bruker .d/.baf to .mzML format before MSIGen parameter configuration) — https://proteowizard.sourceforge.io/download.html
- **Anaconda/Miniconda** (Python environment manager for creating isolated environment (Python >=3.9 and <=3.11) in which MSIGen parameters are configured) — https://www.anaconda.com/download

## Examples

```
msigen_gen = msigen(example_file='/path/to/data.mzML', mass_list_dir='/path/to/mass_list.xlsx', mass_tolerance_MS1=5, mass_tolerance_MS1_units='ppm', img_height=100, img_width=150, pixels_per_line=150, normalize_img_sizes=True, output_file_loc='/output/dir/')
```

## Evaluation signals

- All required parameters (example_file, mass_list_dir, mass_tolerance_MS1, img_height, img_width, pixels_per_line) are non-null and of expected types (string paths, numeric tolerances, integers for dimensions).
- Mass tolerance values are physically plausible (e.g., 1–20 ppm for high-resolution MS; 0.05–0.5 Da for lower-resolution; mobility tolerance in range 0.01–0.1 1/K0 if applicable).
- Image dimensions (img_height × img_width) match the total expected pixel count from acquisition metadata (e.g., number_of_lines × pixels_per_line).
- Subsequent call to get_image_data(verbose=True) completes without ValueError or KeyError related to missing parameters or type mismatches.
- Output NumPy array (pixels.npy) has shape (num_masses, img_height, img_width) matching configured dimensions and mass list length; metadata JSON contains entries for all configured tolerance windows and normalization mode.

## Limitations

- Parameter configuration assumes mass list is already in .xlsx format; no automatic format conversion is provided within MSIGen.
- Ion mobility tolerance is only applicable if input data contains ion mobility dimension (e.g., TIMS-TOF); setting mobility_tolerance on non-mobility data has no effect but does not error.
- Normalization to internal standard ('intl_std' mode) requires that the internal standard m/z is present in the mass list; if absent, normalization defaults to TIC without warning.
- Image dimensions must be known a priori from acquisition metadata; MSIGen cannot auto-detect dimensions from .mzML metadata and will fail if dimensions are misspecified.
- Python version must be >=3.9 and <=3.11 for pyBaf2Sql compatibility; versions outside this range may cause installation or runtime errors during parameter setup.

## Evidence

- [methods] Define processing parameters including file path, mass list, tolerances, image dimensions: "example_file, mass_list_dir, mass_tolerance_MS1, img_height, img_width, normalize_img_sizes, pixels_per_line, output_file_loc"
- [methods] MSIGen processes MSI data with mass and dimension configuration: "mass_tolerance_MS1, mass_tolerance_MS1_units for matching m/z values in MS1 spectra"
- [methods] Ion mobility tolerance filtering for multi-dimensional MSI: "mobility_tolerance, mobility_tolerance_units for matching ion mobility values"
- [methods] Normalization mode selection during parameter configuration: "normalize = 'TIC' to normalize the images to total ion current"
- [methods] Environment and version constraints for parameter setup: "Using an environment with python version >=3.9 and <=3.11"
- [methods] MSIGen initialization with configured parameters: "MSIGen_generator = msigen(example_file=example_file, mass_list_dir=mass_list_dir, ...)"
- [methods] Mass list file format requirement: "An example mass list file is included in the GitHub repository (https://github.com/LabLaskin/MSIGen/blob/main/other_files/example_mass_list.xlsx)"
- [methods] Precursor and fragment ion tolerance for MS/MS data: "mass_tolerance_prec, mass_tolerance_prec_units for precursor ions in MS2 spectra"
