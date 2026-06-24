---
name: interactive-visualization-inspection
description: Use when after msFeaST pipeline execution has produced a dashboard_data.json
  file containing quantification, metadata, and spectral matrices, or when you need
  to validate that preprocessing steps correctly loaded and rendered ms/ms feature
  data before downstream statistical or network analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - msFeaST
  - Desktop web browser
  techniques:
  - LC-MS
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

# interactive-visualization-inspection

## Summary

Load preprocessed mass spectrometry data (quantification tables, metadata, and spectral data) into a browser-based interactive dashboard for exploratory analysis and validation. This skill enables rapid inspection of JSON-serialized pipeline outputs without requiring installation of Python, R, or command-line tools.

## When to use

After msFeaST pipeline execution has produced a dashboard_data.json file containing quantification, metadata, and spectral matrices, or when you need to validate that preprocessing steps correctly loaded and rendered ms/ms feature data before downstream statistical or network analysis.

## When NOT to use

- Input is raw mass spectrometry files (.mzML, .mzXML, or .raw); use preprocessing_mushroom_type_comparison.ipynb instead.
- You need to modify the preprocessing parameters or re-run the feature extraction pipeline; open the msfeast_pipeline_mushroom_type_comparison.ipynb notebooks in Jupyter instead.
- You are working on Windows and have not yet installed conda/R dependencies; the dashboard visualization itself works on Windows, but pipeline execution is not yet supported.

## Inputs

- msFeaST_Dashboard_bundle.html (bundled HTML/JavaScript/CSS file)
- dashboard_data.json (JSON file output by msFeaST jupyter-notebook pipeline containing quantification table, metadata, and spectral data)

## Outputs

- Rendered interactive dataview tab displaying quantification table
- Rendered metadata table and columns
- Rendered spectral data matrices
- Visual confirmation of data integrity and completeness

## How to apply

Download the msFeaST_Dashboard_bundle.html file and the JSON output from your pipeline run. Open the HTML bundle in a desktop web browser (Firefox, Chrome, Edge, or Safari) on any operating system. Use the bundle's data-load interface to select and load your dashboard_data.json file. Navigate to the dataview tab within the dashboard interface. Inspect the loaded quantification table, metadata columns, and spectral data matrices to verify that row/column counts, metadata fields, and intensity values match your expectations from the preprocessing notebook. Check that no cells are empty or malformed before proceeding to statistical analysis.

## Related tools

- **msFeaST** (Produces the dashboard_data.json file via jupyter-notebook pipeline and hosts the interactive visualization bundle) — https://github.com/kevinmildau/msFeaST
- **Desktop web browser** (Renders the msFeaST_Dashboard_bundle.html and provides the interactive dataview interface)

## Evaluation signals

- Dashboard loads without JavaScript errors or blank sections in the browser console.
- Dataview tab renders all three components: quantification table, metadata table, and spectral data matrices with correct row and column counts.
- Metadata columns display expected field names and sample identifiers without truncation or encoding errors.
- Quantification values are numeric and within expected intensity ranges (no NaN, Inf, or text artifacts).
- Spectral data matrices contain non-zero m/z and intensity pairs corresponding to the input features from the JSON.

## Limitations

- Dashboard visualization requires a modern desktop web browser with JavaScript enabled; mobile browsers and text-only terminals are not supported.
- This skill only inspects data; it does not modify, filter, or re-process the JSON. Any preprocessing errors will be visible but must be corrected by re-running the pipeline notebooks.
- Large JSON files (>50 MB) may render slowly or cause browser memory issues on systems with <4 GB RAM.
- No changelog or version tracking is provided in the repository, so compatibility between msFeaST_Dashboard_bundle.html and dashboard_data.json versions must be verified manually.

## Evidence

- [readme] To inspect the interactive dashboard for the illustrative examples, please download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json.: "To inspect the interactive dashboard for the illustrative examples, please download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboar"
- [readme] Open the html bundle in your browser and load the select and load the data. Changing to the dataview tab shows the now loaded data.: "Open the html bundle in your browser and load the select and load the data. Changing to the dataview tab shows the now loaded data."
- [readme] The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari): "The interactive visualization dashboard works regardless of os on desktop browsers (e.g., firefox, chrome, edge, safari)"
- [readme] If you only want to inspect pre-processed example files using the visual dashboard, the *msFeaST_Dashboard_bundle.html* is the only file needed alongside the .json file. No dependencies need to be installed to do so.: "If you only want to inspect pre-processed example files using the visual dashboard, the *msFeaST_Dashboard_bundle.html* is the only file needed alongside the .json file. No dependencies need to be"
- [intro] According to the msFeaST Quickstart instructions, after opening the msFeaST_Dashboard_bundle.html in a browser and loading the dashboard_data.json file, switching to the dataview tab displays the loaded data.: "switching to the dataview tab displays the loaded quantification table, metadata, and spectral data"
