---
name: semantic-metabolite-ranking
description: Use when you have an unknown metabolite with unknown mass spectrum and need to prioritize structural candidates from databases (PubChem, HMDB) by their likelihood of being the true compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# semantic-metabolite-ranking

## Summary

Rank candidate structures retrieved from molecular databases by leveraging deep-learning predictions of structurally related metabolites to reorder candidates based on chemical-space proximity. This skill uses semantic similarity analysis of mass spectral language to identify the potential location of unknown metabolites within structural candidate space.

## When to use

Apply this skill when you have an unknown metabolite with unknown mass spectrum and need to prioritize structural candidates from databases (PubChem, HMDB) by their likelihood of being the true compound. Use it specifically when a deep-learning model has already predicted a set of structurally related metabolites for the unknown compound via semantic similarity of mass spectral language, and you need to reorder database hits to surface the most plausible candidates first.

## When NOT to use

- Input spectrum lacks mandatory metadata tags (PRECURSOR_MZ or IONMODE); the ranking will fail to initialize database filtering.
- No structurally related metabolites have been predicted by the deep-learning model; semantic similarity predictions are required to compute chemical-space proximity.
- The unknown compound's chemical space is not well represented in existing molecular structure databases; ranking will only reorder a sparse or irrelevant candidate set.

## Inputs

- Mass spectrum of unknown compound (mgf format with mandatory PRECURSOR_MZ and IONMODE tags)
- Deep-learning model predictions: list of structurally related metabolites (from semantic similarity analysis)
- Candidate structures retrieved from molecular structure databases (e.g., PubChem, HMDB)

## Outputs

- Ranked list of candidate structures with aggregated chemical-space proximity scores
- CSV export with candidates ranked in descending order by score (e.g., <COMPOUND_NAME>.csv)

## How to apply

Load semantic-similarity predictions (structurally related metabolites) from the deep-learning model output. Retrieve candidate structures from molecular structure databases matching the precursor m/z of the unknown compound. Compute chemical-space similarity metrics (e.g., Tanimoto distance, molecular fingerprints) between each database candidate and each predicted structurally related metabolite. Aggregate similarity scores across all predicted metabolites for each candidate structure using a scoring function (sum or mean). Rank candidates in descending order by aggregated chemical-space proximity score. The rationale is that candidates chemically similar to predicted metabolites occupy nearby regions in chemical space and are therefore more likely to be the unknown compound.

## Related tools

- **DeepMASS2** (Generates deep-learning-based semantic similarity predictions of structurally related metabolites and provides the candidate ranking interface. GUI software tool that executes the complete metabolite annotation workflow including ranking.) — https://github.com/hcji/DeepMASS2_GUI

## Evaluation signals

- Ranked candidate list is sorted in strictly descending order by aggregated chemical-space proximity score; no inversions or ties without secondary sorting criteria.
- For each candidate, verify that the aggregated score is the sum (or mean) of Tanimoto similarities (or other fingerprint metrics) to all predicted structurally related metabolites; spot-check 2–3 candidates by manual recalculation.
- The top-ranked candidate should exhibit higher chemical-space similarity to the set of predicted metabolites than lower-ranked candidates; visualize or compare fingerprint overlap.
- If molecular formula is provided as optional input (FORMULA tag), verify that candidates are chemically plausible (e.g., within mass tolerance of precursor m/z); filtering should have been applied upstream or candidate validity should be confirmed.
- Output CSV contains all input candidates with non-null scores and no missing rows; row count matches retrieved candidate set.

## Limitations

- Ranking quality depends entirely on the accuracy and diversity of deep-learning predictions; if semantic similarity predictions are biased or miss important structural classes, ranking will misdirect candidates.
- Chemical-space proximity (Tanimoto distance, fingerprints) may not correlate with spectral similarity or biological relevance; high ranking does not guarantee the candidate is the true compound.
- Performance improves when molecular formula is provided (optional FORMULA tag), but is degraded without it; chemical space is unconstrained and potentially larger.
- Ranking is agnostic to ion mode (positive/negative); misconfigured IONMODE tag will direct ranking toward chemically similar but ion-incompatible candidates.

## Evidence

- [intro] Deep-learning predictions enable ranking: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [other] Workflow steps for candidate ranking: "1. Load the semantic-similarity predictions (structurally related metabolites) from the deep-learning model output. 2. Retrieve candidate structures from molecular structure databases (e.g., PubChem,"
- [intro] Semantic similarity from mass spectral language: "enables deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language. This approach enables the prediction of structurally related metabolites for the unknown"
- [readme] Mandatory precursor m/z for database filtering: "Precursor m/z - Required. This tag specifies the precursor ion mass-to-charge ratio (m/z). This is a fundamental requirement for the search engine to filter candidates within the structural databases."
- [readme] Optional molecular formula improves ranking: "Molecular Formula - Optional. Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally"
