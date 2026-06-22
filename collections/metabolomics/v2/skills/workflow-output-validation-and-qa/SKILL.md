---
name: workflow-output-validation-and-qa
description: Use when after executing a Nextflow-based MS-DIAL workflow on .mzML LC-HRMS metabolomics data using Docker or Singularity container backends.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSFLO
  - Nextflow
  - MS-DIAL
  - Docker
  - Singularity
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-output-validation-and-qa

## Summary

Verify successful execution of containerized LC-HRMS metabolomics workflows by inspecting presence, format, and integrity of intermediate and final outputs (MS-DIAL .msdial → .tsv files and MSFLO results). This skill ensures reproducibility and detects failures before downstream analysis.

## When to use

After executing a Nextflow-based MS-DIAL workflow on .mzML LC-HRMS metabolomics data using Docker or Singularity container backends. Use this skill when you need to confirm that peak detection, chromatogram alignment, and metabolite identification steps completed without silent failures, and to validate that output files are accessible and in expected formats before loading into spreadsheet or statistical software.

## When NOT to use

- Workflow execution terminated with explicit error messages before completion — validation assumes the workflow was allowed to finish; inspect error.log instead.
- Results directory is empty or inaccessible — this indicates a container initialization or file system permission problem, not an output validation issue.
- You are validating raw .mzML files before processing — use input data quality checks, not output validation.

## Inputs

- .mzML LC-HRMS raw mass spectrometry data files
- MS-DIAL configuration file (msdial_params.txt)
- MS-FLO configuration file (msflo_params.ini)
- MS1 and MS2 spectral libraries (ms1_lib.txt, ms2_lib.msp)

## Outputs

- MS-DIAL .msdial output files (converted to .tsv format)
- MSFLO results files
- execution_report.html (Nextflow runtime and resource summary)
- execution_timeline.html (per-process execution timeline)
- execution.log (detailed workflow metadata and process-level logs)

## How to apply

After workflow completion, navigate to the designated results directory and verify the presence of expected MS-DIAL output files (.msdial, converted to .tsv for spreadsheet compatibility) and MSFLO output files. Check that all output files are non-empty and readable. Cross-reference the execution log (execution.log or execution_report.html) to confirm that all expected processes completed without error. Examine the execution_timeline.html to ensure each process stage (peak detection, alignment, identification) executed in correct order. If using a high-performance computing environment like HiPerGator with Singularity, verify that container initialization and resource allocation messages appear in execution logs. Validate output file schemas by opening a sample .tsv output in a text editor or spreadsheet application to confirm it contains expected metabolite feature columns and intensity values.

## Related tools

- **Nextflow** (Workflow orchestration and process execution tracking; produces execution_report.html, execution_timeline.html, and execution.log artifacts for validation) — https://www.nextflow.io/
- **MS-DIAL** (Peak detection, chromatogram alignment, and metabolite identification; produces primary .msdial output files validated in results directory)
- **MSFLO** (Post-processing and statistical analysis of MS-DIAL features; produces secondary results files included in validation check)
- **Docker** (Container backend for local execution; validation confirms container initialization and file mounts in execution logs) — https://docs.docker.com/engine/installation/
- **Singularity** (Container backend for HPC environments; validation confirms Singularity container binding and resource allocation in execution logs) — https://www.sylabs.io/guides/3.0/user-guide/

## Examples

```
nextflow run main.nf -profile docker > logs/execution.log && ls -lah results/*.tsv && head -n 5 results/sample_output.tsv
```

## Evaluation signals

- Presence of .tsv output files in results directory matching expected count and sample naming convention from input data
- Execution logs report 'Completed successfully' or equivalent for all MS-DIAL and MSFLO processes; no 'FAILED' or 'ERROR' entries
- execution_report.html shows all processes in green/completed state and total execution time > 0
- Sample .tsv file contains metabolite feature columns (RT, m/z, intensity) with numeric values and non-zero row count
- execution_timeline.html shows processes executed in logical sequence: peak detection → alignment → identification → MSFLO

## Limitations

- Workflow does not validate correctness of results against ground truth or reference standards — only confirms file presence and format. Output values may be scientifically invalid.
- No explicit validation of MS1/MS2 library matches or metabolite identification accuracy is performed; inspect MSFLO confidence scores manually.
- File name conventions are strict; special characters in input file names cause silent process skipping and false validation passes. Use underscores only.
- Initial release (Nextflow4MS-DIAL v1.0) lacks explicit reproducibility testing documentation; validation is heuristic-based on log inspection, not formal test suite.
- Execution timeline and resource reports vary between Docker (local) and Singularity (HPC); HPC-specific resource allocations must be verified against job scheduler output (Slurm) separately.

## Evidence

- [other] Verify workflow completion and validate presence of MS-DIAL and MSFLO output files in the designated results directory.: "Verify workflow completion and validate presence of MS-DIAL and MSFLO output files in the designated results directory."
- [readme] Example outputs are stored in the results folder. The file extensions for produced .msdial files have been changed to .tsv so the files can be opened in spreadsheet software.: "Example outputs are stored in the `results` folder. The file extensions for produced `.msdial` files have been changed to `.tsv` so the files can be opened in spreadsheet software such as Microsoft"
- [readme] execution_report.html summarizes workflow runtime and computational resource usage; execution_timeline.html shows the execution timeline for each process; execution.log includes metadata such as workflow version, parameter settings, resource allocation, container information, and process-level logs.: "`execution_report.html` summarizes workflow runtime and computational resource usage. `execution_timeline.html` shows the execution timeline for each process. `logs/execution.log` is an example log"
- [readme] To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use.: "To avoid unexpected errors, do not use special characters in file names. Underscores are safe to use."
- [other] containerized workflow MS-DIAL → MSFLO enables processing of .mzML LC-MS metabolomics data: "Enabling processing .mzML LC-MS metabolomics data through a containerized MS-DIAL workflow."
