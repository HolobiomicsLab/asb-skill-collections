---
name: data-format-validation-and-integrity-checking
description: Use when after converting raw Bruker .d/.baf or other proprietary mass spectrometry imaging formats using pyBaf2Sql or ProteoWizard MSConvert, or after running MSIGen's get_image_data() function.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyBaf2Sql
  - ProteoWizard MSConvert
  - MSIGen
  - Python
  - Anaconda
  - Miniconda
  - Git
  techniques:
  - MS-imaging
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub
- you can convert it to the open-source .mzML format using ProteoWizard's MSConvert tool. You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html
- You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html.
- MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures.
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

# data-format-validation-and-integrity-checking

## Summary

Verify that mass spectrometry imaging data has been correctly converted to expected formats (mzML, NumPy arrays, JSON metadata) and contains required mass spectrometry metadata fields (m/z, intensity, mobility) before downstream processing. This skill ensures data integrity and readability as a prerequisite to successful image generation.

## When to use

After converting raw Bruker .d/.baf or other proprietary mass spectrometry imaging formats using pyBaf2Sql or ProteoWizard MSConvert, or after running MSIGen's get_image_data() function. Use this skill whenever you need assurance that the converted output is readable, complete, and contains the expected mass spectrometry metadata before passing it to image visualization or quantitative analysis pipelines.

## When NOT to use

- If the raw instrument file (Bruker .d, .raw, or other vendor format) has not yet been converted to a standardized format like mzML or processed by MSIGen—validation applies only to converted outputs, not raw files.
- If you are only performing exploratory metadata inspection and do not plan to feed data into MSIGen or image visualization—lightweight format inspection suffices instead.
- If the conversion step explicitly failed with error messages—address the conversion failure first rather than validating incomplete output.

## Inputs

- Converted mzML file (ProteoWizard MSConvert output)
- pyBaf2Sql-processed Bruker .baf data (as pd.DataFrame or handle-based object)
- MSIGen output pixels.npy file
- MSIGen output metadata.json file

## Outputs

- Validation report (console output or log) confirming file readability and metadata presence
- Confirmed readable NumPy array (pixels) with shape (pixels_per_line, img_height, num_masses)
- Confirmed readable metadata JSON with m/z, intensity, and mobility fields
- Pass/fail status for downstream processing eligibility

## How to apply

After conversion or processing, load the output file (converted .mzML file, pyBaf2Sql-processed .baf data, or MSIGen-generated NumPy array and JSON metadata) and verify: (1) the file is readable without I/O errors; (2) core mass spectrometry metadata fields are present (m/z values, intensity arrays, and ion mobility values if applicable); (3) the data structure matches expected dimensions (for NumPy arrays: shape should correspond to pixels_per_line × image_height × number of m/z targets). Use MSIGen's get_image_data(verbose=True) in Python to receive detailed console output confirming successful conversion to pixels.npy and metadata JSON; examine the console output and file existence. For pyBaf2Sql outputs, iterate through the Spectra DataFrame and verify LineMzId and LineIntensityId handles return valid double arrays. Rationale: raw conversion can fail silently or produce truncated files; explicit validation before downstream use prevents propagation of corrupted data into image arrays.

## Related tools

- **ProteoWizard MSConvert** (Converts Bruker .d/.baf files to mzML format; output is validated for file existence and m/z/intensity metadata presence) — https://proteowizard.sourceforge.io/download.html
- **pyBaf2Sql** (Processes Bruker .baf data and returns Spectra DataFrame with LineMzId and LineIntensityId handles; validation checks that DataFrame is non-empty and handles return valid double arrays) — https://github.com/gtluu/pyBaf2Sql
- **MSIGen** (Orchestrates conversion and outputs pixels.npy and metadata.json; get_image_data(verbose=True) provides validation output confirming successful conversion) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment for pyBaf2Sql Spectra iteration, NumPy array shape inspection, and JSON metadata parsing; version >=3.9 and <=3.11 required)

## Examples

```
metadata, pixels = MSIGen_generator.get_image_data(verbose=True); assert pixels.shape == (pixels_per_line, img_height, len(metadata['mass_list'])), 'Shape mismatch'; import json; m = json.load(open('metadata.json')); assert 'mass_list' in m and 'intensity_data' in m, 'Missing metadata keys'
```

## Evaluation signals

- File is readable without I/O errors (confirmed by successful load of pixels.npy and metadata.json or by non-null Spectra DataFrame from pyBaf2Sql)
- NumPy array shape matches expected dimensions: (pixels_per_line, img_height, number_of_m/z_targets)
- Metadata JSON contains all required keys: m/z list, intensity mappings, and (if applicable) ion mobility values
- Console output from get_image_data(verbose=True) reports 'successful conversion' without error messages
- For pyBaf2Sql: all frames in Spectra DataFrame have non-NaN LineMzId and LineIntensityId values; read_double() calls return arrays of expected length (> 0 peaks per frame)

## Limitations

- Validation checks file format and metadata presence but does not verify chemical correctness or expected m/z distribution (e.g., does not detect swapped ion channels or inverted intensity scales).
- pyBaf2Sql requires Python environment >=3.9 and <=3.11; validation cannot be performed in other Python versions without reinstallation.
- ProteoWizard MSConvert validation is limited to mzML schema compliance; user must visually inspect a subset of spectra to confirm correct m/z and intensity values.
- JSON metadata format is MSIGen-specific; validation of mzML or other standard formats requires format-specific schema validators outside MSIGen.

## Evidence

- [other] Verify converted .mzML file or pyBaf2Sql-processed data is readable and contains expected mass spectrometry metadata (m/z, intensity, mobility if applicable).: "Verify converted .mzML file or pyBaf2Sql-processed data is readable and contains expected mass spectrometry metadata (m/z, intensity, mobility if applicable)."
- [other] Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON without errors.: "Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON without errors."
- [readme] Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode.: "Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode."
- [methods] metadata, pixels = MSIGen_generator.get_image_data(verbose=True): "metadata, pixels = MSIGen_generator.get_image_data(verbose=True)"
- [methods] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
