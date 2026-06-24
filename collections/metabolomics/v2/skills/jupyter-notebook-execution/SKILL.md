---
name: jupyter-notebook-execution
description: Use when when you have three coordinated mass spectrometry data tables
  (quantification, metadata, spectral) ready for integrated preprocessing and statistical
  analysis, and you need to generate a standardized JSON artifact for downstream interactive
  exploration rather than static tabular outputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3577
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3307
  tools:
  - jupyter-notebook
  - msFeaST
  - conda
  - R (v4.3.3)
  - Jupyter
  - Python
  - cwieder/metabolomics-ORA
  - metabolomics-ORA repository
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btae584
  title: msFeaST
- doi: 10.1371/journal.pcbi.1009105
  title: ''
evidence_spans:
- The jupyter-notebook pipeline produces the a text file in json format
- github.com__kevinmildau__msFeaST
- The Python code to generate the results is contained within the Jupyter notebook
- Jupyter notebook **src/reproducible_simulations.ipynb**
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  - build: coll_ora_cq
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_msfeast_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae584
  all_source_dois:
  - 10.1093/bioinformatics/btae584
  - 10.1371/journal.pcbi.1009105
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# jupyter-notebook-execution

## Summary

Execute Jupyter notebooks within a conda-managed Python environment to process mass spectrometry data (quantification tables, metadata, spectral data) through the msFeaST pipeline, producing JSON output suitable for interactive dashboard visualization.

## When to use

When you have three coordinated mass spectrometry data tables (quantification, metadata, spectral) ready for integrated preprocessing and statistical analysis, and you need to generate a standardized JSON artifact for downstream interactive exploration rather than static tabular outputs.

## When NOT to use

- Input data is already in JSON dashboard format—skip directly to dashboard loading.
- Windows operating system—msFeaST preprocessing is tested only on macOS and Linux; Windows support is still being developed.
- R dependencies fail to install or sessionInfo() does not confirm globaltest, dplyr, tibble, readr, listenv, survival, and Matrix at required versions—execution will fail without correct R environment.

## Inputs

- quantification_table (numeric matrix, e.g., feature-by-sample abundance)
- metadata_table (sample annotations and experimental design)
- spectral_data (mass spectrometry spectral records)
- msfeast_pipeline.ipynb (preprocessing Jupyter notebook)

## Outputs

- dashboard_data.json (JSON text file conforming to msFeaST dashboard schema)
- processed feature and metadata tables (intermediate notebook outputs)

## How to apply

Create and activate a conda environment (Python 3.10 with R 4.3.3 and msFeaST dependencies) on macOS or Linux. Open the msfeast_pipeline notebook in the activated environment and populate the magenta-italicized user input fields with paths to your quantification, metadata, and spectral data files. Execute the notebook cells sequentially; the pipeline integrates the three data sources and exports a JSON text file conforming to the dashboard data schema. Validate that the resulting JSON contains required fields (inspectable by loading into msFeaST_Dashboard_bundle.html in a desktop browser) before proceeding to interactive visualization.

## Related tools

- **jupyter-notebook** (Interactive notebook interface for executing preprocessing and pipeline cells with user-defined parameters)
- **msFeaST** (Python module providing the data integration and statistical processing workflow; installed via pip from repository) — https://github.com/kevinmildau/msfeast
- **conda** (Environment and dependency manager ensuring isolated, reproducible Python/R versions and package pinning) — https://conda.io/projects/conda/en/latest/user-guide/install/index.html
- **R (v4.3.3)** (Statistical runtime for globaltest and related bioinformatic packages invoked from notebook cells)

## Examples

```
conda activate msfeast_environment && jupyter-notebook && # then open msfeast_pipeline_mushroom_type_comparison.ipynb and update filepaths in magenta italics, execute all cells
```

## Evaluation signals

- JSON file is successfully written to the specified output path with non-zero file size.
- JSON validates against the msFeaST dashboard schema (can be opened and parsed by msFeaST_Dashboard_bundle.html without schema errors).
- Interactive dashboard displays loaded data in the 'dataview' tab, confirming required fields (feature identifiers, abundance values, sample metadata) are present and correctly formatted.
- R sessionInfo() executed before notebook launch confirms all six required packages (dplyr, tibble, readr, listenv, globaltest, survival) are loaded and at development/pinned versions.
- Notebook execution completes without RuntimeError or ImportError related to msFeaST, R integration, or data schema mismatches.

## Limitations

- Tested and working only on macOS and Linux; Windows support is still in development—users on Windows should expect setup failures or incompatibilities.
- R package installation via rscript can be derailed by cached R paths if terminal was previously used; resolving requires closing and reopening the terminal and reactivating conda environment.
- Some IDE terminals (e.g., VSCode) may default into conda environments automatically, causing R/rscript path misalignment; safest practice is to use a fresh terminal and activate the environment explicitly.
- No changelog is available; version pinning and reproducibility guarantees are not formally documented.
- If globaltest or other R dependencies fail to install at required versions, the entire notebook execution will fail because msFeaST statistical functions depend on them; no fallback mode is available.

## Evidence

- [readme] The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
- [readme] Complete example of quantification table, metadata table, and spectral data processing required for msFeaST: "notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST"
- [readme] To make use of your own data, change the data filepath arguments to your own data file location and run the pipeline. Text in magenta italics font highlights required user input for the pipeline.: "To make use of your own data, change the data filepath arguments to your own data file location and run the pipeline. Text in magenta italics font highlights required user input"
- [readme] conda create --name msfeast_environment python=3.10 and conda activate to manage environment isolation: "conda create --name msfeast_environment python=3.10; conda activate msfeast_environment; conda install conda-forge::r-base=4.3"
- [readme] The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on.: "The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on"
- [readme] To avoid rscript command caching problems, we recommend closing the terminal after this step and reopening it, and re-entering conda activate msfeast_environment: "To avoid rscript command caching problems, we recommend closing the terminal after this step and reopening it, and re-entering conda activate msfeast_environment"
- [readme] pip install git+https://github.com/kevinmildau/msfeast.git installs the Python module and dependencies: "pip install "git+https://github.com/kevinmildau/msfeast.git" to install the msFeaST python module and any required Python dependencies"
