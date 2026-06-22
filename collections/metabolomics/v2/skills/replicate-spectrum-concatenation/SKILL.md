---
name: replicate-spectrum-concatenation
description: Use when after extracting raw MS/MS spectra from mzML files for individual features (identified by precursor m/z and retention time) and you have multiple replicate spectra for the same feature that need to be pooled for consensus analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - dures
  - S4Vectors
  - dplyr
  - preprocess
  - Spectra
  - mzR
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- devtools::install_github("BiosystemEngineeringLab-IITB/dures", auth_token = NULL)
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
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
---

# replicate-spectrum-concatenation

## Summary

Concatenate MS/MS spectra across all replicate injections for a given feature to create a unified spectrum object that pools signal across technical replicates. This step unifies fragmentation data before downstream denoising and consensus spectrum generation.

## When to use

Apply this skill after extracting raw MS/MS spectra from mzML files for individual features (identified by precursor m/z and retention time) and you have multiple replicate spectra for the same feature that need to be pooled for consensus analysis. Use when your goal is to aggregate replicate-level fragmentation data before applying TIC-based filtering or consensus spectrum generation.

## When NOT to use

- If spectra are already in a single pre-concatenated Spectra object or feature matrix
- If you are working with single-injection data or non-replicated experiments (no technical replicates to pool)
- If your input files are already consensus spectra rather than raw replicate-level MS/MS data

## Inputs

- folder path containing mzML files (raw mass spectrometry data)
- feature information file (Stats.txt or equivalent) with precursor m/z, retention time, and feature identifiers
- mass tolerance parameter (ppm, e.g., 5)
- retention time tolerance parameter (minutes, e.g., 0.1)

## Outputs

- list of Spectra objects (l1) indexed by feature ID
- each element is a concatenated Spectra object containing all replicate MS/MS spectra for that feature
- filtered feature list excluding features with no extracted MS/MS spectra

## How to apply

Load preprocessed spectra using the `preprocess()` function with specified m/z tolerance (e.g., 5 ppm) and retention time tolerance (e.g., 0.1 min) to extract MS/MS spectra from mzML files and automatically concatenate all replicates per feature into a single Spectra object. The function reads the feature list (e.g., Stats.txt) and performs m/z and RT matching to group all replicate spectra belonging to each feature. The output is a list (`l1`) containing concatenated Spectra objects indexed by feature ID, where each element represents the pooled replicate spectra for that feature. Verify concatenation by checking that the number of spectra in each feature element matches the expected replicate count.

## Related tools

- **preprocess** (reads mzML files, extracts MS/MS spectra matching feature m/z and RT, concatenates spectra for each feature into a Spectra object) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (Bioconductor S4 class for storing and manipulating mass spectrometry spectra data)
- **mzR** (reads and parses mzML files to extract raw MS/MS data)
- **S4Vectors** (provides S4 class infrastructure for Spectra object construction)
- **dures** (package implementing the full denoising workflow including replicate concatenation) — https://github.com/BiosystemEngineeringLab-IITB/dures

## Examples

```
l1 = preprocess(folder_path = "~/metabolomics/test_1/", tol_mz = 5, tol_rt = 0.1)
```

## Evaluation signals

- The returned list (l1) contains one Spectra object per feature with a non-zero number of spectra
- For each feature, the total number of spectra in the concatenated object equals the sum of spectra across all replicates
- Features without any extracted MS/MS spectra (based on m/z and RT tolerance) are removed from the output list
- Spectra are correctly indexed by feature ID and retain all metadata (precursor m/z, retention time, fragment m/z, intensity)
- The concatenated Spectra object preserves individual spectrum identifiers and replicate provenance information

## Limitations

- Concatenation accuracy depends on correct feature m/z and RT tolerance settings; loose tolerances may concatenate spectra from different features, tight tolerances may exclude true replicates
- Features with very few replicates (e.g., n=1) may not benefit from subsequent consensus denoising steps
- mzML file format and feature table format must match expected structure; incompatible file formats will cause parsing errors
- All replicates must be present in the same folder path; missing or misnamed files will result in incomplete concatenation

## Evidence

- [methods] The extracted spectra are then concatenated for all replicate spectra belonging to a given feature: "The extracted spectra are then concatenated for all replicate spectra belonging to a given feature"
- [readme] l1 <- preprocess(folder_path = folder_path, tol_mz = 25, tol_rt = 0.1): "l1 <- preprocess(folder_path = folder_path, tol_mz = 25, tol_rt = 0.1)#reads mzml files, prepares Stats file, extracts spectra and concatenates spectra"
- [methods] Features that do not have any MS/MS spectra extracted, based on the specified RT and m/z tolerance, are removed from the list: "Features that do not have any MS/MS spectra extracted, based on the specified *RT* and *m/z* tolerance, are removed from the list"
- [other] Load preprocessed spectra list (l1) containing concatenated MS/MS replicates for all features using the dures package: "Load preprocessed spectra list (l1) containing concatenated MS/MS replicates for all features using the dures package"
