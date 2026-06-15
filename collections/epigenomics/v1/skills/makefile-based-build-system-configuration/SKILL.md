---
name: makefile-based-build-system-configuration
description: Use when when deploying a complex bioinformatics pipeline (e.g., HiC-Pro) that depends on multiple external tools with version constraints (samtools ≥1.9, bowtie2, R packages, Python libraries) and you need to verify their availability and configure their paths before running the analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3192
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
  tools:
  - MultiQC 1.8
  - samtools (>=1.9)
  - bowtie2
  - samtools
  - Python
  - R
  - GNU g++ compiler
  - GNU sort (with -V option)
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- samtools (>=1.9) can be automatically installed if not detected
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
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

# Makefile-based build system configuration

## Summary

Configure a pipeline's build system by editing a configuration file and running make install to detect, validate, and resolve dependencies (samtools, bowtie2, Python libraries) across heterogeneous systems. This skill ensures all required tools and their versions are correctly installed and recorded before executing the main workflow.

## When to use

When deploying a complex bioinformatics pipeline (e.g., HiC-Pro) that depends on multiple external tools with version constraints (samtools ≥1.9, bowtie2, R packages, Python libraries) and you need to verify their availability and configure their paths before running the analysis. Apply this skill before attempting to run any downstream analysis stages.

## When NOT to use

- Input tools are already packaged in a containerized environment (Docker, Singularity) where versions are pre-configured—use the container directly instead.
- The pipeline has been pre-compiled or pre-installed on a shared cluster with a module system (e.g., 'module load hicpro'); configuration is already applied.
- You are running a lightweight analysis that does not depend on multiple versioned external tools with complex interdependencies.

## Inputs

- config-install.txt (text configuration file with tool path variables)
- System environment variables ($PATH, $PYTHONPATH, $R_LIBS)
- Tool binaries or source distributions available on the system

## Outputs

- config-system.txt (generated configuration file with resolved tool paths and versions)
- Verified installation status of samtools (≥1.9), bowtie2, Python (>3.7) with libraries (pysam, bx-python, numpy, scipy), R (with ggplot2, RColorBrewer packages)

## How to apply

Edit the config-install.txt file to specify the full path to each required tool binary (samtools, bowtie2, R, Python) or leave fields unset to allow automatic detection via the system PATH using the 'which' command. Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration validation, which tests version constraints (e.g., samtools ≥1.9), attempts automatic installation of missing tools if permitted, and generates a config-system.txt file recording all resolved tool paths. Verify the generated config-system.txt contains entries for all critical tools (samtools, bowtie2, Python interpreter, and required libraries) and confirms version requirements are satisfied before proceeding to the analysis workflow.

## Related tools

- **samtools** (SAM/BAM file post-processing and format validation; version constraint ≥1.9 enforced during configuration)
- **bowtie2** (Read alignment mapper; must be detected or installed during configuration; version >2.2.2 strongly recommended for allele-specific analysis) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **Python** (Interpreter and dependency management (pysam ≥0.15.4, bx-python ≥0.8.8, numpy ≥1.18.1, scipy ≥1.4.1); version >3.7 required) — https://www.python.org/
- **R** (Statistical computing and visualization; ggplot2 (>2.2.1) and RColorBrewer packages required for plotting) — http://www.r-project.org/
- **GNU g++ compiler** (C++ compilation support required for pipeline components)
- **GNU sort (with -V option)** (Version-aware sorting of chromosome/genomic intervals; POSIX sort inadequate; required on macOS via coreutils)

## Examples

```
make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- The generated config-system.txt file exists and contains non-empty PATH entries for samtools, bowtie2, Python, and R executables.
- The samtools version in config-system.txt meets the constraint ≥1.9 (verify by `samtools --version` on the recorded path).
- Python ≥3.7 is recorded and all required libraries (pysam, bx-python, numpy, scipy) are importable from the configured PYTHON_PATH.
- R is present in config-system.txt and the packages ggplot2 and RColorBrewer are installed and loadable in that R environment.
- No 'ERROR' or 'NOT FOUND' messages appear in the make install output; all dependency checks pass without manual intervention.

## Limitations

- The Makefile-based configuration assumes Unix/Linux environment and does not support Windows natively; PATH resolution via 'which' command is Unix-specific.
- Automatic tool installation (if not detected) depends on network access and build tools availability; may fail silently on restricted systems or without compiler toolchain.
- The configuration is static once generated; if system tools are updated or moved after config-system.txt is created, the recorded paths become stale and must be reconfigured.
- No changelog is provided with HiC-Pro, so version compatibility between the pipeline and detected tool versions is not automatically validated beyond hard constraints (e.g., samtools ≥1.9).
- Mac OS users must install GNU coreutils to satisfy the Unix sort requirement with -V option; system sort is insufficient.

## Evidence

- [other] Edit the config-install.txt file to specify the full path to the samtools binary (>=1.9), or leave unset to allow automatic detection via the system PATH using the 'which' command.: "Edit the config-install.txt file to specify the full path to the samtools binary (>=1.9), or leave unset to allow automatic detection via the system PATH using the 'which' command."
- [other] Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved tool paths.: "Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved"
- [readme] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [readme] Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries.: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
- [readme] Unix sort (**which support -V option**) is required ! For Mac OS user, please install the GNU core utilities !: "Unix sort (**which support -V option**) is required ! For Mac OS user, please install the GNU core utilities !"
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
