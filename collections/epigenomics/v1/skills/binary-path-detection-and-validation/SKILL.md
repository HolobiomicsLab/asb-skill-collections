---
name: binary-path-detection-and-validation
description: Use when when setting up a bioinformatics pipeline (particularly Hi-C data processing) that depends on multiple external binaries with version constraints, and you need to configure the environment in a way that is both portable across systems and reproducible across runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0084
  tools:
  - MultiQC 1.8
  - bowtie2
  - samtools (>=1.9)
  - R
  - samtools
  - Python
  - iced
  - pysam
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- R (http://www.r-project.org/) with the following packages
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

# binary-path-detection-and-validation

## Summary

A configuration-driven mechanism for detecting and validating required binary tool installations (bowtie2, samtools, R, Python) by querying the system PATH and version constraints, then generating an environment-specific locked configuration file. This skill ensures reproducibility by recording exact tool locations and validating minimum version requirements before pipeline execution.

## When to use

When setting up a bioinformatics pipeline (particularly Hi-C data processing) that depends on multiple external binaries with version constraints, and you need to configure the environment in a way that is both portable across systems and reproducible across runs. Specifically: (1) users provide a configuration template with optional explicit paths, (2) missing paths must be auto-detected from $PATH, (3) detected tools must meet minimum version thresholds (e.g., samtools ≥1.9, Python >3.7), and (4) the final configuration must be locked to prevent accidental runtime modification.

## When NOT to use

- When all tool paths are already hardcoded in pipeline scripts or environment modules—this skill is unnecessary if binaries are already resolved.
- If the pipeline does not have version constraints or does not require specific binaries—the overhead of path detection and validation adds complexity without benefit.
- When deploying via containerized images (Docker, Singularity) where dependencies are pre-installed and environment is fixed—detection is redundant in a sealed container.

## Inputs

- config-install.txt template file (plaintext with placeholder entries for tool paths and cluster scheduler)
- System environment variables ($PATH)
- User-specified tool paths (optional, in config-install.txt)

## Outputs

- config-system.txt (read-only locked configuration file with resolved paths for all dependencies)
- Installed or verified binary tools (bowtie2, samtools, R, Python) at specified locations
- Installation logs and version validation records

## How to apply

First, users edit a config-install.txt template to optionally specify explicit paths for PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, and CLUSTER_SYS; any unset entries trigger automated detection. For each undetected tool, query the system PATH using the 'which' command to locate the binary; if not found, attempt automatic installation (bowtie2 and samtools ≥1.9 are auto-installable). Once located (whether user-specified or auto-detected), validate that the installed version meets minimum requirements—samtools ≥1.9 and Python >3.7 are mandatory. Compile all validated paths and system parameters into a structured config-system.txt file with locked read-only permissions to prevent user modification during pipeline execution. Run 'make configure' followed by 'make CONFIG_SYS=config-install.txt install' to execute the full setup workflow.

## Related tools

- **bowtie2** (Short-read DNA sequence aligner; auto-installed if not detected during binary-path validation) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools** (SAM/BAM file manipulation and coordinate sorting; version ≥1.9 required and auto-installable if missing)
- **Python** (Runtime for iced ICE normalization module and Hi-C data processing scripts; version >3.7 required)
- **R** (Statistical computing environment for ggplot2 and RColorBrewer visualization packages) — http://www.r-project.org/
- **iced** (Python module implementing iterative correction and eigenvector decomposition (ICE) normalization of Hi-C contact matrices; must be independently installed) — https://github.com/hiclib/iced
- **pysam** (Python wrapper for samtools C-API to read and manipulate SAM/BAM alignments; version ≥0.15.4 required) — https://github.com/pysam-developers/pysam

## Examples

```
tar -zxvf HiC-Pro-master.tar.gz && cd HiC-Pro-master && make configure && make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- config-system.txt file exists, is readable, and contains non-empty valid paths for all mandatory dependencies (BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH)
- Version validation passes for all detected binaries: samtools --version reports ≥1.9; python --version reports >3.7
- config-system.txt has read-only permissions (mode 444 or equivalent) to prevent accidental user modification
- No 'tool not found' or 'version mismatch' errors appear in installation logs when running 'make install'
- Subsequent pipeline invocations use the locked config-system.txt without re-detecting or re-validating paths, ensuring reproducibility

## Limitations

- Automatic installation is limited to bowtie2 and samtools ≥1.9; other dependencies (R, Python, iced) must be pre-installed or manually specified in config-install.txt
- The 'which' command used for PATH queries may behave differently across Unix shells and OS distributions, potentially causing false negatives on non-standard systems
- Version detection relies on tool-specific version flag semantics (e.g., 'samtools --version', 'python --version'); tools with non-standard version output may fail validation
- Once config-system.txt is locked as read-only, correcting a path error requires manual unlock or reinstall—no in-place recovery mechanism is documented
- The skill does not validate that detected tools are functional beyond version checking (e.g., corrupt binaries, missing shared libraries, or insufficient file permissions are not caught)

## Evidence

- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] make CONFIG_SYS=config-install.txt install: "make CONFIG_SYS=config-install.txt install"
- [readme] Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries"
- [readme] samtools (>1.9). Unix sort (**which support -V option**) is required!: "samtools (>1.9). Unix sort (**which support -V option**) is required!"
