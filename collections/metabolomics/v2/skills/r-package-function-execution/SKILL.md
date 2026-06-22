---
name: r-package-function-execution
description: Use when you have raw Bruker NMR spectral data files (1D 1H format) stored in a directory structure and need to prepare them for automated metabolite identification and quantification in ASICS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ASICS
  - R
derived_from:
- doi: 10.1021/acs.analchem.0c04232
  title: ASICS
- doi: 10.1007/s11306-017-1244-5
  title: ''
evidence_spans:
- The **R** package `ASICS` is a fully automated procedure to identify and quantify metabolites in $^1$H 1D-NMR spectra
- The **R** package `ASICS`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asics_cq
    doi: 10.1021/acs.analchem.0c04232
    title: ASICS
  dedup_kept_from: coll_asics_cq
schema_version: 0.2.0
---

# r-package-function-execution

## Summary

Execute R package functions in sequence to transform raw Bruker NMR spectral files into a Spectra object suitable for metabolite quantification. This skill chains importSpectraBruker() and createSpectra() as a required preprocessing pipeline before downstream ASICS quantification.

## When to use

You have raw Bruker NMR spectral data files (1D 1H format) stored in a directory structure and need to prepare them for automated metabolite identification and quantification in ASICS. Apply this skill when you have located Bruker data and must convert them to an in-memory Spectra object before calling ASICS quantification functions.

## When NOT to use

- Input is already a Spectra object — proceed directly to ASICS quantification.
- Data are in non-Bruker formats (e.g., mzML, NetCDF, CSV) — use alternative import functions or format conversion first.
- Bruker files are corrupted or missing required header information — data validation and repair are prerequisite.

## Inputs

- Bruker NMR spectral file directory (containing fid, acqu, procs files or equivalent Bruker format)
- System file path to example_spectra or custom Bruker data directory

## Outputs

- Data frame with imported spectral intensities and metadata
- Spectra object with metabolite quantification-ready structure

## How to apply

Load the ASICS R package, locate the Bruker data directory using system.file() or an explicit path, then call importSpectraBruker() with the directory path to import all spectral files into a data frame. From that data frame, call createSpectra() to construct the required Spectra object. This two-step workflow is mandatory: the Spectra object is the only input format accepted by downstream ASICS quantification. Verify that the returned Spectra object has non-empty slots and that the number of imported spectra matches the count of Bruker files in the source directory.

## Related tools

- **ASICS** (R package providing importSpectraBruker, createSpectra, and ASICS quantification functions for end-to-end NMR metabolite identification and quantification) — https://github.com/GaelleLefort/ASICS
- **R** (Runtime environment for executing ASICS package functions and managing Spectra objects)

## Examples

```
library(ASICS); dir_path <- system.file('extdata/example_spectra', package='ASICS'); spectra_df <- importSpectraBruker(dir_path); spectra_obj <- createSpectra(spectra_df)
```

## Evaluation signals

- Returned data frame contains at least one row per Bruker file and columns for spectral intensities across the chemical shift range.
- Spectra object is non-NULL and contains slots with spectral matrix, sample metadata, and chemical shift vector.
- Number of rows in data frame equals number of Bruker files imported from the source directory.
- Spectra object can be passed without error to downstream ASICS() quantification function.
- No NA or infinite values in spectral intensity matrix; chemical shift vector is monotonic and spans expected ppm range (e.g., 0–10 ppm for 1H NMR).

## Limitations

- Function requires Bruker files to follow standard directory and file naming conventions; non-standard Bruker output structures may fail silently or raise import errors.
- Large spectral datasets (many samples or high resolution) may consume substantial memory during data frame and Spectra object construction.
- No built-in validation of spectral quality, baseline correction, or referencing; preprocessing such as baseline correction and phase adjustment are assumed to be performed by Bruker acquisition or post-processing.
- importSpectraBruker() imports all spectra in the specified directory; selective import requires manual file subsetting or pre-filtering the directory contents.

## Evidence

- [other] import_workflow: "Data are imported in a data frame from Bruker files with the `importSpectraBruker` function"
- [other] spectra_object_requirement: "from the data frame, a `Spectra` object is created. This is a required step for the quantification"
- [other] quantification_input: "Identification and quantification of metabolites can now be carried out using only the function `ASICS`"
- [other] asics_package_scope: "The **R** package `ASICS` is a fully automated procedure to identify and quantify metabolites in $^1$H 1D-NMR spectra"
