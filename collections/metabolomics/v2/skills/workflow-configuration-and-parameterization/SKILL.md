---
name: workflow-configuration-and-parameterization
description: Use when when preparing to execute the Nextflow4MS-DIAL workflow on raw LC-HRMS metabolomics data (.mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
  - Java
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- containerized workflow MS-DIAL -> MSFLO
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00364
  all_source_dois:
  - 10.1021/jasms.4c00364
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-configuration-and-parameterization

## Summary

Configure and parameterize a Nextflow-based LC-HRMS metabolomics workflow by specifying tool-specific configuration files, reference libraries, input paths, and container backends before execution. This skill ensures reproducible, portable workflow execution across local, containerized, and HPC environments.

## When to use

When preparing to execute the Nextflow4MS-DIAL workflow on raw LC-HRMS metabolomics data (.mzML or .abf files), you must configure MS-DIAL and MS-FLO parameters, supply MS1/MS2 spectral libraries, specify input/output directories, and select the appropriate container backend (Docker for local execution, Singularity for HPC) before invoking the pipeline.

## When NOT to use

- Input data is not in .mzML or .abf format; convert with ProteoWizard msConvert or Reifycs Abf Converter first.
- You lack the MS-DIAL and MS-FLO configuration files and spectral libraries specific to your analytical method; obtain or generate these before workflow execution.
- The computing environment does not support Docker or Singularity containers; verify container engine availability and HPC scheduler compatibility before configuration.

## Inputs

- Raw LC-HRMS data files (.mzML or .abf format)
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 spectral library file (ms1_lib.txt)
- MS2 spectral library file (ms2_lib.msp)
- Nextflow configuration files (conf/base.config, conf/HiPerGator.config)
- Java runtime (version 11 or later)
- Nextflow installation (≥22.10.0)
- Docker or Singularity container runtime

## Outputs

- Execution report (execution_report.html with runtime and resource metrics)
- Execution timeline (execution_timeline.html showing per-process timing)
- Execution log (logs/execution.log containing metadata, parameters, and process-level details)
- Processed LC-HRMS feature tables (.tsv files converted from .msdial output)

## How to apply

First, prepare MS-DIAL configuration (msdial_params.txt) and MS-FLO configuration (msflo_params.ini) files specific to your analytical method, placing them in the `data/` folder. Add MS1 and MS2 spectral library files (ms1_lib.txt and ms2_lib.msp) to the same directory. Then, configure the Nextflow execution profile: use the `docker` profile in `conf/base.config` for local execution, or the `singularity` profile (defined in `conf/HiPerGator.config`) for HPC systems. Verify that reference file paths in `conf/base.config` match your setup and that file naming conventions follow the workflow's expectations (underscores are safe; avoid special characters). Finally, invoke the workflow with the appropriate profile flag and optional command-line parameter overrides (e.g., `--max_cpus` for resource allocation, not `--cpus`), directing logs to a designated output folder.

## Related tools

- **Nextflow** (Workflow orchestration and execution engine managing task distribution, containerization, and logging across execution environments) — https://www.nextflow.io/
- **MS-DIAL** (Containerized peak detection and chromatogram alignment tool; parameters defined in msdial_params.txt)
- **MSFLO** (Containerized feature quantification and metabolite identification tool; parameters defined in msflo_params.ini)
- **Docker** (Container backend for local execution of MS-DIAL and MSFLO; configured in conf/base.config) — https://docs.docker.com/engine/installation/
- **Singularity** (Container backend for HPC environments; configured in conf/HiPerGator.config for Slurm-based systems) — https://www.sylabs.io/guides/3.0/user-guide/
- **Java** (Runtime environment required for Nextflow execution (version 11.0.8 or later))

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Execution log (logs/execution.log) records successful Nextflow and workflow version metadata, parameter settings, and absence of configuration-related errors.
- Execution report (execution_report.html) shows all pipeline stages completed without error and resource allocation matches CPU/memory requests in configuration.
- Output directory contains expected .tsv feature tables and aligned data matrices with correct naming and non-zero file sizes.
- Log file does not contain 'Process requirement exceed available CPUs' or file-name-related errors; file names in input directory use only safe characters (underscores, alphanumerics).
- Container information in execution log confirms the correct backend (Docker or Singularity) was invoked and container images were successfully pulled/cached.

## Limitations

- Special characters in input file names cause unexpected errors; only underscores and alphanumerics are safe.
- MS-DIAL and MS-FLO version information is not specified in configuration files, limiting reproducibility and version-specific debugging; users must track tool versions manually.
- Slurm job allocation confusion: the `--max_cpus` parameter defines per-process CPU limits in the configuration, not total job CPUs; using `--cpus` instead causes allocation failures.
- The workflow has been tested only on macOS 13.5.1 (Intel Core i7, 16 GB memory) and Red Hat Enterprise Linux 8.8 (HiPerGator); compatibility with other OS versions or HPC schedulers is not documented.
- No explicit reproducibility validation or testing protocol is provided in the initial release; users must manually verify results against example outputs.

## Evidence

- [readme] Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`."
- [readme] Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`.: "Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`."
- [readme] Before processing your own data, confirm that the reference file in `conf/base.config` and the MS-DIAL configuration file are set correctly.: "Before processing your own data, confirm that the reference file in `conf/base.config` and the MS-DIAL configuration file are set correctly."
- [readme] Docker configuration is defined in `conf/base.config`. High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`.: "Docker configuration is defined in `conf/base.config`. High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`."
- [readme] The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce.: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process.: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [other] Configure the workflow parameters (sample input path, output directory, Docker backend specification) in the Nextflow config or command-line arguments.: "Configure the workflow parameters (sample input path, output directory, Docker backend specification) in the Nextflow config or command-line arguments."
