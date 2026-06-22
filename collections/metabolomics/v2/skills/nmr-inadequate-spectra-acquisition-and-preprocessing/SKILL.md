---
name: nmr-inadequate-spectra-acquisition-and-preprocessing
description: Use when when you have raw INADEQUATE NMR spectral data (e.g., from a query sample or library) and need to extract peak coordinates and intensities as a first step toward identifying metabolite peak networks or comparing against a metabolite database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - PyINETA
  - run_pyineta.py
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- pyINETA is a Python package
- python run_pyineta.py <options>
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
---

# nmr-inadequate-spectra-acquisition-and-preprocessing

## Summary

Reading, referencing, and peak-picking INADEQUATE NMR spectra to prepare them for metabolite network identification and database matching. This skill transforms raw INADEQUATE spectral data into picked peaks that can be clustered and filtered to identify metabolite signatures.

## When to use

When you have raw INADEQUATE NMR spectral data (e.g., from a query sample or library) and need to extract peak coordinates and intensities as a first step toward identifying metabolite peak networks or comparing against a metabolite database. Use this skill at the beginning of an INADEQUATE analysis pipeline before clustering or matching.

## When NOT to use

- Input spectra are already peak-picked or have been processed through a different NMR peak-picking pipeline; use this skill only at the raw spectral stage.
- Your goal is to perform 1D NMR analysis or work with single-pulse spectra rather than 2D INADEQUATE experiments.
- You have pre-clustered peak networks and only need to match them to a database; skip acquisition and preprocessing and move directly to the matching step.

## Inputs

- Raw INADEQUATE NMR spectra (NetCDF or manufacturer-specific format)
- Configuration file (INI format) with spectra paths and preprocessing parameters
- Reference or calibration parameters for chemical shift alignment

## Outputs

- Picked peaks: list of peak coordinates (chemical shifts) and intensities
- Preprocessed spectral data: referenced and baseline-corrected INADEQUATE spectra
- Peak picking artifacts or diagnostic plots (if figure generation enabled)

## How to apply

Invoke the PyINETA pipeline entry point (run_pyineta.py) with a configuration file specifying input spectra paths and preprocessing parameters. The pipeline first reads INADEQUATE spectra and applies basic shifting-based referencing to align chemical shift axes. Peak picking is then applied to detect and extract spectral peaks (coordinates and intensities) from the referenced spectra. The picked peaks form the foundation for downstream clustering into networks and matching against simulated or experimental INADEQUATE metabolite databases. Configure the pipeline via command-line options to specify input directory, output directory, and which processing steps to execute (e.g., 'load' and 'pick' steps for acquisition and preprocessing only).

## Related tools

- **PyINETA** (Python package that implements the full INADEQUATE analysis pipeline including spectra reading, referencing via basic shifting, peak picking, clustering, finding, matching, and plotting modules) — https://github.com/edisonomics/PyINETA
- **run_pyineta.py** (Entry point script that orchestrates execution of the INADEQUATE preprocessing and analysis pipeline with command-line configuration of input paths, output directory, and processing steps) — https://github.com/edisonomics/PyINETA

## Examples

```
python run_pyineta.py -c config.ini -o output_dir -s load+pick
```

## Evaluation signals

- Peak picking output contains a non-empty list of detected peaks with valid chemical shift coordinates and intensity values within the expected spectral range.
- Referencing step produces a consistent chemical shift alignment across replicate spectra or reference compounds (e.g., solvent peaks remain at their expected positions after basic shifting).
- Visual inspection of picking module output (plots if enabled) shows peaks aligned with visible spectral features and absence of spurious picks in noise regions.
- The number and distribution of picked peaks is consistent with expected metabolite complexity (e.g., a purified compound should yield a smaller, more clustered peak set than a complex mixture).
- Output files are successfully written to the specified output directory with expected file naming and format conventions.

## Limitations

- Basic shifting is used for referencing, which may not account for complex field inhomogeneity or non-linear chemical shift drift across the spectrum.
- Peak picking algorithm and sensitivity parameters are not explicitly detailed in the documentation; tuning may be required for spectra with unusual noise characteristics or peak densities.
- No changelog is provided in the repository, limiting documentation of fixes or algorithmic improvements across versions.
- Example 2 requires large raw input files (>100 Mb) that are not distributed in the repository, limiting direct reproducibility of a complex real-world example.

## Evidence

- [readme] pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [other] PyINETA reads and references INADEQUATE spectra using basic shifting in the picking module: "PyINETA reads and references INADEQUATE spectra using basic shifting in the picking module"
- [other] Apply peak picking to detect spectral peaks from the input spectra: "Apply peak picking to detect spectral peaks from the input spectra"
- [readme] It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound: "filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [readme] python <path_to_pyineta_repo>/run_pyineta.py -c config.ini <other options>: "python <path_to_pyineta_repo>/run_pyineta.py -c config.ini <other options>"
