---
name: metabolic-function-classification
description: Use when when you have reconstructed metabolic networks from two or more organisms in KEGG and need to compare them not only in terms of reaction topology but also in terms of which metabolic functions (e.g., glycolysis, citric acid cycle) are present and how they differ.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0621
  tools:
  - MetNet
  - Java
  - KEGG
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network
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

# Reconstruct the two-level (structural + functional) representation of a reconstructed metabolic network

## Summary

Construct a dual-layer representation of metabolic networks that encodes both structural topology (nodes as metabolites, edges as reactions) and functional pathway information (pathway-to-function mappings), enabling quantitative and visual comparison of metabolic capabilities across organisms.

## When to use

When you have reconstructed metabolic networks from two or more organisms in KEGG and need to compare them not only in terms of reaction topology but also in terms of which metabolic functions (e.g., glycolysis, citric acid cycle) are present and how they differ. This skill is essential when the research question involves detecting metabolic pathway differences for drug engineering or understanding species-specific metabolic capabilities.

## When NOT to use

- Input organisms are not available in KEGG, or their metabolic data are incomplete or not curated.
- The research question focuses exclusively on sequence homology or evolutionary distance rather than functional metabolic comparison.
- Networks have already been manually curated or experimentally validated to a level where KEGG's automated reconstruction would introduce noise or conflict.

## Inputs

- KEGG organism codes (e.g., 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes)
- KEGG reaction and metabolite data for selected organisms
- KEGG pathway definitions and functional classifications
- Configuration files (organismList.txt, pathwayList.txt)

## Outputs

- Structural-level network representation (metabolite nodes, reaction edges)
- Functional-level network representation (pathway-to-function mappings)
- Similarity indexes at structural level
- Similarity indexes at functional level
- Comparative visualization of network topology and functional differences

## How to apply

First, retrieve metabolic data for each organism from KEGG using MetNet's data parser. Parse KEGG reactions and metabolites into a directed graph representation to form the structural level, where metabolites are nodes and enzymatic reactions are directed edges; this encodes network topology. Then, assign each KEGG pathway to its corresponding metabolic function and map these functional classifications to the structural nodes and edges to form the functional level. Export both levels to structured formats (e.g., adjacency matrices, annotation tables) that support dual-level similarity indexing. Calculate similarity scores at the structural level (e.g., graph isomorphism or topological metrics) and at the functional level (e.g., pathway presence/absence or functional coverage) to enable comprehensive comparison.

## Related tools

- **MetNet** (Java tool that automatically reconstructs metabolic networks from KEGG, builds both structural and functional representations, and computes similarity indexes for dual-level network comparison) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database for metabolic data (reactions, metabolites, pathways, functional classifications) and organism selection)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Structural representation is a valid directed graph with metabolites as nodes and enzymatic reactions as edges, with consistent edge and node counts matching KEGG data.
- Functional representation correctly maps all retrieved KEGG pathways to metabolites and reactions in the structural graph, with no orphaned pathway assignments.
- Similarity indexes at both levels are computed and comparable between organism pairs; structural similarity reflects network topology differences, and functional similarity reflects pathway content differences.
- Visual output shows no topological inconsistencies (e.g., disconnected components that should be connected, or cycles where linear pathways are expected).
- Comparison results for two known organisms (e.g., Homo sapiens vs. Pan troglodytes) align with known metabolic similarities and differences in the literature (e.g., shared central carbon metabolism but potentially different drug-metabolizing pathways).

## Limitations

- MetNet relies on KEGG's automated curation; organisms with incomplete or poorly annotated metabolic data in KEGG will produce incomplete or biased representations.
- The two-level representation assumes that KEGG's functional classifications (pathway-to-function mappings) are complete and accurate; novel or unannotated metabolic functions will not be captured.
- Similarity indexes are dependent on the choice of comparison method ('set' vs. 'multiset') and may not fully capture biological significance of pathway presence/absence differences.
- The tool requires configuration files (organismList.txt, pathwayList.txt) to be manually maintained; outdated lists may exclude newly sequenced organisms or newly discovered pathways.

## Evidence

- [intro] MetNet constructs a two-level representation with structural and functional levels: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [other] Structural level represents metabolites as nodes and reactions as edges: "Build the structural level: represent nodes as metabolites and edges as enzymatic reactions, encoding network topology."
- [other] Functional level maps pathways to functions: "Build the functional level: assign each pathway to its corresponding metabolic function and map functions to the structural nodes and edges."
- [readme] MetNet retrieves data from KEGG and supports automated network reconstruction: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [readme] Similarity indexes support comparisons at both structural and functional levels: "The approach is supported by similarity indexes for the comparisons at both levels."
- [readme] Application to drug engineering and medical science: "Metabolic pathway comparison and interaction between different species can detect important information for drug engineering and medical science."
