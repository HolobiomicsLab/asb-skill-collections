---
name: system-path-configuration-and-environment-setup
description: Use when you are setting up HiC-Pro or a similar multi-tool pipeline for the first time, or you need to validate that all required dependencies are installed and discoverable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3673
  tools:
  - MultiQC 1.8
  - samtools (>=1.9)
  - bowtie2
  - samtools
  - R
  - Python
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

# system-path-configuration-and-environment-setup

## Summary

Configures tool dependencies and environment paths for a bioinformatics pipeline by editing configuration files and running automated dependency detection. This skill ensures that required tools (e.g., samtools, bowtie2) are correctly located and validated before pipeline execution.

## When to use

You are setting up HiC-Pro or a similar multi-tool pipeline for the first time, or you need to validate that all required dependencies are installed and discoverable. Use this skill when the pipeline's installation documentation directs you to configure tool paths and verify dependency availability before running data processing workflows.

## When NOT to use

- Your pipeline dependencies are already installed and working correctly, and you do not need to reconfigure or validate paths.
- You are running the pipeline via Docker or Singularity container, where dependencies are pre-configured and PATH setup is handled by the container environment.
- You are executing a single module or step that does not depend on the full dependency chain (e.g., a standalone R or Python script with self-contained imports).

## Inputs

- config-install.txt (configuration template file with optional tool path entries)
- System PATH environment variable (for automatic tool discovery)
- Makefile and associated build system files

## Outputs

- config-system.txt (resolved configuration file with validated tool paths)
- Tool installation logs (if automatic installation was triggered)
- Confirmed availability of samtools (>=1.9), bowtie2, R, Python (>3.7), and other pipeline dependencies

## How to apply

Edit the config-install.txt file to specify the full path to each required tool binary (e.g., samtools >=1.9, bowtie2), or leave entries unset to allow automatic detection via the system PATH using the 'which' command. Then execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration. The build system will validate tool availability, attempt to install missing dependencies if needed, and generate a resolved config-system.txt file containing all tool paths. Verify that all required tools are detected and recorded in the generated config-system.txt file before proceeding to pipeline execution.

## Related tools

- **samtools** (Post-processing SAM/BAM files; version >=1.9 required for HiC-Pro compatibility)
- **bowtie2** (Read alignment mapping; required for HiC-Pro read alignment stage) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **R** (Statistical computing and visualization; required packages: RColorBrewer, ggplot2 (>2.2.1)) — http://www.r-project.org/
- **Python** (Core scripting language (>3.7); required libraries: pysam (>=0.15.4), bx-python (>=0.8.8), numpy (>=1.18.1), scipy (>=1.4.1))

## Examples

```
make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- config-system.txt file is generated without errors, containing resolved paths for all required tools
- All dependency versions match or exceed specified minimums (e.g., samtools >=1.9, Python >3.7)
- The 'which' command successfully locates each tool binary when entries in config-install.txt are left unset
- No error messages or warnings are reported during the 'make CONFIG_SYS=config-install.txt install' execution
- Subsequent pipeline commands (e.g., HiC-Pro -h) execute without 'command not found' or missing library errors

## Limitations

- If dependencies are not found in the system PATH and no explicit paths are provided in config-install.txt, automatic installation may fail or install incompatible versions.
- The pipeline requires Unix sort with the -V (version sort) option; macOS users must install GNU core utilities separately.
- Chromosome names in bowtie2 indexes must match those in the restriction fragment BED annotation files, or configuration validation may succeed but downstream processing will fail.
- Python 2 is no longer supported; Python >3.7 is mandatory, and older scripts or environments must be upgraded.
- The iced normalization module is no longer bundled with HiC-Pro and must be installed independently, which is not automatically detected by the make configure step.

## Evidence

- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] make CONFIG_SYS=config-install.txt install: "make CONFIG_SYS=config-install.txt install"
- [other] HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system.: "HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system."
- [readme] Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them. You can also edit the *config-install.txt* file and manually defined the paths to dependencies.: "Note that if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them. You can also edit the *config-install.txt* file and manually defined the"
- [readme] Unix sort (**which support -V option**) is required ! For Mac OS user, please install the GNU core utilities !: "Unix sort (**which support -V option**) is required ! For Mac OS user, please install the GNU core utilities !"
- [readme] Note that the current version no longer supports python 2: "Note that the current version no longer supports python 2"
