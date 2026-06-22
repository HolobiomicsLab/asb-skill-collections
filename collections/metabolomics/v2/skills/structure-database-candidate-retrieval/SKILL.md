---
name: structure-database-candidate-retrieval
description: Use when you have a mass spectrum of an unknown metabolite with a known or inferred precursor m/z, you have run a deep-learning semantic similarity model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3559
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - DeepMASS2
derived_from:
- doi: 10.1101/2024.05.30.596727v2
  title: DeepMASS
evidence_spans:
- DeepMASS2 is a cross-platform GUI software tool, which enables deep-learning based metabolite annotation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmass_cq
    doi: 10.1101/2024.05.30.596727v2
    title: DeepMASS
  dedup_kept_from: coll_deepmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.05.30.596727v2
  all_source_dois:
  - 10.1101/2024.05.30.596727v2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structure-database-candidate-retrieval

## Summary

Retrieve and rank candidate structures from molecular databases (PubChem, HMDB) for an unknown compound by leveraging deep-learning predictions of structurally related metabolites and computing chemical-space similarity metrics. This skill improves annotation accuracy by reordering database candidates based on their proximity to predicted structural neighbors in chemical space.

## When to use

You have a mass spectrum of an unknown metabolite with a known or inferred precursor m/z, you have run a deep-learning semantic similarity model (e.g., DeepMASS2) that predicts structurally related metabolites, and you need to disambiguate among multiple candidate structures returned from a public molecular structure database to identify the most likely match.

## When NOT to use

- Deep-learning semantic similarity predictions are unavailable or unreliable for your ion mode or spectral library.
- Your unknown compound is a known metabolite already present in the reference library; direct spectral matching would be more efficient.
- The molecular structure database query returns no candidates (e.g., m/z is outside the mass range of the database); ranking cannot proceed without candidates.

## Inputs

- precursor m/z value
- ion mode (positive or negative)
- optional molecular formula
- deep-learning semantic similarity predictions (list of structurally related metabolites with structures or SMILES)
- candidate structures retrieved from molecular structure database

## Outputs

- ranked list of candidate structures
- aggregated chemical-space proximity scores per candidate
- mapping of each candidate to contributing structurally related metabolites

## How to apply

First, load the semantic-similarity predictions (list of structurally related metabolites) from the deep-learning model output. Second, query a molecular structure database (e.g., PubChem, HMDB) using the precursor m/z and optional molecular formula constraint to retrieve initial candidate structures. Third, compute chemical-space similarity metrics (e.g., Tanimoto distance or molecular fingerprints) between each candidate and each predicted structurally related metabolite. Fourth, aggregate similarity scores across all predicted metabolites for each candidate (e.g., mean or max aggregation). Finally, rank candidates in descending order by aggregated chemical-space proximity score and output the ranked list with scores; candidates with higher aggregated proximity to predicted metabolites are positioned higher, reflecting their greater likelihood of being the correct structure.

## Related tools

- **DeepMASS2** (Predicts structurally related metabolites via deep-learning semantic similarity analysis of mass spectral language; provides the predicted metabolite list that drives candidate ranking) — https://github.com/hcji/DeepMASS2_GUI

## Evaluation signals

- Candidates are ranked in descending order by aggregated chemical-space proximity score; the top-ranked candidate should have the highest mean or max Tanimoto similarity to predicted structurally related metabolites.
- Aggregated scores are reproducible: re-running the ranking on the same inputs (same candidate set, same predicted metabolites, same fingerprint method) yields identical scores and rank order.
- The true structure (if known) appears in the top ranked results; precision or recall of the true metabolite within the top-N candidates is measurable against a validation set.
- Candidates with chemical structures highly similar to predicted metabolites (high Tanimoto similarity) are ranked above structurally dissimilar candidates.
- Scores are computed for all candidates without missing values; no candidate from the database query is excluded from ranking.

## Limitations

- Deep-learning predictions of structurally related metabolites may be poor or unreliable if the unknown compound is highly novel or outside the training chemical space of the model.
- Chemical-space similarity metrics (e.g., Tanimoto fingerprints) capture only 2D structural similarity and do not account for 3D geometry, stereochemistry nuance, or functional group context beyond what fingerprints encode.
- Ranking accuracy depends on the quality and completeness of the queried molecular structure database; missing or incorrectly annotated structures in the database will not be recovered by this skill.
- Aggregation of similarity scores across predicted metabolites can be dominated by one or two highly similar predicted metabolites, potentially masking weaker but still informative signals from other predicted neighbors.

## Evidence

- [other] Deep learning semantic similarity predictions provide chemical-space proximity information: "these predictions provide chemical-space proximity information that identifies the potential location of unknown metabolites within the structural candidate space, thereby reordering candidates from"
- [other] Compute chemical-space similarity metrics between candidates and predicted metabolites: "Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each candidate and the predicted structurally related metabolites"
- [other] Aggregate and rank candidates by chemical-space proximity: "Aggregate similarity scores across all predicted metabolites for each candidate structure. Rank candidates in descending order by aggregated chemical-space proximity score"
- [readme] DeepMASS2 enables prediction and ranking via chemical space analysis: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [readme] Molecular formula is optional but recommended for constraining chemical space: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites"
