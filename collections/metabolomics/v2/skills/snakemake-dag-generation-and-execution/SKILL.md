---
name: snakemake-dag-generation-and-execution
description: Use when you have multiple mzML or mzML.gz files from LC-IMS-MS/MS instruments
  and need to apply DEIMoS feature detection, alignment, and calibration operations
  in a reproducible, traceable manner.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Snakemake
  - DEIMoS
  - Python
  - conda
  - pip
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- A Snakemake configuration file in `YAML <http://yaml.org/>`_ format is required.
- Functionality includes feature detection, feature alignment, collision cross section
  (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment
  with required dependencies.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# snakemake-dag-generation-and-execution

## Summary

Construct and execute a Snakemake directed acyclic graph (DAG) to orchestrate DEIMoS multi-dimensional mass spectrometry workflows, automating mzML ingestion, peak detection, feature alignment, and CCS calibration across local or cluster compute environments. This skill ensures reproducible, scalable processing of high-dimensional LC-IMS-MS/MS data with explicit rule dependencies and configurable execution modes.

## When to use

Use this skill when you have multiple mzML or mzML.gz files from LC-IMS-MS/MS instruments and need to apply DEIMoS feature detection, alignment, and calibration operations in a reproducible, traceable manner. Applies when you want to parallelize processing across multiple input files (via --count and --start filtering), enforce rule ordering (mzML → MS1 peakpicking → MS2 extraction → feature alignment → CCS calibration → isotope detection), and manage compute resources (local cores or cluster job scheduling).

## When NOT to use

- Input data are already in feature table format (aligned .h5 or .csv); use this skill only on raw mzML files that require instrument-agnostic, N-dimensional processing.
- Single mzML file with no need for cross-sample alignment or batch processing; simpler DEIMoS Python API invocations suffice.
- When deterministic rule ordering is not required or workflow dependencies are already resolved; use Snakemake DAG generation only if you need explicit, traceable rule lineage.

## Inputs

- mzML or mzML.gz files (input/ directory)
- YAML configuration file (config.yaml or --config PATH) with algorithm parameters and rule settings
- Optional tuning or reference data files (e.g., example_tune_pos.h5 for CCS calibration)
- DEIMoS CLI arguments (--count, --start, --cores, --cluster, --jobs, --dryrun, --unlock, --touch)

## Outputs

- Snakemake directed acyclic graph (DAG) defining rule dependencies and per-file workflow
- HDF5 (.h5) feature tables (aligned features, MS1/MS2 peaks, isotope signatures)
- Calibration artifacts (CCS calibration parameters, retention time/drift time models)
- Execution logs and status reports (per-rule, per-file)
- Populated output/ directory with all processed and aligned results

## How to apply

First, parse DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure Snakemake execution mode (local or cluster) and set file limits. Auto-detect .mzML and .mzML.gz input files in the input/ directory; apply file-count filtering (--count N, starting at --start IDX) to subset the DAG size if needed. Load a YAML configuration file (default: config.yaml or --config PATH) to parameterize Snakemake rules and DEIMoS algorithm settings (e.g., threshold=500 for peakpicking). Generate the DAG defining the per-run workflow with explicit rule dependencies: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection. Execute the DAG via Snakemake with the specified executor (local with --cores N, or cluster with --cluster PATH and --jobs N); optionally perform dry-run (--dryrun), unlock (--unlock), or touch (--touch) operations. Verify all expected output files are produced in the output/ directory (aligned features, MS1/MS2 results, calibration artifacts).

## Related tools

- **Snakemake** (Workflow orchestration engine; defines, schedules, and executes per-file DAGs with rule dependencies, parallelization, and cluster integration)
- **DEIMoS** (Python API and CLI target for Snakemake rules; performs mzML parsing, feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution) — https://github.com/pnnl/deimos
- **conda** (Virtual environment management; ensures reproducible, isolated DEIMoS and Snakemake dependency resolution)
- **Python** (Primary implementation language for DEIMoS API and Snakemake rule logic; enables data I/O, configuration parsing, and post-processing)
- **ProteoWizard msconvert** (Optional pre-processing tool; converts vendor instrument formats to mzML input for Snakemake workflow)

## Examples

```
snakemake --config config.yaml --count 5 --start 0 --cores 4 --dryrun
```

## Evaluation signals

- DAG visualization (snakemake --dag output) shows all expected rules with correct dependencies: mzML → MS1 → MS2 → alignment → CCS → isotope.
- All input files matching --count and --start filtering are processed (verify input file count matches DAG node count).
- Output directory contains expected .h5 files (aligned features, MS1/MS2 peaks, isotope signatures) with non-zero record counts.
- Snakemake execution log reports 0 failed rules and matches expected runtime parallelization (--cores or --jobs utilization).
- Dry-run (--dryrun) output lists all planned rule invocations without errors; actual execution (re-run without --dryrun) completes with matching file manifest.

## Limitations

- DEIMoS is largely agnostic to acquisition instrumentation, but mzML files must contain valid accession fields (e.g., MS:1000016 for retention_time, MS:1002476 for drift_time); missing accessions cause parsing failures.
- Snakemake DAG generation requires valid YAML configuration; malformed config files or missing algorithm parameters will fail rule instantiation.
- Cluster execution requires a valid --cluster submission template (e.g., SLURM) and network connectivity; local mode is more robust but limited to single-machine parallelization.
- Feature alignment and CCS calibration performance depend on sample representativeness and data quality; poor signal-to-noise or sparse features may produce low-confidence alignments.
- No changelog or versioning guarantees are documented; reproducibility across DEIMoS versions may require explicit dependency pinning in conda environment files.

## Evidence

- [other] mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection: "per-run workflow: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection"
- [other] Parse DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs): "Parse the DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake workflow execution mode"
- [other] Auto-detect .mzML and .mzML.gz input files in the input/ directory; apply file-count filtering: "Auto-detect .mzML and .mzML.gz input files in the input/ directory; apply file-count filtering (--count N, starting at --start IDX) to limit the DAG size"
- [other] Load the YAML configuration file (default: config.yaml, or --config PATH) to parameterize Snakemake rules: "Load the YAML configuration file (default: config.yaml, or --config PATH) to parameterize Snakemake rules and algorithm settings"
- [other] Execute the DAG via Snakemake with the specified executor (local with --cores N, or cluster with --cluster PATH and --jobs N): "Execute the DAG via Snakemake with the specified executor (local with --cores N, or cluster with --cluster PATH and --jobs N); optionally perform dry-run (--dryrun), unlock (--unlock), or touch"
- [methods] A Snakemake configuration file in YAML format is required.: "A Snakemake configuration file in YAML format is required."
- [other] DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time): "DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500)"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
