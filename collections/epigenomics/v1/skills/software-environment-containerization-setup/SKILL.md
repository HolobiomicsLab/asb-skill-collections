---
name: software-environment-containerization-setup
description: Use when you have a bioinformatics pipeline (like HiC-Pro) with mixed Python, R, and compiled tool dependencies, and you need to ensure consistent reproducibility across machines and team members without manual per-tool installation. Use this when dependencies include version-pinned libraries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3169
  tools:
  - MultiQC 1.8
  - R
  - bowtie2
  - samtools (>=1.9)
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - pysam (>=0.15.4)
  - ggplot2 (>2.2.1)
  - RColorBrewer
  - iced
  - conda
  - Python (>3.7)
  - bx-python (>=0.8.8)
  - Miniconda
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- R (http://www.r-project.org/) with the following packages
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- numpy (>=1.18.1) - http://www.scipy.org/scipylib/download.html
- scipy (>=1.4.1) - http://www.scipy.org/scipylib/download.html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hicpro
    doi: 10.1186/s13059-015-0831-x
    title: hicpro
  dedup_kept_from: coll_hicpro
schema_version: 0.2.0
---

# software-environment-containerization-setup

## Summary

Create and verify a reproducible Conda environment for Hi-C data processing pipelines, ensuring all Python (>3.7), R, and compiled tool dependencies are correctly installed, resolved in PATH, and functionally validated. This skill bridges the gap between abstract dependency specifications and a working, testable runtime.

## When to use

You have a bioinformatics pipeline (like HiC-Pro) with mixed Python, R, and compiled tool dependencies, and you need to ensure consistent reproducibility across machines and team members without manual per-tool installation. Use this when dependencies include version-pinned libraries (e.g., scipy >=1.4.1, ggplot2 >2.2.1), optional auto-installable tools (bowtie2, samtools), and external modules no longer bundled with the pipeline (iced).

## When NOT to use

- The pipeline is already running successfully in a pre-built Docker or Singularity container and no local environment customization is needed.
- All dependencies are already system-installed (non-Conda) and you only need to point to existing paths via config files, not create a new isolated environment.
- You are working in a cluster scheduler (TORQUE, SGE, SLURM, LSF) where module files or pre-configured environments are centrally managed and no custom Conda environment is permitted.

## Inputs

- environment.yml or conda environment specification file
- Miniconda/Anaconda installation (or system Python with conda available)
- Optional: config-install.txt or similar configuration template for tool path overrides

## Outputs

- Activated Conda environment with all dependencies installed and verified
- Dependency verification report documenting Python version, all installed library versions, R packages, tool paths, and import/execution test results
- Summary of resolved tool paths (bowtie2, samtools, iced) in PATH or environment variables

## How to apply

Start by obtaining or reconstructing the environment specification file (environment.yml) that lists all Conda-resolvable dependencies with version constraints. Install Miniconda if absent, then create a new isolated Conda environment using `conda env create -f environment.yml -p <install_path>`. Activate the environment and systematically verify each dependency class: (1) Python version and importability of core libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4) via import statements; (2) R availability and required packages (ggplot2 >2.2.1, RColorBrewer, grid) via `library()` calls in R; (3) compiled tool binaries (bowtie2, samtools >=1.9) in PATH via `which` and `--version` checks; (4) separately install and verify non-bundled modules (iced from https://github.com/hiclib/iced). Document all resolved paths, versions, and import success in a summary report, which serves as proof of correct containerization and enables debugging if downstream tools fail.

## Related tools

- **conda** (Environment creation and dependency resolution across Python, R, and compiled tools; isolated workspace management) — https://docs.conda.io/en/latest/
- **Python (>3.7)** (Runtime interpreter for pipeline scripts; core dependency host)
- **bx-python (>=0.8.8)** (Bioinformatics utilities for sequence file manipulation within Hi-C pipeline) — https://pypi.python.org/pypi/bx-python
- **numpy (>=1.18.1)** (Numerical array operations required by scipy, pandas, and Hi-C data structures) — http://www.scipy.org/scipylib/download.html
- **scipy (>=1.4.1)** (Scientific computing routines for matrix operations and statistical functions in contact map processing) — http://www.scipy.org/scipylib/download.html
- **pysam (>=0.15.4)** (Python wrapper for reading and writing SAM/BAM alignment files in Hi-C read mapping pipeline) — https://github.com/pysam-developers/pysam
- **R** (Runtime for statistical graphics and normalization visualization) — http://www.r-project.org/
- **ggplot2 (>2.2.1)** (R package for generating publication-quality contact map and quality control plots)
- **RColorBrewer** (R package providing color palettes for Hi-C heatmap visualization)
- **bowtie2** (Read mapper for aligning Hi-C paired-end reads to reference genome; auto-installable if absent) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools (>=1.9)** (BAM/SAM file sorting, filtering, and coordinate validation; auto-installable if absent)
- **iced** (ICE (Iterative Correction and Eigenvalue) normalization of Hi-C contact matrices; must be independently installed from external repo) — https://github.com/hiclib/iced
- **Miniconda** (Lightweight conda distribution for isolated environment creation and package management) — https://docs.conda.io/en/latest/miniconda.html

## Examples

```
conda env create -f HiC-Pro/environment.yml -p ~/hicpro_env && conda activate ~/hicpro_env && python -c "import pysam, numpy, scipy; print('Python deps OK')" && R --slave -e "library(ggplot2); library(RColorBrewer); cat('R deps OK\n')" && bowtie2 --version && samtools --version && pip install iced && python -c "from iced import normalization; print('iced OK')"
```

## Evaluation signals

- Python version check returns >3.7 and matches environment specification: `python --version`
- All core Python libraries import without error and report correct versions: `python -c 'import numpy; print(numpy.__version__)'` returns >=1.18.1, etc.
- R libraries load successfully and match version constraints: `R --slave -e 'library(ggplot2); packageVersion("ggplot2")'` returns >2.2.1
- Tool binaries are executable and in PATH with correct versions: `bowtie2 --version` returns valid output, `samtools --version` reports >=1.9
- iced module imports and ICE function is callable: `python -c 'from iced import normalization'` succeeds without error
- Dependency summary report lists all resolved paths, versions, and test outcomes—no missing or incompatible versions

## Limitations

- Conda environment.yml file must already exist or be manually constructed; this skill does not generate specifications from scratch. If the specification is incomplete or outdated, auto-installation of fallback tools (bowtie2, samtools) may be triggered, which can be slow or fail on restricted networks.
- iced is no longer bundled with HiC-Pro source and must be independently installed from its external GitHub repository; Conda will not resolve it automatically, requiring manual `pip install` or git clone + setup.py steps.
- On macOS, the default Unix sort command does not support the -V flag required by HiC-Pro; users must manually install GNU core utilities (`brew install coreutils`) before containerization is complete.
- This skill verifies dependency presence and importability but does not validate functional correctness of tools or their integration into the full pipeline—only that binaries are in PATH and libraries can be imported.
- Conda channels (especially bioconda for pysam and iced dependencies) may be slow or unreachable in offline or restricted network environments; pre-built environment files or Docker containers are recommended as fallbacks.

## Evidence

- [other] Install miniconda if not already present, following the official Miniconda installation documentation. Create a Conda environment from the HiC-Pro environment.yml file using conda env create, specifying the installation path with the -p flag.: "Install miniconda if not already present, following the official Miniconda installation documentation. 2. Create a Conda environment from the HiC-Pro environment.yml file using conda env create,"
- [other] Activate the newly created Conda environment using conda activate. Verify that Python version is >3.7 and that all required Python libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4, argparse) are installed and importable.: "Activate the newly created Conda environment using conda activate. 4. Verify that Python version is >3.7 and that all required Python libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1,"
- [other] Verify that R is available and that required packages (ggplot2 >2.2.1, RColorBrewer, grid) are installed by testing library() calls in R. Verify that tool binaries bowtie2 and samtools (>=1.9) are in PATH and executable.: "Verify that R is available and that required packages (ggplot2 >2.2.1, RColorBrewer, grid) are installed by testing library() calls in R. 6. Verify that tool binaries bowtie2 and samtools (>=1.9) are"
- [other] Independently install the iced module from https://github.com/hiclib/iced and verify it is importable, since it is no longer part of HiC-Pro source code.: "Independently install the iced module from https://github.com/hiclib/iced and verify it is importable, since it is no longer part of HiC-Pro source code."
- [readme] In order to ease the installation of HiC-Pro dependancies, we provide a `yml` file for conda with all required tools. In order to build your conda environment, first install miniconda and use: conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV: "In order to ease the installation of HiC-Pro dependancies, we provide a `yml` file for conda with all required tools. In order to build your conda environment, first install miniconda and use: conda"
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them. You can also edit the *config-install.txt* file and manually defined the paths to dependencies.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them. You can also edit the *config-install.txt* file and manually defined the"
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [readme] The pipeline requires the following dependencies: The bowtie2 mapper, Python (>3.7) with pysam (>=0.15.4), bx-python(>=0.8.8), numpy(>=1.18.1), and scipy(>=1.4.1) libraries, R with the RColorBrewer and ggplot2 (>2.2.1) packages, g++ compiler, samtools (>1.9): "The pipeline requires the following dependencies: The bowtie2 mapper, Python (>3.7) with pysam (>=0.15.4), bx-python(>=0.8.8), numpy(>=1.18.1), and scipy(>=1.4.1) libraries, R with the RColorBrewer"
