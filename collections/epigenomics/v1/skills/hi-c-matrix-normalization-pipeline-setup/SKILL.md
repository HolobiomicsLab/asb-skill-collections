---
name: hi-c-matrix-normalization-pipeline-setup
description: Use when before running HiC-Pro's normalization stage on aligned Hi-C BAM files. Specifically, when you have SAM/BAM-formatted aligned Hi-C reads that need bias correction and matrix balancing to produce normalized contact maps suitable for downstream chromatin structure analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0622
  tools:
  - MultiQC 1.8
  - iced
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - numpy
  - scipy
  - HiC-Pro
  - pysam
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

# hi-c-matrix-normalization-pipeline-setup

## Summary

Install and configure the iced Python module and its dependencies to enable iterative correction and eigenvalue decomposition (ICE) normalization of raw Hi-C contact matrices within the HiC-Pro pipeline. This skill ensures that the normalization stage can correct biases and balance contact frequency matrices after read alignment and filtering.

## When to use

Before running HiC-Pro's normalization stage on aligned Hi-C BAM files. Specifically, when you have SAM/BAM-formatted aligned Hi-C reads that need bias correction and matrix balancing to produce normalized contact maps suitable for downstream chromatin structure analysis. The iced module is a required dependency that no longer ships with HiC-Pro source code and must be independently installed.

## When NOT to use

- If you are using a pre-built HiC-Pro container (Docker, Singularity, or conda environment) that already includes iced; the dependency is already resolved.
- If your downstream analysis does not require contact matrix normalization or uses an alternative normalization method (e.g., external normalization tools or raw contact frequencies).
- If Python < 3.7 is your only available interpreter; iced requires Python >3.7 and will not function on Python 2.x.

## Inputs

- System Python (>3.7) installation
- iced module source code (from GitHub repository)
- System package manager or pip environment

## Outputs

- Installed iced Python module with accessible API
- Installed numpy (≥1.18.1) and scipy (≥1.4.1) dependencies
- Configuration file documenting PYTHONPATH and iced installation location

## How to apply

Verify that Python (>3.7) is available on your system. Clone or download the iced module from https://github.com/hiclib/iced and install it along with transitive dependencies (numpy ≥1.18.1, scipy ≥1.4.1) using pip or the iced setup.py installer. Test the installation by importing the module in a Python interpreter and confirming version/API availability. Document the iced installation path and set PYTHONPATH environment variables in a configuration file that will be sourced by downstream HiC-Pro normalization steps. This ensures that when HiC-Pro calls the iced normalization functions, the module is discoverable and its dependencies are met.

## Related tools

- **iced** (Core Python module that implements ICE iterative correction and eigenvalue decomposition algorithm for normalizing Hi-C contact matrices) — https://github.com/hiclib/iced
- **numpy** (Required numerical computing library for iced array operations (≥1.18.1))
- **scipy** (Required scientific computing library for iced linear algebra and optimization routines (≥1.4.1))
- **HiC-Pro** (Parent pipeline that uses iced module to normalize contact matrices in the normalization stage) — https://github.com/nservant/HiC-Pro
- **pysam** (Python wrapper for SAM/BAM manipulation; used by HiC-Pro to handle aligned Hi-C reads upstream of normalization) — https://github.com/pysam-developers/pysam

## Examples

```
python -m pip install numpy>=1.18.1 scipy>=1.4.1 && git clone https://github.com/hiclib/iced.git && cd iced && python setup.py install && python -c 'import iced; print("iced version:", iced.__version__)'
```

## Evaluation signals

- Successfully import iced module in Python interpreter without ImportError: `python -c 'import iced; print(iced.__version__)'`
- Verify transitive dependencies are installed: `python -c 'import numpy, scipy; print(numpy.__version__, scipy.__version__)'` returns versions ≥1.18.1 and ≥1.4.1 respectively
- Confirm PYTHONPATH environment variable is set and points to the correct iced installation directory; test with `echo $PYTHONPATH`
- Validate that HiC-Pro configuration file correctly references the iced installation path and that the normalization stage completes without 'module not found' errors
- Check that iced API functions are callable: `python -c 'from iced import normalization; print(dir(normalization))'` returns expected normalization function signatures

## Limitations

- iced module installation may require compilation of C extensions; this can fail on systems without a C compiler or if numpy development headers are missing.
- The iced module depends on sklearn and pandas (per the README) in addition to the documented numpy and scipy requirements; all four libraries must be available.
- Installation via pip may fail if pip, setuptools, or wheel are outdated; users may need to upgrade packaging tools first.
- On macOS systems, users should use GNU sort (via GNU coreutils) rather than the BSD sort, as HiC-Pro requires Unix sort with the -V option; this is a pipeline-level constraint but may affect overall environment setup.
- If PYTHONPATH is not correctly set or if multiple Python environments are active, the installed iced module may not be discoverable by HiC-Pro at runtime.

## Evidence

- [other] The iced module is a required dependency for HiC-Pro's normalization pipeline and must be independently installed from the HiC-Pro source code.: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [other] Verification and documentation of iced installation in Python environment.: "Validate the iced installation by importing the module and checking version/API availability in a Python interpreter"
- [other] iced module requires specific minimum versions of numpy and scipy.: "Install iced and its transitive dependencies (numpy >=1.18.1, scipy >=1.4.1) using pip or the iced setup.py"
- [readme] iced implements the ICE normalization algorithm for Hi-C contact matrices.: "The python module iced implements the ICE normalization of hic data"
- [readme] HiC-Pro includes a fast implementation of the iterative correction method via iced.: "HiC-Pro includes a fast implementatation of the iterative correction method (see the [iced python package](https://github.com/hiclib/iced) for more information)"
- [readme] Python version requirement for iced and HiC-Pro dependencies.: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries"
