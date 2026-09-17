---
name: annotation-candidate-comparative-scoring
description: Use when you have pseudo-MS/MS spectra from LC-MS all-ion fragmentation
  (AIF) data that have been matched against one or more ion fragment databases (e.g.,
  LipidPos, MassBank), generating multiple candidate annotations per feature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0157
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
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

# annotation-candidate-comparative-scoring

## Summary

Rank and compare metabolite annotation candidates for LC-MS features by matching fragment ion patterns against libraries and scoring candidate matches to identify the most plausible metabolite identity. This skill is essential when a single LC-MS feature generates multiple candidate annotations and you need to determine which is most likely correct based on fragment ion agreement.

## When to use

Apply this skill when you have pseudo-MS/MS spectra from LC-MS all-ion fragmentation (AIF) data that have been matched against one or more ion fragment databases (e.g., LipidPos, MassBank), generating multiple candidate annotations per feature. Use it to prioritize candidates when a feature yields 2+ hits with different metabolite identities, or when you need to validate whether the top-ranked candidate is sufficiently confident for reporting.

## When NOT to use

- Input feature data are already in targeted mode (single known precursor, limited fragmentation) — use targeted identification methods instead.
- Feature table is empty or contains <1 feature — annotation requires at least one feature to match.
- No appropriate fragment library exists for the metabolite class of interest — comparative scoring requires a reference database with curated fragment patterns.

## Inputs

- xcmsSet object (peak-picked LC-MS feature data with retention time and m/z coordinates)
- RAMClustR object (pseudo-MS/MS spectra derived from all-ion fragmentation data)
- Feature table (targetTable.csv format: list of m/z and retention time pairs to annotate)
- Ion fragment library or database (e.g., LipidPos, MassBank, or custom .msp format)

## Outputs

- Ranked candidate annotation table (one or more metabolite identities per feature, ordered by matching score)
- Annotation score metrics (matching score for each candidate)
- Visualization of matched fragment ions overlaid on pseudo-MS/MS spectra for top candidates

## How to apply

Execute the annotateRC function on xcms and RAMClustR objects with your chosen fragment library (e.g., LipidPos for lipids) to generate candidate annotations ranked by matching score. The function compares observed fragment ions in each feature's pseudo-MS/MS spectrum against the fragment patterns in the library, assigning a score that reflects the quality of the ion match. Inspect the ranked candidate list for each feature; the rank-1 candidate is the highest-scoring match. Cross-check multiple candidates for the same feature to assess confidence: if the rank-1 match has a substantially higher score than rank-2, the annotation is more reliable. Verify that observed features contain at least a threshold number of matched ions (the paper demonstrated annotation success with three of six features returning lipid matches). Save and visualize the spectra with matched ions overlaid to confirm visual plausibility of the top candidate.

## Related tools

- **MetaboAnnotatoR** (Provides the annotateRC function for comparative matching of feature spectra against fragment libraries and ranking candidates by score) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Performs peak-picking and feature detection to generate the peak-picked data object required as input to annotateRC)
- **RamClustR** (Generates pseudo-MS/MS spectra from all-ion fragmentation data; output RAMClustR object is the core spectral input to annotateRC)
- **R** (Runtime environment for executing annotateRC and inspecting ranked candidate annotations)

## Examples

```
annotateRC(RC = RC_object, xset = xcms_object, targetTable = targetTable_csv, libraries = 'LipidPos')
```

## Evaluation signals

- Each feature in the input table receives at least one candidate annotation (or None if no match exceeds noise threshold).
- Candidate annotations are ranked with decreasing matching score; rank-1 candidate has the highest score for its feature.
- Three or more observed fragment ions match the top-ranked candidate's library spectrum (indicating sufficient evidence for the match).
- Visualized pseudo-MS/MS spectrum shows clear overlap between observed peaks and library peaks for the rank-1 candidate (no major unmatched peaks dominate the spectrum).
- Comparison of rank-1 vs. rank-2 matching scores shows substantial separation (implying high confidence in top choice) or modest separation (implying ambiguity warranting further investigation).

## Limitations

- Annotation success depends on the completeness and quality of the fragment library: if the true metabolite is absent from or poorly represented in the library, no correct match will be returned.
- Fragment libraries must be in a compatible format (the paper demonstrates use with LipidPos and MassBank); custom or legacy formats may require reformatting.
- Matching score calculation assumes consistent fragmentation patterns; high structural similarity between metabolites (e.g., isomers, homologs with few differing ions) may lead to ambiguous or incorrect ranking.
- No changelog or version history is publicly documented, limiting reproducibility across MetaboAnnotatoR releases.
- The skill requires centroid-mode LC-MS data; profile-mode or non-AIF data cannot be used.

## Evidence

- [intro] annotateRC function successfully annotate three out of six features from the targetTable.csv using xcmsSet and RAMClustR objects with LipidPos libraries: "Three out of the six features were annotated with to a lipid"
- [intro] Ranked candidate annotations for features are retrieved and compared by matching score: "Retrieve and rank candidate annotations by matching score for each feature"
- [intro] Fragment library configuration and annotation execution using annotateRC: "annotations can be performed using the *annotateRC* function"
- [intro] Inspection and visualization of matched fragment ions for candidate evaluation: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [readme] Raw LC-MS data format requirement: centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [readme] MetaboAnnotatoR design purpose and scope: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
