---
name: maximum-score-selection-over-pairs
description: Use when when you have individual pairwise scores (e.g., between BGCs and spectra) and need to rank composite links where one or both sides are collections (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - NPLinker
  - BiG-SCAPE
  - IOKR
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic data
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# maximum-score-selection-over-pairs

## Summary

Generalize pairwise scoring functions (e.g., BGC-spectrum IOKR scores) to group-level links (e.g., GCF-MF pairs) by computing the maximum score over all possible combinations of elements within each group. This approach enables ranking of composite genomic-metabolomic links when one or both sides contain multiple entities.

## When to use

When you have individual pairwise scores (e.g., between BGCs and spectra) and need to rank composite links where one or both sides are collections (e.g., Gene Cluster Families containing multiple BGCs matched against Molecular Families containing multiple spectra), and you want to use the strongest evidence of any single pair within each composite link.

## When NOT to use

- Input scores are already aggregated at the group level (e.g., already scored GCF-to-MF).
- You want to use mean, median, or other aggregation functions instead of maximum; this skill specifically applies the max operator.
- Individual pairwise scores are missing or sparse; the max operation will be biased if many combinations lack scores.

## Inputs

- Table of pairwise scores (BGC ID, spectrum ID, score value)
- List of Gene Cluster Family (GCF) identifiers with their constituent BGC IDs
- List of Molecular Family (MF) identifiers with their constituent spectrum IDs

## Outputs

- Table of composite link scores with columns: GCF_ID, MF_ID, max_score, num_pairs_evaluated
- Ranked list of GCF-MF links sorted by maximum score

## How to apply

For each composite link (e.g., a GCF-MF pair), retrieve all constituent elements from both sides (all BGCs in the GCF and all spectra in the MF). Filter to pairs where both elements exist in your input score table (e.g., IOKR predictions). Compute the maximum score across all valid (BGC, spectrum) combinations for that composite link using σ_IOKR(G, M) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}. Output a table with composite identifiers, the maximum score, and the count of pairs evaluated, which allows downstream filtering or ranking of composite links by their strongest internal signal.

## Related tools

- **IOKR** (Generates individual BGC-spectrum pairwise scores that serve as input to the maximum-score aggregation)
- **BiG-SCAPE** (Clusters BGCs into Gene Cluster Families (GCFs), which are the composite genomic entities aggregated by this skill)
- **NPLinker** (Software framework that implements the GCF-to-MF link scoring and ranking, including the maximum-score aggregation step) — https://github.com/sdrogers/nplinker

## Evaluation signals

- Output table has one row per GCF-MF pair with no duplicates; all GCF_ID and MF_ID values are valid and present in input lists.
- All max_score values lie within the range of individual pairwise scores (e.g., 0–1 for normalized IOKR); no negative or out-of-range values.
- num_pairs_evaluated matches the count of (BGC, spectrum) combinations that existed in the input score table for each GCF-MF pair.
- For any GCF-MF pair, the reported max_score equals the maximum of all scores for that pair's constituent combinations when manually verified.
- Composite links with higher max_score ranks correlate with downstream validation (e.g., known BGC-metabolite relationships) at statistically significant levels.

## Limitations

- Maximum-score aggregation ignores the distribution and quantity of high-scoring pairs; two links with the same max value are ranked equally even if one has many supporting pairs and the other only one.
- The method relies on complete or near-complete input score coverage; missing pairwise scores for any BGC-spectrum combination will underestimate the true maximum.
- Maximum selection amplifies noise if individual pairwise scores are unreliable or were computed using methods with low specificity (e.g., IOKR's dependence on MIBiG homology restricts it to BGCs showing considerable homology to curated references).
- Sparse or imbalanced GCF and MF sizes can lead to composite links with very few evaluated pairs, reducing statistical confidence in the aggregated rank.

## Evidence

- [other] For a GCF G and MF M, σ_IOKR(M, G) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}, where σ_IOKR scores individual BGC-spectrum links.: "For a GCF G and MF M, σ_IOKR(M, G) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}, where σ_IOKR scores individual BGC-spectrum links."
- [other] For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: σ_IOKR(G,M) = max σ_IOKR(m, g) for m ∈ M, g ∈ G.: "For each GCF-MF pair, compute the maximum IOKR score over all matching (BGC, spectrum) pairs: σ_IOKR(G,M) = max σ_IOKR(m, g) for m ∈ M, g ∈ G."
- [other] Output a table with columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated.: "Output a table with columns: GCF_ID, MF_ID, max_IOKR_score, num_pairs_evaluated."
- [other] How should IOKR BGC-spectrum link scores be generalised to score GCF-MF links when a GCF contains multiple BGCs and a MF contains multiple spectra?: "How should IOKR BGC-spectrum link scores be generalised to score GCF-MF links when a GCF contains multiple BGCs and a MF contains multiple spectra?"
- [other] Filter to (BGC, spectrum) pairs where both elements are present in the input IOKR score table.: "Filter to (BGC, spectrum) pairs where both elements are present in the input IOKR score table."
