---
name: fatty-acyl-chain-variant-identification
description: Use when when a metabolite feature has been assigned a top-rank lipid annotation (e.g., LPC(14:0)) but you need to assess whether related lipid species containing the same fatty acyl chain(s) (e.g., PC fragments with 14:0 acyl chains) also match the observed spectrum with lower scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
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

# fatty-acyl-chain-variant-identification

## Summary

Identify and rank alternative lipid annotations for a mass feature by extracting ranked candidate lists from MetaboAnnotatoR results and comparing scores of lipid species that share the same fatty acyl chain composition. This skill enables discovery of structural variants (e.g., PC fragments vs. intact LPC) that may annotate the same m/z feature with differing confidence.

## When to use

When a metabolite feature has been assigned a top-rank lipid annotation (e.g., LPC(14:0)) but you need to assess whether related lipid species containing the same fatty acyl chain(s) (e.g., PC fragments with 14:0 acyl chains) also match the observed spectrum with lower scores. This is most relevant when inspecting features with ambiguous lipid annotations or when exploring structural isobars in untargeted LC–MS AIF datasets.

## When NOT to use

- The feature has only a single candidate annotation with no alternative matches — fatty acyl chain variant identification is unnecessary if no variants exist in the candidate list.
- The input is raw LC–MS AIF chromatogram data in centroid mode; preprocessing (peak-picking with xcms/RamClustR and annotation with annotateRC) must be completed first.
- The analysis goal is to filter or discard low-confidence annotations; this skill is for comparative inspection and hypothesis generation, not filtering.

## Inputs

- annotateRC results object (S4 object from MetaboAnnotatoR containing ranked annotations)
- feature index (numeric, e.g., 3 for feature 3)
- target m/z and retention time (for reference and validation)

## Outputs

- ranked candidate annotation table (data frame with columns: rank, candidate_lipid_name, m/z, annotation_score, match_confidence)
- structured output file (e.g., CSV or TSV) preserving rank order and scores

## How to apply

Load the annotateRC results object and extract the ranked candidate list for the target feature using annotations$rankedResult[[feature_index]]. Display all candidates in rank order, preserving annotation scores and confidence metrics. Verify that the top-ranked candidate (e.g., LPC(14:0)) occupies rank 1. Scan the candidate list for related lipid species that contain the same fatty acyl chain identifier (e.g., PC variants with the 14:0 chain) and note their rank positions and scores relative to rank 1. The rationale is that pseudo-MS/MS spectra from AIF data may fragment intact lipids into characteristic ions that overlap with those of related species, creating competing annotations that can be disambiguated by comparing match scores and biological plausibility (e.g., LPC is more abundant than intact PC in certain tissue types).

## Related tools

- **MetaboAnnotatoR** (Performs metabolite annotation of LC–MS AIF features using ion fragment databases and outputs ranked candidate lists via the annotateRC function) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version ≥4.5.0) for loading and manipulating annotateRC result objects and generating ranked candidate tables)
- **xcms** (Upstream peak-picking and feature detection tool that produces feature tables required for annotateRC input)
- **RamClustR** (Upstream pseudo-MS/MS spectrum generation tool that produces the spectral data annotated by MetaboAnnotatoR)

## Examples

```
# Load annotateRC results and extract ranked candidates for feature 3
ranked_candidates_feature3 <- annotations$rankedResult[[3]]
print(ranked_candidates_feature3)  # Display rank, candidate name, score, confidence
# Inspect PC(14:0+X) variants and compare their scores to LPC(14:0) rank 1
```

## Evaluation signals

- The ranked candidate list is successfully extracted and displays all candidates in descending rank order with no missing or reordered rows.
- The top-ranked candidate is confirmed to be the expected annotation (e.g., LPC(14:0) at rank 1).
- Related lipid species containing the target fatty acyl chain are present and their rank positions and scores are correctly recorded (e.g., PC(14:0+X) variants ranked 2–5 with lower scores than rank 1).
- Annotation scores decrease monotonically from rank 1 to lower ranks, indicating proper ranking consistency.
- The output table can be successfully saved to a structured file (CSV, TSV, or R object) with no data loss or corruption.

## Limitations

- MetaboAnnotatoR's fragment library may be incomplete or biased toward certain lipid classes (e.g., phospholipids); rare or novel fatty acyl chain variants may not appear in the candidate list.
- No changelog or version history is available for MetaboAnnotatoR, limiting reproducibility and traceability of changes to annotation algorithms or scoring metrics across versions.
- Pseudo-MS/MS spectra from AIF data can be ambiguous, especially at moderate mass resolution or low signal-to-noise ratios; multiple lipid species with overlapping fragment ions may receive similar scores, making variant ranking inconclusive.
- Peak-picking threshold parameters (default noise=0.005, mpeaksThres=0.1) can affect the pseudo-MS/MS spectrum composition and thus candidate ranking; sensitivity to these parameters is not fully characterized in the paper.

## Evidence

- [intro] Extracting and displaying ranked candidates with scores: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [other] Verifying top-ranked candidate identity: "Feature 3 (468.3095 m/z) has LPC(14:0) as the rank 1 annotation, but can also be annotated to fragments of several PCs containing the 14:0 fatty acyl chain, although with lower scores and confidence."
- [other] Loading and extracting results from annotateRC object: "Load the annotateRC results object containing annotations$rankedResult[[3]]. Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order."
- [intro] Saving structured output: "It is possible to save the annotation results to a user-specified directory"
