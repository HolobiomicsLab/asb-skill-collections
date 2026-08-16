---
name: lcms-data-format-parsing
description: Use when when you have raw LC/MS data in mzML format and need to execute the LAGF non-targeted screening pipeline. Use this skill as the first step before applying the LAGF algorithm workflow to extract and annotate features from mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pymzml
  - pandas
  - numpy
  - scipy
  - joblib
  - tqdm
  - tqdm_joblib
  - matplotlib
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00060
  title: LAGF
evidence_spans:
- pymzml==2.5.2
- pandas==2.0.3
- numpy==1.22.4
- scipy==1.4.1
- joblib==0.15.1
- tqdm==4.45.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lagf_cq
    doi: 10.1021/acs.analchem.5c00060
    title: LAGF
  dedup_kept_from: coll_lagf_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00060
  all_source_dois:
  - 10.1021/acs.analchem.5c00060
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-data-format-parsing

## Summary

Parse and load LC/MS raw data files in mzML format using pymzml as a prerequisite step for non-targeted feature screening and annotation. This skill enables ingestion of mass spectrometry instrument output into a Python environment for downstream algorithmic processing.

## When to use

When you have raw LC/MS data in mzML format and need to execute the LAGF non-targeted screening pipeline. Use this skill as the first step before applying the LAGF algorithm workflow to extract and annotate features from mass spectrometry data.

## When NOT to use

- Input is already in a parsed feature table or matrix format (e.g., pandas DataFrame, feature × sample matrix)
- Data is in a non-standard LC/MS format not supported by pymzml (e.g., proprietary vendor formats without conversion to mzML)
- The analysis goal does not require full raw spectral data (e.g., only aggregated or pre-processed feature annotations are available)

## Inputs

- mzML format LC/MS data file (XML-based mass spectrometry file format)

## Outputs

- Parsed LC/MS data object (pymzml-compatible Python object with scan metadata and spectral arrays)
- Accessible retention time and m/z intensity arrays for downstream feature detection

## How to apply

Load the LC/MS data file in mzML format using pymzml, which parses the standardized XML-based mass spectrometry data structure and makes it accessible as Python objects. The pymzml library handles the conversion of binary/XML encoded m/z and intensity arrays from the instrument output. Once loaded, the data object can be passed directly to the LAGF algorithm workflow as defined in the example.ipynb notebook, which applies the non-targeted screening pipeline to extract and annotate features. Verify successful parsing by confirming that the data object contains expected scan metadata (retention time, m/z range, precursor ions) and that no parsing errors are raised during initialization.

## Related tools

- **pymzml** (Parses mzML-format LC/MS raw data files and provides Python object interface to spectral metadata and m/z-intensity arrays) — github.com/zsspython/LAGF
- **pandas** (Structures and manipulates parsed spectral and feature metadata after pymzml ingestion) — github.com/zsspython/LAGF
- **numpy** (Handles numerical arrays (m/z, intensity values) extracted from parsed LC/MS data) — github.com/zsspython/LAGF

## Evaluation signals

- No parsing exceptions raised; pymzml successfully instantiates a data object from the mzML file without I/O or XML validation errors
- Parsed data object contains populated scan metadata (retention times, precursor m/z, scan indices) consistent with the instrument's acquisition parameters
- m/z and intensity arrays are correctly extracted and have matching dimensions (equal array length per scan)
- Data object integrates seamlessly with the downstream LAGF algorithm workflow when passed as input to example.ipynb
- Spot-check: m/z ranges and mass resolution match documented instrument specifications and mzML file header metadata

## Limitations

- pymzml 2.5.2 and dependent versions (numpy 1.22.4, scipy 1.4.1) may have compatibility constraints with newer Python patch versions or other installed packages
- Parsing is limited to mzML format; proprietary instrument formats (.RAW, .d, .ms) must be pre-converted to mzML (e.g. via MSConvert) before use
- Large mzML files may require significant memory; joblib and tqdm are used in the downstream workflow to parallelize and monitor processing, but parsing itself is single-threaded
- No changelog documented in the repository; version compatibility with future LAGF algorithm updates is unclear

## Evidence

- [other] Load the LC/MS data file in mzML format using pymzml: "Load the LC/MS data file in mzML format using pymzml."
- [readme] LAGF algorithm workflow is documented in example.inpynb file: "The LAGF algorithm workflow is shown in the file "example.inpynb""
- [readme] LAGF is an LC/MS data non-targeted screening tool: "LC/MS data non-targeted screening tools"
