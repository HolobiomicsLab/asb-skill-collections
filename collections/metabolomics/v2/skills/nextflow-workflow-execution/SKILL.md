---
name: nextflow-workflow-execution
description: Use when you have .mzML or .abf LC-HRMS metabolomics raw data files and
  need to perform peak detection, feature identification, and chromatogram alignment
  reproducibly across different compute environments (local workstations, HPC clusters).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Nextflow ≥22.10.0
  - Nextflow
  - MSFLO
  - MS-DIAL
  - Docker
  - Singularity
  - ProteoWizard msConvert
  - Make
  - Conda/Mamba
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
- doi: 10.1038/s41586-023-06906-8
  title: ''
evidence_spans:
- '[![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A522.10.0-brightgreen.svg)](https://www.nextflow.io/)'
- containerized workflow MS-DIAL -> MSFLO
- To learn NextFlow checkout this documentation
- 'To learn NextFlow checkout this documentation: https://www.nextflow.io/docs/latest/index.html'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  - build: coll_reverse_metabolomics_cq
    doi: 10.1038/s41586-023-06906-8
    title: Reverse metabolomics
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00364
  all_source_dois:
  - 10.1021/jasms.4c00364
  - 10.1038/s41586-023-06906-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nextflow-workflow-execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute a containerized Nextflow workflow for LC-HRMS metabolomics data processing using Docker or Singularity backends. This skill orchestrates sequential MS-DIAL and MSFLO processing of .mzML input files within a reproducible, version-controlled pipeline environment.

## When to use

You have .mzML or .abf LC-HRMS metabolomics raw data files and need to perform peak detection, feature identification, and chromatogram alignment reproducibly across different compute environments (local workstations, HPC clusters). Use this skill when you need to avoid manual tool invocation and leverage containerization for portability and version control.

## When NOT to use

- Input data is already in processed feature table format (.csv/.tsv) — use this skill only for raw mass spectrometry data requiring peak detection and alignment.
- You require manual control over intermediate MS-DIAL or MSFLO parameter tweaking between stages — this workflow executes the entire pipeline sequentially without interactive intervention.
- Your data is in formats other than .mzML or .abf without prior conversion via ProteoWizard msConvert or Reifycs Abf Converter.

## Inputs

- .mzML or .abf raw LC-HRMS data files
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- MS1 reference library file (ms1_lib.txt)
- MS2 reference library file (ms2_lib.msp)

## Outputs

- Processed feature tables (.tsv format)
- Aligned data matrices
- Metabolite annotations and identifications
- Execution report (execution_report.html)
- Execution timeline (execution_timeline.html)
- Execution logs (logs/execution.log)

## How to apply

Clone the Nextflow4MS-DIAL repository and verify Nextflow ≥22.10.0 is installed. Place raw .mzML/.abf data files in the designated input directory (e.g., data/raw_data/), and provide MS-DIAL configuration (msdial_params.txt) and MS-FLO configuration (msflo_params.ini) files along with MS1 and MS2 reference libraries (ms1_lib.txt, ms2_lib.msp). Select the appropriate execution profile: use `-profile docker` for local execution on macOS/Linux with Docker installed, or `-profile singularity` (or HPC-specific profiles like HiPerGator.config) for high-performance computing environments. Invoke the pipeline with `nextflow run main.nf -profile <profile_name>`, optionally specifying resource constraints via `--max_cpus` and output directory via standard parameters. Monitor execution via the generated execution_report.html and execution_timeline.html files. The workflow automatically stages files, executes MS-DIAL containerized processing to generate intermediate peak-detection outputs, pipes those outputs directly to MSFLO for feature alignment and quantification, and collects final feature tables and annotations in the results directory.

## Related tools

- **Nextflow** (Workflow orchestration and execution engine that manages containerization, resource allocation, and pipeline stages) — https://www.nextflow.io/
- **MS-DIAL** (Containerized peak detection, feature identification, and chromatogram alignment for .mzML LC-HRMS data)
- **MSFLO** (Post-processing module for feature quantification, normalization, and annotation following MS-DIAL)
- **Docker** (Container runtime for local and portable execution of the MS-DIAL and MSFLO pipeline stages) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC environments as an alternative to Docker) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Utility for converting non-.mzML raw data formats to .mzML for Nextflow4MS-DIAL input) — https://proteowizard.sourceforge.io/download.html

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Workflow completion status: all processes exit with code 0 and no error messages appear in logs/execution.log or error.txt
- Output file presence: feature tables, aligned data matrices, and annotation files are present in the results directory with expected .tsv/.csv extensions
- Output integrity: feature tables contain numeric values in expected columns (m/z, retention time, intensity) and non-empty metadata rows
- Execution report validation: execution_report.html shows successful completion time, computational resource usage within allocated limits (--max_cpus), and container image hashes confirming Docker/Singularity backend was used
- Log file validation: execution_timeline.html shows sequential execution of MS-DIAL followed by MSFLO stages without process skipping or requeuing

## Limitations

- File naming: avoid special characters in input file names; underscores are safe but other special characters may cause unexpected errors or process skipping
- Version specificity: workflow requires Nextflow ≥22.10.0; older versions may lack required features for containerization and resource management
- No explicit MS-DIAL or MSFLO version pinning: the README does not specify tool versions, which may affect reproducibility if container images auto-update
- HPC configuration specificity: Singularity and cluster-specific configurations (e.g., HiPerGator.config) are provided as examples; other HPC schedulers (SLURM, PBS) require custom configuration
- CPU allocation gotcha: must use --max_cpus in configuration, not --cpus, to correctly specify per-process CPU limits in HPC environments

## Evidence

- [readme] Clone the repository and raw data setup: "Clone the repository: git clone https://github.com/Nextflow4Metabolomics/nextflow4ms-dial.git. Remove the example data and place your raw data files in data/raw_data/. The workflow accepts .mzML and"
- [readme] Configuration and execution command: "Run the pipeline. Use the docker profile for local execution and the singularity profile for high-performance computing environments: nextflow run main.nf -profile docker > logs/execution.log"
- [readme] Containerization backend support: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [other] Sequential pipeline architecture: "The workflow implements a containerized sequential pipeline that processes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container"
- [readme] Output validation requirements: "Example outputs are stored in the results folder. The file extensions for produced .msdial files have been changed to .tsv so the files can be opened in spreadsheet software such as Microsoft Excel."
- [readme] CPU allocation limitation: "Use --max_cpus, not --cpus, in the configuration file to define the CPUs available to each process."
