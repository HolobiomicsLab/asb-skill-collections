---
name: ms2-spectral-interpretation
description: Use when you have extracted an MS1 feature table (from XCMS or custom CSV with m/z, retention time, and intensity columns) and one or more DDA mzXML files from the same or related LC-MS runs, and you need to annotate features with MS2 spectral data and match them against a standard spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ISFrag
  - R
  - RStudio
  - devtools
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
- we recommend using RStudio to complete the installation and usage of ISFrag
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
---

# MS2 Spectral Interpretation

## Summary

Assign MS2 spectra to LC-MS1 features and perform library-based annotation to link detected ions to known metabolites. This skill is essential for converting raw mass spectral data into chemically interpretable compound identifications that enable downstream ISF detection and metabolite annotation.

## When to use

You have extracted an MS1 feature table (from XCMS or custom CSV with m/z, retention time, and intensity columns) and one or more DDA mzXML files from the same or related LC-MS runs, and you need to annotate features with MS2 spectral data and match them against a standard spectral library (in .msp format) to identify metabolites or functional groups.

## When NOT to use

- Input mzXML files are from DIA (data-independent acquisition) or full-scan mode without MS2 data; ISFrag requires DDA spectra for annotation.
- Your MS1 feature table is already pre-annotated with compound identities and MS2 data from an external tool; skip this step and proceed to ISF identification.
- You lack a validated spectral library in .msp format; library-free MS2 interpretation (e.g., neutral loss, fragmentation pattern matching) is not the scope of this workflow.

## Inputs

- MS1 feature table (CSV format: m/z, retention time [s], rtmin [s], rtmax [s], intensity columns)
- One or more DDA mzXML files containing MS2 spectra
- MS2 spectral library in .msp format

## Outputs

- Annotated feature table with MS2 spectral assignments and library match results
- MS2 spectra assigned to MS1 features with compound name, match score, and spectral metadata

## How to apply

Load one or more DDA mzXML files containing MS2 spectra into ISFrag using the MS2 annotation workflow. The mzXML files must be placed in a dedicated folder with no irrelevant files. ISFrag will match MS2 spectra to MS1 features using retention time and m/z alignment, then perform spectral library matching against a user-provided .msp standard library file. The annotation assigns compound names, match scores, and spectral relationships to each feature. Key parameters include retention time tolerance (for feature–spectrum matching) and cosine similarity or spectral similarity thresholds (for library matching); these control the stringency of compound assignment. Export the annotated feature table, which now contains MS2 annotations linked to each MS1 feature, ready for ISF identification in Part 4.

## Related tools

- **ISFrag** (R package that performs MS2 spectral assignment to MS1 features and annotation against .msp standard libraries) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment; ISFrag requires R ≥ 4.0.0)
- **RStudio** (Recommended IDE for installation and execution of ISFrag MS2 annotation workflow)
- **devtools** (R package used to install ISFrag from GitHub)

## Examples

```
# Load ISFrag and R environment
library(ISFrag)

# Part 3: MS2 Annotation (pseudocode based on README structure)
# Assign MS2 spectra from DDA mzXML files to the feature table and annotate against .msp library
MS2directory <- "X:/path/to/DDA/mzXML/files"
library_path <- "X:/path/to/spectral_library.msp"

# ISFrag MS2 annotation function (exact function name not fully specified in README excerpt)
# but follows the pattern of Part 3 workflow
annotated_FT <- ISFrag.MS2.annotation(
  featuretable = customFT,
  MS2directory = MS2directory,
  library = library_path
)

head(annotated_FT)  # View annotated feature table with MS2 data
```

## Evaluation signals

- All MS1 features in the output table carry MS2 spectral annotations (non-null match scores and compound names for matched features)
- Retention time alignment between MS1 features and MS2 spectra is within expected tolerance (typically <10–15 s drift); spot-check a few features visually
- Library match scores (e.g., cosine similarity) are above the configured threshold for accepted annotations; verify distribution and reject low-confidence matches
- The annotated feature table structure matches the input format with added columns for MS2 metadata (compound name, match score, spectral similarity)
- No features have been dropped during annotation; row count should equal or exceed the input feature table (new features may be added if multiple spectra match one feature)

## Limitations

- MS2 annotation accuracy depends entirely on the quality, comprehensiveness, and relevance of the .msp standard library; spectral libraries covering only a subset of metabolite classes will miss true compounds not in the library.
- Retention time tolerance and library match thresholds must be tuned for your chromatographic method and instrument; default parameters may yield false positives or false negatives if not validated for your LC-MS setup.
- CAMERA adduct and isotope annotation (optional enrichment in ISFrag) can only be applied when using XCMS-extracted features, not custom feature tables.
- DDA duty cycle and dynamic exclusion settings affect which precursor ions are fragmented; low-abundance or rapidly eluting features may not yield MS2 spectra.
- The number of mzXML files provided for MS2 annotation does not need to match the number used in MS1 feature extraction, which can lead to incomplete annotation if DDA files are from different experiments or conditions.

## Evidence

- [readme] One or multiple mzXML files from DDA analyses are needed to assign MS2 spectrum to features and perform annotation.: "One or multiple mzXML files from DDA analyses are needed to assign MS2 spectrum to features and perform annotation."
- [readme] In order for `ISFrag` to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities of features detected in each sample.: "it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities"
- [readme] CAMERA adduct and isotope annotation can only be used for `XCMS` ONLY `ISFrag` analysis.: "CAMERA adduct and isotope annotation can only be used for `XCMS` ONLY `ISFrag` analysis."
- [readme] Part 3: MS2 Annotation is where one or multiple mzXML files from DDA analyses are analyzed and MS2 spectra are assigned to features; the standard library used to perform annotation must be in msp format.: "the standard library used to perform annotation must be in msp format"
- [other] ISFrag operates as a four-part workflow: MS1 feature extraction, MS2 annotation, identification of ISF features, and results export of labelled ISF predictions and relationship trees.: "ISFrag operates as a four-part workflow: MS1 feature extraction, MS2 annotation, identification of ISF features, and results export"
