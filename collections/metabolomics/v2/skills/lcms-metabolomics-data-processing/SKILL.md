---
name: lcms-metabolomics-data-processing
description: Use when you have raw LC-HRMS metabolomics data in .mzML or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - Docker
  - Nextflow
  - MS-DIAL
  - MSFLO
  - Singularity
  - ProteoWizard msConvert
  techniques:
  - LC-MS
  - CE-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-metabolomics-data-processing

## Summary

Execute a containerized Nextflow workflow to process liquid chromatography–high-resolution mass spectrometry (LC-HRMS) metabolomics data from raw .mzML or .abf format through MS-DIAL feature detection and peak alignment, followed by MSFLO annotation and statistical analysis. This skill ensures reproducible metabolomics pipelines across local, containerized, and high-performance computing environments.

## When to use

You have raw LC-HRMS metabolomics data in .mzML or .abf format and need to perform feature detection, chromatographic alignment, metabolite annotation, and statistical processing in a reproducible, portable manner across macOS, Linux, or HPC systems without installing MS-DIAL or MSFLO natively.

## When NOT to use

- Input data is already a processed feature table or abundance matrix (use downstream statistical analysis or visualization skills instead).
- Raw mass spectrometry data is in proprietary formats other than .mzML or .abf without prior conversion (convert using ProteoWizard msConvert or Reifycs Abf Converter first).
- Execution environment lacks Docker or Singularity container runtime and native MS-DIAL/MSFLO installation is not available.

## Inputs

- .mzML or .abf raw LC-HRMS data files
- MS-DIAL parameter configuration file (msdial_params.txt)
- MS-FLO parameter configuration file (msflo_params.ini)
- MS1 reference library (ms1_lib.txt)
- MS2 reference library (ms2_lib.msp)

## Outputs

- Feature table (.tsv format, converted from .msdial)
- Aligned and annotated metabolite features
- execution_report.html (workflow runtime and resource summary)
- execution_timeline.html (per-process execution timeline)
- logs/execution.log (process-level logs and metadata)

## How to apply

Clone the Nextflow4MS-DIAL repository and install Nextflow (≥22.10.0) and either Docker (for local execution) or Singularity (for HPC). Prepare raw metabolomics data in the `data/raw_data/` directory as .mzML or .abf files, then place MS-DIAL configuration (`msdial_params.txt`), MS-FLO configuration (`msflo_params.ini`), and reference libraries (`ms1_lib.txt`, `ms2_lib.msp`) in the `data/` folder. Execute the pipeline using `nextflow run main.nf -profile docker` (local) or `-profile singularity` (HPC), which routes .mzML data through the containerized MS-DIAL module for peak detection and alignment, then through MSFLO for annotation. Validate successful completion by checking the `results/` folder for processed feature tables (converted from .msdial to .tsv format) and reviewing execution logs in `logs/execution.log` for resource usage and process-level output.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages parallelization, containerization, and resource allocation across execution platforms) — https://www.nextflow.io/
- **MS-DIAL** (Performs feature detection, peak alignment, and metabolite identification on LC-HRMS data within the containerized workflow)
- **MSFLO** (Conducts annotation and statistical processing of aligned metabolomics features following MS-DIAL output)
- **Docker** (Container runtime for local execution of MS-DIAL and MSFLO in reproducible, isolated environments) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC execution, enabling MS-DIAL and MSFLO deployment on high-performance computing systems) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Converts proprietary vendor mass spectrometry data formats to .mzML for input to the workflow) — https://proteowizard.sourceforge.io/download.html

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Feature table (.tsv) is generated in results/ directory with metabolite identifiers, m/z values, retention time, and abundance columns for all samples.
- execution_report.html documents successful completion with no failed processes and resource usage within allocated limits.
- Processed .msdial files exist and are readable as tab-separated values in spreadsheet software.
- Log files contain no error or exception messages; process-level logs indicate successful container initialization, MS-DIAL peak detection completion, and MSFLO annotation completion.
- Output feature counts and alignment statistics match or exceed expected thresholds based on sample count and library size (e.g., ≥100 aligned features for typical metabolomics samples).

## Limitations

- Raw data filenames must not contain special characters (underscores are safe); special characters may cause unexpected errors during file processing.
- MS-DIAL and MS-FLO parameters must be manually tuned in configuration files for optimal results; default parameters may not suit all metabolomics study designs or ionization modes.
- Singularity container resource allocation requires careful use of `--max_cpus` (not `--cpus`) in HPC configuration to avoid Slurm job rejection due to CPU oversubscription.
- The workflow has been tested on macOS 13.5.1 (Intel) and Red Hat Enterprise Linux 8.8 (HiPerGator HPC); compatibility with other Linux distributions or Apple Silicon macOS is not documented.

## Evidence

- [readme] A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL.: "A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL."
- [readme] Both Docker and Singularity (for high-performance computing) are supported: "Both Docker and Singularity (for high-performance computing) are supported"
- [other] Enabling processing .mzML LC-MS metabolomics data with containerized workflow MS-DIAL -> MSFLO: "Enabling processing .mzML LC-MS metabolomics data with containerized workflow MS-DIAL -> MSFLO"
- [readme] The workflow accepts .mzML and .abf files.: "The workflow accepts `.mzML` and `.abf` files."
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process.: "Use `--max_cpus`, not `--cpus`, in the configuration file to define the CPUs available to each process."
- [readme] Example outputs are stored in the `results` folder. The file extensions for produced `.msdial` files have been changed to `.tsv` so the files can be opened in spreadsheet software such as Microsoft Excel.: "Example outputs are stored in the `results` folder. The file extensions for produced `.msdial` files have been changed to `.tsv`"
- [readme] execution_report.html summarizes workflow runtime and computational resource usage.: "execution_report.html summarizes workflow runtime and computational resource usage."
