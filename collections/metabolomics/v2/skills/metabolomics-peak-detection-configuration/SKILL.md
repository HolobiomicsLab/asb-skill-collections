---
name: metabolomics-peak-detection-configuration
description: Use when when preparing to process raw LC-HRMS metabolomics data (.mzML
  or .abf files) with MS-DIAL within a Nextflow pipeline, before executing peak detection
  and chromatogram alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSFLO
  - MS-DIAL
  - Nextflow
  - Docker
  - Singularity
  - ProteoWizard msConvert
  - Reifycs Abf Converter
  techniques:
  - LC-MS
  - CE-MS
  license_tier: open
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

# metabolomics-peak-detection-configuration

## Summary

Configuration and parameterization of MS-DIAL peak detection for LC-HRMS metabolomics data processing. This skill involves setting up MS-DIAL parameters and reference libraries to enable reproducible feature detection, quantification, and metabolite identification from .mzML LC-MS files within a containerized Nextflow workflow.

## When to use

When preparing to process raw LC-HRMS metabolomics data (.mzML or .abf files) with MS-DIAL within a Nextflow pipeline, before executing peak detection and chromatogram alignment. Specifically indicated when you have mass spectrometry reference libraries (MS1 and MS2) available and need to configure parameter files for consistent, reproducible feature extraction across sample batches.

## When NOT to use

- Input data is already in feature table format (CSV/TSV with m/z, retention time, abundance) — skip directly to statistical analysis or metabolite annotation.
- No reference spectral libraries (MS1/MS2) are available — MS-DIAL identification step will fail; consider using untargeted feature detection workflows or obtain appropriate library data first.
- Raw data is in vendor-specific binary formats (.raw, .d) that have not been converted to .mzML — first convert using ProteoWizard msConvert or Reifycs Abf Converter.

## Inputs

- .mzML files (raw LC-HRMS data)
- .abf files (raw LC-HRMS data, alternative format)
- msdial_params.txt (MS-DIAL configuration file)
- msflo_params.ini (MS-FLO configuration file)
- ms1_lib.txt (MS1 spectral reference library)
- ms2_lib.msp (MS2 spectral reference library)

## Outputs

- .msdial files (peak-detected feature tables)
- .tsv files (MS-DIAL output in spreadsheet format)
- Feature abundance tables with metabolite annotations
- Aligned chromatogram and retention time data

## How to apply

Place MS-DIAL configuration parameters in a file named `msdial_params.txt` and MS-FLO parameters in `msflo_params.ini` within the `data/` folder. Add MS1 and MS2 spectral reference libraries as `ms1_lib.txt` and `ms2_lib.msp` respectively in the same directory. Configure the reference file path and MS-DIAL settings in `conf/base.config` to match your mass spectrometry instrument and metabolomics experiment design (e.g., ion mode, MS/MS collision energy, alignment tolerance). For high-performance computing environments, use `conf/HiPerGator.config` to set Singularity container configuration and resource constraints (e.g., `--max_cpus` to specify available CPUs per process). Validate parameter files against example configurations provided in `functional_test/sample_data/` before running on production data.

## Related tools

- **MS-DIAL** (Primary peak detection and feature identification engine; processes .mzML inputs to generate feature tables with m/z, retention time, and abundance values; matches detected features against MS1 and MS2 reference libraries for metabolite annotation.) — https://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/
- **MSFLO** (Post-processing and statistical filtering of MS-DIAL outputs; receives peak-detected feature tables and applies filtering criteria specified in msflo_params.ini to refine feature quality and remove noise.)
- **Nextflow** (Workflow orchestration and containerization runtime (≥22.10.0); manages pipeline stages, data flow between MS-DIAL and MSFLO modules, and resource allocation across execution environments (local, Docker, Singularity, HPC).) — https://www.nextflow.io/
- **Docker** (Container runtime for local execution; encapsulates MS-DIAL, MSFLO, and dependencies to ensure reproducibility and portability across macOS and Linux systems.) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for high-performance computing environments (e.g., HiPerGator); alternative to Docker with improved integration on shared HPC systems running RHEL 8.8 or similar.) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Raw data format conversion tool; converts vendor-specific binary formats (.raw, .d) to .mzML for Nextflow4MS-DIAL pipeline input.) — https://proteowizard.sourceforge.io/download.html
- **Reifycs Abf Converter** (Raw data format conversion tool; generates .abf files from vendor formats as an alternative input format to .mzML for MS-DIAL processing.) — https://www.reifycs.com/AbfConverter/

## Examples

```
nextflow run main.nf -profile docker
```

## Evaluation signals

- MS-DIAL configuration file (msdial_params.txt) is syntactically valid and all parameter keys match MS-DIAL's expected schema; reference library paths resolve correctly to accessible MS1 and MS2 files.
- Execution report (`execution_report.html`) shows all pipeline processes completed without error; no processes are marked as 'NOT RUN' due to missing or malformed configuration.
- Output .msdial/.tsv feature tables contain non-empty columns for m/z, retention time, peak intensity, and metabolite annotations; row count is consistent with expected sample count and peak complexity.
- Retention time alignment across samples is visually consistent (e.g., same metabolite features appear at similar retention times across replicates); no unexplained retention time shifts > expected instrumental drift (~2–5 min for LC-HRMS).
- Feature abundance values are numeric and non-zero for at least 90% of expected metabolites; blank sample feature counts are significantly lower than treatment samples (indicating successful background discrimination).

## Limitations

- No explicit statement of reproducibility validation or testing framework provided; initial release status means parameter tuning and edge-case robustness may require user testing and community feedback.
- No version information provided for MS-DIAL or MSFLO tools within the configuration; users must independently verify tool version compatibility with Nextflow ≥22.10.0 and each other.
- Configuration process requires manual file naming convention (msdial_params.txt, msflo_params.ini, ms1_lib.txt, ms2_lib.msp) and exact folder structure (data/ subdirectory); deviation from conventions will cause pipeline failure with unclear error messages.
- Special characters in file names cause pipeline failures; only underscores are documented as safe for naming raw data files and configuration parameters.
- HPC execution is tested only on University of Florida's HiPerGator system; portability to other Slurm-based clusters or different batch schedulers is not documented.

## Evidence

- [readme] Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`."
- [readme] Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`.: "Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`."
- [readme] Before processing your own data, confirm that the reference file in `conf/base.config` and the MS-DIAL configuration file are set correctly.: "Before processing your own data, confirm that the reference file in `conf/base.config` and the MS-DIAL configuration file are set correctly."
- [other] Execute MS-DIAL processing module on .mzML inputs within containerized environment, generating intermediate peak-detection and feature-identification outputs.: "Execute MS-DIAL processing module on .mzML inputs within containerized environment, generating intermediate peak-detection and feature-identification outputs."
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`.: "High-performance computing and Singularity configuration is defined in `conf/HiPerGator.config`."
- [readme] The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce.: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
