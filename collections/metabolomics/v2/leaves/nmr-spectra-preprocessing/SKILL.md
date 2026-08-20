---
name: nmr-spectra-preprocessing
description: Use when when you have raw 1D NMR spectroscopic data (urine, worm, or
  other biological samples) in a format supported by NMRBox/NMRPipe and need to generate
  peak tables with automatic phasing, baseline correction, and spectral deconvolution
  without manual intervention.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - SAND
  - NMRPipe
  - NMRBox
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c03078
  title: SAND
evidence_spans:
- Any user is welcome to make new modificaitons on the SAND code, particularly its
  version for NMRBox
- interface to NMRPipe (pipe_scripts/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sand_cq
    doi: 10.1021/acs.analchem.3c03078
    title: SAND
  dedup_kept_from: coll_sand_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03078
  all_source_dois:
  - 10.1021/acs.analchem.3c03078
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectra-preprocessing

## Summary

Automatic preprocessing and deconvolution of 1D NMR spectra into peak tables using the SAND workflow. This skill transforms raw NMR spectroscopic data into quantitative peak assignments suitable for metabolomic or structural analysis.

## When to use

When you have raw 1D NMR spectroscopic data (urine, worm, or other biological samples) in a format supported by NMRBox/NMRPipe and need to generate peak tables with automatic phasing, baseline correction, and spectral deconvolution without manual intervention.

## When NOT to use

- Input is already a peak table or preprocessed feature matrix—skill is designed for raw spectra only.
- Dataset is 2D or multidimensional NMR (COSY, HSQC, etc.)—SAND has only been tested on 1D spectra.
- Spectra require specialized manual phasing or baseline handling outside SAND's automatic workflow.

## Inputs

- raw 1D NMR spectral data in NMRBox/NMRPipe-compatible format
- NMR acquisition parameters (e.g., field strength, pulse sequence metadata)

## Outputs

- peak table (columnar format with chemical shift, intensity, line width)
- processed/deconvolved NMR spectrum

## How to apply

Load the raw 1D NMR spectra into SAND_V7 via the NMRBox interface or local installation. Execute the automatic processing workflow, which applies phasing, baseline correction, and deconvolution to generate peak tables in standard format. The workflow is designed to operate identically on both simulated and experimental datasets. Verify that peak-table outputs are produced in the expected columnar format with chemical shift, intensity, and line width assignments. The same procedural steps apply across dataset types, reducing manual parameter tuning.

## Related tools

- **SAND** (core automatic processing and deconvolution engine for 1D NMR spectra) — https://github.com/edisonomics/SAND
- **NMRBox** (web and HPC deployment platform providing latest SAND_V7 interface and environment) — https://nmrbox.org
- **NMRPipe** (underlying spectral processing pipeline with scripting interface integrated into SAND)

## Evaluation signals

- Peak table output is generated in expected columnar format (chemical shift, intensity, line width) for all input spectra.
- Number and position of detected peaks are consistent with known metabolite assignments for the dataset type (e.g., urine metabolites).
- Baseline is flat and phasing is correct across the spectral window (visual inspection of processed spectrum).
- Output file structure and naming convention match SAND documentation and match outputs from prior successful runs on the same dataset.
- Processing completes without errors or manual intervention required for both experimental and simulated datasets using the same workflow.

## Limitations

- SAND has only been tested on urine and worm datasets; performance on other sample types is not yet documented.
- Workflow is limited to 1D NMR spectra; expansion to other NMR data types is planned but not yet implemented.
- No changelog is available, limiting traceability of algorithm changes between SAND versions.
- Automatic workflow may not handle edge cases (e.g., highly overlapped peaks, severe baseline distortion) without manual intervention.

## Evidence

- [intro] SAND automatically processes and deconvolutes 1D NMR spectra into peak tables: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [intro] Workflow applies uniformly across simulated and experimental datasets: "Similar workflow works for simulated and expermental datasets."
- [intro] Tested on urine and worm datasets with plans for expansion: "We have tested SAND on urine and worm dataset and will expand it to other new data."
- [intro] Available via NMRBox with installation and tutorial support: "SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org). We provide multiple [tutorials](https://github.com/edisonomics/SAND/tree/main/tutorial)"
- [methods] Integration with NMRPipe pipeline scripts: "latest interface to NMRBox (SAND_V7), and interface to NMRPipe"
