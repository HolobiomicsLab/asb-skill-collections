---
name: mass-spectrometry-workflow-orchestration-snakemake
description: Use when when you have a collection of mzML.gz files from a multidimensional
  MS instrument (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Snakemake
  - conda
  - pip
  - Python
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python
  application programming interface and command-line tool
- import deimos
- A Snakemake configuration file in YAML format is required.
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
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

# mass-spectrometry-workflow-orchestration-snakemake

## Summary

Orchestrate end-to-end high-dimensional mass spectrometry (MS) data processing pipelines using Snakemake to automatically execute feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution on mzML input files, producing HDF5-formatted output with characterized features, spectra, and isotopic signatures across study samples.

## When to use

When you have a collection of mzML.gz files from a multidimensional MS instrument (e.g., ion mobility–time-of-flight MS) and need to apply a complete, reproducible workflow that detects features across N-dimensional data space, aligns them across samples, calibrates collision cross sections, and deconvolves tandem mass spectra without manually invoking individual processing steps.

## When NOT to use

- Input data is already a feature table or has been pre-aligned; use this skill only on raw mzML.gz files to avoid redundant re-processing.
- Single-dimensional MS data (e.g., 2D LC–MS without ion mobility) where multi-dimensional feature separation offers minimal benefit.
- Real-time or streaming MS acquisition where Snakemake batch orchestration is inappropriate; use the deimos Python API directly instead.

## Inputs

- mzML.gz files (N-dimensional MS data with accession mappings for drift_time and retention_time)
- config.yaml (Snakemake workflow configuration specifying dataset parameters, thresholds, and output paths)
- CCS calibration reference dataset (tuning file with known CCS values, e.g., example_tune_pos.h5)

## Outputs

- HDF5 feature table (features dataset with detected, aligned features characterized by m/z, drift_time, retention_time, and intensity)
- HDF5 MS1 dataset (thresholded, detected peaks)
- HDF5 MS2 dataset (deconvolved tandem mass spectra by feature)
- HDF5 isotopes dataset (isotopic signatures with parent–daughter relationships and abundance ratios)
- CCS calibration model (fit parameters and r² metric for drift-time-to-CCS conversion)

## How to apply

Clone the DEIMoS repository and activate a conda environment with required dependencies. Prepare a config.yaml file specifying dataset-specific parameters (e.g., thresholds, calibration standards). Place mzML.gz input files in the input/ directory. Invoke the DEIMoS CLI with the configuration file and number of processor cores (e.g., `deimos --config config.yaml --cores N`). Snakemake automatically constructs and executes the rule dependency graph, detecting peaks, aligning features across samples using all N-dimensional coordinates (m/z, drift time, retention time), fitting CCS calibrations (typically yielding r² ≥ 0.9999), identifying isotopic signatures with ≥3 members as a quality screen, and deconvolving MS/MS spectra. Monitor rule completion and verify that all expected HDF5 output files in output/ contain non-zero row counts in the ms1, ms2, features, and isotopes datasets.

## Related tools

- **DEIMoS** (Core Python API and CLI providing feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution algorithms) — http://github.com/pnnl/deimos
- **Snakemake** (Workflow orchestration engine that parses config.yaml, manages rule dependencies, parallelizes execution across cores, and handles input/output staging)
- **conda** (Virtual environment and dependency management system used to install DEIMoS and all transitive Python/system dependencies)
- **ProteoWizard msconvert** (Format conversion utility to convert raw instrument files (e.g., .raw, .d) to mzML.gz before workflow input)

## Examples

```
deimos --config config.yaml --cores 8
```

## Evaluation signals

- Snakemake rule DAG completes without errors; all expected rules (peak_detection, feature_alignment, ccs_calibration, isotope_detection, ms2_deconvolution) execute to completion.
- All output HDF5 files (ms1, ms2, features, isotopes keys) are present in output/ and contain non-zero row counts; features table has ≥1 row per sample.
- CCS calibration r² metric is ≥0.9999, confirming high-quality drift-time-to-CCS model fit.
- Isotopic signatures in the isotopes HDF5 dataset have ≥3 members and consistent mass defect relationships (e.g., expected ¹³C, ¹⁵N shifts).
- Feature retention times and m/z values fall within expected ranges for the instrument and sample; no NaN or inf values in aligned feature table.

## Limitations

- DEIMoS assumes mzML.gz files carry explicit cvParam accession identifiers (e.g., MS:1000016 for retention_time, MS:1002476 for drift_time); missing or non-standard accessions will cause workflow failure.
- CCS calibration requires a reference tuning file with known m/z and CCS standards; absence or poor-quality calibration standards degrades alignment confidence.
- Algorithm performance is dependent on tuning of threshold parameters (e.g., intensity thresholds of 100–1000 for peak detection); no universal threshold works across all instrument types or sample matrices.
- No changelog provided in repository, limiting visibility into versioning and backward compatibility across releases.

## Evidence

- [other] Snakemake workflow execution: "Invoke the DEIMoS CLI with the configuration file, specifying the number of cores and execution mode (local or cluster) as needed: deimos --config config.yaml --cores N."
- [intro] Multi-dimensional feature separation and alignment: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
- [other] Output HDF5 format and datasets: "Verify successful completion by confirming all output HDF5 files are present in output/ and contain expected datasets (ms1, ms2, features, isotopes) with non-zero row counts."
- [intro] Complete workflow rule chain: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [results] Input data format and accession mapping: "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
- [results] Isotope filtering criterion: "A good first screening is to only consider those isotopic signatures with at least 3 members."
- [intro] N-dimensional agnostic processing: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
