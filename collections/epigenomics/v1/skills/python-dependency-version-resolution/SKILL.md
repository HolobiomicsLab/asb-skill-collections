---
name: python-dependency-version-resolution
description: Use when when setting up a new conda environment for a Python-based bioinformatics pipeline and you need to confirm that all declared dependencies (e.g., pysam >=0.15.4, bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3919
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - MultiQC 1.8
  - Python (>3.7)
  - R
  - bowtie2
  - samtools (>=1.9)
  - bx-python (>=0.8.8)
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - pysam (>=0.15.4)
  - ggplot2 (>2.2.1)
  - RColorBrewer
  - iced
  - conda
  - pysam
  - bx-python
  - numpy
  - scipy
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- Python (>3.7) libraries
- R (http://www.r-project.org/) with the following packages
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- bx-python (>=0.8.8) - https://pypi.python.org/pypi/bx-python
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

# Python Dependency Version Resolution

## Summary

Resolve and verify Python library versions (pysam, bx-python, numpy, scipy) and their inter-dependencies within a conda environment to ensure compatibility with a bioinformatics pipeline's requirements. This skill is critical when constructing reproducible computational environments for tools like HiC-Pro that depend on specific minimum versions of scientific Python packages.

## When to use

When setting up a new conda environment for a Python-based bioinformatics pipeline and you need to confirm that all declared dependencies (e.g., pysam >=0.15.4, bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1) are both installed and meet the minimum version thresholds, or when troubleshooting import failures or version-mismatch errors during pipeline initialization.

## When NOT to use

- When working with a pre-built container (Docker, Singularity) where the environment is already sealed and dependencies are guaranteed; verification becomes redundant unless the container is known to be damaged or incompletely built.
- When the pipeline has already been run successfully in the current environment and you have no reason to suspect version drift or breakage.
- When dependency resolution is handled by a higher-level workflow orchestration system (e.g., Snakemake, CWL) that manages environment isolation automatically.

## Inputs

- conda environment specification file (environment.yml)
- activated conda environment (from `conda activate`)
- Python interpreter (>3.7) within that environment

## Outputs

- verified list of installed Python packages and their versions
- test report confirming all imports succeed
- summary document recording resolved paths and versions

## How to apply

After activating a conda environment created from an environment.yml file, test the importability and version of each Python library by executing import statements and version checks in an interactive Python session or test script. For HiC-Pro specifically, verify that Python is >3.7, then check that pysam (>=0.15.4), bx-python (>=0.8.8), numpy (>=1.18.1), and scipy (>=1.4.1) all import successfully and report versions meeting or exceeding the documented thresholds. If any import fails or a version is below the minimum, reinstall or upgrade that package via conda (preferred, as it resolves non-Python C/Fortran dependencies) or pip, then re-verify. Document the final resolved versions and paths in a summary report for reproducibility and troubleshooting.

## Related tools

- **conda** (environment manager that installs and tracks Python package versions and their non-Python dependencies (e.g., C libraries required by pysam, numpy, scipy)) — https://docs.conda.io/en/latest/miniconda.html
- **pysam** (Python wrapper for samtools C-API; version >=0.15.4 required to ensure compatibility with HiC-Pro's BAM file handling) — https://github.com/pysam-developers/pysam
- **bx-python** (Python library for sequence analysis; version >=0.8.8 required by HiC-Pro for genomic interval operations)
- **numpy** (numerical computing library; version >=1.18.1 required for array operations used by scipy and bx-python)
- **scipy** (scientific computing library; version >=1.4.1 required for statistical and signal-processing functions used by HiC-Pro data normalization)

## Examples

```
python -c "import sys; assert sys.version_info >= (3, 7); import pysam; assert tuple(map(int, pysam.__version__.split('.')[:2])) >= (0, 15); import bx; import numpy as np; assert tuple(map(int, np.__version__.split('.')[:2])) >= (1, 18); import scipy; assert tuple(map(int, scipy.__version__.split('.')[:2])) >= (1, 4); print('All dependencies verified')"
```

## Evaluation signals

- All Python imports (pysam, bx-python, numpy, scipy) succeed without ImportError or ModuleNotFoundError.
- Reported version of each package is >= its documented minimum version threshold (e.g., `pysam.__version__ >= '0.15.4'`).
- Python version check confirms interpreter is >3.7 (e.g., `sys.version_info >= (3, 8)`).
- Downstream pipeline steps (e.g., HiC-Pro data processing) execute without version-related warnings, deprecation errors, or runtime failures tied to library compatibility.
- Summary report documents all resolved package paths (from `pip show` or conda metadata) and versions, enabling reproduction and future troubleshooting.

## Limitations

- Conda's dependency solver may encounter conflicts or slow resolution times with complex multi-language environments (e.g., when both Python and R packages with overlapping C/Fortran dependencies are required); in such cases, pre-built containers (Docker, Singularity) are often more reliable.
- Version thresholds documented in the article (e.g., pysam >=0.15.4) reflect the publication date (2015) and may become outdated as dependencies evolve; newer versions of pysam (now wrapping htslib-1.23.1 and samtools-1.23.1 per the README) may introduce breaking API changes not tested in the original HiC-Pro validation.
- The iced module is no longer part of HiC-Pro source code and must be independently installed; this breaks the single-environment isolation and introduces an additional failure point if the iced GitHub repository becomes unavailable or incompatible with newer Python/numpy versions.
- Platform-specific issues (e.g., macOS requiring GNU core utilities for UNIX sort compatibility, or Windows lacking native UNIX tools) may prevent successful package installation or execution even after version resolution.

## Evidence

- [other] Verify that Python version is >3.7 and that all required Python libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4, argparse) are installed and importable.: "Verify that Python version is >3.7 and that all required Python libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4, argparse) are installed and importable."
- [readme] Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries. **Note that the current version no longer supports python 2**: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
- [readme] Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options.: "Installation through bioconda is the recommended way to install pysam as it resolves non-python dependencies and uses pre-configured compilation options."
- [readme] The current version of pysam wraps 3rd-party code from htslib-1.23.1, samtools-1.23.1, and bcftools-1.23.1.: "The current version of pysam wraps 3rd-party code from htslib-1.23.1, samtools-1.23.1, and bcftools-1.23.1."
- [other] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
