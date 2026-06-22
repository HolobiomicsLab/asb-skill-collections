---
name: metabolite-identifier-mapping-to-lipids
description: Use when you have (1) peak-picked LC-MS AIF features in a feature table with m/z and retention time, (2) corresponding xcmsSet and RAMClustR pseudo-MS/MS spectral objects from centroid-mode raw data, and (3) a research goal to identify which features are lipids rather than other metabolite classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  - LipidPos
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identifier-mapping-to-lipids

## Summary

Annotate LC-MS All-ion fragmentation features to lipid identities by matching fragment ion patterns against LipidPos ion fragment libraries using the annotateRC function. This skill produces ranked candidate lipid annotations with matching scores, enabling confident assignment of lipid classes and chain compositions to detected m/z features.

## When to use

Apply this skill when you have (1) peak-picked LC-MS AIF features in a feature table with m/z and retention time, (2) corresponding xcmsSet and RAMClustR pseudo-MS/MS spectral objects from centroid-mode raw data, and (3) a research goal to identify which features are lipids rather than other metabolite classes. Use it specifically when you need rank-ordered candidate lipid annotations with fragment-matching scores to support lipid structural assignment.

## When NOT to use

- Input features are from targeted MS/MS acquisition (not All-ion fragmentation) — use database matching on full experimental spectra instead.
- Feature table lacks corresponding xcmsSet and RAMClustR objects — annotateRC requires both peak-picked data and pseudo-MS/MS spectra.
- Research goal is non-lipid metabolite annotation (e.g., drug metabolites, amino acids) — use general metabolite fragment libraries or spectral databases instead.

## Inputs

- feature table (targetTable.csv format with m/z, retention time, and intensity columns)
- xcmsSet object (peak-picked LC-MS AIF data in centroid mode)
- RAMClustR object (pseudo-MS/MS spectra with fragment ions and intensities)
- LipidPos ion fragment library (database of lipid fragmentation patterns)

## Outputs

- ranked candidate lipid annotations per feature (lipid class and chain composition)
- matching scores for each candidate annotation
- annotated feature table with rank-1 lipid assignment
- visualization of matched ions for each candidate (optional)

## How to apply

Load the feature table (targetTable.csv format), xcmsSet, and RAMClustR objects into R. Configure the LipidPos fragment library as the annotation database source. Execute the annotateRC function to match fragment ions from each feature against the LipidPos library, generating candidate annotations ranked by matching score. The function compares pseudo-MS/MS spectra (ions and intensities) against library entries; candidates with higher matching scores indicate better fragment-pattern alignment. Inspect the rank-1 candidate for each feature and validate by visualizing matched ions in the spectrum. Save results to a user-specified directory for downstream analysis or manual curation.

## Related tools

- **MetaboAnnotatoR** (R package performing feature-to-lipid annotation via annotateRC function and LipidPos library matching) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (preprocessing and peak-picking of raw LC-MS AIF chromatograms in centroid mode to produce peak-picked data object)
- **RamClustR** (clustering and pseudo-MS/MS spectrum generation from AIF data to produce spectral object input to annotateRC)
- **LipidPos** (ion fragment library database queried by annotateRC for lipid candidate matching)

## Examples

```
library(MetaboAnnotatoR); annotateRC(RC_object, xcmsSet_object, targetTable.csv, library='LipidPos', output_dir='./lipid_annotations')
```

## Evaluation signals

- Three or more of six tested features receive lipid annotations (benchmark from the paper: 3/6 features successfully annotated to lipids including LPC(14:0)).
- Rank-1 candidate annotation has a matching score substantially higher than lower-ranked candidates, indicating confident fragmentation pattern alignment.
- Matched ions displayed in spectra visualization correspond visually to the rank-1 lipid candidate's expected fragmentation pattern.
- Feature m/z values and rank-1 lipid assignments are chemically plausible (e.g., LPC(14:0) at 468.3095 m/z corresponds to [M+H]+ adduct mass).
- Annotation results are reproducibly saved to the user-specified output directory in tabular and/or graphical format.

## Limitations

- Requires centroid-mode LC-MS AIF data; profile-mode data must be converted beforehand.
- Annotation success depends on feature fragmentation pattern coverage in the LipidPos library; novel lipid structures or unusual adducts may lack library entries.
- No changelog available in the repository, limiting transparency on version history and algorithm updates.
- Performance is constrained by the completeness and accuracy of the fragment library; lipid classes or chain lengths absent from LipidPos will not be detected.
- Pseudo-MS/MS spectra from RAMClustR clustering may artificially combine fragments from co-eluting features, introducing false candidate annotations.

## Evidence

- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [other] three features receive lipid annotations, with LPC(14:0) assigned as the rank 1 annotation for feature 3 (468.3095 m/z, 82.92009 s): "three features receive lipid annotations, with LPC(14:0) assigned as the rank 1 annotation for feature 3 (468.3095 m/z, 82.92009 s)"
- [intro] a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data: "a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data"
- [intro] annotations can be performed using the *annotateRC* function: "annotations can be performed using the *annotateRC* function"
- [intro] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [intro] It is possible to visualise the spectra containing the matched ions to each candidate: "It is possible to visualise the spectra containing the matched ions to each candidate"
