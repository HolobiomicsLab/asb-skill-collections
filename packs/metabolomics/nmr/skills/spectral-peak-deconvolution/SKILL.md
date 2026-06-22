---
name: spectral-peak-deconvolution
description: Use when you have a raw 1D NMR spectrum (FID or processed format) from urine, worm, or other biological samples and need to extract peak positions, intensities, and linewidths as a tabular peak list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0153
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-deconvolution

## Summary

Automatically deconvolute 1D NMR spectra into individual peaks with quantified parameters (chemical shift, intensity, linewidth) and export as structured peak tables. This skill is essential when raw NMR spectra must be decomposed into component signals for metabolomic or structural analysis.

## When to use

Apply this skill when you have a raw 1D NMR spectrum (FID or processed format) from urine, worm, or other biological samples and need to extract peak positions, intensities, and linewidths as a tabular peak list. Use it for both simulated and experimental NMR datasets where automatic peak identification and quantification are required.

## When NOT to use

- Input is already a manually curated or validated peak table
- Spectrum contains severe artifacts or phase distortions that preprocessing cannot resolve
- Analysis requires 2D or higher-dimensional NMR data (SAND is currently limited to 1D spectra)

## Inputs

- 1D NMR spectrum file (FID format)
- 1D NMR spectrum file (processed spectrum format)
- Raw NMR spectral data

## Outputs

- Peak table (CSV or tabular format)
- Peak parameters (chemical shift, intensity, linewidth)
- Structured peak list

## How to apply

Load the 1D NMR spectrum file (FID or processed spectrum format) into the SAND processing pipeline via the NMRBox interface (SAND_V7). Apply automatic spectral preprocessing including baseline correction and phase correction using integrated NMRPipe utilities (pipe_scripts/). Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, which generates peak parameters including chemical shift, intensity, and linewidth. Validate the output peak table for completeness and expected row count. Export the deconvoluted peak table to a structured output file in CSV or tabular format. The rationale is that automatic deconvolution reduces manual peak picking bias and produces reproducible, quantified peak tables suitable for downstream metabolomic or comparative spectroscopy workflows.

## Related tools

- **SAND** (Core deconvolution algorithm that automatically decomposes 1D NMR spectra into individual peaks) — https://github.com/edisonomics/SAND
- **NMRBox** (Computational platform providing the SAND_V7 interface and execution environment for local, HPC, and cloud-based spectral processing) — https://nmrbox.org
- **NMRPipe** (Provides baseline correction, phase correction, and spectral preprocessing utilities integrated via pipe_scripts/)

## Evaluation signals

- Output peak table row count matches expected peak count for the given spectrum complexity
- Peak chemical shifts fall within expected ranges (0–10 ppm for typical 1D NMR)
- Linewidths and intensities are physically plausible and consistent across replicate runs
- No NaN or missing values in peak parameter columns (chemical shift, intensity, linewidth)
- Peak table schema matches expected CSV/tabular format with complete headers

## Limitations

- SAND has been tested primarily on urine and worm datasets; generalization to other sample types is under development
- Workflow is limited to 1D NMR spectra; expansion to other NMR data types is planned but not yet implemented
- No changelog is currently available, limiting traceability of algorithmic updates or bug fixes
- Requires access to NMRBox, GACRC HPC, or local installation; not suitable for offline or resource-constrained environments

## Evidence

- [intro] Workflow step: automatic processing and deconvolution: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [intro] Applicability across dataset types: "Similar workflow works for simulated and expermental datasets."
- [intro] Validated datasets and future scope: "We have tested SAND on urine and worm dataset and will expand it to other new data."
- [methods] Tool integration for preprocessing: "latest interface to NMRBox (SAND_V7), and interface to NMRPipe"
- [methods] Integration with NMRPipe utilities: "interface to NMRPipe (pipe_scripts/)"
- [intro] Deployment flexibility: "SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org)."
