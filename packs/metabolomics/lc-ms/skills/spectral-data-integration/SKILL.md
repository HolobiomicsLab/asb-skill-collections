---
name: spectral-data-integration
description: Use when you have three distinct mass spectrometry data sources (quantification table, metadata table, and spectral data from an MS library or reference dataset like omsw_pleurotus_ms2deepscore) and need to combine them into a single JSON output that preserves all three modalities for interactive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - msFeaST
  - jupyter-notebook
  - msFeaST_Dashboard_bundle.html
  techniques:
  - LC-MS
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

# spectral-data-integration

## Summary

Integrate mass spectrometry spectral data with quantification tables and metadata in a Jupyter notebook pipeline to produce a unified JSON artifact suitable for interactive dashboard exploration. This skill is essential when combining multi-modal MS data sources (spectral library matches, abundance measurements, sample annotations) into a single downstream-ready format.

## When to use

You have three distinct mass spectrometry data sources (quantification table, metadata table, and spectral data from an MS library or reference dataset like omsw_pleurotus_ms2deepscore) and need to combine them into a single JSON output that preserves all three modalities for interactive visualization and downstream analysis in the msFeaST dashboard.

## When NOT to use

- Input data are already pre-integrated or exist in a single unified matrix format (e.g., a feature table with all metadata as columns); this skill is for combining separate tables.
- Spectral data are not available or not relevant to your analysis goal; use simpler quantification-only pipelines instead.
- You only need to visualize quantification data without spectral or metadata context; simpler export to CSV or HDF5 may suffice.

## Inputs

- quantification table (numeric matrix: features × samples with abundance/intensity values)
- metadata table (sample annotations, experimental metadata, grouping variables)
- spectral data (mass spectrometry spectral library matches, MS2 fragmentation data, or spectral similarity scores, e.g., omsw_pleurotus_ms2deepscore dataset)

## Outputs

- dashboard_data.json (unified JSON text file conforming to msFeaST dashboard schema, containing integrated quantification, metadata, and spectral information)

## How to apply

Load the quantification table (abundance/intensity values across samples), metadata table (sample annotations and experimental design), and spectral data (library matches, fragmentation patterns, or spectral similarity scores) into the msfeast_pipeline notebook within a Jupyter environment. The notebook coordinates alignment and cross-referencing of these three tables by sample and compound identifiers. Execute the pipeline sequentially, ensuring all required user input fields (highlighted in magenta italics in the notebook) are populated with correct file paths and processing parameters. The pipeline outputs a single JSON text file conforming to the dashboard data schema, containing integrated feature information, quantification across samples, metadata for visualization filters, and spectral metadata for compound identification. Validate the output JSON contains all required fields for the interactive dashboard before loading into the msFeaST_Dashboard_bundle.html visualization tool.

## Related tools

- **jupyter-notebook** (Execution environment for the msfeast_pipeline notebook; orchestrates loading, alignment, and transformation of the three data sources into JSON output)
- **msFeaST** (Python module providing the pipeline logic and data integration functions; handles cross-referencing and schema compliance for dashboard-compatible JSON output) — https://github.com/kevinmildau/msFeaST
- **msFeaST_Dashboard_bundle.html** (Interactive visualization tool that loads and displays the integrated JSON output for exploration of quantification, metadata, and spectral data)

## Examples

```
jupyter-notebook
# In notebook cell:
# Load preprocessing_mushroom_type_comparison.ipynb, then msfeast_pipeline_mushroom_type_comparison.ipynb
# Change data filepaths in magenta italics fields to point to your quantification table, metadata table, and spectral data
# Run all cells to produce dashboard_data.json
```

## Evaluation signals

- The output JSON file is valid JSON and can be parsed without errors in Python or a JSON validator.
- The JSON contains required fields for dashboard visualization: quantification data (feature abundance per sample), metadata (sample groupings and annotations), and spectral metadata (library identifiers or MS2 similarity scores).
- The integrated JSON can be successfully loaded into the msFeaST_Dashboard_bundle.html without schema validation errors or missing field warnings.
- Cross-references between sample identifiers in the quantification table, metadata table, and spectral data are consistent and complete (no orphaned samples or features).
- The 'dataview' tab in the interactive dashboard displays all loaded samples and their associated features with correct abundance values and metadata annotations.

## Limitations

- msFeaST pre-processing and pipeline workflows have been tested on macOS and Linux; Windows support is currently being worked on and may encounter path or dependency issues.
- R dependencies (globaltest, dplyr, tibble, readr, listenv, survival, Matrix, BiocManager) must be installed at exact specified versions; mismatched R package versions or R version ≠ 4.3.3 may cause pipeline failures.
- The pipeline assumes alignment of sample identifiers across all three input tables; mismatches or missing identifiers will result in incomplete integration or data loss.
- Spectral data format must match the expected schema (e.g., omsw_pleurotus_ms2deepscore structure); non-standard formats may require manual preprocessing before pipeline execution.
- Terminal and conda environment path caching can cause R and rscript to use incorrect installation paths; a fresh terminal and explicit conda activation are required between installation and execution.

## Evidence

- [intro] complete example of quantification table, metadata table, and spectral data processing: "complete example of quantification table, metadata table, and spectral data processing"
- [intro] The jupyter-notebook pipeline produces a JSON text file for interactive exploration: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
- [methods] Processing three data sources within the pipeline: "Load the omsw_pleurotus example dataset (quantification table, metadata table, and spectral data) into the Jupyter notebook pipeline. 3. Execute the msfeast_pipeline notebook to process and integrate"
- [methods] Output schema compliance requirement: "Export the processed output as a JSON text file conforming to the dashboard data schema. 5. Validate that the generated JSON contains required fields for interactive visualization"
- [readme] R environment configuration with specific versions: "R is installed within this conda environment at version 4.3.3, and any R dependencies are installed"
- [readme] Path caching issue during R installation: "In rare cases where the rscript command is run from the terminal prior to the conda installation of R as instructed above, the temporary cached path to R used within conda may be faulty."
