---
name: mzml-file-parsing-and-loading
description: Use when when you have centroided mzML format LC–MS files from multiple runs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3649
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - Spectra
  - R
  - MsExperiment
  - MsBackendMzR
  - MSConvert
  - TARDIS
  - Python
  - OpenMS
  - VIMMS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
- doi: 10.21105/joss.03990
  title: ''
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
- ViMMS is compatible with Python 3+
- Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  - 10.21105/joss.03990
  - 10.1021/acs.analchem.0c03895
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML File Parsing and Loading

## Summary

Parse and load centroided mzML LC–MS files into Spectra/MsExperiment objects with sample type metadata annotation to enable downstream targeted peak integration and quality assessment workflows. This skill bridges raw MS data acquisition and targeted compound analysis by establishing a unified, annotated spectral container.

## When to use

When you have centroided mzML format LC–MS files from multiple runs (e.g., 14 injections including QC and sample runs) that must be integrated into a single analysis object with run-level metadata (such as sample type or injection position) to distinguish QC from biological samples for quality control and peak integration downstream.

## When NOT to use

- Input files are not in centroided mzML format (e.g., profile-mode mzML, NetCDF, or proprietary vendor format) — convert and centroid first using MSConvert (ProteoWizard)
- Sample type metadata or injection order is unknown or unavailable — cannot reliably populate sampleData without documented correspondence
- Data has already been loaded into MsExperiment/Spectra and you only need to add or update sample type annotations — use direct sampleData assignment instead

## Inputs

- Directory path containing centroided .mzML files
- Vector of sample type labels ('QC' or 'sample') with length equal to number of mzML files
- Documented injection position order or metadata mapping file

## Outputs

- MsExperiment object containing all loaded spectra
- Populated sampleData slot with 'type' column distinguishing QC from sample runs
- Validated one-to-one file-to-type mapping

## How to apply

Read all .mzML files from the input directory using readMsExperiment() with the MsBackendMzR backend to create a single MsExperiment object containing all spectra. Populate the sampleData slot with a 'type' column containing 'QC' or 'sample' labels, ensuring strict one-to-one correspondence between the type vector and loaded files (e.g., positions 1–2 QC, 3–6 sample, 7–8 QC, 9–12 sample, 13–14 QC for a 14-run dataset). Validate alignment by confirming the MsExperiment contains exactly the expected number of files with no missing or mismatched type assignments. This establishes the annotated MsExperiment as input for polarity filtering, screening-mode target visibility checks, and final peak detection workflows.

## Related tools

- **Spectra** (R package that loads and represents MS spectral data; MsExperiment uses Spectra as its backend for storing and accessing spectra objects)
- **MsExperiment** (R container class that wraps Spectra objects and adds sampleData slot for run-level metadata annotation and file linkage)
- **MsBackendMzR** (Backend for MsExperiment/Spectra that enables reading of mzML files using the Rsamtools/rhdf5 family of functions)
- **MSConvert** (ProteoWizard tool to convert vendor raw MS files to mzML format and apply centroiding if needed prior to loading)
- **TARDIS** (Downstream R package that accepts MsExperiment objects as input for targeted peak integration and QC metric calculation) — https://github.com/pablovgd/TARDIS

## Examples

```
library(MsExperiment); library(Spectra); mse <- readMsExperiment('vignette_data/mzML/', backend = MsBackendMzR()); sampleData(mse)$type <- c(rep('QC', 2), rep('sample', 4), rep('QC', 2), rep('sample', 4), rep('QC', 2))
```

## Evaluation signals

- MsExperiment object length matches the number of input .mzML files (e.g., 14 spectra for 14 files)
- sampleData 'type' column contains only 'QC' or 'sample' values with no missing (NA) entries
- Length of sampleData matches number of files; no off-by-one or alignment errors detected when querying sampleData(mse)$type
- Spot-check: randomly sample one or two spectra and verify their assigned type matches the expected injection position order
- No warnings or errors during readMsExperiment() execution; all 14 files successfully parsed without timeout or format errors

## Limitations

- Requires input files to be already centroided and in valid mzML format; profile-mode mzML or unconverted vendor formats will fail or load incorrectly
- Sample type metadata must be manually curated and supplied by the user—the workflow does not auto-detect QC vs. sample from file naming or headers
- Large datasets (many files or high spectral density) may exceed available RAM or cause connection timeouts during download; the TARDIS README recommends increasing timeout settings using options(timeout = '300') or higher
- One-to-one file-to-type correspondence is strict; any mismatch or reordering of the type vector relative to file read order will propagate misannotation downstream

## Evidence

- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [intro] loads MS data as `Spectra` objects so it's easily integrated with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [other] MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values: "MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values"
- [readme] Since the package contains some example data, connection timeout is often an issue. You can increase your timeout setting in R using: options(timeout = '300'): "Since the package contains some example data, connection timeout is often an issue. You can increase your timeout setting in R using: options(timeout = '300')"
