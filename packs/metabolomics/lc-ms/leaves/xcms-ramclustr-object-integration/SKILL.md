---
name: xcms-ramclustr-object-integration
description: Use when you have centroid-mode LC–MS all-ion fragmentation (AIF) data already processed through xcms for feature detection and retention-time correction, and a corresponding RamClustR object that groups co-eluting fragment ions into putative spectral clusters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3663
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
- An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages
- An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages is illustrated here.
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

# xcms-ramclustR-object-integration

## Summary

Integrate processed LC–MS all-ion fragmentation chromatograms from xcms (feature detection and retention-time alignment) with RamClustR spectral clustering objects to enable downstream metabolite annotation. This skill bridges feature-level and spectrum-level representations needed for compound identification via fragment library matching.

## When to use

You have centroid-mode LC–MS all-ion fragmentation (AIF) data already processed through xcms for feature detection and retention-time correction, and a corresponding RamClustR object that groups co-eluting fragment ions into putative spectral clusters. You need to annotate these clustered features against ion fragment databases (e.g., LipidPos) using tools like MetaboAnnotatoR's annotateRC function.

## When NOT to use

- LC–MS data is in profile (non-centroid) mode — xcms and RamClustR require centroid mode input
- You only have raw chromatographic data without prior feature detection — use xcms independently first
- Target features are already annotated — integration is for *de novo* identification, not refinement

## Inputs

- xcms xset object (processed LC–MS features with retention times)
- RamClustR RC object (spectral clusters and co-eluting ion assignments)
- target feature table (CSV format, e.g., targetTable.csv)
- ion fragment database library (e.g., LipidPos for positive mode)

## Outputs

- annotations object containing ranked candidate metabolite matches
- rankedResult data frame with rank-1 and alternative annotations per feature
- optional: visualization and summary reports of annotation results

## How to apply

Load the xcms xset object (containing processed features and retention times) and the RamClustR RC object (containing spectral clustering results and co-eluting ion assignments) into the same R environment. Prepare a target feature table (CSV format, e.g., targetTable.csv) listing the features to annotate, with columns matching the xset feature identifiers. Pass both objects together to the annotateRC function along with the target table and a fragment library (e.g., LipidPos for lipid-positive mode). The function will match experimental spectra against the database using the spectral information from the RC object and chromatographic alignment from the xset. Extract the ranked candidate annotations from the resulting annotations object, prioritizing rank-1 matches. Verify success by checking that annotations are returned and that matched ion pairs are consistent with the fragmentation patterns.

## Related tools

- **xcms** (Feature detection, alignment, and retention-time correction of LC–MS chromatograms)
- **RamClustR** (Spectral clustering and co-eluting ion grouping for all-ion fragmentation data)
- **MetaboAnnotatoR** (Main annotation tool; executes annotateRC function to match xset and RC objects against fragment databases) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher required))

## Examples

```
# Load objects and annotate
library(MetaboAnnotatoR)
load('xset.RData'); load('RC.RData')
targets <- read.csv('targetTable.csv')
annotations <- annotateRC(xset, RC, targets, db='LipidPos')
head(annotations$rankedResult)
```

## Evaluation signals

- Annotations object is successfully created and contains ranked candidate entries for input features
- At least one feature receives a rank-1 annotation (as in the reference study, 3 of 6 features were annotated)
- Matched ion pairs in each annotation correspond to fragment peaks present in both experimental and database spectra
- No missing values or NA entries in critical rankedResult columns (feature ID, candidate name, match score)
- Visualization via plotResultSpec shows visual agreement between experimental spectra and matched ion positions

## Limitations

- Requires raw LC–MS data in centroid mode; profile data must be converted beforehand
- Annotation success is library-dependent — features absent from the fragment database will not be annotated
- In the reference study, only 3 of 6 example features received successful lipid annotations, indicating inherent false-negative rates
- Performance depends on quality of xcms feature detection and RamClustR clustering; poor alignment or clustering reduces annotation reliability
- Installation may require manual fixes for mzR/Rcpp version mismatches or multiarch compilation issues (see README)

## Evidence

- [intro] xcms feature detection and RamClustR spectral clustering prerequisite: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [readme] centroid mode requirement: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [intro] annotateRC function usage with xset and RC objects: "Execute the annotateRC function with the xset, RC object, and LipidPos fragment libraries to match experimental spectra against the database."
- [intro] ranked annotation extraction: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [intro] annotation success rate in reference study: "Three out of the six features were annotated with to a lipid"
- [intro] downstream visualization and export: "It is possible to visualise the spectra containing the matched ions to each candidate"
