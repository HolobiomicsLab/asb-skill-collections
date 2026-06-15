---
name: configuration-file-generation-and-templating
description: Use when when deploying a complex bioinformatics pipeline (like HiC-Pro) across heterogeneous computing environments where required tools (bowtie2, samtools, R, Python) may be installed in non-standard locations, differ in version, or require scheduler-specific configuration (TORQUE, SGE, SLURM.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3790
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3169
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

# configuration-file-generation-and-templating

## Summary

Generate environment-specific configuration files by reading user-editable templates, detecting installed dependencies via system PATH queries, validating version requirements, and locking the final config to prevent accidental modification during pipeline execution. This skill ensures HiC-Pro and similar multi-tool pipelines can adapt to diverse cluster and installation environments without manual binary path management.

## When to use

When deploying a complex bioinformatics pipeline (like HiC-Pro) across heterogeneous computing environments where required tools (bowtie2, samtools, R, Python) may be installed in non-standard locations, differ in version, or require scheduler-specific configuration (TORQUE, SGE, SLURM, LSF). Use this skill during initial setup or reconfiguration when dependencies must be auto-detected or user-specified, and their paths must be reliably recorded for all downstream workflow steps.

## When NOT to use

- Pipeline is already configured and config-system.txt exists and is locked — re-running configuration generation may conflict with active job submissions.
- All required tools are provided pre-containerized (Docker, Singularity, conda environment) — configuration file generation is redundant if the container already bundles all binaries with fixed paths.
- User requires manual control over tool selection or version pinning per workflow step — this skill generates a single locked config that applies uniformly to all steps.

## Inputs

- config-install.txt template file with placeholder paths and cluster scheduler type
- system $PATH environment variable
- user-edited config-install.txt (optional; may contain explicit tool paths)

## Outputs

- config-system.txt locked configuration file with resolved paths for all dependencies
- installed bowtie2 and samtools binaries (if auto-installation was triggered)
- validated Python, R, and tool environment ready for pipeline execution

## How to apply

Read a user-editable config-install.txt template containing placeholder entries for tool paths (PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS). For each unset entry, invoke 'which' to search the system $PATH for bowtie2, samtools, R, and Python binaries. Validate that bowtie2 and samtools are present; if missing, trigger automatic installation (bowtie2 and samtools ≥1.9 support auto-install). Verify installed versions meet minimum thresholds: samtools ≥1.9, Python >3.7, R with required packages (RColorBrewer, ggplot2 >2.2.1). Compile all detected or user-specified paths and cluster scheduler type into a structured config-system.txt file. Lock the final config as read-only to prevent accidental user modification during pipeline execution. Execute the installation via 'make CONFIG_SYS=config-install.txt install' to finalize dependency integration.

## Related tools

- **bowtie2** (Sequence alignment tool; path is detected via which or auto-installed if missing; ≥2.2.2 recommended for allele-specific analysis) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools** (BAM/SAM manipulation tool; version ≥1.9 is required and validated during configuration; path is resolved and recorded in config-system.txt) — http://samtools.sourceforge.net/
- **R** (Statistical computing environment; path is detected and recorded; required packages (RColorBrewer, ggplot2 >2.2.1) are validated)
- **Python** (Scripting runtime; version >3.7 is required and validated; libraries (pysam ≥0.15.4, bx-python ≥0.8.8, numpy ≥1.18.1, scipy ≥1.4.1) are resolved)
- **iced** (ICE (iterative correction and eigenvalue decomposition) normalization module for Hi-C contact matrices; installed independently and path recorded) — https://github.com/hiclib/iced
- **pysam** (Python wrapper for samtools C-API; version ≥0.15.4 required; validates SAM/BAM file I/O capability) — https://github.com/pysam-developers/pysam

## Examples

```
tar -zxvf HiC-Pro-master.tar.gz && cd HiC-Pro-master && vim config-install.txt && make configure && make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- config-system.txt exists and contains all expected keys (PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS) with non-empty, absolute paths
- config-system.txt is read-only (file permissions enforce no accidental writes during pipeline execution)
- make install completes without errors; all detected tools can be invoked (bowtie2 --version, samtools --version, R --version, python --version) and versions match or exceed documented minimums
- Downstream HiC-Pro workflow steps successfully locate and execute bowtie2, samtools, and iced without 'command not found' errors
- If auto-installation was triggered, bowtie2 ≥2.2.2 and samtools ≥1.9 binaries are present in the PREFIX directory and accessible via config-system.txt paths

## Limitations

- If bowtie2 or samtools cannot be auto-installed (e.g., missing compiler, network access, or incompatible OS), manual user intervention is required; the script cannot override missing build dependencies.
- Configuration is environment-specific and locked; moving the installation to a different file system or cluster scheduler type requires manual re-configuration (editing config-install.txt and re-running make install).
- On macOS, GNU core utilities with -V sort option must be manually installed by the user; this is not auto-detected or auto-installed by the configuration script.
- Version validation is static (checked at install time); runtime errors may occur if a tool is later downgraded or removed without re-running configuration.
- Cluster scheduler detection (TORQUE, SGE, SLURM, LSF) relies on user specification in config-install.txt; automatic detection of the current cluster type is not performed.

## Evidence

- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] make CONFIG_SYS=config-install.txt install: "make CONFIG_SYS=config-install.txt install"
- [other] For each path entry not explicitly set by the user, query the system PATH using the 'which' command to locate bowtie2, samtools, R, and Python binaries.: "For each path entry not explicitly set by the user, query the system PATH using the 'which' command to locate bowtie2, samtools, R, and Python binaries."
- [other] Verify installed versions meet minimum requirements: samtools >=1.9 and Python >3.7.: "Verify installed versions meet minimum requirements: samtools >=1.9 and Python >3.7."
- [other] Lock the generated config-system.txt as read-only to prevent accidental user modification during pipeline execution.: "Lock the generated config-system.txt as read-only to prevent accidental user modification during pipeline execution."
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
- [readme] PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS | Scheduler to use for cluster submission. Must be TORQUE, SGE, SLURM or LSF: "CLUSTER_SYS | Scheduler to use for cluster submission. Must be TORQUE, SGE, SLURM or LSF"
