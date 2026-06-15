---
name: bioinformatics-tool-version-compatibility-assessment
description: Use when before executing a complex bioinformatics pipeline (such as Hi-C data processing) that depends on multiple third-party tools with explicit version constraints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
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

# bioinformatics-tool-version-compatibility-assessment

## Summary

Assess and resolve version compatibility requirements for interdependent bioinformatics tools before pipeline execution. This skill ensures that declared tool versions (e.g., samtools ≥1.9, Python >3.7) are available in the system environment or can be automatically installed, preventing runtime failures downstream.

## When to use

Before executing a complex bioinformatics pipeline (such as Hi-C data processing) that depends on multiple third-party tools with explicit version constraints. Apply this skill when tool versions are documented in configuration files or installation instructions and you need to validate that the current system environment satisfies all declared requirements, or when automatic dependency resolution is available and you must configure which tools to auto-install vs. source from PATH.

## When NOT to use

- Pipeline tools are already fully installed and validated in a frozen container (Docker, Singularity) — version compatibility is pre-resolved at container build time, not at runtime.
- You are running a single-tool analysis (e.g., only bowtie2 alignment) that does not require inter-tool version coordination.
- Pipeline provides no version constraints or auto-installation mechanism — manual dependency management is required instead.

## Inputs

- config-install.txt (template configuration file with tool path declarations and version requirements)
- system PATH environment variable
- installed tool binaries (samtools, bowtie2, Python, R, etc.)
- optional: full paths to pre-installed tool binaries

## Outputs

- config-system.txt (resolved configuration file recording detected tool paths and versions)
- validation report indicating which tools met version thresholds
- installation log showing auto-installed dependencies (if applicable)

## How to apply

First, identify all declared tool dependencies and their version thresholds from the pipeline's documentation and configuration templates (e.g., config-install.txt). Create or edit a configuration file (such as config-install.txt) to specify either full paths to tool binaries or leave version fields unset to allow automatic detection via the system PATH using the 'which' command. Then execute the pipeline's dependency-checking build target (e.g., 'make CONFIG_SYS=config-install.txt install') which validates tool availability against declared version constraints and generates a resolved configuration file (e.g., config-system.txt) recording the paths and versions of tools actually found. Finally, inspect the generated system configuration file to confirm that all tools at minimum required versions were detected and recorded, indicating readiness for pipeline stages that depend on those tools.

## Related tools

- **samtools** (SAM/BAM post-processing; version ≥1.9 required for HiC-Pro pipeline compatibility)
- **bowtie2** (Read alignment stage; version >2.2.2 strongly recommended for allele-specific analysis) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **Python** (Runtime for pysam (≥0.15.4), bx-python (≥0.8.8), numpy (≥1.18.1), scipy (≥1.4.1); requires version >3.7) — https://www.python.org/
- **R** (Plotting and statistical outputs; requires RColorBrewer and ggplot2 (>2.2.1) packages) — http://www.r-project.org/
- **pysam** (Python wrapper for SAM/BAM file manipulation; pysam wraps htslib-1.23.1, samtools-1.23.1) — https://github.com/pysam-developers/pysam
- **iced** (ICE normalization of Hi-C contact maps; requires python ≥2.7, numpy ≥1.16, scipy ≥0.19, sklearn, pandas; must be independently installed) — https://github.com/hiclib/iced

## Examples

```
make CONFIG_SYS=config-install.txt install
```

## Evaluation signals

- config-system.txt is generated without errors and contains paths to all declared tools
- Each tool path in config-system.txt points to a working binary that can be invoked (e.g., 'samtools --version' returns ≥1.9)
- Version validation output confirms all tools meet minimum version thresholds (samtools ≥1.9, Python >3.7, R with ggplot2 >2.2.1)
- Pipeline build or setup phase completes without 'tool not found' or 'version mismatch' errors before any data processing step begins
- For auto-installed dependencies, installation log shows successful compilation or download and verification of required versions (e.g., bx-python ≥0.8.8, scipy ≥1.4.1)

## Limitations

- Automatic dependency detection via 'which' relies on correct PATH ordering; if multiple versions of a tool exist in PATH, the first match may not be the desired version — full paths in config-install.txt are recommended for production environments.
- No changelog is provided for version-to-version compatibility mapping, so cross-version breakage must be discovered empirically or via external documentation.
- Iced is no longer bundled with HiC-Pro and must be independently installed; version compatibility between iced and the main pipeline is not automatically validated.
- macOS users must install GNU core utilities (not BSD sort) as Unix sort with -V option support is required; this platform-specific constraint is not auto-detected.

## Evidence

- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [other] HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system.: "HiC-Pro implements SAM processing using samtools (>=1.9), which is automatically installed if not detected in the system."
- [other] Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved tool paths.: "Execute 'make CONFIG_SYS=config-install.txt install' to trigger dependency checking and configuration, which will validate samtools availability and generate the config-system.txt file with resolved"
- [readme] The current version of pysam wraps 3rd-party code from htslib-1.23.1, samtools-1.23.1, and bcftools-1.23.1.: "The current version of pysam wraps 3rd-party code from htslib-1.23.1, samtools-1.23.1, and bcftools-1.23.1."
- [methods] Iced is no longer part of the HiC-Pro source code, and should be independantly installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
