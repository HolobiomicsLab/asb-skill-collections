---
name: structure-selection-filtering
description: Use when when you have an unknown metabolite's predicted structural similarity
  scores (from a deep learning model such as DeepMASS) against all known metabolites
  in a reference database, and need to identify which known metabolites are most likely
  structurally related to the unknown to guide.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - DeepMASS
  techniques:
  - LC-MS
  license_tier: open
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

# structure-selection-filtering

## Summary

Rank and filter candidate metabolite structures from a set of known metabolites based on predicted structural similarity scores to an unknown metabolite. This skill enables selection of the most plausible candidates for unknown metabolite identification by sorting and thresholding deep-learning predictions.

## When to use

When you have an unknown metabolite's predicted structural similarity scores (from a deep learning model such as DeepMASS) against all known metabolites in a reference database, and need to identify which known metabolites are most likely structurally related to the unknown to guide targeted spectral matching or further validation.

## When NOT to use

- The unknown metabolite's MS/MS spectrum has not been processed or the deep-learning model has not yet generated similarity predictions.
- You require exact structural matches only; this skill prioritizes candidates by likelihood, not certainty.
- The reference database is empty or contains no comparable known metabolites.

## Inputs

- predicted structural similarity scores (vector/array mapping known metabolite identifiers to similarity scores)
- reference metabolite database with identifiers
- optional: similarity score threshold value

## Outputs

- ranked candidate list (table with metabolite identifiers, similarity scores, and rank positions)
- filtered subset of known metabolites above threshold (if threshold applied)

## How to apply

Load the predicted similarity scores output by the deep-learning model for the unknown metabolite against all known metabolites in the database. Sort all known metabolites by their similarity scores in descending order. Apply a similarity threshold (if applicable) to filter candidates that meet a minimum confidence level. Assign rank positions to the filtered candidates and output the ranked list with metabolite identifiers, their predicted similarity scores, and assigned ranks. The rationale is that higher-scoring candidates are more likely to share structural features with the unknown metabolite, making them prioritized targets for downstream structure elucidation or experimental validation.

## Related tools

- **DeepMASS** (generates predicted structural similarity scores between unknown and known metabolites; provides the ranked candidate selection as a downstream component) — https://github.com/hcji/DeepMASS

## Evaluation signals

- Ranked candidate list is sorted in descending order by similarity score with no inversions.
- All metabolites included in the output have similarity scores above the specified threshold (if one was set).
- Rank positions are sequential integers starting from 1 with no gaps.
- Metabolite identifiers in output are valid entries from the reference database.
- Top-ranked candidates show structurally plausible relationships to the unknown metabolite upon manual expert review.

## Limitations

- Ranking quality depends entirely on the accuracy of the deep-learning model's similarity predictions; poor predictions will produce poor rankings.
- No changelog or versioning information available for tracking method refinements over time.
- The original experimental spectra dataset (MetDNA) used for validation has been removed from the public repository, limiting reproducibility.
- Performance on novel structural scaffolds or metabolite classes not well-represented in the training database is not characterized.

## Evidence

- [readme] DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra and a rank method for picking out the possible candidate structures of the unknowns.: "a rank method for picking out the possible candidate structures of the unknowns"
- [intro] DeepMASS implements a rank method that picks out possible candidate structures of unknown metabolites, operating as a downstream component that processes structural similarity predictions.: "a rank method for picking out the possible candidate structures of the unknowns"
- [intro] 1. Load the unknown metabolite's predicted similarity scores to all known metabolites from the deep-learning model output. 2. Sort the known metabolites by their predicted structural similarity scores in descending order. 3. Select the top-ranked candidates (filtering by a similarity threshold if applicable) and assign rank positions. 4. Output the ranked candidate list with metabolite identifiers, similarity scores, and rank positions.: "Load the unknown metabolite's predicted similarity scores to all known metabolites from the deep-learning model output. 2. Sort the known metabolites by their predicted structural similarity scores"
- [readme] Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database.: "Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites"
