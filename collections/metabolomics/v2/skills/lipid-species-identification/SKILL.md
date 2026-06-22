---
name: lipid-species-identification
description: Use when you have centroid-mode LC–MS AIF chromatograms processed by xcms and RamClustR (or equivalent), a feature table with m/z and retention time coordinates, and you need to resolve individual lipid species identities with confidence scores and fragmentation evidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - xcms
  - RamClustR
  - R (≥4.5.0)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Species Identification

## Summary

Automated identification of individual lipid species (e.g., LPC(14:0)) from LC–MS All-Ion Fragmentation (AIF) features by matching experimental MS/MS fragment patterns against ion fragment databases using MetaboAnnotatoR. This skill enables rank-ordered candidate annotations with supporting ion-matching evidence, suitable for untargeted metabolomics workflows.

## When to use

You have centroid-mode LC–MS AIF chromatograms processed by xcms and RamClustR (or equivalent), a feature table with m/z and retention time coordinates, and you need to resolve individual lipid species identities with confidence scores and fragmentation evidence. Use this skill when feature-level m/z alone is insufficient and you want to leverage MS/MS fragmentation patterns to disambiguate isomers and assign lipid acyl chain composition.

## When NOT to use

- Input data are already in profile (continuous) mode rather than centroid mode; MetaboAnnotatoR requires centroid spectra.
- You lack MS/MS fragmentation data (e.g., only MS1 precursor m/z and retention time); this skill requires all-ion fragmentation or product ion spectra.
- Your lipid class is not represented in the selected fragment database; check available libraries before annotation.

## Inputs

- Centroid-mode LC–MS AIF raw chromatograms (mzML, NetCDF, or raw instrument format)
- xcms or RamClustR processed feature list with m/z, retention time, and intensity
- Feature table (CSV or data frame, e.g., targetTable.csv format)
- Lipid fragment ion database (e.g., LipidPos library in MetaboAnnotatoR)

## Outputs

- annotations object with rankedResult containing rank-ordered lipid candidate names
- Annotation scores and matched ion counts for each candidate per feature
- plotResultSpec visualization showing experimental spectrum with annotated fragment ions

## How to apply

Load your centroid LC–MS AIF data and feature table (targets) into R and call MetaboAnnotatoR's annotateRC function, specifying the LipidPos fragment library (or other relevant lipid database) as the reference. The function compares experimental fragment ion patterns from each feature against library spectra, scoring matches by number of matched ions and spectral similarity. Extract ranked candidate annotations from the rankedResult object in the returned annotations object; the rank-1 candidate represents the highest-confidence lipid species assignment. Inspect matched ion counts and annotation scores to validate biological plausibility (e.g., confirm that neutral loss patterns are consistent with the proposed acyl chain structure). Visualize matched spectra using plotResultSpec to confirm fragment assignments.

## Related tools

- **MetaboAnnotatoR** (Core annotation engine that matches experimental AIF fragment patterns against lipid ion fragment databases and ranks candidate lipid species identities.) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream LC–MS peak detection and feature extraction; produces the processed centroid chromatograms that MetaboAnnotatoR uses as input.)
- **RamClustR** (Upstream clustering and RT alignment of xcms-detected features; output used directly by MetaboAnnotatoR for annotation.)
- **R (≥4.5.0)** (Runtime environment for MetaboAnnotatoR and dependent packages (BiocManager, mzR).)

## Examples

```
library(MetaboAnnotatoR); annotations <- annotateRC(RCobject, MS1_features, use_library='LipidPos'); top_lipid <- annotations$rankedResult[[1]]$annotation_name[1]
```

## Evaluation signals

- The rank-1 candidate annotation is consistent with the observed feature m/z and known lipid mass rules (e.g., for LPC(14:0) [M+H]+ the predicted m/z matches the observed 468.3095 within instrument tolerance).
- Matched ion count is non-zero and aligns with expected neutral losses and fragmentation pathways for the annotated lipid species (e.g., loss of fatty acid as carboxylic acid or ketene for lysophospholipids).
- Annotation score (annotation evidence metric) is above a project-defined threshold (not specified in the article but typically cosine similarity or spectral match score); documents show this can be accessed from rankedResult.
- Replicate features with the same lipid annotation show consistent rank-1 assignment across replicates, indicating reproducibility.
- Visual inspection of plotResultSpec output shows reasonable alignment of experimental peaks with predicted fragment ions for the top-ranked lipid.

## Limitations

- MetaboAnnotatoR requires centroid-mode data; profile-mode spectra will produce spurious annotations or errors.
- Annotation confidence depends heavily on the completeness and accuracy of the fragment ion library; lipids absent from or poorly represented in LipidPos or other chosen libraries will be missed or misannotated.
- The method cannot distinguish between structural isomers (e.g., different sn-positions of acyl chains) based on fragmentation alone unless position-specific fragments are present; rank-1 lipid assignments refer to composition (e.g., LPC(14:0)) not stereochemistry.
- Retention time alone is not used for discrimination in the ranking algorithm; co-eluting isobars with similar or identical m/z may receive ambiguous annotations.
- Installation can fail due to dependency conflicts (e.g., mzR version mismatch with Rcpp); see README guidance for environment variable adjustments.

## Evidence

- [intro] Core workflow and output structure: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [readme] Data requirements and centroid mode specification: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [intro] Library specification for lipid annotation: "annotation can be performed using the default Lipid Positive mode libraries "*LipidPos*""
- [intro] Upstream processing workflow: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [intro] Spectrum visualization for validation: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [intro] Design purpose and scope: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
