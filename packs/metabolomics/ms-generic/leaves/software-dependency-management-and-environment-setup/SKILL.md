---
name: software-dependency-management-and-environment-setup
description: Use when you are preparing to run the MetaboDirect pipeline for the first
  time on a new machine, or you need to reproduce a published benchmark or analysis
  on a different OS (Windows, Linux, MacOS) and want to guarantee that all six pipeline
  steps (data pre-processing, diagnostics, exploration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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
  - py4cytoscape
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based
  approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and
  is available to install through the Python Package Index... It requires the Python
  dependencies NumPy
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

# software-dependency-management-and-environment-setup

## Summary

Install and configure MetaboDirect and its runtime dependencies (Python, R, Cytoscape with specific libraries) to ensure a reproducible computational environment for FT-ICR MS data analysis. This skill is essential because MetaboDirect's pipeline integrates multiple languages and external tools, and version mismatches or missing libraries cause silent failures or incomplete output.

## When to use

You are preparing to run the MetaboDirect pipeline for the first time on a new machine, or you need to reproduce a published benchmark or analysis on a different OS (Windows, Linux, MacOS) and want to guarantee that all six pipeline steps (data pre-processing, diagnostics, exploration, chemodiversity, statistics, transformation networks) execute without missing dependencies or version conflicts.

## When NOT to use

- You are analyzing metabolomic data in a different format (e.g., mzML or netCDF raw spectra) that has not already been processed through Formularity or CoreMS to produce assigned molecular formulas in .csv format—MetaboDirect expects pre-assigned formulas as input, not raw mass spectrometry data.
- Your analysis goal requires only visualization or post-hoc statistical comparison of already-computed diversity metrics; dependency setup is unnecessary overhead if you are reusing pre-computed outputs.
- You are running on a shared HPC cluster with pre-installed module systems (e.g., Lmod or Environment Modules) where a system administrator has already configured a MetaboDirect environment module—use `module load metabodirect` instead of manual installation.

## Inputs

- Python interpreter (version ≥3.5)
- R interpreter (version ≥4)
- Cytoscape application (version ≥3.8) with FileTransfer plugin
- pip or Python package manager
- R library installation method (install.packages or conda)
- System PATH environment variable

## Outputs

- Functional MetaboDirect command-line tool accessible via `metabodirect` command
- Python environment with argparse, numpy, pandas, seaborn, more-itertools, py4cytoscape, statsmodels installed
- R environment with tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, SYNCSA, ggvenn, ggrepel installed
- Cytoscape application with FileTransfer plugin enabled and py4cytoscape connectivity verified
- Test run report with pipeline execution time and confirmation that all six steps completed

## How to apply

Install MetaboDirect v0.3.4 from PyPI using `pip install metabodirect`, then verify that Python 3.5+ and R 4+ are in your PATH. Install R packages (tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, SYNCSA, ggvenn, ggrepel) using R's install.packages() or a dependency manager. Install Cytoscape 3.8+ and the FileTransfer plugin separately; MetaboDirect calls py4cytoscape to communicate with it. Verify installation by running `metabodirect -h` and test the full pipeline on a small dataset (e.g., 4–40 samples) to confirm all six steps and optional KEGG annotation execute without errors. Record the wall-clock time for this test run to establish a baseline for performance validation.

## Related tools

- **MetaboDirect** (Primary command-line pipeline for FT-ICR MS analysis that orchestrates data pre-processing, diagnostics, exploration, chemodiversity, statistics, and transformation network generation) — https://github.com/Coayala/MetaboDirect
- **Python** (Runtime language for MetaboDirect core pipeline logic and dependency management via pip)
- **R** (Runtime language for statistical analysis (vegan, SYNCSA), visualization (ggpubr, ggnewscale), and KEGG database queries (KEGGREST))
- **Cytoscape** (Desktop application for visualization and interactive exploration of biochemical transformation networks generated by MetaboDirect; communicates via py4cytoscape)
- **py4cytoscape** (Python library that enables MetaboDirect to programmatically control Cytoscape for network visualization)
- **KEGGREST** (R package that queries the KEGG database to annotate mass-based transformations with putative metabolic pathways and modules)
- **vegan** (R package providing diversity metrics (alpha and beta diversity) used in chemodiversity analysis step)
- **SYNCSA** (R package providing community phylogenetic diversity and functional trait-based metrics for chemodiversity analysis)

## Examples

```
pip install metabodirect && metabodirect -h
```

## Evaluation signals

- Running `metabodirect -h` produces a help menu with all required arguments and does not raise ImportError or ModuleNotFoundError.
- All Python imports (numpy, pandas, seaborn, py4cytoscape, statsmodels) succeed without version conflicts when MetaboDirect executes.
- All R packages (tidyverse, vegan, SYNCSA, KEGGREST, ggpubr, ggnewscale, UpSetR, factoextra, pmartR, ggvenn, ggrepel) load successfully via `library()` within R scripts called by MetaboDirect.
- A test run on a small FT-ICR MS dataset (4–40 samples in Formularity .csv format) completes all six pipeline steps without hanging, timeout, or segmentation fault; wall-clock time for main pipeline on 40 samples is <1 minute, matching published benchmarks.
- Cytoscape launches and connects to MetaboDirect via py4cytoscape without authentication or socket errors; transformation networks render in the Cytoscape interface.

## Limitations

- MetaboDirect requires R 4 and above; installations on systems with R 3.x will fail to load tidyverse and modern packages, and downgrading R may break system package managers.
- Cytoscape 3.8+ must be installed and running as a separate desktop application; MetaboDirect cannot use Cytoscape if it is not in the user's PATH or if the FileTransfer plugin is not loaded, causing transformation network visualization to fail silently.
- KEGGREST queries are network-dependent and may timeout or return incomplete annotations if the KEGG REST API is unavailable or rate-limited; offline KEGG mirror or local database setup is not documented.
- Cross-platform path handling (Windows backslashes vs. Unix forward slashes) may cause issues if environment variables or shell commands are not properly escaped; testing on each target OS (Windows, Linux, MacOS) is recommended.
- Python 3.5 support is nominally specified but is outdated; NumPy and pandas have dropped Python 3.5 support in recent versions, so actual minimum Python version is likely 3.8 or higher.

## Evidence

- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules"
- [other] Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS).: "Install MetaboDirect (v0.3.4) via Python Package Index with dependencies NumPy, pandas, seaborn, py4cytoscape, and matplotlib, ensuring compatibility on the target OS (Windows, Linux, or MacOS)"
- [readme] MetaboDirect can be installed directly from PyPi using: pip install metabodirect: "MetaboDirect can be installed directly from PyPi using: pip install metabodirect"
- [readme] For more information please check the User Manual at metabodirect.readthedocs.io: "For more information please check the User Manual"
- [other] Run the main MetaboDirect pipeline (six steps: data pre-processing, data diagnostics, data exploration, chemodiversity analysis, statistical analysis, and transformation network analysis) on each of the 40-sample and 120-sample mock datasets using a single command, recording elapsed wall-clock time.: "Run the main MetaboDirect pipeline (six steps: data pre-processing, data diagnostics, data exploration, chemodiversity analysis, statistical analysis, and transformation network analysis) on each of"
