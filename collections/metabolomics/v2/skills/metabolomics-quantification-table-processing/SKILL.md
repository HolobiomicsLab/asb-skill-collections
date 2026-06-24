---
name: metabolomics-quantification-table-processing
description: Use when you have a quantification table (rows = metabolite features,
  columns = samples with abundance values), corresponding metadata table (sample annotations,
  groupings), and spectral data files, and you need to produce a unified JSON dashboard
  artifact that can be loaded into an interactive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - msFeaST
  - msfeast_pipeline.ipynb
  - jupyter-notebook
  - msFeaST Python module
  - R (v4.3.3) with globaltest, dplyr, tibble, readr dependencies
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

# metabolomics-quantification-table-processing

## Summary

Transform raw mass spectrometry abundance tables into standardized JSON format suitable for interactive exploration and statistical analysis in metabolomics dashboards. This skill integrates quantification data with metadata and spectral annotations to produce a unified exploratory artifact.

## When to use

You have a quantification table (rows = metabolite features, columns = samples with abundance values), corresponding metadata table (sample annotations, groupings), and spectral data files, and you need to produce a unified JSON dashboard artifact that can be loaded into an interactive browser-based visualization for metabolomics exploration and feature discovery.

## When NOT to use

- Your quantification data is already in JSON format and has been validated against the dashboard schema.
- You only want to visualize pre-processed example data without running the pipeline on your own samples — use the bundled msFeaST_Dashboard_bundle.html with ready-made dashboard_data.json instead.
- Spectral data or metadata tables are unavailable or in non-standard formats that cannot be parsed by the preprocessing notebooks.

## Inputs

- quantification table (CSV or tabular format with metabolite features × samples)
- metadata table (sample annotations, experimental conditions, groupings)
- spectral data files (mass spectrometry fragmentation spectra)
- msfeast_pipeline.ipynb notebook

## Outputs

- dashboard_data.json (JSON text file conforming to msFeaST dashboard schema)
- processed and integrated metabolomics artifact ready for interactive exploration

## How to apply

Within a Jupyter notebook environment, load the quantification table, metadata table, and spectral data files into memory. Execute the msfeast_pipeline notebook which orchestrates preprocessing, integration, and normalization of these three data sources. The pipeline processes the tabular data and spectral annotations to conform to a dashboard data schema (a JSON structure with required fields for interactive visualization). After execution, validate that the output JSON contains all required fields and can be successfully loaded into the msFeaST Dashboard bundle in a desktop browser. The workflow has been tested on macOS and Linux; Windows support is in development.

## Related tools

- **msfeast_pipeline.ipynb** (Main orchestration notebook that integrates quantification, metadata, and spectral data into a unified dashboard-ready JSON artifact) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Execution environment for running the msfeast_pipeline notebook and interactive parameter configuration)
- **msFeaST Python module** (Core data integration and transformation functions for preprocessing and pipeline execution) — https://github.com/kevinmildau/msFeaST
- **R (v4.3.3) with globaltest, dplyr, tibble, readr dependencies** (Statistical analysis and feature validation performed within the pipeline)

## Examples

```
conda activate msfeast_environment; jupyter-notebook msfeast_pipeline.ipynb
```

## Evaluation signals

- The output JSON file parses without errors and can be loaded into msFeaST_Dashboard_bundle.html in a desktop browser (Firefox, Chrome, Edge, Safari).
- The JSON contains all required fields specified by the dashboard data schema; validate schema conformance by attempting to load and display data in the dataview tab.
- Sample counts and metabolite feature counts in the JSON match the dimensions of the input quantification table (no rows or columns lost during processing).
- Metadata fields (sample annotations, experimental groupings) are correctly preserved and accessible in the dashboard interface.
- The JSON file is valid, well-formed text that can be deserialized by a JSON parser without truncation or corruption.

## Limitations

- msFeaST preprocessing and pipeline workflow tested only on macOS and Linux; Windows support currently in development and untested.
- R package installation and path configuration can fail if rscript commands are run before conda environment activation, requiring terminal restart and re-activation.
- Some terminal interfaces (e.g., VSCode terminal) may buffer conda environment paths, requiring a fresh terminal window and immediate conda activation to avoid installation failures.
- Interactive visualization dashboard requires a desktop web browser; mobile browsers are not explicitly supported.
- No changelog or version history is documented, limiting traceability of changes to the pipeline schema or processing logic.

## Evidence

- [readme] quantification table, metadata table, and spectral data processing: "complete example of quantification table, metadata table, and spectral data processing"
- [readme] JSON output format for dashboard loading: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
- [readme] Platform compatibility and testing: "The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems"
- [intro] Schema validation requirement: "Validate that the generated JSON contains required fields for interactive visualization and can be loaded in the msFeaST Dashboard bundle"
- [readme] R path configuration known issue: "In rare cases where the rscript command is run from the terminal prior to the conda installation of R as instructed above, the temporary cached path to R used within conda may be faulty"
