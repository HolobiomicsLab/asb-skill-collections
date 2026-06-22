---
name: component-candidate-prioritization-filtering
description: Use when after generateComponents has assigned candidate TP features to parent features and computed similarity metrics (spectrum similarity, fragment matches, neutral loss matches, retention time differences), use this skill to narrow the candidate pool to high-confidence parent–TP pairs that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0639
  tools:
  - patRoon
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  dedup_kept_from: coll_patroon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00477-w
  all_source_dois:
  - 10.1186/s13321-020-00477-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Component Candidate Prioritization Filtering

## Summary

Apply post-componentization filters to rank and retain parent–transformation product (TP) candidate pairs based on spectral similarity, retention time behavior, and shared fragmentation patterns. This prioritizes biologically or chemically plausible TP–parent links for downstream validation and reporting.

## When to use

After generateComponents has assigned candidate TP features to parent features and computed similarity metrics (spectrum similarity, fragment matches, neutral loss matches, retention time differences), use this skill to narrow the candidate pool to high-confidence parent–TP pairs that reflect expected mass spectrometry and chromatographic behavior. Apply this when you have multiple TP candidates per parent and want to prioritize based on chemical plausibility and data quality.

## When NOT to use

- Input componentsTPs object is empty or contains no parent–TP candidate pairs (filter will yield no output).
- Parent and TP features have not yet been linked by generateComponents; filtering requires a populated componentsTPs structure.
- Retention time or spectral metadata are missing or unreliable; retDirMatch and spectrum similarity filters will be ineffective.

## Inputs

- componentsTPs object (output from generateComponents with algorithm='tp')
- formulas object (optional, required for retDirMatch filtering)
- MSPeakLists or MS/MS spectral data (implicit, used in similarity calculations)

## Outputs

- filtered componentsTPs object with reduced candidate set ranked by similarity metrics

## How to apply

Filter the componentsTPs object using one or more of the following criteria: (1) Set minSpecSim or minSpecSimBoth to enforce a minimum spectrum similarity threshold (e.g., cosine similarity ≥ 0.5) between parent and TP MS/MS spectra; (2) Apply retDirMatch=TRUE to enforce expected retention time direction (e.g., TPs elute earlier or later than parents, depending on chemical transformation); (3) Set minFragMatches or minNLMatches to require a minimum number of shared fragment ions or neutral loss patterns between parent and TP spectra; (4) Optionally filter by minRTDiff (retention time tolerance in seconds) to exclude implausibly distant candidates. Combine filters iteratively—start with loose thresholds and tighten based on inspection of candidate rankings and prior chemical knowledge of the transformation pathway.

## Related tools

- **patRoon** (provides filter() method and minSpecSim, minFragMatches, minNLMatches, retDirMatch parameters for componentsTPs filtering) — https://github.com/rickhelmus/patRoon

## Examples

```
componTP <- filter(componTP, retDirMatch = TRUE, formulas = formulas); componTP <- filter(componTP, minSpecSim = 0.5, minFragMatches = 2)
```

## Evaluation signals

- Filtered componentsTPs object contains only candidate pairs meeting all specified thresholds (minSpecSim, minFragMatches, etc.).
- Candidate rankings within each parent group reflect decreasing similarity scores or match counts.
- Inspection of top-ranked candidates confirms chemical plausibility (e.g., expected mass shifts, retention time direction, fragment pattern inheritance from parent).
- Number of retained candidates per parent is substantially reduced compared to pre-filter componentsTPs, indicating effective prioritization.
- No parent is left without any TP candidates unless all candidates were below thresholds (expected outcome for false positives).

## Limitations

- Filters rely on high-quality MS/MS spectral data and accurate retention time measurements; poor spectral resolution or chromatographic drift may cause valid candidates to be filtered out.
- Spectrum similarity and fragment matching thresholds are data-dependent and may require empirical tuning for different ionization modes, instrument types, or compound classes.
- retDirMatch filter requires accurate formula predictions; if formulas are incorrect or unavailable, this criterion cannot be applied.
- No automatic threshold recommendation is provided; users must set minSpecSim, minFragMatches, and related parameters based on prior knowledge or iterative validation.

## Evidence

- [other] Post-componentization filters include retDirMatch, minSpecSim, minFragMatches, and minNLMatches to prioritize candidates.: "Apply post-componentization filters such as retDirMatch (expected retention direction), minSpecSim or minSpecSimBoth (spectrum similarity threshold), and minFragMatches or minNLMatches (shared"
- [other] Spectrum similarity and fragment matching are computed during componentization.: "Call generateComponents with algorithm='tp', passing fGroups, fGroupsTPs, TPs object, and optional annotation data (MSPeakLists, formulas, compounds) to calculate spectrum similarity and"
- [readme] README documents filter parameters for componentsTPs.: "Componentization & adduct annotation | Grouping of related features based on chemistry (e.g. isotopes, adducts and homologs), hierarchical clustering or MS/MS similarity into components."
