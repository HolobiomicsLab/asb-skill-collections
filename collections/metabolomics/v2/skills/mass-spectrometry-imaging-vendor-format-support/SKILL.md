---
name: mass-spectrometry-imaging-vendor-format-support
description: Use when your input mass spectrometry imaging data is in a proprietary
  vendor format (Bruker .d/.baf, or other binary formats not natively supported by
  MSIGen) and you need to convert it to an open, readable format (mzML or processed
  binary) compatible with MSIGen's msigen() function.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
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
  - Anaconda / Miniconda
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: open
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

# Mass Spectrometry Imaging Vendor Format Support

## Summary

Enable processing of proprietary vendor mass spectrometry imaging formats (particularly Bruker .d/.baf) by installing and configuring format-specific conversion tools before ingestion into MSIGen. This skill bridges the gap between raw instrument data and MSIGen's line-scan processing pipeline.

## When to use

Your input mass spectrometry imaging data is in a proprietary vendor format (Bruker .d/.baf, or other binary formats not natively supported by MSIGen) and you need to convert it to an open, readable format (mzML or processed binary) compatible with MSIGen's msigen() function. Use this skill when the raw data has not yet been converted and you receive an error indicating unrecognized file format or missing metadata.

## When NOT to use

- Input data is already in mzML, NetCDF, or other open format supported directly by MSIGen — use the standard MSIGen workflow instead.
- Your instrument vendor provides native MSIGen support or a direct conversion plugin — check MSIGen documentation for pre-built handlers.
- The .d folder is corrupted or missing the .baf file — repair or reacquire the raw data first.

## Inputs

- Bruker .d directory containing .baf binary file(s)
- Raw mass spectrometry imaging line-scan data in vendor binary format

## Outputs

- mzML file (if using ProteoWizard MSConvert)
- Processed .baf data with extracted m/z and intensity arrays (if using pyBaf2Sql)
- Metadata-enriched intermediate data ready for MSIGen ingestion

## How to apply

First, assess whether your raw data is Bruker .d/.baf format. If yes, choose a conversion pathway: (1) pyBaf2Sql (GitHub installation into Python ≥3.9, ≤3.11 conda environment), which directly reads BAF files and extracts m/z and intensity arrays, or (2) ProteoWizard MSConvert (GUI-based), which converts .baf to mzML via a graphical workflow. For pyBaf2Sql: install via `pip install git+https://github.com/gtluu/pyBaf2Sql`, initialize the Baf2Sql API, instantiate a BafData object pointing to your .d folder, and iterate over spectra frames to extract m/z and intensity arrays as NumPy or pandas objects. For MSConvert: open the GUI, add .d/.baf files, set output format to mzML, specify output directory, and click Start. After conversion, validate that the output file contains expected mass spectrometry metadata (m/z values, intensity, ion mobility if applicable) before passing the file path to MSIGen's msigen() function with the example_file parameter. The conversion is successful when get_image_data(verbose=True) executes without file-format errors and produces pixels.npy and metadata JSON.

## Related tools

- **pyBaf2Sql** (Direct Python wrapper for Bruker Baf2Sql data access library; reads .baf binary files and extracts m/z, intensity, and metadata arrays into pandas DataFrames or NumPy arrays) — https://github.com/gtluu/pyBaf2Sql
- **ProteoWizard MSConvert** (GUI and command-line tool for converting Bruker .d/.baf to mzML format; provides graphical workflow for batch conversion) — https://proteowizard.sourceforge.io/download.html
- **Anaconda / Miniconda** (Python distribution and environment manager; required to create isolated ≥3.9, ≤3.11 Python environment for pyBaf2Sql and MSIGen compatibility) — https://www.anaconda.com/download
- **Git** (Version control and repository access tool; required to install pyBaf2Sql from GitHub via pip) — https://git-scm.com/downloads
- **MSIGen** (Downstream tool that consumes converted format; receives file path via example_file parameter to msigen() function) — https://github.com/LabLaskin/MSIGen

## Examples

```
pip install git+https://github.com/gtluu/pyBaf2Sql && python -c "from pyBaf2Sql.init_baf2sql import init_baf2sql_api; from pyBaf2Sql.classes import BafData; dll = init_baf2sql_api(); data = BafData(bruker_d_folder_name='sample.d', baf2sql=dll); print(f'Loaded {data.analysis[\"Spectra\"].shape[0]} spectra')"
```

## Evaluation signals

- Converted file exists and is readable; no file-format or codec errors when opening in the chosen tool (pyBaf2Sql or MSConvert).
- Extracted m/z and intensity arrays are non-empty NumPy/pandas objects with expected shapes and data types (float64 for m/z and intensity).
- Metadata JSON or spectral header contains mass spectrometry-specific fields (acquisition time, instrument model, ion count, m/z range) consistent with the original raw data.
- MSIGen's get_image_data(verbose=True) completes without file-format exceptions and produces pixels.npy (NumPy array) and metadata JSON file in the specified output directory.
- Ion images generated from the converted data show recognizable spatial patterns consistent with the sample being imaged (e.g., expected m/z features in expected spatial regions).

## Limitations

- pyBaf2Sql requires Python version ≥3.9 and ≤3.11; newer Python versions may lack compatible Baf2Sql .dll/.so library files.
- pyBaf2Sql is a community wrapper around Bruker's proprietary Baf2Sql library; functionality and bug fixes depend on Bruker's API stability and the maintainer's updates.
- ProteoWizard MSConvert may require separate installation of vendor-specific libraries (e.g., Bruker's DLL files on Windows) and is not fully portable across operating systems.
- Conversion can be time-intensive for large .d folders (>10 GB); memory requirements scale with spectral density and ion mobility dimension.
- Some metadata fields (e.g., collision energy, MS/MS fragmentation data) may not be fully preserved or correctly mapped during conversion, depending on the format translator.

## Evidence

- [methods] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [methods] Using an environment with python version >=3.9 and <=3.11: "Using an environment with python version >=3.9 and <=3.11"
- [readme] pip install git+https://github.com/gtluu/pyBaf2Sql: "This package can be installed to a Python virtual environment using `pip`. ```
pip install git+https://github.com/gtluu/pyBaf2Sql
```"
- [readme] Initialize the Baf2Sql library using the packaged .dll or .so files for Windows or Linux, respectively.: "Initialize the Baf2Sql library using the packaged .dll or .so files for Windows or Linux, respectively."
- [readme] Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode.: "Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode."
- [other] Pass the prepared file path to MSIGen's msigen() function with example_file parameter pointing to the converted .mzML or processed .baf data: "Pass the prepared file path to MSIGen's msigen() function with example_file parameter pointing to the converted .mzML or processed .baf data, along with mass_list_dir, tolerances, and image"
- [other] Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON without errors.: "Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON without errors."
