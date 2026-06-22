---
name: metabolite-candidate-ranking-interpretation
description: Use when after running annotateRC() on LC-MS AIF features, when you need to validate whether a feature's rank-1 annotation is reliable or when you suspect that structurally similar metabolites (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_0625
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  - R (version or higher)
  - plotResultSpec
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  - build: coll_metaboannotator_cq
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

# metabolite-candidate-ranking-interpretation

## Summary

Inspect and interpret ranked candidate metabolite annotations for a given LC-MS feature, comparing scores and confidence levels to assess annotation quality and identify alternative structural assignments. This skill reveals whether the top-ranked annotation is robust or if lower-ranked candidates warrant consideration based on fragment matching patterns.

## When to use

After running annotateRC() on LC-MS AIF features, when you need to validate whether a feature's rank-1 annotation is reliable or when you suspect that structurally similar metabolites (e.g., lipid homologs containing the same fatty acyl chain) may also explain the observed fragmentation pattern with non-negligible scores.

## When NOT to use

- Feature has not yet been processed through the annotateRC workflow; use annotateRC first to generate rankedResult.
- You only want to extract the single top-ranked hit; use a simpler row-indexing method instead.
- Input is a raw LC-MS AIF chromatogram in centroid mode; preprocess with xcms and RamClustR to obtain peak-picked data and pseudo-MS/MS spectra first.

## Inputs

- annotateRC results object (containing rankedResult list)
- feature index or m/z and retention time identifier
- target feature m/z and retention time

## Outputs

- ranked candidate annotation table (preserving scores and rank order)
- structured output file (CSV or tabular format)

## How to apply

Load the annotateRC results object and extract the rankedResult list for the feature of interest using annotations$rankedResult[[feature_index]]. Display the full ranked candidate table preserving annotation scores, rank order, and any confidence metrics. Verify that the rank-1 annotation appears at the top and note the score magnitude (absolute value and relative to lower-ranked candidates). Systematically scan lower-ranked candidates for structural variants (e.g., PC species with shared fatty acyl chains to an LPC hit) and compare their scores; a substantial score gap (e.g., rank 1 >> rank 2) indicates a strong annotation, while close scores suggest ambiguity. Format the ranked table as a structured output (e.g., CSV or data frame) for downstream reporting.

## Related tools

- **MetaboAnnotatoR** (Performs ion fragment-based metabolite annotation of LC-MS AIF features and generates ranked candidate lists via annotateRC() function) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Programming environment for loading, extracting, and formatting ranked annotation results from MetaboAnnotatoR objects)
- **xcms** (Upstream peak-picking and feature detection on raw LC-MS AIF chromatograms (required before annotateRC))
- **RamClustR** (Upstream pseudo-MS/MS spectrum clustering and extraction from AIF chromatograms (required before annotateRC))

## Examples

```
# Load annotateRC results and inspect ranked candidates for feature 3
library(MetaboAnnotatoR)
ranked_feature_3 <- annotations$rankedResult[[3]]
print(ranked_feature_3)
write.csv(ranked_feature_3, file='feature_3_ranked_candidates.csv', row.names=FALSE)
```

## Evaluation signals

- Rank-1 annotation is present and appears at the top of the ranked candidate table with the highest score.
- Score values are correctly extracted and displayed for all ranked candidates in descending order; no missing or NaN values.
- Lower-ranked structural variants (e.g., PC(14:0/18:2) when rank 1 is LPC(14:0)) are present and identifiable by their shared fatty acyl chain nomenclature.
- Score gap between rank 1 and rank 2 is quantified and documented; large gaps (e.g., >0.5 or >50% difference) indicate confident annotation, small gaps suggest ambiguity.
- Output table is saved in a portable format (CSV) with column headers and can be parsed by downstream tools or human reviewers.

## Limitations

- The ranked candidate list depends entirely on the quality and completeness of the fragment library supplied to annotateRC; missing database entries will not appear as candidates.
- Fragment matching relies on the signal-to-noise thresholds (noise=0.005 and mpeaksThres=0.1 by default); low-intensity pseudo-MS/MS spectra may yield shallow candidate lists with poor discrimination.
- Score ranking does not account for biological plausibility or pathway context; a high-scoring structural variant may be chemically similar but biologically irrelevant.
- No changelog or version history is documented in the repository, making it difficult to assess whether score algorithms or ranking criteria have changed between versions.

## Evidence

- [other] Extract and display ranked candidate list preservation: "Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order."
- [other] Rank-1 annotation verification: "Verify that LPC(14:0) appears as the top-ranked candidate."
- [other] Lower-ranked structural variants identification: "Confirm the presence and rank positions of PC species variants containing the 14:0 fatty-acyl chain at lower scores."
- [intro] Ranked candidate inspection workflow: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [intro] annotateRC function purpose: "annotations can be performed using the *annotateRC* function"
- [intro] Fragment database dependency: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [intro] Peak-picking noise threshold: "Peak-picking above noise level threshold (default: 0.005)"
