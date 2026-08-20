---
name: nextflow-pipeline-orchestration
description: Use when when you have raw LC-HRMS metabolomics data in .mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Nextflow ≥22.10.0
  - Nextflow
  - Docker
  - MS-DIAL
  - MSFLO
  - Singularity
  - ProteoWizard msConvert
  - Reifycs Abf Converter
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- '[![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A522.10.0-brightgreen.svg)](https://www.nextflow.io/)'
- nextflow4ms-dial
- Both Docker and Singularity (for high-performance computing) are supported
- Both Docker and Singularity (for high-performance computing) are supported.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial_cq
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00364
  all_source_dois:
  - 10.1021/jasms.4c00364
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nextflow-pipeline-orchestration

## Summary

Nextflow pipeline orchestration is a containerized workflow execution method for LC-HRMS metabolomics data processing that routes .mzML mass spectrometry files through modular analysis steps (MS-DIAL feature detection, MSFLO annotation) with reproducible results across local, container, and HPC environments.

## When to use

When you have raw LC-HRMS metabolomics data in .mzML or .abf format that requires reproducible, multi-stage processing (feature detection → peak alignment → annotation → statistical analysis) and you need to run the same workflow consistently across different computational environments (macOS, Linux, HPC clusters) without manual reconfiguration of tool dependencies.

## When NOT to use

- Input data is already in a processed feature table format (CSV/TSV) or peak-aligned matrix — the workflow is designed for raw LC-MS data, not pre-processed features
- Raw data is in vendor-specific binary formats (e.g., .raw, .d) without prior conversion to .mzML or .abf — use ProteoWizard msConvert or Reifycs Abf Converter first
- MS-DIAL or MSFLO parameter files are not available or cannot be configured — the workflow requires pre-tuned parameters for your analytical method

## Inputs

- Raw LC-HRMS data files (.mzML or .abf format)
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- MS1 reference library (ms1_lib.txt)
- MS2 reference library (ms2_lib.msp)

## Outputs

- Feature table (.tsv format, converted from .msdial)
- Execution report (execution_report.html)
- Execution timeline (execution_timeline.html)
- Process-level logs (logs/execution.log)

## How to apply

Install Nextflow (≥22.10.0), Java 11+, and a container runtime (Docker for local execution or Singularity for HPC). Clone the Nextflow4MS-DIAL repository and place raw .mzML files in the designated data/raw_data/ directory. Prepare MS-DIAL configuration (msdial_params.txt) and MS-FLO configuration (msflo_params.ini) files, along with MS1 and MS2 reference libraries (ms1_lib.txt, ms2_lib.msp). Execute the pipeline with `nextflow run main.nf -profile docker` (or `-profile singularity` for HPC). The workflow automatically routes data through containerized MS-DIAL for feature detection and peak alignment, then through MSFLO for annotation and statistical processing. Validate outputs by checking the results/ folder for .tsv feature tables and reviewing execution_report.html and execution_timeline.html for resource usage and process completion.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages containerized task execution and resource allocation across local and HPC environments) — https://www.nextflow.io/
- **MS-DIAL** (Performs feature detection and peak alignment on LC-HRMS data within the containerized pipeline)
- **MSFLO** (Performs metabolite annotation and statistical processing of aligned features downstream of MS-DIAL)
- **Docker** (Container runtime for local execution of containerized MS-DIAL and MSFLO modules) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC execution of containerized MS-DIAL and MSFLO modules) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Upstream tool for converting vendor-specific LC-MS data formats to .mzML) — https://proteowizard.sourceforge.io/download.html
- **Reifycs Abf Converter** (Upstream tool for creating .abf format files from other LC-MS data formats) — https://www.reifycs.com/AbfConverter/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Execution report (execution_report.html) shows all processes completed successfully with non-zero exit code 0
- Output feature table (.tsv) contains expected columns (m/z, retention time, peak intensity, metabolite annotations) with row count matching sample count × detected features
- Execution timeline (execution_timeline.html) shows MS-DIAL and MSFLO processes executed in correct sequence without gaps or resubmissions
- No errors in logs/execution.log; process-level logs confirm container image pulled and MS-DIAL/MSFLO ran with specified parameters
- Results folder contains .tsv files for all input .mzML samples; file sizes are consistent with data complexity

## Limitations

- File names with special characters (other than underscores) cause pipeline execution failures; only alphanumeric characters and underscores are safe
- CPU resource allocation must use --max_cpus (not --cpus) in configuration; misuse causes Slurm errors on HPC systems
- Workflow has been tested on macOS 13.5.1 (Intel Core i7, 16 GB memory) and Red Hat Enterprise Linux 8.8 (HiPerGator); behavior on other systems is not documented
- Limited validation and benchmarking data in current documentation; this is an initial release based on nf-core template
- MS-DIAL and MS-FLO parameters must be manually tuned for each analytical method; no default parameters are provided for different LC-MS instrument configurations

## Evidence

- [other] Nextflow4MS-DIAL implements a containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container runtimes.: "containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container runtimes"
- [readme] Installation and setup requirements: "Install Java 11 or later. The workflow was developed with Java 11.0.8. Install Nextflow. Install Docker for local execution or Singularity for many high-performance computing systems."
- [readme] Data preparation and configuration: "Remove the example data and place your raw data files in data/raw_data/. The workflow accepts .mzML and .abf files."
- [readme] Configuration requirements: "Add the MS-DIAL and MS-FLO configuration files to the data/ folder and name them msdial_params.txt and msflo_params.ini."
- [readme] Execution command: "Run the pipeline. Use the docker profile for local execution and the singularity profile for high-performance computing environments"
- [readme] File naming constraints: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] CPU allocation on HPC: "Use --max_cpus, not --cpus, in the configuration file to define the CPUs available to each process"
- [readme] Testing and validation: "The workflow was developed with Java 11.0.8. It supports macOS and Linux and has been tested successfully on: macOS 13.5.1 with a 2.6 GHz 6-Core Intel Core i7 processor and 16 GB memory. HiPerGator,"
