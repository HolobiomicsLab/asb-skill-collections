---
name: qc-sample-classification-labeling
description: Use when when loading multiple LC-MS runs (mzML files) into an MsExperiment object and the injection sequence contains an interleaved or documented pattern of QC and sample runs (e.g., two QC, four sample, two QC, four sample, two QC).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC-Sample Classification and Labeling

## Summary

Systematic annotation of LC-MS injection runs as either QC (quality control) or sample based on their position in an acquisition sequence, implemented by populating the sampleData 'type' column of an MsExperiment object. This classification enables downstream quality assessment and differential treatment of QC versus analytical samples.

## When to use

When loading multiple LC-MS runs (mzML files) into an MsExperiment object and the injection sequence contains an interleaved or documented pattern of QC and sample runs (e.g., two QC, four sample, two QC, four sample, two QC). Essential when TARDIS or other quality-control workflows need to segregate QC runs for metric averaging or sample runs for feature extraction.

## When NOT to use

- Injection sequence or run labeling is not documented or unknown — classification will be unreliable.
- All runs are samples with no QC injections — the classification adds no discriminative value.
- Input is already a feature table or aggregated results table rather than individual spectra runs — sampleData type labeling applies only to run-level objects.

## Inputs

- mzML file collection (centroided LC-MS runs)
- MsExperiment object with loaded spectra
- documented injection sequence / run metadata (specifying QC vs. sample positions)

## Outputs

- MsExperiment object with populated sampleData 'type' column
- labeled run metadata enabling QC/sample segregation in downstream analyses

## How to apply

After loading all mzML files from the data directory using readMsExperiment() with MsBackendMzR backend, create or retrieve a documented 'type' vector that labels each of the loaded files as either 'QC' or 'sample' according to the known injection sequence. Assign this vector to the sampleData slot of the MsExperiment object, ensuring strict one-to-one correspondence between vector positions and the 14 (or relevant count of) loaded spectra files. Validate that the MsExperiment object contains all files with correct sampleData labeling and no missing or misaligned type assignments, then pass the classified object to downstream TARDIS or QC analysis functions that depend on the 'type' field to compute average metrics for QC runs separately from samples.

## Related tools

- **MsExperiment** (Container object that holds loaded spectra and sampleData metadata, including the 'type' classification column)
- **Spectra** (R package for reading and representing MS data; loads mzML files into Spectra objects that are integrated into MsExperiment)
- **MsBackendMzR** (Backend for Spectra that reads mzML files using ProteoWizard interface)
- **TARDIS** (Downstream tool that consumes MsExperiment objects with 'type' classification to compute separate quality metrics for QC vs. sample runs) — https://github.com/pablovgd/TARDIS
- **R** (Statistical computing environment in which MsExperiment, Spectra, and classification logic are executed) — https://cloud.r-project.org/index.html

## Examples

```
library(MsExperiment); library(Spectra); mse <- readMsExperiment(files=list.files('vignette_data/mzML/', full.names=TRUE), backend='MsBackendMzR'); sampleData(mse)$type <- c('QC', 'QC', 'sample', 'sample', 'sample', 'sample', 'QC', 'QC', 'sample', 'sample', 'sample', 'sample', 'QC', 'QC')
```

## Evaluation signals

- MsExperiment object's sampleData slot contains a 'type' column with exactly the expected count of 'QC' and 'sample' labels matching the documented injection sequence (e.g., two QC, four sample, two QC, four sample, two QC for 14 runs).
- No NA or missing values in the sampleData 'type' column; all loaded files are assigned a label.
- Length of sampleData 'type' vector equals the number of loaded spectra files; one-to-one correspondence verified.
- Downstream TARDIS results show separate tibbles/data.frames for QC run metrics vs. sample run metrics, indicating successful segregation by 'type' field.
- Manual spot-check of 2–3 file names against their assigned 'type' labels confirms alignment with the documented injection sequence.

## Limitations

- Relies on accurate documentation of the injection sequence; if the documented pattern does not match the actual run order, classification will be incorrect.
- Does not validate that QC or sample files have inherently different spectral properties; it is a metadata assignment only.
- No automated detection of QC vs. sample from file content or spectral characteristics; purely positional/sequence-based.
- If files are reordered or subsetted after loading, the sampleData 'type' labels must be manually updated to remain in sync.

## Evidence

- [full_text] MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values: "MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values corresponding to the 14"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an MsExperiment object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [results] a tibble that contains a feature table with the average metrics for each target in the QC runs: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
- [intro] Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [readme] Read the vignettes for a tutorial on how to use TARDIS: "**Read the vignettes** for a tutorial on how to use `TARDIS`"
