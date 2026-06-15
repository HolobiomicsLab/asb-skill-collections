---
name: conda-environment-creation-and-management
description: Use when you need to deploy a complex multi-language pipeline (e.g., HiC-Pro) that requires Python >3.7 libraries (pysam, bx-python, numpy, scipy), R packages (ggplot2, RColorBrewer), and compiled tool binaries (bowtie2, samtools >=1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3673
  tools:
  - MultiQC 1.8
  - conda
  - R
  - bowtie2
  - samtools (>=1.9)
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - pysam (>=0.15.4)
  - ggplot2 (>2.2.1)
  - RColorBrewer
  - iced
  - samtools
  - pysam
  - bx-python
  - numpy
  - scipy
  - ggplot2
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml
- R (http://www.r-project.org/) with the following packages
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- numpy (>=1.18.1) - http://www.scipy.org/scipylib/download.html
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

# conda-environment-creation-and-management

## Summary

Create and activate isolated Conda environments from YAML specification files to deploy multi-language scientific pipelines (Python, R, compiled binaries) with pinned dependency versions. This skill ensures reproducible installation of Hi-C data processing tools and their dependencies across heterogeneous computing environments.

## When to use

You need to deploy a complex multi-language pipeline (e.g., HiC-Pro) that requires Python >3.7 libraries (pysam, bx-python, numpy, scipy), R packages (ggplot2, RColorBrewer), and compiled tool binaries (bowtie2, samtools >=1.9) in a way that is reproducible, isolated from system packages, and portable across laptops and HPC clusters. Use this skill when an environment.yml specification file is provided and you want to avoid manual installation of interdependent tools with conflicting system dependencies.

## When NOT to use

- The target environment already exists and is actively in use — use `conda update` or environment reconstruction instead of `create`.
- You require a container-based deployment (Docker or Singularity) — use HiC-Pro's pre-built Docker image from Docker Hub or Singularity recipe instead.
- Python or R dependencies have unresolvable conflicts in Conda — fall back to manual compilation or virtual environments (venv) for isolated Python-only workflows.

## Inputs

- environment.yml specification file (YAML format with Python, R, and bioconda package declarations)
- Miniconda or Anaconda distribution (pre-installed or to be installed)
- Target installation path (directory where environment will be created)

## Outputs

- Isolated Conda environment directory with all dependencies installed and verified
- Activated environment shell session ready for pipeline execution
- Summary report documenting all resolved tool paths, library versions, and dependency integrity

## How to apply

First, install Miniconda if not already present by following the official Miniconda installation documentation. Second, create a Conda environment from the HiC-Pro environment.yml file using `conda env create -f environment.yml -p <installation_path>`, where the `-p` flag specifies the full path for the environment rather than installing into the default envs directory. Third, activate the environment using `conda activate <installation_path>`. Fourth, verify Python version is >3.7 and test import statements for critical libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4). Fifth, verify R availability and test R package installation via `library(ggplot2); library(RColorBrewer)` calls. Finally, verify that tool binaries bowtie2 and samtools >=1.9 are in PATH and executable, noting that bowtie2 and samtools can be automatically installed by HiC-Pro if not detected, but iced must be independently installed from https://github.com/hiclib/iced since it is no longer bundled with HiC-Pro.

## Related tools

- **conda** (Package manager and environment orchestrator for creating, activating, and managing isolated computational environments from YAML specifications) — https://docs.conda.io/en/latest/miniconda.html
- **bowtie2** (Read mapper installed automatically by HiC-Pro if not detected in PATH; requires version >2.2.2 for allele-specific analysis) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools** (BAM/SAM file manipulator installed automatically by HiC-Pro if not detected; requires version >=1.9) — http://samtools.sourceforge.net/
- **pysam** (Python wrapper for samtools C-API; required version >=0.15.4) — https://github.com/pysam-developers/pysam
- **iced** (Python module for ICE normalization of Hi-C contact maps; must be independently installed since it is no longer part of HiC-Pro source code) — https://github.com/hiclib/iced
- **bx-python** (Bioinformatics library for interval set operations and sequence handling; required version >=0.8.8)
- **numpy** (Numerical computing library for array operations; required version >=1.18.1) — http://www.scipy.org/scipylib/download.html
- **scipy** (Scientific computing library for signal processing and statistics; required version >=1.4.1) — http://www.scipy.org/scipylib/download.html
- **ggplot2** (R package for data visualization of Hi-C contact maps and quality metrics; required version >2.2.1)
- **RColorBrewer** (R package providing color palettes for visualization)

## Examples

```
conda env create -f /path/to/HiC-Pro/environment.yml -p /opt/hicpro_env && conda activate /opt/hicpro_env && python -c 'import pysam, numpy, scipy; print("Dependencies OK")' && R -e 'library(ggplot2); cat(packageVersion("ggplot2"))'
```

## Evaluation signals

- Verify Python version output: `python --version` returns Python 3.x where x ≥ 7; version below 3.7 indicates environment creation failed or incorrect Python selected
- Test critical library imports without errors: `python -c 'import pysam, bx, numpy, scipy; print(pysam.__version__)'` confirms >=0.15.4 and all numpy/scipy/bx-python versions match specification
- Verify R packages are loadable: `R -e 'library(ggplot2); library(RColorBrewer); cat(packageVersion("ggplot2"))'` confirms ggplot2 >2.2.1
- Confirm tool binaries are in PATH and correct version: `which bowtie2 && bowtie2 --version` and `samtools --version` both succeed and return >=1.9 for samtools
- Test iced module installation separately: `python -c 'import iced; print(iced.__version__)'` succeeds after independent installation from GitHub, indicating HiC-Pro can access the normalization module

## Limitations

- HiC-Pro provides flexible installation that attempts automatic tool detection and installation only for bowtie2 and samtools; iced must be independently installed and is not managed by the environment.yml, requiring a separate manual step
- Conda channel priority and configuration (bioconda, conda-forge) must be correctly set before environment creation; users must add channels explicitly or rely on environment.yml to specify channel URLs, otherwise dependency resolution may fail
- The environment.yml file is specific to HiC-Pro version; upgrading HiC-Pro may require a new environment.yml to ensure compatibility of tool versions (e.g., samtools >=1.9 requirement, iced removal from bundled code)
- Conda environments can occupy significant disk space (multi-gigabyte for compiled tools and R packages); multiple environments for different projects will multiply storage costs, particularly on HPC systems with quota limits
- macOS users must install GNU core utilities to replace BSD sort (which does not support the -V option required by HiC-Pro); this prerequisite is not automatically resolved by Conda and must be handled separately

## Evidence

- [readme] In order to build your conda environment, first install miniconda and use: conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV; conda activate WHERE_TO_INSTALL_MY_ENV: "conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV"
- [readme] Python (>3.7) libraries, specifically pysam (>=0.15.4), bx-python(>=0.8.8), numpy(>=1.18.1), and scipy(>=1.4.1) libraries: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries"
- [methods] A couple of tools such as bowtie2 and samtools (>=1.9) can be automatically installed if not detected: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [readme] R with the RColorBrewer and ggplot2 (>2.2.1) packages required: "R with the *RColorBrewer* and *ggplot2 (>2.2.1)* packages"
- [readme] For Mac OS user, please install the GNU core utilities since Unix sort with -V option is required: "Unix sort (**which support -V option**) is required ! For Mac OS user, please install the GNU core utilities !"
- [readme] Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options: "Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options."
