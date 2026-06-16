# Evaluation Strategy

## Direct Checks

- verify that github:shuzhao-li-lab/PythonCentricPipelineForMetabolomics repository is accessible and contains a README
- file_exists: README.md or equivalent documentation in the repository root
- contains_substring: README describes a fixed architecture pipeline with steps for (1) experiment assembly, (2) Asari feature extraction, (3) blank masking, (4) sample dropping, (5) normalization, (6) imputation, (7) empCpd construction
- file_exists: a Python orchestrator script or module that implements the fixed control loop (e.g., main.py, pipeline.py, or equivalent in the repo)
- script_runs: the orchestrator script executes without errors on a minimal valid mzML input and produces intermediate outputs at each of the seven pipeline stages
- output_matches_reference: intermediate outputs from a reference execution (if provided in asari_pcpfm_tutorials or deployment guide) match in structure (column names, data types, row counts for identical inputs) — robust to parameter choices
- file_format_is: final output of pipeline is one of (.txt, JSON) as stated in EnrichedIndex
- verify that the orchestrator implements a bounded, deterministic, sequentially-ordered control loop with no branching or conditional re-entry — no 'and then', 'if', or loops over variable sub-task counts

## Expert Review

- Evaluate whether the documented pipeline architecture faithfully represents the method as described in the published article (DOI: 10.1371/journal.pcbi.1011912), particularly the role and configuration of blank masking, sample dropping, normalization, and imputation steps
- Assess whether the fixed control loop design is scientifically sound for typical LC-MS metabolomics workflows and whether any documented deviations or optional branches undermine the 'fixed' characterization
- Review documentation clarity: does the README or equivalent explicitly describe the purpose, input contracts, and output semantics of each of the seven stages?
