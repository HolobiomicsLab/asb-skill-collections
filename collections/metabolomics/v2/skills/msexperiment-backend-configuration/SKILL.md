---
name: msexperiment-backend-configuration
description: Use when you have multiple centroided .mzML LC-MS files that need to be loaded into a unified object for targeted peak integration, and you need to distinguish QC runs from sample runs to compute per-group quality metrics (e.g., average SNR, peak correlation, area under curve per QC cohort).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MsExperiment
  - Spectra
  - R
  - MsBackendMzR
  - TARDIS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MsExperiment Backend Configuration

## Summary

Configure and populate an MsExperiment object with LC-MS spectral data using a specified backend (e.g., MsBackendMzR) and annotate sample metadata (such as QC vs. sample type) to enable downstream targeted integration and quality assessment workflows.

## When to use

You have multiple centroided .mzML LC-MS files that need to be loaded into a unified object for targeted peak integration, and you need to distinguish QC runs from sample runs to compute per-group quality metrics (e.g., average SNR, peak correlation, area under curve per QC cohort).

## When NOT to use

- Input files are already in a non-centroided format (e.g., profile mode .mzML); centroiding must be performed separately before backend configuration.
- You have only a single LC-MS file; MsExperiment is designed for multi-file cohorts to enable QC-stratified analysis.
- Spectral data is already loaded into a different container format (e.g., a Spectra object or feature matrix); reconfiguring into MsExperiment would duplicate processing.

## Inputs

- collection of centroided .mzML files (14 files in the reference workflow)
- injection sequence metadata defining QC/sample labels for each file position

## Outputs

- MsExperiment object with 14 spectra samples
- sampleData slot populated with 'type' column (QC or sample)
- validated one-to-one correspondence between files and sample metadata rows

## How to apply

Use readMsExperiment() with the MsBackendMzR backend to load all .mzML files from the input directory into a single MsExperiment object, preserving the one-to-one correspondence between files and spectra. Construct a sampleData vector with a 'type' column that labels each file as 'QC' or 'sample' according to the injection sequence (e.g., QC–sample–QC pattern). Assign this vector to the sampleData slot of the MsExperiment object. Validate that the row count of sampleData matches the number of loaded files and that all type assignments are correctly aligned. This configuration enables TARDIS and other Spectra-based tools to perform polarity filtering, targeted peak detection, and QC-stratified metrics calculation downstream.

## Related tools

- **MsExperiment** (Container object for loading, storing, and managing multi-file LC-MS experiments with associated sample metadata)
- **Spectra** (Backend framework for efficient MS spectra representation and integration; MsExperiment wraps Spectra objects with sample-level annotations)
- **MsBackendMzR** (Backend provider that reads .mzML files and populates Spectra/MsExperiment with mass-to-charge and intensity arrays)
- **TARDIS** (Downstream consumer that accepts configured MsExperiment objects as input for targeted peak integration and QC-stratified quality metrics) — https://github.com/pablovgd/TARDIS

## Evaluation signals

- MsExperiment object nrow(sampleData) equals the number of input .mzML files (e.g., 14 files → 14 rows in sampleData).
- sampleData 'type' column contains only 'QC' or 'sample' values with no missing (NA) entries; injection sequence matches documented pattern (e.g., 2 QC, 4 sample, 2 QC, 4 sample, 2 QC for 14 runs).
- No misalignment warnings when querying spectra by sample index; row i of sampleData corresponds to the i-th loaded file.
- Downstream TARDIS screening mode executes without errors on the configured MsExperiment, confirming metadata schema compatibility.
- QC-cohort filtering using sampleData$type == 'QC' successfully subsets spectra and returns correct count of QC runs (e.g., 6 QC spectra for the reference 14-file design).

## Limitations

- Backend configuration assumes input files are already centroided and in .mzML format; profile-mode or other formats (NetCDF, raw vendor formats) require prior conversion using MSConvert/ProteoWizard.
- sampleData must be manually constructed or retrieved from documentation; no automated inference of QC vs. sample labels from filename or metadata is provided by MsExperiment alone.
- One-to-one file-to-row correspondence is enforced; non-uniform sample groupings (e.g., technical replicates of the same sample) must be encoded as separate rows in sampleData.
- The 'type' column is user-defined and not validated against a controlled vocabulary; incorrect or inconsistent labels (e.g., typos: 'qc' vs. 'QC') will silently propagate and cause incorrect downstream QC-stratified metrics.

## Evidence

- [other] MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values: "MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values"
- [intro] loads MS data as `Spectra` objects so it's easily integrated with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [other] Read all 14 .mzML files from vignette_data/mzML/ directory using MsBackendMzR backend in Spectra/MsExperiment: "Read all 14 .mzML files from vignette_data/mzML/ directory using MsBackendMzR backend in Spectra/MsExperiment"
