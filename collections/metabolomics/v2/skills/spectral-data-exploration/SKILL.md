---
name: spectral-data-exploration
description: Use when you have completed msFeaST pipeline preprocessing and generated a JSON output file (dashboard_data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# spectral-data-exploration

## Summary

Interactive browser-based exploration of mass spectrometry spectral data, quantification tables, and metadata loaded from JSON files into the msFeaST dashboard. Use this skill to visually inspect, navigate, and validate pre-processed MS data across multiple linked views without requiring local software installation.

## When to use

You have completed msFeaST pipeline preprocessing and generated a JSON output file (dashboard_data.json) containing quantification tables, metadata, and spectral data, and you need to interactively inspect the results across linked dataview, quantification, metadata, and spectral visualization tabs to validate processing quality or explore feature patterns.

## When NOT to use

- Input JSON file has not been validated against the msFeaST pipeline schema or was generated outside msFeaST—dataview may not render correctly.
- You need to modify, reprocess, or export spectral data—exploration is read-only; use the jupyter-notebook pipeline for data manipulation.
- You require statistical analysis, feature selection, or downstream metabolite annotation—exploration alone does not perform these operations; proceed to msFeaST analytical modules.

## Inputs

- msFeaST_Dashboard_bundle.html (self-contained HTML/JavaScript/CSS bundle)
- dashboard_data.json (JSON file containing quantification table, metadata, and spectral data from msFeaST pipeline)

## Outputs

- Interactive multi-tab visualization displaying quantification table in dataview
- Rendered metadata table accessible in dataview
- Spectral data (MS2 or MS1) visualized across linked tabs
- Browser session state (no persistent file output from exploration itself)

## How to apply

Download the msFeaST_Dashboard_bundle.html and your dashboard_data.json file. Open the HTML bundle in a desktop web browser (Firefox, Chrome, Edge, or Safari) on any operating system. Use the bundle's data-load interface to select and load the JSON file. Navigate to the dataview tab to inspect the loaded quantification table, metadata table, and spectral data rendered in tabular and graphical form. The dataview tab is the entry point for exploring loaded data; switch between tabs to examine different aspects (quantification, metadata, spectra) of the same dataset. The process requires no Python, R, or system dependencies—only a modern browser.

## Related tools

- **msFeaST** (Provides the jupyter-notebook pipeline that generates the dashboard_data.json file and the bundled HTML visualization dashboard) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Runs the msFeaST preprocessing and pipeline notebooks that produce the JSON file consumed by the dashboard)

## Evaluation signals

- The dataview tab displays a populated quantification table with feature identifiers, intensities/areas, and sample columns without rendering errors.
- Metadata table in dataview shows all loaded sample metadata (e.g., sample names, conditions, batch info) with correct row and column alignment.
- Spectral data visualization (MS2 or MS1 spectra) renders for selected features or samples with m/z and intensity axes properly scaled.
- No JavaScript console errors appear in the browser developer tools when loading and navigating between tabs.
- Dashboard responds to user interactions (tab switching, data selection) within the same session without requiring page reload or file re-upload.

## Limitations

- The msFeaST pre-processing and pipeline workflow has been tested on macOS and Linux; Windows support is currently being worked on (though the dashboard HTML itself runs on Windows browsers).
- Exploration is read-only—no editing, filtering, or export of spectral data is possible from the dashboard itself; modifications require returning to the jupyter-notebook pipeline.
- Browser performance may degrade with very large JSON files (e.g., thousands of features or samples); no explicit size limits are documented.
- The dashboard is designed for desktop browsers; mobile or tablet rendering is not explicitly supported.

## Evidence

- [readme] The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari): "The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari)"
- [readme] Download the msFeaST_Dashboard_bundle.html and load the dashboard_data.json file into the browser and switch to the dataview tab: "download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json. Open the html bundle in your browser and load the select and"
- [readme] Loaded data includes quantification table, metadata, and spectral data: "complete example of quantification table, metadata table, and spectral data processing"
- [readme] No dependencies need to be installed to inspect pre-processed example files using the visual dashboard: "If you only want to inspect pre-processed example files using the visual dashboard, the *msFeaST_Dashboard_bundle.html* is the only file needed alongside the .json file. No dependencies need to be"
- [readme] The jupyter-notebook pipeline produces a JSON text file that can be interactively explored in the interactive dashboard: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
