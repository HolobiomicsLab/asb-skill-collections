---
name: singularity-container-backend-setup
description: Use when your LC-HRMS metabolomics analysis must run on a high-performance
  computing cluster (e.g., HiPerGator, SLURM-managed systems) that lacks Docker support
  or prefers Singularity for security and portability. You have .mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MSFLO
  - Singularity
  - Nextflow
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- containerized workflow MS-DIAL -> MSFLO
- Both Docker and Singularity (for high-performance computing) are supported
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# singularity-container-backend-setup

## Summary

Configure and execute a Nextflow workflow using Singularity as the container backend for reproducible LC-HRMS metabolomics data processing on high-performance computing environments. This skill enables portable, containerized execution of MS-DIAL and MSFLO tools across HPC systems without Docker.

## When to use

Your LC-HRMS metabolomics analysis must run on a high-performance computing cluster (e.g., HiPerGator, SLURM-managed systems) that lacks Docker support or prefers Singularity for security and portability. You have .mzML or .abf raw MS data files and need reproducible MS-DIAL → MSFLO processing across multiple compute nodes.

## When NOT to use

- Your compute environment has Docker available and no security constraints against it; Docker provides faster image startup than Singularity.
- You are running on a local macOS or Linux workstation with sufficient disk space; the docker profile is simpler to configure for single-machine execution.
- Your raw data is already in a processed feature matrix or aligned peak table format; this skill targets raw .mzML/.abf ingestion only.

## Inputs

- .mzML raw LC-HRMS data files
- .abf raw LC-HRMS data files (alternative format)
- msdial_params.txt configuration file
- msflo_params.ini configuration file
- ms1_lib.txt MS1 spectral library
- ms2_lib.msp MS2 spectral library

## Outputs

- .tsv feature tables (MS-DIAL peak detection results)
- Aligned peak list (MS-DIAL chromatogram alignment output)
- Metabolite identification results (MSFLO annotated compounds)
- execution_report.html (workflow runtime and resource usage summary)
- execution_timeline.html (per-process execution timeline)

## How to apply

Install Nextflow ≥22.10.0 and Singularity on your HPC system. Clone the Nextflow4MS-DIAL repository and place your .mzML input files in the data/raw_data/ directory. Configure MS-DIAL and MS-FLO parameter files (msdial_params.txt and msflo_params.ini) and MS1/MS2 spectral libraries (ms1_lib.txt and ms2_lib.msp) in the data/ folder. Execute the workflow using the singularity profile via `nextflow run main.nf -profile singularity`, which selects the Singularity executor and retrieves pre-built container images for MS-DIAL and MSFLO. Monitor execution via the generated execution_report.html and execution_timeline.html files. Validate completion by checking the results/ directory for .tsv-formatted MS-DIAL and MSFLO output files.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages containerized task execution and resource allocation across HPC environments) — https://www.nextflow.io/
- **Singularity** (Container runtime that isolates MS-DIAL and MSFLO tools with their dependencies and executes them on HPC clusters) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Core metabolomics tool for untargeted peak detection, alignment, and deconvolution of LC-HRMS data)
- **MSFLO** (Post-processing tool for metabolite identification and annotation of MS-DIAL peak features)

## Examples

```
nextflow run main.nf -profile singularity > logs/execution.log
```

## Evaluation signals

- Workflow execution completes without containerization errors; check logs/execution.log for 'completed successfully' or absence of OCI/Singularity runtime exceptions.
- All expected output files are present in results/: .tsv feature tables, aligned peak list, and MSFLO annotations match the number of input .mzML files.
- execution_report.html and execution_timeline.html are generated and show non-zero CPU/memory usage and process completion times for MS-DIAL and MSFLO tasks.
- Output .tsv files are non-empty and contain numeric feature intensities, m/z values, retention times, and metabolite names (if annotated by MSFLO).
- Singularity container image pull/cache messages appear in execution logs, confirming image retrieval before task execution.

## Limitations

- Singularity container images must be pre-built and hosted in a registry (e.g., Docker Hub, Singularity Hub) accessible from the HPC cluster; custom MS-DIAL or MSFLO versions require rebuilding the container.
- MS-DIAL and MSFLO version information is not explicitly specified in the container tags; reproducibility depends on pinning image digests, not just tags, which the current configuration does not enforce.
- HPC configuration (CPU, memory, wall-time limits) is environment-specific; the provided HiPerGator.config example may not transfer directly to other SLURM or non-SLURM schedulers without manual adjustment.
- File naming must avoid special characters (underscores are safe); the workflow does not sanitize input filenames, leading to silent failures or skipped files with problematic names.
- Parameter validation and MS1/MS2 library consistency are not automatically checked; malformed msdial_params.txt or missing/empty library files will cause cryptic downstream MS-DIAL failures.

## Evidence

- [readme] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] Configure Singularity as container backend for HPC: "Configure the Nextflow workflow to use Singularity as the container backend (as an alternative to Docker)."
- [readme] Execute with Singularity profile: "Use the `docker` profile for local execution and the `singularity` profile for high-performance computing environments"
- [readme] Validate outputs in results directory: "Example outputs are stored in the `results` folder. The file extensions for produced `.msdial` files have been changed to `.tsv`"
- [readme] Tested on HiPerGator HPC environment: "HiPerGator, the University of Florida public research computing environment, running Red Hat Enterprise Linux 8.8"
