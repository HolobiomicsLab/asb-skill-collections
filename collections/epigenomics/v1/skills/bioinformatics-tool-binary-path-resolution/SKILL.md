---
name: bioinformatics-tool-binary-path-resolution
description: Use when when setting up a bioinformatics pipeline (such as HiC-Pro) that depends on multiple compiled or independently distributed binaries and you need to confirm that all required tools are installed, executable, meet version requirements (e.g., samtools ≥1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0091
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

# bioinformatics-tool-binary-path-resolution

## Summary

Resolve and verify the installation paths and executable availability of external bioinformatics tool binaries (e.g., bowtie2, samtools, iced) within a conda environment or system PATH, ensuring correct versions and runtime accessibility for a pipeline to function correctly.

## When to use

When setting up a bioinformatics pipeline (such as HiC-Pro) that depends on multiple compiled or independently distributed binaries and you need to confirm that all required tools are installed, executable, meet version requirements (e.g., samtools ≥1.9), and can be located at runtime by the pipeline's configuration and execution steps.

## When NOT to use

- The pipeline is already containerized (Docker/Singularity) and you are running it within that container — binary paths are pre-resolved by the container build.
- All required binaries are already manually installed in standard system locations (e.g., /usr/bin) and the pipeline successfully auto-detects them without configuration.
- You are using a pre-built conda lock file or manifest that guarantees binary availability — manual path resolution is not needed.

## Inputs

- environment.yml or equivalent dependency specification file
- config-install.txt configuration file with tool path placeholders
- Pipeline source code directory

## Outputs

- Activated conda environment with all dependencies installed
- Summary report documenting resolved tool paths, versions, and executability status
- config-system.txt or analogous generated configuration file with concrete tool paths

## How to apply

Create a Conda environment from the pipeline's environment.yml specification file (e.g., using `conda env create -f environment.yml -p /installation/path`), then activate it and systematically verify each external tool: (1) check that the binary is in PATH and executable (e.g., `which bowtie2`); (2) confirm version constraints (e.g., `samtools --version` to verify ≥1.9); (3) for tools not included in the environment specification (such as iced, which is no longer part of HiC-Pro source), independently install from the upstream repository and verify importability in Python; (4) document all resolved paths, versions, and import status in a summary report. Use the pipeline's config-install.txt file to manually specify paths if automatic detection fails, and rely on the pipeline's built-in fallback mechanisms (which attempt automatic installation of bowtie2 and samtools if not detected in $PATH).

## Related tools

- **conda** (Environment and dependency manager used to create isolated environments and resolve Python and compiled tool dependencies from specification files) — https://docs.conda.io/
- **bowtie2** (Read aligner whose binary path must be resolved and made executable within the environment; HiC-Pro can auto-install if not detected) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools (>=1.9)** (BAM/SAM file manipulator whose version must be verified to meet ≥1.9 requirement; HiC-Pro attempts automatic installation if not in PATH) — http://samtools.sourceforge.net/
- **iced** (Python module for ICE normalization of Hi-C data; must be independently installed from upstream repository since it is no longer bundled with HiC-Pro) — https://github.com/hiclib/iced
- **pysam (>=0.15.4)** (Python wrapper for samtools C-API; verified as importable within the activated environment) — https://github.com/pysam-developers/pysam
- **Python (>3.7)** (Interpreter for Python libraries; version constraint must be verified via `python --version`)
- **R** (Runtime for R packages (ggplot2, RColorBrewer); availability and package importability verified via library() calls) — http://www.r-project.org/

## Examples

```
conda env create -f HiC-Pro/environment.yml -p /opt/hicpro-env && conda activate /opt/hicpro-env && which bowtie2 && samtools --version && python -c 'import pysam; print(pysam.__version__)' && python -c 'import iced' && echo 'All binaries and libraries resolved successfully'
```

## Evaluation signals

- All binaries referenced in the pipeline (bowtie2, samtools, iced) are located in PATH or resolved via config file and respond to `which` or equivalent lookup without error.
- Version constraints are satisfied: `samtools --version` returns ≥1.9; `python --version` returns >3.7; R packages (ggplot2 >2.2.1, RColorBrewer) import successfully via `library()` calls.
- Python libraries (pysam ≥0.15.4, bx-python ≥0.8.8, numpy ≥1.18.1, scipy ≥1.4.1) are importable in the activated environment with `python -c 'import <module>; print(<module>.__version__)'`.
- The iced module (independently installed from https://github.com/hiclib/iced) is importable in Python: `python -c 'import iced'` succeeds without error.
- A summary report file (e.g., tool_resolution_report.txt) documents the resolved path, executable status, and version for each tool, permitting downstream pipeline steps to reference them without further discovery.

## Limitations

- The iced module is no longer part of HiC-Pro source code and must be independently installed, requiring manual verification that it is importable and compatible with the installed Python version (iced depends on numpy ≥1.16, scipy ≥0.19, sklearn, pandas).
- Automatic binary installation (bowtie2, samtools) by HiC-Pro's make system relies on network access and write permissions in the installation directory; failures in automatic download/compilation require manual intervention and path configuration in config-install.txt.
- macOS users must install GNU core utilities (specifically GNU sort with -V flag support) separately, as BSD sort does not support the version-sort flag required by HiC-Pro; this constraint is outside conda's automated dependency resolution.
- Path resolution depends on consistent chromosome naming between bowtie2 indexes and annotation BED files; mismatches will not be caught by binary path verification alone and will cause silent or cryptic downstream failures.
- Conda channel priority and configuration (e.g., bioconda and conda-forge channels) can affect which version of a tool is installed; strict channel priority settings are recommended but not enforced by this skill.

## Evidence

- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independently installed.: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH.: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [readme] In order to build your conda environment, first install miniconda and use: `conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV`: "conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV"
- [readme] The python module iced implements the ICE normalization of hic data. Depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19, sklearn, pandas: "The python module iced implements the ICE normalization of hic data. Depends on python >= 2.7, numpy >= 1.16, scipy >= 0.19, sklearn, pandas"
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
- [readme] Python (>3.7) with pysam (>=0.15.4), bx-python(>=0.8.8), numpy(>=1.18.1), and scipy(>=1.4.1) libraries.: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
