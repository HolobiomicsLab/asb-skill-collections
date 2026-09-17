---
name: lipid-species-annotation-assessment
description: Use when after running MetaboAnnotatoR's annotateRC function when you
  need to (1) verify that the top-ranked annotation for a feature is correct, (2)
  understand what alternative lipid structures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - MetaboAnnotatoR
  - R
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS
  All-ion fragmentation (AIF) datasets
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Species Annotation Assessment

## Summary

Inspect, rank, and compare alternative candidate lipid annotations for a given LC-MS feature, evaluating score distributions and chain-level variants to understand annotation confidence and structural ambiguity. This skill is essential when a feature matches multiple lipid species or fragments and you need to systematically document which candidates rank highest and why lower-scoring alternatives remain plausible.

## When to use

Apply this skill after running MetaboAnnotatoR's annotateRC function when you need to (1) verify that the top-ranked annotation for a feature is correct, (2) understand what alternative lipid structures (e.g., fragments of related PC species or different LPC regioisomers) could explain the same m/z and retention time, or (3) assess the confidence gap between rank 1 and rank 2+ candidates to decide whether a single annotation is warranted or multiple hypotheses should be retained.

## When NOT to use

- Input feature has not yet been processed through MetaboAnnotatoR's annotateRC function; you must run annotation first.
- You only have a single pre-selected 'best' annotation and no ranked candidate list; this skill requires access to the full rankedResult object.
- Goal is to filter features by annotation quality across a whole dataset rather than deeply characterize one feature's ambiguity; use feature-level QC filtering instead.

## Inputs

- annotateRC results object (R list/S4 class)
- rankedResult artifact for a specific feature (numeric index or m/z)
- MetaboAnnotatoR lipid fragment database

## Outputs

- Ranked candidate annotation table (data frame or CSV) with columns: rank, compound_name, score, delta_from_rank1, m/z_match, rt_match
- Verbal summary of score gaps and structural relationships among top candidates
- Confidence assessment (pass/flag) indicating whether rank 1 is unambiguous or multiple hypotheses remain viable

## How to apply

Load the annotateRC results object and extract the ranked candidate list for the target feature using the rankedResult artifact. Display all ranked candidates with their annotation scores and rank positions, preserving sort order. Verify that the expected top-ranked lipid (e.g., LPC(14:0)) appears at rank 1 and examine the m/z and retention time match quality. Systematically traverse the ranked list to identify lower-scoring alternative annotations that share a common fatty acyl chain or structural motif (e.g., PC(14:0)-containing fragments). Compare score deltas between consecutive ranks to quantify confidence attenuation. Document the presence, rank position, and score of each candidate variant and format the results as a structured table (e.g., CSV or R data frame) with columns for rank, compound name, score, and delta from rank 1. This assessment reveals whether ambiguity is driven by true isobaric overlap, in-source fragmentation, or weak spectral matching.

## Related tools

- **MetaboAnnotatoR** (Performs metabolite annotation of LC-MS All-ion fragmentation features and produces the ranked candidate results inspected by this skill) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Programming environment for loading annotateRC objects, extracting rankedResult lists, and formatting output tables) — https://www.r-project.org/

## Examples

```
annotations <- annotateRC(RC_obj, databases = fragment_libs); candidates_feature3 <- annotations$rankedResult[[3]]; print(candidates_feature3[, c('rank', 'compound_name', 'score')])
```

## Evaluation signals

- Ranked candidate list is complete and sorted by descending score with no gaps or reordering.
- Top-ranked annotation (rank 1) matches the expected compound name and has the highest score.
- All candidates with the same fatty acyl chain motif (e.g., all 14:0-containing lipids) are identified and their ranks documented.
- Score deltas between consecutive ranks are positive and monotonically decrease, indicating consistent ranking logic.
- Output table is machine-readable (CSV or R data frame) with no missing values in required columns (rank, compound_name, score).

## Limitations

- MetaboAnnotatoR relies on fragment database completeness; rare lipids or non-standard adducts may not be in the database, yielding incomplete ranked lists.
- Score comparison is only meaningful within a single feature and single run; scores are not calibrated across different features or datasets.
- In-source fragmentation and neutral loss can generate multiple high-scoring candidates for a single m/z; score alone does not resolve true identity without orthogonal evidence (e.g., MS/MS validation).
- No changelog is available for MetaboAnnotatoR, so scoring algorithm changes across versions are not documented; reproducibility across package versions is not guaranteed.

## Evidence

- [other] Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order.: "Extract and display the ranked candidate list for feature 3, preserving annotation scores and rank order."
- [other] Feature 3 (468.3095 m/z) has LPC(14:0) as the rank 1 annotation, but can also be annotated to fragments of several PCs containing the 14:0 fatty acyl chain, although with lower scores and confidence.: "Feature 3 (468.3095 m/z) has LPC(14:0) as the rank 1 annotation, but can also be annotated to fragments of several PCs containing the 14:0 fatty acyl chain, although with lower scores and confidence."
- [intro] It is also possible to inspect if there were other candidate annotations for a given feature: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
