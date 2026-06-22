---
name: mzml-metabolomics-data-import
description: 'Use when you have raw LC-HRMS metabolomics data in mzML or ABF format that needs to be processed through a reproducible pipeline. Use this skill when: (1) you have public or proprietary .mzML LC-MS datasets (e.g. from MetaboLights, MassIVE, or PRIDE);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MSFLO
  - Nextflow
  - Docker
  - Singularity
  - MS-DIAL
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

# mzML Metabolomics Data Import

## Summary

Import and validate liquid chromatography–high-resolution mass spectrometry (LC-HRMS) metabolomics data in mzML format into a reproducible containerized Nextflow workflow for downstream processing with MS-DIAL. This skill ensures data integrity and format compliance before peak detection and feature quantification.

## When to use

You have raw LC-HRMS metabolomics data in mzML or ABF format that needs to be processed through a reproducible pipeline. Use this skill when: (1) you have public or proprietary .mzML LC-MS datasets (e.g. from MetaboLights, MassIVE, or PRIDE); (2) you need to standardize data input across local, container, and HPC environments; (3) you require traceability of preprocessing steps and parameter settings before peak detection and metabolite identification.

## When NOT to use

- Input data is already in a processed feature table format (CSV, TSV, or mzTab) rather than raw spectra — use direct feature import instead.
- Raw data is in vendor-specific binary format (.raw, .d) without access to ProteoWizard msConvert for conversion.
- Analysis requires targeted metabolomics with pre-specified transitions (selected reaction monitoring / SRM) rather than untargeted LC-HRMS discovery.

## Inputs

- .mzML files (LC-HRMS metabolomics data)
- .abf files (alternative LC-HRMS format)
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 reference library (ms1_lib.txt)
- MS2 reference library (ms2_lib.msp)

## Outputs

- Validated mzML dataset staged in containerized workflow environment
- Container environment configuration (Docker or Singularity)
- Nextflow execution metadata (workflow version, parameter settings, container info)

## How to apply

Clone the Nextflow4MS-DIAL repository and verify that Nextflow ≥22.10.0 is installed along with either Docker or Singularity (for HPC). Place your .mzML raw data files in the `data/raw_data/` directory. If your data is in an alternative format (e.g. vendor-specific .raw or .d), first convert to .mzML using ProteoWizard msConvert or to .abf using Reifycs Abf Converter. Ensure filenames contain only alphanumeric characters and underscores (no special characters, which cause silent failures). Configure the workflow by placing MS-DIAL parameter file (`msdial_params.txt`), MS-FLO parameter file (`msflo_params.ini`), and reference libraries (`ms1_lib.txt` and `ms2_lib.msp`) in the `data/` folder. Execute the containerized workflow with `nextflow run main.nf -profile docker` (local) or `-profile singularity` (HPC). The workflow automatically detects and ingests all .mzML files in `data/raw_data/`, validates container integrity via Docker or Singularity, and stages data for the MS-DIAL → MSFLO processing pipeline.

## Related tools

- **Nextflow** (Workflow orchestration and execution engine across local, container, and HPC environments) — https://www.nextflow.io/
- **Docker** (Container runtime for reproducible local and cloud execution of MS-DIAL workflow) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC environments, enabling MS-DIAL execution without elevated privileges) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Untargeted peak detection and feature quantification from mzML spectra)
- **MSFLO** (Downstream metabolite identification and statistical feature filtering after MS-DIAL)
- **ProteoWizard msConvert** (Format conversion from vendor-specific raw formats to mzML for workflow input) — https://proteowizard.sourceforge.io/download.html
- **Reifycs Abf Converter** (Format conversion from vendor formats to .abf (alternative to mzML)) — https://www.reifycs.com/AbfConverter/

## Examples

```
git clone https://github.com/Nextflow4Metabolomics/nextflow4ms-dial.git && cd nextflow4ms-dial && cp /path/to/your/data/*.mzML data/raw_data/ && nextflow run main.nf -profile docker
```

## Evaluation signals

- All .mzML files in `data/raw_data/` are detected and registered by Nextflow without silent failures due to special characters in filenames.
- Container image (Docker or Singularity) is successfully built and pulls required MS-DIAL and MSFLO versions without errors.
- Nextflow execution log (`execution.log`) shows successful staging of input data and correct parameter file registration before the first MS-DIAL process begins.
- Execution report (`execution_report.html`) confirms all input files were processed (workflow completion status); no files are skipped due to format or naming issues.
- MS-DIAL and MSFLO output files (`.msdial`, `.tsv`) appear in the `results/` directory after workflow completion, confirming data was successfully ingested and processed.

## Limitations

- Filenames containing special characters (e.g., spaces, dashes, special symbols) cause silent failures and processes to be skipped; only alphanumeric characters and underscores are safe.
- Initial release of Nextflow4MS-DIAL lacks explicit version information for MS-DIAL or MSFLO tools within the workflow configuration, making version tracking and reproducibility auditing difficult.
- No discussion section or detailed validation report is provided in the primary documentation; reproducibility testing is not formally documented beyond functional test profile.
- Workflow requires pre-conversion of non-mzML/non-abf formats (e.g. .raw, .d) using external tools (ProteoWizard, Reifycs) with no built-in conversion step.
- HPC configuration is documented only for HiPerGator (University of Florida's cluster); generalization to other SLURM-based HPC systems or non-SLURM schedulers requires manual configuration adjustment.

## Evidence

- [readme] The workflow accepts `.mzML` and `.abf` files and requires conversion from other formats.: "The workflow accepts `.mzML` and `.abf` files. Convert other raw data formats to `.mzML` with ProteoWizard msConvert, or create `.abf` files with Reifycs Abf Converter."
- [readme] Data placement and configuration file requirements for workflow input.: "Remove the example data and place your raw data files in `data/raw_data/`. Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and"
- [readme] Container backend support for reproducibility across environments.: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [readme] Container backend configuration and environment selection.: "Use the `docker` profile for local execution and the `singularity` profile for high-performance computing environments"
- [readme] Known failure mode: special characters in filenames.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [other] Data input format and validation objective.: "Enabling processing .mzML LC-MS metabolomics data with containerized workflow MS-DIAL -> MSFLO"
