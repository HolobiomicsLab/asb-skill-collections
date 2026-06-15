---
name: dependency-installation-and-verification
description: Use when when setting up HiC-Pro or similar multi-tool pipelines where tool availability and version constraints are prerequisites for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3168
  tools:
  - MultiQC 1.8
  - samtools (>=1.9)
  - bowtie2
  - samtools
  - Python
  - R
  - pysam
  - iced
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

# dependency-installation-and-verification

## Summary

Automatically detect, configure, and validate critical bioinformatics tool dependencies (samtools, bowtie2, Python libraries) before executing a multi-stage Hi-C processing pipeline. This skill ensures reproducibility by recording resolved tool paths and versions in a system configuration file.

## When to use

When setting up HiC-Pro or similar multi-tool pipelines where tool availability and version constraints are prerequisites for downstream analysis. Use this skill at pipeline initialization time, before any data processing steps (alignment, SAM post-processing, normalization) begin, to avoid runtime failures due to missing or incompatible dependencies.

## When NOT to use

- When all dependencies are already manually installed and their paths are hardcoded in an existing config-system.txt file — skip this skill and proceed directly to pipeline execution.
- When running HiC-Pro via a pre-built container (Docker, Singularity, conda environment) — dependency management is handled by the container image itself.
- When working with a subset of the pipeline that does not require the full dependency chain (e.g., post-hoc normalization scripts that only need R and iced, not bowtie2).

## Inputs

- config-install.txt configuration template file
- system PATH environment variable
- installed tool binaries (samtools, bowtie2, Python interpreter)

## Outputs

- config-system.txt — resolved system configuration file with validated tool paths and versions
- installation log or status report indicating which dependencies were auto-installed vs. detected

## How to apply

Edit the config-install.txt file to specify full paths to required tools (samtools >=1.9, bowtie2, Python >3.7 with pysam, bx-python, numpy, scipy) or leave paths unset to trigger automatic detection via system PATH using the 'which' command. Execute 'make CONFIG_SYS=config-install.txt install' to invoke the dependency checking and configuration workflow. This command validates tool availability, resolves version requirements, and generates a config-system.txt file containing the confirmed paths and versions of all detected tools. Verify the generated config-system.txt records all required tools with appropriate versions (samtools >=1.9), confirming readiness for downstream SAM/BAM post-processing and Hi-C data normalization operations.

## Related tools

- **samtools** (validates and post-processes SAM/BAM alignment files in HiC-Pro; must be version >=1.9)
- **bowtie2** (performs paired-end read alignment against reference genome in the first stage of HiC-Pro; version >2.2.2 strongly recommended for allele-specific analysis) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **Python** (runtime for pysam (>=0.15.4), bx-python (>=0.8.8), numpy (>=1.18.1), scipy (>=1.4.1) — required for read processing and normalization; must be >3.7) — http://www.python.org/
- **R** (runtime for ggplot2 (>2.2.1) and RColorBrewer packages used in visualization and quality reporting) — http://www.r-project.org/
- **pysam** (Python wrapper for samtools C-API; provides programmatic SAM/BAM file reading and manipulation) — https://github.com/pysam-developers/pysam
- **iced** (Python module implementing ICE (iterative correction) normalization of Hi-C contact maps; must be independently installed as it is no longer bundled with HiC-Pro) — https://github.com/hiclib/iced

## Examples

```
make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- config-system.txt file is generated and contains non-empty paths for samtools, bowtie2, Python, and R
- samtools version string in config-system.txt is >=1.9 (e.g., 'samtools-1.23.1')
- bowtie2 binary is detected and recorded; version >2.2.2 is preferred for allele-specific workflows
- Python version is >3.7 and includes pysam (>=0.15.4), bx-python (>=0.8.8), numpy (>=1.18.1), scipy (>=1.4.1) — can be verified by importing each module
- 'make install' completes without fatal errors related to missing dependencies; any auto-installed tools are logged and match version constraints

## Limitations

- Automatic installation of missing dependencies (bowtie2, samtools) may fail if the system lacks a package manager (e.g., apt, yum, conda) or has insufficient permissions; manual path specification in config-install.txt is a workaround.
- The 'which' command for PATH-based detection is not portable to Windows environments without GNU coreutils; Windows users must explicitly specify paths in config-install.txt.
- Unix sort with the -V (version-sort) option is required but not checked explicitly during installation; this may cause silent failures on macOS unless GNU coreutils are installed.
- The skill validates tool availability at configuration time but does not test actual functionality (e.g., samtools can be called but may fail on real BAM files due to library issues); integration testing with sample Hi-C data is needed to confirm end-to-end readiness.

## Evidence

- [other] HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system.: "HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system."
- [other] Edit the config-install.txt file to specify the full path to the samtools binary (>=1.9), or leave unset to allow automatic detection via the system PATH using the 'which' command.: "Edit the config-install.txt file to specify the full path to the samtools binary (>=1.9), or leave unset to allow automatic detection via the system PATH using the 'which' command."
- [other] Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved tool paths.: "Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [readme] Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries.: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [readme] Edit config-install.txt file if necessary... make configure... make install: "Edit config-install.txt file if necessary... make configure... make install"
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
