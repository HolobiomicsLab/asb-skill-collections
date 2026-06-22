---
name: ranked-result-extraction-and-display
description: Use when after running annotateRC on LC–MS AIF data when you need to inspect whether a feature has multiple plausible annotations (e.g., isobaric lipids, isomers with the same fatty-acyl chain) or when the rank-1 annotation confidence is borderline and alternatives should be evaluated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
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
---

# ranked-result-extraction-and-display

## Summary

Extract and display ranked candidate metabolite annotations for a specific LC–MS feature from the annotateRC results object, preserving annotation scores and rank order. This skill enables inspection of alternative candidate annotations beyond the top-ranked hit, critical for understanding annotation ambiguity and lipid isomer/isobar confusion in untargeted AIF metabolomics.

## When to use

Apply this skill after running annotateRC on LC–MS AIF data when you need to inspect whether a feature has multiple plausible annotations (e.g., isobaric lipids, isomers with the same fatty-acyl chain) or when the rank-1 annotation confidence is borderline and alternatives should be evaluated. Use it specifically when a feature m/z value could map to multiple lipid species or fragments with different annotation scores.

## When NOT to use

- Feature has not yet been processed by annotateRC; run annotation first.
- You only need the single top-ranked annotation and are not investigating annotation ambiguity or isomer/isobar confusion.
- Input is already a manually curated or consensus annotation table rather than raw annotateRC output.

## Inputs

- annotateRC results object (R list)
- rankedResult sublist for a single feature (e.g., annotations$rankedResult[[feature_index]])
- target feature identifier (m/z and retention time or index)

## Outputs

- ranked candidate annotation table (data frame or matrix with columns: rank, metabolite name, m/z, annotation score, confidence)
- structured output file (CSV, TSV, or RDS format)

## How to apply

Load the annotateRC results object and access the rankedResult sublist for your target feature (e.g., annotations$rankedResult[[3]] for feature 3). Extract the ranked candidate table, which contains all alternative annotations ordered by decreasing annotation score, preserving rank position and score magnitude. Verify that the top-ranked candidate is the expected annotation (e.g., LPC(14:0) for m/z 468.3095). Then inspect lower-ranked candidates to identify structural variants that share key fragmentation patterns—for example, PC species containing the same fatty-acyl chain (e.g., 14:0) at lower confidence. Format the output as a structured table showing rank, metabolite name, m/z, annotation score, and confidence metric. This reveals which alternative structures are biochemically plausible and how much score separation exists between them—a small gap suggests true ambiguity, while a large gap indicates the rank-1 annotation is robust.

## Related tools

- **MetaboAnnotatoR** (R package that performs metabolite annotation of LC–MS AIF features and generates the annotateRC results object containing rankedResult sublists) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Programming environment for loading, subsetting, and formatting annotateRC results objects; version 4.5.0 or higher required)
- **xcms** (Upstream feature detection and peak-picking tool; processes LC–MS chromatograms before annotation)
- **RamClustR** (Upstream pseudo-MS/MS spectrum generation from AIF data; outputs object used alongside annotateRC results)

## Examples

```
# Load annotateRC results and extract ranked candidates for feature 3
ranked_feature3 <- annotations$rankedResult[[3]]
write.csv(ranked_feature3, file='feature3_ranked_candidates.csv', row.names=FALSE)
```

## Evaluation signals

- Rank-1 candidate appears at position 1 in the extracted table with the highest annotation score.
- All alternative candidates are present with lower scores; rank order is strictly decreasing.
- Structural variants (e.g., PC species with the same fatty-acyl chain as the top hit) appear in the candidate list at expected lower ranks.
- Score gap between rank 1 and rank 2 is large (>10% relative difference) if rank-1 annotation is reliable, or small (<5%) if annotation is ambiguous.
- Output table schema matches expected columns (rank, metabolite name, m/z, score, confidence) with no missing or malformed entries.

## Limitations

- Ranked candidates are constrained by the fragment library used during annotateRC; annotations not in the library will not appear regardless of true biological presence.
- Score comparison is only valid within a single feature; cannot directly compare annotation scores across different features due to feature-specific spectral properties.
- Does not automatically distinguish between true isomers vs. isobars; visual inspection of matched fragment ions or external standards is required for disambiguation.
- No changelog available for MetaboAnnotatoR; version history and any changes to ranking algorithm are undocumented.

## Evidence

- [other] Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order.: "Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order."
- [intro] It is also possible to inspect if there were other candidate annotations for a given feature: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [other] Feature 3 (468.3095 m/z) has LPC(14:0) as the rank 1 annotation, but can also be annotated to fragments of several PCs containing the 14:0 fatty acyl chain, although with lower scores and confidence.: "Feature 3 (468.3095 m/z) has LPC(14:0) as the rank 1 annotation, but can also be annotated to fragments of several PCs containing the 14:0 fatty acyl chain, although with lower scores and confidence."
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [intro] annotations can be performed using the *annotateRC* function: "annotations can be performed using the *annotateRC* function"
