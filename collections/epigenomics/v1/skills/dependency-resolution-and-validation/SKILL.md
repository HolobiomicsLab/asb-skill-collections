---
name: dependency-resolution-and-validation
description: Use when before running HiC-Pro or similar multi-stage pipelines on a new system or environment, especially when dependency installation is not automated (e.g., not in a conda environment or container).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
  tools:
  - MultiQC 1.8
  - iced
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - Python (>3.7)
  - pysam (>=0.15.4)
  - bx-python (>=0.8.8)
  - bowtie2
  - samtools (>=1.9)
  - R with RColorBrewer and ggplot2 (>2.2.1)
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- iced module is also required (https://github.com/hiclib/iced)
- Note that the iced module is also required (https://github.com/hiclib/iced)
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

# dependency-resolution-and-validation

## Summary

Systematically identify, install, and validate transitive dependencies for bioinformatics pipelines, ensuring compatibility across Python, compiled tools, and R packages before executing the main workflow. This skill is critical for reproducible Hi-C data processing, where missing or mismatched dependencies (e.g., iced, numpy, scipy) silently break normalization steps.

## When to use

Before running HiC-Pro or similar multi-stage pipelines on a new system or environment, especially when dependency installation is not automated (e.g., not in a conda environment or container). Use this skill when the article or README explicitly lists external dependencies with version constraints, and when downstream processing steps depend on optional modules that must be independently installed.

## When NOT to use

- Dependencies are already installed in a conda environment or container (use the pre-built environment instead)
- The pipeline provides an automated dependency-resolution mechanism (e.g., setup.py with install_requires, or a conda environment.yml file) that you have not yet attempted to run
- The input is a pre-configured Docker or Singularity container image with dependencies baked in

## Inputs

- Pipeline README or documentation specifying dependency list with version constraints
- config-install.txt or similar configuration template file
- Target system environment (Python version, package manager availability, PATH)
- Optional: existing environment.yml or requirements.txt file

## Outputs

- Configured and validated Python environment with all required packages installed
- Updated config file (e.g., config-install.txt) with paths to dependencies and environment variables
- Installation log or validation report confirming version and API checks
- Ready-to-run pipeline environment for downstream workflow execution

## How to apply

First, verify the availability and version of the Python interpreter (>3.7 for HiC-Pro) in your target environment. Next, systematically install each required dependency and its transitive dependencies in order of declaration, checking version constraints against the pipeline's documented requirements (e.g., numpy >=1.18.1, scipy >=1.4.1, iced from https://github.com/hiclib/iced). For optional dependencies that are no longer bundled with the main pipeline (e.g., iced, which HiC-Pro no longer includes in its source code), clone or download from the authoritative repository and install via pip or setup.py. After each installation, validate by importing the module in a Python interpreter and checking version/API availability. Document the installation paths and environment variables (PYTHONPATH, PREFIX, tool-specific paths) in a configuration file referenced by the main pipeline's install script (e.g., config-install.txt for HiC-Pro). Finally, run a smoke test that exercises the normalization or core functionality (e.g., import iced and call a key ICE method) to confirm dependencies are accessible to the pipeline.

## Related tools

- **iced** (Python module implementing ICE normalization algorithm for Hi-C contact matrices; must be independently installed from its source repository and imported to validate correct installation) — https://github.com/hiclib/iced
- **Python (>3.7)** (Interpreter required to run the pipeline and import all Python-based dependencies; version must be verified before proceeding)
- **numpy (>=1.18.1)** (Core numerical library required by iced and other Python modules; version constraint must be checked during installation) — http://www.scipy.org/scipylib/download.html
- **scipy (>=1.4.1)** (Scientific computing library for numerical algorithms; transitive dependency of iced with explicit version constraint) — http://www.scipy.org/scipylib/download.html
- **pysam (>=0.15.4)** (Python wrapper for SAM/BAM file manipulation; required for Hi-C read alignment processing steps) — https://github.com/pysam-developers/pysam
- **bx-python (>=0.8.8)** (Bioinformatics utilities for sequence and interval operations; required dependency with explicit version constraint) — https://pypi.python.org/pypi/bx-python
- **bowtie2** (Read mapper tool; may be automatically installed if not detected in PATH during HiC-Pro setup) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools (>=1.9)** (SAM/BAM file manipulation tool; may be automatically installed if not detected, with version constraint enforced)
- **R with RColorBrewer and ggplot2 (>2.2.1)** (Statistical and visualization environment; R packages required for Hi-C contact map plotting and QC reporting) — http://www.r-project.org/

## Examples

```
# Verify Python version and install iced with transitive dependencies
python --version  # confirm >3.7
pip install numpy>=1.18.1 scipy>=1.4.1
git clone https://github.com/hiclib/iced.git && cd iced && pip install .
# Validate installation
python -c "import iced; import numpy; import scipy; print('iced:', iced.__version__); print('Dependencies validated')"
# Update config-install.txt and run HiC-Pro setup
make configure && make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- Python interpreter version returned by `python --version` is >3.7
- Import test in Python interpreter: `import iced; print(iced.__version__)` returns a valid version string without ImportError or AttributeError
- Import test for transitive dependencies: `import numpy; import scipy; import pysam; import bx` all succeed without version or API errors
- Configuration file (config-install.txt) is populated with validated paths to bowtie2, samtools, R, and Python installations, and PYTHONPATH is set correctly
- Smoke test of ICE normalization: `python -c 'from iced import normalization; M = normalization.ICE_normalization(...)'` executes without import or runtime errors, confirming iced is callable from the pipeline

## Limitations

- The iced module is no longer bundled with HiC-Pro source code and must be independently installed; automatic installation via HiC-Pro's setup does not guarantee correct iced installation, requiring manual verification
- Version compatibility between iced and its transitive dependencies (numpy, scipy, scikit-learn, pandas) is not explicitly stated in the pipeline documentation; incompatible versions can cause silent failures in normalization that are difficult to debug after pipeline execution begins
- On macOS, the native sort command does not support the -V (version-sort) option required by HiC-Pro; GNU core utilities must be installed separately, adding an additional dependency-resolution step not mentioned in the Python/R dependency list
- Configuration file paths (config-install.txt) must be manually edited if dependencies are not in the system PATH; no automated fallback or environment variable substitution is provided, increasing risk of misconfiguration
- Docker, Singularity, and conda containers provide pre-resolved dependency stacks, but manual installation environments (e.g., cluster systems without container support) require full dependency resolution, making this skill essential but labor-intensive for non-standard platforms

## Evidence

- [methods] Iced is no longer part of the HiC-Pro source code, and should be independently installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [other] iced module is a required dependency for HiC-Pro's normalization pipeline and must be independently installed from HiC-Pro source code: "The iced module is a required dependency for HiC-Pro's normalization pipeline and must be independently installed from the HiC-Pro source code."
- [other] Verify Python (>3.7) availability and install iced with transitive dependencies (numpy >=1.18.1, scipy >=1.4.1) using pip or setup.py, then validate by importing and checking version/API in Python interpreter: "1. Verify Python (>3.7) is available and functional on the target system. 2. Clone or download the iced module from https://github.com/hiclib/iced. 3. Install iced and its transitive dependencies"
- [other] Document iced installation path and Python environment variables (PYTHONPATH) in configuration file for downstream HiC-Pro normalization steps: "5. Document the iced installation path and Python environment variables (e.g., PYTHONPATH) in a configuration file for downstream HiC-Pro normalization steps."
- [readme] Edit config-install.txt file and set paths; if not set, dependencies will be sought in PATH, or HiC-Pro will attempt to install them: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH. Note that if some of these dependencies are not installed (i.e. not detected in the"
- [readme] Python (>3.7) with pysam (>=0.15.4), bx-python (>=0.8.8), numpy (>=1.18.1), and scipy (>=1.4.1) are required: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
- [readme] Pysam is a lightweight wrapper of samtools C-API for reading and manipulating SAM/BAM files: "Pysam is a python module for reading and manipulating files in the SAM/BAM format. Pysam is a lightweight wrapper of the samtools_ C-API."
- [readme] iced implements the ICE normalization of hic data and depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19, sklearn, pandas: "The python module iced implements the ICE normalization of hic data. Depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19, sklearn, pandas"
