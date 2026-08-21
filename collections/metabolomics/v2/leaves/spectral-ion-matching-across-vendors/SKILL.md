---
name: spectral-ion-matching-across-vendors
description: Use when you have raw line-scan MSI data from any supported vendor (Agilent
  .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3755
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - pyBaf2Sql
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you want to use MSIGen in a Jupyter notebook, you may also need to install jupyter
  notebook
- MSIGen is most easily used through Jupyter Notebooks or through the GUI.
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
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

# Spectral Ion Matching Across Vendors

## Summary

Match observed m/z values and ion mobility features from line-scan mass spectrometry imaging data to a curated mass list across multiple vendor formats (Agilent, Bruker, Thermo) by applying tolerance thresholds for MS1, precursor, fragment, and mobility dimensions. This skill enables vendor-agnostic ion detection and localization in raw MSI data before pixel-level binning and visualization.

## When to use

Apply this skill when you have raw line-scan MSI data from any supported vendor (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML) and a curated mass list (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion mobility columns), and you need to localize specific ions in 2D space by matching observed spectral features to expected m/z and mobility values within predefined tolerances.

## When NOT to use

- Input MSI data is not line-scan format (e.g., already a raster image or 2D array) — use direct image loading instead
- Mass list is empty or malformed — validation must precede matching
- Tolerance parameters are not calibrated for your instrument; excessively loose tolerances will create false matches and excessively tight tolerances will miss true ions

## Inputs

- Raw line-scan MSI data file (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML)
- Mass list file (Excel .xlsx or CSV with columns: m/z, precursor m/z, fragment m/z, ion mobility)
- MS1 mass tolerance value and unit (ppm or mz)
- Precursor ion mass tolerance value and unit
- Fragment ion mass tolerance value and unit
- Ion mobility tolerance value and unit (1/K0 or μs)
- Image acquisition geometry (scanned area height, width, unit)

## Outputs

- 3D NumPy array pixels.npy with shape (n+1, y, x) where n = number of matched masses, plus one TIC image
- JSON metadata file pixels_metadata.json containing matched ion identities, tolerances applied, and imaging parameters
- Console log (verbose=True) showing extraction, matching, and binning progress

## How to apply

Define four independent tolerance parameters—MS1 mass tolerance (ppm or mz for parent ions), precursor ion tolerance, fragment ion tolerance, and ion mobility tolerance (1/K0 or μs)—based on your instrument's mass accuracy and resolving power. Initialize the MSIGen object with the input file path, mass list file, all tolerance parameters, and image geometry (scanned area height, width, pixels per line). Call get_image_data(verbose=True) to extract spectra from all spatial locations, bin each spectrum's peaks, and match observed m/z and mobility values against the mass list. MSIGen returns a 3D array (n+1, y, x) where n is the number of matched masses plus one TIC image; verify that all expected ions are present in the output metadata and that the array dimensions match your image geometry.

## Related tools

- **MSIGen** (Core Python package that implements spectral extraction, m/z matching, ion mobility matching, and spatial binning across vendor file formats) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Enables MSIGen to parse Bruker .baf format data by wrapping Bruker's Baf2Sql library) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Runtime environment (≥3.9 and ≤3.11) for executing MSIGen matching logic)
- **Jupyter Notebook** (Interactive interface for defining tolerance parameters, executing matching, and inspecting output metadata) — https://github.com/LabLaskin/MSIGen/blob/main/other_files/MSIGen_jupyter.ipynb

## Examples

```
metadata, pixels = MSIGen_generator.get_image_data(verbose=True)
```

## Evaluation signals

- Output array dimensions (n+1, y, x) match the input image geometry: y = scanned area height in pixels, x = width in pixels, n = number of rows in mass list
- All rows in the mass list appear in the output metadata with their m/z, precursor m/z, fragment m/z, and ion mobility values matched or tagged as unmatched
- Verbose output log shows zero failed extraction steps and reports the number of spectra extracted from each spatial location
- Pixel intensity values in the output array are non-negative and within the expected range (e.g., 0 to 1e6 counts) for the input instrument and acquisition duration
- Random spot-checks of matched ions in 2–3 spatial locations confirm that observed m/z values fall within the specified tolerance of the mass list entries

## Limitations

- Matching accuracy depends critically on calibration of tolerance parameters; instruments with poor mass accuracy will require very loose tolerances, increasing false-match risk
- Bruker .baf format matching requires separate installation of pyBaf2Sql from GitHub; this is not bundled with the main MSIGen pip package
- Ion mobility matching is optional and only functions if the input mass list contains ion mobility values and the raw data includes mobility information (e.g., Bruker timsTOF)
- Matching is performed per-spectrum without spatial context; co-localization of multiple ions or spatial validation is not part of this workflow step
- Python version constraint (≥3.9 and ≤3.11, specifically <3.12) may conflict with other dependencies in some environments

## Evidence

- [other] how does MSIGen convert raw line-scan mass spectrometry imaging data into a standardized NumPy pixel array and accompanying JSON metadata file?: "MSIGen converts raw line-scan MSI data to a visualizable format by processing the data through a pipeline that generates both a NumPy pixel array and JSON metadata as intermediate outputs"
- [other] tolerance parameters explained: "Define processing parameters: specify the input file path (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML), mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion"
- [other] get_image_data matching process: "call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances, bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number"
- [methods] vendor format support: "MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures"
- [readme] pyBaf2Sql dependency for Bruker: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
