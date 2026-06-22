---
name: open-source-mass-spectrometry-file-format-interoperability
description: Use when when working with Bruker .d/.baf mass spectrometry imaging data and needing to feed it into MSIGen or other open-source MSI processing pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - pyBaf2Sql
  - ProteoWizard MSConvert
  - MSIGen
  - Python
  - Anaconda
  - Miniconda
  - Git
  - Anaconda/Miniconda
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
---

# Open-source mass spectrometry file format interoperability

## Summary

Enable conversion and interoperability between proprietary Bruker .baf/.d mass spectrometry imaging formats and open standards (mzML) using pyBaf2Sql or ProteoWizard MSConvert. This skill bridges vendor lock-in and prepares raw instrument data for downstream processing in MSIGen and other open-source platforms.

## When to use

When working with Bruker .d/.baf mass spectrometry imaging data and needing to feed it into MSIGen or other open-source MSI processing pipelines. Specifically, when your input is raw Bruker binary data and your analysis goal requires conversion to a portable, open format (mzML) or direct programmatic access via Python.

## When NOT to use

- Input is already in an open format such as mzML, mzXML, or netCDF — conversion is unnecessary and introduces potential data loss.
- Data is from a non-Bruker vendor (e.g., Thermo, Waters, SCIEX) — pyBaf2Sql and this workflow are Bruker-specific.
- The Bruker .d folder is corrupted or missing the .baf file — conversion will fail or produce incomplete spectra.

## Inputs

- Bruker .d folder (directory containing proprietary mass spectrometry imaging data)
- Bruker .baf binary file (raw binary spectra data within .d folder)
- Ion mobility mass spectrometry data (optional, if acquired in TIMS mode)

## Outputs

- mzML file (standardized, portable XML-based mass spectrometry data format)
- NumPy array or Pandas DataFrame with m/z and intensity columns (from pyBaf2Sql)
- Metadata-enriched data structure readable by MSIGen msigen() function

## How to apply

Install either pyBaf2Sql (via `pip install git+https://github.com/gtluu/pyBaf2Sql` with Python >=3.9 and <=3.11) or ProteoWizard MSConvert GUI for format conversion. For pyBaf2Sql: load the Bruker .d folder into a BafData object, iterate through spectra frames, and extract m/z and intensity arrays as NumPy arrays or DataFrames. For MSConvert: open the GUI, select Bruker .d/.baf input file(s), set output format to 'mzML', specify an output directory, and execute conversion. Verify that the output file (converted .mzML or pyBaf2Sql-processed data) contains expected mass spectrometry metadata (m/z values, intensity arrays, and ion mobility if applicable) before passing the file path to MSIGen's msigen() function with the example_file parameter.

## Related tools

- **pyBaf2Sql** (Programmatic Python wrapper for Bruker Baf2Sql data access library; extracts m/z, intensity, and metadata from .baf files into NumPy arrays or Pandas DataFrames.) — https://github.com/gtluu/pyBaf2Sql
- **ProteoWizard MSConvert** (GUI-based vendor-neutral mass spectrometry data converter; converts Bruker .d/.baf to mzML format.) — https://proteowizard.sourceforge.io/download.html
- **MSIGen** (Downstream consumer tool; accepts converted .mzML or pyBaf2Sql-processed data via msigen() function for mass spectrometry imaging visualization.) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment; required version >=3.9 and <=3.11 for pyBaf2Sql and MSIGen compatibility.)
- **Anaconda/Miniconda** (Virtual environment manager; recommended for isolating pyBaf2Sql and MSIGen dependencies.) — https://www.anaconda.com/download

## Examples

```
pip install git+https://github.com/gtluu/pyBaf2Sql && python -c "from pyBaf2Sql.init_baf2sql import init_baf2sql_api; from pyBaf2Sql.classes import BafData; dll = init_baf2sql_api(); data = BafData(bruker_d_folder_name='sample.d', baf2sql=dll); print(f'Loaded {data.analysis[\"Spectra\"].shape[0]} spectra')"
```

## Evaluation signals

- Converted .mzML file is readable by MSIGen without errors; verify using MSIGen's msigen().get_image_data(verbose=True) and check for successful NumPy array (pixels.npy) and metadata JSON output.
- Mass spectrometry metadata is present and consistent: m/z arrays match expected mass ranges for the experiment, intensity values are non-negative, and metadata JSON contains expected fields (scan count, polarity, mass analyzer type).
- pyBaf2Sql extraction produces non-empty Pandas DataFrames for each spectrum frame with m/z and intensity columns; verify no NaN or infinite values introduced during conversion.
- Ion mobility values (if TIMS-acquired data) are preserved and fall within expected ranges; check metadata for 'mobility' or 'CCS' columns.
- File size and spectrum count of converted data match or are proportional to the original Bruker .d folder; unexpectedly small output files may indicate truncated or failed conversion.

## Limitations

- pyBaf2Sql requires Python 3.9–3.11; later Python versions (≥3.12) are not supported and will cause installation or runtime failures.
- Bruker .d data must be in .baf format; older or alternative Bruker formats (.ms, .ser) are not supported by pyBaf2Sql.
- ProteoWizard MSConvert is a GUI tool and requires manual file selection and parameter specification; it is less suitable for batch processing than pyBaf2Sql but is easier for single-file conversion.
- No changelog was available in the source materials; version compatibility and breaking changes between pyBaf2Sql and MSIGen versions are not documented.
- Ion mobility data preservation depends on the instrument acquisition mode (TIMS vs. non-TIMS); standard mzML conversion may not fully capture all Bruker-proprietary ion mobility metadata.

## Evidence

- [readme] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [other] Install pyBaf2Sql from GitHub as a prerequisite dependency before feeding data into MSIGen conversion.: "Install pyBaf2Sql from GitHub as a prerequisite dependency before feeding data into MSIGen conversion."
- [methods] Using an environment with python version >=3.9 and <=3.11: "Using an environment with python version >=3.9 and <=3.11"
- [other] If using MSConvert, open the MSConvert GUI, select Bruker .d/.baf input file(s) via 'Add Files', set output format to 'mzML', specify output directory, and click 'Start' to convert.: "If using MSConvert, open the MSConvert GUI, select Bruker .d/.baf input file(s) via 'Add Files', set output format to 'mzML', specify output directory, and click 'Start' to convert."
- [other] Verify converted .mzML file or pyBaf2Sql-processed data is readable and contains expected mass spectrometry metadata (m/z, intensity, mobility if applicable).: "Verify converted .mzML file or pyBaf2Sql-processed data is readable and contains expected mass spectrometry metadata (m/z, intensity, mobility if applicable)."
- [other] Pass the prepared file path to MSIGen's msigen() function with example_file parameter pointing to the converted .mzML or processed .baf data: "Pass the prepared file path to MSIGen's msigen() function with example_file parameter pointing to the converted .mzML or processed .baf data"
- [readme] Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode.: "Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode."
