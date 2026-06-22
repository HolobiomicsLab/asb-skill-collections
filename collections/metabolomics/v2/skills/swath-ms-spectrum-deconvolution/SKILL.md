---
name: swath-ms-spectrum-deconvolution
description: Use when you have SWATH-MS raw data (mzML or vendor format) from an untargeted metabolomics experiment and need to identify metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - DecoMetDIA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b02655
  title: DecoMetDIA
evidence_spans:
- DecoMetDIA was developed to process SWATH-MS based data for metabolomics.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_decometdia_cq
    doi: 10.1021/acs.analchem.9b02655
    title: DecoMetDIA
  dedup_kept_from: coll_decometdia_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02655
  all_source_dois:
  - 10.1021/acs.analchem.9b02655
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# swath-ms-spectrum-deconvolution

## Summary

Deconvolutes overlapping MS/MS spectra from SWATH-MS (Sequential Window Acquisition of All Theoretical Mass Spectra) data to recover individual component spectra for each precursor ion, enabling accurate metabolite identification in untargeted metabolomics. This skill resolves the fundamental challenge that SWATH-MS acquires multiplexed spectra across broad isolation windows, making direct spectral matching impossible.

## When to use

Apply this skill when you have SWATH-MS raw data (mzML or vendor format) from an untargeted metabolomics experiment and need to identify metabolites. SWATH-MS deliberately multiplexes many precursor ions within each isolation window to increase data completeness, but this multiplexing prevents direct library matching. Use this skill specifically when spectral deconvolution is required to separate co-fragmented ions before database searching or when you observe overlapping fragment peaks at the same retention time across multiple precursor isolation windows.

## When NOT to use

- Input is already a feature table or peak intensity matrix — deconvolution operates on raw spectral data, not pre-aggregated features
- Data were acquired with targeted MS/MS (e.g., selected reaction monitoring or parallel reaction monitoring) where no multiplexing occurred
- Spectra are already deconvoluted or from non-multiplexed acquisition methods (e.g., traditional DDA or high-resolution data-independent acquisition without isolation windows)

## Inputs

- SWATH-MS raw data files (mzML format or vendor binary format)
- Precursor ion isolation window definitions (m/z ranges and collision energies)
- Retention time alignment metadata (optional, for improved grouping)

## Outputs

- Deconvoluted MS/MS spectra in MGF format
- Deconvoluted spectra in mzTab format with precursor m/z, retention time, and intensity annotations
- Quality control metrics per spectrum (peak count, intensity distribution statistics)

## How to apply

Load SWATH-MS raw data files into DecoMetDIA and apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra. Execute DecoMetDIA's multiplexed spectrum decomposition algorithm, which mathematically separates overlapping MS/MS spectra into individual component spectra by modeling the contribution of each precursor ion to the observed multiplexed spectrum. Export deconvoluted spectra in MGF or mzTab format with associated precursor m/z, retention time, and intensity annotations. Validate output quality by checking for appropriate peak counts per spectrum (typically ≥3 significant peaks), reasonable intensity distributions (avoiding flat or single-peak spectra), and mass accuracy within the instrument's calibration tolerance (typically <5 ppm for high-resolution mass spectrometers).

## Related tools

- **DecoMetDIA** (R package that implements the spectral deconvolution algorithm for multiplexed MS/MS spectra separation) — https://github.com/ZhuMSLab/DecoMetDIA

## Examples

```
devtools::install_github("ZhuMSLab/DecoMetDIA"); library(DecoMetDIA); deconvoluted <- decoMS(rawdata = "sample.mzML", mz.window = 25, rt.window = 30)
```

## Evaluation signals

- Deconvoluted spectra exhibit peak counts consistent with known metabolite fragmentation patterns (≥3 significant peaks per spectrum)
- Mass accuracy of fragment peaks is within instrument tolerance (typically <5 ppm for high-resolution instruments)
- Intensity distributions show realistic ratios (no single-peak spectra; no artificially flat distributions indicating algorithmic failure)
- Precursor m/z and retention time annotations in output match source SWATH-MS isolation windows and elution times
- Library search performance improves after deconvolution compared to raw multiplexed spectra (higher cosine similarity scores or match counts against metabolite databases)

## Limitations

- Performance depends on sufficient spectral resolution and mass accuracy to distinguish overlapping precursor ions
- Deconvolution quality degrades when many precursors (>10) co-elute within a single isolation window, making algorithmic separation ambiguous
- Requires accurate knowledge of isolation window boundaries and collision energy settings from the acquisition method
- Tool is licensed under CC BY-NC-ND 4.0, restricting commercial use and derivative works

## Evidence

- [readme] DecoMetDIA was developed to process SWATH-MS based data for metabolomics: "DecoMetDIA was developed to process SWATH-MS based data for metabolomics."
- [intro] SWATH-MS multiplexes many precursor ions, making direct matching impossible until deconvolution: "Deconvolution of Multiplexed MS/MS Spectra for Metabolite Identification in SWATH-MS-Based Untargeted Metabolomics"
- [other] Workflow includes loading raw data, applying isolation and retention time windowing, performing spectral decomposition, and exporting annotated spectra: "1. Load SWATH-MS raw data files (mzML or vendor format) into DecoMetDIA. 2. Apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra. 3. Perform spectral"
- [other] Output validation checks peak counts, intensity distributions, and mass accuracy: "Validate deconvoluted spectra quality by checking for appropriate peak counts, intensity distributions, and mass accuracy."
- [readme] DecoMetDIA requires Rcpp compilation and is installed as an R package: "DecoMetDIA was developed as an R package with Rcpp code. Compiling is needed when installing."
