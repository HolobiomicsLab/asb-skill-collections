---
name: container-image-management
description: Use when your LC-HRMS metabolomics data (.mzML or .abf files) must be
  processed reproducibly across multiple machines (local workstations, HPCs, cloud)
  without manual tool installation, or when you need to enforce identical computational
  environments for peer review and long-term archival.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - Nextflow
  - Singularity
  - MS-DIAL
  - MSFLO
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
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

# container-image-management

## Summary

Deploy and manage containerized bioinformatics workflows using Docker or Singularity runtimes to ensure reproducible LC-HRMS metabolomics analysis across heterogeneous compute environments. This skill enables portable execution of MS-DIAL and MSFLO pipelines without dependency resolution or system-specific compilation.

## When to use

Your LC-HRMS metabolomics data (.mzML or .abf files) must be processed reproducibly across multiple machines (local workstations, HPCs, cloud) without manual tool installation, or when you need to enforce identical computational environments for peer review and long-term archival.

## When NOT to use

- Your input data is already a processed feature table (.csv, .tsv) — container deployment is unnecessary for downstream statistical analysis.
- You require real-time interactive parameter tuning within the MS-DIAL GUI; containerized workflows enforce static configurations.
- Your compute environment prohibits container runtimes entirely (neither Docker nor Singularity available); fall back to native tool installation.

## Inputs

- .mzML or .abf raw mass spectrometry data files
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- MS1 spectral library (ms1_lib.txt)
- MS2 spectral library (ms2_lib.msp)

## Outputs

- Aligned feature table (.tsv / .msdial)
- Annotated metabolite features (post-MSFLO)
- Execution report (execution_report.html)
- Execution timeline (execution_timeline.html)
- Process-level logs (logs/execution.log)

## How to apply

Select your target execution environment: Docker for local macOS/Linux machines with direct container runtime access, or Singularity for HPC systems (e.g., SLURM-managed clusters) where unprivileged container execution is required. Install the Nextflow workflow (≥22.10.0) and the corresponding container runtime. Prepare your .mzML input files in the `data/raw_data/` directory, along with MS-DIAL configuration (`msdial_params.txt`), MS-FLO configuration (`msflo_params.ini`), and reference spectral libraries (`ms1_lib.txt`, `ms2_lib.msp`). Invoke the Nextflow pipeline with the `-profile docker` or `-profile singularity` flag; Nextflow will automatically pull, build, and execute the MS-DIAL and MSFLO container images, routing aligned features through both stages and collecting the final feature table (.tsv) output. Validate that container layer caching and process parallelization completed without errors by inspecting the HTML execution reports (`execution_report.html`, `execution_timeline.html`) and confirming output file schemas match expected metabolomics feature tables.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages container lifecycle, process parallelization, and resource scheduling across Docker/Singularity runtimes) — https://www.nextflow.io/
- **Docker** (Container runtime for local execution on macOS and Linux workstations; provides isolated, reproducible MS-DIAL and MSFLO execution environments) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC systems; enables unprivileged container execution on SLURM-managed clusters and shared computing facilities) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Containerized peak detection and feature alignment engine for LC-HRMS metabolomics data; first stage of the two-stage pipeline) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial
- **MSFLO** (Containerized annotation and statistical processing module; second stage of the pipeline that processes MS-DIAL-aligned features) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Container image pull and build logs appear in execution.log with no download/layer resolution errors.
- All processes complete with exit code 0 and produce non-empty .tsv feature tables in the `results` directory.
- execution_report.html and execution_timeline.html show expected process DAG (MS-DIAL → MSFLO) without task retries or failures.
- Output feature table schema matches expected metabolomics format: rows = features, columns = samples + m/z + RT + annotation metadata.
- Reproducibility check: identical input data + configuration produces identical output feature tables across separate Nextflow runs (checksums match).

## Limitations

- Container image builds may require 30–60 min on first execution; subsequent runs benefit from layer caching.
- File name special characters (other than underscores) in input .mzML files cause silent process failures; strict naming convention required.
- SLURM CPU overallocation errors occur if `--max_cpus` (not `--cpus`) is not set correctly in the HiPerGator.config; per-process resource requests must not exceed cluster allocation.
- Only .mzML and .abf input formats supported; other raw MS formats (e.g., .raw, .d) require pre-conversion with ProteoWizard msConvert or Reifycs Abf Converter.
- Reference spectral libraries (ms1_lib.txt, ms2_lib.msp) must be present and correctly formatted; missing or malformed libraries cause downstream annotation to fail silently.

## Evidence

- [readme] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [readme] Nextflow to run MS-DIAL-based analyses reproducibly across local computers, containers, and high-performance computing environments: "It uses Nextflow to run MS-DIAL-based analyses reproducibly across local computers, containers, and high-performance computing environments."
- [other] containerized workflow MS-DIAL -> MSFLO: "containerized workflow MS-DIAL -> MSFLO"
- [readme] Remove the example data and place your raw data files in `data/raw_data/`. The workflow accepts `.mzML` and `.abf` files.: "Remove the example data and place your raw data files in `data/raw_data/`. The workflow accepts `.mzML` and `.abf` files."
- [readme] Docker configuration is defined in `conf/base.config`. High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`.: "Docker configuration is defined in `conf/base.config`. High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`."
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process.: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [readme] Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`."
