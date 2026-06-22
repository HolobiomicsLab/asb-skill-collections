---
name: lcms-feature-classification
description: Use when you have an LCMS feature table annotated with MS2 spectral data and need to distinguish in-source fragments (mass loss patterns, same retention time, MS2 spectral relationships) from true metabolite features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - ISFrag
  - R
  - RStudio
  - devtools
  - XCMS
  - CAMERA
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

# LCMS Feature Classification

## Summary

Identify and classify in-source fragment (ISF) features in LCMS metabolite feature tables by detecting spectral and chromatographic relationships between parent and fragment ions. This skill distinguishes true ISF features from independent metabolites, enabling cleaner annotation and relationship mapping in untargeted metabolomics.

## When to use

Apply this skill when you have an LCMS feature table annotated with MS2 spectral data and need to distinguish in-source fragments (mass loss patterns, same retention time, MS2 spectral relationships) from true metabolite features. Use it to reduce redundancy and false positive identifications in large feature tables from DDA or fullscan LC-MS experiments.

## When NOT to use

- Feature table already contains pre-validated parent–fragment assignments or has been manually curated for ISF.
- Input is a single isolated mass spectrum or lacks retention time information; ISFrag requires chromatographic clustering.
- MS2 annotation data are absent or unreliable; ISFrag depends on spectral relationships to confidently predict ISF patterns.
- Data are from data-independent acquisition (DIA) without clear precursor–fragment isolation (XCMS can process DIA but ISFrag's MS2 assignment workflow is optimized for DDA).

## Inputs

- MS1 feature table (CSV: m/z, retention time, rtmin, rtmax, sample intensities)
- DDA mzXML file(s) containing MS2 spectra
- MSP-format spectral library for annotation
- Optionally: XCMS-extracted features from mzXML raw data

## Outputs

- Annotated feature table with ISF binary or confidence scores per feature
- ISF relationship tree(s) showing parent–fragment linkages
- Structured export file with labelled ISF predictions

## How to apply

Load your annotated feature table (m/z, retention time, rtmin, rtmax, and intensity columns) and MS2 spectral annotations into ISFrag. Apply the four-part workflow: (1) extract or import MS1 features using XCMS or custom CSV format, (2) assign MS2 spectra to features via DDA mzXML files and a standard library in msp format, (3) run ISFrag's Part 4 identification algorithm which detects ISF patterns by clustering features on mass and retention time, then scoring MS2 spectral relationships to infer parent–fragment links, and (4) export the annotated table with binary or confidence-scored ISF labels and relationship trees showing which features are fragments of which parents. The key decision point is choosing appropriate mass and retention time tolerances for clustering; ISFrag automates this but allows parameter tuning via help() functions.

## Related tools

- **ISFrag** (Performs in-source fragment identification via four-part workflow: MS1 extraction, MS2 annotation, ISF feature detection, and results export.) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment; ISFrag requires R version 4.0.0 or above.)
- **RStudio** (Recommended IDE for ISFrag installation and interactive analysis.)
- **devtools** (R package used to install ISFrag from GitHub repository.)
- **XCMS** (Optional upstream tool to extract MS1 features from mzXML files; supports DDA, DIA, and fullscan modes.) — https://rdrr.io/bioc/xcms/man/
- **CAMERA** (Optional adduct and isotope annotation for XCMS-only ISFrag analysis.)

## Examples

```
library(ISFrag); customFT <- custom.featuretable(ft_directory = "X:/Users/Sam_Shen/ISFtest20210127/RP(-)", ft_name = "NISTplasmaDDARP(-)1featuretable.csv"); # Then apply Part 3 MS2 annotation and Part 4 ISF identification (specific function calls require help() documentation)
```

## Evaluation signals

- Output feature table contains ISF labels (binary or confidence scores) for all input features with no missing values.
- Exported relationship tree shows parent–fragment links where fragments have mass loss ≤ parent mass, same or proximal retention time (within rtmin–rtmax bounds), and compatible MS2 spectra.
- Redundancy in feature table is reduced; the same metabolite is no longer represented by multiple rows (parent + independent fragments).
- No features are labeled as ISF if their MS2 spectra lack spectral similarity to any parent candidate or if retention times differ by >2–3× the feature's rtmin–rtmax window.
- Example invocation runs without errors and generates both a results feature table (.csv) and relationship tree output.

## Limitations

- ISFrag's performance depends on MS2 spectral quality and library coverage; poor MS/MS fragmentation or missing library entries will reduce ISF prediction confidence.
- CAMERA adduct and isotope annotation are only supported when using XCMS exclusively; custom feature tables cannot use CAMERA output.
- In-source fragmentation patterns vary by ionization mode and instrument; parameters may require tuning for different LC-MS platforms (e.g., ESI+ vs. ESI−).
- Features with very similar m/z and retention time (unresolved co-elutions) may be incorrectly clustered or assigned parent–fragment relationships.
- ISFrag does not distinguish between in-source fragments and true isobaric metabolites eluting at similar times; manual inspection of relationship trees is recommended for validation.

## Evidence

- [readme] ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.: "ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table."
- [other] ISFrag operates as a four-part workflow: MS1 feature extraction, MS2 annotation, identification of ISF features, and results export of labelled ISF predictions and relationship trees.: "ISFrag operates as a four-part workflow: MS1 feature extraction, MS2 annotation, identification of ISF features, and results export of labelled ISF predictions and relationship trees."
- [readme] To install ISFrag package R version 4.0.0 or above is required, and we recommend using RStudio to complete the installation and usage of ISFrag.: "To install ISFrag package R version 4.0.0 or above is required, and we recommend using RStudio to complete the installation and usage of ISFrag"
- [readme] In order for ISFrag to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities of features detected in each sample.: "In order for ISFrag to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an"
- [other] ISFrag applies Part 4 identification algorithm to detect in-source fragment patterns based on MS2 spectral relationships and retention time/mass clustering.: "Apply ISFrag's Part 4 identification algorithm to detect in-source fragment patterns based on MS2 spectral relationships and retention time/mass clustering."
- [readme] CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis.: "CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis."
