---
name: html-bundle-rendering-in-browser
description: Use when you have a dashboard_data.json file (JSON export from the msFeaST
  pipeline) and need to interactively explore quantification tables, metadata, and
  spectral data on a desktop machine (macOS, Linux, or Windows).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - msFeaST
  - jupyter-notebook
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btae584
  title: msFeaST
evidence_spans:
- github.com__kevinmildau__msFeaST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  dedup_kept_from: coll_msfeast_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae584
  all_source_dois:
  - 10.1093/bioinformatics/btae584
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# html-bundle-rendering-in-browser

## Summary

Load a self-contained HTML dashboard bundle into a desktop web browser and render pre-processed mass spectrometry data (quantification tables, metadata, and spectral data) in an interactive visualization interface. This skill enables cross-platform inspection of msFeaST analysis outputs without requiring local Python or R installation.

## When to use

You have a dashboard_data.json file (JSON export from the msFeaST pipeline) and need to interactively explore quantification tables, metadata, and spectral data on a desktop machine (macOS, Linux, or Windows). Use this skill when the msFeaST pre-processing and pipeline steps have already been completed and you want to visualize the results without re-running the analysis.

## When NOT to use

- You need to re-run or modify the msFeaST analysis pipeline—use the Jupyter notebooks (preprocessing_mushroom_type_comparison.ipynb and msfeast_pipeline_mushroom_type_comparison.ipynb) instead.
- You only have raw mass spectrometry data (mzML, NetCDF, or other vendor formats)—you must first run the msFeaST pre-processing and pipeline steps to generate the dashboard_data.json file.
- You are running on a headless or server-only environment without a graphical desktop browser—the bundle requires a modern web browser with HTML5 support.

## Inputs

- msFeaST_Dashboard_bundle.html (self-contained HTML/JavaScript/CSS bundle)
- dashboard_data.json (JSON export from msFeaST pipeline containing quantification table, metadata, and spectral data)

## Outputs

- Interactive visualization dashboard with dataview tab showing loaded quantification table, metadata table, and spectral data

## How to apply

Download the msFeaST_Dashboard_bundle.html file and the corresponding dashboard_data.json file to the same local directory or accessible location. Open the HTML bundle in a modern desktop web browser (Firefox, Chrome, Edge, or Safari)—the bundle is self-contained and requires no server or internet connection. Use the HTML interface's data-load feature to select and import the dashboard_data.json file. Navigate to the dataview tab to verify that the quantification table, metadata table, and spectral data are rendered and accessible. The dashboard renders identically across operating systems in desktop browsers, making this a platform-independent approach to data inspection.

## Related tools

- **msFeaST** (Generates the dashboard_data.json output file via its Jupyter notebook pipeline; the HTML bundle is the visualization frontend for msFeaST outputs) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Runs the msFeaST preprocessing and pipeline workflows to generate the JSON input file that is loaded into the HTML bundle) — https://github.com/kevinmildau/msFeaST

## Evaluation signals

- The HTML bundle opens without error in the specified desktop browsers (Firefox, Chrome, Edge, Safari).
- The data-load interface successfully accepts and parses the dashboard_data.json file without schema validation errors.
- Switching to the dataview tab displays the quantification table with correct row and column structure matching the input JSON.
- Metadata fields are populated and accessible in the dataview tab.
- Spectral data (if present in the JSON) renders in the visualization tab without missing or corrupted values.
- No browser console errors or warnings related to JSON parsing or data rendering.

## Limitations

- The HTML bundle only displays pre-processed data; it does not support re-running analysis or modifying pipeline parameters. Any changes to analysis require re-generating the dashboard_data.json file using the msFeaST Jupyter notebooks.
- The msFeaST pre-processing and pipeline workflow itself has only been tested on macOS and Linux; Windows support is currently being worked on. However, the HTML bundle (this skill) works identically across all operating systems in desktop browsers.
- The bundle requires a modern desktop web browser with JavaScript enabled; it does not work in mobile browsers or headless environments.
- If the dashboard_data.json file is very large, browser rendering performance may degrade depending on available system memory and browser capabilities.

## Evidence

- [readme] To inspect the interactive dashboard for the illustrative examples, please download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json. Open the html bundle in your browser and load the select and load the data.: "download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json. Open the html bundle in your browser and load the select and"
- [readme] Changing to the dataview tab shows the now loaded data.: "Changing to the dataview tab shows the now loaded data."
- [intro] The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari): "The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari)"
- [readme] If you only want to inspect pre-processed example files using the visual dashboard, the *msFeaST_Dashboard_bundle.html* is the only file needed alongside the .json file. No dependencies need to be installed to do so.: "If you only want to inspect pre-processed example files using the visual dashboard, the *msFeaST_Dashboard_bundle.html* is the only file needed alongside the .json file."
- [intro] complete example of quantification table, metadata table, and spectral data processing: "complete example of quantification table, metadata table, and spectral data processing"
