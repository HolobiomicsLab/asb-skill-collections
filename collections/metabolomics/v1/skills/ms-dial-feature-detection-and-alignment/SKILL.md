---
name: ms-dial-feature-detection-and-alignment
description: Use when when you have raw LC-HRMS metabolomics data in .mzML or .abf format and need to perform untargeted feature detection with chromatographic alignment across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MS-DIAL
  - MSFLO
  - Nextflow
  - Docker
  - Singularity
  - ProteoWizard msConvert
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL.
- containerized workflow MS-DIAL -> MSFLO
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial
schema_version: 0.2.0
---

# ms-dial-feature-detection-and-alignment

## Summary

Feature detection and chromatogram alignment of LC-HRMS metabolomics data using the MS-DIAL tool within a containerized, reproducible Nextflow workflow. This skill enables systematic peak detection, retention time alignment, and generation of annotated feature tables from raw .mzML LC-MS files.

## When to use

When you have raw LC-HRMS metabolomics data in .mzML or .abf format and need to perform untargeted feature detection with chromatographic alignment across multiple samples. Use this skill as the core processing step before metabolite identification or downstream statistical analysis of feature intensities.

## When NOT to use

- Input data is already in processed feature table format (e.g., CSV with aligned m/z × sample intensity matrix) — feature detection and alignment have already been performed.
- Raw data are in non-standard formats (e.g., vendor-specific .raw files without conversion to .mzML or .abf) — ProteoWizard msConvert or Reifycs Abf Converter must be applied first.
- Analysis scope is limited to targeted metabolite quantification with pre-defined m/z and retention time windows — consider simpler targeted extraction methods instead of untargeted feature detection.

## Inputs

- Raw LC-HRMS data files (.mzML or .abf format)
- MS-DIAL configuration file (msdial_params.txt)
- MS1 reference library (.txt format)
- MS2 reference library (.msp format)

## Outputs

- MS-DIAL feature tables (.msdial files, converted to .tsv)
- Aligned data matrices with m/z, retention time, and intensity values
- Processed annotations linked to reference libraries
- Execution logs and runtime reports (execution_report.html, execution_timeline.html)

## How to apply

Deploy the Nextflow4MS-DIAL workflow with containerized MS-DIAL execution (Docker or Singularity backend) on your .mzML input files. Configure MS-DIAL parameters via the msdial_params.txt configuration file placed in the data/ folder, specifying peak detection sensitivity, mass tolerance, and retention time alignment window. Execute the workflow using `nextflow run main.nf -profile docker` (or `-profile singularity` for HPC), which orchestrates the MS-DIAL → MSFLO pipeline. Monitor execution logs in execution.log and verify that all samples progress through peak detection and alignment stages without error. Validate output by confirming presence of .msdial result files (converted to .tsv format for accessibility) in the results directory, checking that feature tables contain aligned m/z and retention time values with intensity measurements across all samples.

## Related tools

- **MS-DIAL** (Core feature detection and chromatogram alignment engine; performs peak picking, retention time alignment, and annotation matching)
- **MSFLO** (Post-processing and feature list refinement following MS-DIAL output)
- **Nextflow** (Workflow orchestration engine; manages containerized execution of MS-DIAL pipeline across local and HPC environments) — https://www.nextflow.io/
- **Docker** (Container backend for reproducible local execution of MS-DIAL and MSFLO tools) — https://docs.docker.com/engine/installation/
- **Singularity** (Alternative container backend optimized for high-performance computing environments) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Optional upstream tool for converting vendor-specific raw mass spectrometry formats to .mzML) — https://proteowizard.sourceforge.io/download.html

## Examples

```
nextflow run main.nf -profile docker
```

## Evaluation signals

- All samples complete peak detection and alignment stages without error, confirmed by `nextflow run` exit status 0 and absence of error entries in execution.log
- Output .msdial/.tsv files are present in the results directory for each input sample, with non-zero file sizes indicating successful feature detection
- Feature tables contain expected columns: m/z values, retention time (in minutes), intensity measurements across all samples, and aligned feature IDs consistent across samples
- Execution timeline (execution_timeline.html) shows MS-DIAL process completion for all samples without process failures or timeouts
- Example outputs from the Li et al. (2018) 10-sample dataset (5 per group) match the reference outputs provided in the repository's results folder in terms of feature count and annotation distribution

## Limitations

- Special characters in input file names (except underscores) may cause unexpected errors due to Nextflow parameter parsing; only alphanumeric characters and underscores are safe.
- No explicit version information is provided for MS-DIAL or MSFLO within the workflow documentation; reproducibility relies on pinned container image versions rather than tool version specifications.
- The workflow has been tested on macOS 13.5.1 and Red Hat Enterprise Linux 8.8 (HiPerGator); behavior on other Linux distributions or older macOS versions is not documented.
- Custom MS1 and MS2 reference libraries must be manually prepared and placed in the data/ folder; the workflow does not automatically download or validate library formats.
- CPU allocation in HPC environments must use `--max_cpus` configuration; using `--cpus` instead may result in Slurm resource allocation conflicts.

## Evidence

- [readme] Nextflow4MS-DIAL is a bioinformatics workflow for Liquid Chromatography-High Resolution Mass Spectrometry (LC-HRMS) metabolomics data processing.: "Nextflow4MS-DIAL is a bioinformatics workflow for Liquid Chromatography-High Resolution Mass Spectrometry (LC-HRMS) metabolomics data"
- [other] Feature detection and chromatogram alignment are core operations performed by the MS-DIAL tool within the workflow.: "peak detection [EDAM:operation_3215], chromatogram alignment [EDAM:operation_3628], metabolite identification [EDAM:operation_3803]"
- [readme] The workflow supports containerized execution via Docker and Singularity for reproducibility.: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
- [readme] MS-DIAL parameters are user-configurable via a dedicated configuration file.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`."
- [readme] Output feature tables are generated in .tsv format for accessibility.: "The file extensions for produced `.msdial` files have been changed to `.tsv` so the files can be opened in spreadsheet software"
- [readme] Reference MS1 and MS2 libraries are required inputs for annotation.: "Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`."
- [readme] Input format acceptance includes .mzML and .abf files.: "The workflow accepts `.mzML` and `.abf` files."
- [readme] File naming conventions must avoid special characters to prevent errors.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
