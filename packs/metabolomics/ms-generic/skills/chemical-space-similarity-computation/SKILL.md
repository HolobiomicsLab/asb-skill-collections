---
name: chemical-space-similarity-computation
description: Use when you have retrieved multiple candidate structures from a molecular structure database (e.g., PubChem, HMDB) for an unknown compound, and you have predictions of structurally related metabolites from a deep-learning mass spectral model (e.g., DeepMASS2).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - DeepMASS2
  techniques:
  - mass-spectrometry
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

# chemical-space-similarity-computation

## Summary

Compute chemical-space similarity metrics between candidate molecular structures and predicted structurally related metabolites to reorder database candidates by proximity in chemical space. This skill enables ranking of molecular structure database hits by leveraging deep-learning predicted semantic neighbors, improving the likelihood of identifying the correct metabolite among candidates.

## When to use

You have retrieved multiple candidate structures from a molecular structure database (e.g., PubChem, HMDB) for an unknown compound, and you have predictions of structurally related metabolites from a deep-learning mass spectral model (e.g., DeepMASS2). Use this skill to systematically rank those candidates by their chemical-space proximity to the predicted neighbors, thereby identifying which candidates occupy the most plausible region of chemical space for the unknown.

## When NOT to use

- The deep-learning model has not been run or predictions are unavailable; chemical-space reranking requires predicted structurally related metabolites as input.
- Only a single candidate structure is retrieved from the database; ranking is meaningful only when there are multiple candidates to differentiate.
- Input molecular formula is not provided and chemical-space constraint cannot be applied; ranking accuracy may be degraded without formula-based filtering.

## Inputs

- semantic-similarity predictions from deep-learning model (list of structurally related metabolites with identifiers or structures)
- candidate structures from molecular structure database (SMILES strings, InChI, or structure objects with molecular identifiers)
- molecular structure database records (e.g., PubChem, HMDB entries with precursor m/z constraints)

## Outputs

- ranked candidate list ordered by aggregated chemical-space proximity score (descending)
- scores or metrics quantifying chemical-space similarity for each candidate
- mapping of candidates to their similarity-score contributions from individual predicted metabolites

## How to apply

Load the semantic-similarity predictions (structurally related metabolites) from the deep-learning model output and compute molecular fingerprints (e.g., ECFP, Tanimoto distance) for each predicted metabolite and each database candidate. For each candidate, aggregate the pairwise chemical-space similarity scores (e.g., mean or sum Tanimoto distance) across all predicted metabolites. Rank candidates in descending order by aggregated chemical-space proximity score. The rationale is that candidates sharing structural features with multiple predicted neighbors are more likely to represent the true identity, as the predicted neighbors collectively define a chemical-space neighborhood that constrains the location of the unknown.

## Related tools

- **DeepMASS2** (Provides deep-learning semantic-similarity predictions (structurally related metabolites) and enables GUI-based annotation workflow; performs mass spectral language analysis to predict neighbor metabolites in chemical space.) — https://github.com/hcji/DeepMASS2_GUI

## Evaluation signals

- Ranked candidate list contains all input candidates with no duplicates and ranks are in descending order by aggregated score.
- Aggregated scores for each candidate are reproducible; recomputing from the same predicted metabolites and candidate structures yields identical scores.
- Top-ranked candidates exhibit structural features (fingerprint overlap) consistent with the predicted metabolite ensemble; visual inspection of molecular structures confirms plausible chemical-space clustering.
- When a ground-truth metabolite is known, verify that it ranks higher than decoy candidates; if present, it should occupy a top position reflecting its proximity to predicted neighbors.
- Score distributions are reasonable: aggregated scores should show variance across candidates; uniform or bimodal distributions may indicate fingerprint or similarity-metric miscalibration.

## Limitations

- Ranking accuracy depends on quality and diversity of predicted structurally related metabolites; if the deep-learning model makes poor predictions, chemical-space reranking will not improve candidate selection.
- Molecular fingerprint choice (e.g., ECFP, MACCS) and similarity metric (e.g., Tanimoto distance) can significantly affect ranking; no single fingerprint is optimal for all chemical spaces.
- Adding molecular formula as an optional constraint significantly improves ranking accuracy; without it, the chemical-space neighborhood may be overly broad and rank candidates less effectively.
- The method assumes that structurally related metabolites form a coherent neighborhood in fingerprint space; for compounds at the boundary of chemical space or with sparse neighbor predictions, aggregation may not discriminate candidates well.

## Evidence

- [other] DeepMASS2 ranks database candidates by leveraging structurally related metabolites predicted via deep learning; these predictions provide chemical-space proximity information that identifies the potential location of unknown metabolites within the structural candidate space.: "DeepMASS2 ranks database candidates by leveraging structurally related metabolites predicted via deep learning; these predictions provide chemical-space proximity information that identifies the"
- [other] Compute chemical-space similarity metrics between candidates and predicted metabolites, aggregate scores, and rank candidates by aggregated proximity score.: "Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each candidate and the predicted structurally related metabolites. Aggregate similarity scores"
- [readme] Structurally related metabolites from chemical space provide valuable information and assist in ranking candidates from molecular structure databases.: "these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates obtained from molecular structure databases"
- [readme] Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites.: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites"
