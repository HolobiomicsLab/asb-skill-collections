---
name: lc-hrms-data-preprocessing-pipeline
description: Use when you have raw LC-HRMS metabolomics data in .mzML or .abf format and need to perform peak detection, feature alignment, and metabolite annotation in a reproducible, containerized environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
  - ProteoWizard msConvert
  - Reifycs Abf Converter
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lc-hrms-data-preprocessing-pipeline

## Summary

A reproducible Nextflow workflow for processing Liquid Chromatography-High Resolution Mass Spectrometry (LC-HRMS) metabolomics data through containerized MS-DIAL peak detection and feature identification followed by MSFLO annotation. The workflow executes sequentially on .mzML or .abf raw data files and outputs annotated feature tables suitable for downstream statistical analysis.

## When to use

You have raw LC-HRMS metabolomics data in .mzML or .abf format and need to perform peak detection, feature alignment, and metabolite annotation in a reproducible, containerized environment. Use this workflow when you require consistent results across local machines, HPC clusters, or cloud systems, or when your analysis pipeline must be portable across macOS and Linux platforms.

## When NOT to use

- Your input data is not in .mzML or .abf format and cannot be converted with ProteoWizard msConvert or Reifycs Abf Converter.
- You already have processed feature tables or aligned peak matrices and need only annotation or statistical analysis.
- Your analysis environment cannot support containerization (Docker or Singularity) and you lack the ability to install or configure them.

## Inputs

- .mzML files (Liquid Chromatography-Mass Spectrometry raw data format)
- .abf files (proprietary LC-MS raw data format)
- msdial_params.txt (MS-DIAL configuration file)
- msflo_params.ini (MS-FLO configuration file)
- ms1_lib.txt (MS1 spectral reference library)
- ms2_lib.msp (MS2 spectral reference library)

## Outputs

- .tsv feature tables (peak detection and quantification results)
- Metabolite annotations and identifications
- Sample metadata and processing logs
- execution_report.html (runtime and resource usage summary)
- execution_timeline.html (per-process execution timeline)

## How to apply

Install Nextflow ≥22.10.0 and either Docker or Singularity. Prepare your raw .mzML or .abf files in the `data/raw_data/` directory. Provide MS-DIAL configuration file (`msdial_params.txt`) and MS-FLO configuration file (`msflo_params.ini`) in the `data/` folder, along with MS1 and MS2 spectral libraries (`ms1_lib.txt` and `ms2_lib.msp`). Execute the pipeline using `nextflow run main.nf -profile docker` (or `-profile singularity` for HPC). The workflow internally stages .mzML inputs into the Nextflow work directory, executes MS-DIAL for peak detection and feature identification within a containerized environment, pipes outputs directly to MSFLO for metabolite annotation, and collects final feature tables and metadata to the `results` directory. Confirm that special characters are not used in input file names (underscores are safe) and verify resource allocation using `--max_cpus` rather than `--cpus` when running on HPC systems.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages sequential execution of MS-DIAL and MSFLO within containerized environments across local, HPC, and cloud platforms) — https://www.nextflow.io/
- **MS-DIAL** (Peak detection, feature identification, and chromatographic alignment of LC-HRMS data; executed first in the pipeline on .mzML inputs)
- **MSFLO** (Metabolite identification and annotation of MS-DIAL detected features using MS1 and MS2 spectral libraries; executed sequentially after MS-DIAL)
- **Docker** (Containerization runtime for local execution and portability of the complete workflow across macOS and Linux systems) — https://docs.docker.com/engine/installation/
- **Singularity** (Alternative containerization runtime optimized for high-performance computing systems (e.g., HiPerGator) as an alternative to Docker) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Optional utility to convert vendor-specific raw data formats to .mzML for compatibility with the workflow) — https://proteowizard.sourceforge.io/download.html
- **Reifycs Abf Converter** (Optional utility to convert vendor-specific raw data formats to .abf for compatibility with the workflow) — https://www.reifycs.com/AbfConverter/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Execution completes without errors; check `execution.log` for successful workflow progress and process-level completion messages.
- All output files (.tsv feature tables, metadata, HTML reports) are present in the `results/` directory with non-zero file sizes.
- The `execution_report.html` shows realistic resource usage (CPU, memory, runtime) consistent with sample size and computational complexity.
- No special characters appear in input file names; if workflow fails with cryptic errors, verify filenames contain only alphanumeric characters and underscores.
- Feature table structure matches expected MS-DIAL output schema (columns for m/z, retention time, peak intensity/area; rows for detected features), and annotations include metabolite names or identifiers populated by MSFLO from spectral libraries.

## Limitations

- The initial release (as indicated in the README) does not include explicit discussion or validation of reproducibility across independent datasets; testing has been performed on macOS 13.5.1 and Red Hat Enterprise Linux 8.8 only.
- MS-DIAL and MSFLO tool versions are not explicitly specified in the workflow; version pinning or compatibility constraints are not documented, which may affect reproducibility if tool versions change.
- File naming is strict: special characters in input filenames cause silent or cryptic pipeline failures; only alphanumeric characters and underscores are safe.
- The workflow requires manual configuration file preparation (msdial_params.txt, msflo_params.ini) and spectral library curation (ms1_lib.txt, ms2_lib.msp); errors in these configuration files will not be caught until runtime.
- Resource allocation on HPC systems requires careful use of `--max_cpus` (not `--cpus`) in configuration; incorrect CPU specification will cause SLURM job failures.

## Evidence

- [readme] A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL.: "**A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL.**"
- [other] The workflow processes .mzML files through MS-DIAL followed by MSFLO with containerization support.: "containerized workflow MS-DIAL -> MSFLO"
- [readme] Containerization support for both Docker and Singularity runtimes.: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] Sequential pipeline stages from raw data input through MS-DIAL to MSFLO output.: "Execute MS-DIAL processing module on .mzML inputs within containerized environment, generating intermediate peak-detection and feature-identification outputs. 4. Pipe MS-DIAL outputs directly to"
- [readme] Installation and execution requirements for running the workflow.: "Install Java 11 or later. The workflow was developed with Java 11.0.8. 2. Install [Nextflow](https://nf-co.re/usage/installation). 3. Install [Docker](https://docs.docker.com/engine/installation/)"
- [readme] Input format specification and conversion tools for data preparation.: "The workflow accepts `.mzML` and `.abf` files. 3. Convert other raw data formats to `.mzML` with [ProteoWizard msConvert]"
- [readme] Required configuration files for MS-DIAL and MS-FLO customization.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`"
- [readme] Documented failure mode related to special characters in file names.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] HPC resource allocation configuration requirement.: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [readme] Publication of the workflow with concrete validation and testing.: "Du X, Dobrowolski A, Brochhausen M, Garrett TJ, Hogan WR, Lemas DJ. Nextflow4MS-DIAL: A Reproducible Nextflow-Based Workflow"
