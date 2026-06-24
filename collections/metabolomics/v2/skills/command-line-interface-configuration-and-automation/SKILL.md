---
name: command-line-interface-configuration-and-automation
description: Use when you have a batch of raw LC-IMS-MS/MS data in mzML or mzML.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section
  (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment
  with required dependencies.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# command-line-interface-configuration-and-automation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and execute a DEIMoS CLI workflow via Snakemake to automate the end-to-end processing of multidimensional mass spectrometry data from raw mzML files to aligned, characterized features. This skill chains CLI arguments, YAML configuration parameters, and Snakemake DAG orchestration to reproducibly execute feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution across multiple samples.

## When to use

Apply this skill when you have a batch of raw LC-IMS-MS/MS data in mzML or mzML.gz format that requires consistent, reproducible processing across multiple runs, and you want to leverage Snakemake to manage dependencies, parallelize execution (locally or on a cluster), and track intermediate outputs without manually invoking each algorithmic step.

## When NOT to use

- Input is already a pre-processed feature table or aligned matrix; use this skill only when raw mzML data requires end-to-end processing.
- Single-file, one-off analysis with no need for reproducibility or parallelization; direct Python API calls via deimos.load() and deimos.peakpick() may be more efficient.
- Workflow requires custom, non-standard algorithmic steps not supported by DEIMoS's built-in rules; manual Snakemake rule authoring would be required.

## Inputs

- mzML or mzML.gz files (raw LC-IMS-MS/MS data with accession metadata for retention_time 'MS:1000016' and drift_time 'MS:1002476')
- YAML configuration file (Snakemake workflow parameters and algorithm settings)
- CLI arguments (--config, --count, --start, --cores, --cluster, --jobs, --dryrun, --unlock, --touch)

## Outputs

- Aligned feature table (HDF5 or CSV with columns: m/z, drift_time, retention_time, intensity, CCS, isotope signature)
- MS1 peakpicked data (HDF5 with detected local maxima satisfying signal criteria)
- MS2 deconvolved spectra (HDF5 or text format with fragmentation patterns)
- Snakemake execution logs and DAG visualization (optional)

## How to apply

Parse DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake execution mode and file limits. Auto-detect mzML and mzML.gz input files in the input/ directory and apply file-count filtering (--count N, starting at --start IDX) to manage DAG size. Load a YAML configuration file (default: config.yaml or --config PATH) to parameterize Snakemake rules and algorithm settings such as threshold (e.g., threshold=500 for intensity filtering). Construct a Snakemake DAG that defines the per-run workflow: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection. Execute the DAG via Snakemake with the specified executor (local with --cores N, or cluster submission with --cluster PATH and --jobs N), optionally performing dry-run (--dryrun), unlock (--unlock), or touch (--touch) operations. Populate the output/ directory with aligned features and processed MS1/MS2 results, then verify all expected output files are produced and conform to expected dimensionality (m/z, drift_time, retention_time, intensity) and data types (HDF5 or CSV).

## Related tools

- **Snakemake** (Orchestrates the DAG of DEIMoS processing rules, manages parallelization (local or cluster), and tracks intermediate outputs across batches of mzML files.)
- **DEIMoS** (Provides the Python API and CLI for feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution; invoked via Snakemake rules.) — http://github.com/pnnl/deimos
- **conda** (Creates a virtual environment with DEIMoS, Snakemake, and other dependencies to ensure reproducibility.)
- **Python** (Runtime environment for DEIMoS API and Snakemake rule execution.)
- **ProteoWizard msconvert** (Converts raw MS data from vendor formats (e.g., .raw, .d) to mzML for DEIMoS input.)

## Examples

```
snakemake --snakefile Snakefile --config config.yaml --cores 4 --count 10 --start 0 --dryrun
```

## Evaluation signals

- All expected output files exist in output/ directory with correct naming and dimensionality (m/z, drift_time, retention_time, intensity columns).
- Snakemake DAG completes without errors; log reports 0 failed rules and matches expected file counts (number of input mzML files × number of output stages).
- Feature alignment r-squared values are ≥ 0.9999 (consistent with DEIMoS benchmarks showing r-squared ~0.9999784552958134).
- Isotope signatures contain at least 3 members (minimum screening criterion stated in article); check isotope detection output for compliance.
- Dry-run (--dryrun) produces identical DAG structure on subsequent runs, confirming reproducibility of workflow definition.

## Limitations

- DEIMoS assumes mzML or mzML.gz input; vendor formats require prior conversion with ProteoWizard msconvert, adding preprocessing overhead.
- N-dimensional algorithmic implementations are data-agnostic but require calibration accessions (e.g., 'MS:1000016', 'MS:1002476') to be present in mzML metadata; missing accessions will cause parsing errors.
- Cluster execution (--cluster PATH, --jobs N) requires prior Snakemake cluster profile configuration and may introduce scheduling delays; local execution with --cores N is simpler but limited to single-machine resources.
- No changelog found; reproducibility across DEIMoS versions not formally tracked, so pinning DEIMoS and Snakemake versions in conda environment is critical.

## Evidence

- [other] Parse the DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake workflow execution mode and set file limits.: "Parse the DEIMoS CLI arguments (--config, --count, --start, --cores, --cluster, --jobs) to configure the Snakemake workflow execution mode and set file limits."
- [other] Load the YAML configuration file (default: config.yaml, or --config PATH) to parameterize Snakemake rules and algorithm settings.: "Load the YAML configuration file (default: config.yaml, or --config PATH) to parameterize Snakemake rules and algorithm settings."
- [other] Generate a Snakemake directed acyclic graph (DAG) defining the per-run workflow: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection.: "Generate a Snakemake directed acyclic graph (DAG) defining the per-run workflow: mzML → MS1 peakpicking → MS2 extraction/deconvolution → feature alignment → CCS calibration → isotope detection."
- [other] DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500), index building from factors, and persistent homology-based peak detection.: "DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500)"
- [methods] A Snakemake configuration file in YAML format is required.: "A Snakemake configuration file in YAML format is required."
- [readme] DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool: "DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
