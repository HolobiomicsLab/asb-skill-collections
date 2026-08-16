---
name: metabolomics-data-standardization
description: Use when you have raw 1D NMR spectral data (urine, worm, or other biological samples) that needs to be converted into peak tables for metabolite identification and quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - SAND
  - NMRPipe
  - NMRBox
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.3c03078
  title: SAND
evidence_spans:
- Any user is welcome to make new modificaitons on the SAND code, particularly its version for NMRBox
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

# metabolomics-data-standardization

## Summary

Automatic processing and deconvolution of 1D NMR spectra into standardized peak tables using SAND, enabling uniform downstream analysis of both simulated and experimental metabolomics datasets. This skill converts raw NMR spectral data into quantitative peak assignments suitable for comparative and statistical analysis.

## When to use

Apply this skill when you have raw 1D NMR spectral data (urine, worm, or other biological samples) that needs to be converted into peak tables for metabolite identification and quantification. Use SAND when you require automatic, reproducible deconvolution without manual peak picking, and when your workflow targets NMRBox, local, or HPC environments.

## When NOT to use

- Input data are already in peak-table or feature-matrix format (e.g., already deconvoluted); SAND adds no value to pre-processed outputs.
- Your NMR data type is not 1D or is a non-standard variant (e.g., 2D COSY, HSQC) unless SAND has been explicitly expanded to support that type.
- Your analysis requires manual, interactive peak picking or domain-expert curation; SAND's automatic workflow is not designed for iterative expert refinement.

## Inputs

- 1D NMR spectral data files (raw FID or processed spectra in standard NMR formats)
- Urine or worm NMR datasets
- Simulated or experimental NMR spectra

## Outputs

- Peak tables (tabular format with chemical shift, intensity, and peak assignments)
- Standardized metabolomics feature matrices suitable for downstream statistical analysis

## How to apply

Install SAND_V7 via NMRBox or locally following the provided installation scripts at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh. Load your 1D NMR spectrum files into SAND's automatic processing pipeline, which applies spectral deconvolution algorithms to separate overlapping peaks and assign intensities. Execute the full workflow (preprocessing → deconvolution → peak table generation) on your dataset. Verify that peak-table output is produced in the expected format—typically containing chemical shift, intensity, and peak assignment columns. The same workflow is applicable to both simulated and experimental datasets, so no parameter adjustment is needed between data types.

## Related tools

- **SAND** (Primary NMR deconvolution engine performing automatic spectral processing and peak table generation) — https://github.com/edisonomics/SAND
- **NMRBox** (Containerized environment and web service platform for running SAND (SAND_V7 interface)) — https://nmrbox.org
- **NMRPipe** (Spectral processing pipeline with which SAND integrates for advanced preprocessing steps)

## Evaluation signals

- Peak-table files are successfully generated in expected format for all input spectra (urine, worm, or other datasets).
- Peak table columns include chemical shift, intensity, and peak assignments with no missing or null values in core fields.
- Output peak tables from experimental and simulated datasets conform to the same schema and numeric ranges, demonstrating workflow consistency.
- Deconvoluted peaks are non-overlapping and chemically plausible (chemical shifts within 0–12 ppm for 1H NMR; no negative intensities).
- Re-running the same input spectrum through SAND produces identical or near-identical peak tables, confirming reproducibility.

## Limitations

- SAND has been tested on urine and worm datasets; expansion to other dataset types and NMR modalities (beyond 1D) is planned but not yet complete.
- No changelog is currently available in the repository, making it difficult to track which versions fixed specific deconvolution issues.
- The skill requires either NMRBox account access, HPC setup (e.g., GACRC), or local installation; no web-based graphical interface is mentioned for non-expert users.

## Evidence

- [readme] SAND automatic process and deconvolute 1D NMR spectra into peak tables. Similar workflow works for simulated and expermental datasets.: "SAND automatic process and deconvolute 1D NMR spectra into peak tables. Similar workflow works for simulated and expermental datasets."
- [readme] We have tested SAND on urine and worm dataset and will expand it to other new data.: "We have tested SAND on urine and worm dataset and will expand it to other new data."
- [intro] SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org).: "SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org)."
- [other] Set up the NMRBox environment and install SAND_V7 by following the installation script at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh. Load the urine dataset NMR spectra into SAND and run the automatic processing and deconvolution workflow to generate peak tables.: "Set up the NMRBox environment and install SAND_V7 by following the installation script at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh. Load the urine dataset NMR spectra into SAND and run the"
