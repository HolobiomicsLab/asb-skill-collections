---
name: mass-spectrometry-imaging-line-scan-data-handling
description: Use when you have raw line-scan MSI data from a vendor instrument (Agilent, Bruker, Thermo, or open-source .mzML format) and need to extract ion images for specified m/z targets with spatial binning and tolerance-based filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - pyBaf2Sql
  - GUI tool (make GUI shortcut.py)
  - MSIGen_CLI.py
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you want to use MSIGen in a Jupyter notebook, you may also need to install jupyter notebook
- MSIGen is most easily used through Jupyter Notebooks or through the GUI.
- If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-imaging-line-scan-data-handling

## Summary

Convert raw line-scan mass spectrometry imaging (MSI) data from vendor formats (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML) into standardized NumPy pixel arrays and JSON metadata for downstream visualization and quantification. This skill is essential for preparing nano-DESI MSI and other line-scan acquisition modes into a uniform array representation indexed by m/z, spatial position, and optional ion mobility.

## When to use

Use this skill when you have raw line-scan MSI data from a vendor instrument (Agilent, Bruker, Thermo, or open-source .mzML format) and need to extract ion images for specified m/z targets with spatial binning and tolerance-based filtering. Apply it at the start of an MSI analysis pipeline when you need reproducible, normalized pixel arrays and accompanying metadata for subsequent visualization, quantification, or statistical analysis.

## When NOT to use

- Input is already a processed pixel array (pixels.npy) or a pre-made visualization — use load_pixels() instead to reload existing arrays.
- Line-scan data has been acquired in raster or orthogonal grid mode rather than continuous line motion — MSIGen is designed specifically for line-scan geometries.
- Raw data is from a non-supported vendor format or custom binary format without mzML or vendor SDK conversion — preprocessing to a supported format is required first.

## Inputs

- Raw vendor MSI file (Agilent .d, Bruker .tsf, Bruker .baf, Bruker .tdf, Thermo .raw, or mzML)
- Mass list file (Excel .xlsx or CSV with columns for m/z, precursor m/z, fragment m/z, and/or ion mobility)
- Image acquisition geometry (scanned area height and width in mm or other units)

## Outputs

- pixels.npy: 3D NumPy array of shape (n+1, y, x) with n target ion images plus TIC
- pixels_metadata.json: JSON metadata file with m/z values, tolerance settings, image dimensions, spatial binning info, and normalization parameters

## How to apply

Install MSIGen via pip with Python ≥3.9 and ≤3.11, optionally including pyBaf2Sql for Bruker .baf support. Define processing parameters: specify the input file path, a mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion mobility columns), and tolerance windows (MS1, precursor, fragment, and mobility tolerances in ppm, mz, 1/K0, or μs units). Set image acquisition parameters: scanned area height and width, and whether to normalize all images to the same pixel count per line using max, min, or mean. Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z and mobility values within tolerances, bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of target masses plus one TIC image. Verify output files pixels.npy and pixels_metadata.json are written to the output directory with correct dimensions and all metadata fields populated.

## Related tools

- **MSIGen** (Core pipeline for converting raw line-scan MSI data to standardized pixel arrays and metadata via m/z matching, spatial binning, and normalization) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Optional dependency for reading Bruker .baf format files via wrapper around Bruker's Baf2Sql data access library) — https://github.com/gtluu/pyBaf2Sql
- **Jupyter Notebook** (Execution environment for interactive pipeline control using MSIGen_jupyter.ipynb template from repository) — https://github.com/LabLaskin/MSIGen/blob/main/other_files/MSIGen_jupyter.ipynb
- **GUI tool (make GUI shortcut.py)** (Desktop graphical interface for parameter entry and pipeline execution without command-line knowledge) — https://github.com/LabLaskin/MSIGen/tree/main/other_files
- **MSIGen_CLI.py** (Command-line interface for batch processing multiple datasets via JSON configuration files) — https://github.com/LabLaskin/MSIGen/tree/main/other_files

