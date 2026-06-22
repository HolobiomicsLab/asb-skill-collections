---
name: nmr-workflow-pipeline-execution
description: Use when you have raw 1D NMR spectra (FID or processed spectrum files) and need to extract peak parameters (chemical shift, intensity, linewidth) in a tabular format for downstream metabolomic or structural analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
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

# nmr-workflow-pipeline-execution

## Summary

Execute the SAND automated workflow to process raw 1D NMR spectra (FID or processed format) through baseline correction, phase correction, and deconvolution to produce structured peak tables with chemical shift, intensity, and linewidth parameters. This skill applies uniformly to both simulated and experimental NMR datasets.

## When to use

You have raw 1D NMR spectra (FID or processed spectrum files) and need to extract peak parameters (chemical shift, intensity, linewidth) in a tabular format for downstream metabolomic or structural analysis. Use this skill when manual peak picking is impractical or when you require reproducible, automated deconvolution across multiple spectra (e.g., urine or biological samples).

## When NOT to use

- Input is already a manually validated or literature peak assignment table
- Spectrum contains severe artifacts or corrupted baseline that standard NMRPipe processing cannot correct
- You require 2D NMR deconvolution or other NMR data types beyond 1D (the tool has not yet been expanded to those modalities)

## Inputs

- 1D NMR spectrum file (FID format or processed spectrum)
- NMR dataset (urine, worm, or other biological sample)

## Outputs

- Peak table (CSV or tabular format)
- Peak parameters: chemical shift, intensity, linewidth

## How to apply

Load the 1D NMR spectrum file into the SAND processing pipeline via the NMRBox interface (SAND_V7). Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/. Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, extracting peak parameters (chemical shift, intensity, linewidth). Validate the output peak table for completeness and expected row count by checking the CSV or tabular format export. The same workflow is applicable to both simulated and experimental datasets without modification.

## Related tools

- **SAND** (Core deconvolution engine that performs automatic spectral decomposition into individual peaks and generates peak parameters) — https://github.com/edisonomics/SAND
- **NMRBox** (Execution environment and web interface (SAND_V7) for running the SAND pipeline on local, HPC, or cloud resources) — https://nmrbox.org
- **NMRPipe** (Integrated utility suite for baseline correction and phase correction of spectra via pipe_scripts/)

## Evaluation signals

- Output peak table is non-empty with row count matching expected number of peaks in the input spectrum
- All required columns are present: chemical shift, intensity, and linewidth with numeric values in expected ranges (e.g., chemical shift in ppm, positive intensity and linewidth values)
- Exported CSV or tabular file is well-formed and parseable without schema errors
- Workflow produces consistent peak tables when applied to the same spectrum (reproducibility check)
- Peak table can be successfully validated against simulated or experimental reference datasets (urine or worm) provided in the SAND tutorial

## Limitations

- SAND has been tested on urine and worm datasets; expansion to other dataset types and NMR data types (beyond 1D) is planned but not yet complete
- No changelog is available in the repository, making version-to-version compatibility and change history unclear
- Automated processing relies on NMRPipe baseline and phase correction; severely compromised spectra may require manual preprocessing before SAND deconvolution

## Evidence

- [readme] SAND automatic process and deconvolute 1D NMR spectra into peak tables.: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [readme] Similar workflow works for simulated and expermental datasets.: "Similar workflow works for simulated and expermental datasets."
- [other] Load the 1D NMR spectrum file (FID or processed spectrum format) into the SAND processing pipeline via NMRBox interface (SAND_V7). Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/.: "Load the 1D NMR spectrum file (FID or processed spectrum format) into the SAND processing pipeline via NMRBox interface (SAND_V7). Apply automatic spectral processing including baseline correction"
- [other] Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, generating peak parameters (chemical shift, intensity, linewidth).: "Execute the SAND deconvolution algorithm to decompose the spectrum into individual peaks, generating peak parameters (chemical shift, intensity, linewidth)."
- [readme] We have tested SAND on urine and worm dataset and will expand it to other new data. It will also be expand to other NMR data types.: "We have tested SAND on urine and worm dataset and will expand it to other new data. It will also be expand to other NMR data types."
