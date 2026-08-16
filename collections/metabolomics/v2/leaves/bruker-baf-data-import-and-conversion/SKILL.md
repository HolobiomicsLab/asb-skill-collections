---
name: bruker-baf-data-import-and-conversion
description: Use when you have Bruker .d/.baf format mass spectrometry imaging data
  and need to ingest it into MSIGen for conversion to visualizable ion images. This
  skill applies when your raw data originates from Bruker TIMSTOF or similar instruments
  and you lack direct .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0943
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

# Bruker .baf data import and conversion

## Summary

Convert Bruker .d/.baf mass spectrometry imaging files to mzML or processable format via pyBaf2Sql or ProteoWizard MSConvert, preparing raw line-scan data for MSIGen processing. This skill is essential when working with Bruker TIMSTOF or similar instruments that output .baf format, which MSIGen requires in either converted or pre-processed form.

## When to use

You have Bruker .d/.baf format mass spectrometry imaging data and need to ingest it into MSIGen for conversion to visualizable ion images. This skill applies when your raw data originates from Bruker TIMSTOF or similar instruments and you lack direct .baf support in your downstream analysis pipeline.

## When NOT to use

- Input data is already in mzML, netCDF, or other open format natively supported by MSIGen — skip conversion and pass directly to msigen().
- Input is Bruker .d/.baf data but your Python environment is outside the 3.9–3.11 range — pyBaf2Sql will fail; use MSConvert GUI instead or adjust your environment.
- You lack system permissions to install external dependencies (pyBaf2Sql, ProteoWizard) — consider using a managed compute cluster or Docker environment.

## Inputs

- Bruker .d directory (containing .baf file and associated metadata)
- Bruker raw line-scan mass spectrometry imaging data in .baf format

## Outputs

- mzML file (if using ProteoWizard MSConvert)
- Processed .baf data with extracted m/z and intensity arrays (if using pyBaf2Sql)
- NumPy array (pixels.npy) containing pixel intensity data
- Metadata JSON file with m/z values and imaging parameters

## How to apply

Choose one of two conversion pathways: (1) pyBaf2Sql route: install pyBaf2Sql from GitHub into a Python environment ≥3.9 and ≤3.11 managed by Anaconda/Miniconda, then programmatically read the .baf file using BafData class to extract m/z and intensity arrays; or (2) ProteoWizard MSConvert route: install MSConvert from ProteoWizard, open the GUI, add Bruker .d/.baf file(s), set output format to mzML, and execute conversion. After conversion, verify the output file (.mzML or processed .baf data) contains expected mass spectrometry metadata (m/z, intensity, mobility if applicable). Pass the converted file path to MSIGen's msigen() function with appropriate parameters (example_file, mass_list_dir, tolerances, image dimensions). Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON.

## Related tools

- **pyBaf2Sql** (Programmatic Python wrapper for Bruker Baf2Sql library to parse .baf files and extract m/z and intensity arrays) — https://github.com/gtluu/pyBaf2Sql
- **ProteoWizard MSConvert** (GUI-based file format converter to transform Bruker .d/.baf data to mzML format) — https://proteowizard.sourceforge.io/download.html
- **MSIGen** (Downstream Python package that accepts converted .mzML or processed .baf data to generate ion images and metadata) — https://github.com/LabLaskin/MSIGen
- **Anaconda / Miniconda** (Python environment manager for isolating pyBaf2Sql dependencies and ensuring correct Python version (3.9–3.11)) — https://www.anaconda.com/download
- **Git** (Version control tool required to clone and install pyBaf2Sql from GitHub) — https://git-scm.com/downloads

## Examples

```
pip install git+https://github.com/gtluu/pyBaf2Sql && python -c "from pyBaf2Sql.init_baf2sql import init_baf2sql_api; from pyBaf2Sql.classes import BafData; dll = init_baf2sql_api(); data = BafData(bruker_d_folder_name='sample.d', baf2sql=dll)"
```

## Evaluation signals

- Converted .mzML file is readable and contains valid mass spectrometry metadata (m/z arrays, intensity arrays, scan headers).
- MSIGen msigen() function executes without errors when passed the converted file path and returns non-empty metadata dict and pixels NumPy array.
- get_image_data(verbose=True) generates pixels.npy and metadata JSON files without runtime errors.
- Pixel intensity values fall within expected range (non-negative, no unexpected NaN or infinity values) and match the number of mass list entries.
- Ion images produced by get_and_display_images() show recognizable spatial patterns consistent with known sample anatomy or experimental design.

## Limitations

- pyBaf2Sql requires Python ≥3.9 and ≤3.11; environments outside this range will fail at import or runtime.
- pyBaf2Sql installation requires Git and GitHub access; airgapped or restricted network environments may require pre-staged wheels or alternative deployment.
- MSConvert GUI is platform-specific and may have reduced functionality or UI quirks on non-Windows systems; command-line alternatives may be more reliable.
- Large .baf files (>10 GB) may consume significant RAM during pyBaf2Sql parsing or MSConvert operation; consider batch processing or memory-optimized workstations.
- No changelog is available for pyBaf2Sql or integration changes; version pinning or compatibility testing is recommended when updating dependencies.

## Evidence

- [other] For Bruker .d data in .baf format, users must install pyBaf2Sql from GitHub as a prerequisite dependency before feeding data into MSIGen conversion.: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [methods] pyBaf2Sql requires Python 3.9–3.11 in Anaconda/Miniconda environment.: "Using an environment with python version >=3.9 and <=3.11"
- [readme] ProteoWizard MSConvert is the alternative pathway for .baf conversion to mzML.: "pip install git+https://github.com/gtluu/pyBaf2Sql"
- [readme] pyBaf2Sql extracts m/z and intensity arrays from .baf files via BafData class.: "Get all spectra from a BAF file as a list of pd.DataFrames with columns for m/z and intensity in centroid mode."
- [other] Converted data must be passed to msigen() with appropriate parameters and verified via get_image_data().: "Pass the prepared file path to MSIGen's msigen() function with example_file parameter pointing to the converted .mzML or processed .baf data, along with mass_list_dir, tolerances, and image"
- [other] Successful conversion produces pixels.npy NumPy array and metadata JSON without errors.: "Execute get_image_data(verbose=True) to confirm successful conversion to NumPy array (pixels.npy) and metadata JSON without errors."
