---
name: system-dependency-version-checking
description: Use when you are preparing to run a complex multi-tool bioinformatics pipeline (such as HiC-Pro) on a new system or cluster, and need to confirm that all required binaries exist in the execution environment and meet minimum version thresholds (e.g., samtools >=1.9, Python >3.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3316
  tools:
  - MultiQC 1.8
  - bowtie2
  - samtools (>=1.9)
  - R
  - samtools
  - Python
  - pysam
  - bx-python
  - numpy
  - scipy
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

# system-dependency-version-checking

## Summary

Detect and validate installed dependency binaries (bowtie2, samtools, R, Python) against minimum version requirements, and automatically install missing or outdated tools to ensure pipeline environment compatibility. This skill bridges the gap between user configuration and runtime readiness in bioinformatics pipelines.

## When to use

You are preparing to run a complex multi-tool bioinformatics pipeline (such as HiC-Pro) on a new system or cluster, and need to confirm that all required binaries exist in the execution environment and meet minimum version thresholds (e.g., samtools >=1.9, Python >3.7) before launching data processing workflows.

## When NOT to use

- You are running a containerized pipeline (Docker, Singularity) where all dependencies are already pinned and installed inside the image — the container build process, not the end-user, is responsible for version checking.
- You have a pre-built, system-wide installation of all tools that is guaranteed to be compatible (e.g., managed by a cluster admin via module systems like Lmod); direct path lookup is sufficient.
- Your pipeline is designed to use only system-provided binaries and does not support automatic installation fallback.

## Inputs

- config-install.txt (template configuration file with placeholder tool paths)
- System PATH environment variable
- User-edited configuration entries for PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS

## Outputs

- config-system.txt (locked, system-specific configuration with validated tool paths and versions)
- Installation artifacts for automatically installed tools (bowtie2, samtools binaries if required)
- Version validation report (implicit in successful config-system.txt generation)

## How to apply

First, define explicit version and path requirements for each dependency (bowtie2, samtools, R, Python) in a configuration template (config-install.txt). For each dependency not explicitly set by the user, query the system PATH using the 'which' command to locate the binary. Once located, validate the installed version against the minimum threshold (samtools >=1.9, Python >3.7). If a required binary is missing or the version is below the threshold, trigger automatic installation of pre-packaged binaries (bowtie2 and samtools >=1.9 support auto-install). Compile all detected paths and system parameters into a read-only system configuration file (config-system.txt) that the pipeline will reference at runtime. This ensures that version conflicts are resolved before execution begins, and users have a locked record of which tool versions were actually used.

## Related tools

- **bowtie2** (Short-read sequence aligner; must be >=2.2.2 for allele-specific analysis, auto-installable if missing) — http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
- **samtools** (BAM/SAM file manipulation and validation; minimum version >=1.9, auto-installable if missing) — http://samtools.sourceforge.net/
- **R** (Statistical computing runtime; required for visualization packages (ggplot2, RColorBrewer))
- **Python** (Scripting language for data processing pipelines; minimum version >3.7, used for pysam, bx-python, numpy, scipy) — https://www.python.org/
- **pysam** (Python wrapper around samtools C-API for BAM/SAM manipulation; version >=0.15.4) — https://github.com/pysam-developers/pysam
- **bx-python** (Python interval/genome utilities; minimum version >=0.8.8) — https://pypi.python.org/pypi/bx-python
- **numpy** (Numerical computing library; minimum version >=1.18.1) — http://www.scipy.org/scipylib/download.html
- **scipy** (Scientific computing library; minimum version >=1.4.1) — http://www.scipy.org/scipylib/download.html
- **iced** (Iterative correction and eigenvalue decomposition for Hi-C normalization; independently installed, not bundled) — https://github.com/hiclib/iced

## Examples

```
make configure && make install
```

## Evaluation signals

- config-system.txt is successfully generated with non-empty, validated paths for all required binaries (bowtie2, samtools, R, Python, etc.)
- Version checks pass: bowtie2 is detected, samtools version >=1.9 is confirmed, Python version >3.7 is confirmed, R with ggplot2 (>2.2.1) and RColorBrewer is available
- config-system.txt is marked read-only (file permissions prevent accidental user modification during pipeline execution)
- If auto-install was triggered, bowtie2 and/or samtools binaries are installed in the PREFIX directory and appear in the final config-system.txt paths
- Pipeline execution proceeds without 'command not found' or version mismatch errors; all downstream tools are able to locate and invoke dependencies

## Limitations

- Auto-installation is limited to bowtie2 and samtools; other dependencies (R packages, Python libraries) must be pre-installed or require manual intervention.
- The 'which' command may not locate binaries in non-standard PATH configurations or in secure computing environments that restrict environment variable access.
- Version detection relies on standard --version or -version flags; tools with non-standard version reporting may fail validation.
- The pipeline does not validate dependency compatibility with each other (e.g., scipy 1.4.1 compatibility with the specific numpy version); only individual minimum thresholds are checked.
- On macOS, the system 'sort' command may not support the -V option required by HiC-Pro; GNU coreutils must be explicitly installed and configured.

## Evidence

- [methods] Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH: "Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH"
- [methods] A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.: "A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected."
- [other] Verify installed versions meet minimum requirements: samtools >=1.9 and Python >3.7.: "Verify installed versions meet minimum requirements: samtools >=1.9 and Python >3.7."
- [other] Compile all detected or user-specified paths and system parameters into a structured config-system.txt file with entries for each dependency path and cluster scheduler type.: "Compile all detected or user-specified paths and system parameters into a structured config-system.txt file with entries for each dependency path and cluster scheduler type."
- [other] Lock the generated config-system.txt as read-only to prevent accidental user modification during pipeline execution.: "Lock the generated config-system.txt as read-only to prevent accidental user modification during pipeline execution."
- [readme] samtools (>1.9) is required: "samtools (>1.9) is required ! For Mac OS user, please install the GNU core utilities !"
- [readme] if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them.: "if some of these dependencies are not installed (i.e. not detected in the $PATH), HiC-Pro will try to install them."
- [readme] Bowtie >2.2.2 is strongly recommanded for allele specific analysis: "Bowtie >2.2.2 is strongly recommanded for allele specific analysis."
