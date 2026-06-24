---
name: functional-level-similarity-index-computation
description: Use when when you have two metabolic networks (e.g., from KEGG) and need
  to measure similarity not by network topology but by the metabolic functions and
  pathway annotations each organism possesses. Use this skill when your research question
  focuses on functional overlap—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3946
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0821
  tools:
  - MetNet
  - Java
  - KEGG
  license_tier: open
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network
- MetNet is a Java tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metnet_cq
    doi: 10.1371/journal.pone.0246962
    title: MetNet
  dedup_kept_from: coll_metnet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0246962
  all_source_dois:
  - 10.1371/journal.pone.0246962
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# functional-level-similarity-index-computation

## Summary

Compute quantitative similarity indexes between two organisms by comparing metabolic pathway annotations and functional assignments at the functional level of their metabolic networks. This produces a scalar or vector of functional similarity scores that quantify how similar the two organisms are in terms of which metabolic functions and pathways they carry out.

## When to use

When you have two metabolic networks (e.g., from KEGG) and need to measure similarity not by network topology but by the metabolic functions and pathway annotations each organism possesses. Use this skill when your research question focuses on functional overlap—e.g., 'Do these two species share the same metabolic capabilities?' rather than 'Do they have the same network structure?'

## When NOT to use

- Input is already a pre-computed similarity matrix or single scalar similarity value—you would be re-computing what is already known.
- The two networks are from the same organism at different time points or conditions; use time-series or condition-comparison methods instead.
- You only have structural network topology (nodes, edges, connectivity) with no functional annotations; functional-level comparison requires explicit pathway and metabolic function metadata.

## Inputs

- KEGG organism codes for two organisms (e.g., 'hsa', 'ptr')
- Metabolic network functional representations (pathway annotations and metabolic function assignments per organism from KEGG)

## Outputs

- Functional-level similarity index scores (scalar or vector of similarity values)
- Structured comparison report showing functional similarities and differences between the two organisms

## How to apply

After loading functional-level metabolic representations (pathway annotations and metabolic function assignments) for both organisms from KEGG using MetNet, extract the functional feature set for each organism—specifically, the set of metabolic functions and pathway annotations assigned to each pathway node. Apply a similarity index (such as set-based or multiset-based comparison) to compute the degree of overlap or distance between these two functional feature sets. The choice between 'set' (ignoring multiplicity) and 'multiset' (preserving multiplicity of functional annotations) depends on whether you want to treat repeated or redundant functional assignments as distinct. Aggregate the functional-level similarity scores and report them alongside any structural-level indexes to provide a comprehensive comparison view.

## Related tools

- **MetNet** (Loads two-level metabolic network representations from KEGG, extracts functional features (pathway annotations and metabolic function assignments), and computes functional-level similarity indexes using user-specified comparison methods ('set' or 'multiset')) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database from which metabolic data and pathway functional annotations are retrieved for both organisms)

## Examples

```
java -jar MetNet.jar hsa ptr multiset
```

## Evaluation signals

- Functional similarity scores fall within the expected range (e.g., 0–1 for normalized indexes) and are comparable in magnitude to structural-level scores from the same organism pair.
- The functional index correctly reflects known biological relationships: organisms with similar metabolic capabilities (e.g., two human pathogens) score higher than phylogenetically distant organisms with divergent metabolism.
- The choice of comparison method ('set' vs. 'multiset') produces interpretable differences; 'multiset' should yield equal or higher scores than 'set' if functional annotations are redundant.
- Output report is structured and includes both the raw similarity index values and a qualitative summary of which functional pathways/metabolic functions are shared versus divergent.
- Re-running the computation with the same organism pair and comparison method produces identical or negligibly different scores (reproducibility check).

## Limitations

- Functional similarity depends entirely on the completeness and accuracy of KEGG pathway annotations; missing or incorrectly annotated pathways will bias results.
- The method does not account for the activity level, expression, or flux rate of metabolic functions—only presence or absence of annotations.
- Comparison results are sensitive to the choice of comparison method ('set' vs. 'multiset'); the README does not provide detailed guidance on when each is appropriate.
- Organisms not present in the KEGG database or with incomplete metabolic pathway annotations cannot be compared.

## Evidence

- [intro] Two-level comparison and functional similarity index definition: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [other] Functional feature extraction step: "Extract functional features (pathway annotations, metabolic functions) from each organism's functional representation"
- [other] Functional similarity index computation method: "Compute functional-level similarity indexes by comparing metabolic function assignments and pathway annotations between the two organisms"
- [intro] Similarity index support for both levels: "The approach is supported by similarity indexes for the comparisons at both levels"
- [readme] Comparison method options and invocation: "comparison method: "set" or "multiset""
- [readme] Two-level representation and comprehensive output: "The comparison results are composed and presented to offer a comprehensive view of the similarities/differences of the two organisms"
