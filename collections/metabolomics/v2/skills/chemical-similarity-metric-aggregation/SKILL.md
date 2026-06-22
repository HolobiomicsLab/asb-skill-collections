---
name: chemical-similarity-metric-aggregation
description: Use when when you have an unknown metabolite compound with mass spectral data, have retrieved candidate structures from a molecular structure database (PubChem, HMDB), and have obtained predictions of structurally related metabolites from a deep-learning semantic similarity model (e.g., DeepMASS2).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
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

# chemical-similarity-metric-aggregation

## Summary

Aggregate chemical-space similarity scores between database candidate structures and deep-learning predicted structurally related metabolites to rerank molecular structure database hits. This skill leverages molecular fingerprints and similarity metrics to identify chemical-space proximity and relocate unknown metabolites within the structural candidate space.

## When to use

When you have an unknown metabolite compound with mass spectral data, have retrieved candidate structures from a molecular structure database (PubChem, HMDB), and have obtained predictions of structurally related metabolites from a deep-learning semantic similarity model (e.g., DeepMASS2). Use this skill to reorder the candidates by their proximity to the predicted related metabolites in chemical space, which improves the ranking quality by incorporating structural similarity information beyond simple m/z matching.

## When NOT to use

- Input contains no predicted structurally related metabolites or the deep-learning model has not been run.
- Candidate structure set is empty or database retrieval has not been performed.
- The chemical space is sparse or the predicted metabolites are not chemically representative of the unknown compound's likely structural class.

## Inputs

- Predicted structurally related metabolites (from deep-learning semantic similarity model)
- Candidate structures retrieved from molecular structure databases (SMILES, molecular identifiers, or structure objects)
- Precursor m/z value
- Optional: molecular formula constraint

## Outputs

- Ranked list of candidate structures with aggregated chemical-space proximity scores
- Scored and reordered candidate structures (e.g., CSV format with candidate identifier, structure, and aggregated similarity score)

## How to apply

Load the semantic-similarity predictions (structurally related metabolites) output from the deep-learning model. Retrieve candidate structures from molecular structure databases (e.g., PubChem, HMDB) for the unknown compound, filtered by precursor m/z and optional molecular formula constraints. Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each candidate structure and each predicted structurally related metabolite. Aggregate similarity scores across all predicted metabolites for each candidate—typically by summing or averaging—to produce a single aggregated chemical-space proximity score per candidate. Rank candidates in descending order by aggregated score and output the reranked list with scores. The rationale is that candidates structurally similar to the predicted related metabolites occupy nearby regions of chemical space to the unknown compound, providing valuable location information that improves candidate ranking.

## Related tools

- **DeepMASS2** (Generates semantic similarity predictions (structurally related metabolites) from mass spectral data via deep learning; output feeds into the chemical-similarity-metric-aggregation workflow) — https://github.com/hcji/DeepMASS2_GUI

## Evaluation signals

- Aggregated scores for each candidate are within a reasonable numerical range (e.g., 0–1 if normalized, or 0–max_fingerprint_bits if summed).
- Candidates with higher aggregated similarity scores are structurally more similar to the predicted related metabolites than low-scoring candidates (spot-check SMILES/fingerprints).
- The reranked candidate list is ordered strictly in descending aggregated score; ties are handled consistently.
- The number of reranked candidates equals the number of input candidates (no duplicates or losses).
- Candidates that were distant in the original database ranking move closer to the top if they are chemically similar to the predicted metabolites, reflecting improved ranking quality.

## Limitations

- The quality of chemical-space ranking depends entirely on the quality and coverage of predicted structurally related metabolites from the deep-learning model; poor predictions will degrade reranking.
- Molecular fingerprint choice (e.g., Tanimoto, Morgan, MACCS) and aggregation strategy (sum vs. mean vs. max) can significantly affect reranking; the article does not specify exact fingerprint type or aggregation method.
- Molecular formula constraints, if provided, help improve ranking accuracy, but optional and not always available.
- The skill assumes candidate structures are valid and retrievable from the molecular database; malformed or absent structures may cause fingerprint computation to fail.

## Evidence

- [other] DeepMASS2 ranks database candidates by leveraging structurally related metabolites predicted via deep learning; these predictions provide chemical-space proximity information that identifies the potential location of unknown metabolites within the structural candidate space, thereby reordering candidates from molecular structure databases.: "DeepMASS2 ranks database candidates by leveraging structurally related metabolites predicted via deep learning; these predictions provide chemical-space proximity information that identifies the"
- [other] Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each candidate and the predicted structurally related metabolites. Aggregate similarity scores across all predicted metabolites for each candidate structure. Rank candidates in descending order by aggregated chemical-space proximity score.: "Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each candidate and the predicted structurally related metabolites. Aggregate similarity scores"
- [readme] By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates obtained from molecular structure databases.: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [readme] Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites.: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites"
