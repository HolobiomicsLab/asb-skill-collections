---
name: metabolite-feature-annotation
description: 'Use when after MS1 feature extraction from mzXML files when you have: (1) a feature table with m/z, retention time, and intensity values; (2) DDA (Data-Dependent Acquisition) mzXML files containing MS2 fragmentation spectra; and (3) a reference spectral library in MSP format.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - ISFrag
  - R
  - RStudio
  techniques:
  - LC-MS
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
  - build: coll_fermo_2_cq
    doi: 10.1038/s41467-024-50111-8
    title: FERMO
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-annotation

## Summary

Assign MS2 spectral annotations to LC-MS metabolite features by matching experimental fragmentation spectra against standard reference libraries. This skill bridges the gap between untargeted feature detection and metabolite identification in LCMS metabolomics workflows.

## When to use

Apply this skill after MS1 feature extraction from mzXML files when you have: (1) a feature table with m/z, retention time, and intensity values; (2) DDA (Data-Dependent Acquisition) mzXML files containing MS2 fragmentation spectra; and (3) a reference spectral library in MSP format. Use it to annotate features with compound identities and MS2 spectral relationships before ISF identification.

## When NOT to use

- Input data contains only MS1 spectra without DDA MS2 data — MS2 annotation requires fragmentation spectra
- Reference library is in non-MSP format (e.g., JSON, mzML) without prior conversion
- Feature table lacks required columns (m/z, retention time, rtmin, rtmax, intensities) or uses non-standard units (e.g., minutes instead of seconds)

## Inputs

- Feature table (CSV format with columns: m/z, retention time, rtmin, rtmax, sample intensities)
- DDA mzXML files containing MS2 fragmentation spectra
- Standard spectral library (MSP format)

## Outputs

- Feature table with MS2 spectral annotations
- Annotated feature table with MS2 spectral relationships

## How to apply

Load one or more DDA mzXML files (number and source independent of MS1 extraction) containing MS2 spectra into ISFrag. Match the experimental fragmentation spectra against a standard MSP-format reference library using ISFrag's MS2 annotation algorithm (Part 3). The algorithm assigns MS2 spectra to features and performs library matching to generate spectral annotations. Store the resulting feature table with annotated MS2 data for downstream ISF identification. Success depends on spectral quality, library coverage, and matching parameters (consult ISFrag documentation for similarity thresholds and scoring metrics).

## Related tools

- **ISFrag** (R package that performs MS2 annotation via Part 3 workflow; matches experimental MS2 spectra against MSP reference libraries) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment for ISFrag; version 4.0.0 or above required)
- **RStudio** (Recommended IDE for ISFrag installation and execution)

## Examples

```
# In R/RStudio after loading ISFrag: MS2_annotation_result <- ISFrag::MS2.annotation(MS2directory = "path/to/DDA/mzXML/folder", ft = feature_table, lib = "path/to/reference.msp")
```

## Evaluation signals

- Feature table contains new columns with MS2 spectral annotations and library match scores
- Each annotated feature has a corresponding MS2 spectrum identifier and match quality metric (e.g., cosine similarity or spectral matching score)
- No missing values in MS2 annotation columns for features with detected fragmentation spectra in the DDA data
- Consistency check: retention time of annotated features aligns with MS2 spectrum retention time windows in source mzXML files
- Annotation coverage: proportion of input features with successful MS2 matches is documented and reasonable given library size and sample complexity

## Limitations

- CAMERA adduct and isotope annotation can only be used for XCMS-only ISFrag analysis, not for custom feature tables
- MS2 annotation quality depends on spectral library completeness and accuracy; unknown compounds or non-library standards will not be annotated
- DDA mzXML files must be placed in a folder containing no other irrelevant mzXML files to avoid processing errors
- Number and source of DDA mzXML files do not need to correspond with MS1 extraction files, which may complicate experimental traceability

## Evidence

- [readme] One or multiple mzXML files from DDA analyses are needed to assign MS2 spectrum to features and perform annotation.: "One or multiple mzXML files from DDA analyses are needed to assign MS2 spectrum to features and perform annotation."
- [readme] The standard library used to perform annotation must be in msp format.: "In addition, the standard library used to perform annotation must be in msp format."
- [readme] All mzXML file(s) need to be placed in a separate folder containing no other irrelevant mzXML files.: "All mzXML file(s) need to be placed in a separate folder containing no other irrelevant mzXML files."
- [readme] The number of mzXML file(s) provided here does not need to correspond with the number of mzXML files used in the feature extraction step earlier.: "The number of mzXML file(s) provided here does not need to correspond with the number of mzXML files used in the feature extraction step earlier."
- [readme] CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis.: "CAMERA adduct and isotope annotation can only be used for XCMS ONLY ISFrag analysis."
