---
name: nmr-peak-deconvolution
description: Use when when you have raw or processed 1D NMR spectra (FID or frequency-domain format) and need to extract individual peak identities and quantitative parameters in tabular form.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - SAND
  - NMRPipe
  - NMRBox
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
---

# nmr-peak-deconvolution

## Summary

Automatic deconvolution of 1D NMR spectra into peak tables using SAND, which applies baseline and phase correction followed by spectral decomposition to extract peak parameters (chemical shift, intensity, linewidth). The workflow is applicable to both simulated and experimental NMR datasets from diverse sample types (urine, worm, and others).

## When to use

When you have raw or processed 1D NMR spectra (FID or frequency-domain format) and need to extract individual peak identities and quantitative parameters in tabular form. Use this skill when manual peak picking is infeasible, when you need consistent automated processing across multiple spectra, or when working with experimental datasets like urine or worm NMR samples that have been validated in SAND's test suite.

## When NOT to use

- Input is already a validated peak table or annotation; re-deconvolution is redundant.
- Multi-dimensional NMR data (2D, 3D) without prior adaptation of SAND to those NMR data types (article notes SAND is planned for expansion to other NMR data types).
- Spectra requiring manual expert curation or where automatic deconvolution is expected to fail (e.g., severe overlap, very low signal-to-noise, or highly unusual phase distortions not correctable by NMRPipe).

## Inputs

- 1D NMR spectrum file (FID format or processed spectrum)
- NMR dataset (simulated or experimental)
- Raw or partially processed spectral data from supported sample types (urine, worm, or related biological matrices)

## Outputs

- Peak table (CSV or tabular format)
- Peak parameters: chemical shift, intensity, linewidth
- Deconvoluted spectrum annotation

## How to apply

Load the 1D NMR spectrum file (FID or processed spectrum) into SAND_V7 via the NMRBox interface. Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/. Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, extracting chemical shift, intensity, and linewidth parameters. The same workflow is designed to work on both simulated and experimental datasets. Validate that the peak table output contains the expected row count and is exported in structured format (CSV or tabular). The deconvolution rationale is grounded in automatic signal decomposition rather than manual annotation.

## Related tools

- **SAND** (Core deconvolution algorithm that implements automatic spectral decomposition and peak parameter extraction) — https://github.com/edisonomics/SAND
- **NMRBox** (Execution environment providing SAND_V7 interface, containerized deployment, and HPC integration (GACRC)) — https://nmrbox.org
- **NMRPipe** (Baseline correction and phase correction utilities called via pipe_scripts/ within SAND's processing pipeline)

## Evaluation signals

- Peak table is produced in expected structured format (CSV or tabular) with no missing or malformed rows.
- Peak parameters (chemical shift, intensity, linewidth) are present and numeric for all detected peaks.
- Row count in peak table is consistent with visual peak count in the spectrum (sanity check for over/under-detection).
- Deconvolution workflow completes without errors on both simulated and experimental datasets from the test suite (urine and worm datasets).
- Phase and baseline correction preprocessing steps complete successfully before deconvolution algorithm execution.

## Limitations

- SAND has been tested and validated only on urine and worm datasets; expansion to other datasets and NMR data types is planned but not yet complete.
- No changelog is available in the article or README, limiting traceability of algorithm updates and reproducibility across versions.
- Deconvolution accuracy is dependent on the quality of upstream baseline and phase correction; severely distorted spectra may yield unreliable peak tables.

## Evidence

- [intro] SAND implements automatic deconvolution for 1D NMR spectra.: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [intro] The workflow applies uniformly to both simulated and experimental datasets.: "Similar workflow works for simulated and expermental datasets."
- [intro] SAND has been validated on urine and worm datasets with plans for expansion.: "We have tested SAND on urine and worm dataset and will expand it to other new data."
- [methods] Baseline and phase correction are applied via NMRPipe integration.: "Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/."
- [methods] Deconvolution extracts peak parameters (chemical shift, intensity, linewidth).: "Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, generating peak parameters (chemical shift, intensity, linewidth)."
- [intro] SAND operates via NMRBox deployment and can run on HPC.: "SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org)."
