# Evaluation Strategy

## Direct Checks

- verify file exists: github:Nextflow4Metabolomics__nextflow4ms-dial repository is accessible and contains a Nextflow workflow definition (nextflow.config or main.nf)
- file_format_is: workflow accepts .mzML files as input (inspect workflow input channel definitions in main.nf or nextflow.config)
- script_runs: Nextflow workflow executes without error on a minimal .mzML test file using Docker container runtime (robust to parameter choices for container image versions)
- script_runs: Nextflow workflow executes without error on a minimal .mzML test file using Singularity container runtime (robust to parameter choices for container image versions)
- contains_substring: workflow definition includes MS-DIAL as a process step (search process blocks in main.nf or included modules)
- contains_substring: workflow definition includes MSFLO as a downstream process step following MS-DIAL (search process blocks to confirm sequential ordering)
- file_format_is: final workflow output artifacts are produced in MSFLO-compatible format (inspect output declarations and artifact naming conventions; solution_space: MSFLO format specification must be inferred from MSFLO documentation or output file extension patterns)
- file_exists: Docker image URI or pull command is documented in workflow configuration or README
- file_exists: Singularity image URI or build definition is documented in workflow configuration or README

## Expert Review

- Assess whether the MS-DIAL → MSFLO sequential pipeline architecture as implemented matches the intended metabolomics data processing workflow (requires domain knowledge of LC-HRMS metabolomics processing steps and tool compatibility)
- Evaluate whether containerization (Docker/Singularity) preserves tool functionality and parameter passing fidelity for both MS-DIAL and MSFLO components relative to non-containerized reference execution
