---
name: replicate-spectrum-aggregation-sample-level
description: Use when after frequency-based denoising has been applied to individual replicate spectra within each feature (via generate_denoised_spectra), you have a collection of denoised fragment ion lists per feature per scan.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - S4Vectors
  - readr
  - dplyr
  - magrittr
  - pbapply
  - Spectra
  - MsBackendMzR
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

# replicate-spectrum-aggregation-sample-level

## Summary

Aggregates denoised replicate MS/MS spectra from a single sample into a unified Spectra object and exports it to standardized mzML format with ion mode annotation. This consolidation step produces sample-level consensus spectra suitable for downstream metabolite annotation and comparative analysis.

## When to use

After frequency-based denoising has been applied to individual replicate spectra within each feature (via generate_denoised_spectra), you have a collection of denoised fragment ion lists per feature per scan. Use this skill when you need to: (1) consolidate all denoised replicates from a single sample into one portable spectral object, (2) preserve ion mode metadata (positive or negative) for library matching, or (3) produce final output mzML files for downstream metabolite annotation workflows.

## When NOT to use

- Denoising has not yet been performed — fragments still contain noise-associated ions below the frequency threshold; apply generate_denoised_spectra first.
- Individual replicate spectrum inspection or QC is the goal — sample-level aggregation obscures per-scan variation; work with per-replica .txt files instead.
- Output format is not mzML-compatible (e.g., your downstream tool requires raw netCDF or .mgf) — use format-specific exporters outside this skill.

## Inputs

- Denoised replicate spectra as individual .txt files (one per Feature_ID/Scan_ID), each containing m/z-sorted fragment ions that passed the frequency threshold
- Sample metadata including ion mode (positive or negative)
- Folder path specifying output directory structure

## Outputs

- Sample-level aggregated Spectra S4 object containing all denoised replicates
- mzML file per sample (written to <folder_path>/Denoised_spectra_mzML/) with ion mode specified

## How to apply

For each sample in the analysis, gather all denoised replicate spectra that were output as individual .txt files (sorted by m/z) from the generate_denoised_spectra step. Load these filtered fragment lists into a Spectra S4 object using the Spectra package, specifying the ion mode (pos or neg) as a metadata attribute. Aggregate all denoised replicates for that sample into a single Spectra object, preserving scan IDs and feature associations. Export the aggregated sample-level Spectra object to mzML format using the MsBackendMzR backend, which serializes the spectrum collection with standardized mzML XML structure and ion mode annotation. This produces one mzML file per sample in <folder_path>/Denoised_spectra_mzML/, ready for spectral library matching and metabolite identification.

## Related tools

- **Spectra** (S4 container for MS spectra; used to load denoised fragment data and manage sample-level aggregation before mzML export) — https://bioconductor.org/packages/release/bioc/html/Spectra.html
- **MsBackendMzR** (mzML serialization backend; exports aggregated Spectra object to standardized mzML XML format with ion mode metadata) — https://bioconductor.org/packages/release/bioc/html/MsBackendMzR.html
- **readr** (Reads individual denoised .txt spectrum files into memory for integration into Spectra object) — https://readr.tidyverse.org/
- **data.table** (Optional high-performance tabular operations for loading and organizing fragment data across replicates) — https://github.com/Rdatatable/data.table

## Examples

```
l5 = generate_denoised_spectra(l4, folder_path = "~/metabolomics/test_1/", ion_mode = "pos")
```

## Evaluation signals

- Output mzML file is valid XML and can be parsed by standard mzML validators or downstream MS software (e.g., pymzml, pwiz).
- Spectra object contains all expected samples and spectra with correct scan IDs and feature associations; length(output_spectra) > 0 and all metadata fields are populated.
- Ion mode attribute is correctly set (pos or neg) and matches the input sample classification.
- Fragment counts in aggregated spectra are consistent with the union of all input .txt file fragments; no spectra are duplicated or lost during aggregation.
- mzML file size and structure reflect the expected number of spectra and fragment ions; file can be read back into Spectra without parse errors.

## Limitations

- Aggregation assumes all denoised replicate .txt files for a sample are present and correctly named; missing or misnamed files will silently reduce the aggregated spectrum count.
- Ion mode must be specified a priori (pos or neg); the skill does not auto-detect ion mode from spectrum data and will tag all aggregated spectra with the same mode even if mixed-mode replicates exist.
- mzML export may lose non-standard metadata stored in intermediate Spectra objects if those fields are not explicitly supported by MsBackendMzR backend.
- Large sample sets with thousands of replicate spectra per feature may incur high memory overhead during Spectra object construction; no streaming or chunked export is implemented.

## Evidence

- [methods] For each sample, aggregate all denoised replicate spectra into a single Spectra object.: "For each sample, aggregate all denoised replicate spectra into a single Spectra object."
- [methods] Export the sample-level aggregated spectrum to .mzML format using Spectra and MsBackendMzR backend in <folder_path>/Denoised_spectra_mzML/ with ion mode specified (pos or neg).: "Export the sample-level aggregated spectrum to .mzML format using Spectra and MsBackendMzR backend in <folder_path>/Denoised_spectra_mzML/ with ion mode specified (pos or neg)."
- [readme] This step removes fragments with frequencies below the given threshold (denoising step): "#This step removed fragments with frequencies below the given threshold (denoising step)
l5 = generate_denoised_spectra(l4, folder_path, ion_mode = "pos")"
- [readme] It outputs a set of mzML files with the same number of samples but containing denoised MS/MS spectra.: "It outputs a set of mzML files with the same number of samples but containing denoised MS/MS spectra."
