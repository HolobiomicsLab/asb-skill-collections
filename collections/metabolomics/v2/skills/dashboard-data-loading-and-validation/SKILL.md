---
name: dashboard-data-loading-and-validation
description: Use when after generating a dashboard_data.json file from the msFeaST Jupyter pipeline, use this skill to verify that the JSON file is correctly formatted and completely loaded into the interactive dashboard before conducting visual exploration or sharing the dashboard with collaborators.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - msFeaST
  - jupyter-notebook
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dashboard-data-loading-and-validation

## Summary

Load and validate mass spectrometry quantification, metadata, and spectral data from a JSON file into the msFeaST interactive visualization dashboard for exploratory analysis. This skill confirms that the dashboard successfully renders and provides access to all three data components in the dataview tab.

## When to use

After generating a dashboard_data.json file from the msFeaST Jupyter pipeline, use this skill to verify that the JSON file is correctly formatted and completely loaded into the interactive dashboard before conducting visual exploration or sharing the dashboard with collaborators.

## When NOT to use

- You do not have a valid dashboard_data.json file (e.g., file is from a non-msFeaST source or was corrupted during export).
- You are working on a server-side or headless environment without access to a desktop web browser (the dashboard requires a graphical browser interface).
- You only need to validate the JSON schema without interactive visualization; use a JSON schema validator instead.

## Inputs

- msFeaST_Dashboard_bundle.html (standalone HTML file)
- dashboard_data.json (JSON-formatted text file output from msFeaST Jupyter pipeline containing quantification table, metadata, and spectral data)

## Outputs

- Rendered interactive visualization dashboard with populated dataview tab
- Accessibility confirmation for quantification table, metadata table, and spectral data within the browser

## How to apply

Download the msFeaST_Dashboard_bundle.html standalone file and the dashboard_data.json output from your msFeaST preprocessing and pipeline notebooks. Open the HTML bundle in a desktop web browser (Firefox, Chrome, Edge, or Safari). Use the HTML bundle's data-load interface to select and load the dashboard_data.json file. Navigate to the dataview tab and verify that the quantification table, metadata table, and spectral data are all rendered and accessible. If any of the three data components is missing or displays incorrectly, the JSON file may be malformed or incomplete; regenerate it from the pipeline notebooks.

## Related tools

- **msFeaST** (Generates the dashboard_data.json file and provides the bundled HTML dashboard interface for visualization) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Environment in which msFeaST preprocessing and pipeline notebooks are executed to produce the JSON file prior to loading)

## Evaluation signals

- All three data components (quantification table, metadata table, spectral data) render without errors in the dataview tab after loading.
- The quantification table displays row and column headers matching the expected sample and feature counts from the input data.
- The metadata table is populated with all sample-level attributes used in the pipeline preprocessing notebooks.
- Spectral data is accessible and shows expected mass-to-charge (m/z) and intensity values without truncation or formatting artifacts.
- No console errors or failed data-fetch messages appear in the browser developer tools when switching between tabs.

## Limitations

- The interactive dashboard is currently tested and verified to work on macOS and Linux only; Windows support for the full msFeaST pipeline is under development, though the dashboard itself should work on Windows desktop browsers.
- The HTML bundle does not validate R/Python dependencies; it only provides visualization. If the upstream JSON file was generated with incompatible software versions or incomplete data processing, the dashboard will load but may display incomplete or incorrect results.
- Large JSON files (>~500 MB) may cause browser performance degradation or memory issues depending on available client-side RAM; no explicit file size limits are documented.

## Evidence

- [other] After opening the msFeaST_Dashboard_bundle.html in a browser and loading the dashboard_data.json file, switching to the dataview tab displays the loaded data.: "according to the msFeaST Quickstart instructions, after opening the msFeaST_Dashboard_bundle.html in a browser and loading the dashboard_data.json file, switching to the dataview tab displays the"
- [readme] To inspect the interactive dashboard, download msFeaST_Dashboard_bundle.html and dashboard_data.json; open the HTML bundle and load the data; the dataview tab shows the loaded quantification, metadata, and spectral data.: "download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json. Open the html bundle in your browser and load the select and"
- [readme] The interactive visualization dashboard works on desktop browsers regardless of operating system.: "The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari)"
- [readme] The Jupyter pipeline produces a JSON text file for interactive exploration in the interactive dashboard.: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
- [readme] Complete example of quantification table, metadata table, and spectral data processing is provided in the pipeline notebooks.: "complete example of quantification table, metadata table, and spectral data processing"
