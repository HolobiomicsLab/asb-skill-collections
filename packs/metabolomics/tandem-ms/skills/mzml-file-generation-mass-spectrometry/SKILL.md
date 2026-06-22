---
name: mzml-file-generation-mass-spectrometry
description: Use when after frequency-based denoising and sample-level aggregation of replicate MS/MS spectra, when you need to export denoised spectra to a standardized, vendor-independent format compatible with spectral matching pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
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
  - MsBackendMzR
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

# mzML File Generation for Mass Spectrometry

## Summary

This skill exports denoised MS/MS spectra aggregated at the sample level into standardized mzML format files using Bioconductor's Spectra package and MsBackendMzR backend, preserving ion mode metadata (positive or negative ionization). It is essential for converting processed tandem mass spectrometry data into portable, machine-readable formats suitable for downstream metabolite annotation and spectral library matching.

## When to use

Apply this skill after frequency-based denoising and sample-level aggregation of replicate MS/MS spectra, when you need to export denoised spectra to a standardized, vendor-independent format compatible with spectral matching pipelines. Specifically, use this when you have a sample-level aggregated Spectra object and need to produce mzML files ready for metabolite library matching or data sharing.

## When NOT to use

- Do not use this skill if your spectra are already in mzML format and you only need to filter or denoise within that format — use preprocessing or filtering steps instead.
- Do not use this skill if you need to preserve raw, unnormalized spectra or have not yet applied frequency-based denoising — aggregate and denoise first.
- Do not use this skill if your output target is a different format (e.g., mgf, MS2, or proprietary vendor formats) — use format-specific export functions.

## Inputs

- sample-level aggregated Spectra object (from label_individual_spectrum output)
- ion_mode parameter (character: 'pos' or 'neg')
- folder_path (character, directory where output mzML files will be written)

## Outputs

- mzML files (one per sample) in <folder_path>/Denoised_spectra_mzML/
- mzML file exports contain denoised MS/MS spectra with ion mode annotation

## How to apply

After completing intra-spectrum grouping, fragment frequency labeling, and frequency-threshold filtering (default threshold = 0.1), aggregate all denoised replicate spectra belonging to each sample into a single Spectra object. Export each sample-level aggregated spectrum to mzML format using the Spectra package with the MsBackendMzR backend, specifying the ion mode (pos or neg) to preserve ionization metadata. Store the mzML files in a standardized output directory structure (e.g., <folder_path>/Denoised_spectra_mzML/) with descriptive file naming. Verify that the exported mzML files preserve fragment m/z values (sorted), intensity values, and spectrum-level metadata (precursor m/z, retention time, sample name, ion mode).

## Related tools

- **Spectra** (R/Bioconductor package for storing, manipulating, and exporting mass spectrometry spectra objects in multiple formats including mzML) — https://bioconductor.org/packages/Spectra
- **MsBackendMzR** (Bioconductor backend driver for Spectra that enables mzML I/O using mzR and netCDF libraries) — https://bioconductor.org/packages/MsBackendMzR
- **S4Vectors** (Bioconductor package providing S4 class infrastructure used by Spectra for spectrum metadata management) — https://bioconductor.org/packages/S4Vectors
- **dplyr** (Data manipulation utility used in the broader DuReS workflow for metadata preparation and filtering) — https://github.com/tidyverse/dplyr

## Examples

```
l5 = generate_denoised_spectra(l4, folder_path, ion_mode = "pos")
```

## Evaluation signals

- All mzML output files exist in the specified output directory with correct naming (sample identifiers match input feature metadata).
- mzML files are valid and readable by standard mass spectrometry software (e.g., can be opened by Proteowizard, MSFragger, or similar tools).
- Exported spectra contain correct ion mode annotation (positive or negative as specified) in file metadata.
- Fragment m/z and intensity values in the mzML file match the sorted, filtered values from the denoised Spectra object (compare via readSpectra() round-trip verification).
- Spectrum-level metadata (precursor m/z, retention time, scan ID) are preserved and consistent with source label_individual_spectrum output.

## Limitations

- The generate_denoised_spectra function requires that the input Spectra object has already been labeled with fragment recurrence frequencies; it does not recalculate frequencies independently.
- Ion mode must be explicitly specified (pos or neg) and is applied uniformly to all spectra in the export; mixed-mode spectra require separate export calls.
- File system permissions and disk space must be available in the output directory; no automatic fallback or compression is built in.
- The mzML export does not include charge state inference or adduct annotations beyond ion mode; downstream annotation steps are required for metabolite matching.
- Large sample sets or very high-density spectra may encounter memory constraints during Spectra object aggregation, particularly on systems with <8 GB RAM.

## Evidence

- [methods] Export each denoised replicate spectrum to .txt format in <folder_path>/Denoised_spectra_txt/<Feature_ID>/<Scan_ID>.txt using readr or data.table. 5. For each sample, aggregate all denoised replicate spectra into a single Spectra object. 6. Export the sample-level aggregated spectrum to .mzML format using Spectra and MsBackendMzR backend in <folder_path>/Denoised_spectra_mzML/ with ion mode specified (pos or neg).: "Export the sample-level aggregated spectrum to .mzML format using Spectra and MsBackendMzR backend in <folder_path>/Denoised_spectra_mzML/ with ion mode specified (pos or neg)."
- [readme] This step removed fragments with frequencies below the given threshold (denoising step) l5 = generate_denoised_spectra(l4, folder_path, ion_mode = "pos"): "l5 = generate_denoised_spectra(l4, folder_path, ion_mode = "pos")"
- [methods] For each sample, aggregate all denoised replicate spectra into a single Spectra object.: "For each sample, aggregate all denoised replicate spectra into a single Spectra object."
- [methods] After applying all five steps of the package, only 9 fragments remained from the original spectrum: "After applying all five steps of the package, only 9 fragments remained from the original spectrum"
- [methods] The first step of the workflow involves reading mzML files and extracting MS/MS spectra within the specified *m/z* and *RT* tolerance: "The first step of the workflow involves reading mzML files and extracting MS/MS spectra within the specified *m/z* and *RT* tolerance"
