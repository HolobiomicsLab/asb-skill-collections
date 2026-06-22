---
name: metabolite-lipid-annotation-ranking
description: Use when you have LC–MS All-ion fragmentation chromatograms processed through xcms and RamClustR, a feature table with unknown identities, and you want to recover lipid annotations by matching observed spectra against lipid fragment libraries (e.g., LipidPos).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  - R (≥4.5.0)
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-lipid-annotation-ranking

## Summary

Rank candidate lipid annotations for LC–MS All-ion fragmentation features by matching experimental spectra against fragment ion databases using the annotateRC function. This skill identifies which features receive valid rank-1 lipid assignments and produces a globally ranked annotation summary.

## When to use

You have LC–MS All-ion fragmentation chromatograms processed through xcms and RamClustR, a feature table with unknown identities, and you want to recover lipid annotations by matching observed spectra against lipid fragment libraries (e.g., LipidPos). Use this skill when you need to determine which features in your cohort can be confidently assigned to known lipids and to quantify annotation coverage.

## When NOT to use

- Input chromatograms are in profile mode rather than centroid mode; annotateRC requires centroid-mode spectra.
- Feature table is already annotated with validated lipid identities; this skill is for de novo annotation discovery, not validation.
- Raw LC–MS data have not been processed through xcms and RamClustR; annotateRC depends on RamClustR RC objects as input.

## Inputs

- xcms xset object (processed LC–MS AIF chromatograms in centroid mode)
- RamClustR RC object (clustered features from AIF data)
- Feature table (.csv; e.g., targetTable.csv with columns for m/z, retention time, intensity)
- Lipid fragment ion library (e.g., LipidPos database)

## Outputs

- Ranked annotations object (annotations) with candidate lipid assignments per feature
- rankedResult object containing rank-1 and lower-ranked candidates with match scores
- Global annotation summary report (count and names of successfully annotated lipids)
- Annotated feature table with lipid identities and confidence metrics

## How to apply

Load the xcms xset object, RamClustR RC object, and target feature table (e.g., targetTable.csv containing six features). Execute the annotateRC function, specifying the LipidPos fragment libraries to match experimental spectra against the database. Extract ranked candidate annotations from the resulting annotations object, prioritizing rank-1 lipid matches. Inspect the rankedResult object to verify which features received valid lipid annotations and generate a global annotation summary report showing the count and identity of successfully annotated lipids. Judge success by whether the expected proportion of features (e.g., ≥3 of 6) receive rank-1 lipid assignments and whether matched ions are consistent with the proposed lipid structure when visualized.

## Related tools

- **MetaboAnnotatoR** (Primary annotation engine; provides annotateRC function to match feature spectra against fragment libraries and rank candidates.) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream feature detection and processing of LC–MS All-ion fragmentation chromatograms in centroid mode.)
- **RamClustR** (Upstream clustering and spectral aggregation; produces RC object required by annotateRC.)
- **R (≥4.5.0)** (Runtime environment for MetaboAnnotatoR, xcms, and RamClustR packages.)

## Examples

```
library(MetaboAnnotatoR); annotations <- annotateRC(xset, RC, targetTable, lib='LipidPos'); rankedLipids <- annotations$rankedResult; summary(rankedLipids)
```

## Evaluation signals

- Number of features receiving rank-1 lipid annotations matches or exceeds expected baseline (e.g., ≥3 of 6 in the targetTable.csv example).
- rankedResult object is non-empty and contains candidate lipid identities sorted by match score for each feature.
- Visualization of matched ions via plotResultSpec shows significant spectral overlap between observed and database spectra for annotated features.
- Global annotation summary report documents the count, names, and lipid classes of successfully assigned features with no duplicates.
- Feature annotations are reproducible when annotateRC is re-executed with the same inputs, xset, RC, and library versions.

## Limitations

- Only features with sufficient spectral complexity and database coverage will receive lipid annotations; sparse or unusual fragment patterns may not match any library entry.
- Annotation success depends critically on data quality: chromatograms must be centroid-mode and processed consistently through xcms and RamClustR.
- The LipidPos library covers lipids in positive ionization mode; negative-mode data require alternative libraries or re-processing.
- Installation may fail in some R environments due to dependency conflicts (e.g., mzR version mismatches); see README for remediation.
- Rank-1 annotations are not equivalent to identifications; even high-scoring matches should be validated by orthogonal MS/MS data or standards.

## Evidence

- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [intro] An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [intro] Then annotations can be performed using the *annotateRC* function: "Then annotations can be performed using the *annotateRC* function"
- [intro] This information can be accessed from the *rankedResult* object stored in the *annotations*: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [intro] Three out of the six features were annotated with to a lipid: "Three out of the six features were annotated with to a lipid"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode.: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [intro] It is possible to visualise the spectra containing the matched ions to each candidate: "It is possible to visualise the spectra containing the matched ions to each candidate"
