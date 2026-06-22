---
name: spectral-data-object-construction
description: Use when you have a set of centroided .mzML LC-MS files from a targeted metabolomics or lipidomics experiment and need to represent them as a structured object that links raw spectra to sample-level metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - R
  - MsExperiment
  - MsBackendMzR
  - MSConvert
  - TARDIS
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
---

# spectral-data-object-construction

## Summary

Load centroided LC-MS data from mzML files into a Spectra or MsExperiment object and annotate sample metadata (run type, polarity, retention time windows) to enable downstream targeted peak integration and quality assessment workflows.

## When to use

You have a set of centroided .mzML LC-MS files from a targeted metabolomics or lipidomics experiment and need to represent them as a structured object that links raw spectra to sample-level metadata (e.g., QC vs. sample runs, ionization mode) for use with TARDIS or other Bioconductor mass spectrometry tools.

## When NOT to use

- Input files are already in profile (non-centroided) mode — centroiding must be performed first (e.g. via MSConvert).
- Data is already loaded as a feature table or intensity matrix — this skill is for raw spectral object construction, not quantification or aggregation.
- You are working with data from non-targeted or untargeted workflows where sample-level run type annotation is not available or not relevant.

## Inputs

- Directory of centroided .mzML files (one per LC-MS run)
- Metadata table or vector describing sample type (QC or sample), ionization mode, and run order

## Outputs

- MsExperiment object with Spectra slot populated by all mzML files
- sampleData slot containing one row per run with 'type' column (QC or sample) and other relevant metadata

## How to apply

Read all centroided .mzML files from a directory using the MsExperiment constructor with MsBackendMzR backend and the Spectra package. Construct a metadata table with one row per file, including columns for sample type (QC or sample), ionization polarity (positive or negative), and any expected retention-time windows for targets. Assign this metadata table to the sampleData slot of the MsExperiment object, ensuring one-to-one correspondence between files and rows. Validate that the object contains the correct number of spectra files and that sampleData columns align with the experimental design (e.g., alternating QC and sample runs as documented in the vignette: two QC, four sample, two QC, four sample, two QC).

## Related tools

- **MsExperiment** (Container for linking raw spectra data to sample metadata; accepts Spectra objects via the spectra slot)
- **Spectra** (Loads MS data as Spectra objects for integration with Bioconductor tools; reads mzML via MsBackendMzR)
- **MsBackendMzR** (Backend for reading mzML files into Spectra; part of the Spectra ecosystem)
- **MSConvert** (File conversion and centroiding of raw vendor formats to .mzML before spectral object construction)
- **TARDIS** (Downstream tool for targeted peak integration; accepts MsExperiment objects as input) — https://github.com/pablovgd/TARDIS

## Examples

```
library(MsExperiment); library(Spectra); mse <- readMsExperiment(files = list.files('vignette_data/mzML/', full.names=TRUE), backend = MsBackendMzR()); sampleData(mse)$type <- rep(c('QC', 'QC', 'sample', 'sample', 'sample', 'sample'), length.out=14); sampleData(mse)$polarity <- 'positive'; mse
```

## Evaluation signals

- MsExperiment object contains exactly N spectra files matching the number of input .mzML files in the directory.
- sampleData slot has N rows (one per file) and includes a 'type' column with only 'QC' or 'sample' values.
- sampleData row order matches the order of files as loaded, with no missing or misaligned type assignments.
- Spectra object is accessible via the spectra slot and can be queried for m/z, retention time, and intensity values.
- Run-level metadata (polarity, RT windows) is correctly populated in sampleData and can be used for subsetting or filtering (e.g., selecting positive-mode runs only).

## Limitations

- Input .mzML files must be centroided before loading; profile-mode or uncorrected retention-time data may cause peak detection and integration errors downstream.
- One-to-one correspondence between file order and sampleData metadata must be maintained manually; misalignment of file order and metadata will propagate errors to TARDIS and other downstream analyses.
- Connection timeouts may occur during installation of TARDIS and related dependencies; increasing R timeout setting (e.g., options(timeout = '300')) may be necessary.
- The skill assumes that sample type and ionization mode metadata are available and correctly documented; incomplete or conflicting metadata will result in failed screening or polarity filtering steps in TARDIS.

## Evidence

- [other] MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend: "MzML files are read into an MsExperiment object using readMsExperiment() with MsBackendMzR backend, then the sampleData 'type' column is populated with 'QC' or 'sample' values"
- [intro] Loads MS data as Spectra objects for integration with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [intro] MsExperiment can be used as input to TARDIS instead of file paths: "instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [intro] Input files must be centroided before use: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Polarity filtering is performed within TARDIS after spectral data object construction: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
