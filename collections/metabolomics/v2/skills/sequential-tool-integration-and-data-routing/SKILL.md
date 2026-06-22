---
name: sequential-tool-integration-and-data-routing
description: Use when when you have raw LC-HRMS metabolomics data in .mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
  - ProteoWizard msConvert
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

# Sequential Tool Integration and Data Routing

## Summary

Construct a containerized Nextflow pipeline that chains multiple LC-MS metabolomics tools (MS-DIAL → MSFLO) in strict sequential order, routing intermediate outputs from one tool directly into the next within a single orchestrated workflow. This skill ensures reproducible, portable execution across local machines and high-performance computing environments via Docker or Singularity containerization.

## When to use

When you have raw LC-HRMS metabolomics data in .mzML or .abf format that requires sequential peak detection and feature identification followed by statistical annotation, and you need to enforce deterministic tool chaining with version-controlled containerization to make results reproducible across different computational platforms (macOS, Linux, HPC clusters).

## When NOT to use

- Input data is already in processed feature-table format (e.g., peak-picked CSV or aligned feature matrix); the workflow targets raw .mzML/.abf chromatographic data.
- You require non-sequential or parallel execution of peak detection and annotation; this skill enforces strict sequential piping of MS-DIAL → MSFLO.
- Your raw data is in vendor-specific formats other than .mzML or .abf without prior conversion using ProteoWizard msConvert or Reifycs Abf Converter.

## Inputs

- .mzML LC-HRMS raw data files
- .abf LC-HRMS raw data files (after conversion)
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 spectral library (ms1_lib.txt)
- MS2 spectral library (ms2_lib.msp)

## Outputs

- MS-DIAL intermediate peak-detection and feature-identification outputs
- MSFLO final feature tables (converted .msdial files as .tsv)
- Metabolite annotations and metadata
- execution_report.html (workflow runtime and resource summary)
- execution_timeline.html (per-process execution timeline)
- execution.log (detailed process-level and metadata logs)

## How to apply

Install Nextflow ≥22.10.0 and select a containerization backend (Docker for local execution or Singularity for HPC). Stage raw .mzML input files into the Nextflow work directory and validate file integrity. Define a Nextflow workflow with explicit process dependencies: the MS-DIAL process reads .mzML inputs and produces intermediate peak-detection and feature-identification outputs; pipe those outputs directly as inputs to the MSFLO process within the same DAG, ensuring both tools run sequentially in the containerized environment. Configure MS-DIAL parameters (msdial_params.txt) and MS-FLO parameters (msflo_params.ini) in the `data/` folder, include required MS1 and MS2 spectral libraries (ms1_lib.txt and ms2_lib.msp), and execute the pipeline using the appropriate profile (`-profile docker` or `-profile singularity`). Monitor execution logs and timeline reports to confirm sequential execution and resource utilization.

## Related tools

- **Nextflow** (Orchestrates containerized sequential pipeline execution, manages process dependencies, and enables reproducible workflow runs across local and HPC environments) — https://www.nextflow.io/
- **MS-DIAL** (Performs peak detection, feature identification, and chromatogram alignment on .mzML LC-HRMS input files within containerized process)
- **MSFLO** (Consumes MS-DIAL feature outputs and performs statistical annotation and filtering to produce final annotated feature tables)
- **Docker** (Provides containerization backend for local execution, ensuring consistent tool environments across macOS and Linux systems) — https://docs.docker.com/engine/installation/
- **Singularity** (Provides containerization backend for HPC systems, enabling portable execution on resource-managed clusters with constrained privileges) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Converts vendor-specific raw LC-MS data formats to .mzML for input into the pipeline) — https://proteowizard.sourceforge.io/download.html

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Execution log confirms both MS-DIAL and MSFLO processes completed without error, with no intermediate file I/O failures or format mismatches.
- execution_timeline.html shows MS-DIAL process completion before MSFLO process initiation, confirming strict sequential execution (no overlap).
- MSFLO final outputs are present in the results directory with expected file extensions (.tsv for feature tables) and non-empty content matching schema of input MS-DIAL outputs.
- execution_report.html indicates successful containerization (Docker or Singularity image ID logged) and total runtime consistent with sequential processing (not parallel speedup artifacts).
- No special characters in input file names; underscores are present and process completion is not blocked by unexpected naming errors.

## Limitations

- Initial release lacks detailed methodology discussion and explicit reproducibility validation or testing against external benchmark datasets.
- No version information is provided for MS-DIAL or MSFLO tools; users must ensure compatibility between containerized tool versions and configuration parameter syntax.
- Pipeline configuration is sensitive to correct placement of msdial_params.txt, msflo_params.ini, ms1_lib.txt, and ms2_lib.msp files; missing or misconfigured files will cause silent failures or incorrect annotations.
- Special characters in filenames (other than underscores) can trigger unexpected errors; naming conventions must be strictly enforced upstream.
- Testing was limited to macOS 13.5.1 (Intel i7, 16 GB RAM) and Red Hat Enterprise Linux 8.8 (HiPerGator); performance on other architectures or resource-constrained systems is unvalidated.

## Evidence

- [other] The workflow implements a containerized sequential pipeline that processes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO: "The workflow implements a containerized sequential pipeline that processes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container"
- [other] Execute MS-DIAL processing module on .mzML inputs within containerized environment, then pipe outputs directly to MSFLO: "Execute MS-DIAL processing module on .mzML inputs within containerized environment, generating intermediate peak-detection and feature-identification outputs. 4. Pipe MS-DIAL outputs directly to"
- [other] Initialize Nextflow ≥22.10.0 runtime environment with containerization backend selection: "Initialize Nextflow ≥22.10.0 runtime environment with containerization backend selection (Docker or Singularity)."
- [readme] Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [readme] Add the MS-DIAL and MS-FLO configuration files to the data/ folder and name them msdial_params.txt and msflo_params.ini: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`. Example configuration files are available in"
- [readme] To avoid unexpected errors, do not use special characters in file names: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] execution_timeline.html shows the execution timeline for each process: "`execution_timeline.html` shows the execution timeline for each process."
