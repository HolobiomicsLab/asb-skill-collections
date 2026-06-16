# Workflow Challenge: `coll_hicpro_workflow`


> HiC-Pro is an optimized and flexible pipeline for Hi-C data processing that automates installation of key dependencies and provides containerized deployment options.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

HiC-Pro describes a configurable pipeline architecture for Hi-C data processing with integrated dependency management. The pipeline implements SAM processing using samtools (>=1.9), which can be automatically installed if not detected; requires the iced module for normalization, which must be independently installed as it is no longer part of the HiC-Pro source code; and supports an installation configuration mechanism where users edit a config-install.txt file to specify tool paths. When paths are not explicitly set, the system searches for dependencies in the $PATH environment variable before executing the installation command. HiC-Pro provides multiple deployment options through conda, Docker, and Singularity containers to ease dependency installation.

## Research questions

- What post-processing operations does HiC-Pro apply to SAM/BAM files output from the alignment stage?
- How does the ICE normalization algorithm iteratively correct and balance raw Hi-C contact matrices using the iced Python module?
- How does HiC-Pro detect the installation paths of required binary tools (Bowtie2, samtools) and generate an environment-specific configuration file during setup?
- Can a Conda environment be successfully created from an environment specification file with all required Python (>3.7) and R dependencies for HiC-Pro, and can tool binaries (bowtie2, samtools, iced) be correctly resolved within that environment?

## Methods overview

