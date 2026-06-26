---
name: r-data-structure-manipulation
description: Use when when xcms has produced misaligned feature groups and you need
  to extract raw LC-MS profiles from source files into a structured format acceptable
  by ncGTW's realignment functions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
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
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
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

# R data structure manipulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and validate structured R objects (e.g., ncGTWinputs lists) that organize raw LC-MS profile data by feature and sample identifiers for downstream alignment analysis. This skill bridges xcms-processed output and ncGTW's graph-based realignment workflow.

## When to use

When xcms has produced misaligned feature groups and you need to extract raw LC-MS profiles from source files into a structured format acceptable by ncGTW's realignment functions. Specifically, after detecting which feature groups are misaligned (via p-value thresholds and disjoint sample subsets), use this skill to load and organize the corresponding raw profiles for constraint-based pairwise alignment.

## When NOT to use

- Input profiles are already aligned by xcms with high confidence (no detected misalignments).
- Raw LC-MS data files are unavailable or in incompatible format (must be xcms-processed profiles).
- excluGroups table is empty or contains no qualifying features (p-value and sample disjointness criteria not met).

## Inputs

- file paths (xcms-processed LC-MS profile files)
- excluGroups table (detected misaligned feature groups)
- sample metadata (sample identifiers)

## Outputs

- ncGTWinputs object (structured list of raw profiles keyed by feature and sample)

## How to apply

Call the loadProfile() function from the ncGTW R package, providing file paths to xcms-processed LC-MS data and the excluGroups table (detected misaligned feature groups) as input parameters. The function parses these inputs and constructs ncGTWinputs, a list object that organizes raw profiles by feature and sample keys. Validate the output by confirming the list structure contains profiles accessible by both feature and sample identifiers, ensuring all misaligned features have corresponding raw data entries ready for the reference-free pairwise alignment step.

## Related tools

- **ncGTW** (Provides loadProfile() function to extract and structure raw profiles from xcms output for realignment) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS data processing; produces profiles that loadProfile() reads and ncGTW realigns)
- **R** (Execution environment for ncGTW package and data structure manipulation)

## Examples

```
ncGTW_inputs <- loadProfile(file_paths = my_xcms_files, excluGroups = detected_misaligned_features)
```

## Evaluation signals

- ncGTWinputs object is a valid list structure with feature-level and sample-level keys accessible via $ or [[ ]] operators.
- All profiles in excluGroups (detected misaligned features) have corresponding entries in the ncGTWinputs output.
- Profile data types and dimensions match expected raw LC-MS format (e.g., retention time vectors, intensity matrices per feature-sample pair).
- No missing or NA values in profile entries for features and samples present in excluGroups.
- Object can be passed directly to ncGTW's realignment functions without reformatting errors.

## Limitations

- loadProfile() requires xcms-processed profiles in a specific format; incompatible or corrupted source files will cause parsing failure.
- The excluGroups table must contain only features meeting both the p-value significance threshold (derived from higher-resolution alignment) and sample subset disjointness criterion; features not meeting these criteria cannot be loaded.
- Memory constraints may arise when loading large numbers of samples or long LC-MS runs; no built-in filtering or subsetting within loadProfile() is documented.
- No changelog is available, limiting visibility into backward compatibility or schema changes across ncGTW versions.

## Evidence

- [other] loadProfile() function definition and role: "Call loadProfile() function from the ncGTW R package to read xcms-processed profiles and construct the ncGTWinputs object, which organizes raw profiles by feature and sample identifiers."
- [other] Input and output specifications: "loadProfile() accepts file paths and detected feature groups (excluGroups) as inputs and outputs ncGTWinputs, a structured object containing the raw profiles needed for downstream realignment"
- [other] Validation criterion for output structure: "Validate that the output object contains the expected list structure with profiles accessible by feature and sample keys."
- [readme] ncGTW detection and realignment context: "ncGTW can detect the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [intro] xcms misalignment scenario: "xcms may have misaligned features that can be identified and realigned with ncGTW for more accurate downstream analysis such as peak-regrouping or peak-filling."
