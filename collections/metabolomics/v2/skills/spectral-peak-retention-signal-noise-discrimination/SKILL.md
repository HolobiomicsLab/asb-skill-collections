---
name: spectral-peak-retention-signal-noise-discrimination
description: Use when when you have replicate MS/MS spectra for the same feature (precursor m/z and retention time) and need to distinguish genuine fragment ions from noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - S4Vectors
  - readr
  - dplyr
  - magrittr
  - pbapply
  - Spectra
  - data.table
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dures_cq
    doi: 10.1021/acs.analchem.5c01726
    title: DuReS
  dedup_kept_from: coll_dures_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01726
  all_source_dois:
  - 10.1021/acs.analchem.5c01726
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-retention-signal-noise-discrimination

## Summary

Applies a user-defined frequency threshold to MS/MS fragment ions from replicate spectra, retaining signal-associated peaks and filtering noise-associated fragments based on their recurrence frequency across replicates. This discriminates true analyte fragments from random or spurious peaks.

## When to use

When you have replicate MS/MS spectra for the same feature (precursor m/z and retention time) and need to distinguish genuine fragment ions from noise. Apply this skill after consensus spectrum generation and fragment frequency labeling, when you have calculated recurrence frequencies across replicates and need to produce clean, denoised spectra for downstream annotation or matching.

## When NOT to use

- Input spectra lack replicate replicates or fragment frequency annotations from consensus spectrum generation
- Single-acquisition MS/MS spectra without replicate information — frequency-based filtering requires recurrence data across replicates
- Already-denoised or vendor-processed spectra where noise filtering has been applied upstream

## Inputs

- Labeled spectrum object (l4) with fragment recurrence frequencies
- Aggregate spectrum list containing replicate MS/MS spectra
- User-defined frequency threshold parameter (numeric, default 0.1)
- Ion mode specification (pos or neg)
- Output folder path for export

## Outputs

- Denoised replicate spectra in .txt format (per Feature_ID/Scan_ID)
- Sample-level aggregated Spectra object
- Denoised spectra in .mzML format (per sample, ion mode specified)

## How to apply

Load the labeled spectrum object (l4) containing replicate MS/MS spectra annotated with fragment recurrence frequencies from the consensus step. Iterate through each feature's replicate spectra and apply a user-defined frequency threshold (default = 0.1) to filter fragments, retaining only those with frequency ≥ custom_threshold. The rationale is that true signal fragments appear consistently across multiple replicates, while noise fragments appear sporadically. Sort filtered fragments by m/z, export each denoised replicate spectrum to .txt format, then aggregate all denoised spectra per sample into a single Spectra object and export to .mzML format with the appropriate ion mode (pos or neg) using the MsBackendMzR backend.

## Related tools

- **Spectra** (Load, manipulate, and export MS spectra objects; aggregate replicate spectra and write to .mzML format with MsBackendMzR backend) — https://bioconductor.org/packages/Spectra/
- **readr** (Export denoised replicate spectra to .txt format)
- **data.table** (Efficient filtering and iteration over fragment data during threshold application)
- **pbapply** (Parallel application of frequency filtering across features with progress reporting)
- **S4Vectors** (S4 object manipulation for spectrum metadata and frequency annotations)
- **dplyr** (Data manipulation and filtering of fragments by frequency threshold)

## Examples

```
l5 = generate_denoised_spectra(l4, folder_path = "~/metabolomics/test_1/", ion_mode = "pos")
```

## Evaluation signals

- Fragment count per replicate spectrum decreases after threshold application (e.g., 98 → 81 fragments after grouping and filtering steps)
- All retained fragments have frequency ≥ user-defined threshold; no fragments below threshold remain in output
- Output .txt files contain only m/z-sorted fragments with non-zero signal intensity
- .mzML output is valid and readable by standard mass spectrometry software (Spectra, MS-DIAL, etc.)
- Ion mode (pos/neg) matches input specification and is correctly encoded in output metadata

## Limitations

- Frequency threshold is user-defined; optimal cutoff varies by experimental design and noise characteristics (see parameter tuning vignette for optimization workflow)
- Requires multiple replicate spectra per feature; features with <2 replicates cannot be reliably denoised by frequency-based approach
- May over-filter or under-filter depending on threshold choice; Pareto front analysis and Wilcoxon rank-sum testing recommended to identify optimal frequency cutoff
- Only filters fragments within individual spectra; does not perform cross-feature denoising or global normalization

## Evidence

- [methods] The denoising mechanism applies a user-defined frequency threshold (default = 0.1) to retain signal fragments from consensus spectra, filtering out noise-associated fragments based on their recurrence frequency across replicates.: "applies a user-defined frequency threshold (default = 0.1) to retain signal fragments from consensus spectra, filtering out noise-associated fragments based on their recurrence frequency across"
- [methods] Load the aggregate spectrum list (l4) containing replicate MS/MS spectra annotated with fragment recurrence frequencies. Iterate through each feature and retrieve its associated replicate spectra from the labeled spectrum object. For each replicate scan within a feature, apply the user-defined frequency threshold (default 0.1) to filter fragments, retaining only those with frequency ≥ custom_threshold.: "Load the aggregate spectrum list (l4) containing replicate MS/MS spectra annotated with fragment recurrence frequencies. Iterate through each feature and retrieve its associated replicate spectra"
- [methods] Sort filtered fragments by m/z value and export each denoised replicate spectrum to .txt format in <folder_path>/Denoised_spectra_txt/<Feature_ID>/<Scan_ID>.txt using readr or data.table. For each sample, aggregate all denoised replicate spectra into a single Spectra object. Export the sample-level aggregated spectrum to .mzML format using Spectra and MsBackendMzR backend in <folder_path>/Denoised_spectra_mzML/ with ion mode specified (pos or neg).: "Sort filtered fragments by m/z value and export each denoised replicate spectrum to .txt format in <folder_path>/Denoised_spectra_txt/<Feature_ID>/<Scan_ID>.txt using readr or data.table. For each"
- [readme] This step removed fragments with frequencies below the given threshold (denoising step): "This step removed fragments with frequencies below the given threshold (denoising step)"
- [readme] A detailed walkthrough is available through an example analysis using an open-source experimental tandem mass spectrometry dataset... DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra.: "DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra"
