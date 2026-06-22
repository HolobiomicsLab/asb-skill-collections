---
name: command-line-tool-installation-and-configuration
description: 'Use when before launching any MetaboDirect pipeline run on a new system or environment. Trigger conditions: (1) first-time setup on a target OS (Windows, Linux, or macOS); (2) environment lacks Python 3.5+, R 4.0+, or Cytoscape 3.8+;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MetaboDirect
  - Python
  - R
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - Formularity
  - KEGGREST
  - vegan
  - SYNCSA
  - Cytoscape
  - pip
  - numpy
  - py4cytoscape
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# command-line-tool-installation-and-configuration

## Summary

Installation and configuration of MetaboDirect and its dependencies (Python, R, Cytoscape, and domain libraries) to establish a working command-line environment for FT-ICR MS data analysis. This skill ensures all required computational infrastructure is in place before running the pipeline.

## When to use

Before launching any MetaboDirect pipeline run on a new system or environment. Trigger conditions: (1) first-time setup on a target OS (Windows, Linux, or macOS); (2) environment lacks Python 3.5+, R 4.0+, or Cytoscape 3.8+; (3) required Python packages (numpy, pandas, seaborn, py4cytoscape, statsmodels) or R packages (tidyverse, vegan, KEGGREST, SYNCSA, UpSetR, ggpubr, pmartR) are missing or outdated; (4) reproducibility demands pin specific versions of MetaboDirect (e.g., v0.3.4 for benchmarking).

## When NOT to use

- If MetaboDirect is already installed and verified with `metabodirect -h` — skip to data preparation and pipeline execution.
- If input is already a processed metabolomic feature table or molecular formula assignment (`.csv` format) — proceed directly to pipeline execution with `metabodirect` command, not installation.
- If targeting a system where system-level package management (conda, apt, Homebrew) conflicts with pip or manual R installation — consult the README and resolve environment conflicts first before attempting installation.

## Inputs

- System with internet access for package downloads
- Python ≥3.5 installation
- R ≥4.0 installation
- Cytoscape ≥3.8 installation
- PyPI or GitHub repository access

## Outputs

- Functional MetaboDirect command-line executable
- Installed Python dependencies (numpy, pandas, seaborn, py4cytoscape, statsmodels, more-itertools, argparse)
- Installed R packages (tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, SYNCSA, ggvenn, ggrepel)
- Cytoscape with FileTransfer app enabled
- Environment configuration verified via `metabodirect -h`

## How to apply

Install MetaboDirect via PyPI or from source by cloning the GitHub repository, ensuring Python ≥3.5, R ≥4.0, and Cytoscape ≥3.8 are present on the target system. Install all listed Python dependencies (argparse, numpy, pandas, seaborn, more-itertools, py4cytoscape, statsmodels) and R packages (tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, SYNCSA, ggvenn, ggrepel). In Cytoscape, ensure the FileTransfer app is installed. Verify installation by running `metabodirect -h` to confirm the command-line interface is accessible. Document the installed version and environment details (OS, Python/R versions, package versions) for reproducibility and troubleshooting.

## Related tools

- **Python** (Runtime environment and dependency manager for MetaboDirect core and package installation)
- **R** (Computational backend for statistical analysis, diversity metrics (vegan, SYNCSA), and visualization (ggpubr, ggnewscale))
- **Cytoscape** (Graph visualization and network analysis platform for biochemical transformation network generation and display)
- **pip** (Python package installer for MetaboDirect and Python dependencies)
- **numpy** (Numerical computation library for array operations in MetaboDirect data processing)
- **pandas** (Data manipulation and I/O library for handling Formularity .csv molecular formula tables)
- **seaborn** (Statistical data visualization library for generating plots and heatmaps in MetaboDirect)
- **py4cytoscape** (Python-to-Cytoscape bridge for programmatic network construction and visualization)
- **vegan** (R package for ecological diversity metrics (chemodiversity) calculation)
- **KEGGREST** (R package for querying KEGG database to obtain putative pathway and module annotations)
- **SYNCSA** (R package for calculating diversity metrics in MetaboDirect chemodiversity analysis)

## Examples

```
pip install metabodirect && python -c 'import metabodirect; print("Installation successful")' && metabodirect -h
```

## Evaluation signals

- Successfully execute `metabodirect -h` without errors; output displays command-line options and help text.
- Python import test: `python -c 'import metabodirect; print(metabodirect.__version__)'` returns version string (e.g., 0.3.4).
- Verify all Python dependencies are installed: `pip show numpy pandas seaborn py4cytoscape statsmodels` returns package information for each.
- Verify all R packages are installed: `Rscript -e 'library(vegan); library(KEGGREST); library(SYNCSA)'` completes without package loading errors.
- Test end-to-end: run `metabodirect -h` followed by `metabodirect --version` (if available) or a dry-run on sample data to confirm pipeline initialization.
- Check Cytoscape is accessible: Cytoscape should launch and FileTransfer app should be listed in app manager.

## Limitations

- Installation requires internet access to download packages from PyPI and R CRAN repositories; offline environments need pre-cached packages.
- MetaboDirect requires both Python and R ecosystems, increasing system complexity and potential for version conflicts between language runtimes.
- R package pmartR (for normalization tests) may have compilation requirements on some systems; building from source can fail if system development tools are missing.
- Cytoscape 3.8+ and FileTransfer app installation are OS-specific and manual; no automated script provided in the README.
- Python 3.5 support (minimum specified version) is deprecated; testing on Python 3.8+ is recommended but not explicitly documented in the README.

## Evidence

- [readme] MetaboDirect can be installed directly from PyPi using: pip install metabodirect: "MetaboDirect can be installed directly from [PyPi](https://pypi.org/project/metabodirect/0.1.1/) using: ```pip install metabodirect```"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules:"
- [methods] Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS).: "Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS)."
- [readme] Additionally it can be installed from source by cloning its GitHub repository: "Additionally it can be installed from source by cloning its [GitHub repository](https://github.com/Coayala/MetaboDirect)"
- [readme] Information about the arguments can be obtaining using the option -h/--help: metabodirect -h: "Information about the arguments can be obtaining using the option -h/--help: ```metabodirect -h```"
- [supplementary] The complete code for the MetaboDirect pipeline is freely available at its GitHub repository: https://github.com/Coayala/MetaboDirect: "The complete code for the MetaboDirect pipeline is freely available at its GitHub repository: https:// github.com/ Coaya la/ Metab oDire ct."
