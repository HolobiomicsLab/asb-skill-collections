---
name: shell-environment-variable-resolution
description: Use when use this skill during pipeline installation or initialization when you need to locate required external binaries (e.g., bowtie2, samtools, R, Python) but the user has not explicitly provided their installation paths in a configuration file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MultiQC 1.8
  - bowtie2
  - samtools (>=1.9)
  - R
  - samtools
  - Python
  - pysam
  - iced
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

# shell-environment-variable-resolution

## Summary

Automatically detect and resolve binary tool paths by querying the system $PATH environment variable when explicit paths are not provided in a configuration file. This skill enables pipeline setup to gracefully fall back to system-wide tool discovery, reducing manual configuration burden while maintaining the option for explicit path overrides.

## When to use

Use this skill during pipeline installation or initialization when you need to locate required external binaries (e.g., bowtie2, samtools, R, Python) but the user has not explicitly provided their installation paths in a configuration file. Apply it when you want to support both automated and manual tool discovery, allowing users to either edit a config file with explicit paths or rely on standard system PATH lookups.

## When NOT to use

- User has explicitly specified all tool paths in the configuration file and you are certain they are correct—direct use of the provided paths is more efficient than redundant PATH searching.
- The target environment does not use standard Unix $PATH conventions (e.g., embedded systems, containers with atypical path layouts) where 'which' will not work reliably.
- Pipeline execution has already begun and configuration is locked—re-resolving paths after initialization may corrupt running jobs or introduce inconsistency.

## Inputs

- Configuration template file with placeholder entries (e.g., config-install.txt with PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS)
- System environment variables, particularly $PATH
- Shell environment context (access to 'which' command)

## Outputs

- Environment-specific configuration file with resolved tool paths (e.g., config-system.txt)
- Read-only locked configuration file
- Binary discovery log or report (implicit)

## How to apply

First, read the user-provided configuration file (e.g., config-install.txt) and identify which tool paths have been left unset or blank. For each unset path entry, use the shell 'which' command to search the system $PATH for the corresponding binary (e.g., 'which bowtie2', 'which samtools'). If a tool is not found in $PATH, flag it for automatic installation if supported (bowtie2 and samtools ≥1.9 can be auto-installed). After discovery or installation, validate that found/installed versions meet minimum requirements (e.g., samtools ≥1.9, Python >3.7). Compile all resolved paths—whether user-specified or auto-discovered—into a new, environment-specific configuration file (e.g., config-system.txt) with structured entries for each dependency. Finally, lock the generated configuration file as read-only to prevent accidental modification during pipeline execution.

## Related tools

- **bowtie2** (Read aligner whose installation path must be resolved during HiC-Pro setup; auto-installable if not detected in $PATH) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools** (BAM/SAM file manipulation tool (≥1.9 required); version validation and auto-installation performed after PATH resolution)
- **R** (Statistical environment for visualization and analysis; installation path resolved from $PATH or user config) — http://www.r-project.org/
- **Python** (Scripting environment (>3.7 required); path resolved to confirm presence of required libraries (pysam, bx-python, numpy, scipy))
- **pysam** (Python module for SAM/BAM manipulation; version ≥0.15.4 required; validated after Python path resolution) — https://github.com/pysam-developers/pysam
- **iced** (Python module implementing ICE normalization; independently installed after discovery of Python path) — https://github.com/hiclib/iced

## Examples

```
make configure && make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- Verify that config-system.txt file is created with all tool paths populated (no empty placeholder entries remaining)
- Confirm that all resolved paths point to valid, executable binaries by running a test command with each tool (e.g., 'bowtie2 --version', 'samtools --version')
- Validate that version checks pass: samtools ≥1.9, Python >3.7, R with required packages (RColorBrewer, ggplot2 >2.2.1) present
- Ensure config-system.txt is set to read-only permissions to prevent accidental modification during pipeline execution
- Check that auto-installation was triggered only for tools not found in $PATH and that installation logs confirm successful completion

## Limitations

- The 'which' command relies on standard Unix $PATH conventions; will fail or be unreliable on non-Unix systems or in environments with unusual path structures (Windows CMD, embedded systems).
- Auto-installation of bowtie2 and samtools may fail in offline or restricted network environments, or if build dependencies (g++ compiler) are not available.
- Version validation requires tools to support standard version-reporting flags (--version); some packaged or legacy versions may not respond as expected.
- Iced module is no longer part of HiC-Pro source code and must be independently installed; PATH resolution does not guarantee it will be found—explicit installation step is required.

## Evidence

- [methods] If not set, the dependencies will be sought in the $PATH: "If not set, the dependencies will be sought in the $PATH"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [methods] make CONFIG_SYS=config-install.txt install: "make CONFIG_SYS=config-install.txt install"
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
- [readme] You can also edit the *config-install.txt* file and manually defined the paths to dependencies.: "You can also edit the *config-install.txt* file and manually defined the paths to dependencies."
