---
name: similarity-score-sorting
description: Use when after a deep-learning model has predicted structural similarity scores between an unknown metabolite's MS/MS spectrum and all known metabolites in a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3172
  tools:
  - DeepMASS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.8b05405
  title: Deep MS/MS similarity
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  dedup_kept_from: coll_deep_ms_ms_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.8b05405
  all_source_dois:
  - 10.1021/acs.analchem.8b05405
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# similarity-score-sorting

## Summary

Sort known metabolites by their predicted structural similarity scores to an unknown metabolite in descending order, then select top-ranked candidates above a similarity threshold. This is a critical downstream step in the DeepMASS workflow that converts continuous similarity predictions into an actionable ranked candidate list for metabolite identification.

## When to use

Apply this skill after a deep-learning model has predicted structural similarity scores between an unknown metabolite's MS/MS spectrum and all known metabolites in a reference database. Use it when you have a vector of similarity predictions (one score per known metabolite) and need to surface the most likely structural matches for expert curation or downstream validation.

## When NOT to use

- Unknown metabolite's MS/MS spectrum has not yet been processed by the deep-learning model; scores do not exist.
- Similarity scores are already provided in pre-ranked format (e.g., already sorted by curator).
- The reference database of known metabolites is empty or unavailable.

## Inputs

- Vector of predicted structural similarity scores (one float per known metabolite in reference database)
- Mapping of score indices to known metabolite identifiers
- Optional: similarity threshold parameter (e.g., 0.5–0.9, domain-dependent)

## Outputs

- Ranked candidate list with metabolite identifiers, similarity scores, and rank positions
- Optionally: filtered/thresholded subset meeting minimum similarity criterion

## How to apply

Load the predicted structural similarity scores for the unknown metabolite against all known metabolites from the deep-learning model output. Sort the known metabolites in descending order by their similarity scores (highest scores first). Apply a similarity threshold to filter candidates (if specified by domain knowledge or cross-validation); retain only metabolites exceeding this cutoff. Assign rank positions to the filtered candidates (1st, 2nd, 3rd, etc.). Output the ranked candidate list with metabolite identifiers, their similarity scores, and rank positions in a structured format (e.g., TSV or JSON) for downstream review or automated matching.

## Related tools

- **DeepMASS** (Deep-learning model that produces structural similarity score predictions; rank method is a downstream component of this workflow) — https://github.com/hcji/DeepMASS

## Evaluation signals

- Ranked list is sorted in strictly descending order by similarity score (no inversions).
- All candidates above the similarity threshold are included; all below are excluded (binary filtering).
- Rank positions are consecutive integers starting from 1, with no gaps.
- Metabolite identifiers match the reference database and are not duplicated.
- Score and identifier correspondence is preserved (no misalignment between score and metabolite ID).

## Limitations

- The quality of ranking depends entirely on the accuracy of the upstream deep-learning model's similarity predictions; poor model calibration will produce misleading rank orders.
- Threshold selection is not automated in the described workflow; domain expertise or cross-validation is needed to set an appropriate cutoff.
- The original DeepMASS package dataset (MetDNA) was removed from the repository; users must train models on in-house or public databases, limiting reproducibility.
- Ranking does not account for additional features (e.g., chemical prior, fragmentation plausibility) beyond learned similarity; tie-breaking or secondary ranking criteria are not described.

## Evidence

- [other] Load the unknown metabolite's predicted similarity scores to all known metabolites from the deep-learning model output.: "Load the unknown metabolite's predicted similarity scores to all known metabolites from the deep-learning model output."
- [other] Sort the known metabolites by their predicted structural similarity scores in descending order.: "Sort the known metabolites by their predicted structural similarity scores in descending order."
- [other] Select the top-ranked candidates (filtering by a similarity threshold if applicable) and assign rank positions.: "Select the top-ranked candidates (filtering by a similarity threshold if applicable) and assign rank positions."
- [readme] a rank method for picking out the possible candidate structures of the unknowns: "a rank method for picking out the possible candidate structures of the unknowns"
- [readme] DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra: "DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based"
