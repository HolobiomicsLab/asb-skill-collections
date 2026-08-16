---
name: structural-level-pathway-topology-modeling
description: Use when when you need to compare metabolic network architecture between
  two organisms and want to analyze their topological properties (e.g., network connectivity,
  reaction ordering, pathway structure) separately from functional annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0621
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

# structural-level-pathway-topology-modeling

## Summary

Reconstruct and represent metabolic networks at the structural level by retrieving pathway and reaction data from KEGG and automatically building metabolic network topology for comparative analysis across organisms. This level of representation captures the topological organization of metabolic reactions independent of functional annotation.

## When to use

When you need to compare metabolic network architecture between two organisms and want to analyze their topological properties (e.g., network connectivity, reaction ordering, pathway structure) separately from functional annotations. Use this skill as the first stage of a two-level metabolic network comparison when structural differences (e.g., missing reactions, alternative pathways) are relevant to your research question on drug engineering or medical science applications.

## When NOT to use

- When you need to analyze metabolic function assignments or pathway roles—use the functional-level representation instead
- When input organisms are not available in KEGG or organism codes are invalid
- When you require pathway-level annotations or enzyme classification data beyond topological connectivity

## Inputs

- KEGG organism identifiers (e.g., 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes)
- KEGG metabolic pathway and reaction data retrieved via KEGG API or database query
- Configuration file (organismList.txt) containing available KEGG organism codes

## Outputs

- Metabolic network topology representation for organism 1 (structural level)
- Metabolic network topology representation for organism 2 (structural level)
- Network graph objects or serialized formats suitable for topology analysis and structural comparison

## How to apply

Load the KEGG organism identifiers for your two selected organisms from the organism list. Query the KEGG database to retrieve metabolic pathway and reaction data for each organism. Execute MetNet with the retrieved KEGG data to automatically reconstruct the metabolic network topology, representing the structural organization of reactions and their connectivity. The structural representation focuses on network graph properties (nodes as metabolites/reactions, edges as reaction relationships) without functional layer mapping. Export the resulting topology representation for each organism in a format suitable for graph analysis and comparison using structural similarity indexes.

## Related tools

- **MetNet** (Java tool that automatically reconstructs metabolic network topology from KEGG data and generates structural-level network representations for comparison) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database from which metabolic pathway and reaction data are retrieved for the two organisms being compared)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Both organisms produce valid network topology representations with non-zero node (metabolite/reaction) and edge (reaction relationship) counts
- Network topology can be successfully parsed and rendered as a directed acyclic graph or reaction network structure
- Structural similarity indexes can be computed at the topology level (e.g., comparing network motifs, node degree distributions, or reaction pathway ordering) between the two organisms
- Manual spot-check: known metabolic pathways (e.g., glycolysis, citric acid cycle) are correctly represented in the topology with expected reaction sequences and intermediates

## Limitations

- MetNet depends on the completeness and currency of KEGG data; missing or outdated pathway annotations in KEGG will propagate to the reconstructed topology
- Structural topology does not capture enzymatic regulation, cofactor requirements, or reaction reversibility—these require the functional-level representation
- Comparison results are sensitive to the choice of organisms and configuration in pathwayList.txt; custom pathway subsets may not be representative of whole-cell metabolism

## Evidence

- [other] MetNet automatically reconstructs the metabolic network topology (structural level) for each organism: "Execute MetNet (Java tool) with the retrieved KEGG data to automatically reconstruct the metabolic network topology (structural level) for each organism."
- [intro] Structural level represents metabolic network topology: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [intro] KEGG is the source for metabolic data retrieval: "their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built"
- [readme] MetNet is a Java tool for automatic network reconstruction: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [other] Query KEGG for metabolic pathway and reaction data: "Query KEGG database to retrieve metabolic pathway and reaction data for each of the two organisms."
