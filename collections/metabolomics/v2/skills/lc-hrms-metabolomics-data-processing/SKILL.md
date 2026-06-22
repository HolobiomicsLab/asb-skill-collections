---
name: lc-hrms-metabolomics-data-processing
description: Use when you have LC-HRMS raw data files (.mzML or .abf format) from metabolomics experiments and need to extract, align, and annotate features in a reproducible manner across multiple computational environments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
  - ProteoWizard msConvert
  - Reifycs Abf Converter
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

# LC-HRMS metabolomics data processing

## Summary

A containerized Nextflow workflow for reproducible processing of liquid chromatography–high resolution mass spectrometry (LC-HRMS) metabolomics data using MS-DIAL peak detection, alignment, and annotation. The workflow automates feature extraction, quantification, and metabolite identification from .mzML or .abf raw data files across local, containerized, and HPC environments.

## When to use

You have LC-HRMS raw data files (.mzML or .abf format) from metabolomics experiments and need to extract, align, and annotate features in a reproducible manner across multiple computational environments. This skill is appropriate when you require containerized, version-controlled processing with configurable MS-DIAL and MS-FLO parameters.

## When NOT to use

- Input data are already in aligned feature table format — skip directly to downstream statistical or multivariate analysis.
- Raw mass spectrometry data are in vendor-specific formats (.raw, .d) that have not been converted to .mzML or .abf — convert first using ProteoWizard or vendor-supplied tools.
- You require custom peak detection algorithms or parameters not supported by MS-DIAL and MS-FLO — consider alternative metabolomics pipelines.

## Inputs

- .mzML raw LC-HRMS data files
- .abf raw LC-HRMS data files
- MS1 spectral library (ms1_lib.txt)
- MS2 spectral library (ms2_lib.msp)
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)

## Outputs

- Feature table (.tsv)
- Aligned data matrix (.tsv)
- Processed annotations
- .msdial files (converted to .tsv for spreadsheet software compatibility)
- Execution report (execution_report.html)
- Execution timeline (execution_timeline.html)
- Execution log (logs/execution.log)

## How to apply

Clone the Nextflow4MS-DIAL repository and install Nextflow (≥22.10.0), Java 11 or later, and either Docker or Singularity. Prepare your .mzML or .abf raw data files in the data/raw_data/ directory; if needed, convert other formats using ProteoWizard msConvert or Reifycs Abf Converter. Add MS1 and MS2 spectral libraries (named ms1_lib.txt and ms2_lib.msp) and MS-DIAL and MS-FLO configuration files (msdial_params.txt and msflo_params.ini) to the data/ folder. Configure the workflow by verifying the reference file and container backend settings in conf/base.config (Docker) or conf/HiPerGator.config (Singularity/HPC). Execute the containerized MS-DIAL → MSFLO pipeline using `nextflow run main.nf -profile docker` (or `singularity` for HPC) and monitor the execution logs and HTML reports (execution_report.html, execution_timeline.html) to verify all pipeline stages complete without error.

## Related tools

- **Nextflow** (Workflow orchestration engine for reproducible pipeline execution across local, container, and HPC environments) — https://www.nextflow.io/
- **MS-DIAL** (Peak detection, alignment, and feature annotation in the containerized MS-DIAL → MSFLO pipeline)
- **MSFLO** (Post-processing and additional quantification for MS-DIAL output features)
- **Docker** (Container backend for reproducible local execution of the workflow) — https://docs.docker.com/engine/installation/
- **Singularity** (Container backend for high-performance computing environments and cluster execution) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Utility for converting vendor-specific raw data formats to .mzML) — https://proteowizard.sourceforge.io/download.html
- **Reifycs Abf Converter** (Utility for creating .abf format files from other raw data formats) — https://www.reifycs.com/AbfConverter/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- All pipeline processes complete without error; execution_report.html shows 100% completion and no failed stages.
- Expected output files are present in the results directory: feature tables and aligned data matrices with non-empty content.
- Output feature tables contain a reasonable number of detected features (relative to input sample complexity and MS-DIAL parameters); feature count should be non-zero and consistent with metabolomics studies on similar sample types.
- Processed annotations include metabolite identifications linked to MS1 and MS2 spectral libraries; annotation coverage should reflect the specificity of the provided libraries.
- Execution log (logs/execution.log) contains no error.txt or warning messages related to container image pull failures, missing configuration files, or incompatible file formats.

## Limitations

- File names should not contain special characters (underscores are safe); special characters can cause unexpected pipeline errors.
- Process CPU allocation must use `--max_cpus` (not `--cpus`) in configuration files; incorrect specification can cause Slurm job failures on HPC systems.
- MS-DIAL and MSFLO tool versions are not explicitly specified in the containerized workflow; version pinning is handled internally by the Docker/Singularity image.
- The workflow has been validated on macOS 13.5.1 and Red Hat Enterprise Linux 8.8; behavior on other operating systems or Linux distributions is not documented.
- Raw data format support is limited to .mzML and .abf; other formats require prior conversion using external tools.

## Evidence

- [readme] Nextflow workflow for LC-HRMS metabolomics data processing: "A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL."
- [other] Containerized MS-DIAL to MSFLO workflow: "containerized workflow MS-DIAL -> MSFLO"
- [readme] Docker and Singularity container support: "Both Docker and Singularity (for high-performance computing) are supported"
- [readme] Input data format specifications: "The workflow accepts `.mzML` and `.abf` files."
- [readme] Configuration file and library file requirements: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`. Example configuration files are available in"
- [readme] Special character restriction in file names: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [methods] Expected output file types: "Validate presence and integrity of expected output files (feature tables, aligned data matrices, processed annotations) in the designated output directory."
- [readme] Nextflow version requirement: "[![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A522.10.0-brightgreen.svg)](https://www.nextflow.io/)"
