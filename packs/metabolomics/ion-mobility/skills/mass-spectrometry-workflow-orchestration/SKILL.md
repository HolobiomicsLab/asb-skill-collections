---
name: mass-spectrometry-workflow-orchestration
description: Use when you have a collection of mzML or mzML.gz files from LC-IMS-MS/MS experiments and need to apply a consistent, reproducible sequence of feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution operations across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3934
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - Snakemake
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment with required dependencies.
- 'Install DEIMoS using `pip <https://pypi.org/project/pip/>`_: ``pip install -e .``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-workflow-orchestration

## Summary

Orchestrate multi-stage LC-IMS-MS/MS data processing pipelines using Snakemake DAGs to automate mzML ingestion, peak detection, feature alignment, and spectral deconvolution. This skill ensures reproducible, scalable execution of DEIMoS analysis across batches of samples with parameterized algorithm configuration.

## When to use

You have a collection of mzML or mzML.gz files from LC-IMS-MS/MS experiments and need to apply a consistent, reproducible sequence of feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution operations across multiple samples. Use this skill when manual per-file processing is infeasible and you want to parallelize or submit jobs to a compute cluster.

## When NOT to use

- Input data are already aligned features or a processed feature table (use this skill for raw mzML only).
- You require real-time or interactive parameter tuning during execution (Snakemake is batch-oriented; consider manual scripts for exploratory analysis).
- Your computational environment does not support Snakemake (e.g., restricted Python/conda access); in such cases, invoke DEIMoS directly via Python API or shell commands.

## Inputs

- mzML or mzML.gz files (raw LC-IMS-MS/MS data with embedded MS:1000016 retention_time and MS:1002476 drift_time accessions)
- Snakemake configuration file (YAML format, defining algorithm parameters and rule execution settings)
- CLI arguments (--config, --count, --start, --cores, --cluster, --jobs, --dryrun, --unlock, --touch)

## Outputs

- Aligned feature table (HDF5 format, with m/z, CCS, retention_time, intensity, isotopic signature, and tandem MS spectra per feature)
- MS1 peak-picked data (per-sample feature lists after threshold filtering and persistent homology detection)
- MS2 deconvolved spectra (per-feature tandem mass spectra)
- Execution logs and Snakemake DAG visualization

## How to apply

Define a Snakemake workflow by (1) specifying CLI arguments (--config for YAML settings, --count and --start for file-count filtering, --cores for local parallelization or --cluster/--jobs for cluster submission); (2) auto-detecting .mzML or .mzML.gz input files in the input/ directory; (3) loading the configuration YAML to parameterize DEIMoS algorithm settings (e.g., threshold=500 for peak detection, accession field mappings for m/z and drift_time extraction); (4) generating a DAG that chains mzML → MS1 peakpicking → MS2 extraction → feature alignment → CCS calibration → isotope detection; (5) executing the DAG via `snakemake` with the chosen executor (local or cluster); and (6) verifying output/ contains aligned feature tables and processed MS1/MS2 results. Rationale: Snakemake tracks file dependencies and re-runs only changed rules, reducing redundant computation; YAML configuration decouples algorithm parameters from workflow logic, enabling rapid prototyping and reproducibility across studies.

## Related tools

- **Snakemake** (Workflow orchestration engine; defines, schedules, and executes the multi-stage DAG for batch processing mzML files through DEIMoS rules)
- **DEIMoS** (Core analytical engine invoked by Snakemake rules to parse mzML, detect features via persistent homology, align features across samples, calibrate CCS, detect isotopes, and deconvolve MS/MS spectra) — http://github.com/pnnl/deimos
- **conda** (Environment management; creates isolated virtual environments with DEIMoS and dependency versions specified in the workflow configuration)
- **Python** (Scripting language for DEIMoS API calls, data I/O, and custom rule logic within the Snakemake workflow)
- **ProteoWizard msconvert** (Optional upstream tool to convert raw vendor formats (e.g., .raw, .d) to mzML before ingestion into the workflow)

## Examples

```
snakemake --config config.yaml --cores 4 --count 10 --start 0
```

## Evaluation signals

- All input mzML/mzML.gz files are successfully parsed: verify by checking Snakemake log for zero parse errors and accession field extraction (MS:1000016, MS:1002476) confirmed in per-sample logs.
- Output feature table schema is valid: m/z, CCS, retention_time, intensity, isotopic signature, and MS/MS spectra are all present and non-null for detected features.
- Feature alignment consistency: r-squared between technical replicate feature lists is ≥ 0.999 (as reported in the DEIMoS reference publication).
- Isotope detection filter applied: isotopic signatures retained in the output contain at least 3 members, matching DEIMoS screening guidance.
- Workflow DAG completeness: all expected output files exist in output/ directory with non-zero file size; `snakemake --dryrun` reports no failed rules.

## Limitations

- DEIMoS is agnostic to instrumentation but requires that mzML files contain standardized accession fields for retention_time and drift_time; non-compliant or legacy formats may require pre-conversion via ProteoWizard.
- Peak detection threshold (default: 500) is data-dependent; suboptimal thresholds may result in false positives or missed weak features; tuning requires exploratory analysis before full batch execution.
- Feature alignment confidence depends on sufficient dimensional separation (m/z, drift_time, retention_time); low-resolution or 1D data may exhibit higher false-positive alignment rates.
- Cluster execution requires pre-configured scheduler (e.g., SLURM); misconfigured --cluster arguments will cause job submission failures without recovery.
- No changelog documented; version pinning (e.g., DEIMoS==1.6.2) is essential for reproducibility across studies or time intervals.

## Evidence

- [other] Parse the DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake workflow execution mode: "Parse the DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake workflow execution mode and set file limits."
- [other] Load the YAML configuration file to parameterize Snakemake rules and algorithm settings: "Load the YAML configuration file (default: config.yaml, or --config PATH) to parameterize Snakemake rules and algorithm settings."
- [other] Generate a Snakemake DAG defining per-run workflow with progressive feature detection, alignment, and calibration: "Generate a Snakemake directed acyclic graph (DAG) defining the per-run workflow: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection."
- [other] DEIMoS parses mzML by extracting accession fields for retention_time and drift_time, then applies threshold filtering: "DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500)"
- [methods] A Snakemake configuration file in YAML format is required: "A Snakemake configuration file in YAML format is required."
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [results] Isotope detection filter best practice: only consider isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
