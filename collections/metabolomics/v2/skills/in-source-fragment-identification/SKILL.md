---
name: in-source-fragment-identification
description: Use when you have an LCMS feature table (from XCMS, MS-DIAL, MZmine2, or other feature extraction software) with m/z, retention time, and intensity columns, plus MS2 spectral annotations from DDA data, and you need to identify which features are in-source fragments rather than distinct metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ISFrag
  - R
  - RStudio
  - XCMS
  - CAMERA
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# in-source-fragment-identification

## Summary

ISFrag is an R package workflow for identifying and annotating in-source fragment (ISF) features in LCMS metabolite feature tables by leveraging MS1 feature clustering, MS2 spectral relationships, and retention time proximity. Apply this skill when you have an annotated LCMS feature table and need to detect which detected features are fragments of parent ions generated during ionization, not independent metabolites.

## When to use

You have an LCMS feature table (from XCMS, MS-DIAL, MZmine2, or other feature extraction software) with m/z, retention time, and intensity columns, plus MS2 spectral annotations from DDA data, and you need to identify which features are in-source fragments rather than distinct metabolites. This prevents inflated feature counts and erroneous metabolite annotations in downstream analysis.

## When NOT to use

- Your input is already an identified metabolite list (not a raw feature table); ISFrag operates on feature-level data, not post-identification results.
- You lack MS2 spectral data; ISFrag's ISF detection relies on MS2 fragmentation patterns and cannot operate on MS1-only feature tables.
- Your retention time data is not in seconds or your feature table lacks m/z, rt, rtmin, rtmax columns in that exact order; ISFrag will fail to parse malformed input.

## Inputs

- LCMS feature table (CSV format): columns in order of m/z, retention time (seconds), retention time minimum, retention time maximum, sample intensity columns
- MS2 spectral annotations (from DDA mzXML files or pre-computed spectral library matches)
- Optionally: mzXML files from DDA acquisition if performing de novo MS2 annotation within ISFrag

## Outputs

- Annotated feature table with ISF binary labels or confidence scores for each feature
- ISF relationship tree (parent–fragment mappings with supporting evidence)

## How to apply

Load your feature table (containing m/z, retention time bounds, and sample intensities) and MS2 annotations into ISFrag in R. ISFrag's Part 4 identification algorithm detects ISF patterns by clustering features on m/z and retention time proximity, then examining MS2 spectral relationships (shared fragment ions, parent-daughter mass differences) to assign binary or confidence-scored ISF labels. The workflow outputs an annotated feature table with ISF predictions and a relationship tree showing parent–fragment connections. Key decision: ensure your feature table has exactly the required column structure (m/z, rt, rtmin, rtmax, followed by intensity columns) and all retention times in seconds, otherwise ISFrag will fail to parse the input.

## Related tools

- **XCMS** (MS1 feature extraction from mzXML files; provides aligned feature table input to ISFrag) — https://rdrr.io/bioc/xcms/man/
- **CAMERA** (Optional adduct and isotope annotation for XCMS-extracted features prior to ISFrag ISF identification)
- **R** (Runtime environment; ISFrag requires R ≥ 4.0.0)
- **devtools** (R package installer; required to install ISFrag from GitHub)
- **RStudio** (Recommended IDE for ISFrag installation and execution)

## Examples

```
library(ISFrag); customFT <- custom.featuretable(ft_directory="./data", ft_name="feature_table.csv"); isf_result <- ISFrag(customFT, MS2_annotation_data); head(isf_result$ISF_labels)
```

## Evaluation signals

- Output feature table contains all input features plus ISF label/confidence columns with no missing values or parsing errors.
- ISF relationship tree shows parent features with higher m/z and higher intensity than assigned daughter fragments, consistent with in-source fragmentation chemistry.
- Clustered features (assigned as ISF parent–daughter pairs) share retention time windows (rtmin–rtmax overlap or proximity within expected chromatographic peak width) and exhibit mass differences corresponding to known neutral losses (e.g., 18 for H₂O, 44 for CO₂, 132 for phosphorylation).
- Visual inspection of MS2 spectra for parent and assigned fragment features confirms shared major fragment ions (cosine similarity or spectral dot product above typical threshold ~0.7).
- Downstream metabolite annotation count decreases compared to using the unfiltered feature table, and annotation confidence increases for remaining features.

## Limitations

- CAMERA adduct and isotope annotation are only compatible with XCMS-extracted features, not custom feature tables from other software.
- ISFrag requires properly formatted CSV input with exact column order (m/z, rt, rtmin, rtmax, then intensities); malformed or reordered columns will cause parse failures.
- Retention time data must be in seconds; ISFrag does not auto-convert minutes or other units.
- ISF detection relies on MS2 data quality and spectral library matching accuracy; poor MS2 annotation or incomplete spectral libraries will reduce ISF identification sensitivity.
- ISFrag is tuned for DDA-mode LCMS; DIA or data-independent acquisition modes are supported for feature extraction but ISF identification sensitivity may differ.

## Evidence

- [readme] ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.: "ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table."
- [intro] ISFrag's Part 4 identification algorithm detects in-source fragment patterns based on MS2 spectral relationships and retention time/mass clustering.: "Apply ISFrag's Part 4 identification algorithm to detect in-source fragment patterns based on MS2 spectral relationships and retention time/mass clustering."
- [readme] Feature table must contain m/z, retention time, min retention time, max retention time, then intensity columns in that exact order, with all retention times in seconds.: "In order for ISFrag to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an"
- [readme] R version 4.0.0 or above is required to use ISFrag.: "To install ISFrag package R version 4.0.0 or above is required"
- [intro] ISFrag outputs include an annotated feature table with ISF predictions and a structured relationship tree.: "Export the annotated feature table with ISF predictions as a structured output file."
- [readme] CAMERA adduct and isotope annotation can only be used for XCMS-only ISFrag analysis.: "Note: CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis."
