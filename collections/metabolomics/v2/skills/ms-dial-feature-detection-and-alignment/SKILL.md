---
name: ms-dial-feature-detection-and-alignment
description: Use when when you have raw LC-HRMS data in .mzML or .abf format and need to detect metabolite features (peaks) across multiple samples, align them temporally and by mass-to-charge ratio, and generate a reproducible feature matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - MS-DIAL
  - Docker
  - Nextflow
  - Singularity
  - ProteoWizard msConvert
  - MSFLO
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- A reproducible Nextflow workflow for LC-HRMS metabolomics data processing with MS-DIAL.
- containerized workflow MS-DIAL -> MSFLO
- Both Docker and Singularity (for high-performance computing) are supported
- Both Docker and Singularity (for high-performance computing) are supported.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
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

# MS-DIAL Feature Detection and Alignment

## Summary

MS-DIAL is a containerized module within Nextflow4MS-DIAL that performs peak detection and chromatogram alignment on LC-HRMS metabolomics data in .mzML format. It transforms raw mass spectrometry signals into aligned feature tables suitable for downstream annotation and statistical analysis.

## When to use

When you have raw LC-HRMS data in .mzML or .abf format and need to detect metabolite features (peaks) across multiple samples, align them temporally and by mass-to-charge ratio, and generate a reproducible feature matrix. Use this skill if you are processing untargeted metabolomics cohorts where feature consistency across samples is required for statistical comparison.

## When NOT to use

- Input data is already a processed feature table (e.g., from another feature detection tool); re-running MS-DIAL would introduce redundant processing and potential loss of information.
- Raw data format cannot be converted to .mzML or .abf (e.g., vendor-specific binary formats without ProteoWizard msConvert support).
- Sample set contains highly variable retention time drift or instrument performance issues not corrected in msdial_params.txt; alignment will fail or produce spurious feature merging.

## Inputs

- .mzML LC-HRMS raw data files
- MS-DIAL configuration file (msdial_params.txt)
- MS1 reference library (.txt format, optional)
- MS2 reference library (.msp format, optional)

## Outputs

- Aligned feature table (.msdial/.tsv format)
- Peak detection and alignment metadata
- Aligned m/z and retention time coordinates per feature

## How to apply

Place .mzML LC-MS metabolomics data in the designated input directory (data/raw_data/). Prepare an MS-DIAL configuration file (msdial_params.txt) specifying detection parameters, mass tolerance, retention time windows, and alignment thresholds, and place it in the data/ folder. Execute the containerized MS-DIAL module via Nextflow using either Docker (local) or Singularity (HPC) runtime. MS-DIAL performs peak detection by identifying m/z and retention time signals, then aligns features across all samples using the specified mass and time tolerances. The module outputs aligned feature intensities and metadata. Validate the feature table by checking for: (1) expected feature count matching your sample complexity and ionization mode; (2) no spurious features at system noise thresholds; (3) aligned features present in ≥2 samples (dependent contamination filtering); (4) mass accuracy within specified ppm tolerance.

## Related tools

- **Nextflow** (Workflow orchestration engine that executes MS-DIAL containerized processes across local and HPC environments) — https://www.nextflow.io/
- **Docker** (Container runtime for local execution of containerized MS-DIAL module) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC execution of containerized MS-DIAL module) — https://www.sylabs.io/guides/3.0/user-guide/
- **ProteoWizard msConvert** (Pre-processing tool to convert vendor-specific raw LC-MS formats to .mzML standard format required by MS-DIAL) — https://proteowizard.sourceforge.io/download.html
- **MSFLO** (Downstream annotation module that processes MS-DIAL-aligned features for metabolite identification and statistical filtering)

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log
```

## Evaluation signals

- Feature table row count is consistent with expected metabolite complexity for your biological matrix and ionization mode (e.g., 500–5000 features for untargeted serum metabolomics in ESI±).
- Mass accuracy of detected features falls within the specified ppm tolerance (typically ≤5 ppm for high-resolution instruments).
- Aligned features are present across expected sample replicates and groups; features unique to single samples are minimal and correspond to noise/contaminants at system baseline.
- Retention time alignment produces smooth time axis without gaps or compression artifacts; retention time range matches experimental LC gradient duration.
- Configuration file parameters (msdial_params.txt) are reflected in output metadata; mis-specified tolerance thresholds should produce diagnostic warnings in execution logs.

## Limitations

- MS-DIAL alignment quality depends on accurate msdial_params.txt configuration; suboptimal mass tolerance, retention time window, or peak minimum height settings will produce feature merging, fragmentation, or noise inflation.
- Raw data filenames should not contain special characters; only underscores are safe. Files with hyphens, spaces, or other symbols may cause workflow errors.
- Input data must be in .mzML or .abf format; other vendor formats (Thermo .raw, Agilent .d, Waters .raw) require prior conversion with ProteoWizard msConvert.
- Workflow has been validated on macOS 13.5.1 and Red Hat Enterprise Linux 8.8; behavior on other OS versions or configurations is not documented.
- MS-DIAL configuration files and reference libraries (MS1, MS2) must be manually prepared and placed in data/ folder; no automatic parameter optimization is performed.

## Evidence

- [other] containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO: "Nextflow4MS-DIAL implements a containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container runtimes."
- [other] peak detection and alignment performed by containerized MS-DIAL module: "The pipeline routes the data through the containerized MS-DIAL module for feature detection and peak alignment."
- [readme] input file format and configuration requirements: "The workflow accepts `.mzML` and `.abf` files. Convert other raw data formats to `.mzML` with ProteoWizard msConvert. Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name"
- [readme] container runtime support for local and HPC environments: "It includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce. It supports macOS and Linux and has been tested successfully on macOS"
- [readme] example dataset and reproducibility validation: "The example dataset is publicly available on Google Drive. It comes from Li, Z., Lu, Y., Guo, Y., Cao, H., Wang, Q., & Shui, W. (2018). Comprehensive evaluation of untargeted metabolomics data"
- [readme] file naming constraint: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] EDAM semantic annotation for MS-DIAL operations: "Operations: peak detection [EDAM:operation_3215], chromatogram alignment [EDAM:operation_3628], metabolite identification [EDAM:operation_3803]"
