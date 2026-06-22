---
name: sampledata-annotation-and-assignment
description: Use when after loading multiple LC-MS .mzML files into an MsExperiment object using MsBackendMzR backend, when you have a documented injection sequence (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - R
  - MsExperiment
  - MsBackendMzR
  - TARDIS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
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

# sampledata-annotation-and-assignment

## Summary

Annotation and assignment of sample metadata (e.g., QC vs. sample type) to loaded LC-MS spectral data in an MsExperiment object. This skill ensures that each injection is correctly labeled with its experimental role, enabling downstream QC-based filtering and stratified analysis.

## When to use

After loading multiple LC-MS .mzML files into an MsExperiment object using MsBackendMzR backend, when you have a documented injection sequence (e.g., two QC, four sample, two QC, four sample, two QC for 14 runs) and need to label each file's sampleData 'type' column to distinguish QC from sample runs for quality control assessment and metrics calculation.

## When NOT to use

- Input MsExperiment object already has a populated and validated 'type' or equivalent sample classification column — re-annotation risks overwriting correct labels.
- Injection sequence or QC/sample designation is unknown or undocumented — annotation requires ground truth.
- Number of type labels does not match the number of loaded spectra files — misalignment will cause errors or false assignments.

## Inputs

- MsExperiment object loaded with 14 LC-MS .mzML spectra files
- Vector of 'type' labels (e.g., c('QC', 'QC', 'sample', 'sample', 'sample', 'sample', 'QC', 'QC', 'sample', 'sample', 'sample', 'sample', 'QC', 'QC')) corresponding to injection positions

## Outputs

- MsExperiment object with sampleData 'type' column populated with 'QC' or 'sample' labels
- Annotated spectra object enabling stratified QC and sample analysis

## How to apply

Load all .mzML files from a directory using readMsExperiment() with the MsBackendMzR backend to create an MsExperiment object containing spectra from all injections in order. Create or retrieve a 'type' annotation vector that assigns 'QC' or 'sample' labels corresponding to the documented injection positions (e.g., positions 1–2 as QC, 3–6 as sample, 7–8 as QC, 9–12 as sample, 13–14 as QC). Assign this vector to the sampleData slot of the MsExperiment object, ensuring one-to-one positional correspondence between the loaded files and type labels. Validate that the length of the type vector matches the number of loaded spectra files and that no missing or misaligned assignments exist. This labeling enables TARDIS and downstream tools to compute average QC metrics separately from sample runs and to flag quality issues specific to each injection type.

## Related tools

- **MsExperiment** (Container object for storing annotated LC-MS spectra with sampleData metadata slots)
- **Spectra** (Loads MS data as Spectra objects and integrates with MsExperiment for metadata assignment)
- **MsBackendMzR** (Backend for reading .mzML files into MsExperiment with correct file ordering)
- **TARDIS** (Uses annotated 'type' column to calculate average QC metrics and separate QC from sample results) — https://github.com/pablovgd/TARDIS

## Evaluation signals

- Length of sampleData 'type' vector equals the number of loaded spectra files (14 in the article's example); no NA or NULL values present.
- sampleData(MsExperiment)$type returns the expected label sequence: exactly 2 QC + 4 sample + 2 QC + 4 sample + 2 QC in order.
- Downstream QC metric aggregation in TARDIS correctly stratifies results by type: a tibble with average metrics for each target in the QC runs is returned without duplication or misalignment.
- Positional correspondence verified: the sampleData$type label at index i matches the injection sequence documented for the i-th .mzML file.
- No error or warning when accessing sampleData(MsExperiment)$type; all 14 entries are non-missing character strings.

## Limitations

- Annotation is positional and order-dependent: if .mzML files are loaded in the wrong order (e.g., alphabetically sorted instead of chronologically), type labels will be misaligned with the actual injection sequence.
- The skill requires accurate prior documentation of the injection sequence and QC/sample designation; if the source injection log is incorrect or incomplete, all downstream QC calculations will be invalid.
- Manual annotation is error-prone for large batches; no automatic detection of QC vs. sample runs is performed by this skill alone.

## Evidence

- [other] MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values: "MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values"
- [other] Assign the 'type' vector to the sampleData slot of the MsExperiment object, ensuring one-to-one correspondence with the 14 loaded spectra files: "Assign the 'type' vector to the sampleData slot of the MsExperiment object, ensuring one-to-one correspondence with the 14 loaded spectra files."
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an MsExperiment object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [results] a tibble that contains a feature table with the average metrics for each target in the QC runs: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
