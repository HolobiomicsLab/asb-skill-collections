---
name: retention-time-intensity-data-extraction
description: Use when you have xcms-processed LC-MS data with detected misaligned
  feature groups and need to recover the underlying raw retention time–intensity profiles
  for each feature and sample combination prior to realignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - xcms
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an
  alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
  dedup_kept_from: coll_ncgtw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaa037
  all_source_dois:
  - 10.1093/bioinformatics/btaa037
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-intensity-data-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and organize raw LC-MS retention time and intensity profiles from xcms-processed source files for specific feature groups using the ncGTW loadProfile() function. This skill is essential for reconstructing raw profile data needed to realign misaligned features detected by xcms.

## When to use

Apply this skill when you have xcms-processed LC-MS data with detected misaligned feature groups and need to recover the underlying raw retention time–intensity profiles for each feature and sample combination prior to realignment. Specifically, use it after ncGTW has identified features with sufficiently small p-values and disjoint sample subsets that require realignment.

## When NOT to use

- Input data has not yet been processed by xcms; loadProfile() expects xcms output as upstream input.
- No misaligned features have been detected by ncGTW; extraction is unnecessary if alignment quality is already acceptable.
- Raw instrument data files (mzML, NetCDF) are available but xcms processing has not been run; use xcms preprocessing first.

## Inputs

- file paths to xcms-processed LC-MS profile data
- excluGroups table (detected misaligned feature groups with sample subsets)
- xcms feature grouping output

## Outputs

- ncGTWinputs object (structured list of raw retention time–intensity profiles organized by feature and sample identifiers)
- validated profile dictionary accessible by feature and sample keys

## How to apply

Parse file paths pointing to xcms-processed profiles and a table of detected feature groups (excluGroups) as input parameters to loadProfile(). The function reads the xcms output and constructs the ncGTWinputs object, which organizes raw profiles hierarchically by feature and sample identifiers. This structured representation enables downstream pairwise alignments and warping function estimation. Validate that the returned object contains the expected list structure with profiles accessible via feature and sample keys before proceeding to realignment. The key rationale is that loadProfile() bridges xcms output and ncGTW's reference-free multiple alignment algorithm by organizing raw chromatographic data in a form amenable to individualized per-compound warping functions.

## Related tools

- **ncGTW** (Provides loadProfile() function to extract and structure raw profiles from xcms output into ncGTWinputs object for realignment) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS alignment tool whose output (misaligned features, profiles) is parsed by loadProfile() as input)
- **R** (Programming language in which ncGTW and loadProfile() are implemented)

## Examples

```
ncGTWinputs <- loadProfile(file_paths, excluGroups)
```

## Evaluation signals

- ncGTWinputs object is returned as a list with non-empty structure containing profiles indexed by feature and sample
- All feature groups in excluGroups input are present in the output object with corresponding raw profiles
- Profile values (retention time and intensity pairs) are numeric and within expected ranges for LC-MS data
- Number of profiles in output matches the product of number of features and number of samples in the input groups
- No missing or null values for profiles corresponding to feature–sample combinations listed in excluGroups

## Limitations

- loadProfile() strictly depends on xcms output format; changes to xcms processing pipeline or file organization will break input compatibility.
- The function assumes file paths are correctly formatted and accessible; missing or corrupted source files will cause extraction to fail.
- Only profiles for features listed in excluGroups are extracted; full raw data recovery is not possible if the feature detection step was incomplete.
- Performance and memory usage scale with the number of features and samples; very large datasets may exceed available memory.

## Evidence

- [other] loadProfile() function to read xcms-processed profiles and construct the ncGTWinputs object, which organizes raw profiles by feature and sample identifiers: "Call loadProfile() function from the ncGTW R package to read xcms-processed profiles and construct the ncGTWinputs object, which organizes raw profiles by feature and sample identifiers."
- [other] loadProfile() accepts file paths and detected feature groups (excluGroups) as inputs: "loadProfile() accepts file paths and detected feature groups (excluGroups) as inputs and outputs ncGTWinputs, a structured object containing the raw profiles needed for downstream realignment"
- [intro] xcms may have misaligned features that can be identified and realigned with ncGTW: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments."
- [readme] ncGTW is a plug-in of xcms developed to detect and fix bad alignments in LC-MS data: "The purpose of ncGTW is to detect and fix the bad alignments in the LC-MS data. Currently, ncGTW is implemented in a R-package as a plug-in for XCMS."
- [readme] ncGTW performs all possible pairwise alignments with structure information: "ncGTW performs all possible pairwise alignments between each two sample with the structure information in the dataset."
