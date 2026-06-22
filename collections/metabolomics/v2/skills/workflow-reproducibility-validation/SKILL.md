---
name: workflow-reproducibility-validation
description: Use when after implementing or deploying a containerized Nextflow workflow that processes LC-HRMS metabolomics .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0552
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - Docker
  - Nextflow
  - Singularity
  - MS-DIAL
  - MSFLO
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

# Workflow Reproducibility Validation

## Summary

Validate that a containerized bioinformatics workflow (specifically Nextflow-based LC-HRMS metabolomics pipelines) produces consistent, portable results across diverse compute environments by executing functional tests, comparing outputs against reference datasets, and verifying resource logs and execution traces.

## When to use

After implementing or deploying a containerized Nextflow workflow that processes LC-HRMS metabolomics .mzML data through tools like MS-DIAL and MSFLO, or when porting a workflow to a new compute environment (local, HPC, cloud) to ensure feature detection, peak alignment, and annotation outputs are invariant and reproducible.

## When NOT to use

- Workflow has not yet been containerized or does not include a functional_test profile — focus first on implementation and documentation of expected outputs.
- Input data is already a processed feature table or CSV — this skill validates raw-to-feature transformation, not downstream statistical analysis.
- Workflow execution succeeded but you have no reference dataset or prior baseline outputs to compare against — establish a reference run before validating reproducibility across environments.

## Inputs

- .mzML or .abf raw LC-MS data files
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 reference library (ms1_lib.txt)
- MS2 reference library (ms2_lib.msp)

## Outputs

- Feature table (.tsv or .msdial files with peak/feature annotations)
- execution_report.html (runtime and resource summary)
- execution_timeline.html (per-process execution timeline)
- execution.log (workflow progress and process-level logs)
- error.txt (failure diagnostics, if applicable)

## How to apply

First, run the workflow's built-in functional test profile on a small reference dataset to establish a baseline output signature. Execute the pipeline with explicit container backend (Docker or Singularity) and capture execution logs and HTML timeline reports. Compare the resulting feature tables (peak lists, aligned features, annotated metabolites) against reference outputs using file checksums or schema validation. Verify that resource utilization (CPU, memory, runtime) remains within expected bounds across test environments by inspecting the execution_report.html and execution_timeline.html. If outputs diverge, check for differences in configuration files (msdial_params.txt, msflo_params.ini), library versions, or container definitions. Document any deviations and confirm they are expected (e.g., due to platform-specific floating-point precision or parameter tuning).

## Related tools

- **Nextflow** (Workflow orchestration and execution engine; enables reproducible runs across local, container, and HPC environments with built-in logging and trace reporting) — https://www.nextflow.io/
- **Docker** (Container runtime for local execution; packages MS-DIAL, MSFLO, and dependencies to ensure consistent environment across machines) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for HPC systems; alternative to Docker for high-performance computing environments where root access is restricted) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Feature detection and peak alignment on containerized .mzML LC-HRMS data; produces aligned peak table passed to MSFLO) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial
- **MSFLO** (Annotation and statistical processing of aligned features; final output validation compares MSFLO results against reference feature tables) — https://github.com/Nextflow4Metabolomics/nextflow4ms-dial

## Examples

```
nextflow run main.nf -profile functional_test > logs/execution.log && diff <(grep -E '^[0-9]' results/example_output.tsv | md5sum) <(grep -E '^[0-9]' reference/example_output.tsv | md5sum)
```

## Evaluation signals

- Functional test profile executes without errors on both Docker and Singularity backends, producing non-empty feature tables with consistent row and column counts
- Feature table checksums or content hashes are identical when the same input data and configuration files are processed across different compute environments (local macOS, Linux HPC such as HiPerGator)
- execution_report.html shows total runtime, CPU and memory usage within expected ranges (no runaway processes or OOM errors); execution_timeline.html displays all workflow processes completing in expected order
- Execution logs contain no warnings related to missing libraries, incompatible tool versions, or container pull failures; error.txt is absent or contains only expected edge-case handling
- Feature table schema matches reference (same number and names of metabolite/peak columns, consistent data types and value ranges for m/z, retention time, intensity)

## Limitations

- Floating-point precision differences in peak intensity or retention time values may occur across platforms due to CPU/OS differences; establish absolute tolerance thresholds (e.g., ±0.01 ppm for m/z) before comparing outputs
- Special characters in input file names can cause unexpected pipeline failures; only alphanumeric characters and underscores are safe (as noted in FAQ)
- If Slurm job scheduler is used on HPC, CPU allocation must be specified with `--max_cpus` rather than `--cpus` to avoid 'Process requirement exceed available CPUs' errors; this affects reproducibility on some HPC platforms
- Validation depends on availability of reference datasets and ground-truth feature tables; the workflow ships with functional_test data but lacks validation metrics (accuracy, sensitivity, specificity) against published benchmarks
- No automated comparison or diffing tool is provided in the repository; validation currently requires manual inspection of logs, HTML reports, and feature table outputs

## Evidence

- [readme] Establish baseline output signature and reference comparison: "Run the functional test profile: `nextflow run main.nf -profile functional_test > logs/execution.log`"
- [readme] Verify environment portability: "It supports macOS and Linux and has been tested successfully on: - macOS 13.5.1 with a 2.6 GHz 6-Core Intel Core i7 processor and 16 GB memory. - HiPerGator, the University of Florida public research"
- [readme] Check for file naming issues affecting reproducibility: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [readme] Inspect execution logs and resource usage: "`execution_report.html` summarizes workflow runtime and computational resource usage. `execution_timeline.html` shows the execution timeline for each process."
- [readme] Containerization ensures reproducibility: "The workflow includes Docker and Singularity support to simplify installation, improve portability, and make results easier to reproduce."