Prepare HiC-Pro installation directory and config-install.txt template. Set SAMTOOLS_PATH in config-install.txt to the full path of samtools binary (>=1.9), or leave empty for automatic PATH-based detection. Execute 'make CONFIG_SYS=config-install.txt install' to run dependency checking and validation. Validate: Confirm that samtools (>=1.9) is correctly detected and its full path is recorded in the generated config-system.txt file. References: source article (DOI: 10.1186/s13059-015-0831-x) Verify Python >3.7 interpreter availability and accessibility. Obtain iced module source code from the official GitHub repository (https://github.com/hiclib/iced). Install iced and declare transitive dependencies (numpy ≥1.18.1, scipy ≥1.4.1) via pip or setup.py. Validate iced installation by importing the module and querying version and core API functions. Validation: confirm iced module is importable, all required dependencies meet version thresholds, and no import errors occur on test invocation. References: source article (DOI: 10.1186/s13059-015-0831-x) Parse config-install.txt user input to extract explicit paths and cluster scheduler preference. Query system PATH using 'which' for each binary (bowtie2, samtools, R, Python) where user did not provide explicit path. Verify bowtie2 and samtools presence; auto-install either if missing and version requirements (samtools >=1.9, Python >3.7) are not met. Collect all resolved paths and parameters into a key–value structure conforming to the config-system.txt schema. Write the locked, immutable config-system.txt file to the installation PREFIX directory. Validation: config-system.txt exists, is read-only, and contains non-empty entries for all six required fields (PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS). References: source article (DOI: 10.1186/s13059-015-0831-x) Install Miniconda package manager from official sources. Create Conda environment from HiC-Pro environment.yml with specified installation path. Activate the Conda environment to make all dependencies available. Verify Python version and import all required Python libraries (bx-python, numpy, scipy, pysam, argparse) to confirm correct installation. Verify R availability and test loading of required R packages (ggplot2, RColorBrewer, grid). Verify tool binaries (bowtie2, samtools >=1.9) are executable and in PATH. Independently install and import iced module since it is not part of HiC-Pro source. Validation: Generate dependency verification report confirming all tool versions meet minimum requirements, all Python and R packages are importable, and all binary paths are resolved. References: source article (DOI: 10.1186/s13059-015-0831-x)

**Domain:** bioinformatics

**Techniques:** quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** HiC-Pro is an optimized and flexible pipeline for Hi-C data processing. _[grounded: hicpro_system]_
- **(finding)** R version with ggplot2 greater than 2.2.1 is required as a dependency.
- **(finding)** Python greater than 3.7 is required as a dependency. _[grounded: tool_python]_
- **(finding)** bx-python version 0.8.8 or greater is required. _[grounded: tool_python]_
- **(finding)** numpy version 1.18.1 or greater is required.
- **(finding)** scipy version 1.4.1 or greater is required.
- **(finding)** pysam version 0.15.4 or greater is required.
- **(finding)** samtools version 1.9 or greater can be automatically installed if not detected. _[grounded: tool_bowtie2]_
- **(finding)** bowtie2 can be automatically installed if not detected. _[grounded: tool_bowtie2]_
- **(finding)** The iced module is required for HiC-Pro installation. _[grounded: hicpro_system]_
- **(finding)** Iced is no longer part of the HiC-Pro source code and should be independently installed. _[grounded: hicpro_system]_
- **(finding)** HiC-Pro version 3.X provides conda, Docker, and Singularity recipes. _[grounded: hicpro_system]_
- **(finding)** A conda environment can be created using the provided yml file from HiC-Pro. _[grounded: hicpro_system]_
- **(finding)** miniconda must be installed first to build a conda environment for HiC-Pro. _[grounded: hicpro_system]_
- **(finding)** A Docker image for HiC-Pro is automatically built and available on Docker Hub. _[grounded: hicpro_system]_
- **(finding)** The docker pull command nservant/hicpro:latest retrieves the latest HiC-Pro Docker image. _[grounded: hicpro_system]_
- **(finding)** A ready-to-use Singularity container for HiC-Pro is available at a specified URL. _[grounded: hicpro_system]_
- **(finding)** The config-install.txt file must be edited to set paths for HiC-Pro installation. _[grounded: hicpro_system]_
- **(finding)** CLUSTER_SYS configuration must be set to TORQUE, SGE, or SLURM for cluster submission.
- **(finding)** The installation command for HiC-Pro is make CONFIG_SYS=config-install.txt install. _[grounded: hicpro_system]_
- **(finding)** Installation generates a config-system.txt file that defines all paths to HiC-Pro dependencies. _[grounded: hicpro_system]_
- **(finding)** The config-system.txt file should not be edited. _[grounded: comp_config_system]_
- **(finding)** RColorBrewer is a required R package for HiC-Pro. _[grounded: hicpro_system]_
- **(finding)** The R grid package is required for HiC-Pro. _[grounded: hicpro_system]_
- **(finding)** argparse is a required Python library for HiC-Pro. _[grounded: hicpro_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- TORQUE scheduler as alternative to SLURM or SGE
- SGE scheduler as alternative to TORQUE or SLURM
- SLURM scheduler as alternative to TORQUE or SGE

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- samtools version must be >=1.9 or >=0.1.19 depending on context
- Python version must be >3.7 or >2.7

## Steps

### Step `task_001`
- Title: Reconstruct the bowtie2-based read alignment stage of the HiC-Pro pipeline
- Task kind: `component_reconstruction`
- Task: Install and configure samtools (>=1.9) as a dependency for HiC-Pro's SAM processing stage, verifying that the tool is correctly integrated into the system PATH and accessible for downstream BAM filtering, sorting, and indexing operations.
- Inputs:
  - HiC-Pro installation source directory containing config-install.txt template and Makefile
  - samtools binary (version >=1.9) installed on system or available in PATH
- Expected outputs:
  - config-system.txt file containing resolved full path to samtools binary and all other HiC-Pro dependencies
- Tools: MultiQC 1.8, samtools (>=1.9), bowtie2
- Landmark output files: config-install.txt (edited with samtools path or left empty for auto-detection), installation.log (output from 'make install' showing dependency resolution)
- Primary expected artifact: `config-system.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the SAM processing stage that filters and sorts aligned Hi-C reads
- Task kind: `component_reconstruction`
- Task: Install and configure the iced Python module as a standalone dependency for Hi-C matrix normalization, producing a validated iced environment ready for ICE normalization workflows.
- Inputs:
  - Python interpreter version >3.7 with pip or setuptools available
  - iced module source repository from https://github.com/hiclib/iced
- Expected outputs:
  - Functional iced Python module installed and importable in the target environment
  - Installation validation log confirming iced version, API availability, and dependency versions (numpy, scipy)
- Tools: MultiQC 1.8, Python (>3.7), iced, numpy (>=1.18.1), scipy (>=1.4.1)
- Landmark output files: iced_version_check.txt, dependency_versions.txt
- Primary expected artifact: `iced_installation_validation.log`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the ICE normalization stage that balances a Hi-C contact matrix
- Task kind: `component_reconstruction`
- Task: Generate a config-system.txt file that detects and records the file system paths to HiC-Pro binary dependencies (bowtie2, samtools, R, Python) by parsing a user-edited config-install.txt template and querying the system PATH. The output file encodes environment-specific configuration for subsequent pipeline execution.
- Inputs:
  - config-install.txt template file with placeholder path entries and cluster configuration
- Expected outputs:
  - config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type
- Tools: MultiQC 1.8, bowtie2, samtools (>=1.9), R, Python (>3.7)
- Landmark output files: bowtie2_path_resolved.log, samtools_version_check.log, r_and_python_paths.log
- Primary expected artifact: `config-system.txt`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the config-system.txt generation step performed during HiC-Pro installation
- Task kind: `component_reconstruction`
- Task: Install and verify a HiC-Pro Conda environment by creating the environment from the provided YAML specification, installing all required Python (>3.7) and R dependencies with specified versions, and confirming that tool binaries (bowtie2, samtools, iced) are correctly resolved and accessible.
- Inputs:
  - HiC-Pro environment.yml specification file
  - Miniconda installation package or access to conda package manager
- Expected outputs:
  - Active Conda environment with all HiC-Pro dependencies installed and verified
  - Dependency verification report listing Python version, all Python package versions, R version, R package availability, tool binary paths, and iced module status
- Tools: MultiQC 1.8, conda, Python (>3.7), R, bowtie2, samtools (>=1.9), bx-python (>=0.8.8), numpy (>=1.18.1), scipy (>=1.4.1), pysam (>=0.15.4), ggplot2 (>2.2.1), RColorBrewer, iced
- Landmark output files: environment.yml, conda_env_creation.log, python_dependencies.txt, r_dependencies.txt, tool_binary_paths.txt, hicpro_env_verification_report.txt
- Primary expected artifact: `hicpro_env_verification_report.txt`

## Final expected outputs

- `config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type` (type: file, tolerance: hash)
- `Active Conda environment with all HiC-Pro dependencies installed and verified` (type: file, tolerance: hash)
- `Dependency verification report listing Python version, all Python package versions, R version, R package availability, tool binary paths, and iced module status` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_hicpro_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type": "<locator>",
    "Active Conda environment with all HiC-Pro dependencies installed and verified": "<locator>",
    "Dependency verification report listing Python version, all Python package versions, R version, R package availability, tool binary paths, and iced module status": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