## Examples

```
conda activate MSIGen
python -c "from msigen import msigen; gen = msigen(example_file='sample.d', mass_list_dir='masses.xlsx', mass_tolerance_MS1=5, mass_tolerance_MS1_units='ppm', img_height=10, img_width=10, output_file_loc='./output'); metadata, pixels = gen.get_image_data(verbose=True)"
```

## Evaluation signals

- pixels.npy has correct output shape (n+1, y, x) where n equals the number of target masses in the mass list plus one for TIC image
- pixels_metadata.json contains all specified m/z values, tolerance windows, spatial dimensions, and normalization method used
- Pixel intensity ranges are non-negative and TIC image sums to expected ion current totals across the spatial grid
- Image dimensions (y, x) match the normalized or original scanned area geometry specified in img_height and img_width parameters
- All target m/z values from the mass list appear in metadata with correct precursor/fragment and ion mobility classifications

## Limitations

- Python version constraint: ≥3.9 and ≤3.11 (not 3.12 or later); users must create a compatible conda environment.
- Bruker .baf format support requires separate installation of pyBaf2Sql from GitHub; this dependency is not included in standard pip install.
- No changelog provided in repository, so version history and breaking changes between releases are not documented.
- Tolerance-based m/z and mobility filtering can result in missed or false-positive ion matches if tolerances are set too broadly or too narrowly; empirical validation against known ion masses is recommended.
- Spatial pixel binning is performed uniformly across the entire scanned area; local variations in scan line density or sample topography are not explicitly modeled.

## Evidence

- [other] MSIGen converts raw line-scan MSI data to visualizable format by processing data through pipeline generating NumPy pixel array and JSON metadata: "MSIGen converts raw line-scan MSI data to a visualizable format by processing the data through a pipeline that generates both a NumPy pixel array and JSON metadata as intermediate outputs for"
- [methods] Install MSIGen via pip with Python 3.9–3.11 and optionally pyBaf2Sql for Bruker .baf support: "Install MSIGen via pip with Python ≥3.9 and ≤3.11, optionally installing pyBaf2Sql for Bruker .baf support."
- [methods] Define processing parameters: input file path, mass list file, and tolerance windows; set image acquisition geometry; initialize msigen object and call get_image_data(): "Define processing parameters: specify the input file path (Agilent .d, Bruker .tsf/.baf/.tdf, Thermo .raw, or .mzML), mass list file (Excel or CSV with m/z, precursor m/z, fragment m/z, and/or ion"
- [methods] Set image acquisition parameters: scanned area height/width and normalization; call get_image_data() to generate 3D array: "Set image acquisition parameters: scanned area height and width in specified units (e.g., mm), and whether to normalize all images to the same size using max, min, or mean pixels per line. Initialize"
- [methods] Verify output files pixels.npy and pixels_metadata.json with correct dimensions and metadata fields: "Verify output files pixels.npy and pixels_metadata.json are written to the specified output directory with correct dimensions and metadata fields."
- [intro] MSIGen designed for converting MSI from raw line-scan data to visualizable format: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format"
- [intro] MSIGen designed with nano-DESI MSI in mind: "is designed with nano-DESI MSI in mind"
- [readme] Create conda environment with Python 3.9–3.11 and install MSIGen via pip: "conda create --name MSIGen python=3.11 -y
conda activate MSIGen
pip install MSIGen"
- [readme] For Jupyter Notebook tool, download MSIGen_jupyter.ipynb from repository and open in Jupyter: "Download "MSIGen_jupyter.ipynb" from the other_files folder in the Github repository. Open Anaconda Navigator and run Jupyter Notebook in the MSIGen environment."
- [readme] pyBaf2Sql wraps Bruker's Baf2Sql library for reading .baf files: "This package is a Python wrapper for Bruker's Baf2Sql data access library to be used with other Python packages."
