# SciTask Card: Reconstruct the ICE normalization stage that balances a Hi-C contact matrix

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:03:07.177659+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_hicpro/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `information-extraction`
- DOI: `10.1186/s13059-015-0831-x`
- GitHub: `pysam-developers/pysam`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `gene-regulation`
- Techniques: `quality-control`

## Research Question
How does HiC-Pro detect the installation paths of required binary tools (Bowtie2, samtools) and generate an environment-specific configuration file during setup?

## Connected Finding
HiC-Pro implements an installation configuration mechanism where users edit a config-install.txt file to set tool paths; if paths are not explicitly set, the system searches for dependencies in the $PATH environment variable, and then executes 'make CONFIG_SYS=config-install.txt install' to complete the setup.

## Task Description
Generate a config-system.txt file that detects and records the file system paths to HiC-Pro binary dependencies (bowtie2, samtools, R, Python) by parsing a user-edited config-install.txt template and querying the system PATH. The output file encodes environment-specific configuration for subsequent pipeline execution.

## Inputs
- config-install.txt template file with placeholder path entries and cluster configuration

## Expected Outputs
- config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type

## Expected Output File

- `config-system.txt`

## Landmark Outputs

- `bowtie2_path_resolved.log`
- `samtools_version_check.log`
- `r_and_python_paths.log`

## Tools
- MultiQC 1.8
- bowtie2
- samtools (>=1.9)
- R
- Python (>3.7)

## Skills
- binary-path-detection-and-validation
- system-dependency-version-checking
- configuration-file-generation-and-templating
- shell-environment-variable-resolution
- hpc-cluster-scheduler-configuration

## Workflow Description
1. Read the config-install.txt template provided by the user, which contains placeholder entries for PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, and CLUSTER_SYS. 2. For each path entry not explicitly set by the user, query the system PATH using the 'which' command to locate bowtie2, samtools, R, and Python binaries. 3. Validate that bowtie2 and samtools are present; if either is missing, trigger automatic installation (bowtie2 and samtools >=1.9 can be auto-installed). 4. Verify installed versions meet minimum requirements: samtools >=1.9 and Python >3.7. 5. Compile all detected or user-specified paths and system parameters into a structured config-system.txt file with entries for each dependency path and cluster scheduler type. 6. Lock the generated config-system.txt as read-only to prevent accidental user modification during pipeline execution.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/button_blue.png` | figure | False |
| `figures/button_blue.svg` | figure | False |
| `figures/button_green.png` | figure | False |
| `figures/button_green.svg` | figure | False |
| `figures/button_orange.png` | figure | False |
| `figures/button_orange.svg` | figure | False |
| `figures/hicpro_contactstat_IMR90rep1.png` | figure | False |
| `figures/hicpro_filteringstat_IMR90rep1.png` | figure | False |
| `figures/hicpro_fragsize_IMR90rep1.png` | figure | False |
| `figures/hicpro_mappingstat_IMR90rep1.png` | figure | False |
| `figures/hicpro_pairingstat_IMR90rep1.png` | figure | False |
| `figures/hicpro_wkflow.png` | figure | False |
| `figures/logo_1.png` | figure | False |
| `figures/logo_1.svg` | figure | False |
| `figures/logos.svg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting installation configuration changes, version history, or modification log for config-system.txt generation is available.

## Domain Knowledge
- HiC-Pro requires bowtie2 and samtools >=1.9 as core aligners; these two tools are the only dependencies eligible for automatic installation if missing, all others must be pre-installed by the user.
- The 'which' command is the standard mechanism to resolve binary names to full filesystem paths when user has not explicitly provided them in config-install.txt.
- CLUSTER_SYS must be set to one of exactly three values (TORQUE, SGE, or SLURM) to specify the job scheduler for cluster submission.
- The generated config-system.txt is write-protected to prevent accidental user modification; it encodes the frozen environment state at installation time and must not be edited after generation.
- Python >3.7 is required alongside R with packages ggplot2 (>2.2.1), RColorBrewer, and grid; scipy, numpy, bx-python, and pysam are also mandatory Python dependencies but their version/availability is checked post-configuration.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does HiC-Pro detect the installation paths of required binary tools (Bowtie2, samtools) and generate an environment-specific configuration file during setup?: 'An optimized and flexible pipeline for Hi-C data processing'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] HiC-Pro implements an installation configuration mechanism where users edit a config-install.txt file to set tool paths; if paths are not explicitly set, the system searches for dependencies in the $PATH environment variable, and then executes 'make CONFIG_SYS=config-install.txt install' to complete the setup.: 'Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] config-install.txt template file with placeholder path entries and cluster configuration: 'Edit the config-install.txt file and set the paths. If not set, the dependencies will be sought in the $PATH and defined using the 'which' command.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] config-system.txt file encoding detected or user-supplied paths to bowtie2, samtools, R, and Python binaries, plus cluster scheduler type: 'The installation process will generate a config-system.txt file which defines all paths to HiC-Pro dependencies. Please, do not edit this file !'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] bowtie2: 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] samtools (>=1.9): 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] R: 'R (http://www.r-project.org/) with the following packages'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Python (>3.7): 'Python (>3.7) libraries'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting installation configuration changes, version history, or modification log for config-system.txt generation is available.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file config-system.txt exists in package after installation step
- verify config-system.txt contains field for bowtie2 binary path (key-value pair or structured format)
- verify config-system.txt contains field for samtools binary path (key-value pair or structured format)
- verify script that generates config-system.txt runs without error when bowtie2 and samtools are available in PATH or specified in inputs
- verify config-system.txt format matches the documented structure (exact format robust to whitespace normalization)
- verify output file is valid text or INI format (file_format_is text or INI)
- verify bowtie2 path value in config-system.txt points to existing executable or matches reference path from inputs

### Expert Review
- assess whether detected bowtie2 and samtools versions satisfy documented minimum version requirements (bowtie2 any version, samtools >=1.9)
- evaluate whether environment variable substitution and PATH fallback logic are correctly implemented in config-system.txt generation
- review whether config-system.txt encoding is compatible with downstream runtime pipeline consumption

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Parse config-install.txt user input to extract explicit paths and cluster scheduler preference.
2. Query system PATH using 'which' for each binary (bowtie2, samtools, R, Python) where user did not provide explicit path.
3. Verify bowtie2 and samtools presence; auto-install either if missing and version requirements (samtools >=1.9, Python >3.7) are not met.
4. Collect all resolved paths and parameters into a key–value structure conforming to the config-system.txt schema.
5. Write the locked, immutable config-system.txt file to the installation PREFIX directory.
6. Validation: config-system.txt exists, is read-only, and contains non-empty entries for all six required fields (PREFIX, BOWTIE2_PATH, SAMTOOLS_PATH, R_PATH, PYTHON_PATH, CLUSTER_SYS).
7. References: source article (DOI: 10.1186/s13059-015-0831-x)

## Workflow Ports

**Inputs:**

- `config_template` — config-install.txt template with user-edited path entries ← `task_001/config_system`

**Outputs:**

- `config_system` — config-system.txt system configuration file with resolved dependency paths

**Used:** `urn:asb:port:task_001/config_system`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:nservant__HiC-Pro`
- **Synthesized at:** 2026-06-15T19:09:16+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
