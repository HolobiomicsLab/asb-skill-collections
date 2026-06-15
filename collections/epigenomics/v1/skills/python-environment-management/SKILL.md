---
name: python-environment-management
description: Use when you are preparing to run Hi-C data normalization or read alignment filtering steps that depend on Python modules (iced, pysam, numpy, scipy) and you need to ensure consistent module versions across multiple runs or compute nodes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0080
  tools:
  - MultiQC 1.8
  - Python (>3.7)
  - iced
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - numpy
  - scipy
  - pysam
  - bx-python
  - Python
  - pip
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- Python (>3.7) libraries
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

# python-environment-management

## Summary

Establish and validate isolated Python environments with pinned dependency versions (numpy ≥1.18.1, scipy ≥1.4.1, pysam ≥0.15.4, bx-python ≥0.8.8) required for Hi-C data processing pipelines. This skill ensures reproducible execution of Python-dependent bioinformatics workflows by verifying interpreter version (>3.7), resolving transitive dependencies, and documenting environment configuration for downstream pipeline steps.

## When to use

You are preparing to run Hi-C data normalization or read alignment filtering steps that depend on Python modules (iced, pysam, numpy, scipy) and you need to ensure consistent module versions across multiple runs or compute nodes. Use this skill at the start of any HiC-Pro pipeline execution or when setting up a new computational environment for Hi-C analysis.

## When NOT to use

- If Hi-C data has already been normalized using a pre-configured HiC-Pro Docker/Singularity container or conda environment — environment setup is already handled.
- If you are only performing SAM/BAM read alignment filtering without downstream normalization — pysam alone may not require the full iced+numpy+scipy stack.
- If Python 2.x is the only available interpreter and cannot be upgraded — the pipeline requires Python >3.7.

## Inputs

- Target system shell environment (bash/sh)
- Python interpreter (>3.7) executable path
- Optional: existing config-install.txt or environment configuration file

## Outputs

- Validated Python environment with iced module installed
- Configuration file with PYTHONPATH and dependency paths documented
- Version verification report (Python version, iced version, numpy/scipy versions)

## How to apply

First, verify that Python >3.7 is available on the target system by checking the interpreter version. Then, install the iced module independently from https://github.com/hiclib/iced along with its required transitive dependencies (numpy ≥1.18.1, scipy ≥1.4.1) using pip or the module's setup.py. Validate installation by importing each module in a Python interpreter and checking version and API availability. Document the iced installation path and set PYTHONPATH environment variables to point to the installation directory in a configuration file that will be sourced before running HiC-Pro normalization steps. This ensures the ICE normalization algorithm can correctly locate and use the iced module during Hi-C contact matrix correction.

## Related tools

- **iced** (ICE normalization of Hi-C contact matrices; must be independently installed and imported into Python environment) — https://github.com/hiclib/iced
- **numpy** (Transitive dependency of iced; required version ≥1.18.1 for numerical array operations) — http://www.scipy.org/scipylib/download.html
- **scipy** (Transitive dependency of iced; required version ≥1.4.1 for scientific computing functions) — http://www.scipy.org/scipylib/download.html
- **pysam** (Python wrapper for SAM/BAM alignment file manipulation; required for read filtering and alignment processing (≥0.15.4)) — https://github.com/pysam-developers/pysam
- **bx-python** (Bioinformatics utility library for interval operations; required version ≥0.8.8)
- **Python** (Interpreter and runtime environment; must be version >3.7 (current version no longer supports Python 2))
- **pip** (Package installer for Python modules; used to install iced and dependencies)

## Examples

```
python3 -c "import iced; import numpy; import scipy; import pysam; print('iced:', iced.__version__, 'numpy:', numpy.__version__, 'scipy:', scipy.__version__, 'pysam:', pysam.__version__)"
```

## Evaluation signals

- Python interpreter invocation returns version string matching pattern '>3.7' (e.g., 'Python 3.9.x')
- Import iced in Python interpreter succeeds without ModuleNotFoundError; `import iced; print(iced.__version__)` returns valid version string
- Import numpy, scipy, pysam, bx_python all succeed; verify version strings match required minimums (numpy ≥1.18.1, scipy ≥1.4.1, pysam ≥0.15.4, bx-python ≥0.8.8)
- PYTHONPATH environment variable contains the path to installed iced module; verify with `echo $PYTHONPATH` or `python -c 'import sys; print(sys.path)'`
- Configuration file (config-install.txt or equivalent) contains documented paths to Python installation and PYTHONPATH settings; file is human-readable and sourced without errors

## Limitations

- Iced is no longer part of the HiC-Pro source code and must be independently installed; installation can fail if pip/setuptools are not properly configured or if C compilation tools are unavailable.
- Transitive dependencies (numpy, scipy) have their own system-level requirements (e.g., BLAS/LAPACK libraries) that may not be automatically resolved by pip on all systems, especially HPC clusters.
- PYTHONPATH configuration is environment-specific; if a new shell session or compute node is used without sourcing the configuration file, subsequent pipeline steps will fail to locate the iced module.
- Python 2.x is no longer supported; legacy environments or older HPC systems may still use Python 2 as the default, requiring explicit module loading or environment activation to access Python >3.7.

## Evidence

- [methods] Iced is no longer part of the HiC-Pro source code, and should be independently installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [methods] Python (>3.7) with pysam (>=0.15.4), bx-python(>=0.8.8), numpy(>=1.18.1), and scipy(>=1.4.1) libraries. Note that the current version no longer supports python 2: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries. Note that the current version no longer supports python 2"
- [other] 1. Verify Python (>3.7) is available and functional on the target system. 2. Clone or download the iced module from https://github.com/hiclib/iced. 3. Install iced and its transitive dependencies (numpy >=1.18.1, scipy >=1.4.1) using pip or the iced setup.py. 4. Validate the iced installation by importing the module and checking version/API availability in a Python interpreter. 5. Document the iced installation path and Python environment variables (e.g., PYTHONPATH) in a configuration file for downstream HiC-Pro normalization steps.: "Verify Python (>3.7) is available and functional on the target system. 2. Clone or download the iced module from https://github.com/hiclib/iced. 3. Install iced and its transitive dependencies (numpy"
- [readme] Pysam is a python module for reading and manipulating files in the SAM/BAM format: "Pysam is a python module for reading and manipulating files in the SAM/BAM format"
- [readme] Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options: "Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options"
- [readme] The python module iced implements the ICE normalization of hic data. Depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19, sklearn, pandas: "The python module iced implements the ICE normalization of hic data. Depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19"
